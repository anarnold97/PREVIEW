#!/usr/bin/env python3
"""
Check that TOC (table of contents) nesting in openshift-docs topic map does not
exceed level 3 (CQA requirement: no more than 3 levels).

Reads _topic_maps/_topic_map.yml. Optional path argument limits the check to a
specific branch (e.g. virt, backup_and_restore, backup_and_restore/application_backup_and_restore).
If no path is given, runs on the directory where the script lives and its logical
branch in the topic map (inferred from script location), or the whole map if not
under a known branch.

Usage:
  python check_toc_level.py [PATH]
  python check_toc_level.py virt
  python check_toc_level.py backup_and_restore
  python check_toc_level.py backup_and_restore/application_backup_and_restore

Exit code: 0 if all checked branches have TOC depth <= 3; 1 if any exceed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


# Default topic map path relative to repo root
TOPIC_MAP_REL = "_topic_maps/_topic_map.yml"
MAX_TOC_LEVEL = 3  # CQA: no greater than level 3 (0-based depths 0..3 allowed)


def find_repo_root(start: Path) -> Path | None:
    """Find repo root by looking for _topic_maps directory."""
    current = start.resolve()
    for _ in range(30):
        if (current / "_topic_maps").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def load_topic_map_documents(topic_map_path: Path) -> list[dict]:
    """Load all YAML documents from the topic map file (documents separated by ---)."""
    try:
        text = topic_map_path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"Error: could not read topic map: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        import yaml
    except ImportError:
        print("Error: PyYAML is required. Install with: pip install pyaml", file=sys.stderr)
        sys.exit(2)

    documents = []
    for raw in text.split("\n---"):
        block = raw.strip()
        if not block or block.startswith("#"):
            continue
        try:
            doc = yaml.safe_load(block)
            if doc and isinstance(doc, dict):
                documents.append(doc)
        except yaml.YAMLError as e:
            print(f"Warning: skipped malformed YAML block: {e}", file=sys.stderr)
    return documents


def get_topic_entries(node: dict) -> list[dict]:
    """Return the Topics list from a record or topic group node."""
    topics = node.get("Topics")
    if topics is None:
        return []
    if not isinstance(topics, list):
        return []
    return topics


def path_matches_filter(record_dir: str, path_filter: list[str] | None) -> bool:
    """True if this top-level record should be included given path_filter."""
    if not path_filter:
        return True
    return path_filter[0] == record_dir


def get_subtree_for_path(record: dict, path_segments: list[str]) -> dict | None:
    """
    From a top-level record, descend by path segments (Dir names).
    Returns the topic group node at that path, or None if not found.
    """
    if not path_segments:
        return record
    current = record
    for segment in path_segments:
        topics = get_topic_entries(current)
        found = None
        for item in topics:
            if isinstance(item, dict) and item.get("Dir") == segment:
                found = item
                break
        if found is None:
            return None
        current = found
    return current


def check_toc_depth(
    node: dict,
    depth: int,
    path_from_root: list[str],
    violations: list[tuple[int, list[str], str]],
    max_allowed: int = MAX_TOC_LEVEL,
) -> None:
    """
    Recursively check TOC depth. Records any (depth, path, name) where depth > max_allowed.
    path_from_root is the list of Dir/Name segments from root to this node.
    """
    if depth > max_allowed:
        name = node.get("Name", "(unnamed)")
        violations.append((depth, list(path_from_root), name))

    topics = get_topic_entries(node)
    for item in topics:
        if not isinstance(item, dict):
            continue
        name = item.get("Name", "")
        dir_name = item.get("Dir", "")
        segment = dir_name or name or "(entry)"
        child_path = path_from_root + [segment]
        # This entry is at depth; if it has Topics, those children are at depth+1
        check_toc_depth(item, depth + 1, child_path, violations, max_allowed)


def run_checks(
    topic_map_path: Path,
    path_filter: list[str] | None,
    max_allowed: int = MAX_TOC_LEVEL,
) -> list[tuple[int, list[str], str]]:
    """
    Load topic map, optionally filter to path_filter, and collect all violations.
    Returns list of (depth, path_segments, name) for each node that exceeds max_allowed.
    """
    records = load_topic_map_documents(topic_map_path)
    violations: list[tuple[int, list[str], str]] = []

    for rec in records:
        if not isinstance(rec, dict):
            continue
        rec_dir = rec.get("Dir") or ""
        if not rec_dir:
            continue
        if path_filter and path_filter[0] != rec_dir:
            continue

        if path_filter and len(path_filter) > 1:
            root = get_subtree_for_path(rec, path_filter[1:])
            if root is None:
                continue
            path_prefix = path_filter
        else:
            root = rec
            path_prefix = [rec_dir]

        # Root of this branch is at depth 0; its Topics entries are at depth 1
        check_toc_depth(root, 1, path_prefix, violations, max_allowed)

    return violations


def default_path_from_script_location(script_path: Path, repo_root: Path) -> list[str] | None:
    """
    If the script lives under virt/ or backup_and_restore/, return the path segment(s)
    for that branch so we check only that branch by default. Otherwise return None (check all).
    """
    try:
        rel = script_path.parent.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    if parts[0] == "virt":
        return ["virt"]
    if parts[0] == "backup_and_restore":
        if len(parts) >= 2 and parts[1] == "application_backup_and_restore":
            return ["backup_and_restore", "application_backup_and_restore"]
        return ["backup_and_restore"]
    return None


def path_segments_from_cwd(cwd: Path, repo_root: Path) -> list[str] | None:
    """
    If cwd is under virt/ or backup_and_restore/, return path segment(s) for that branch.
    Used when script is run with no PATH argument from a subdirectory.
    """
    try:
        rel = cwd.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    if parts[0] == "virt":
        return ["virt"]
    if parts[0] == "backup_and_restore":
        if len(parts) >= 2 and parts[1] == "application_backup_and_restore":
            return ["backup_and_restore", "application_backup_and_restore"]
        return ["backup_and_restore"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TOC depth in _topic_maps/_topic_map.yml (max level 3).",
        epilog="PATH can be 'virt', 'backup_and_restore', or 'backup_and_restore/application_backup_and_restore'.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Limit check to this branch (e.g. virt, backup_and_restore/application_backup_and_restore). "
        "If omitted, uses script location to infer branch or checks entire map.",
    )
    parser.add_argument(
        "--topic-map",
        type=Path,
        default=None,
        help="Path to topic map YAML (default: repo_root/_topic_maps/_topic_map.yml)",
    )
    parser.add_argument(
        "--max-level",
        type=int,
        default=MAX_TOC_LEVEL,
        metavar="N",
        help=f"Maximum allowed TOC level (default: {MAX_TOC_LEVEL})",
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
        print("Error: could not find repo root (directory containing _topic_maps)", file=sys.stderr)
        return 2

    topic_map_path = args.topic_map or (repo_root / TOPIC_MAP_REL)
    if not topic_map_path.is_file():
        print(f"Error: topic map not found: {topic_map_path}", file=sys.stderr)
        return 2

    path_filter: list[str] | None
    if args.path is not None:
        path_filter = [p.strip() for p in args.path.split("/") if p.strip()]
    else:
        # Prefer script location, then cwd, then check entire map
        path_filter = default_path_from_script_location(Path(__file__).resolve(), repo_root)
        if path_filter is None:
            path_filter = path_segments_from_cwd(Path.cwd(), repo_root)

    violations = run_checks(topic_map_path, path_filter, max_allowed=args.max_level)

    if not args.quiet:
        scope = "/".join(path_filter) if path_filter else "entire topic map"
        print(f"TOC level check (max level {args.max_level}) for: {scope}")
        print(f"Topic map: {topic_map_path}")
        if not violations:
            print("OK: No TOC nesting exceeds level 3.")
        else:
            print(f"\nFound {len(violations)} node(s) with TOC level > {args.max_level}:\n")
            for depth, path_segments, name in sorted(violations, key=lambda v: (v[1], v[2])):
                path_str = " / ".join(path_segments)
                print(f"  Level {depth}: {path_str}")
                print(f"    Name: {name}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
