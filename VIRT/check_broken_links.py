#!/usr/bin/env python3
"""
Check for broken links, xrefs, and includes in openshift-docs virt AsciiDoc files.

Usage:
  python check_broken_links.py [--repo-root DIR] [--check-urls] [--validate-against URL] [PATH]

  PATH: Directory to scan (default: virt/). Can be the full virt/ directory
        or a subdirectory (e.g. virt/about_virt, virt/nodes).

  --repo-root DIR:       Repository root (default: auto-detect).
  --check-urls:          Validate external link: URLs (HEAD request).
  --validate-against URL: Validate xrefs against published docs (e.g. https://docs.okd.io/latest).
                         Resolves each xref to the published page URL and checks it with HTTP.
  --no-xref:             Skip xref validation.
  --no-include:          Skip include:: validation.

When --validate-against is set, xrefs are checked against the live site (recommended for virt:
  --validate-against https://docs.okd.io/latest). Without it, xrefs are checked locally (file
exists and [id="..."] anchor in source), which can yield false positives due to build-generated IDs.

Examples:
  python check_broken_links.py virt/about_virt
  python check_broken_links.py --validate-against https://docs.okd.io/latest virt/about_virt
  python check_broken_links.py --check-urls virt/about_virt
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import urllib.request
    import urllib.error
    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False

# Regex for xref:path#anchor[ or xref:path[ (path may contain #anchor)
XREF_RE = re.compile(r'xref:([^\[]+?)(?:\[|$)')
# Regex for link:url[ (url can be http/https)
LINK_RE = re.compile(r'link:(https?://[^\[]+?)(?:\[|$)')
# Regex for include::path[
INCLUDE_RE = re.compile(r'include::([^\[]+?)\[')

# In AsciiDoc, [id="foo"] or [id='foo'] - also id may be at start of line
ID_RE = re.compile(r'\[id=["\']([^"\']+)["\']\]')
CONTEXT_RE = re.compile(r'^:context:\s*(\S+)', re.MULTILINE)


def find_repo_root(start: Path) -> Path:
    """Find repo root (directory containing e.g. modules/, _attributes/).
    Prefer the topmost such directory so we get the real repo root even when
    virt/modules is a symlink to ../modules/.
    """
    current = start.resolve()
    found = None
    for _ in range(20):
        if (current / "modules").exists() or (current / "_attributes").exists():
            found = current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return found if found is not None else start.resolve()


def get_adoc_files(root: Path, scan_path: Path) -> list[Path]:
    """Return all .adoc files under scan_path, with paths relative to root for resolution."""
    if not scan_path.is_dir():
        return []
    files = []
    for p in scan_path.rglob("*.adoc"):
        if p.is_file():
            files.append(p)
    return sorted(files)


def resolve_path(from_file: Path, raw_path: str, repo_root: Path) -> Path | None:
    """Resolve a relative path from the file's directory or repo root. Returns absolute Path or None."""
    from_dir = from_file.parent
    # Normalize: remove leading ./
    raw = raw_path.strip().split("[")[0].strip()
    if not raw:
        return None
    # Try relative to current file
    candidate = (from_dir / raw).resolve()
    if candidate.is_file():
        return candidate
    # Try relative to repo root (for modules/, _attributes/, snippets/)
    candidate = (repo_root / raw).resolve()
    if candidate.is_file():
        return candidate
    # File not found
    return None


def get_ids_and_context(content: str) -> tuple[set[str], str | None]:
    """Extract all [id="..."] values and :context: attribute. Expand {context} in ids if present."""
    ids = set()
    for m in ID_RE.finditer(content):
        ids.add(m.group(1))
    ctx_match = CONTEXT_RE.search(content)
    context = ctx_match.group(1).strip() if ctx_match else None
    # If we have context, add resolved ids for [id="something_{context}"]
    if context:
        for i in list(ids):
            if "{context}" in i:
                ids.add(i.replace("{context}", context))
    return ids, context


def check_xref(
    from_file: Path,
    target_path: str,
    anchor: str | None,
    repo_root: Path,
) -> tuple[bool, str]:
    """Check xref target file exists and anchor exists if present. Returns (ok, message)."""
    path_part = target_path.split("#")[0].strip()
    anchor_part = target_path.split("#", 1)[1].strip() if "#" in target_path else None
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return False, f"target file not found: {path_part}"
    try:
        content = resolved.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"cannot read file: {e}"
    ids, _ = get_ids_and_context(content)
    if anchor_part:
        if anchor_part in ids:
            return True, "ok"
        # Allow anchor to match without context expansion in target (e.g. target has {context})
        for aid in ids:
            if aid.replace("{context}", "").rstrip("_") == anchor_part.rstrip("_"):
                return True, "ok"
        try:
            rel = resolved.relative_to(repo_root)
        except ValueError:
            rel = resolved
        return False, f"anchor '{anchor_part}' not found in {rel} (ids: {sorted(ids)[:5]}...)"
    return True, "ok"


def check_include(from_file: Path, raw_path: str, repo_root: Path) -> tuple[bool, str]:
    """Check include target file exists. Returns (ok, message)."""
    path_part = raw_path.strip().split("[")[0].strip()
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return False, f"included file not found: {path_part}"
    return True, "ok"


def check_url(url: str, timeout: int = 15, method: str = "HEAD") -> tuple[bool, str]:
    """HEAD or GET request to check URL. Returns (ok, message)."""
    if not URLLIB_AVAILABLE:
        return True, "url check skipped (no urllib)"
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "openshift-docs-link-check/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, "ok"
            return False, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def _docs_root_for_path(abs_path: Path) -> Path | None:
    """Find the docs repo root (directory that contains 'virt/') by walking up from abs_path."""
    current = abs_path.resolve()
    for _ in range(30):
        if (current / "virt").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def resolve_xref_to_repo_relative(from_file: Path, target_path: str, repo_root: Path) -> tuple[str | None, str | None]:
    """Resolve xref target to repo-relative path and optional anchor.
    Returns (path_with_forward_slashes, anchor) or (None, None) if target file not found.
    Uses the directory containing 'virt/' as the docs root for the relative path so published
    URLs are correct (e.g. virt/about_virt/... not Documents/.../openshift-docs/virt/...).
    """
    path_part = target_path.split("#")[0].strip()
    anchor_part = target_path.split("#", 1)[1].strip() if "#" in target_path else None
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return None, anchor_part
    # Use docs root (directory containing virt/) for URL-safe relative path
    docs_root = _docs_root_for_path(resolved)
    if docs_root is None:
        try:
            rel = resolved.relative_to(repo_root)
        except ValueError:
            return None, anchor_part
    else:
        try:
            rel = resolved.relative_to(docs_root)
        except ValueError:
            return None, anchor_part
    return str(rel).replace("\\", "/"), anchor_part


def xref_to_published_url(repo_rel_path: str, anchor: str | None, base_url: str) -> str:
    """Build published docs URL from repo-relative .adoc path and optional anchor.
    base_url should not have a trailing slash (e.g. https://docs.okd.io/latest).
    """
    base = base_url.rstrip("/")
    # AsciiDoc builds to .html
    html_path = repo_rel_path.replace(".adoc", ".html") if repo_rel_path.endswith(".adoc") else repo_rel_path
    url = f"{base}/{html_path}"
    if anchor:
        url += "#" + anchor
    return url


def scan_file(
    filepath: Path,
    repo_root: Path,
    check_urls: bool,
    check_xrefs: bool,
    check_includes: bool,
    validate_against_url: str | None = None,
) -> list[dict]:
    """Scan one .adoc file; return list of issue dicts (empty if no issues)."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [{"type": "read_error", "path": str(filepath), "message": str(e)}]
    try:
        rel_path = filepath.relative_to(repo_root)
    except ValueError:
        rel_path = filepath
    issues = []

    if check_xrefs:
        for m in XREF_RE.finditer(content):
            target = m.group(1).strip()
            if validate_against_url:
                # Validate against published docs URL
                repo_rel, anchor = resolve_xref_to_repo_relative(filepath, target, repo_root)
                if repo_rel is None:
                    issues.append({
                        "type": "xref",
                        "path": str(rel_path),
                        "target": target,
                        "message": f"target file not found (cannot resolve for live check): {target.split('#')[0].strip()}",
                    })
                else:
                    pub_url = xref_to_published_url(repo_rel, anchor, validate_against_url)
                    ok, msg = check_url(pub_url, method="GET")
                    if not ok:
                        issues.append({
                            "type": "xref",
                            "path": str(rel_path),
                            "target": target,
                            "message": f"published URL failed: {msg}",
                            "url": pub_url,
                        })
            else:
                # Local file + anchor check
                ok, msg = check_xref(filepath, target, None, repo_root)
                if not ok:
                    issues.append({
                        "type": "xref",
                        "path": str(rel_path),
                        "target": target,
                        "message": msg,
                    })

    if check_includes:
        for m in INCLUDE_RE.finditer(content):
            raw = m.group(1).strip()
            ok, msg = check_include(filepath, raw, repo_root)
            if not ok:
                issues.append({
                    "type": "include",
                    "path": str(rel_path),
                    "target": raw,
                    "message": msg,
                })

    if check_urls:
        for m in LINK_RE.finditer(content):
            url = m.group(1).strip()
            ok, msg = check_url(url)
            if not ok:
                issues.append({
                    "type": "link",
                    "path": str(rel_path),
                    "url": url,
                    "message": msg,
                })

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check for broken links, xrefs, and includes in virt AsciiDoc files.",
        epilog="PATH can be virt/ or a subdirectory (e.g. virt/about_virt).",
    )
    script_dir = Path(__file__).resolve().parent
    default_repo = script_dir.parent if script_dir.name == "virt" else script_dir
    parser.add_argument(
        "path",
        nargs="?",
        default=str(script_dir),
        help="Directory to scan (default: virt/ or script directory)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detect from PATH)",
    )
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Validate external link: URLs (HEAD request)",
    )
    parser.add_argument(
        "--validate-against",
        metavar="URL",
        default=None,
        help="Validate xrefs against published docs (e.g. https://docs.okd.io/latest). Resolves xrefs to published URLs and checks them with HTTP GET.",
    )
    parser.add_argument("--no-xref", action="store_true", help="Skip xref validation")
    parser.add_argument("--no-include", action="store_true", help="Skip include:: validation")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only print summary")
    args = parser.parse_args()

    scan_path = Path(args.path).resolve()
    if not scan_path.exists():
        print(f"Error: path does not exist: {scan_path}", file=sys.stderr)
        return 2
    if not scan_path.is_dir():
        print(f"Error: not a directory: {scan_path}", file=sys.stderr)
        return 2

    repo_root = args.repo_root
    if repo_root is None:
        repo_root = find_repo_root(scan_path)
    else:
        repo_root = repo_root.resolve()
    if not (repo_root / "modules").is_dir() and not (repo_root / "_attributes").is_dir():
        print(f"Warning: repo root may be wrong (no modules/ or _attributes/): {repo_root}", file=sys.stderr)

    adoc_files = get_adoc_files(repo_root, scan_path)
    if not adoc_files:
        print(f"No .adoc files found under {scan_path}", file=sys.stderr)
        return 0

    check_xrefs = not args.no_xref
    check_includes = not args.no_include
    all_issues = []
    for f in adoc_files:
        issues = scan_file(
            f,
            repo_root,
            args.check_urls,
            check_xrefs,
            check_includes,
            validate_against_url=args.validate_against,
        )
        all_issues.extend(issues)

    if not all_issues:
        if not args.quiet:
            try:
                scan_rel = scan_path.relative_to(repo_root)
            except ValueError:
                scan_rel = scan_path
            print(f"Scanned {len(adoc_files)} file(s) under {scan_rel}. No broken links or xrefs found.")
        return 0

    if not args.quiet:
        print(f"Scanned {len(adoc_files)} file(s). Found {len(all_issues)} issue(s):\n")
        for i in all_issues:
            if i["type"] == "xref":
                print(f"  xref   {i['path']}")
                print(f"         -> {i['target']}")
                if i.get("url"):
                    print(f"         URL: {i['url']}")
                print(f"         {i['message']}\n")
            elif i["type"] == "include":
                print(f"  include {i['path']}")
                print(f"         -> {i['target']}")
                print(f"         {i['message']}\n")
            elif i["type"] == "link":
                print(f"  link   {i['path']}")
                print(f"         -> {i['url']}")
                print(f"         {i['message']}\n")
            else:
                print(f"  {i['type']} {i['path']}: {i['message']}\n")
    else:
        print(f"{len(all_issues)} issue(s) in {len(adoc_files)} file(s)")

    return 1


if __name__ == "__main__":
    sys.exit(main())
