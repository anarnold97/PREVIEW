# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/storage/`  
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
# All files in virt/storage (12 files, no subdirs):
vale --config=.vale-cqa.ini virt/storage/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/storage/*.adoc` (12 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/storage/*.adoc` | 12 | 15 | 30 | 12 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/storage/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/storage/` — No TOC violations under `storage`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/storage
```

**Result:** **4 issue(s)** in 12 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 4 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issues:**

- **virt-automatic-bootsource-updates.adoc** (2 xrefs):
  - → `../../virt/storage/virt-automatic-bootsource-updates.adoc#virt-disable-auto-updates-single-boot-source_virt-automatic-bootsource-updates` — anchor not found (ids include `virt-automatic-bootsource-updates`, `managing-custom-boot-source-updates_virt-automatic-bootsource-updates`, …).
  - → `../../storage/dynamic-provisioning.adoc#defining-storage-classes_dynamic-provisioning` — anchor not found (target has id `dynamic-provisioning`).
- **virt-preparing-cdi-scratch-space.adoc** → `../../storage/dynamic-provisioning.adoc#about_dynamic-provisioning` — anchor not found.
- **virt-storage-config-overview.adoc** → `../../storage/dynamic-provisioning.adoc#defining-storage-classes_dynamic-provisioning` — anchor not found.

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/storage
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/storage
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **12** `virt/storage/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| install-configure-fusion-access-san.adoc | 4 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| install-configure-fusion-access-san.adoc | 26 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-automatic-bootsource-updates.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-automatic-bootsource-updates.adoc | 27 | AsciiDocDITA.AssemblyContents | Content other than additional resources… |
| virt-configuring-cdi-for-namespace-resourcequota.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-configuring-local-storage-with-hpp.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-configuring-storage-profile.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-enabling-user-permissions-to-clone-datavolumes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-managing-data-volume-annotations.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-reserving-pvc-space-fs-overhead.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-storage-with-csi-paradigm.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-using-preallocation-for-datavolumes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |

**Total:** 12 DITA errors (10 ShortDescription, 2 AssemblyContents) across 10 files. *virt-preparing-cdi-scratch-space.adoc* and *virt-storage-config-overview.adoc* have no DITA errors (warnings/suggestions only).

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 12 errors (DITA) |
| Vale — no warnings | Does not meet | 15 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under storage |
| No broken links | Does not meet | 4 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| install-configure-fusion-access-san.adoc | 2 | ShortDescription, AssemblyContents |
| virt-automatic-bootsource-updates.adoc | 2 | ShortDescription, AssemblyContents; 2 broken xrefs |
| virt-configuring-cdi-for-namespace-resourcequota.adoc | 1 | ShortDescription |
| virt-configuring-local-storage-with-hpp.adoc | 1 | ShortDescription |
| virt-configuring-storage-profile.adoc | 1 | ShortDescription |
| virt-enabling-user-permissions-to-clone-datavolumes.adoc | 1 | ShortDescription |
| virt-managing-data-volume-annotations.adoc | 1 | ShortDescription |
| virt-preparing-cdi-scratch-space.adoc | 0 | 1 broken xref |
| virt-reserving-pvc-space-fs-overhead.adoc | 1 | ShortDescription |
| virt-storage-config-overview.adoc | 0 | Warnings/suggestions only; 1 broken xref |
| virt-storage-with-csi-paradigm.adoc | 1 | ShortDescription |
| virt-using-preallocation-for-datavolumes.adoc | 1 | ShortDescription |
| **Total** | **12** errors, **15** warnings, **30** suggestions | 12 files |

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph (short description) in each topic per DITA convention (10 files at line 3; *install-configure-fusion-access-san.adoc* at line 4).
- **AssemblyContents:** In *install-configure-fusion-access-san.adoc* (line 26) and *virt-automatic-bootsource-updates.adoc* (line 27), ensure only “additional resources”–type content follows include directives (or restructure per AsciiDocDITA.AssemblyContents).
- **Broken xrefs:** Update or remove the four xrefs whose anchors are not present in the target files (or confirm against published build IDs). Three point to `storage/dynamic-provisioning.adoc` with section anchors; one is an internal anchor in *virt-automatic-bootsource-updates.adoc*.
- **RedHat:** Address spelling (e.g. “DVs”, “preallocation”, “preallocate”), DoNotUseTerms (“overhead”), passive voice, product-centric writing, sentence-style headings, and PascalCamelCase (e.g. PersistentVolume in backticks) where flagged.

---

## 6. Next steps

1. Fix all 12 DITA errors (ShortDescription + AssemblyContents).
2. Resolve 4 broken xref anchors (or validate against published docs).
3. Work through Vale warnings and suggestions for style compliance.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
