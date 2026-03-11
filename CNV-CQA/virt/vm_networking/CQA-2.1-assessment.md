# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/vm_networking/`  
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
# All files in virt/vm_networking (18 files, no subdirs):
vale --config=.vale-cqa.ini virt/vm_networking/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/vm_networking/*.adoc` (18 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/vm_networking/*.adoc` | 23 | 30 | 77 | 18 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/vm_networking/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/vm_networking/` — No TOC violations under `vm_networking`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/vm_networking
```

**Result:** **32 issue(s)** in 18 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 32 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Files with issues (sample):** *virt-accessing-vm-internal-fqdn.adoc*, *virt-accessing-vm-secondary-network-fqdn.adoc*, *virt-connecting-vm-to-default-pod-network.adoc*, *virt-connecting-vm-to-linux-bridge.adoc* (5 xrefs), *virt-connecting-vm-to-ovn-secondary-network.adoc*, *virt-connecting-vm-to-primary-udn.adoc*, *virt-connecting-vm-to-secondary-udn.adoc*, *virt-connecting-vm-to-sriov.adoc* (3 xrefs), *virt-dedicated-network-live-migration.adoc*, *virt-exposing-vm-with-service.adoc*, *virt-hot-plugging-network-interfaces.adoc* (3 xrefs), *virt-networking-overview.adoc* (6 xrefs), *virt-using-dpdk-with-sriov.adoc* (2 xrefs), and others. Many targets are internal (same or other virt modules) or point to networking/operators; anchors are often context-generated section IDs.

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/vm_networking
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/vm_networking
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **18** `virt/vm_networking/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-accessing-vm-internal-fqdn.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-accessing-vm-secondary-network-fqdn.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-configuring-viewing-ips-for-vms.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-configuring-viewing-ips-for-vms.adoc | 27 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-connecting-vm-to-default-pod-network.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-connecting-vm-to-linux-bridge.adoc | 27 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-connecting-vm-to-ovn-secondary-network.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-connecting-vm-to-ovn-secondary-network.adoc | 47 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-connecting-vm-to-primary-udn.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-connecting-vm-to-primary-udn.adoc | 46 | AsciiDocDITA.BlockTitle | Block titles only on examples, figures, tables |
| virt-connecting-vm-to-primary-udn.adoc | 46 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-connecting-vm-to-primary-udn.adoc | 61 | AsciiDocDITA.BlockTitle | Block titles only on examples, figures, tables |
| virt-connecting-vm-to-secondary-udn.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-connecting-vm-to-service-mesh.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-dedicated-network-live-migration.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-exposing-vm-with-service.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-hot-plugging-network-interfaces.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-networking-overview.adoc | 52 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-networking-overview.adoc | 207 | AsciiDocDITA.NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| virt-setting-interface-link-state.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-using-dpdk-with-sriov.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-using-dpdk-with-sriov.adoc | 31 | AsciiDocDITA.RelatedLinks | Content other than links cannot be mapped to DITA related-links. |

**Total:** 23 DITA errors (14 ShortDescription, 5 AssemblyContents, 2 BlockTitle, 1 NestedSection, 1 RelatedLinks) across 15 files. *virt-configuring-physical-networks.adoc* and *virt-using-mac-address-pool-for-vms.adoc* have no DITA errors.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 23 errors (DITA) |
| Vale — no warnings | Does not meet | 30 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under vm_networking |
| No broken links | Does not meet | 32 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| virt-accessing-vm-internal-fqdn.adoc | 1 | ShortDescription |
| virt-accessing-vm-secondary-network-fqdn.adoc | 1 | ShortDescription |
| virt-configuring-physical-networks.adoc | 0 | — |
| virt-configuring-viewing-ips-for-vms.adoc | 2 | ShortDescription, AssemblyContents |
| virt-connecting-vm-to-default-pod-network.adoc | 1 | ShortDescription |
| virt-connecting-vm-to-linux-bridge.adoc | 1 | AssemblyContents |
| virt-connecting-vm-to-ovn-secondary-network.adoc | 2 | ShortDescription, AssemblyContents |
| virt-connecting-vm-to-primary-udn.adoc | 4 | ShortDescription, BlockTitle (46), AssemblyContents (46), BlockTitle (61) |
| virt-connecting-vm-to-secondary-udn.adoc | 1 | ShortDescription |
| virt-connecting-vm-to-service-mesh.adoc | 1 | ShortDescription |
| virt-connecting-vm-to-sriov.adoc | 0 | — |
| virt-dedicated-network-live-migration.adoc | 1 | ShortDescription |
| virt-exposing-vm-with-service.adoc | 1 | ShortDescription |
| virt-hot-plugging-network-interfaces.adoc | 1 | ShortDescription |
| virt-networking-overview.adoc | 2 | AssemblyContents, NestedSection |
| virt-setting-interface-link-state.adoc | 1 | ShortDescription |
| virt-using-dpdk-with-sriov.adoc | 2 | ShortDescription, RelatedLinks |
| virt-using-mac-address-pool-for-vms.adoc | 0 | — |
| **Total** | **23** errors, **30** warnings, **77** suggestions | 18 files |

*virt-connecting-vm-to-sriov.adoc* has no DITA errors but has broken xrefs from other files pointing to it.

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph in each topic per DITA convention (14 files, line 3).
- **AssemblyContents:** Ensure only “additional resources”–type content follows include directives in *virt-configuring-viewing-ips-for-vms.adoc* (27), *virt-connecting-vm-to-linux-bridge.adoc* (27), *virt-connecting-vm-to-ovn-secondary-network.adoc* (47), *virt-connecting-vm-to-primary-udn.adoc* (46), *virt-networking-overview.adoc* (52); restructure if needed.
- **BlockTitle:** In *virt-connecting-vm-to-primary-udn.adoc* (lines 46, 61), use block titles only on examples, figures, or tables.
- **NestedSection:** In *virt-networking-overview.adoc* (line 207), level-2+ sections are not supported in DITA; restructure (e.g. split topics or use supported structures).
- **RelatedLinks:** In *virt-using-dpdk-with-sriov.adoc* (line 31), ensure only link content in the related-links section.
- **Broken xrefs:** Update or remove the 32 xrefs whose anchors are not present in targets (or validate against published build IDs). Many are section anchors in virt or networking docs.
- **RedHat:** Address spelling (e.g. “localnet”, “NICs”, “VLANs”), passive voice, sentence-style headings, PascalCamelCase (KubeMacPool, etc.), and terminology where flagged.

---

## 6. Next steps

1. Fix all 23 DITA errors (ShortDescription, AssemblyContents, BlockTitle, NestedSection, RelatedLinks).
2. Resolve 32 broken xref anchors (or validate against published docs).
3. Work through Vale warnings and suggestions for style compliance.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
