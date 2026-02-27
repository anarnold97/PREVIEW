# check_links.py

Checks for broken links in **MTA (Migration Toolkit for Applications)** documentation AsciiDoc (`.adoc`) files. Designed to run from the **root of the `mta-documentation`** repository.

## Where to put the script

1. **Place the script in the `mta-documentation` repo root** — the same directory that contains `docs`, `assemblies`, and the `topics` symlink (e.g. `mta-documentation/check_links.py`).
2. **Run it from the repo root** with no arguments to check all `.adoc` files, or pass a path to check a specific directory (and its subdirectories).

You do not need to install anything; Python 3 and the script are enough. If you run the script from a different location, use the two-argument form: repo root path and optional directory path.

## What it checks

| Link type | Syntax | How it's verified |
|-----------|--------|--------------------|
| **Internal xref** (path-style) | `xref:path/to/file.adoc#anchor[text]` | Target file must exist (path relative to the current file). Path-style only; `xref:ref_component[]` (Antora-style) is not validated. |
| **Include** | `include::path/to/file[]` | Target must exist (path relative to **repo root**: `topics/`, `assemblies/`, etc.). Commented `//include::` lines are skipped. |
| **External** | `link:https://example.com[text]` | URL is fetched; expects HTTP 2xx. |

Only `link:http://` and `link:https://` are treated as external; other link types are ignored.

## Requirements

- **Python 3** (no extra packages)
- For external link checks: network access (some environments may block or restrict it)

## How to use

1. **Open a terminal** and go to your `mta-documentation` repo root.
2. **Run the script:**
   - **Check entire repo:** `python3 check_links.py`
   - **Check a specific directory (and subdirs):** `python3 check_links.py docs/install-guide` or `python3 check_links.py docs/topics/mta-ui`
3. **Read the output.** It prints the repo root, the directory being checked, the number of `.adoc` files, then internal links (OK or broken) and external links (OK, HTTP status, or FAIL).
4. **Fix any broken links** reported. If the script exits with code 1, at least one link failed.

## Usage

**Script in repo root, run from repo root** — check everything (default):

```bash
cd /path/to/mta-documentation
python3 check_links.py
```

**Check a specific guide or topic tree** — one argument (path relative to repo root):

```bash
python3 check_links.py docs/install-guide
python3 check_links.py docs/topics/mta-ui
python3 check_links.py docs/rules-development-guide
```

**Script not in repo root (two arguments)** — repo root, then optional directory:

```bash
python3 check_links.py /path/to/mta-documentation
python3 check_links.py /path/to/mta-documentation docs/install-guide
```

## Output

- Prints repo root and the directory being checked (and how many `.adoc` files).
- **Internal links:** Lists any broken path-style xref or include targets (missing files).
- **External links:** For each URL, prints `OK`, an HTTP status code (e.g. `404`), or `FAIL` with the error.
- Exit code **0** if everything is OK, **1** if any internal or external link is broken or unreachable.

Example (all OK):

```
Repo root: /path/to/mta-documentation
Checking: /path/to/mta-documentation (238 .adoc files)

Internal links: all OK

External links:
  OK some-file.adoc: https://example.com/page

All links OK.
```

Example (failures):

```
Broken internal links (1):
  master.adoc -> topics/templates/revision-info.adoc

External links:
  404 my-file.adoc: https://example.com/gone
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All internal and external links OK |
| 1 | One or more broken internal links or unreachable external URLs |

Suitable for use in CI or scripts, e.g. `python3 check_links.py || exit 1`.

## How the script finds the repo root

When you pass **no arguments** or **one argument** (directory path), the script finds the repo root by walking up from its own directory until it finds a directory that contains both `docs` and `assemblies` (the MTA docs layout). When you pass **two arguments**, the first is used as the repo root. Include paths like `include::topics/...` and `include::assemblies/...` are resolved against that repo root.

## Notes

- **Antora-style xrefs** (`xref:ref_component[]`) are not validated; only path-style xrefs (containing `.adoc` or starting with `../`) are checked.
- **Recursive:** All `.adoc` files under the given directory (or the whole repo if no path is given) are scanned.
- External link checks can fail or return 403 in restricted networks; that indicates environment limits, not necessarily broken URLs.
