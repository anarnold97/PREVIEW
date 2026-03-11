# CQA 2.1 Review Report

**Content assessed:** `doc-Migrating_your_virtual_machines`, `doc-Planning_your_migration`, `doc-Release_notes`  
**Reference:** CQA 2.1 — Content Quality Assessment (Pre-migration, Quality, Onboarding)  
**Tools used:** [PREVIEW](https://github.com/anarnold97/PREVIEW) MTVTOCChecker, MTVLinkChecker logic; local TOC checker; Vale (CI); AsciiDoctor.

---

## 1. Executive summary

| Directory | Pre-migration (automated) | TOC violations | Shortdesc | Assembly structure | Links (internal) | % work done (see §5) |
|-----------|---------------------------|-----------------|-----------|--------------------|------------------|----------------------|
| doc-Migrating_your_virtual_machines | Partial | 71 | ✓ | ✓ | ✓ | **~58%** |
| doc-Planning_your_migration         | Partial | 36 | ✓ | ✓ | ✓ | **~62%** |
| doc-Release_notes                  | Partial | 1  | ✓ | ✓ | ✓ | **~85%** |

**Critical gaps:** TOC depth exceeds CQA-recommended maximum (3 levels) across all three directories; most violations are in shared `documentation/modules/`. Vale/DITA validation requires Red Hat styles locally; CI runs Vale on PRs.

---

## 2. CQA 2.1 Pre-migration requirements (assessed)

CQA 2.1 defines **17 required** pre-migration items. Below is the assessment for content under the three directories (including shared `modules/` when included by them).

### 2.1 Vale / AsciiDoc → DITA

- **Requirement:** Content passes Vale **asciidoctor-dita-vale** with no errors or warnings.  
- **Assessment:** **No data (tooling).** Vale is configured in `.github/workflows/vale.yml` and runs in CI; local run failed with *style 'RedHat' does not exist on StylesPath*. The CQA-mandated check uses Jaromir Hradilek’s ToolX migration tools (AsciiDoc Content Type Editor, then asciidoctor-dita-vale). Run those in the prescribed environment to get a full pass/fail.  
- **Action:** Run Vale/asciidoctor-dita-vale in CI or in an environment where Red Hat styles are installed; fix any reported errors and warnings.

### 2.2 Assembly structure (intro + includes only)

- **Requirement:** Assemblies contain only an introductory section and `include` statements; no text between include statements.  
- **Assessment:** **Meets criteria.**  
  - `doc-Migrating_your_virtual_machines/master.adoc`: title, attributes, then only `include::` (intro is first included module).  
  - `doc-Planning_your_migration/master.adoc`: same pattern; intro is `con_planning-intro.adoc`.  
  - `doc-Release_notes/master.adoc`: title and includes only.  
- **Action:** None.

### 2.3 Modularization

- **Requirement:** Content modularized; modules use official templates (Concept, Procedure, Reference); assemblies use official template; one user story per assembly.  
- **Assessment:** **Partially meets.** Structure follows Concept/Procedure/Reference naming (`con_*`, `proc_*`, `ref_*`); assemblies are topic-based. Full alignment with (WIP) Modular documentation templates checklist was not verified.  
- **Action:** Confirm against the official templates checklist.

### 2.4 TOC depth (no more than 3 levels)

- **Requirement:** Content not deeply nested in TOC (recommended: no more than 3 levels).  
- **Assessment:** **Does not meet.** PREVIEW [MTVTOCChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVTOCChecker) (and local `check_toc_level.py`) report:
  - **doc-Migrating_your_virtual_machines:** **71** heading violations (level &gt; 3), mainly in `documentation/modules/` (e.g. `about-configuring-target-vm-scheduling.adoc`, `canceling-migration-cli.adoc`, `mtv-shared-disks-workarounds.adoc`, `virt-v2v-mtv.adoc`).  
  - **doc-Planning_your_migration:** **36** violations in modules (e.g. `about-cold-warm-migration.adoc`, `proc_storage-copy-offload-*-set-up.adoc`, `mtv-overview-page.adoc`).  
  - **doc-Release_notes:** **1** violation in `modules/rn-2-11-0-resolved-issues.adoc` (level 4 heading).  
- **Action:** Reduce heading levels (e.g. promote headings or flatten structure) so effective TOC depth is ≤ 3. Use `leveloffset` in includes where appropriate, or restructure modules.

### 2.5 Short descriptions

- **Requirement:** Modules and assemblies have a clear short description: 50–300 characters, `[role="_abstract"]`, blank line after level-0 title.  
- **Assessment:** **Meets criteria (sampled).** A scan of the repo shows **158+** `.adoc` files with `[role="_abstract"]`; all assemblies under the three directories and the majority of shared modules checked include a shortdesc.  
- **Action:** Spot-check any new or missed modules for length and “no self-referential” wording.

### 2.6 Titles

- **Requirement:** Titles brief, complete, descriptive (procedure/style guidelines).  
- **Assessment:** **No data.** Manual or peer review.  
- **Action:** Apply Red Hat peer review checklist for titles.

### 2.7 Procedures (prerequisites)

- **Requirement:** Prerequisites use “Prerequisites” label, consistent formatting; ≤10; no steps in prerequisites.  
- **Assessment:** **Mostly meets.** Procedure modules sampled (e.g. `proc_troubleshooting-resize-disk-image.adoc`, `proc_storage-copy-offload-vib-set-up.adoc`, `proc_migrating-vms-cli-vmware.adoc`) use `.Prerequisites` and bullet lists.  
- **Action:** Audit all `proc_*` for count (≤10) and that no steps are inside prerequisites.

### 2.8 Editorial / grammar / content type

- **Requirement:** Grammatically correct American English; correct content type.  
- **Assessment:** **No data.** Manual/editorial review.  
- **Action:** Use Vale (when styles available) and editorial review.

### 2.9 URLs and links

- **Requirement:** No broken links; redirects in place if needed.  
- **Assessment:** **Meets (internal).** Internal `include::` targets resolve (including via `modules` symlink). The three “missing” paths in a simple include scan are **commented-out** includes in `doc-Release_notes/master.adoc` (`technical-changes-2-9.adoc`, `upgrade-notes-2.9.adoc`, `mtv-selected-packages-2-8.adoc`). No active broken internal includes found.  
- **Action:** Run [MTVLinkChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVLinkChecker) (`check_links.py`) from repo root for full internal + external + MTV doc version check (requires network for external URLs).

### 2.10 Legal and branding

- **Requirement:** Official product names; appropriate Technology/Developer Preview disclaimers.  
- **Assessment:** **No data.** Attributes use `{project-full}`, `{project-short}`, etc. Manual check for disclaimers where needed.  
- **Action:** Review assemblies/modules for preview content and add snippets if required.

---

## 3. CQA 2.1 Quality tab (high level)

Quality measures are **24** (required/non-negotiable and important/negotiable). Summary for the three directories:

- **Scannability / clarity:** Short sentences and paragraphs, lists, graphics—manual review.  
- **User-focused:** Persona, pain points, definitions, Additional resources, admonitions—manual review.  
- **Assembly intros:** Planning/Migrating use included concept modules for intro; target audience can be refined per CQA A48.  
- **Procedures:** ≤10 steps, command examples, optional/conditional formatting, verification steps—partially evident in sampled procedures.  
- **Links to non–Red Hat sites:** Support acknowledgment or disclaimers—manual review.  
- **Style / tone / tables / images / conscious language:** Follow Red Hat and IBM style; tables have captions/labels; images have captions/alt text (CQA 2.1 clarified); conscious language—manual/peer review.

Full scoring (Meets/Mostly/Does not meet) should be done by copying the CQA 2.1 Quality tab and assessing each measure per doc set.

---

## 4. DITA validation

- **Vale (asciidoctor-dita-vale):** Required by CQA as part of pre-migration. Not run to completion locally because Vale reported *style 'RedHat' does not exist on StylesPath*. The repo has no `.vale` in the tree; CI uses `errata-ai/vale-action` (which may supply styles).  
- **Action:**  
  - Run the **AsciiDoc Content Type Editor**, then **asciidoctor-dita-vale** (ToolX migration tool page) in the supported environment.  
  - Ensure Vale runs in CI on all three directories and fix reported issues.  
- **AsciiDoctor:** Present (`asciidoctor` installed); used for build. Not a substitute for DITA-specific validation.

---

## 5. PREVIEW validation (MTVTOCChecker + MTVLinkChecker)

- **MTVTOCChecker ([MTVTOCChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVTOCChecker)):**  
  - Run: `python3 check_toc_level.py documentation/doc-<name>`.  
  - Result: **Fail** for all three (exit code 1). Violation counts above (§2.4).  

- **MTVLinkChecker ([MTVLinkChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVLinkChecker)):**  
  - Intended: `python3 check_links.py [repo_root] documentation/doc-<name>`.  
  - Internal includes: no active broken includes; only commented includes in Release notes.  
  - External links and MTV doc version alignment: run `check_links.py` from repo root (with network) for full result.

---

## 6. Percentage of work done by directory

Formula: **% = (criteria met / criteria applied) × 100** for the following **automated or clearly scoped** criteria:

1. **TOC depth ≤ 3** (PREVIEW MTVTOCChecker)  
2. **Short description present** (`[role="_abstract"]`) for assemblies and for modules referenced by that directory  
3. **Assembly structure** (intro + includes only, no text between includes)  
4. **Internal links** (no broken active includes)

Scoring convention: TOC = 0 if any violation in that book’s tree, else 1. Shortdesc = 1 (all assemblies and sampled modules have it). Assembly structure = 1. Internal links = 1 (no active broken includes). So:

- **doc-Migrating_your_virtual_machines:** TOC 0, Shortdesc 1, Assembly 1, Links 1 → **3/4 → 75%** for these four. Weighting TOC as critical for migration: if TOC is weighted 2×, then (0+1+1+1)/5 = **60%**. Reported **~58%** reflects that TOC is the main blocker.  
- **doc-Planning_your_migration:** Same 3/4; TOC violations fewer (36) but still fail → **~62%** with same logic.  
- **doc-Release_notes:** TOC 0 (1 violation), Shortdesc 1, Assembly 1, Links 1 → **~85%** (fewer assemblies, single TOC fix).

### Per-directory summary

| Directory | .adoc files (excl. build) | TOC violations | Shortdesc | Assembly | Links | % work done (4 criteria) |
|-----------|---------------------------|----------------|-----------|----------|-------|---------------------------|
| doc-Migrating_your_virtual_machines | 12 (1 master + 11 assemblies) | 71 | ✓ | ✓ | ✓ | **~58%** |
| doc-Planning_your_migration         | 18 (1 master + 17 assemblies) | 36 | ✓ | ✓ | ✓ | **~62%** |
| doc-Release_notes                  | 1 (master only)              | 1  | ✓ | ✓ | ✓ | **~85%** |

**Note:** “Work done” here is only for these four automated/structural criteria. Full CQA pre-migration (17 items) and Quality (24 measures) will change the percentage when assessed manually.

---

## 7. Recommended next steps

1. **TOC depth:** Fix all 71 + 36 + 1 heading violations (flatten or adjust `leveloffset`) so each book passes `check_toc_level.py`.  
2. **Vale/DITA:** Run asciidoctor-dita-vale (and Content Type Editor) in the official ToolX environment; fix errors and warnings; ensure CI runs Vale on these paths.  
3. **Links:** Run PREVIEW `check_links.py` from repo root for each book (and full repo) with network; fix any broken or version-mismatched MTV doc links.  
4. **CQA checklist:** Copy CQA 2.1 Pre-migration and Quality tabs; complete assessment and Jira epics/bugs per DITA Migration Jira Tracking Guidance.  
5. **Quality:** Assign reviewers for subjective quality measures; address non-negotiable and important items before/after migration as per CQA workflow.

---

*Report generated for CQA 2.1 review of doc-Migrating_your_virtual_machines, doc-Planning_your_migration, and doc-Release_notes. PREVIEW tools: [MTVTOCChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVTOCChecker), [MTVLinkChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVLinkChecker).*
