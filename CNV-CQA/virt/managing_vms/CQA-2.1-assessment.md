# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/managing_vms/`  
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
# Top-level files only (14 files):
vale --config=.vale-cqa.ini virt/managing_vms/*.adoc
# Subdirs (run separately if needed):
vale --config=.vale-cqa.ini virt/managing_vms/advanced_vm_management/*.adoc
vale --config=.vale-cqa.ini virt/managing_vms/virtual_disks/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Full coverage (all 38 files):**

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| Top-level `virt/managing_vms/*.adoc` | 25 | 13 | 64 | 14 |
| `advanced_vm_management/*.adoc` | 24 | 32 | 55 | 19 |
| `virtual_disks/*.adoc` | 7 | 1 | 8 | 5 |
| **Total** | **56** | **46** | **127** | **38** |

**CQA pre-migration (row 37):** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

**Re-run (full DITA check):**
```bash
vale --config=.vale-cqa.ini virt/managing_vms/*.adoc
vale --config=.vale-cqa.ini virt/managing_vms/advanced_vm_management/*.adoc
vale --config=.vale-cqa.ini virt/managing_vms/virtual_disks/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Does not meet** for `virt/managing_vms/` — **24** of the 32 virt-branch TOC violations are under `managing_vms`:

- **virt / managing_vms / advanced_vm_management /** — 19 level-4 nodes (About high availability…, About multi-queue…, Assigning compute resources, Configuring PCI passthrough, PXE booting, USB host passthrough, Application-Aware Quota Operator, default CPU model, virtual GPUs, Control plane tuning, dedicated resources, descheduler evictions, OpenShift GitOps, Scheduling VMs, Specifying nodes, UEFI mode, huge pages, NUMA topology, resource quotas).
- **virt / managing_vms / virtual_disks /** — 5 level-4 nodes (Configuring shared volumes, Expanding VM disks, Hot-plugging VM disks, Inserting CD-ROMs…, Migrating VM disks…).

Flatten the topic map under `managing_vms` so no node exceeds level 3 (e.g. promote level-4 entries or merge sections).

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
python3 virt/install/check_broken_links.py virt/managing_vms
```

**Result:** **18 issue(s)** in 38 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 18 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Files with issues (sample):** `advanced_vm_management/virt-NUMA-topology.adoc`, `advanced_vm_management/virt-configuring-pci-passthrough.adoc`, `advanced_vm_management/virt-schedule-vms.adoc`, `advanced_vm_management/virt-understanding-aaq-operator.adoc`, `advanced_vm_management/virt-working-with-resource-quotas-for-vms.adoc`, `virt-accessing-vm-consoles.adoc`, `virt-accessing-vm-ssh.adoc`, `virt-edit-vms.adoc`, `virt-enabling-disabling-vm-delete-protection.adoc`, `virt-exporting-vms.adoc`, `virt-managing-vms-openshift-pipelines.adoc`.

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/managing_vms
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/managing_vms
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **14** `virt/managing_vms/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| `virt-accessing-vm-consoles.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-accessing-vm-consoles.adoc` | 75 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-accessing-vm-ssh.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-accessing-vm-ssh.adoc` | 33 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-accessing-vm-ssh.adoc` | 42 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `virt-list-vms.adoc` | 4 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-manage-vmis.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-managing-vms-openshift-pipelines.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-managing-vms-openshift-pipelines.adoc` | 32 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-migrating-vms-in-single-cluster-to-different-storage-class.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-using-vtpm-devices.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `advanced_vm_management/virt-configuring-pci-passthrough.adoc` | 38, 43, 48 | LineBreak | Hard line breaks are not supported in DITA. |

**Summary (top-level only):** 25 Vale errors in 14 files; DITA types above: ShortDescription (7), AssemblyContents (3), NestedSection (1), LineBreak (3). **Full DITA check** for subdirs below (Section 2.4).

---

## 2.4 DITA full check: `advanced_vm_management/` and `virtual_disks/`

Vale (RedHat + AsciiDocDITA) was run on both subdirectories for full coverage.

### advanced_vm_management/

**Command:** `vale --config=.vale-cqa.ini virt/managing_vms/advanced_vm_management/*.adoc`

**Result:** 24 errors, 32 warnings, 55 suggestions in **19 files**.

**DITA errors (AsciiDocDITA) in advanced_vm_management/:**

| File | Line | Rule | Message |
|------|------|------|---------|
| `virt-about-multi-queue.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph for `<shortdesc>` in DITA. |
| `virt-assigning-compute-resources.adoc` | 3 | ShortDescription | Same. |
| `virt-assigning-compute-resources.adoc` | 26 | TaskStep | Content other than a single list cannot be mapped to DITA steps. |
| `virt-NUMA-topology.adoc` | 4 | ShortDescription | Same. |
| `virt-NUMA-topology.adoc` | 16 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-schedule-vms.adoc` | 3 | ShortDescription | Same. |
| `virt-specifying-nodes-for-vms.adoc` | 3 | ShortDescription | Same. |
| `virt-specifying-nodes-for-vms.adoc` | 14 | AssemblyContents | Same. |
| `virt-uefi-mode-for-vms.adoc` | 3 | ShortDescription | Same. |
| `virt-understanding-aaq-operator.adoc` | 3 | ShortDescription | Same. |
| `virt-using-huge-pages-with-vms.adoc` | 3 | ShortDescription | Same. |
| `virt-vm-control-plane-tuning.adoc` | 3 | ShortDescription | Same. |

*Additional DITA errors may appear in other advanced_vm_management files (output truncated); run Vale locally for the full list.*

### virtual_disks/

**Command:** `vale --config=.vale-cqa.ini virt/managing_vms/virtual_disks/*.adoc`

**Result:** 7 errors, 1 warning, 8 suggestions in **5 files**.

**DITA errors (AsciiDocDITA) in virtual_disks/:**

| File | Line | Rule | Message |
|------|------|------|---------|
| `virt-configuring-shared-volumes-for-vms.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph for `<shortdesc>` in DITA. |
| `virt-expanding-vm-disks.adoc` | 3 | ShortDescription | Same. |
| `virt-expanding-vm-disks.adoc` | 18 | BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| `virt-expanding-vm-disks.adoc` | 18 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-expanding-vm-disks.adoc` | 26 | BlockTitle | Same. |
| `virt-hot-plugging-virtual-disks.adoc` | 3 | ShortDescription | Same. |
| `virt-migrating-storage-class.adoc` | 4 | ShortDescription | Same. |

**Combined (managing_vms full):** 56 errors, 46 warnings in 38 files. Fix all DITA errors (ShortDescription, AssemblyContents, NestedSection, LineBreak, BlockTitle, TaskStep) to pass the asciidoctor-dita-vale check.

---

## 3. Pre-migration requirements (CQA 2.1)

### 3.1 AsciiDoc / Vale (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Content passes Vale asciidoctor-dita-vale check with **no errors or warnings** | **Does not meet** | 56 errors, 46 warnings in 38 files (Sections 2.3, 2.4, and 4). |
| Assemblies: only intro + include statements; optional Additional resources at end; **no text between include statements** | **Does not meet** | AsciiDocDITA.AssemblyContents: content after includes in multiple files (e.g. virt-accessing-vm-consoles, virt-accessing-vm-ssh, virt-managing-vms-openshift-pipelines). |

### 3.2 Short descriptions (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Modules/assemblies have a clear short description ([role="_abstract"]); 50–300 chars; single paragraph; blank line after level-0 title | **Does not meet** | AsciiDocDITA.ShortDescription: add paragraph with `[role="_abstract"]` in multiple files across top-level, advanced_vm_management/, and virtual_disks/ (Sections 2.3 and 2.4). |

### 3.3 DITA / structure (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No level 2–5 sections in assemblies (DITA maps do not support nested sections in this way in the assembly) | **Does not meet** | AsciiDocDITA.NestedSection in virt-accessing-vm-ssh.adoc (L42). Move level 2+ content into modules. |
| Content is not deeply nested in the TOC (recommended: no more than 3 levels) | **Does not meet** | 24 nodes under managing_vms at level 4 (Section 2.1). Flatten topic map. |

### 3.4 Red Hat style / terminology (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Official product names; consistent terminology | **Partially meets** | 46 warnings across 38 files (e.g. RedHat.Spelling: virtctl, VMIs, viostor, viorng, multiqueue, vNICs; RedHat.CaseSensitiveTerms: SSH; RedHat.TermsWarnings: may, can not). |
| Content grammatically correct; American English | **Partially meets** | Multiple suggestions (passive voice, simple words, definitions, sentence length, symbols). |

### 3.5 URLs and links (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No broken links | **Review** | 18 xref anchor mismatches (Section 2.2). Verify with `--validate-against` or fix anchors. |

---

## 4. Breakdown by file and rule type

### 4.1 DITA / AsciiDocDITA (must fix for migration)

- **ShortDescription (error):** Add proper short description paragraph with `[role="_abstract"]` in all modules that lack it (top-level, advanced_vm_management/, virtual_disks/ — see Sections 2.3 and 2.4).
- **AssemblyContents (error):** No content other than “Additional resources” after include directives (e.g. virt-accessing-vm-consoles, virt-accessing-vm-ssh, virt-managing-vms-openshift-pipelines, virt-NUMA-topology, virt-specifying-nodes-for-vms, virt-expanding-vm-disks).
- **NestedSection (error):** virt-accessing-vm-ssh.adoc L42 — move level 2+ sections into included modules.
- **LineBreak (error):** advanced_vm_management/virt-configuring-pci-passthrough.adoc L38, 43, 48 — hard line breaks not supported in DITA; use paragraphs or lists.
- **BlockTitle (error):** In DITA, block titles only on examples, figures, tables (e.g. virtual_disks/virt-expanding-vm-disks.adoc L18, 26).
- **TaskStep (error):** Content other than a single list cannot be mapped to DITA steps (e.g. advanced_vm_management/virt-assigning-compute-resources.adoc L26).

### 4.2 Red Hat style — warnings (should fix)

- **Full coverage:** 46 warnings across 38 files (top-level 13, advanced_vm_management 32, virtual_disks 1).
- **RedHat.Spelling:** virtctl, VMIs, viostor, viorng, Tx, multiqueue, vNICs, vhost, VM's, preallocation (add to vocabulary or accept).
- **RedHat.CaseSensitiveTerms:** Use “SSH” not “ssh”.
- **RedHat.TermsWarnings:** Consider “might” or “can” rather than “may”; “cannot” rather than “can not” where appropriate.
- **RedHat.Using:** Use “by using” instead of “using” when it follows a noun.

### 4.3 Red Hat style — suggestions (improve quality)

- Passive voice, simple words, acronym definitions (e.g. EFI, PCI), sentence length, Pascal/camel case (e.g. ArtifactHub, VirtIO), avoid “&” symbol per style guide.

---

## 5. Quality tab (post-migration)

To be assessed after migration; not blocking for pre-migration:

- Content is scannable (short sentences/paragraphs, lists, graphics).
- Content is user-focused (persona, pain points, new terms defined).
- Procedures: ≤10 steps, examples, verification steps, optional/conditional formatting.
- Editorial: minimum style guide, conversational tone, conscious language, table/image captions and alt text.
- Links: relevant in-content and Additional resources; non–Red Hat links approved or disclaimed.

---

## 6. Recommended next steps

1. **Fix all Vale errors (56)**  
   - **ShortDescription:** add `[role="_abstract"]` paragraph in every module that reports this (top-level, advanced_vm_management/, virtual_disks/).  
   - **AssemblyContents:** remove or relocate content after include directives (see Sections 2.3 and 2.4).  
   - **NestedSection:** move level 2+ sections into modules in virt-accessing-vm-ssh.adoc.  
   - **LineBreak:** replace hard line breaks in advanced_vm_management/virt-configuring-pci-passthrough.adoc with DITA-safe markup.  
   - **BlockTitle:** fix or remove block titles that are not on examples, figures, or tables (e.g. virtual_disks/virt-expanding-vm-disks.adoc).  
   - **TaskStep:** ensure procedure content maps to a single step list (e.g. advanced_vm_management/virt-assigning-compute-resources.adoc).

2. **Address Vale warnings (46)**  
   - Spelling, case (SSH), terms (may, can not, like), “by using” vs “using”. See Section 4.2.

3. **Re-run Vale (full DITA check)**  
   - `vale --config=.vale-cqa.ini virt/managing_vms/*.adoc`  
   - `vale --config=.vale-cqa.ini virt/managing_vms/advanced_vm_management/*.adoc`  
   - `vale --config=.vale-cqa.ini virt/managing_vms/virtual_disks/*.adoc`  
   - Target: **0 errors, 0 warnings** for pre-migration sign-off.

4. **Flatten TOC under managing_vms (max level 3)**  
   - Restructure `_topic_maps/_topic_map.yml` so no node under virt/managing_vms exceeds level 3 (24 nodes currently at level 4).

5. **Verify links**  
   - Run broken-links check; optionally `--validate-against <OCP virt docs URL>`. Fix or confirm the 18 xref anchors.

6. **Complete remaining pre-migration items**  
   - Modularization, templates, procedures, editorial, URLs, legal/branding per CQA 2.1 Pre-migration tab.

---

## 7. References

- CQA 2.1 — Content Quality Assessment (PDF)
- [ToolX migration tool page](https://toolbox.redhat.com/) (Vale asciidoctor-dita-vale)
- [AsciiDocDITA (asciidoctor-dita-vale)](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- Vale config used: `.vale-cqa.ini` (RedHat + AsciiDocDITA only)
- TOC level check: [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local: `virt/install/check_toc_level.py`)
- Broken links / xrefs / includes: [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) (local: `virt/install/check_broken_links.py`)
