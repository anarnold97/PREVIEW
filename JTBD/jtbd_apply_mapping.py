#!/usr/bin/env python3
"""
Apply JTBD (Jobs-to-be-Done) mapping to MTA documentation.
... (docstring remains the same)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Safety check for PyYAML dependency
try:
    import yaml
except ImportError:
    yaml = None

# CQA 2.1 Content Quality Standards for short descriptions
SHORTDESC_MIN = 50
SHORTDESC_MAX = 300

# Regex: Matches the AsciiDoc role attribute for abstracts
RE_ROLE_ABSTRACT = re.compile(r"^\[role=\"_abstract\"\]\s*$", re.MULTILINE)

# Regex: Captures the actual text block (paragraph) following the abstract role
# Uses DOTALL to allow the '.' to match newlines within the paragraph
RE_FIRST_PARAGRAPH = re.compile(
    r"\[role=\"_abstract\"\]\s*\n(.*?)\n\s*\n",
    re.MULTILINE | re.DOTALL,
)

# Constants for the JTBD comment block insertion
JTBD_BLOCK_START = "// JTBD job:"
JTBD_BLOCK_RE = re.compile(
    r"^// JTBD job:.*?(?=^// JTBD job:|\n(?:ifdef::|ifndef::|\[id=)|$)",
    re.MULTILINE | re.DOTALL,
)

def load_mapping(repo: Path) -> dict | None:
    """Safely loads the YAML mapping file from the docs directory."""
    path = repo / "docs" / "jtbd-mapping.yaml"
    if not path.is_file() or not yaml:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_path_to_job(mapping: dict, repo: Path) -> tuple[dict, dict]:
    """
    Parses the YAML structure into two flat dictionaries for fast lookup:
    one for assemblies and one for topics.
    """
    assembly_to_job = {}
    topic_to_job = {}
    for job in mapping.get("jobs", []):
        # Map Assemblies: includes potential metadata overrides (like shortdesc_focus)
        for a in job.get("assemblies", []):
            path = a.get("path") if isinstance(a, dict) else a
            if path:
                key = (repo / path).resolve()
                assembly_to_job[key] = (job, a if isinstance(a, dict) else {})
        # Map Topics: simple path-to-job relationship
        for t in job.get("topics", []):
            key = (repo / t).resolve()
            topic_to_job[key] = (job, {})
    return assembly_to_job, topic_to_job

def job_shortdesc(job: dict, assembly_entry: dict, existing: str | None) -> str | None:
    """
    Logic engine for generating a job-focused short description.
    Priority: 1. Manual Focus -> 2. Job Outcomes -> 3. Statement transformation.
    """
    # 1. Use the explicit override if provided in the YAML
    focus = assembly_entry.get("shortdesc_focus", "").strip()
    if focus:
        if len(focus) > SHORTDESC_MAX:
            focus = focus[: SHORTDESC_MAX - 1].rsplit(maxsplit=1)[0] + "."
        if len(focus) >= SHORTDESC_MIN:
            return focus

    # 2. Derive from 'outcomes' list by combining the first two points
    outcomes = job.get("outcomes", [])
    if outcomes:
        combined = " ".join(outcomes[:2])
        if len(combined) > SHORTDESC_MAX:
            combined = combined[: SHORTDESC_MAX - 1].rsplit(maxsplit=1)[0] + "."
        if len(combined) >= SHORTDESC_MIN:
            return combined

    # 3. Transform the 'so I can' part of a JTBD statement into 'So you can'
    statement = job.get("statement", "")
    if " so I can " in statement:
        part = statement.split(" so I can ", 1)[1].strip().rstrip(".")
        part = "So you can " + part
        if len(part) > SHORTDESC_MAX:
            part = part[: SHORTDESC_MAX - 1].rsplit(maxsplit=1)[0] + "."
        if len(part) >= SHORTDESC_MIN:
            return part

    # Fallback: if no rules match or are too short, do nothing
    return None

def first_paragraph_after_abstract(content: str) -> tuple[str, int, int]:
    """Locates the abstract text and returns the string plus its start/end indexes."""
    m = RE_FIRST_PARAGRAPH.search(content)
    if not m:
        return None, -1, -1
    # Clean up internal newlines for comparison
    para = m.group(1).replace("\n", " ").strip()
    return para, m.start(1), m.end(1)

def ensure_jtbd_comment_block(content: str, job: dict) -> str:
    """
    Injects or updates the internal comment block used for internal tracking.
    Attempts to place it immediately after the content-type attribute.
    """
    # Avoid duplicate insertion if the ID is already present
    if JTBD_BLOCK_START in content and f"// JTBD job: {job.get('id', '')}"