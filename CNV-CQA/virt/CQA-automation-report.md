# CQA Automation Report: openshift-docs/virt/

**Date:** 2025-03-10  
**Scope:** Automating CQA 2.1 checks (Vale, TOC, broken links) and assessment report generation for the `virt/` directory.

---

## 1. Current state

### 1.1 Checks performed (manual today)

| Check | Tool | How it runs | Output |
|-------|------|-------------|--------|
| **Vale (RedHat + AsciiDocDITA)** | Vale CLI | `vale --config=.vale-cqa.ini virt/<subdir>/*.adoc` (and subdirs if any) | Human-readable; `--output=JSON` available |
| **TOC depth (≤ 3 levels)** | `check_toc_level.py` | `python3 virt/install/check_toc_level.py virt` | stdout; exit 0/1; violations by path |
| **Broken xrefs / includes** | `check_broken_links.py` | `python3 virt/install/check_broken_links.py virt/<subdir>` | stdout; exit 0/1; list of issues |

- **Vale** is a Go binary; it is not a Python script. The repo uses a single config at repo root: `.vale-cqa.ini` (RedHat + AsciiDocDITA only).
- **TOC** and **broken links** are already implemented as Python scripts (sources: [PREVIEW/VIRT](https://github.com/anarnold97/PREVIEW)); local copies live under `virt/install/`.

### 1.2 Assessment artifacts

- One **CQA-2.1-assessment.md** per subdirectory, written by hand (or with one-off assistance). Each report includes:
  - Vale config and re-run commands
  - Vale summary (errors, warnings, suggestions, file count)
  - TOC result (meets / does not meet; which path if not)
  - Broken links result (count, sample issues)
  - DITA errors table (File, Line, Rule, Message)
  - Pre-migration checklist, breakdown by file, quality notes, next steps, references

**Subdirs with assessments today:** `install`, `live_migration`, `managing_vms`, `monitoring`, `nodes`, `post_installation_configuration`, `release_notes`, `storage`, `support`, `updating`, `vm_networking`.

### 1.3 Pain points

- Running three different commands per subdir and copying results into the assessment is repetitive and error-prone.
- Vale must be run with explicit file globs (e.g. `virt/monitoring/*.adoc`); subdirs (e.g. `managing_vms/advanced_vm_management/*.adoc`) require extra runs. Discovering all `.adoc` paths under a branch is not automated.
- TOC is run once for the whole `virt` branch; mapping “which violations belong to which subdir” is done manually.
- DITA errors are extracted by grepping Vale output; no structured parsing.
- Assessment markdown is hand-maintained; totals and tables can get out of date when re-running checks.

---

## 2. Automation goals

1. **Single entry point:** Run all CQA checks for one or more `virt/` subdirs (or all of `virt/`) from one command.
2. **Structured data:** Capture Vale (JSON), TOC (violations list), and broken-links (list of issues) in a form that can be reused.
3. **Report generation:** Produce a new `CQA-2.1-completed-assessment.md` from that data so that re-running checks refreshes the report without manual copy-paste.
4. **CI-friendly:** Scripts can be invoked from the repo root with minimal setup (e.g. `vale sync` once; Python 3 + PyYAML).

---

## 3. Python scripts required

### 3.1 Existing scripts (keep as-is, call from automation)

| Script | Location | Role |
|--------|----------|------|
| **check_toc_level.py** | `virt/install/check_toc_level.py` | Reads `_topic_maps/_topic_map.yml`, checks depth for branch `virt` (or given path). Returns violations (level, path segments, name). No changes required; orchestration will invoke it and parse stdout / exit code. |
| **check_broken_links.py** | `virt/install/check_broken_links.py` | Scans `.adoc` under a given path for xref/include (optional link URL check). Returns list of issues. Optional: add a `--output=json` (or similar) to emit machine-readable results; otherwise the orchestrator can parse the existing stdout format. |

**Dependencies:**  
- `check_toc_level.py`: PyYAML.  
- `check_broken_links.py`: stdlib only (optional: `urllib` for `--check-urls` / `--validate-against`).

---

### 3.2 New scripts (to add)

#### A. **run_virt_cqa.py** (orchestrator)

**Purpose:** Run Vale, TOC, and broken-links for a given path (e.g. `virt`, `virt/monitoring`, or a list of subdirs) and collect all results in a single structure.

**Responsibilities:**

- **Discovery:** Given a root path (e.g. `virt/`), find all “scan units”:
  - Either: every immediate subdir that contains `.adoc` (e.g. `virt/install`, `virt/monitoring`, …), or
  - A single path (e.g. `virt/storage`) when the user specifies one.
- **Vale:** For each scan unit:
  - Discover all `**/*.adoc` under that path (respecting the rule that Vale is run with explicit globs to avoid include-resolution issues).
  - Build the right globs (e.g. `virt/storage/*.adoc` only, or for `managing_vms` also `virt/managing_vms/advanced_vm_management/*.adoc`, `virt/managing_vms/virtual_disks/*.adoc`).
  - Run: `vale --config=.vale-cqa.ini --output=JSON <globs>` from repo root.
  - Parse JSON and derive: total errors/warnings/suggestions, file count, list of DITA errors (rule name, file, line, message).
- **TOC:** Run once per “virt branch” (e.g. `python3 virt/install/check_toc_level.py virt`), capture exit code and full stdout. Parse violations (e.g. “Level 4: virt / managing_vms / virtual_disks / …”) and, for each scan unit, decide “meets” if no violation path starts with that subdir.
- **Broken links:** For each scan unit, run `python3 virt/install/check_broken_links.py <path>` (and optional `--validate-against`), capture exit code and stdout. Parse issue count and list (file, target, anchor).
- **Output:** Write a single JSON (or Python pickle) “run result” per scan unit (or one file with all units) containing:
  - `vale`: { errors, warnings, suggestions, files, dita_errors[] }
  - `toc`: { meets: bool, violations_in_scope: [] }
  - `broken_links`: { count, issues[] }

**Invocation (example):**

```bash
python3 virt/install/run_virt_cqa.py --virt-root virt --output results.json
python3 virt/install/run_virt_cqa.py --path virt/monitoring --output results-monitoring.json
```

**Dependencies:** Python 3, subprocess, json, pathlib. Repo root must have `.vale-cqa.ini` and `vale` on PATH; `vale sync` assumed already run.

---

#### B. **generate_assessment.py** (report generator)

**Purpose:** Turn the structured output from `run_virt_cqa.py` into a new `virt/<subdir>/CQA-2.1-completed-assessment.md`.

**Responsibilities:**

- Read the run result (JSON) for one or more scan units.
- For each unit, render the assessment markdown from a **template** (e.g. Jinja2 or a simple string template) filling in:
  - Content location (e.g. `virt/monitoring/`)
  - Date of review (run date)
  - Vale summary table (errors, warnings, suggestions, files)
  - Vale re-run command(s) for that path
  - TOC result (meets / does not meet) and, if not, which violations fall under that path
  - Broken links count and list (with target and anchor)
  - DITA errors table (File, Line, Rule, Message)
  - Pre-migration checklist (derived from counts: Vale 0 errors, 0 warnings, TOC meets, 0 broken links)
  - Breakdown by file (from Vale JSON per-file stats)
  - Static “quality notes” and “next steps” can be templated or derived from rule types.

**Invocation (example):**

```bash
python3 virt/install/generate_assessment.py --input results.json --virt-root virt
# Or: read results.json and only write virt/monitoring/CQA-2.1-completed-assessment.md
python3 virt/install/generate_assessment.py --input results.json --path virt/monitoring
```

**Dependencies:** Python 3, json, pathlib; optional Jinja2 for templates (or use `string.Template` / f-strings).

---

#### C. Optional: **vale_runner.py** (Vale wrapper)

**Purpose:** Encapsulate “run Vale with .vale-cqa.ini and return structured results” so the orchestrator doesn’t duplicate Vale CLI logic.

**Responsibilities:**

- Accept a list of globs or paths and the path to `.vale-cqa.ini`.
- Run `vale --config=... --output=JSON <globs>` via subprocess.
- Parse JSON and return: totals (errors, warnings, suggestions), per-file breakdown, and a list of “DITA” alerts (where rule name starts with `AsciiDocDITA.` or matches a known list).
- Optionally support `--no-json` and parse line-based Vale output for environments where JSON is not available.

This can be a separate module called by `run_virt_cqa.py`, or the same logic can live inside `run_virt_cqa.py`. Splitting it out is useful if you want to run Vale from other tools (e.g. a pre-commit hook or a different runner).

**Dependencies:** Python 3, subprocess, json.

---

### 3.3 Single script vs multiple scripts: recommended approach

**Recommendation: start with a single Python script** for the “one folder at a time” workflow.

| Approach | Pros | Cons |
|----------|------|------|
| **Single script** (e.g. `cnv-cqa-fix.py`) | One command per folder; no intermediate JSON to manage; easier to run and document; all logic in one place; no file handoff. | File can grow (e.g. 400–600 lines); Vale/TOC/links/report logic are coupled. |
| **Multiple scripts** (runner + report generator, optional Vale wrapper) | Smaller, testable units; can run “checks only” and “report only” separately; can reuse report generator with cached JSON. | Two (or three) commands per folder; need to pass paths and JSON; more surface area to maintain. |

**Best approach for your case:**

- **One folder at a time + Python:** Use **one script** that, for a given path (e.g. `virt/monitoring`), runs Vale, TOC, and broken links, then writes `CQA-2.1-completed-assessment.md` in that folder. One invocation, one outcome. Keep it in a single file; use clear functions (e.g. `run_vale()`, `run_toc()`, `run_broken_links()`, `generate_markdown()`) so the script stays readable.
- **Consider splitting later** only if you need (a) “run all virt subdirs and produce one JSON” without writing markdown, or (b) “regenerate reports from existing JSON.” Then you can extract a “run checks → JSON” module and a “JSON → markdown” module and call them from a thin CLI or a second script.

So: **single script first**; split into multiple scripts only if you add workflows that need it.

---

### 3.4 Summary: what Python scripts are required

| Script | Status | Purpose |
|--------|--------|---------|
| **check_toc_level.py** | Existing | TOC depth check for topic map branch. |
| **check_broken_links.py** | Existing | Xref/include (and optional URL) validation. |
| **run_virt_cqa.py** | **New** (optional) | Orchestrate Vale + TOC + broken links; output JSON; use if you need “all folders” or “checks only” workflows. |
| **cnv-cqa-fix.py** | **New** (recommended) | Single script: one folder, run all checks, write `CQA-2.1-completed-assessment.md`. |
| **generate_assessment.py** | **New** (optional) | Generate report from JSON; only needed if you split “run checks” and “generate report.” |
| **vale_runner.py** | **Optional** | Wrap Vale CLI and parse JSON for reuse. |

All new/optional scripts are assumed to live under `virt/install/` (or a dedicated `virt/scripts/` if you prefer). The two existing scripts stay as they are; optional enhancement for `check_broken_links.py` is a machine-readable output mode for easier parsing.

---

## 4. Suggested workflow

1. **One-time:** From repo root, `vale sync` (and ensure PyYAML is installed for `check_toc_level.py`).
2. **Per run (all virt subdirs):**  
   `python3 virt/install/run_virt_cqa.py --virt-root virt --output virt/cqa_run.json`  
   Then:  
   `python3 virt/install/generate_assessment.py --input virt/cqa_run.json --virt-root virt`  
   This creates (or overwrites) every `virt/<subdir>/CQA-2.1-completed-assessment.md` for which there is a scan unit in the run.
3. **Single subdir:**  
   `python3 virt/install/run_virt_cqa.py --path virt/storage --output virt/cqa_storage.json`  
   `python3 virt/install/generate_assessment.py --input virt/cqa_storage.json --path virt/storage`
4. **CI:** Run the same two commands (e.g. on a schedule or on push to `virt/`); optionally fail the job if any scan unit has errors &gt; 0 or broken_links &gt; 0.

---

## 5. Vale and globs

- Vale is run from **repo root** with explicit file lists/globs so that `include::` resolution works.
- For a path like `virt/managing_vms` that has subdirs with `.adoc` (e.g. `advanced_vm_management`, `virtual_disks`), the orchestrator must run Vale **once per distinct “glob level”** (e.g. `virt/managing_vms/*.adoc`, then `virt/managing_vms/advanced_vm_management/*.adoc`, then `virt/managing_vms/virtual_disks/*.adoc`) and merge the JSON results for that scan unit so the assessment shows one combined Vale summary and one combined DITA table for that subdir.

---

## 6. Automation scope: one folder at a time (Python)

This section describes **how much of the assessment can be automated** when using **Python** and processing **one folder at a time**, and how the existing **CQA-2.1-assessment.md** fits in.

### 6.1 What can be fully automated (from run data)

For a **single folder** (e.g. `virt/monitoring`), the following sections of `CQA-2.1-assessment.md` can be **100% generated** from running the three tools and parsing their output:

| Section | Source of data | Automated? |
|--------|----------------|------------|
| **Header** (content location, date, scope) | Path argument + today’s date | Yes |
| **1. Vale configuration used** | Static text + path (e.g. “9 files, no subdirs”) | Yes |
| **2. Vale results summary** | Vale `--output=JSON`: totals + file count; “meets” vs “does not meet” from error/warning counts | Yes |
| **2.1 TOC level check** | `check_toc_level.py virt` stdout: parse violations; “Meets” if no violation path contains this folder’s segment | Yes |
| **2.2 Broken links** | `check_broken_links.py <path>` stdout: count + list of issues (file, target, anchor) | Yes |
| **2.3 DITA errors table** | Vale JSON: filter alerts where `Severity==error`, optionally `Rule` starts with `AsciiDocDITA.` or is `RedHat.TermsErrors`; build File, Line, Rule, Message table | Yes |
| **3. Pre-migration checklist** | Derived: Vale 0 errors → Meets, else Does not meet; same for warnings; TOC from 2.1; broken links count → Meets/Does not meet | Yes |
| **4. Breakdown by file** | Vale JSON: per-file error/warning/suggestion counts; optional note from broken-links (which file has xref issues) | Yes |
| **7. References** | Static list | Yes |

So **most of the report** is data-driven and can be produced by a script that runs the tools and fills a template.

### 6.2 What can be partly automated

| Section | How to automate |
|--------|------------------|
| **5. Quality notes** | From rule types: e.g. “ShortDescription” → add bullet “Add [role=\"_abstract\"]…”; “AssemblyContents” → “Ensure only additional resources…”; “Broken xrefs” → “Update or remove the N xrefs…”. Generic bullets per rule; optional short “or validate against published build IDs.” |
| **6. Next steps** | From counts: if errors > 0 → “Fix all N DITA/style errors”; if broken_links > 0 → “Resolve N broken xref anchors”; if warnings > 0 → “Work through Vale warnings”; always “Re-run Vale and broken-links check to confirm.” |

Quality notes and next steps can be **template-driven** (one bullet per rule type or condition) so they stay consistent; only the numbers and file names are variable.

### 6.3 Using the existing CQA-2.1-assessment.md

The **existing assessment files** (e.g. `virt/monitoring/CQA-2.1-assessment.md`) are the **definition of the report structure**:

- **Section order and headings** (1–7) and **static wording** (e.g. “Requirement (CQA Pre-migration): …”) can be taken from any one of them and turned into a **string template** (e.g. Python `string.Template` or a single .md file with placeholders like `$content_location`, `$vale_errors`, `$dita_table`).
- The script does **not** need to “read” the existing assessment to get numbers—those come from the **current run**. The existing file is only the **template** (structure + boilerplate). When generating, the script **writes** `virt/<folder>/CQA-2.1-completed-assessment.md` with the new content (leaving any existing `CQA-2.1-assessment.md` unchanged).

So: **use CQA-2.1-assessment.md as the template for layout and static text**; all variable content (numbers, tables, issue lists) comes from the run.

### 6.4 One script, one folder at a time (Python)

A single Python script can do both “run checks” and “write assessment” for **one folder** per invocation:

**Script name:** `cnv-cqa-fix.py`

**Behaviour:**

1. **Input:** One path argument, e.g. `virt/monitoring` or `virt/storage` (relative to repo root).
2. **Discovery:** Under that path, find all `.adoc` files. Build Vale globs: if there are no subdirs with .adoc, use `path/*.adoc`; if there are subdirs (e.g. `virt/managing_vms/advanced_vm_management`), use `path/*.adoc`, `path/subdir1/*.adoc`, `path/subdir2/*.adoc`, etc.
3. **Run Vale:** `vale --config=.vale-cqa.ini --output=JSON <globs>` from repo root. Parse JSON → totals, per-file stats, list of errors (for DITA table).
4. **Run TOC:** `python3 virt/install/check_toc_level.py virt`. Parse stdout for “Level 4: virt / …” lines. “Meets” for this folder if no violation path starts with the folder’s segment (e.g. `monitoring`).
5. **Run broken links:** `python3 virt/install/check_broken_links.py <path>`. Parse stdout for “Found N issue(s)” and the list of xref/file/target lines.
6. **Generate markdown:** Fill the assessment template (sections 1–7) with the collected data; write `virt/<folder>/CQA-2.1-completed-assessment.md`.

**Invocation (from repo root):**

```bash
python3 virt/install/cnv-cqa-fix.py virt/monitoring
python3 virt/install/cnv-cqa-fix.py virt/storage
```

No JSON file needed if the script writes the assessment directly. Optionally support `--dry-run` (run checks, print summary, do not write the file) or `--output <path>` to write the assessment elsewhere.

### 6.5 How much work this automates

| Task | Without automation | With one-folder Python script |
|------|--------------------|-------------------------------|
| Run Vale for folder | Manual globs, copy totals | Script discovers globs, runs Vale, parses JSON |
| Run TOC and interpret for folder | Run once, manually check if “monitoring” in violations | Script runs once, filters violations by folder |
| Run broken links | Manual command, copy count and list | Script runs, parses stdout |
| Build DITA table | Grep Vale output, hand-format table | Script filters errors from JSON, formats table |
| Pre-migration checklist | Hand-update from totals | Script derives from counts |
| Breakdown by file | Hand-count from Vale | Script uses Vale JSON per-file |
| Write CQA-2.1-completed-assessment.md | Copy-paste into template | Script fills template and writes file |

Roughly **90%+ of the per-folder work** (running the three checks, extracting numbers and lists, and producing the markdown) can be automated with this one Python script. The remaining 10% is optional refinement of “Quality notes” and “Next steps” (e.g. more tailored bullets by rule type) and any one-off edits you might want to add after generation.

### 6.6 Dependencies (one-folder script)

- **Python 3** (pathlib, subprocess, json, re).
- **Vale** on PATH and **`.vale-cqa.ini`** at repo root (`vale sync` run once).
- **PyYAML** only if the script needs to read the topic map itself; for “one folder” the script can just run `check_toc_level.py` and parse its stdout, so PyYAML is not required in the one-folder script.
- **Template:** One in-repo template (e.g. `virt/install/cqa_assessment_template.md`) or the template embedded as a string in the script, derived from the current `CQA-2.1-assessment.md` structure.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF).
- Vale: `vale --help`, `--output=JSON`.
- Existing scripts: `virt/install/check_toc_level.py`, `virt/install/check_broken_links.py`.
- PREVIEW repo: [VIRT/check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py), [VIRT/check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py).
- Example assessments: `virt/install/CQA-2.1-assessment.md`, `virt/monitoring/CQA-2.1-assessment.md`, etc.
