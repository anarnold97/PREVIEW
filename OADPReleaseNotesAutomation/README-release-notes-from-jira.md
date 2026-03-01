# OADP release notes from JIRA

This folder contains a script to generate an OADP release notes module (AsciiDoc) from a JIRA filter CSV export.

## Process

1. **Version** – You provide the release version (e.g. `1.5.5`).
2. **JIRA export** – You export a JIRA filter result as CSV with these issue types:
   - **Bug fix** → becomes *Resolved issues*
   - **Enhancement** → becomes *New features* (section is omitted if there are no enhancements)
   - **Known issue** → becomes *Known issues*

## JIRA CSV export

1. In JIRA, run a saved filter (or search) that returns the issues for the release.
2. **Export** → **Export CSV** (or **Export** → **Export Excel (current fields)** then save as CSV).
3. Ensure the export includes at least:
   - **Issue Key** (e.g. OADP-1234)
   - **Summary**
   - **Issue Type** (values: Bug fix, Enhancement, Known issue)
   - **Release Note Text** – Provides a customer-facing description of the change. This text is the body of each release note and the basis for the Renoa-generated draft.

Column names can vary (e.g. "Key", "Issue Type"). The script auto-detects common names; if your export uses different headers, use the `--key-column`, `--summary-column`, `--type-column`, and `--body-column` options.

## Usage

```bash
# From the release-notes directory
python3 oadp_release_notes_from_jira.py <VERSION> <PATH_TO_CSV>

# Example
python3 oadp_release_notes_from_jira.py 1.5.5 ~/Downloads/jira_oadp_1.5.5.csv
```

By default, the script writes:

- **Output file:** `modules/oadp-<version>-release-notes.adoc` under the repo root (e.g. `openshift-docs/modules/oadp-1-5-5-release-notes.adoc`).

Options:

- `-o PATH` / `--output PATH` – Write the module to a specific path.
- `--context NAME` – AsciiDoc context suffix for section IDs (default: `context`).
- `--key-column`, `--summary-column`, `--type-column`, `--body-column` – Override CSV column names if auto-detection fails (e.g. `--body-column "Release Note Text"`).

## After generating

1. Open the new module and adjust the abstract (`[role="_abstract"]`) and any wording as needed.
2. Add the module to the main OADP release notes assembly (e.g. `release-notes/oadp-1-5-release-notes.adoc`) with:

   ```asciidoc
   include::modules/oadp-1-5-5-release-notes.adoc[leveloffset=+1]
   ```

3. Build/preview the docs to confirm formatting and links.

## Sample CSV format

Minimal CSV that the script can parse (body comes from **Release Note Text**):

```csv
Issue Key,Summary,Issue Type,Release Note Text
OADP-6700,Simultaneous updates cause resource conflicts,Known issue,"Simultaneous updates to the same ..."
OADP-6765,Self-signed certificate for internal image backup,Bug fix,"Before this update..."
```

- **Release Note Text** – Customer-facing description; used as the body of each release note and as the basis for the Renoa-generated draft. If this column is missing, the script falls back to **Description**.
- Issue Type must be exactly one of: **Bug fix**, **Enhancement**, **Known issue** (case-insensitive).
