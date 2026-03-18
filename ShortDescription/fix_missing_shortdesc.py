#!/usr/bin/env python3
"""
Apply CQA 2.1 shortdesc fixes: add missing [role="_abstract"] or adjust length.
Discovers all .adoc files missing a shortdesc, derives one from the title (or uses
shortdesc_overrides.csv), and fixes too-long / too-short abstracts. Use --dry-run
to preview. Optional: run after cqa_jtbd_validate.py to fix reported failures.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

# Regex to match AsciiDoc level-1 title (e.g. "= My Title")
RE_TITLE = re.compile(r"^=+\s+(.+)$", re.MULTILINE)
# Regex to find the [role="_abstract"] block that wraps the short description
RE_ROLE_ABSTRACT = re.compile(r"^\[role=\"_abstract\"\]\s*$", re.MULTILINE)
# CQA 2.1 shortdesc length constraints (characters)
SHORTDESC_MIN, SHORTDESC_MAX = 50, 300
# Default suffix used to reach minimum length when deriving or expanding shortdesc
DEFAULT_SUFFIX = " Use this when writing or matching rules."
# Name of optional override file in repo root: path,shortdesc (CSV)
OVERRIDES_FILENAME = "shortdesc_overrides.csv"


def load_shortdesc_overrides(repo: Path) -> dict[str, str]:
    """Load path -> shortdesc from repo/shortdesc_overrides.csv if present."""
    overrides = {}
    path = repo / OVERRIDES_FILENAME
    if not path.is_file():
        return overrides
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 2:
                overrides[row[0].strip()] = row[1].strip()
    return overrides


def derive_shortdesc_from_title(title: str) -> str:
    """
    Build a CQA-compliant shortdesc from the topic title.
    Ensures length is between SHORTDESC_MIN and SHORTDESC_MAX.
    """
    raw = title.strip()
    if not raw:
        raw = "This topic."
    # Prefer sentence form: add period if missing, then append default suffix
    base = raw if raw.endswith(".") else f"{raw}."
    candidate = (base + DEFAULT_SUFFIX).strip()
    if len(candidate) <= SHORTDESC_MAX:
        return candidate if len(candidate) >= SHORTDESC_MIN else (candidate + DEFAULT_SUFFIX)[:SHORTDESC_MAX]
    # Too long: truncate at word boundary (leave room for "…")
    truncated = base[: SHORTDESC_MAX - 1].rsplit(maxsplit=1)[0]
    result = truncated + "…" if len(truncated) < len(base) else truncated
    if len(result) < SHORTDESC_MIN:
        result = (result + DEFAULT_SUFFIX)[:SHORTDESC_MAX]
    return result


def first_paragraph_after_abstract(content: str) -> tuple[str, int, int]:
    """Return (first_paragraph, start, end) after [role="_abstract"]."""
    m = RE_ROLE_ABSTRACT.search(content)
    if not m:
        return None, -1, -1
    # Paragraph runs from after the role line until the next blank line
    start = m.end()
    end = content.find("\n\n", start)
    if end == -1:
        end = len(content)
    # Normalize newlines to spaces for a single-line paragraph string
    para = content[start:end].replace("\n", " ").strip()
    return para, start, end

def add_abstract(content: str, title: str, shortdesc: str) -> str:
    """Insert [role="_abstract"] and shortdesc after first = title (and :context: if present)."""
    lines = content.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if re.match(r"^=+\s+", line):
            # After = title, preserve blank lines, :attribute: lines, and // comments
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if next_line.strip() == "" or next_line.strip().startswith(":") or next_line.strip().startswith("//"):
                    out.append(next_line)
                    i += 1
                else:
                    break
            # Insert abstract block: blank line, role, shortdesc (capped), blank line
            out.append("")
            out.append('[role="_abstract"]')
            out.append(shortdesc[:SHORTDESC_MAX])
            out.append("")
            continue
        i += 1
    return "\n".join(out)

def shorten_paragraph(para: str, max_len: int = 297) -> str:
    """Truncate at word boundary; append ellipsis if text was cut."""
    if len(para) <= max_len:
        return para
    # Drop the last (partial) word to avoid mid-word cut
    truncated = para[:max_len].rsplit(maxsplit=1)[0]
    return truncated + "…" if len(truncated) < len(para) else truncated

def fix_file(path: Path, repo: Path, dry_run: bool, missing_shortdescs: dict) -> bool:
    """Apply fixes for one file (add abstract, shorten, or expand). Return True if file was modified."""
    content = path.read_text(encoding="utf-8")
    modified = False
    try:
        rel = path.relative_to(repo).as_posix()
    except ValueError:
        rel = path.as_posix()

    # Case 1: File has no abstract and is in the known list — add [role="_abstract"] and shortdesc
    if not RE_ROLE_ABSTRACT.search(content) and rel in missing_shortdescs:
        shortdesc = missing_shortdescs[rel]
        title_m = RE_TITLE.search(content)
        if title_m and shortdesc:
            new_content = add_abstract(content, title_m.group(1), shortdesc)
            if new_content != content:
                if not dry_run:
                    path.write_text(new_content, encoding="utf-8")
                modified = True

    # Case 2: Abstract exists but is too long — truncate at word boundary
    para, start, end = first_paragraph_after_abstract(content)
    if para and len(para) > SHORTDESC_MAX:
        new_para = shorten_paragraph(para, SHORTDESC_MAX)
        if new_para != para:
            new_content = content[:start] + new_para + content[end:]
            if not dry_run:
                path.write_text(new_content, encoding="utf-8")
            modified = True

    # Case 3: Abstract exists but is too short — append generic suffix up to SHORTDESC_MAX
    if para and len(para) < SHORTDESC_MIN:
        new_para = (para + DEFAULT_SUFFIX)[:SHORTDESC_MAX]
        if len(new_para) >= SHORTDESC_MIN:
            new_content = content[:start] + new_para + content[end:]
            if not dry_run:
                path.write_text(new_content, encoding="utf-8")
            modified = True

    return modified


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix CQA 2.1 shortdesc: add missing [role=\"_abstract\"] or adjust length."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    parser.add_argument(
        "repo",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent.parent,
        help="Repository root containing .adoc files (default: parent of script directory)",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir():
        print("Error: repo is not a directory:", repo, file=sys.stderr)
        return 1

    overrides = load_shortdesc_overrides(repo)

    # Build map of relative path -> shortdesc for every file missing [role="_abstract"]
    missing_shortdescs: dict[str, str] = {}
    for path in repo.rglob("*.adoc"):
        if "website" in path.parts:
            continue
        try:
            rel = path.relative_to(repo).as_posix()
        except ValueError:
            continue
        content = path.read_text(encoding="utf-8")
        if RE_ROLE_ABSTRACT.search(content):
            continue
        # Use override if present, otherwise derive from title
        title_m = RE_TITLE.search(content)
        title = (title_m.group(1).strip()) if title_m else "This topic"
        missing_shortdescs[rel] = overrides.get(rel) or derive_shortdesc_from_title(title)

    fixed = 0
    # First pass: add missing abstracts
    for rel in missing_shortdescs:
        path = repo / rel
        if path.is_file() and fix_file(path, repo, args.dry_run, missing_shortdescs):
            fixed += 1
            print("Fixed:", rel)

    # Second pass: fix length (too long or too short) for files that already have an abstract
    for path in repo.rglob("*.adoc"):
        if "website" in path.parts:
            continue
        try:
            rel = path.relative_to(repo).as_posix()
        except ValueError:
            continue
        if rel in missing_shortdescs:
            continue
        content = path.read_text(encoding="utf-8")
        para, start, end = first_paragraph_after_abstract(content)
        if not para:
            continue
        if len(para) > SHORTDESC_MAX:
            new_para = shorten_paragraph(para, SHORTDESC_MAX)
            if new_para != para:
                new_content = content[:start] + new_para + content[end:]
                if not args.dry_run:
                    path.write_text(new_content, encoding="utf-8")
                fixed += 1
                print("Shortened:", rel)
        elif len(para) < SHORTDESC_MIN:
            new_para = (para + DEFAULT_SUFFIX)[:SHORTDESC_MAX]
            if len(new_para) >= SHORTDESC_MIN:
                new_content = content[:start] + new_para + content[end:]
                if not args.dry_run:
                    path.write_text(new_content, encoding="utf-8")
                fixed += 1
                print("Expanded:", rel)

    print("Total changes:", fixed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
