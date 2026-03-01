# check_links.py

Checks for broken links in **MTV (Migration Toolkit for Virtualization)** documentation AsciiDoc (`.adoc`) files. Designed for the **forklift-documentation** repository. Run from the repo root or pass the repo path and an optional book directory.

---

## Overview (in plain language)

**What does this tool do?**  
It scans the MTV documentation source files and reports **broken links**—links that point to a missing page, a missing file, or a web address that no longer works. Fixing these before publishing helps readers avoid "Page not found" or dead links.

**Who is it for?**  
Anyone who edits or reviews MTV (forklift) documentation: writers, editors, or reviewers. You don’t need to be a developer. You run one command and read the report.

**When should I use it?**  
Run it before you submit a change (e.g. a pull request) or when you’ve added or moved topics. It only checks; it does not change any files.

**What do I need?**  
- A copy of the **forklift-documentation** project on your computer (the "repo").  
- **Python 3** installed (see [Requirements](#requirements) below for how to check).  
- This script (`check_links.py`) placed in the repo or run with the path to the repo.

---

## Quick start (simple steps)

1. **Open a terminal** (command line) on your computer—e.g. Terminal on macOS/Linux, or Command Prompt / PowerShell on Windows.
2. **Go to the documentation project folder**—the main folder that contains the `documentation` folder (this is often called the "repo root").  
   Example: `cd C:\Users\YourName\forklift-documentation` or `cd ~/forklift-documentation`.
3. **Run the checker:** type `python3 check_links.py` and press Enter.
4. **Read the result:**
   - If it says **"All links OK"** at the end, you’re done.
   - If it lists **"Broken internal links"** or shows **FAIL** or **404** for a URL, those are the links to fix (update the path or URL in the source file, or create the missing file).

No installation of extra software is needed beyond Python 3.

---

## Where to put the script

1. **Place the script in the `forklift-documentation` repo root** (e.g. `forklift-documentation/check_links.py`), or keep it elsewhere and pass the repo root as the first argument.
2. **Run it from the repo root** with no arguments to check all `.adoc` files under the repo, or pass a path to check a specific book (e.g. `documentation/doc-Planning_your_migration`).

You do not need to install anything; Python 3 and the script are enough.

## Terms explained

| Term | Meaning |
|------|--------|
| **Repo** | The documentation project folder (e.g. `forklift-documentation`) that you cloned or downloaded. |
| **Repo root** | The main folder of that project—the one that contains the `documentation` folder. |
| **Terminal** | The window where you type text commands (also called command line or shell). |
| **Script** | The `check_links.py` file—a small program you run with Python. |
| **Broken link** | A reference to another page or file that doesn’t exist or can’t be opened (e.g. file was moved or URL is wrong). |
| **Internal link** | A link from one documentation file to another inside the same project. |
| **External link** | A link to a website outside the project (e.g. `https://example.com`). |

## What it checks

| Link type | Syntax | How it's verified |
|-----------|--------|--------------------|
| **Internal xref** (path-style) | `xref:path/to/file.adoc#anchor[text]` | Target file must exist (path relative to the current file). Path-style only; Antora-style `xref:ref_component[]` is not validated. |
| **Include** | `include::path/to/file[]` | Target must exist. Path is relative to the **component root** of the current file (the `documentation/doc-*` directory that contains `assemblies/`, `modules/`, or `master.adoc`). Commented `//include::` lines are skipped. |
| **External** | `link:https://example.com[text]` | URL is fetched; expects HTTP 2xx. |

Only `link:http://` and `link:https://` are treated as external; other link types are ignored.

## Requirements

- **Python 3**  
  The script is written for Python. You don’t need to install any extra packages (no `pip install`).  
  **How to check if you have Python:** Open a terminal and type `python3 --version` (or `python --version` on some Windows setups). If you see a version number (e.g. `Python 3.10.5`), you’re set. If you get "command not found" or similar, install Python from [python.org](https://www.python.org/downloads/) or your system’s package manager.

- **Network access (for checking external links only)**  
  To verify that web links (e.g. `https://...`) still work, the script needs to contact the internet. If you’re on a locked-down network (e.g. some corporate or school networks), external link checks might fail or show errors—that can be a network restriction, not necessarily a broken URL.

## How to use

1. **Open a terminal** and go to your `forklift-documentation` repo root (or any directory; see [Usage](#usage) below).
2. **Run the script:**
   - **Check the whole documentation:** `python3 check_links.py` (when you’re already in the repo root).
   - **Check only one book:** `python3 check_links.py documentation/doc-Planning_your_migration` or `python3 check_links.py documentation/doc-Migrating_your_virtual_machines`.
3. **Read the output.** The script prints which folder it’s checking, how many files it scanned, then a list of internal links (OK or broken) and external links (OK, or an error code like 404).
4. **Fix any broken links** it reports: open the source file mentioned, correct the path or URL, or add the missing file. Re-run the script to confirm everything passes.

## Usage

**Script in repo root, run from repo root** — check everything (default):

```bash
cd /path/to/forklift-documentation
python3 check_links.py
```

**Check a specific book** — one argument (path relative to repo root):

```bash
python3 check_links.py documentation/doc-Planning_your_migration
python3 check_links.py documentation/doc-Migrating_your_virtual_machines
python3 check_links.py documentation/doc-Release_notes
```

**Script not in repo root (two arguments)** — repo root, then optional book path:

```bash
python3 check_links.py /path/to/forklift-documentation
python3 check_links.py /path/to/forklift-documentation documentation/doc-Planning_your_migration
```

## Output (what you see on screen)

- **First lines:** The script shows which folder it’s using as the repo root and which folder (or book) it’s checking, plus how many `.adoc` files it found.
- **Internal links:** It then reports either "Internal links: all OK" or a list of **broken** internal links. Each line shows which file has the problem and which target file or path is missing (e.g. `master.adoc -> modules/missing-topic.adoc` means `master.adoc` references a file that doesn’t exist).
- **External links:** For each web URL it found, it prints either `OK`, or an error (e.g. `404` = page not found, or `FAIL` with a short reason).
- **End:** It finishes with "All links OK." if nothing is wrong, or it exits with an error so that scripts or CI can detect failure (see [Exit codes](#exit-codes)).

**What to do when something is broken:**  
- **Internal link broken:** Open the source file (first part of the line, e.g. `master.adoc`). Fix the path to the other file (e.g. correct a typo, or add the missing `.adoc` file in the right place).  
- **External link 404 or FAIL:** The web page may have moved or been removed. Update the URL in the source file to the new address, or remove/replace the link if the page is gone.

Example (all OK):

```
Repo root: /path/to/forklift-documentation
Checking: /path/to/forklift-documentation (42 .adoc files)

Internal links: all OK

External links:
  OK some-file.adoc: https://example.com/page

All links OK.
```

Example (failures):

```
Broken internal links (1):
  master.adoc -> modules/missing-topic.adoc

External links:
  404 my-file.adoc: https://example.com/gone
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All internal and external links OK—nothing to fix. |
| 1 | One or more broken internal links or unreachable external URLs—check the report and fix the listed items. |

In practice: if the script ends with "All links OK." you get 0; if it lists any broken links or failed URLs, it exits with 1. Automated systems (e.g. CI) can use this to pass or fail a build: `python3 check_links.py || exit 1`.

## How the script finds the repo root

*(You can skip this if you always run the script from inside the repo root.)*  
When you don’t pass a path, or pass only a book path, the script looks for the repo root by starting in the folder where the script lives and moving up until it finds a folder named **`documentation`**. That folder is the top of the forklift-documentation layout. If you pass **two** arguments (repo path and book path), it uses the first argument as the repo root.

## Include path resolution (for the curious)

In forklift-documentation, each book lives under `documentation/doc-<name>/` and has its own `assemblies/` and a `modules` link to shared content. The script resolves `include::modules/...` and `include::assemblies/...` relative to the **component root** of the file that contains the include (the `documentation/doc-*` directory containing that file). This matches how the Antora/Jekyll build resolves includes.

## Notes

- **What gets checked:** The script only validates path-style cross-references (those that point to a specific `.adoc` file). Other reference styles are skipped.
- **How much is scanned:** It checks all `.adoc` files in the folder you chose (and in any subfolders). If you don’t pass a folder, it checks the whole repo.
- **External links on locked-down networks:** If your network blocks or restricts web access, external link checks may fail or show 403—that’s often a network restriction, not necessarily a broken URL.
