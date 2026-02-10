# fix_missing_shortdesc.py

A Python script that applies **CQA 2.1 shortdesc** fixes to AsciiDoc (`.adoc`) topics: it adds missing short descriptions and adjusts existing ones to meet length rules.

## What this script does

- **Finds topics without a shortdesc**  
  Scans the repository for `.adoc` files that do not contain a `[role="_abstract"]` block (the CQA short description).

- **Adds missing shortdescs**  
  For each such file it:
  - Takes the level-1 title (`= Title`) and derives a CQA-compliant shortdesc, or
  - Uses a custom shortdesc from `shortdesc_overrides.csv` if that file exists and lists the topic path.

- **Enforces length (50–300 characters)**  
  - **Too long:** Truncates the abstract at a word boundary and appends "…" so it stays within 300 characters.  
  - **Too short:** Appends a standard suffix so the abstract is at least 50 characters (up to 300).

- **Respects structure**  
  When inserting an abstract, it places it after the first `= Title` and after any blank lines, `:attribute:` lines, or `//` comments.

- **Skips `website`**  
  Any `.adoc` under a `website` directory is ignored.

Optional override file in the **repository root**: `shortdesc_overrides.csv`. Format one row per topic:  
`path/to/file.adoc,Custom short description text.`

## How to use this script in the MTA repo

**Prerequisites:** Python 3. No extra packages required.

1. **Preview first (recommended)**  
   Run in dry-run mode so no files are changed; the script only reports what it would do:

   ```bash
   python3 /path/to/PREVIEW/fix_missing_shortdesc.py --dry-run /path/to/mta-documentation
   ```

   Or from inside the MTA repo:

   ```bash
   python3 /path/to/PREVIEW/fix_missing_shortdesc.py --dry-run .
   ```

2. **Apply changes**  
   Omit `--dry-run` to actually add or edit shortdescs:

   ```bash
   python3 /path/to/PREVIEW/fix_missing_shortdesc.py /path/to/mta-documentation
   ```

3. **Optional: custom shortdescs**  
   In the MTA repo root, add `shortdesc_overrides.csv` with lines like:

   ```csv
   docs/topics/some-topic.adoc,Your preferred short description for this topic.
   ```

   The script will use these instead of the title-derived text for the listed paths.

**Arguments:**

- `repo` — Path to the repository root that contains the `.adoc` files. Optional; if omitted, defaults to the parent of the directory containing the script.
- `--dry-run` — Show what would be fixed without writing any files.

**Note:** This script is intended to be run against a copy or branch of the MTA documentation repo. Review the diff before committing.
