#!/usr/bin/env python3
"""
Check for broken links in OpenShift docs .adoc files (any book):
- xref: targets (internal .adoc files; path relative to current file)
- include:: targets (modules/, _attributes/, etc. from repo root)
- link:https?:// (external URLs; optional fetch check)

Usage:
  # Check vm_networking (when run from repo root or from this script's dir):
  python3 virt/vm_networking/check_links.py

  # Check any book: pass repo root and the book directory (relative or absolute):
  python3 virt/vm_networking/check_links.py /path/to/openshift-docs virt/vm_networking
  python3 virt/vm_networking/check_links.py /path/to/openshift-docs applications/creating_applications
"""

import re
import sys
import urllib.request
from pathlib import Path


def find_repo_root(book_dir: Path) -> Path:
    """Find openshift-docs repo root by walking up until _attributes exists as a real dir (not a symlink)."""
    d = book_dir.resolve()
    for _ in range(10):  # avoid infinite loop
        attrs = d / "_attributes"
        if attrs.exists() and attrs.is_dir() and not attrs.is_symlink():
            return d
        parent = d.parent
        if parent == d:
            break
        d = parent
    return book_dir  # fallback


def extract_xrefs(content: str) -> list[tuple[str, str]]:
    """Return list of (path_relative_to_file, anchor_or_empty). Path includes ../ and .adoc."""
    out = []
    # xref:../../path/to/file.adoc#anchor[link text] or xref:../../path.adoc[text]
    for m in re.finditer(r"xref::(\.\./)*([^#\[]+)(?:#([^\]]+))?\[", content):
        path = (m.group(1) or "") + m.group(2).strip()
        anchor = m.group(3) or ""
        out.append((path, anchor))
    return out


def extract_includes(content: str) -> list[str]:
    """Return include paths (e.g. modules/foo.adoc)."""
    out = []
    for m in re.finditer(r"include::([^\]\[]+)\[\]", content):
        out.append(m.group(1).strip())
    return out


def extract_external_links(content: str) -> list[str]:
    """Return link:https?://... URLs (up to ])."""
    out = []
    for m in re.finditer(r"link:(https?://[^\]]+)\[", content):
        out.append(m.group(1))
    return out


def check_internal_links(repo_root: Path, book_dir: Path) -> list[tuple[str, str, str, bool]]:
    """Check xref and include targets. Return (source_file, target_path, anchor, exists)."""
    results = []
    for adoc in sorted(book_dir.glob("*.adoc")):
        text = adoc.read_text(encoding="utf-8")
        # xrefs: path is relative to current file's directory
        for path, anchor in extract_xrefs(text):
            # Resolve relative to the .adoc file's parent
            target_file = (adoc.parent / path).resolve()
            try:
                rel_path = target_file.relative_to(repo_root)
            except ValueError:
                rel_path = path
            exists = target_file.exists()
            results.append((adoc.name, str(rel_path), anchor, exists))
        # includes: paths are relative to repo root (Antora convention)
        for inc in extract_includes(text):
            target = repo_root / inc
            exists = target.exists()
            results.append((adoc.name, inc, "", exists))
    return results


def check_external_links(book_dir: Path, fetch: bool = True) -> list[tuple[str, str, int | None, str]]:
    """Return (source_file, url, status_code_or_None, error_message)."""
    results = []
    for adoc in sorted(book_dir.glob("*.adoc")):
        text = adoc.read_text(encoding="utf-8")
        for url in extract_external_links(text):
            status = None
            err = ""
            if fetch:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "OpenShift-Docs-LinkChecker/1.0"})
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
    if len(sys.argv) >= 3:
        repo_root = Path(sys.argv[1]).resolve()
        book_dir = Path(sys.argv[2]).resolve()
        if not book_dir.is_absolute():
            book_dir = (repo_root / sys.argv[2]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        repo_root = find_repo_root(script_dir)
        book_dir = script_dir
    if not book_dir.exists():
        print(f"Directory not found: {book_dir}", file=sys.stderr)
        sys.exit(1)
    print(f"Repo root: {repo_root}")
    print(f"Checking: {book_dir}\n")

    # Internal (xref + include)
    internal_broken = []
    for source, target, anchor, exists in check_internal_links(repo_root, book_dir):
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
    ext = check_external_links(book_dir, fetch=True)
    ext_broken = False
    for source, url, status, err in ext:
        if status is None:
            print(f"  FAIL  {source}: {url}")
            print(f"        {err}")
            ext_broken = True
        elif status >= 400:
            print(f"  {status}  {source}: {url}")
            ext_broken = True
        else:
            print(f"  OK    {source}: {url}")

    if internal_broken or ext_broken:
        sys.exit(1)
    print("\nAll links OK.")


if __name__ == "__main__":
    main()
