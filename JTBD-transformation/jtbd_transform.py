#!/usr/bin/env python3
"""
AsciiDoc to JTBD Transformation Script

Transforms AsciiDoc files to use impersonal, JTBD-like language.
Features: Dry-run with colorized diffs, automatic branching, and staging.
"""

import os
import re
import subprocess
import sys
import argparse
import difflib
from pathlib import Path

# --- Terminal Colors ---
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

def run_command(cmd, cwd=None, capture=True):
    """Run a shell command and return the output."""
    try:
        if capture:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running command: {cmd}{RESET}")
        print(f"Details: {e.stderr if capture else e}")
        sys.exit(1)

def transform_to_jtbd(text):
    """Transform text to impersonal JTBD-like format using regex."""
    replacements = [
        # Questions to statements
        (r'\bHow do I\b', 'How to'),
        (r'\bHow can I\b', 'How to'),
        (r'\bCan I\b', 'Whether to'),
        (r'\bShould I\b', 'Whether to'),
        (r'\bWhat do I need to\b', 'What is needed to'),
        (r'\bWhen should I\b', 'When to'),
        (r'\bWhere do I\b', 'Where to'),
        (r'\bWhy should I\b', 'Why to'),

        # First-person to impersonal
        (r'\bI want to\b', 'To'),
        (r'\bI need to\b', 'To'),
        (r'\bI can\b', 'One can'),
        (r'\bI am\b', 'Users are'),
        (r'\bmy\b', 'the'),
        (r'\bMy\b', 'The'),

        # Make action-oriented
        (r'\bYou can\b', 'To'),
        (r'\bYou should\b', 'To'),
        (r'\bYou need to\b', 'To'),
        (r'\byour\b', 'the'),
        (r'\bYour\b', 'The'),

        # Clean up gerunds (e.g., "To Migrating" -> "Migrating")
        (r'^To ([a-zA-Z]+)ing\b', r'\1ing'),
    ]

    result = text
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # Cleanup double spaces
    return re.sub(r' +', ' ', result).strip()

def transform_asciidoc_file(file_path):
    """Parses AsciiDoc and transforms text while protecting syntax."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    transformed_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        
        # Protect code blocks (---- or ....)
        if stripped.startswith('----') or stripped.startswith('....'):
            in_code_block = not in_code_block
            transformed_lines.append(line)
            continue

        if in_code_block:
            transformed_lines.append(line)
            continue

        # Transform Titles
        if re.match(r'^=+\s+', line):
            markers, title = re.match(r'^(=+)\s+(.+)$', line).groups()
            transformed_lines.append(f"{markers} {transform_to_jtbd(title)}\n")
        
        # Transform Body Text (Skip attributes and block tags)
        elif stripped and not stripped.startswith(':') and not stripped.startswith('['):
            newline = '\n' if line.endswith('\n') else ''
            transformed_lines.append(transform_to_jtbd(line) + newline)
        else:
            transformed_lines.append(line)

    return transformed_lines

def show_color_diff(original, transformed, file_name):
    """Prints a colorized diff to the terminal."""
    use_color = sys.stdout.isatty()
    diff = difflib.unified_diff(original, transformed, fromfile=f'a/{file_name}', tofile=f'b/{file_name}')

    has_changes = False
    for line in diff:
        has_changes = True
        if use_color:
            if line.startswith('+') and not line.startswith('+++'):
                print(f"{GREEN}{line}{RESET}", end="")
            elif line.startswith('-') and not line.startswith('---'):
                print(f"{RED}{line}{RESET}", end="")
            elif line.startswith('@@'):
                print(f"{CYAN}{line}{RESET}", end="")
            else:
                print(line, end="")
        else:
            print(line, end="")
            
    if not has_changes:
        print(f"{CYAN}No changes needed. File is already JTBD-compliant.{RESET}")

def get_repo_root(file_path):
    """Climb tree to find .git directory."""
    current = Path(file_path).resolve().parent
    while current != current.parent:
        if (current / '.git').exists():