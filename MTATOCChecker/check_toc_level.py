#!/usr/bin/env python3
"""
Check that TOC (table of contents) nesting in MTA documentation does not
exceed the configured level (default 3), as required by CQA for docs.redhat.com.

Walks master.adoc files under docs/, resolves include:: directives (topics/, assemblies/),
and reports any heading that would appear in the TOC at a depth greater than :toclevels:.

Usage:
  python check_toc_level.py
  python check_toc_level.py docs/cli-guide
  python check_toc_level.py docs/web-console-guide/master.adoc

Exit code: 0 if all checked content has TOC depth <= max; 1 if any exceed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_TOC_LEVEL_DEFAULT = 3  # CQA: no greater than level 3
DOCS_DIR = "docs"
ASSEMBLIES_DIR = "assemblies"
TOPICS_DIR = "topics"
DOCUMENT_ATTRIBUTES = "docs/topics/templates/document-attributes.adoc"
MASTER_GLOB = "**/master.adoc"


def find_repo_root(start: Path) -> Path | None:
    """Find repo root: directory containing both docs and assemblies."""
    current = start.resolve()
    for _ in range(30):
        if (current / DOCS_DIR).is_dir() and (current / ASSEMBLIES_DIR).is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def resolve_include_path(repo_root: Path, inc_path: str, from_file: Path) -> Path | None:
    """Resolve include path (e.g. topics/foo.adoc, assemblies/bar.adoc) to absolute path."""
    path = inc_path.strip()
    if not path:
        return None
    # Try repo root first (topics/ and assemblies/ as used in masters)
    candidate = repo_root / path
    if candidate.is_file():
        return candidate
    # topics/ may live under docs/
    if path.startswith("topics/"):
        candidate = repo_root / DOCS_DIR / path
        if candidate.is_file():
            return candidate
    return None


def get_toclevels_from_attributes(repo_root: Path) -> int:
    """Read :toclevels: from document-attributes.adoc; default MAX_TOC_LEVEL_DEFAULT."""
    for base in (repo_root, repo_root / DOCS_DIR):
        attrs = base / DOCUMENT_ATTRIBUTES.lstrip("docs/") if DOCS_DIR in DOCUMENT_ATTRIBUTES else base / "topics/templates/document-attributes.adoc"
        if not attrs.is_file():
            attrs = base / "docs/topics/templates/document-attributes.adoc"
        if attrs.is_file():
            try:
                text = attrs.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for line in text.splitlines():
                m = re.match(r":toclevels:\s*(\d+)", line.strip())
                if m:
                    return int(m.group(1))
    return MAX_TOC_LEVEL_DEFAULT


def get_toclevels_from_master(content: str, default: int) -> int:
    """Parse :toclevels: from master/adoc content; return default if not set."""
    for line in content.splitlines():
        m = re.match(r":toclevels:\s*(\d+)", line.strip())
        if m:
            return int(m.group(1))
    return default


def extract_includes(content: str) -> list[tuple[str, int]]:
    """Return list of (include_path, leveloffset). Skips // commented lines."""
    out = []
    for line in content.splitlines():
        if line.strip().startswith("//"):
            continue
        # include::path[leveloffset=+N] or include::path[]
        m = re.search(r"include::([^\]\[]+)\[(.*?)\]", line)
        if not m:
            continue
        path = m.group(1).strip()
        opts = (m.group(2) or "").strip()
        offset = 0
        for part in re.split(r"[, \t]+", opts):
            if part.startswith("leveloffset="):
                val = part.split("=", 1)[1].strip()
                if val.startswith("+") and val[1:].isdigit():
                    offset = int(val[1:])
                elif val.startswith("-") and val[1:].isdigit():
                    offset = -int(val[1:])
                elif val.isdigit():
                    offset = int(val)
                break
        out.append((path, offset))
    return out


def extract_headings(content: str) -> list[tuple[int, int, str]]:
    """Return list of (line_number, level, title) for each = heading. level = number of =."""
    out = []
    for i, line in enumerate(content.splitlines(), start=1):
        m = re.match(r"^(=+)\s+(.+)$", line.strip())
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            out.append((i, level, title))
    return out


def check_file(
    repo_root: Path,
    file_path: Path,
    level_offset: int,
    max_level: int,
    default_toclevels: int,
    visited: set[Path],
    violations: list[tuple[Path, int, int, str, int]],
) -> None:
    """Recursively check a single .adoc file and its includes; append violations."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if file_path in visited:
        return
    visited.add(file_path)
    # Master files can override :toclevels:
    if "master.adoc" in file_path.name:
        max_level = get_toclevels_from_master(content, default_toclevels)
    for ln, h_level, title in extract_headings(content):
        effective = h_level + level_offset
        if effective > max_level:
            violations.append((file_path, ln, effective, title, max_level))
    for inc_path, offset in extract_includes(content):
        resolved = resolve_include_path(repo_root, inc_path, file_path)
        if resolved is not None:
            check_file(
                repo_root,
                resolved,
                level_offset + offset,
                max_level,
                default_toclevels,
                visited,
                violations,
            )
    visited.discard(file_path)


def find_master_files(repo_root: Path, path_arg: str | None) -> list[Path]:
    """Return list of master.adoc files to check. path_arg can be a dir or a single master.adoc."""
    if path_arg is None:
        docs = repo_root / DOCS_DIR
        return sorted(docs.rglob("master.adoc"))
    p = (repo_root / path_arg).resolve()
    if not p.exists():
        return []
    if p.is_file():
        return [p] if "master.adoc" in p.name else []
    return sorted(p.rglob("master.adoc"))


def run_checks(
    repo_root: Path,
    path_arg: str | None,
    max_level_override: int | None,
) -> list[tuple[Path, int, int, str, int]]:
    """Run TOC level checks; return list of (file, line, effective_level, title, max_allowed)."""
    default_toclevels = get_toclevels_from_attributes(repo_root)
    max_level = max_level_override if max_level_override is not None else default_toclevels
    masters = find_master_files(repo_root, path_arg)
    violations: list[tuple[Path, int, int, str, int]] = []
    visited: set[Path] = set()
    for master in masters:
        try:
            initial_content = master.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_max = get_toclevels_from_master(initial_content, default_toclevels)
        if max_level_override is not None:
            file_max = max_level_override
        check_file(
            repo_root,
            master,
            level_offset=0,
            max_level=file_max,
            default_toclevels=default_toclevels,
            visited=visited,
            violations=violations,
        )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TOC depth in MTA documentation master.adoc and includes (max level 3 by default).",
        epilog="PATH can be a directory (e.g. docs/cli-guide) or a single master.adoc. If omitted, all docs/*/master.adoc are checked.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Limit check to this directory or master.adoc file. Default: all docs.",
    )
    parser.add_argument(
        "--max-level",
        type=int,
        default=None,
        metavar="N",
        help=f"Maximum allowed TOC level (default: from document-attributes or {MAX_TOC_LEVEL_DEFAULT})",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only exit code; no summary output",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    if repo_root is None:
        print("Error: could not find repo root (directory containing docs/ and assemblies/)", file=sys.stderr)
        return 2

    violations = run_checks(repo_root, args.path, args.max_level)

    if not args.quiet:
        scope = args.path or "all docs"
        print(f"TOC level check for: {scope}")
        print(f"Repo root: {repo_root}")
        default_toc = get_toclevels_from_attributes(repo_root)
        print(f"Max TOC level: from document-attributes or override ({default_toc})")
        if not violations:
            print("OK: No TOC nesting exceeds the configured level.")
        else:
            print(f"\nFound {len(violations)} heading(s) with TOC level exceeding the maximum:\n")
            for file_path, line_no, effective, title, max_allowed in sorted(
                violations, key=lambda v: (str(v[0]), v[1])
            ):
                try:
                    rel = file_path.relative_to(repo_root)
                except ValueError:
                    rel = file_path
                print(f"  {rel}:{line_no}  level {effective} (max {max_allowed})")
                print(f"    {title[:70]}{'...' if len(title) > 70 else ''}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
