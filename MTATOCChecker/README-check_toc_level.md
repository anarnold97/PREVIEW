# TOC Level Check Script

`check_toc_level.py` checks that the **table of contents (TOC)** in **MTA (Migration Toolkit for Applications)** documentation does not exceed the configured level (default **level 3**), as required by **CQA (Content Quality Assessment)** for docs.redhat.com.

The script walks `master.adoc` files under `docs/`, follows `include::` directives (`topics/`, `assemblies/`), and reports any heading that would appear in the TOC at a depth greater than `:toclevels:`.

---

## Requirements

- **Python 3.8+** (no extra packages; standard library only)

The script must be run from somewhere under the **mta-documentation** repository so it can find the repo root (directory containing both `docs/` and `assemblies/`). Repo root is detected automatically.

---

## Usage

### Basic usage

```bash
# Check all guides (all docs/*/master.adoc)
python check_toc_level.py

# Check a single guide by directory
python check_toc_level.py docs/cli-guide
python check_toc_level.py docs/web-console-guide

# Check a single master file
python check_toc_level.py docs/install-guide/master.adoc
```

### Optional arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Limit the check to this directory (e.g. `docs/cli-guide`) or a single `master.adoc` file. If omitted, all `docs/*/master.adoc` files are checked. |
| `--max-level N` | Override the maximum allowed TOC level (default: from `docs/topics/templates/document-attributes.adoc` or from each master’s `:toclevels:`). |
| `-q`, `--quiet` | Only set exit code; no summary or violation list. |

### Examples

```bash
# From repo root — check everything
python check_toc_level.py

# Check only the CLI guide
python check_toc_level.py docs/cli-guide

# Check only the web console guide
python check_toc_level.py docs/web-console-guide

# Override max level (e.g. allow 4 levels)
python check_toc_level.py --max-level 4

# Quiet mode (exit code only)
python check_toc_level.py -q
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| **0** | All checked content has TOC depth ≤ configured max (pass). |
| **1** | At least one heading has TOC level > max (fail). |
| **2** | Error (e.g. repo root not found). |

---

## How TOC level is determined

- **Repo root** is the directory that contains both `docs/` and `assemblies/`.
- **Default max level** is read from `docs/topics/templates/document-attributes.adoc` (`:toclevels:`; default 3).
- Each **master.adoc** can override the max with its own `:toclevels:` (e.g. `:toclevels: 4`).
- The script follows `include::path[leveloffset=+N]` from each master into `topics/` and `assemblies/` (resolved from repo root; `topics/` may be under `docs/` or a symlink).
- **Effective TOC level** for a heading is: (number of `=` in the heading) + (sum of `leveloffset` from the include chain). For example, a `===` heading in a file included with `leveloffset=+1` has effective level 4.
- Any heading whose effective level is **greater than** the max (for that book) is reported as a violation.

So “max level 3” means only `=`, `==`, and `===` are allowed in the effective TOC; any heading that would appear as level 4 or deeper is reported.

---

## Relation to CQA

The **CQA 2.1** pre-migration requirements state:

> **Content is not deeply nested in the TOC (recommended: no more than 3 levels).**

This script automates that check using the **AsciiDoc master and include structure** as the source of truth. Fixing reported violations (by flattening headings or adjusting `leveloffset`) helps ensure the content meets the “no greater than level 3” rule (or the level set in `:toclevels:`).

---

## Where to put the script

- **Recommended:** Keep the script in the **mta-documentation repo root** (same directory as `docs/` and `assemblies/`) and run it from there:

  ```bash
  cd /path/to/mta-documentation
  python check_toc_level.py
  python check_toc_level.py docs/cli-guide
  ```

- You can also run it from any subdirectory; repo root is found by walking up until both `docs/` and `assemblies/` exist.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `Error: could not find repo root` | Run the script from inside the mta-documentation repo (a parent directory must contain both `docs/` and `assemblies/`). |
| No output when run with no path | The script checks all `docs/*/master.adoc` files; use a path (e.g. `docs/cli-guide`) to limit scope. |
| Violations in included files | Flatten headings in the included file, or reduce `leveloffset` in the `include::` so the effective TOC level does not exceed the book’s `:toclevels:`. |

---

## Difference from the OpenShift-docs version

The **openshift-docs** repo uses a YAML **topic map** (`_topic_maps/_topic_map.yml`) to define the TOC. The **mta-documentation** repo uses **AsciiDoc master files** and `include::` directives; the TOC is the heading hierarchy in the composed document. This script is written for the MTA layout: it discovers `docs/*/master.adoc`, resolves includes from repo root, applies `leveloffset`, and checks effective heading depth against `:toclevels:`.
