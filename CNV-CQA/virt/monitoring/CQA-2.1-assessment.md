# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/monitoring/`  
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
# All files in virt/monitoring (9 files, no subdirs):
vale --config=.vale-cqa.ini virt/monitoring/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/monitoring/*.adoc` (9 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/monitoring/*.adoc` | 7 | 76 | 88 | 9 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/monitoring/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/monitoring/` — No TOC violations under `monitoring`. The virt branch reports 32 nodes with level > 3; all are under `virt/managing_vms/` (advanced_vm_management, virtual_disks).

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
python3 virt/install/check_broken_links.py virt/monitoring
```

**Result:** **4 issue(s)** in 9 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 4 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issues:**

- **virt-exposing-custom-metrics-for-vms.adoc** → `../../nodes/pods/nodes-pods-configmaps.adoc#nodes-pods-configmaps` — anchor `nodes-pods-configmaps` not found (ids include `configmaps`, `nodes-pods-configmaps-consuming-configmap-in-pods`, …).
- **virt-exposing-downward-metrics.adoc** → `../../virt/monitoring/virt-exposing-downward-metrics.adoc#virt-viewing-downward-metrics-cli_virt-exposing-downward-metrics` — anchor not found (ids include `virt-enabling-disabling-feature-gate`, `virt-exposing-downward-metrics`, …).
- **virt-prometheus-queries.adoc** → `../../machine_configuration/machine-configs-configure.adoc#nodes-nodes-kernel-arguments_machine-configs-configure` — anchor not found (ids include `machine-configs-configure`, …).
- **virt-storage-checkups.adoc** → `../../virt/support/virt-collecting-virt-data.adoc#virt-using-virt-must-gather_virt-collecting-virt-data` — anchor not found (ids include `virt-collecting-data-about-vms_virt-collecting-virt-data`, …).

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/monitoring
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/monitoring
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **9** `virt/monitoring/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-exposing-custom-metrics-for-vms.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-exposing-downward-metrics.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-monitoring-overview.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-monitoring-vm-health.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-monitoring-vm-health.adoc | 20 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-prometheus-queries.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-runbooks.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |

**Total:** 7 DITA errors (6 ShortDescription, 1 AssemblyContents) across 6 files.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 7 errors (all DITA) |
| Vale — no warnings | Does not meet | 76 warnings (RedHat + spelling, etc.) |
| TOC depth ≤ 3 levels | Meets | No violations under monitoring |
| No broken links | Does not meet | 4 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors + warnings)

| File | Errors | Warnings | Suggestions |
|------|--------|----------|-------------|
| virt-exposing-custom-metrics-for-vms.adoc | 1 | — | 1 |
| virt-exposing-downward-metrics.adoc | 1 | — | 1 |
| virt-latency-checkups.adoc | — | 1 | 1 |
| virt-monitoring-overview.adoc | 1 | — | 2 |
| virt-monitoring-vm-health.adoc | 2 | — | 2 |
| virt-prometheus-queries.adoc | 1 | — | 2 |
| virt-runbooks.adoc | 1 | 44 | 52 |
| virt-running-cluster-checkups.adoc | — | 1 | 1 |
| virt-storage-checkups.adoc | — | 2 | 2 |
| **Total** | **7** | **76** | **88** |

*virt-runbooks.adoc* accounts for most warnings (e.g. “runbook” spelling, sentence-style headings) and suggestions.

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph (short description) in each topic per DITA convention.
- **AssemblyContents:** In *virt-monitoring-vm-health.adoc*, ensure only “additional resources”–type content appears at line 20 (or restructure per AsciiDocDITA.AssemblyContents).
- **Broken xrefs:** Update or remove the four xrefs whose anchors are not present in the target files (or confirm against published build IDs).
- **RedHat:** Address passive voice, readability, spelling (“runbook”, “VM's”, “Runbooks”), sentence-style headings, and terminology where flagged.

---

## 6. Next steps

1. Fix all 7 DITA errors (ShortDescription + AssemblyContents).
2. Resolve 4 broken xref anchors (or validate against published docs).
3. Work through Vale warnings (prioritize *virt-runbooks.adoc*) and suggestions as needed for style compliance.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
