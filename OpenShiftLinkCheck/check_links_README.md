# check_links.py

Checks for broken links in OpenShift docs AsciiDoc (`.adoc`) files. Works for **any book** in the openshift-docs repository, not only vm_networking.

## What it checks

| Link type | Syntax | How it's verified |
|-----------|--------|-------------------|
| **Internal xref** | `xref:path/to/file.adoc#anchor[text]` | Target file must exist (path relative to the current file). |
| **Include** | `include::path/to/file[]` | Target must exist (path relative to **repo root**). |
| **External** | `link:https://example.com[text]` | URL is fetched; expects HTTP 2xx. |

Only `link:http://` and `link:https://` are treated as external; other link types are ignored.

## Requirements

- **Python 3** (no extra packages)
- For external link checks: network access (some environments may block or restrict it)

## Usage

### Check vm_networking (default)

Run with no arguments from the repo root or from the script’s directory. The script finds the repo root and checks all `.adoc` files in `virt/vm_networking`.

From repo root:

```bash
cd /path/to/openshift-docs
python3 virt/vm_networking/check_links.py
```

From the script directory:

```bash
cd virt/vm_networking
python3 check_links.py
```

### Check any other book

Pass the **repo root** and the **book directory** (relative or absolute):

```bash
python3 virt/vm_networking/check_links.py /path/to/openshift-docs applications/creating_applications
python3 virt/vm_networking/check_links.py /path/to/openshift-docs authentication/identity_providers
```

**Note:** Only `.adoc` files **in the given directory** are scanned (no subdirectories). For a book split into subdirs, run the script once per subdir you want to check.

## Output

- Prints repo root and the directory being checked.
- **Internal links:** Lists any broken xref or include targets (missing files).
- **External links:** For each URL, prints `OK`, an HTTP status code (e.g. `404`), or `FAIL` with the error.
- Exit code **0** if everything is OK, **1** if any internal or external link is broken or unreachable.

Example (all OK):

```
Repo root: /path/to/openshift-docs
Checking: /path/to/openshift-docs/virt/vm_networking

Internal links: all OK

External links:
  OK    some-file.adoc: https://example.com/page

All links OK.
```

Example (failures):

```
Broken internal links (1):
  my-file.adoc -> missing-module.adoc

External links:
  404  my-file.adoc: https://example.com/gone
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All internal and external links OK |
| 1 | One or more broken internal links or unreachable external URLs |

Suitable for use in CI or scripts, e.g. `python3 virt/vm_networking/check_links.py || exit 1`.

## Repo root detection

When you don’t pass arguments, the script finds the openshift-docs repo root by walking up from its own directory until it finds an `_attributes` directory that is a **real directory** (not a symlink). Book directories often symlink `_attributes` and `modules`; the script uses the actual repo root so that `include::` paths resolve correctly.
