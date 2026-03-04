#!/usr/bin/env python3
"""
Check for broken links in MTV (Migration Toolkit for Virtualization) documentation
AsciiDoc (`.adoc`) files. Target repo: forklift-documentation.

- xref: targets (internal .adoc path relative to current file; path-style only)
- include:: targets (modules/, assemblies/ relative to each file's component root)
- link:https?:// (external URLs; optional fetch check)
- MTV documentation comparison: external links to docs.redhat.com/.../migration_toolkit_for_virtualization/
  are checked against the version in modules/common-attributes.adoc (:project-version:).

Usage (script in repo root, run from repo root):
  python3 check_links.py
  python3 check_links.py documentation/doc-Planning_your_migration
  python3 check_links.py documentation/doc-Migrating_your_virtual_machines

Usage (script elsewhere; pass repo root and optional book path):
  python3 check_links.py /path/to/forklift-documentation
  python3 check_links.py /path/to/forklift-documentation documentation/doc-Planning_your_migration
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Pattern for :project-version: in common-attributes.adoc
PROJECT_VERSION_RE = re.compile(r"^:project-version:\s*(\S+)\s*$", re.MULTILINE)
# Pattern for MTV docs base URL; group(1) = version segment
MTV_DOCS_URL_RE = re.compile(
    r"https?://docs\.redhat\.com/en/documentation/migration_toolkit_for_virtualization/([^/#?\s]+)"
)


def find_repo_root(start: Path) -> Path:
    """Find forklift-documentation repo root: directory containing 'documentation'."""
    d = start.resolve()
    for _ in range(15):
        if (d / "documentation").is_dir():
            return d
        parent = d.parent
        if parent == d:
            break
        d = parent
    return start


def find_component_root(adoc_path: Path) -> Path | None:
    """Find the component root for an .adoc file (dir containing assemblies/ or modules/ or master.adoc)."""
    d = adoc_path.parent.resolve()
    for _ in range(15):
        if (d / "assemblies").exists() or (d / "modules").exists() or (d / "master.adoc").exists():
            return d
        parent = d.parent
        if parent == d:
            break
        d = parent
    return None


def get_mtv_version_from_attributes(repo_root: Path) -> str | None:
    """Read :project-version: from common-attributes.adoc. Tries documentation/modules then modules/."""
    for rel in ("documentation/modules/common-attributes.adoc", "modules/common-attributes.adoc"):
        path = repo_root / rel
        if path.exists():
            try:
                text = path.read_text(encoding="utf-8")
                m = PROJECT_VERSION_RE.search(text)
                if m:
                    return m.group(1).strip()
            except Exception:
                pass
    return None


def extract_mtv_version_from_url(url: str) -> str | None:
    """Return the MTV version segment from a docs.redhat.com MTV URL, or None."""
    m = MTV_DOCS_URL_RE.search(url)
    return m.group(1) if m else None


def check_mtv_doc_links_version(
    ext_results: list[tuple[str, str, int | None, str]], expected_version: str
) -> list[tuple[str, str, str]]:
    """From external link results, return (source_file, url, url_version) for links whose MTV version != expected."""
    mismatches = []
    for source, url, _status, _err in ext_results:
        url_ver = extract_mtv_version_from_url(url)
        if url_ver is not None and url_ver != expected_version:
            mismatches.append((source, url, url_ver))
    return mismatches


def extract_xrefs(content: str) -> list[tuple[str, str]]:
    """Return list of (path_relative_to_file, anchor_or_empty). Path-style only (contains .adoc or ../).
    Antora-style xref:ref_component[] are not validated (no file path)."""
    out = []
    # xref: or xref:: ../../path/to/file.adoc#anchor[link text]
    for m in re.finditer(r"xref::?(\.\./)*([^#\[]+)(?:#([^\]]+))?\[", content):
        path = (m.group(1) or "") + m.group(2).strip()
        anchor = m.group(3) or ""
        if ".adoc" in path or path.startswith("../"):
            out.append((path, anchor))
    return out


def extract_includes(content: str) -> list[str]:
    """Return include paths (e.g. modules/foo.adoc, assemblies/bar.adoc). Skips // commented lines."""
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


def check_internal_links(
    repo_root: Path, adoc_files: list[Path]
) -> list[tuple[str, str, str, bool]]:
    """Check xref and include targets. Return (source_file, target_path, anchor, exists).
    Includes are resolved relative to each file's component root (doc-* directory)."""
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
        # includes: paths are relative to component root (e.g. documentation/doc-Planning_your_migration)
        comp_root = find_component_root(adoc)
        for inc in extract_includes(text):
            if comp_root is not None:
                target = (comp_root / inc).resolve()
            else:
                target = repo_root / inc
            exists = target.exists()
            try:
                rel_path = target.relative_to(repo_root)
            except (ValueError, TypeError):
                rel_path = inc
            results.append((adoc.name, str(rel_path), "", exists))
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
                        url, headers={"User-Agent": "MTV-Docs-LinkChecker/1.0"}
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

    # MTV documentation comparison (version from common-attributes.adoc)
    mtv_version = get_mtv_version_from_attributes(repo_root)
    mtv_mismatches: list[tuple[str, str, str]] = []
    if mtv_version is not None:
        mtv_mismatches = check_mtv_doc_links_version(ext, mtv_version)
    mtv_base = (
        f"https://docs.redhat.com/en/documentation/migration_toolkit_for_virtualization/{mtv_version}"
        if mtv_version
        else None
    )
    print("\nMTV documentation comparison:")
    if mtv_version is None:
        print("  (could not read :project-version: from documentation/modules/common-attributes.adoc or modules/common-attributes.adoc; skipping version check)")
    else:
        print(f"  Version from modules/common-attributes.adoc (:project-version:): {mtv_version}")
        print(f"  Base URL: {mtv_base}")
        if mtv_mismatches:
            print(f"  MTV version mismatch ({len(mtv_mismatches)}): links should use {mtv_version}")
            for source, url, url_ver in mtv_mismatches:
                print(f"    {source}: version in URL is {url_ver} -> {url}")
        else:
            print("  All MTV doc links use the current project version.")

    if internal_broken or ext_broken or mtv_mismatches:
        sys.exit(1)
    print("\nAll links OK.")


if __name__ == "__main__":
    main()
