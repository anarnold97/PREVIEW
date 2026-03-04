#!/usr/bin/env python3
"""
Check for broken links in the OADP (OpenShift API for Data Protection) documentation.

Validates links in: openshift-docs/backup_and_restore/application_backup_and_restore/
- xref: targets (internal .adoc; path relative to current file or repo root)
- include:: targets (modules/, _attributes/, snippets/ from repo root)
- link:https?:// (external URLs; optional fetch check)

Comparison: Reports how many links point inside the OADP documentation set vs outside,
and validates that all internal OADP xrefs resolve to existing files with valid anchors.

Usage:
  # From repo root (defaults to OADP book):
  python3 backup_and_restore/application_backup_and_restore/check_links.py

  # From this directory:
  python3 check_links.py

  # Explicit repo root and path:
  python3 check_links.py /path/to/openshift-docs backup_and_restore/application_backup_and_restore

  # With external URL checks and optional published-docs validation:
  python3 check_links.py --check-urls
  python3 check_links.py --validate-against https://docs.redhat.com/en/documentation/.../application_backup_and_restore
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import urllib.request
    import urllib.error
    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False

# OADP book path relative to repo root (used for default and comparison)
OADP_BOOK_REL = "backup_and_restore/application_backup_and_restore"

XREF_RE = re.compile(r"xref:([^\[]+?)(?:\[|$)")
LINK_RE = re.compile(r"link:(https?://[^\[]+?)(?:\[|$)")
INCLUDE_RE = re.compile(r"include::([^\[]+?)\[")
ID_RE = re.compile(r'\[id=["\']([^"\']+)["\']\]')
CONTEXT_RE = re.compile(r"^:context:\s*(\S+)", re.MULTILINE)


def find_repo_root(start: Path) -> Path:
    """Find openshift-docs repo root: directory containing OADP book and modules/ or _attributes/.
    Prefer the closest such directory when walking up from the script (so we get the real repo root).
    """
    current = start.resolve()
    found_any = None
    for _ in range(20):
        has_attrs = (current / "modules").exists() or (current / "_attributes").exists()
        if has_attrs:
            found_any = current
            if (current / OADP_BOOK_REL).exists():
                return current  # return first (closest) root that contains the OADP book
        parent = current.parent
        if parent == current:
            break
        current = parent
    return found_any if found_any is not None else start.resolve()


def get_adoc_files(repo_root: Path, scan_path: Path) -> list[Path]:
    """Return all .adoc files under scan_path."""
    if not scan_path.is_dir():
        return []
    return sorted(p for p in scan_path.rglob("*.adoc") if p.is_file())


def resolve_path(from_file: Path, raw_path: str, repo_root: Path) -> Path | None:
    """Resolve a relative path from the file's directory or repo root."""
    from_dir = from_file.parent
    raw = raw_path.strip().split("[")[0].strip()
    if not raw:
        return None
    candidate = (from_dir / raw).resolve()
    if candidate.is_file():
        return candidate
    candidate = (repo_root / raw).resolve()
    if candidate.is_file():
        return candidate
    return None


def get_ids_and_context(content: str) -> tuple[set[str], str | None]:
    """Extract [id="..."] and :context:; expand {context} in ids."""
    ids = set()
    for m in ID_RE.finditer(content):
        ids.add(m.group(1))
    ctx_match = CONTEXT_RE.search(content)
    context = ctx_match.group(1).strip() if ctx_match else None
    if context:
        for i in list(ids):
            if "{context}" in i:
                ids.add(i.replace("{context}", context))
    return ids, context


def check_xref(
    from_file: Path,
    target_path: str,
    repo_root: Path,
) -> tuple[bool, str, Path | None]:
    """Check xref target file exists and anchor exists if present. Returns (ok, message, resolved_path)."""
    path_part = target_path.split("#")[0].strip()
    anchor_part = target_path.split("#", 1)[1].strip() if "#" in target_path else None
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return False, f"target file not found: {path_part}", None
    try:
        content = resolved.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"cannot read file: {e}", resolved
    ids, _ = get_ids_and_context(content)
    if anchor_part:
        if anchor_part in ids:
            return True, "ok", resolved
        for aid in ids:
            if aid.replace("{context}", "").rstrip("_") == anchor_part.rstrip("_"):
                return True, "ok", resolved
        try:
            rel = resolved.relative_to(repo_root)
        except ValueError:
            rel = resolved
        return False, f"anchor '{anchor_part}' not found in {rel} (ids: {sorted(ids)[:5]}...)", resolved
    return True, "ok", resolved


def check_include(from_file: Path, raw_path: str, repo_root: Path) -> tuple[bool, str]:
    """Check include target exists."""
    path_part = raw_path.strip().split("[")[0].strip()
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return False, f"included file not found: {path_part}"
    return True, "ok"


def check_url(url: str, timeout: int = 15, method: str = "HEAD") -> tuple[bool, str]:
    """HEAD or GET request to check URL."""
    if not URLLIB_AVAILABLE:
        return True, "url check skipped (no urllib)"
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "OpenShift-Docs-OADP-LinkCheck/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, "ok"
            return False, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def resolve_xref_to_repo_relative(
    from_file: Path, target_path: str, repo_root: Path
) -> tuple[str | None, str | None]:
    """Resolve xref to repo-relative path and optional anchor. Returns (path, anchor) or (None, anchor)."""
    path_part = target_path.split("#")[0].strip()
    anchor_part = target_path.split("#", 1)[1].strip() if "#" in target_path else None
    resolved = resolve_path(from_file, path_part, repo_root)
    if resolved is None:
        return None, anchor_part
    try:
        rel = resolved.relative_to(repo_root)
    except ValueError:
        return None, anchor_part
    return str(rel).replace("\\", "/"), anchor_part


def xref_to_published_url(repo_rel_path: str, anchor: str | None, base_url: str) -> str:
    """Build published docs URL from repo-relative .adoc path and optional anchor."""
    base = base_url.rstrip("/")
    html_path = (
        repo_rel_path.replace(".adoc", ".html")
        if repo_rel_path.endswith(".adoc")
        else repo_rel_path
    )
    url = f"{base}/{html_path}"
    if anchor:
        url += "#" + anchor
    return url


def is_under_oadp_book(resolved: Path, repo_root: Path, oadp_book: Path) -> bool:
    """True if resolved path is under the OADP book directory."""
    try:
        rel = resolved.relative_to(repo_root)
        return rel == oadp_book or str(rel).startswith(oadp_book.as_posix() + "/")
    except ValueError:
        return False


def run_checks(
    repo_root: Path,
    book_path: Path,
    check_urls: bool,
    validate_against_url: str | None,
    quiet: bool,
) -> tuple[list[dict], int]:
    """Run all checks. Returns (list of issue dicts, number of adoc files scanned)."""
    adoc_files = get_adoc_files(repo_root, book_path)
    if not adoc_files:
        return [], 0

    oadp_book_rel = Path(OADP_BOOK_REL)
    oadp_book_abs = (repo_root / oadp_book_rel).resolve()
    # Set of repo-relative paths for "OADP documentation" comparison
    oadp_doc_paths = set()
    for p in adoc_files:
        try:
            r = p.relative_to(repo_root)
            oadp_doc_paths.add(str(r).replace("\\", "/"))
        except ValueError:
            pass

    all_issues = []
    stats = {"internal_oadp": 0, "internal_oadp_ok": 0, "internal_external": 0, "internal_external_ok": 0}

    for filepath in adoc_files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            all_issues.append({"type": "read_error", "path": str(filepath), "message": str(e)})
            continue
        try:
            rel_path = filepath.relative_to(repo_root)
        except ValueError:
            rel_path = filepath

        # xrefs
        for m in XREF_RE.finditer(content):
            target = m.group(1).strip()
            if validate_against_url:
                repo_rel, anchor = resolve_xref_to_repo_relative(filepath, target, repo_root)
                if repo_rel is None:
                    all_issues.append({
                        "type": "xref",
                        "path": str(rel_path),
                        "target": target,
                        "message": f"target file not found: {target.split('#')[0].strip()}",
                    })
                else:
                    pub_url = xref_to_published_url(repo_rel, anchor, validate_against_url)
                    ok, msg = check_url(pub_url, method="GET")
                    if not ok:
                        all_issues.append({
                            "type": "xref",
                            "path": str(rel_path),
                            "target": target,
                            "message": f"published URL failed: {msg}",
                            "url": pub_url,
                        })
            else:
                ok, msg, resolved = check_xref(filepath, target, repo_root)
                if resolved is not None and is_under_oadp_book(resolved, repo_root, oadp_book_abs):
                    stats["internal_oadp"] += 1
                    if ok:
                        stats["internal_oadp_ok"] += 1
                elif resolved is not None:
                    stats["internal_external"] += 1
                    if ok:
                        stats["internal_external_ok"] += 1
                if not ok:
                    all_issues.append({
                        "type": "xref",
                        "path": str(rel_path),
                        "target": target,
                        "message": msg,
                    })

        # includes
        for m in INCLUDE_RE.finditer(content):
            raw = m.group(1).strip()
            ok, msg = check_include(filepath, raw, repo_root)
            if not ok:
                all_issues.append({
                    "type": "include",
                    "path": str(rel_path),
                    "target": raw,
                    "message": msg,
                })

        # external links
        if check_urls:
            for m in LINK_RE.finditer(content):
                url = m.group(1).strip()
                ok, msg = check_url(url)
                if not ok:
                    all_issues.append({
                        "type": "link",
                        "path": str(rel_path),
                        "url": url,
                        "message": msg,
                    })

    if not quiet and not validate_against_url and (stats["internal_oadp"] or stats["internal_external"]):
        total_in = stats["internal_oadp_ok"] + stats["internal_oadp"] - stats["internal_oadp_ok"]
        total_out = stats["internal_external_ok"] + stats["internal_external"] - stats["internal_external_ok"]
        print("Comparison with OADP documentation:")
        print(f"  Internal to OADP (within application_backup_and_restore): {stats['internal_oadp_ok']} OK, {stats['internal_oadp'] - stats['internal_oadp_ok']} broken")
        print(f"  External (other books/repo): {stats['internal_external_ok']} OK, {stats['internal_external'] - stats['internal_external_ok']} broken")
        print(f"  OADP doc set: {len(adoc_files)} .adoc file(s)")
        print()

    return all_issues, len(adoc_files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check links in OADP documentation (application_backup_and_restore).",
        epilog="Validates xrefs, include::, and optional link: URLs. Compares links against the OADP doc set.",
    )
    script_dir = Path(__file__).resolve().parent
    repo_root_default = find_repo_root(script_dir)
    default_book = repo_root_default / OADP_BOOK_REL
    if not default_book.exists():
        default_book = script_dir
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=None,
        help=f"Repository root (default: auto-detect). Book path is {OADP_BOOK_REL}.",
    )
    parser.add_argument(
        "book_path",
        nargs="?",
        default=None,
        help=f"Book directory relative to repo root (default: {OADP_BOOK_REL}).",
    )
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Validate external link: URLs (HEAD request).",
    )
    parser.add_argument(
        "--validate-against",
        metavar="URL",
        default=None,
        help="Validate xrefs against published docs (GET request to built HTML).",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Only print issues, no comparison summary.")
    args = parser.parse_args()

    if args.repo_root is not None:
        repo_root = Path(args.repo_root).resolve()
        if args.book_path is not None:
            book_path = Path(args.book_path).resolve()
            if not book_path.is_absolute():
                book_path = (repo_root / args.book_path).resolve()
        else:
            book_path = (repo_root / OADP_BOOK_REL).resolve()
    else:
        repo_root = find_repo_root(script_dir)
        book_path = default_book if default_book.exists() else script_dir

    if not book_path.exists():
        print(f"Directory not found: {book_path}", file=sys.stderr)
        return 2
    if not book_path.is_dir():
        print(f"Not a directory: {book_path}", file=sys.stderr)
        return 2

    if not (repo_root / "modules").is_dir() and not (repo_root / "_attributes").is_dir():
        print(f"Warning: repo root may be wrong (no modules/ or _attributes/): {repo_root}", file=sys.stderr)

    try:
        book_rel = book_path.relative_to(repo_root)
    except ValueError:
        book_rel = book_path
    if not args.quiet:
        print(f"Repo root: {repo_root}")
        print(f"Checking OADP documentation: {book_rel}\n")

    all_issues, num_files = run_checks(
        repo_root,
        book_path,
        check_urls=args.check_urls,
        validate_against_url=args.validate_against,
        quiet=args.quiet,
    )

    if num_files == 0:
        print("No .adoc files found under the book path.", file=sys.stderr)
        return 0

    if not all_issues:
        if not args.quiet:
            print("All links OK (validated against OADP documentation).")
        return 0

    if not args.quiet:
        print(f"Found {len(all_issues)} issue(s):\n")
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
        print(f"{len(all_issues)} issue(s) in {num_files} file(s)")

    return 1


if __name__ == "__main__":
    sys.exit(main())
