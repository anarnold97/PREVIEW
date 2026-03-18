#!/usr/bin/env python3
"""
MTA TOC Fixer: Creates new modules for content that is too deep.
This script ensures that the Table of Contents (TOC) stays readable by splitting 
long modules into smaller chunks when their effective heading level exceeds 3.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass

# Constants matching Red Hat / MTA documentation standards
DOCS_DIR = "documentation"
MODULES_DIR = "documentation/modules"
MAX_TOC_LEVEL = 3

@dataclass
class MigrationRecord:
    """Data class to store information for the final summary report."""
    original_module: str
    new_module: str
    heading_moved: str
    assemblies_affected: list[str]

def find_repo_root(start: Path) -> Path | None:
    """
    Climbs up the directory tree to find the root of the MTA repository.
    Looks for the 'documentation' folder and common entry point files.
    """
    current = start.resolve()
    for _ in range(30):  # Limit search depth to 30 parents
        docs = current / DOCS_DIR
        # Check for both master.adoc (traditional) and index.adoc (modern MTA)
        if docs.is_dir() and (any(docs.glob("**/master.adoc")) or any(docs.glob("**/index.adoc"))):
            return current
        parent = current.parent
        if parent == current:  # Hit the filesystem root
            break
        current = parent
    return None

def resolve_include_path(repo_root: Path, inc_path: str, from_file: Path) -> Path | None:
    """
    Converts an AsciiDoc include path (e.g., ../modules/file.adoc) 
    into an absolute filesystem path.
    """
    path = inc_path.strip()
    if not path: return None
    candidate = (from_file.parent / path).resolve()
    if not candidate.is_file(): return None
    try:
        # Ensure the file is actually inside the repo to avoid escaping via ../../
        candidate.relative_to(repo_root)
    except ValueError:
        return None
    return candidate

def extract_includes(content: str) -> list[tuple[str, int, int]]:
    """
    Parses a file for 'include::' directives.
    Returns: (path, leveloffset_value, line_number)
    """
    out = []
    for i, line in enumerate(content.splitlines(), start=1):
        if line.strip().startswith("//"): continue  # Ignore commented-out includes