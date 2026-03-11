# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/updating/`  
**Date of review:** 2025-03-10  
**Scope:** Pre-migration requirements + Vale (RedHat + AsciiDocDITA only) + Quality criteria

---

## 1. Vale configuration used

Validation was run with **only** these packages (per CQA focus):

- **RedHat** — Red Hat style guide (language, terminology, grammar)
- **AsciiDocDITA** — [asciidoctor-dita-vale](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip) (DITA 1.3–compatible markup)

Config file: repo root **`.vale-cqa.ini`** (RedHat + AsciiDocDITA only; no AsciiDoc, no OpenShiftAsciiDoc).

**How to re-run Vale (RedHat + AsciiDocDITA) on this directory:**

```bash
# From repo root; ensure packages are synced first
vale sync
# All files in virt/updating (1 file, no subdirs):
vale --config=.vale-cqa.ini virt/updating/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/updating/*.adoc` (1 file)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/updating/*.adoc` | 0 | 0 | 1 | 1 |

**CQA pre-migration:** Content **meets** Vale asciidoctor-dita-vale for errors and warnings (no errors, no warnings). One suggestion (readability) remains.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/updating/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/updating/` — No TOC violations under `updating`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

**Re-run:**

```bash
python3 virt/install/check_toc_level.py virt
```

---

## 2.2 Broken links / xrefs / includes check

**Script:** [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) (local copy: `virt/install/check_broken_links.py`)

**Requirement (CQA Pre-migration):** No broken links.

**Command run (local xref + include validation):**

```bash
python3 virt/install/check_broken_links.py virt/updating
```

**Result:** **1 issue** in 1 file (xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 1 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issue:**

- **upgrading-virt.adoc** → `../../operators/understanding/olm/olm-understanding-olm.adoc#olm-csv_olm-understanding-olm` — anchor `olm-csv_olm-understanding-olm` not found (target has id `olm-understanding-olm`).

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/updating
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/updating
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

No DITA-related Vale errors in the scanned **1** `virt/updating/` file. No DITA errors to fix for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| *(none)* | — | — | — |

**Total:** 0 DITA errors.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Meets | 0 errors |
| Vale — no warnings | Meets | 0 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under updating |
| No broken links | Does not meet | 1 xref anchor issue |

---

## 4. Breakdown by file (Vale: errors / warnings)

| File | Errors | Warnings | Notes |
|------|--------|----------|--------|
| upgrading-virt.adoc | 0 | 0 | 1 suggestion (ReadabilityGrade); 1 broken xref |
| **Total** | **0** | **0** | 1 suggestion, 1 file |

---

## 5. Quality notes

- **Broken xref:** Update or remove the xref to `olm-understanding-olm.adoc#olm-csv_olm-understanding-olm`, or use an anchor that exists in the target (e.g. `#olm-understanding-olm`) or validate against published build IDs.
- **RedHat suggestion:** Consider simplifying language to lower the Flesch–Kincaid grade level (currently 10.85; recommended ≤ 9).

---

## 6. Next steps

1. Resolve the 1 broken xref anchor (or validate against published docs).
2. Optionally address the readability suggestion.
3. Re-run the broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
