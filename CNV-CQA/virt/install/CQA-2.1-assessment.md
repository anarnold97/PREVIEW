# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/install/`  
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
vale --config=.vale-cqa.ini virt/install/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

| Severity   | Count |
|-----------|--------|
| **Errors** | 23 |
| **Warnings** | 20 |
| **Suggestions** | 37 |
| **Files** | 4 |

**CQA pre-migration (row 37):** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

*(Full Vale output: run `vale --config=.vale-cqa.ini virt/install/*.adoc` from repo root.)*

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Does not meet** — 32 node(s) in the **virt** branch have TOC level > 3 (all at level 4).

| TOC path | Name (sample) |
|----------|----------------|
| virt / creating_vms_advanced / creating_vms_advanced_web / … | Cloning VMs; Creating VMs by importing images…; Creating VMs by uploading images; Creating virtual machines from Red Hat images; Heterogeneous cluster support |
| virt / creating_vms_advanced / creating_vms_cli / … | Creating VMs by cloning PVCs; Creating VMs by using container disks; Creating virtual machines from the command line |
| virt / managing_vms / advanced_vm_management / … | About high availability…; About multi-queue…; Assigning compute resources; Configuring PCI passthrough; Configuring PXE booting…; Configuring USB host passthrough; Configuring the Application-Aware Quota Operator; Configuring the default CPU model; Configuring virtual GPUs; Control plane tuning; Enabling dedicated resources…; Enabling descheduler evictions…; Managing VMs by using OpenShift GitOps; Scheduling VMs; Specifying nodes for VMs; UEFI mode for VMs; Using huge pages…; Working with NUMA topology…; Working with resource quotas… |
| virt / managing_vms / virtual_disks / … | Configuring shared volumes; Expanding VM disks; Hot-plugging VM disks; Inserting CD-ROMs…; Migrating VM disks… |

**Note:** The `virt/install/` content itself is not among the violating nodes; violations are under `creating_vms_advanced` and `managing_vms`. For the full virt branch to meet CQA, the topic map should be flattened so no node exceeds level 3 (e.g. promote or merge level-4 entries).

**Re-run:**

```bash
# From repo root; limit to virt branch
python3 virt/install/check_toc_level.py virt
```

---

## 2.2 Broken links / xrefs / includes check

**Script:** [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) (local copy: `virt/install/check_broken_links.py`)

**Requirement (CQA Pre-migration):** No broken links.

**Command run (local xref + include validation):**

```bash
python3 virt/install/check_broken_links.py virt/install
```

**Result:** **24 issue(s)** in 4 files (xref only; includes resolved successfully).

| Category | Count | Notes |
|----------|--------|--------|
| **Target file not found** | 4 | xrefs to `../../rosa_cluster_admin/...` and `../../osd_cluster_admin/...` (`.html` targets — build output; not present as source in repo). |
| **Anchor not found** | 20 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source. Many IDs are build-generated or use `{context}`; local check can yield false positives. |

**Files with issues:** `virt/install/installing-virt.adoc`, `virt/install/preparing-cluster-for-virt.adoc`, `virt/install/uninstalling-virt.adoc`.

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs (resolves to HTML URLs and checks with HTTP):

```bash
# Red Hat OCP virtualization (adjust version as needed)
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/install

# Optional: validate external link: URLs
python3 virt/install/check_broken_links.py --check-urls virt/install
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/install
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in `virt/install/` (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| `installing-virt.adoc` | 4 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `installing-virt.adoc` | 42 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `installing-virt.adoc` | 42 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `preparing-cluster-for-virt.adoc` | 4 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `preparing-cluster-for-virt.adoc` | 119 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `preparing-cluster-for-virt.adoc` | 119 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `preparing-cluster-for-virt.adoc` | 229 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `preparing-cluster-for-virt.adoc` | 248 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `preparing-cluster-for-virt.adoc` | 262 | NestedSection | Level 2, 3, 4, and 5 sections are not supported in DITA. |
| `uninstalling-virt.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |

**Summary:** 10 DITA errors in 3 files. `virt-install-ibm-cloud-bm-nodes.adoc` has no AsciiDocDITA errors.

---

## 3. Pre-migration requirements (CQA 2.1)

### 3.1 AsciiDoc / Vale (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Content passes Vale asciidoctor-dita-vale check with **no errors or warnings** | **Does not meet** | 23 errors, 20 warnings. See Section 4. |
| Assemblies: only intro + include statements; optional Additional resources at end; **no text between include statements** | **Does not meet** | AsciiDocDITA.AssemblyContents errors: content after includes in `installing-virt.adoc` (line 42), `preparing-cluster-for-virt.adoc` (line 119). |

### 3.2 Short descriptions (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Modules/assemblies have a clear short description ([role="_abstract"]); 50–300 chars; single paragraph; blank line after level-0 title | **Does not meet** | AsciiDocDITA.ShortDescription: `[role="_abstract"]` must be assigned to a paragraph in all four assemblies (installing-virt, preparing-cluster-for-virt, uninstalling-virt, virt-install-ibm-cloud-bm-nodes). |

### 3.3 DITA / structure (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No level 2–5 sections in assemblies (DITA maps do not support nested sections in this way in the assembly) | **Does not meet** | AsciiDocDITA.NestedSection: multiple level 2+ sections in assemblies (e.g. installing-virt.adoc L42, preparing-cluster-for-virt.adoc L119, 229, 248, 262). Content must be moved into included modules. |
| Content is not deeply nested in the TOC (recommended: no more than 3 levels) | **Does not meet** | TOC check: 32 nodes in virt branch at level 4 (see Section 2.1). Flatten topic map for creating_vms_advanced and managing_vms. |

### 3.4 Red Hat style / terminology (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Official product names; consistent terminology | **Partially meets** | RedHat.TermsErrors: e.g. "bare metal" → "bare-metal"; "IPI" → "installer-provisioned infrastructure"; "Bare metal" → "bare-metal" (hyphenation and casing). |
| Content grammatically correct; American English | **Partially meets** | RedHat spelling/case: e.g. "Knowledgebase", "hot plug"/"Hotplug", "Intel Virtualization Technology" (not "VT"); RedHat.GitLinks: one github.com link to verify. |

### 3.5 URLs and links (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No broken links | **Review** | Broken-links check: 24 xref issues (4 missing .html targets for ROSA/OSD; 20 anchor mismatches — verify with `--validate-against`). See Section 2.2. |

---

## 4. Breakdown by file and rule type

### 4.1 DITA / AsciiDocDITA (must fix for migration)

- **ShortDescription (error):** All 4 assemblies need `[role="_abstract"]` on a **paragraph** (not only the role on a line by itself).
- **AssemblyContents (error):** No content other than “Additional resources” after include directives. Fix: move “Next steps” and any other content in `installing-virt.adoc` and `preparing-cluster-for-virt.adoc` into modules or restructure so assemblies contain only intro + includes + optional Additional resources.
- **NestedSection (error):** Level 2–5 sections are not supported in the assembly; move into included modules.

### 4.2 Red Hat style — errors (must fix)

- **TermsErrors:** “bare metal” → “bare-metal” (and “Bare metal” → “bare-metal”); “IPI” → “installer-provisioned infrastructure” (or add to glossary and use per style guide).

### 4.3 Red Hat style — warnings (should fix)

- **Spelling/Case:** LPARs, Portworx, FSx, Hotplug → “hot plug”, Multus, Knowledgebase, etc. Add to vocabulary or fix per Red Hat style.
- **RedHat.GitLinks:** One link to github.com — confirm approval per CQA.
- **RedHat.Hyphens:** e.g. “Hotplug” → “hot plug”.
- **RedHat.CaseSensitiveTerms:** “VT” → “Intel Virtualization Technology”; “knowledgebase” → “Knowledgebase”.
- **RedHat.DoNotUseTerms:** Avoid “respective”/“respectively”.
- **RedHat.TermsWarnings:** e.g. “execute” → consider “run”, “issue”, “start”, or “enter”.

### 4.4 Red Hat style — suggestions (improve quality)

- Readability: Flesch–Kincaid grade level slightly above 9 (aim for ≤9).
- Headings: sentence-style capitalization.
- Passive voice, acronyms (define on first use), simple words, “that”/“which” where appropriate.

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

1. **Fix all Vale errors (23)**  
   - ShortDescription: add proper short description paragraph with `[role="_abstract"]` in each assembly.  
   - AssemblyContents: remove or relocate content that appears after include directives so assemblies contain only intro + includes + optional Additional resources.  
   - NestedSection: move level 2+ sections into modules and include them.  
   - RedHat.TermsErrors: apply “bare-metal” and “installer-provisioned infrastructure” (or approved equivalents).

2. **Address Vale warnings (20)**  
   - Terminology, spelling, case, hyphens, Git links, and “respective”/“execute” as above.

3. **Re-run Vale with CQA config**  
   - `vale --config=.vale-cqa.ini virt/install/*.adoc`  
   - Target: **0 errors, 0 warnings** for pre-migration sign-off.

4. **Optionally improve suggestions**  
   - Readability, headings, passive voice, definitions, simple words (Quality tab).

5. **Complete remaining pre-migration items**  
   - Modularization, templates, titles/short descriptions, procedures (prerequisites, labels), editorial, URLs, legal/branding per CQA 2.1 Pre-migration tab.

6. **Flatten TOC for virt branch (max level 3)**  
   - Run `python3 virt/install/check_toc_level.py virt` until 0 violations. Restructure `_topic_maps/_topic_map.yml` under virt so no node exceeds level 3 (e.g. under creating_vms_advanced, managing_vms/advanced_vm_management, managing_vms/virtual_disks).

7. **Verify links (no broken links)**  
   - Run `python3 virt/install/check_broken_links.py virt/install` (local). For published-docs validation, run with `--validate-against <OCP virt docs URL>`. Fix or confirm ROSA/OSD .html xrefs and any anchor mismatches. Optionally run with `--check-urls` for external `link:` URLs.

---

## 7. References

- CQA 2.1 — Content Quality Assessment (PDF)
- [ToolX migration tool page](https://toolbox.redhat.com/) (Vale asciidoctor-dita-vale)
- [AsciiDocDITA (asciidoctor-dita-vale)](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- Vale config used: `.vale-cqa.ini` (RedHat + AsciiDocDITA only)
- TOC level check: [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local: `virt/install/check_toc_level.py`)
- Broken links / xrefs / includes: [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) (local: `virt/install/check_broken_links.py`)
