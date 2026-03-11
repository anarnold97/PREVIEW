# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/live_migration/`  
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
vale --config=.vale-cqa.ini virt/live_migration/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

| Severity     | Count |
|-------------|--------|
| **Errors**  | 8     |
| **Warnings**| 2     |
| **Suggestions** | 17 |
| **Files**   | 6     |

**CQA pre-migration (row 37):** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors and warnings must be addressed before migration.

*(Full Vale output: run `vale --config=.vale-cqa.ini virt/live_migration/*.adoc` from repo root.)*

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/live_migration/` — No TOC violations occur under the `live_migration` path. The 32 nodes with level > 3 in the virt branch are under `creating_vms_advanced` and `managing_vms` only.

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
python3 virt/install/check_broken_links.py virt/live_migration
```

**Result:** **9 issue(s)** in 2 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 9 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Files with issues:** `virt/live_migration/virt-about-live-migration.adoc` (3), `virt/live_migration/virt-configuring-live-migration.adoc` (1), `virt/live_migration/virt-initiating-live-migration.adoc` (5).

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/live_migration
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/live_migration
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in `virt/live_migration/` (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| `virt-about-live-migration.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-about-live-migration.adoc` | 46 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-about-mtv-providers.adoc` | 16 | BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| `virt-configuring-live-migration.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-configuring-live-migration.adoc` | 25 | AssemblyContents | Content other than additional resources cannot follow include directives. |
| `virt-enabling-cclm-for-vms.adoc` | 3 | ShortDescription | Assign `[role="_abstract"]` to a paragraph to use it as `<shortdesc>` in DITA. |
| `virt-enabling-cclm-for-vms.adoc` | 12 | BlockTitle | Block titles can only be assigned to examples, figures, and tables in DITA. |
| `virt-initiating-live-migration.adoc` | 29 | AssemblyContents | Content other than additional resources cannot follow include directives. |

**Summary:** 8 DITA errors in 4 files. `virt-configuring-cross-cluster-live-migration-network.adoc` has no AsciiDocDITA errors.

---

## 3. Pre-migration requirements (CQA 2.1)

### 3.1 AsciiDoc / Vale (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Content passes Vale asciidoctor-dita-vale check with **no errors or warnings** | **Does not meet** | 8 errors, 2 warnings. See Section 2.3 and 4. |
| Assemblies: only intro + include statements; optional Additional resources at end; **no text between include statements** | **Does not meet** | AsciiDocDITA.AssemblyContents: content after includes in `virt-about-live-migration.adoc` (L46), `virt-configuring-live-migration.adoc` (L25), `virt-initiating-live-migration.adoc` (L29). |

### 3.2 Short descriptions (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Modules/assemblies have a clear short description ([role="_abstract"]); 50–300 chars; single paragraph; blank line after level-0 title | **Does not meet** | AsciiDocDITA.ShortDescription: add paragraph with `[role="_abstract"]` in `virt-about-live-migration.adoc`, `virt-configuring-live-migration.adoc`, `virt-enabling-cclm-for-vms.adoc`. |

### 3.3 DITA / structure (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No level 2–5 sections in assemblies (DITA maps do not support nested sections in this way in the assembly) | **Meets** | No NestedSection errors in live_migration. |
| Content is not deeply nested in the TOC (recommended: no more than 3 levels) | **Meets** | No TOC violations under live_migration (Section 2.1). |

### 3.4 Red Hat style / terminology (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| Official product names; consistent terminology | **Meets** | No RedHat.TermsErrors in this set. |
| Content grammatically correct; American English | **Partially meets** | 2 warnings (RedHat.Spelling: "Multus"); 17 suggestions (passive voice, simple words, definitions). |

### 3.5 URLs and links (required)

| Requirement | Assessment | Notes |
|-------------|------------|--------|
| No broken links | **Review** | 9 xref anchor mismatches (Section 2.2). Verify with `--validate-against` or fix anchors. |

---

## 4. Breakdown by file and rule type

### 4.1 DITA / AsciiDocDITA (must fix for migration)

- **ShortDescription (error):** Add proper short description paragraph with `[role="_abstract"]` in `virt-about-live-migration.adoc`, `virt-configuring-live-migration.adoc`, `virt-enabling-cclm-for-vms.adoc`.
- **AssemblyContents (error):** Ensure no content other than “Additional resources” after include directives in `virt-about-live-migration.adoc`, `virt-configuring-live-migration.adoc`, `virt-initiating-live-migration.adoc`.
- **BlockTitle (error):** In DITA, block titles are only for examples, figures, and tables. Fix in `virt-about-mtv-providers.adoc` (L16), `virt-enabling-cclm-for-vms.adoc` (L12).

### 4.2 Red Hat style — warnings (should fix)

- **RedHat.Spelling:** “Multus” not in dictionary (virt-about-live-migration.adoc L34, virt-configuring-live-migration.adoc L41). Add to vocabulary or accept.

### 4.3 Red Hat style — suggestions (improve quality)

- Passive voice, simple words (“sufficient”, “determine”, “approximate”, “Initiate”/“initiate”), acronym definitions (e.g. MTV), product-centric writing.

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

1. **Fix all Vale errors (8)**  
   - ShortDescription: add `[role="_abstract"]` paragraph in 3 assemblies.  
   - AssemblyContents: remove or relocate content after include directives in 3 files.  
   - BlockTitle: change or remove block titles that are not on examples, figures, or tables (2 files).

2. **Address Vale warnings (2)**  
   - “Multus” spelling (add to vocab or accept).

3. **Re-run Vale with CQA config**  
   - `vale --config=.vale-cqa.ini virt/live_migration/*.adoc`  
   - Target: **0 errors, 0 warnings** for pre-migration sign-off.

4. **Verify links**  
   - Run `python3 virt/install/check_broken_links.py virt/live_migration`; optionally `--validate-against <OCP virt docs URL>`. Fix or confirm the 9 xref anchors.

5. **Complete remaining pre-migration items**  
   - Modularization, templates, titles/short descriptions, procedures, editorial, URLs, legal/branding per CQA 2.1 Pre-migration tab.

---

## 7. References

- CQA 2.1 — Content Quality Assessment (PDF)
- [ToolX migration tool page](https://toolbox.redhat.com/) (Vale asciidoctor-dita-vale)
- [AsciiDocDITA (asciidoctor-dita-vale)](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- Vale config used: `.vale-cqa.ini` (RedHat + AsciiDocDITA only)
- TOC level check: [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local: `virt/install/check_toc_level.py`)
- Broken links / xrefs / includes: [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) (local: `virt/install/check_broken_links.py`)
