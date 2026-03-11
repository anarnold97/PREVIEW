#!/usr/bin/env python3
"""
Fix TOC depth by creating new modules for content that is too deep. Does NOT change
any leveloffset on existing includes and does NOT change `==` to `=` in place.

Strategy:
- Find modules under documentation/modules/ that have headings at level >= 2 (== or
  deeper) whose effective TOC level (offset + heading_level) exceeds 3.
- For each such module: extract the content from the first violating section to the
  end into a NEW module. The new module gets a document title `=` and keeps `==`
  (and deeper) as-is so effective level in the new module (included at leveloffset=+1)
  is <= 3.
- Trim the original module to end before that section.
- In every assembly that includes the original module, add after that include a new
  line: include::../modules/<new-module>.adoc[leveloffset=+1].

Usage:
  python fix_toc_by_new_modules.py [--dry-run] [path]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOCS_DIR = "documentation"
MODULES_DIR = "documentation/modules"
MAX_TOC_LEVEL = 3


def find_repo_root(start: Path) -> Path | None:
    current = start.resolve()
    for _ in range(30):
        docs = current / DOCS_DIR
        if docs.is_dir() and any(docs.glob("doc-*/master.adoc")):
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def resolve_include_path(repo_root: Path, inc_path: str, from_file: Path) -> Path | None:
    path = inc_path.strip()
    if not path:
        return None
    candidate = (from_file.parent / path).resolve()
    if not candidate.is_file():
        return None
    try:
        candidate.relative_to(repo_root)
    except ValueError:
        return None
    return candidate


def extract_includes(content: str) -> list[tuple[str, int, int]]:
    """Return (include_path, leveloffset, 1-based line_number)."""
    out = []
    for i, line in enumerate(content.splitlines(), start=1):
        if line.strip().startswith("//"):
            continue
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
                elif val.isdigit():
                    offset = int(val)
                break
        out.append((path, offset, i))
    return out


def extract_headings(content: str) -> list[tuple[int, int, str]]:
    """(line_number, level, title)."""
    out = []
    for i, line in enumerate(content.splitlines(), start=1):
        m = re.match(r"^(=+)\s+(.+)$", line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def is_module_path(repo_root: Path, path: Path) -> bool:
    try:
        rel = path.relative_to(repo_root)
        return len(rel.parts) >= 2 and rel.parts[0] == DOCS_DIR and rel.parts[1] == "modules" and path.suffix == ".adoc"
    except ValueError:
        return False


def collect_max_offset_and_includers(
    repo_root: Path,
    masters: list[Path],
) -> tuple[dict[Path, int], dict[Path, list[tuple[Path, int]]]]:
    """Returns (max_offset per file, module_path -> [(assembly_path, line_number)])."""
    max_offset: dict[Path, int] = {}
    includers: dict[Path, list[tuple[Path, int]]] = {}

    def visit(file_path: Path, level_offset: int, visited: set[Path]) -> None:
        key = file_path.resolve()
        max_offset[key] = max(max_offset.get(key, level_offset), level_offset)
        if file_path in visited:
            return
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return
        visited.add(file_path)
        for inc_path, offset, line_num in extract_includes(content):
            resolved = resolve_include_path(repo_root, inc_path, file_path)
            if resolved is not None:
                rkey = resolved.resolve()
                if is_module_path(repo_root, resolved):
                    includers.setdefault(rkey, []).append((file_path.resolve(), line_num))
                visit(resolved, level_offset + offset, visited)
        visited.discard(file_path)

    for master in masters:
        visit(master.resolve(), 0, set())
    return max_offset, includers


def run(
    repo_root: Path,
    path_arg: str | None,
    dry_run: bool,
) -> tuple[int, int]:
    """Returns (new_modules_created, assemblies_updated)."""
    modules_dir = repo_root / MODULES_DIR
    if not modules_dir.is_dir():
        return 0, 0

    if path_arg:
        p = (repo_root / path_arg).resolve()
        if not p.exists():
            return 0, 0
        masters = sorted(p.rglob("master.adoc")) if p.is_dir() else ([p] if p.name == "master.adoc" else [])
    else:
        masters = sorted((repo_root / DOCS_DIR).rglob("master.adoc"))

    max_offset, includers = collect_max_offset_and_includers(repo_root, masters)
    new_count = 0
    asm_updated = 0

    for mod_file in sorted(modules_dir.rglob("*.adoc")):
        try:
            mod_file.relative_to(repo_root)
        except ValueError:
            continue
        if not is_module_path(repo_root, mod_file):
            continue
        mod_key = mod_file.resolve()
        offset = max_offset.get(mod_key, 0)
        max_allowed = max(1, MAX_TOC_LEVEL - offset)
        try:
            content = mod_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        headings = extract_headings(content)
        lines = content.splitlines()
        # Find first heading that violates and is level >= 2 (so we can move it to a new module)
        first_violating_line = None
        for ln, level, _ in headings:
            if level >= 2 and (offset + level) > MAX_TOC_LEVEL:
                first_violating_line = ln
                break
        if first_violating_line is None:
            continue
        # Build new module content: add = title, then from first violating line to end (keep == as ==)
        # Use first violating heading's title as the new module's document title so we have one =
        first_title = None
        for ln, level, title in headings:
            if ln == first_violating_line:
                first_title = title
                break
        if not first_title:
            continue
        # New module: = first_title (so the new doc has one =), then the rest of the content
        # from first_violating_line to end. In that rest, the first line is == Title; we already
        # used that as = so we skip that line and output the rest, OR we output the block as-is
        # and add = first_title at the top. Then the moved content has == and === unchanged.
        # So new module = "= <first_title>\n\n" + content from first_violating_line to end.
        # That would duplicate the first heading (once as = and once as ==). So instead:
        # new module = "= <first_title>\n\n" + content from (first_violating_line + 1) to end,
        # but we need to keep the structure. So we take from first_violating_line to end; the
        # first line is "== Title". In the new module we want = Title and then the rest. So we
        # replace the first "==" with "=" in the extracted block only (that's promoting the
        # first section to doc title in the new file, not "changing == to =" in the original).
        extracted = lines[first_violating_line - 1 :]
        if not extracted:
            continue
        # New module: one = document title (reuse first section title), then rest of extracted content.
        # Skip the first line if it is "== <first_title>" to avoid duplicating the heading.
        new_module_lines = ["= " + first_title, ""]
        for i, line in enumerate(extracted):
            if i == 0 and re.match(r"^==\s+", line.strip()):
                continue
            new_module_lines.append(line)
        new_module_content = "\n".join(new_module_lines)

        base = mod_file.stem
        new_name = base + "-toc-sections.adoc"
        new_path = mod_file.parent / new_name
        if new_path.exists() and not dry_run:
            # avoid overwriting
            continue
        includer_list = includers.get(mod_key, [])
        if not includer_list:
            continue

        if not dry_run:
            new_path.write_text(new_module_content + "\n", encoding="utf-8")
        new_count += 1

        # Trim original: keep lines 1 .. first_violating_line - 1; drop trailing block attributes [id=...] etc.
        trimmed_lines = lines[: first_violating_line - 1]
        while trimmed_lines and re.match(r"^\[[\w-]+=.*\]\s*$", trimmed_lines[-1].strip()):
            trimmed_lines.pop()
        trimmed = "\n".join(trimmed_lines).rstrip() + "\n"
        if not dry_run:
            mod_file.write_text(trimmed, encoding="utf-8")

        # Add include of new module once per assembly (after the first include of the original module)
        seen_asm: set[Path] = set()
        for asm_path, line_num in includer_list:
            if asm_path in seen_asm:
                continue
            seen_asm.add(asm_path)
            try:
                asm_lines = asm_path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            # Insert after line_num (1-based): new line include::../modules/<new_name>[leveloffset=+1]
            insert_line = "include::../modules/" + new_name + "[leveloffset=+1]"
            idx = line_num  # 0-based index for "after this line"
            if idx >= len(asm_lines):
                continue
            new_asm = asm_lines[: idx + 1] + [insert_line, ""] + asm_lines[idx + 1 :]
            if not dry_run:
                asm_path.write_text("\n".join(new_asm) + "\n", encoding="utf-8")
            asm_updated += 1

    return new_count, asm_updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix TOC by creating new modules (no leveloffset change, no == to =).")
    parser.add_argument("path", nargs="?", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    if repo_root is None:
        print("Error: repo root not found.", file=sys.stderr)
        return 2
    n_new, n_asm = run(repo_root, args.path, args.dry_run)
    print(f"New modules created: {n_new}; assembly includes added: {n_asm}")
    if args.dry_run:
        print("(Dry run; no files written.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
