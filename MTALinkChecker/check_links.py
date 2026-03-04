#!/usr/bin/env python3
"""
Check for broken links in MTA documentation AsciiDoc (`.adoc`) files.
Place this script in the mta-documentation repo root and run it from there.

- xref: targets (internal .adoc path relative to current file; path-style only)
- include:: targets (topics/, assemblies/ etc. from repo root)
- link:https?:// (external URLs; optional fetch check)
- MTA doc links: link: URLs to docs.redhat.com/.../migration_toolkit_for_applications/...
  are checked against the latest MTA docs version (from the live site or
  docs/topics/templates/document-attributes.adoc).

Usage (script in repo root, run from repo root):
  python3 check_links.py
  python3 check_links.py docs/install-guide
  python3 check_links.py docs/topics/mta-ui

Usage (script elsewhere; pass repo root and optional book path):
  python3 check_links.py /path/to/mta-documentation
  python3 check_links.py /path/to/mta-documentation docs/install-guide
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Base URL for MTA documentation (no version segment)
MTA_DOCS_BASE = "https://docs.redhat.com/en/documentation/migration_toolkit_for_applications"


def find_repo_root(start: Path) -> Path:
    """Find mta-documentation repo root: directory containing both docs and assemblies."""
    d = start.resolve()
    for _ in range(15):
        if (d / "docs").exists() and (d / "assemblies").exists():
            return d
        parent = d.parent
        if parent == d:
            break
        d = parent
    return start


def extract_xrefs(content: str) -> list[tuple[str, str]]:
    """Return list of (path_relative_to_file, anchor_or_empty). Path-style only (contains .adoc or ../).
    Antora-style xref:ref_component[] are not validated (no file path)."""
    out = []
    # xref: or xref:: ../../path/to/file.adoc#anchor[link text]
    for m in re.finditer(r"xref::?(\.\./)*([^#\[]+)(?:#([^\]]+))?\[", content):
        path = (m.group(1) or "") + m.group(2).strip()
        anchor = m.group(3) or ""
        # Only path-style xrefs: has .adoc or starts with ../
        if ".adoc" in path or path.startswith("../"):
            out.append((path, anchor))
    return out


def extract_includes(content: str) -> list[str]:
    """Return include paths (e.g. topics/foo.adoc, assemblies/bar.adoc). Skips // commented lines."""
    out = []
    for line in content.splitlines():
        if line.strip().startswith("//"):
            continue
        for m in re.finditer(r"include::([^\]\[]+)\[\]", line):
            out.append(m.group(1).strip())
    return out


def extract_external_links(content: str) -> list[str]:
    """Return link:https?://... URLs (up to ])."""
    out = []
    for m in re.finditer(r"link:(https?://[^\]]+)\[", content):
        out.append(m.group(1))
    return out


def get_mta_version_from_attributes(repo_root: Path) -> str | None:
    """Read DocInfoProductNumber for MTA from topics/templates/document-attributes.adoc.
    Returns the version string (e.g. '8.0') or None if not found."""
    attrs_path = repo_root / "docs" / "topics" / "templates" / "document-attributes.adoc"
    if not attrs_path.exists():
        attrs_path = repo_root / "topics" / "templates" / "document-attributes.adoc"
    if not attrs_path.exists():
        return None
    try:
        text = attrs_path.read_text(encoding="utf-8")
    except Exception:
        return None
    in_mta = False
    for line in text.splitlines():
        line = line.strip()
        if line == "ifdef::mta[]":
            in_mta = True
            continue
        if line == "endif::[]":
            in_mta = False
            continue
        if in_mta and line.startswith(":DocInfoProductNumber:"):
            val = line.split(":", 2)[-1].strip()
            if val:
                return val
    return None


def get_mta_version_from_web() -> str | None:
    """Fetch MTA docs landing page and parse the latest version (e.g. from title).
    Returns version string (e.g. '8.0') or None on failure."""
    try:
        req = urllib.request.Request(
            f"{MTA_DOCS_BASE}/",
            headers={"User-Agent": "MTA-Docs-LinkChecker/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    # Match title like "Migration Toolkit for Applications | 8.0 | Red Hat"
    m = re.search(r"Migration Toolkit for Applications\s*\|\s*(\d+\.\d+)", html, re.I)
    if m:
        return m.group(1)
    # Fallback: first path segment that looks like a version (e.g. 8.0 in the URL)
    m = re.search(r"migration_toolkit_for_applications/(\d+\.\d+)/", html)
    if m:
        return m.group(1)
    return None


def extract_mta_doc_links(content: str) -> list[str]:
    """Return list of link: URLs that point to MTA documentation on docs.redhat.com."""
    out = []
    for m in re.finditer(r"link:(https?://[^\]]+)\[", content):
        url = m.group(1)
        if "docs.redhat.com" in url and "migration_toolkit_for_applications" in url:
            out.append(url)
    return out


def normalize_mta_doc_url(url: str, version: str) -> str:
    """Replace the version segment in an MTA docs URL with the given version."""
    # .../migration_toolkit_for_applications/8.0/... or .../7.3/...
    return re.sub(
        r"(migration_toolkit_for_applications/)(?:\d+\.\d+)(/)",
        r"\g<1>" + version + r"\2",
        url,
        count=1,
    )


def check_mta_doc_links(
    repo_root: Path,
    adoc_files: list[Path],
    fetch: bool = True,
) -> list[tuple[str, str, str, int | None, str]]:
    """Validate links to MTA documentation. Use latest version (web or document-attributes).
    Returns (source_file, original_url, normalized_url, status_code_or_None, error_message)."""
    version = get_mta_version_from_web()
    if version is None:
        version = get_mta_version_from_attributes(repo_root)
    if version is None:
        version = "8.0"
    results = []
    seen: set[tuple[str, str]] = set()
    for adoc in sorted(adoc_files):
        try:
            text = adoc.read_text(encoding="utf-8")
        except Exception:
            continue
        for url in extract_mta_doc_links(text):
            normalized = normalize_mta_doc_url(url, version)
            key = (adoc.name, normalized)
            if key in seen:
                continue
            seen.add(key)
            status = None
            err = ""
            if fetch:
                try:
                    req = urllib.request.Request(
                        normalized,
                        headers={"User-Agent": "MTA-Docs-LinkChecker/1.0"},
                        method="HEAD",
                    )
                    with urllib.request.urlopen(req, timeout=15) as r:
                        status = r.status
                except urllib.error.HTTPError as e:
                    status = e.code
                    err = str(e)
                except Exception as e:
                    err = str(e)
            results.append((adoc.name, url, normalized, status, err))
    return results


def check_internal_links(
    repo_root: Path, adoc_files: list[Path]
) -> list[tuple[str, str, str, bool]]:
    """Check xref and include targets. Return (source_file, target_path, anchor, exists)."""
    results = []
    for adoc in sorted(adoc_files):
        try:
            text = adoc.read_text(encoding="utf-8")
        except Exception:
            continue
        # xrefs: path is relative to current file's directory
        for path, anchor in extract_xrefs(text):
            target_file = (adoc.parent / path).resolve()
            try:
                rel_path = target_file.relative_to(repo_root)
            except ValueError:
                rel_path = path
            exists = target_file.exists()
            results.append((adoc.name, str(rel_path), anchor, exists))
        # includes: paths are relative to repo root (topics/, assemblies/)
        for inc in extract_includes(text):
            target = repo_root / inc
            exists = target.exists()
            results.append((adoc.name, inc, "", exists))
    return results


def check_external_links(
    adoc_files: list[Path], fetch: bool = True
) -> list[tuple[str, str, int | None, str]]:
    """Return (source_file, url, status_code_or_None, error_message)."""
    results = []
    for adoc in sorted(adoc_files):
        try:
            text = adoc.read_text(encoding="utf-8")
        except Exception:
            continue
        for url in extract_external_links(text):
            status = None
            err = ""
            if fetch:
                try:
                    req = urllib.request.Request(
                        url, headers={"User-Agent": "MTA-Docs-LinkChecker/1.0"}
                    )
                    with urllib.request.urlopen(req, timeout=15) as r:
                        status = r.status
                except urllib.error.HTTPError as e:
                    status = e.code
                    err = str(e)
                except Exception as e:
                    err = str(e)
            results.append((adoc.name, url, status, err))
    return results


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    if len(sys.argv) >= 3:
        repo_root = Path(sys.argv[1]).resolve()
        book_path = sys.argv[2]
        book_dir = (repo_root / book_path).resolve() if not Path(book_path).is_absolute() else Path(book_path).resolve()
    elif len(sys.argv) == 2:
        repo_root = find_repo_root(script_dir)
        book_dir = (repo_root / sys.argv[1]).resolve()
    else:
        repo_root = find_repo_root(script_dir)
        book_dir = repo_root

    if not repo_root.exists():
        print(f"Repo root not found: {repo_root}", file=sys.stderr)
        sys.exit(1)
    if not book_dir.exists():
        print(f"Directory not found: {book_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect .adoc files: recursive under book_dir
    adoc_files = list(book_dir.rglob("*.adoc"))
    if not adoc_files:
        print(f"No .adoc files under {book_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Repo root: {repo_root}")
    print(f"Checking: {book_dir} ({len(adoc_files)} .adoc files)\n")

    # Internal (xref + include)
    internal_broken = []
    for source, target, anchor, exists in check_internal_links(repo_root, adoc_files):
        if not exists:
            internal_broken.append((source, target, anchor))

    if internal_broken:
        print(f"Broken internal links ({len(internal_broken)}):")
        for source, target, anchor in internal_broken:
            print(f"  {source} -> {target}" + (f"#{anchor}" if anchor else ""))
    else:
        print("Internal links: all OK")

    # External (fetch)
    print("\nExternal links:")
    ext = check_external_links(adoc_files, fetch=True)
    ext_broken = False
    for source, url, status, err in ext:
        if status is None:
            print(f"  FAIL {source}: {url}")
            print(f"    {err}")
            ext_broken = True
        elif status >= 400:
            print(f"  {status} {source}: {url}")
            ext_broken = True
        else:
            print(f"  OK {source}: {url}")

    # MTA documentation links (validate against latest version at docs.redhat.com)
    mta_version = get_mta_version_from_web()
    if mta_version is None:
        mta_version = get_mta_version_from_attributes(repo_root) or "8.0"
    print(f"\nMTA documentation links (checked against {MTA_DOCS_BASE}/{mta_version}):")
    mta_results = check_mta_doc_links(repo_root, adoc_files, fetch=True)
    mta_broken = False
    for source, orig_url, normalized_url, status, err in mta_results:
        if status is None:
            print(f"  FAIL {source}: {orig_url}")
            print(f"    {err}")
            mta_broken = True
        elif status >= 400:
            print(f"  {status} {source}: {normalized_url}")
            mta_broken = True
        else:
            print(f"  OK {source}: {normalized_url}")

    if internal_broken or ext_broken or mta_broken:
        sys.exit(1)
    print("\nAll links OK.")


if __name__ == "__main__":
    main()
