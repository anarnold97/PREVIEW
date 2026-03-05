# TOC Level Check Script

`check_toc_level.py` checks that the **table of contents (TOC)** in the openshift-docs topic map does not exceed **level 3**, as required by the **CQA (Content Quality Assessment)** for migration and docs.redhat.com.

The script reads `_topic_maps/_topic_map.yml` and reports any branch where nesting goes deeper than three levels.

---

## Requirements

- **Python 3.8+**
- **PyYAML** (for parsing the topic map):

  ```bash
  pip install pyyaml
  ```

The script must be run from somewhere under the openshift-docs repository so it can find the `_topic_maps` directory (repo root is detected automatically).

---

## Usage

### Basic usage

```bash
# Check only the 'virt' branch (recommended for virt work)
python check_toc_level.py virt

# Check only the 'backup_and_restore' branch
python check_toc_level.py backup_and_restore

# Check only the OADP application backup and restore subtree
python check_toc_level.py backup_and_restore/application_backup_and_restore
```

### No path argument

If you **do not** pass a path:

- If the script lives under **`virt/`** (e.g. `virt/check_toc_level.py`), it checks only the **virt** branch.
- If the script lives under **`backup_and_restore/application_backup_and_restore/`**, it checks only **backup_and_restore/application_backup_and_restore**.
- If the script lives under **`backup_and_restore/`** (but not in `application_backup_and_restore`), it checks only **backup_and_restore**.
- Otherwise, it checks the **entire topic map**.

So for typical use in `virt/` or `backup_and_restore/application_backup_and_restore/`, you can run:

```bash
python check_toc_level.py
```

and only your branch is checked.

### Optional arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Limit the check to this branch. Use `virt`, `backup_and_restore`, or `backup_and_restore/application_backup_and_restore`. |
| `--topic-map PATH` | Use a specific topic map file (default: `repo_root/_topic_maps/_topic_map.yml`). |
| `--max-level N` | Maximum allowed TOC level (default: `3`). |
| `-q`, `--quiet` | Only set exit code; no summary or violation list. |

### Examples

```bash
# From repo root
python virt/check_toc_level.py virt

# From virt/
cd virt && python check_toc_level.py

# From backup_and_restore/application_backup_and_restore/
cd backup_and_restore/application_backup_and_restore && python ../../virt/check_toc_level.py

# Check entire map (from repo root, no path)
python virt/check_toc_level.py

# Custom topic map or max level
python check_toc_level.py virt --topic-map /path/to/_topic_map.yml
python check_toc_level.py virt --max-level 4
```

---

## Exit codes

| Code | Meaning |
|------|--------|
| **0** | All checked branches have TOC depth ≤ 3 (pass). |
| **1** | At least one node has TOC level > 3 (fail). |
| **2** | Error (e.g. topic map not found, missing PyYAML). |

---

## How TOC level is counted

The topic map is a hierarchy of **topic groups** and **topics**:

- **Level 1:** Top-level section (e.g. *Virtualization*, *Backup and restore*) — the `Dir` at the root of each `---` block.
- **Level 2:** First level of `Topics` under that section (e.g. *Creating a virtual machine*, *Managing VMs*).
- **Level 3:** Nested `Topics` (e.g. *Advanced VM creation* → *Creating VMs in the web console*).
- **Level 4:** Any further nesting — **this is the first level that fails** the “no greater than 3” rule.

So “max level 3” means the deepest **visible** TOC level is 3 (four levels total: root section + three levels of entries). Any node that would appear at level 4 or deeper is reported as a violation.

---

## Typical use cases

### 1. Virt documentation (`openshift-docs/virt`)

Run from `virt/` or repo root:

```bash
python check_toc_level.py virt
```

If the script is in `virt/`, you can also run:

```bash
python check_toc_level.py
```

Violations are listed with full path and name (e.g. `virt / managing_vms / advanced_vm_management / …`). To comply with CQA, flatten or reorganize those branches in `_topic_maps/_topic_map.yml` so nothing goes beyond level 3.

### 2. OADP / Application backup and restore (`backup_and_restore/application_backup_and_restore`)

Run from repo root or from that directory:

```bash
python virt/check_toc_level.py backup_and_restore/application_backup_and_restore
```

Or, if you copy the script into `backup_and_restore/application_backup_and_restore/`:

```bash
python check_toc_level.py
```

Only the OADP application backup and restore subtree is checked.

---

## Relation to CQA

The **CQA 2.1** pre-migration requirements state:

> **Content is not deeply nested in the TOC (recommended: no more than 3 levels).**

This script automates that check using the **topic map** as the source of truth for the doc site TOC. Fixing reported violations in `_topic_map.yml` helps ensure the content is ready for migration and meets the “no greater than level 3” rule.

---

## Where to put the script

- **Recommended:** Keep a single copy under **`virt/`** (e.g. `virt/check_toc_level.py`) and run it with an explicit path when needed:

  ```bash
  python virt/check_toc_level.py virt
  python virt/check_toc_level.py backup_and_restore/application_backup_and_restore
  ```

- You can also copy it into **`backup_and_restore/application_backup_and_restore/`** and run it with no arguments there to check only that branch.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `Error: could not find repo root` | Run the script from inside the openshift-docs repo (a parent directory must contain `_topic_maps/`). |
| `Error: topic map not found` | Ensure `_topic_maps/_topic_map.yml` exists at repo root, or pass `--topic-map` to a valid file. |
| `Error: PyYAML is required` | Install with `pip install pyyaml` (or `pip3 install pyyaml`). |
| No output when run with no path | If the script is not under `virt/` or `backup_and_restore/`, it checks the entire map; use an explicit path to limit scope. |

---

## Topic map reference

- **File:** `openshift-docs/_topic_maps/_topic_map.yml`
- **Format:** Multiple YAML documents separated by `---`. Each document has:
  - `Name`: Display name of the topic group
  - `Dir`: Directory name (e.g. `virt`, `backup_and_restore`)
  - `Topics`: List of entries; each entry has `Name` and either `File` (leaf) or `Dir` + `Topics` (nested group)

Nesting is defined by repeated `Dir` + `Topics` structures. The script walks this tree and reports any path that reaches level 4 or deeper.
