# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/nodes/`  
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
# All files in virt/nodes (5 files, no subdirs):
vale --config=.vale-cqa.ini virt/nodes/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/nodes/*.adoc` (5 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/nodes/*.adoc` | 9 | 7 | 21 | 5 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/nodes/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/nodes/` — No TOC violations under `nodes`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/nodes
```

**Result:** **2 issue(s)** in 5 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 2 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issues:**

- **virt-node-maintenance.adoc** → `../../virt/live_migration/virt-configuring-live-migration.adoc#virt-configuring-a-live-migration-policy_virt-configuring-live-migration` — anchor not found (ids include `virt-configuring-live-migration`, `live-migration-policies`, …).
- **virt-triggering-vm-failover-resolving-failed-node.adoc** → `../../nodes/nodes/nodes-nodes-viewing.adoc#nodes-nodes-viewing-listing_nodes-nodes-viewing` — anchor not found (ids include `nodes-nodes-viewing`, …).

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/nodes
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/nodes
```

---

## 2.3 DITA and style errors (Vale)

All Vale **errors** in the scanned **5** `virt/nodes/` files. Fix these to pass the CQA pre-migration check.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-activating-ksm.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-activating-ksm.adoc | 32 | AsciiDocDITA.RelatedLinks | Content other than links… |
| virt-managing-node-labeling-obsolete-cpu-models.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-managing-node-labeling-obsolete-cpu-models.adoc | 9 | RedHat.TermsErrors | Use 'if' or 'provided that' |
| virt-node-maintenance.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-node-maintenance.adoc | 83 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-preventing-node-reconciliation.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-triggering-vm-failover-resolving-failed-node.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-triggering-vm-failover-resolving-failed-node.adoc | 21 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |

**Total:** 9 errors (6 ShortDescription, 2 AssemblyContents, 1 RelatedLinks, 1 RedHat.TermsErrors) across 5 files.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 9 errors |
| Vale — no warnings | Does not meet | 7 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under nodes |
| No broken links | Does not meet | 2 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| virt-activating-ksm.adoc | 2 | ShortDescription, RelatedLinks |
| virt-managing-node-labeling-obsolete-cpu-models.adoc | 2 | ShortDescription, RedHat.TermsErrors |
| virt-node-maintenance.adoc | 2 | ShortDescription, AssemblyContents |
| virt-preventing-node-reconciliation.adoc | 1 | ShortDescription |
| virt-triggering-vm-failover-resolving-failed-node.adoc | 2 | ShortDescription, AssemblyContents |
| **Total** | **9** errors, **7** warnings, **21** suggestions | 5 files |

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph (short description) in each topic per DITA convention.
- **AssemblyContents:** In *virt-node-maintenance.adoc* (line 83) and *virt-triggering-vm-failover-resolving-failed-node.adoc* (line 21), ensure only “additional resources”–type content follows include directives (or restructure per AsciiDocDITA.AssemblyContents).
- **RelatedLinks:** In *virt-activating-ksm.adoc* (line 32), ensure only link content appears in the related-links section (AsciiDocDITA.RelatedLinks).
- **RedHat.TermsErrors:** In *virt-managing-node-labeling-obsolete-cpu-models.adoc* (line 9), replace the flagged term with “if” or “provided that” as appropriate.
- **Broken xrefs:** Update or remove the two xrefs whose anchors are not present in the target files (or confirm against published build IDs).
- **RedHat:** Address passive voice, definitions (VMIs), spelling (e.g. “unschedulable”), and simple language where flagged.

---

## 6. Next steps

1. Fix all 9 Vale errors (ShortDescription, AssemblyContents, RelatedLinks, TermsErrors).
2. Resolve 2 broken xref anchors (or validate against published docs).
3. Work through Vale warnings and suggestions for style compliance.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
