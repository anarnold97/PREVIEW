# TOC Level Check Script

`check_toc_level.py` checks that the **table of contents (TOC)** in **MTV (Migration Toolkit for Virtualization)** documentation in the **forklift-documentation** repository does not exceed the configured level (default **level 3**), as required by **CQA (Content Quality Assessment)** for docs.redhat.com.

The script walks `master.adoc` files under `documentation/`, follows `include::` directives (`modules/`, `assemblies/` per doc), and reports any heading that would appear in the TOC at a depth greater than `:toclevels:`.

---

## Requirements

- **Python 3.8+** (no extra packages; standard library only)

The script must be run from somewhere under the **forklift-documentation** repository so it can find the repo root (directory containing `documentation/` with at least one `documentation/doc-*/master.adoc`). Repo root is detected automatically.

---

## Usage

### Basic usage

```bash
# Check all guides (all documentation/doc-*/master.adoc)
python check_toc_level.py

# Check a single guide by directory
python check_toc_level.py documentation/doc-Planning_your_migration
python check_toc_level.py documentation/doc-Migrating_your_virtual_machines

# Check a single master file
python check_toc_level.py documentation/doc-Release_notes/master.adoc
```

### Optional arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Limit the check to this directory (e.g. `documentation/doc-Planning_your_migration`) or a single `master.adoc` file. If omitted, all `documentation/doc-*/master.adoc` files are checked. |
| `--max-level N` | Override the maximum allowed TOC level (default: from each master’s `:toclevels:` or from `documentation/modules/common-attributes.adoc` if present). |
| `-q`, `--quiet` | Only set exit code; no summary or violation list. |

### Examples

```bash
# From repo root — check everything
python check_toc_level.py

# Check only the Planning guide
python check_toc_level.py documentation/doc-Planning_your_migration

# Check only the Migrating guide
python check_toc_level.py documentation/doc-Migrating_your_virtual_machines

# Check only Release notes
python check_toc_level.py documentation/doc-Release_notes

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

- **Repo root** is the directory that contains `documentation/` with at least one `documentation/doc-*/master.adoc`.
- **Default max level** is read from `documentation/modules/common-attributes.adoc` if it sets `:toclevels:`; otherwise the script uses **3**. Each **master.adoc** sets its own `:toclevels:` (e.g. `:toclevels: 3` for Planning/Migrating, `:toclevels: 2` for Release notes).
- The script follows `include::path[leveloffset=+N]` from each master. Paths are resolved **relative to the including file**: e.g. from `documentation/doc-*/master.adoc`, `modules/foo.adoc` and `assemblies/bar.adoc` resolve under that doc; from an assembly, `../modules/foo.adoc` resolves to the shared `documentation/modules/` (via the per-doc `modules` symlink).
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

- **Recommended:** Keep the script in the **forklift-documentation repo root** (same directory as `documentation/`) and run it from there:

  ```bash
  cd /path/to/forklift-documentation
  python check_toc_level.py
  python check_toc_level.py documentation/doc-Planning_your_migration
  ```

- You can also run it from any subdirectory; repo root is found by walking up until `documentation/` with `doc-*/master.adoc` exists.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `Error: could not find repo root` | Run the script from inside the forklift-documentation repo (a parent directory must contain `documentation/` with at least one `documentation/doc-*/master.adoc`). |
| No output when run with no path | The script checks all `documentation/doc-*/master.adoc` files; use a path (e.g. `documentation/doc-Planning_your_migration`) to limit scope. |
| Violations in included files | Flatten headings in the included file, or reduce `leveloffset` in the `include::` so the effective TOC level does not exceed the book’s `:toclevels:`. |

---

## Layout: forklift-documentation (MTV) vs other repos

The **forklift-documentation** repo uses:

- **documentation/** as the docs root (not `docs/`).
- **documentation/doc-*/** — one directory per book (e.g. `doc-Planning_your_migration`, `doc-Migrating_your_virtual_machines`, `doc-Release_notes`), each with its own `master.adoc` and **assemblies/**.
- **documentation/modules/** — shared modules; each `doc-*` has a `modules` symlink to `../modules`.
- **Include resolution** — paths in `include::` are relative to the including file (e.g. from master: `modules/...`, `assemblies/...`; from assembly: `../modules/...`).

This script is written for that MTV layout: it discovers `documentation/doc-*/master.adoc`, resolves includes relative to the current file, applies `leveloffset`, and checks effective heading depth against each master’s `:toclevels:`.
