# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/support/`  
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
# All files in virt/support (3 files, no subdirs):
vale --config=.vale-cqa.ini virt/support/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/support/*.adoc` (3 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/support/*.adoc` | 11 | 6 | 22 | 3 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/support/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/support/` — No TOC violations under `support`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/support
```

**Result:** **11 issue(s)** in 3 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 11 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issues:**

- **virt-collecting-virt-data.adoc** (7 xrefs):
  - → `../../support/getting-support.adoc#support-submitting-a-case_getting-support` — anchor not found.
  - → `../../support/gathering-cluster-data.adoc#support_gathering_data_gathering-cluster-data` — anchor not found.
  - → `../../virt/support/virt-collecting-virt-data.adoc#virt-using-virt-must-gather_virt-collecting-virt-data` — anchor not found (internal).
  - → `../../virt/managing_vms/virt-installing-qemu-guest-agent.adoc#virt-installing-qemu-guest-agent-on-linux-vm_virt-installing-qemu-guest-agent` — anchor not found.
  - → `../../virt/managing_vms/virt-installing-qemu-guest-agent.adoc#virt-installing-virtio-drivers-existing-windows_virt-installing-qemu-guest-agent` — anchor not found.
  - → `../../virt/support/virt-collecting-virt-data.adoc#virt-must-gather-options_virt-collecting-virt-data` — anchor not found (internal).
  - → `../../virt/support/virt-collecting-virt-data.adoc#virt-generating-a-vm-memory-dump_virt-collecting-virt-data` — anchor not found (internal).
- **virt-support-overview.adoc** (2 xrefs):
  - → `../../support/getting-support.adoc#support-submitting-a-case_getting-support` — anchor not found.
  - → `../../virt/support/virt-collecting-virt-data.adoc#virt-using-virt-must-gather_virt-collecting-virt-data` — anchor not found.
- **virt-troubleshooting.adoc** (2 xrefs):
  - → `../../nodes/clusters/nodes-containers-events.adoc#nodes-containers-events-list_nodes-containers-events` — anchor not found.
  - → `../../virt/support/virt-troubleshooting.adoc#virt-viewing-logs-loki_virt-troubleshooting` — anchor not found (internal).

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/support
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/support
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **3** `virt/support/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-collecting-virt-data.adoc | 37 | AsciiDocDITA.BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| virt-collecting-virt-data.adoc | 50 | AsciiDocDITA.BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| virt-collecting-virt-data.adoc | 68 | AsciiDocDITA.BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| virt-collecting-virt-data.adoc | 77 | AsciiDocDITA.BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| virt-support-overview.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-support-overview.adoc | 19 | AsciiDocDITA.NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| virt-support-overview.adoc | 26 | AsciiDocDITA.NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| virt-support-overview.adoc | 43 | AsciiDocDITA.NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| virt-troubleshooting.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-troubleshooting.adoc | 52 | AsciiDocDITA.AssemblyContents | Content other than additional resources cannot follow include directives. |
| virt-troubleshooting.adoc | 87 | AsciiDocDITA.BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |

**Total:** 11 DITA errors (2 ShortDescription, 3 NestedSection, 1 AssemblyContents, 5 BlockTitle) across 3 files.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 11 errors (DITA) |
| Vale — no warnings | Does not meet | 6 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under support |
| No broken links | Does not meet | 11 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| virt-collecting-virt-data.adoc | 4 | BlockTitle (lines 37, 50, 68, 77); 7 broken xrefs |
| virt-support-overview.adoc | 4 | ShortDescription, 3 NestedSection; 2 broken xrefs |
| virt-troubleshooting.adoc | 3 | ShortDescription, AssemblyContents, BlockTitle; 2 broken xrefs |
| **Total** | **11** errors, **6** warnings, **22** suggestions | 3 files |

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph in *virt-support-overview.adoc* and *virt-troubleshooting.adoc* (line 3) per DITA convention.
- **NestedSection:** In *virt-support-overview.adoc*, level-2+ sections (lines 19, 26, 43) are not supported in DITA; restructure (e.g. split into separate topics or use supported structures).
- **AssemblyContents:** In *virt-troubleshooting.adoc* (line 52), ensure only “additional resources”–type content follows include directives (or restructure per AsciiDocDITA.AssemblyContents).
- **BlockTitle:** In *virt-collecting-virt-data.adoc* (lines 37, 50, 68, 77) and *virt-troubleshooting.adoc* (line 87), use block titles only on examples, figures, or tables; convert other titled blocks to supported DITA elements.
- **Broken xrefs:** Update or remove the 11 xrefs whose anchors are not present in the target files (or confirm against published build IDs). Many are context-generated section IDs.
- **RedHat:** Address spelling (e.g. “Alertmanager”), simple language, passive voice, sentence-style headings, and PascalCamelCase (VirtualMachine, LokiStack, LogQL in backticks) where flagged.

---

## 6. Next steps

1. Fix all 11 DITA errors (ShortDescription, NestedSection, AssemblyContents, BlockTitle).
2. Resolve 11 broken xref anchors (or validate against published docs).
3. Work through Vale warnings and suggestions for style compliance.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
