#!/usr/bin/env python3
"""
AsciiDoc to JTBD Transformation Script

This script transforms AsciiDoc files to use impersonal, JTBD-like language.
It creates a new branch, updates the file, and stages it for review.
"""

import os
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, capture=True):
    """Run a shell command and return the output."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr if capture else e}")
        sys.exit(1)


def transform_to_jtbd(text):
    """
    Transform text to task-oriented JTBD-like format.

    Converts:
    - Questions to task statements
    - Make text more action-oriented
    - Keep pronouns but focus on tasks
    """
    # Task-oriented transformations (keeping pronouns)
    replacements = [
        # Questions to task statements (keep pronouns where natural)
        (r'\bHow do I\b', 'How to'),
        (r'\bHow can I\b', 'How to'),
        (r'\bHow do you\b', 'How to'),
        (r'\bHow can you\b', 'How to'),

        # Direct task statements - remove filler words
        (r'\bYou can use\b', 'Use'),
        (r'\bYou can migrate\b', 'Migrate'),
        (r'\bYou can configure\b', 'Configure'),
        (r'\bYou can create\b', 'Create'),
        (r'\bYou can add\b', 'Add'),
        (r'\bYou can set\b', 'Set'),
        (r'\bYou can install\b', 'Install'),
        (r'\bYou can perform\b', 'Perform'),

        # Keep "you" in descriptive/benefit statements but make more direct
        # (These patterns are more conservative)
    ]

    result = text
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    # Clean up double spaces (but preserve newlines)
    result = re.sub(r' +', ' ', result)

    return result


def transform_asciidoc_title(line):
    """Transform an AsciiDoc title line to JTBD format."""
    # Match AsciiDoc title markers (=, ==, ===, etc.)
    match = re.match(r'^(=+)\s+(.+)$', line)
    if match:
        markers, title = match.groups()
        transformed_title = transform_to_jtbd(title)
        return f"{markers} {transformed_title}"
    return line


def transform_asciidoc_file(file_path):
    """
    Transform an entire AsciiDoc file to JTBD format.
    Returns the transformed content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    transformed_lines = []
    in_code_block = False
    in_admonition_block = False

    for line in lines:
        # Track code blocks to avoid transforming them
        if line.strip().startswith('----') or line.strip().startswith('....'):
            in_code_block = not in_code_block
            transformed_lines.append(line)
            continue

        if in_code_block:
            transformed_lines.append(line)
            continue

        # Track admonition blocks (====)
        if line.strip() == '====':
            in_admonition_block = not in_admonition_block
            transformed_lines.append(line)
            continue

        if in_admonition_block:
            transformed_lines.append(line)
            continue

        # Preserve blank lines
        if not line.strip():
            transformed_lines.append(line)
            continue

        # Preserve comments (lines starting with //)
        if line.strip().startswith('//'):
            transformed_lines.append(line)
            continue

        # Preserve include statements
        if line.strip().startswith('include::'):
            transformed_lines.append(line)
            continue

        # Preserve ifdef/ifndef/endif conditionals
        if line.strip().startswith(('ifdef::', 'ifndef::', 'endif::')):
            transformed_lines.append(line)
            continue

        # Preserve admonition headers [NOTE], [IMPORTANT], etc.
        if re.match(r'^\[(NOTE|IMPORTANT|WARNING|TIP|CAUTION)\]', line.strip()):
            transformed_lines.append(line)
            continue

        # Transform titles
        if re.match(r'^=+\s+', line):
            transformed_lines.append(transform_asciidoc_title(line))
        # Transform regular text (but preserve attributes, etc.)
        elif not line.strip().startswith(':') and not line.strip().startswith('['):
            transformed_lines.append(transform_to_jtbd(line))
        else:
            transformed_lines.append(line)

    return ''.join(transformed_lines)


def get_repo_root(file_path):
    """Find the git repository root for the given file."""
    current = Path(file_path).resolve().parent
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent
    print("Error: Not in a git repository")
    sys.exit(1)


def main():
    print("=== AsciiDoc to JTBD Transformation ===\n")

    # Get file path from command line or user input
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Processing file: {file_path}")
    else:
        file_path = input("Enter the path to the AsciiDoc file: ").strip()

    # Convert to absolute path
    file_path = os.path.abspath(file_path)

    # Validate file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)

    # Validate it's an AsciiDoc file
    if not file_path.endswith('.adoc'):
        print("Warning: File does not have .adoc extension")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(0)

    # Get repository root
    repo_root = get_repo_root(file_path)
    print(f"Repository root: {repo_root}")

    # Get current branch
    current_branch = run_command("git branch --show-current", cwd=repo_root)
    print(f"Current branch: {current_branch}")

    # Create branch name from file name
    file_name = Path(file_path).stem  # Get filename without extension
    branch_name = f"jtbd-transformation-{file_name}"
    print(f"Creating branch: {branch_name}")

    # Check if branch already exists
    existing_branches = run_command("git branch --list", cwd=repo_root)
    if branch_name in existing_branches:
        print(f"\nWarning: Branch '{branch_name}' already exists")
        response = input("Switch to it and continue? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(0)
        run_command(f"git checkout {branch_name}", cwd=repo_root)
    else:
        # Create and checkout new branch
        run_command(f"git checkout -b {branch_name}", cwd=repo_root)

    print(f"\nTransforming file: {file_path}")

    # Read and transform the file
    transformed_content = transform_asciidoc_file(file_path)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(transformed_content)

    print("✓ File transformed successfully")

    # Stage the file
    relative_path = Path(file_path).relative_to(repo_root)
    run_command(f"git add {relative_path}", cwd=repo_root)
    print(f"✓ File staged: {relative_path}")

    # Show status
    print("\n=== Git Status ===")
    status = run_command("git status --short", cwd=repo_root)
    print(status)

    print("\n=== Next Steps ===")
    print(f"1. Review the changes: git diff --cached")
    print(f"2. Commit when ready: git commit -m 'Transform {file_name} to JTBD format'")
    print(f"3. Push to remote: git push origin {branch_name}")
    print(f"\nCurrent branch: {branch_name}")


if __name__ == "__main__":
    main()
