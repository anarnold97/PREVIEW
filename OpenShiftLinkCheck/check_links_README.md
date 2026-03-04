# check_links.py (OADP documentation)

> [!NOTE]
>
> This script is to be used to validate links in the OADP (OpenShift API for Data Protection) documentation.

Checks for broken links in OpenShift docs AsciiDoc (`.adoc`) files for the **OADP book**:  
`openshift-docs/backup_and_restore/application_backup_and_restore/`.  
It scans all `.adoc` files in that directory and its subdirectories (e.g. `installing/`, `troubleshooting/`, `backing_up_and_restoring/`), and reports a **comparison** of links against the OADP documentation set (internal vs external, OK vs broken).

## What it checks

| Link type | Syntax | How it's verified |
|-----------|--------|-------------------|
| **Internal xref** | `xref:path/to/file.adoc#anchor[text]` | Target file must exist (path relative to current file or repo root). If `#anchor` is present, the target file must contain a matching `[id="..."]` (with `:context:` expansion). |
| **Include** | `include::path/to/file[]` | Target must exist (path relative to **repo root**, e.g. `modules/`, `_attributes/`, `snippets/`). |
| **External** | `link:https://example.com[text]` | Optional: use `--check-urls` to fetch each URL (HEAD request); expects HTTP 2xx. |

Only `link:http://` and `link:https://` are treated as external; other link types are ignored.

## Comparison with OADP documentation

The script classifies **xref** targets and reports:

- **Internal to OADP** – xrefs whose target file is under `application_backup_and_restore/`. These are validated against the OADP doc set (file exists, anchor exists if specified).
- **External** – xrefs whose target is outside that tree (other books or shared `modules/`). Same validation (file + anchor).
- **OADP doc set** – Total number of `.adoc` files under the book (all subdirs).

Example summary:

```
Comparison with OADP documentation:
  Internal to OADP (within application_backup_and_restore): 45 OK, 2 broken
  External (other books/repo): 73 OK, 5 broken
  OADP doc set: 58 .adoc file(s)
```

## Requirements

- **Python 3** (no extra packages)
- For external link checks: `--check-urls` and network access (some environments may block or restrict it)

## Usage

### Check OADP documentation (default)

Run with no arguments from the repo root or from the script's directory. The script finds the repo root and checks all `.adoc` files under `backup_and_restore/application_backup_and_restore` (including subdirectories).

From repo root:

```bash
cd /path/to/openshift-docs
python3 backup_and_restore/application_backup_and_restore/check_links.py
```

From the script directory:

```bash
cd backup_and_restore/application_backup_and_restore
python3 check_links.py
```

### Explicit repo root and book path

Pass the **repo root** and optionally the **book directory** (relative to repo root):

```bash
python3 check_links.py /path/to/openshift-docs
python3 check_links.py /path/to/openshift-docs backup_and_restore/application_backup_and_restore
```

### Optional flags

| Flag | Description |
|------|-------------|
| `--check-urls` | Validate each `link:https?://` URL (HEAD request). |
| `--validate-against URL` | Resolve each xref to the published docs URL and check it with a GET request (e.g. Red Hat or OKD docs). |
| `-q`, `--quiet` | Only print a short summary of issue count; no comparison block or per-issue details. |

Examples:

```bash
python3 check_links.py --check-urls
python3 check_links.py --validate-against https://docs.redhat.com/en/documentation/.../application_backup_and_restore
python3 check_links.py -q
```

## Output

- Prints repo root and the directory being checked.
- **Internal links:** For each broken xref or include, prints source file, target path (and anchor if any), and reason (file not found, anchor not found, etc.).
- **External links:** Only when `--check-urls` is used; for each URL, prints `OK` or the error.
- **Comparison:** (unless `-q`) Summary of internal-to-OADP vs external xrefs (OK / broken) and OADP doc set size.
- Exit code **0** if everything is OK, **1** if any internal or external link is broken or unreachable.

Example (all OK):

```
Repo root: /path/to/openshift-docs
Checking OADP documentation: backup_and_restore/application_backup_and_restore

Comparison with OADP documentation:
  Internal to OADP (within application_backup_and_restore): 12 OK, 0 broken
  External (other books/repo): 80 OK, 0 broken
  OADP doc set: 58 .adoc file(s)

All links OK (validated against OADP documentation).
```

Example (failures):

```
Found 3 issue(s):

  xref   backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.adoc
         -> ../../../operators/admin/olm-restricted-networks.adoc#olm-restricted-networks
         target file not found: ../../../operators/admin/olm-restricted-networks.adoc

  include backup_and_restore/application_backup_and_restore/troubleshooting/troubleshooting.adoc
         -> modules/oadp-installation-issues.adoc
         included file not found: modules/oadp-installation-issues.adoc
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All internal and external links OK |
| 1 | One or more broken internal links or unreachable external URLs |
| 2 | Invalid arguments or path (e.g. directory not found) |

Suitable for use in CI or scripts, e.g. `python3 backup_and_restore/application_backup_and_restore/check_links.py || exit 1`.

## Repo root detection

When you don't pass a repo root, the script finds the openshift-docs repo root by walking up from its own directory until it finds a directory that has both **modules/** or **_attributes/** and the **OADP book path** (`backup_and_restore/application_backup_and_restore`). It uses the **closest** such directory so that the correct repo root is used even when parent directories also contain similar layout.
