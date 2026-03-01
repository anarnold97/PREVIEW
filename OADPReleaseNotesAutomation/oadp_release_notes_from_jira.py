#!/usr/bin/env python3
"""Generate OADP release notes module (.adoc) from a JIRA filter CSV export.

Purpose
-------
Reads a CSV exported from Red Hat JIRA (e.g. from a filter for a given OADP release),
groups issues by type (Bug fix, Enhancement, Known issue), and writes a single AsciiDoc
module suitable for inclusion in the OpenShift docs release notes assembly.

Inputs
------
- VERSION: Release version string (e.g. 1.5.5).
- CSV_PATH: Path to the JIRA CSV. The CSV must include:
  - Issue Key (e.g. OADP-1234)
  - Summary (becomes the release note title)
  - Issue Type (Bug fix | Enhancement | Known issue)
  - Release Note Text: customer-facing body text for each note (basis for Renoa draft).
    If this column is missing, the script falls back to the Description column.

Output
------
A single .adoc file containing:
- A level-1 heading and abstract for the release
- Sections: New features (Enhancements), Resolved issues (Bug fixes), Known issues
- Each issue rendered as a definition list item: title:: body + link to issues.redhat.com

Usage
-----
  1. In JIRA, run a filter that returns issues for the release.
  2. Export results as CSV (include columns: Issue Key, Summary, Issue Type, Release Note Text).
  3. Run:

     python3 oadp_release_notes_from_jira.py 1.5.5 path/to/jira_export.csv

Section mapping (JIRA issue type -> AsciiDoc section)
----------------------------------------------------
  - Bug fix       -> "Resolved issues" (section id: resolved-issues-<version>)
  - Enhancement   -> "New features" (section omitted if there are no enhancements)
  - Known issue   -> "Known issues"
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


# -----------------------------------------------------------------------------
# Column and section mapping (JIRA CSV export column names vary by locale/setup)
# -----------------------------------------------------------------------------

# JIRA issue type (lowercase, as normalized) -> (AsciiDoc section title, id fragment).
# Only these three types are included; other issue types in the CSV are skipped.
TYPE_TO_SECTION = {
    "bug fix": ("Resolved issues", "resolved-issues"),
    "enhancement": ("New features", "new-features"),
    "known issue": ("Known issues", "known-issues"),
}

# Candidate header names for auto-detection (first match wins).
# Add variants here if your JIRA export uses different column labels.
DEFAULT_KEY_COLUMNS = ("Issue Key", "Key", "key")
DEFAULT_SUMMARY_COLUMNS = ("Summary", "summary")
DEFAULT_TYPE_COLUMNS = ("Issue Type", "Issue type", "Type", "type")
# Body text: prefer "Release Note Text" (customer-facing, Renoa draft source); fallback to Description.
DEFAULT_BODY_COLUMNS = ("Release Note Text", "Release note text", "Description", "description")


def normalize_type(raw: str) -> str | None:
    """Normalize JIRA issue type to a key used in TYPE_TO_SECTION.

    Returns the lowercase key if it is one of: bug fix, enhancement, known issue;
    otherwise None (such issues are skipped when grouping).
    """
    if not raw or not raw.strip():
        return None
    key = raw.strip().lower()
    return key if key in TYPE_TO_SECTION else None


def get_column_name(header_keys: dict, candidates: tuple[str, ...]) -> str | None:
    """Find which CSV header matches one of the candidate names (case-insensitive).

    Used to support different JIRA export column names. Returns the first candidate
    that has a matching header, or None if none match.
    """
    for c in candidates:
        for h in header_keys:
            if h and h.strip().lower() == c.lower():
                return h
    return None


def escape_adoc(text: str) -> str:
    """Prepare text for safe use in AsciiDoc (inline).

    Currently only strips surrounding whitespace. Further escaping (e.g. for leading
    dots or square brackets) is applied later where needed (e.g. in build_adoc).
    """
    if not text:
        return ""
    return text.strip()


def format_issue_link(key: str) -> str:
    """Format an AsciiDoc link to the issue on issues.redhat.com.

    Example: OADP-1234 -> link:https://issues.redhat.com/browse/OADP-1234[OADP-1234]
    """
    key = (key or "").strip()
    if not key:
        return ""
    return f"link:https://issues.redhat.com/browse/{key}[{key}]"


def version_to_id(version: str) -> str:
    """Turn a version string into an AsciiDoc-friendly id fragment.

    Dots are not allowed in AsciiDoc ids; we use hyphens instead.
    Example: "1.5.5" -> "1-5-5".
    """
    return version.strip().replace(".", "-")


def read_jira_csv(path: Path) -> list[dict[str, str]]:
    """Read the JIRA CSV and return a list of row dicts.

    - Uses utf-8-sig so a BOM (common in Excel exports) is stripped.
    - Keys and values are stripped of surrounding whitespace for consistent lookups.
    - Rows with empty or missing keys are dropped from each row's dict.
    """
    content = path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(content.splitlines())
    rows = list(reader)
    if not rows:
        return []
    normalized = []
    for row in rows:
        normalized.append({k.strip(): (v or "").strip() for k, v in row.items() if k})
    return normalized


def group_by_type(
    rows: list[dict],
    key_col: str,
    summary_col: str,
    type_col: str,
    body_col: str | None,
) -> dict[str, list[dict]]:
    """Group CSV rows by issue type into the three release-note sections.

    Only rows whose Issue Type is Bug fix, Enhancement, or Known issue are included.
    Each stored item is a dict with:
      - "key": JIRA issue key (e.g. OADP-1234)
      - "summary": title line for the release note
      - "description": body text (from Release Note Text column, or Description fallback)

    Returns a dict with keys "bug fix", "enhancement", "known issue", each holding
    a list of such item dicts.
    """
    grouped: dict[str, list[dict]] = {
        "bug fix": [],
        "enhancement": [],
        "known issue": [],
    }
    for row in rows:
        raw_type = row.get(type_col, "")
        ntype = normalize_type(raw_type)
        if ntype not in grouped:
            continue
        key = row.get(key_col, "").strip()
        summary = row.get(summary_col, "").strip()
        body = (row.get(body_col or "") or "").strip()
        if not key:
            continue
        grouped[ntype].append({"key": key, "summary": summary, "description": body})
    return grouped


def build_adoc(version: str, grouped: dict[str, list[dict]], context: str | None) -> str:
    """Build the complete AsciiDoc module string for the release notes.

    Structure:
      - Comment block for assembly inclusion
      - Content type attribute and document id
      - Level-1 title and abstract
      - For each section (New features, Resolved issues, Known issues):
          - Section id and level-2 heading
          - For each issue: definition list term (summary::), optional body, then link

    context: If None, section ids get suffix "_{context}"; otherwise the given suffix
    (e.g. "ga") is used so the module can be included in different assemblies.
    """
    vid = version_to_id(version)
    context_suffix = "_{context}" if context is None else f"_{context}"

    # --- Document header (metadata, title, abstract) ---
    lines = [
        "// Module included in the following assemblies:",
        "//",
        "// * backup_and_restore/application_backup_and_restore/release-notes/oadp-X-Y-Z-release-notes.adoc",
        "",
        ":_mod-docs-content-type: REFERENCE",
        "",
        f'[id="oadp-{vid}-release-notes{context_suffix}"]',
        f"= OADP {version} release notes",
        "",
        '[role="_abstract"]',
        f"The {{oadp-first}} {version} release notes list new features, resolved issues, and known issues.",
        "",
    ]

    # Order of sections in the output (Enhancements first, then Bug fixes, then Known issues).
    section_order = [
        ("enhancement", "New features", "new-features"),
        ("bug fix", "Resolved issues", "resolved-issues"),
        ("known issue", "Known issues", "known-issues"),
    ]

    for type_key, section_title, section_id in section_order:
        items = grouped.get(type_key, [])
        if not items:
            # Omit "New features" section entirely when there are no enhancements.
            if type_key == "enhancement":
                continue
            # For Bug fix / Known issue, emit an empty section so structure is consistent.
            lines.append(f'[id="{section_id}-{vid}{context_suffix}"]')
            lines.append(f"== {section_title}")
            lines.append("")
            continue

        lines.append(f'[id="{section_id}-{vid}{context_suffix}"]')
        lines.append(f"== {section_title}")
        lines.append("")

        # Each issue: definition list term (title::), optional body from Release Note Text, link.
        for it in items:
            key = it["key"]
            summary = escape_adoc(it["summary"]) or key
            body = escape_adoc(it["description"])
            lines.append(f"{summary}::")
            if body:
                # Body lines: leading "." would start an AsciiDoc block, so escape it.
                for bline in body.splitlines():
                    bline = bline.strip()
                    if bline.startswith("."):
                        bline = "\\" + bline
                    lines.append(bline)
                lines.append("+")  # continuation so the following link stays with the definition
            lines.append("")
            lines.append(format_issue_link(key))
            lines.append("")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def detect_columns(rows: list[dict]) -> tuple[str | None, str | None, str | None, str | None]:
    """Infer CSV column names from the first row's headers.

    Returns (key_col, summary_col, type_col, body_col). Any of these may be None
    if no matching header was found. body_col is used for the release note body
    (Release Note Text or Description).
    """
    if not rows:
        return None, None, None, None
    header_keys = rows[0].keys()
    key_col = get_column_name(header_keys, DEFAULT_KEY_COLUMNS)
    summary_col = get_column_name(header_keys, DEFAULT_SUMMARY_COLUMNS)
    type_col = get_column_name(header_keys, DEFAULT_TYPE_COLUMNS)
    body_col = get_column_name(header_keys, DEFAULT_BODY_COLUMNS)
    return key_col, summary_col, type_col, body_col


def main() -> int:
    """Parse arguments, load CSV, group by type, generate AsciiDoc, and write output."""
    parser = argparse.ArgumentParser(
        description="Generate OADP release notes .adoc from JIRA filter CSV export.",
        epilog="JIRA CSV should include Issue Key, Summary, Issue Type, and Release Note Text (body).",
    )
    parser.add_argument(
        "version",
        metavar="VERSION",
        help="Release version (e.g. 1.5.5)",
    )
    parser.add_argument(
        "csv_path",
        metavar="CSV_PATH",
        type=Path,
        help="Path to JIRA export CSV",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output .adoc path (default: modules/oadp-<version>-release-notes.adoc in repo)",
    )
    parser.add_argument(
        "--context",
        default=None,
        metavar="SUFFIX",
        help="AsciiDoc id suffix: use _{context} when not set (default)",
    )
    parser.add_argument(
        "--key-column",
        default=None,
        help="CSV column for issue key (default: auto-detect)",
    )
    parser.add_argument(
        "--summary-column",
        default=None,
        help="CSV column for summary (default: auto-detect)",
    )
    parser.add_argument(
        "--type-column",
        default=None,
        help="CSV column for issue type (default: auto-detect)",
    )
    parser.add_argument(
        "--body-column",
        default=None,
        help="CSV column for release note body, e.g. Release Note Text (default: auto-detect)",
    )
    args = parser.parse_args()

    # --- Validate version (numeric dots only, e.g. 1.5.5) ---
    version = args.version.strip()
    if not re.match(r"^\d+(\.\d+)*$", version):
        print("Error: version must be numeric (e.g. 1.5.5)", file=sys.stderr)
        return 1

    if not args.csv_path.is_file():
        print(f"Error: CSV file not found: {args.csv_path}", file=sys.stderr)
        return 1

    rows = read_jira_csv(args.csv_path)
    if not rows:
        print("Error: no rows in CSV", file=sys.stderr)
        return 1

    # --- Resolve column names: CLI overrides take precedence, else auto-detect ---
    key_col = args.key_column or detect_columns(rows)[0]
    summary_col = args.summary_column or detect_columns(rows)[1]
    type_col = args.type_column or detect_columns(rows)[2]
    body_col = args.body_column or detect_columns(rows)[3]

    if not key_col or not summary_col or not type_col:
        print("Error: could not detect required columns (Issue Key, Summary, Issue Type).", file=sys.stderr)
        print("Available columns:", list(rows[0].keys()), file=sys.stderr)
        print("Use --key-column, --summary-column, --type-column if names differ.", file=sys.stderr)
        return 1

    grouped = group_by_type(rows, key_col, summary_col, type_col, body_col)
    total = sum(len(g) for g in grouped.values())
    if total == 0:
        print("Error: no rows with Issue Type in: Bug fix, Enhancement, Known issue", file=sys.stderr)
        return 1

    adoc = build_adoc(version, grouped, args.context)

    # --- Output path: explicit -o/--output, or default under repo root ---
    if args.output is not None:
        out_path = args.output
    else:
        # Assumes script lives at .../release-notes/oadp_release_notes_from_jira.py -> parents[3] = repo root
        repo_root = Path(__file__).resolve().parents[3]
        out_path = repo_root / "modules" / f"oadp-{version_to_id(version)}-release-notes.adoc"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(adoc, encoding="utf-8")
    print(f"Wrote {total} issues to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
