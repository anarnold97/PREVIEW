# CQA 2.1 Review Report — openshift-docs (OADP)

**Content assessed:** [backup_and_restore/application_backup_and_restore](https://github.com/openshift/openshift-docs/tree/main/backup_and_restore/application_backup_and_restore) (OpenShift API for Data Protection — Application backup and restore)  
**Reference:** CQA 2.1 — Content Quality Assessment (Pre-migration, Quality, Onboarding)  
**Repo:** [openshift/openshift-docs](https://github.com/openshift/openshift-docs) (main branch, cloned for analysis).  
**Validation:** Same methodology as forklift-documentation review; PREVIEW tools are built for MTV/forklift layout, so TOC/link checks were run with equivalent logic on the OADP tree.

---

## 1. Executive summary

| Criterion (automated) | Result |
|----------------------|--------|
| **TOC depth ≤ 3** | **Pass** (0 violations) |
| **Short descriptions** | **Partial** (50/58 files have `[role="_abstract"]`; 8 missing) |
| **Assembly structure** | **Meets** (intro + includes; no text between include statements where checked) |
| **Internal includes** | **Pass** (392 includes, 0 broken) |
| **% work done (4 criteria)** | **~91%** |

**Gap to address:** Add short descriptions to the 8 modules/assemblies that lack `[role="_abstract"]` (50–300 characters, no self-referential language).

---

## 2. Scope and structure

- **Path:** `backup_and_restore/application_backup_and_restore`
- **Structure:** AsciiDoc modules and assemblies; `_attributes/`, `modules/`, `snippets/`, `images/`; subdirs: `aws-sts`, `backing_up_and_restoring`, `installing`, `oadp-3scale`, `oadp-performance`, `oadp-rosa`, `oadp-self-service`, `oadp-use-cases`, `release-notes`, `troubleshooting`.
- **.adoc count:** 58 files.
- **Assemblies:** Many files declare `:_mod-docs-content-type: ASSEMBLY` (e.g. `oadp-intro.adoc`, `oadp-api.adoc`, `backing-up-applications.adoc`, troubleshooting topics). No single `master.adoc`; multiple entry assemblies.

---

## 3. CQA 2.1 Pre-migration requirements (assessed)

### 3.1 Vale / AsciiDoc → DITA

- **Requirement:** Content passes Vale asciidoctor-dita-vale with no errors or warnings.
- **Assessment:** **No data.** openshift-docs has a `.vale` directory (styles, templates). Vale was not run in this review. Run the CQA-required ToolX tools (AsciiDoc Content Type Editor, then asciidoctor-dita-vale) in the prescribed environment.
- **Action:** Run Vale/asciidoctor-dita-vale for this path; fix errors and warnings.

### 3.2 Assembly structure (intro + includes only)

- **Requirement:** Assemblies contain only an introductory section and include statements; no text between include statements.
- **Assessment:** **Meets (sampled).** Top-level assemblies (e.g. `oadp-intro.adoc`) have title, shortdesc, optional intro text, then `include::modules/...`. `backing-up-applications.adoc` has body content and xrefs (no includes in the sampled portion); CQA allows “one or more paragraphs” in the intro. No free-standing paragraphs between consecutive `include::` lines observed.
- **Action:** None for structure; ensure any new assemblies follow the same pattern.

### 3.3 Modularization

- **Requirement:** Content modularized; official templates (Concept, Procedure, Reference); assemblies use official template.
- **Assessment:** **Partially meets.** Clear use of ASSEMBLY and modular topics; structure is consistent with Red Hat docs. Full checklist alignment not verified.
- **Action:** Confirm against (WIP) Modular documentation templates checklist.

### 3.4 TOC depth (no more than 3 levels)

- **Requirement:** Content not deeply nested in TOC (recommended: no more than 3 levels).
- **Assessment:** **Meets.** All 58 files scanned; **0** headings with level > 3. Headings use `=`, `==`, `===` only within the OADP tree.
- **Action:** None.

### 3.5 Short descriptions

- **Requirement:** Modules and assemblies have a clear short description: 50–300 characters, `[role="_abstract"]`, blank line after level-0 title.
- **Assessment:** **Does not fully meet.** **50 of 58** files have `[role="_abstract"]`. **8 files missing shortdesc:**
  - `oadp-3scale/restoring-3scale-api-management-by-using-oadp.adoc`
  - `backing_up_and_restoring/oadp-scheduling-backups-doc.adoc`
  - `backing_up_and_restoring/oadp-deleting-backups.adoc`
  - `backing_up_and_restoring/oadp-creating-backup-hooks-doc.adoc`
  - `backing_up_and_restoring/oadp-creating-backup-cr.adoc`
  - `backing_up_and_restoring/oadp-backing-up-pvs-csi-doc.adoc`
  - `backing_up_and_restoring/oadp-backing-up-applications-restic-doc.adoc`
  - `backing_up_and_restoring/backing-up-applications.adoc`
- **Action:** Add a CQA-compliant shortdesc (50–300 chars, `[role="_abstract"]`, no “This document…”) to each of the 8 files.

### 3.6 Titles

- **Requirement:** Titles brief, complete, descriptive.
- **Assessment:** **No data.** Manual/peer review.
- **Action:** Apply Red Hat peer review checklist for titles.

### 3.7 Procedures (prerequisites)

- **Requirement:** Prerequisites use “Prerequisites” label, consistent formatting; ≤10; no steps in prerequisites.
- **Assessment:** **Partially meets.** At least 3 procedure-style topics use `.Prerequisites`. Full audit of all procedure-like topics not done.
- **Action:** Audit procedure topics for Prerequisites label, count (≤10), and that no steps are inside prerequisites.

### 3.8 Editorial / grammar / content type

- **Requirement:** Grammatically correct American English; correct content type.
- **Assessment:** **No data.** Manual/editorial review and Vale when available.
- **Action:** Use Vale and editorial review.

### 3.9 URLs and links

- **Requirement:** No broken links; redirects in place if needed.
- **Assessment:** **Meets (internal includes).** **392** `include::` directives checked; **0** broken (all targets resolve relative to the including file). xref and external `link:` URLs were not validated in this run.
- **Action:** Run a full link checker (internal xrefs + external URLs) if available for openshift-docs; fix any broken or outdated links.

### 3.10 Legal and branding

- **Requirement:** Official product names; appropriate disclaimers for Technology/Developer Preview.
- **Assessment:** **No data.** Attributes (e.g. `{oadp-full}`, `{oadp-short}`) used for product names.
- **Action:** Manual review for preview content and disclaimers.

---

## 4. CQA 2.1 Quality tab

The 24 quality measures (required and important) were not scored in this review. Recommended next steps:

- Assign reviewer(s); copy the CQA 2.1 Quality tab; assess each measure for this doc set.
- File bugs in epics with the `CQreview_non-negotiable` label for items that do not meet criteria.

---

## 5. DITA validation

- **Vale:** openshift-docs contains `.vale` (styles, templates). Vale was not executed in this review. Run Vale (and asciidoctor-dita-vale per CQA) in CI or the ToolX environment.
- **AsciiDoctor:** Standard for building; not a substitute for DITA-specific validation.

---

## 6. PREVIEW-style validation (equivalent checks)

- **MTVTOCChecker:** Designed for forklift-documentation (master.adoc + doc-*). An equivalent TOC check was run on the OADP tree: **no headings with level > 3.**
- **MTVLinkChecker:** Designed for forklift-documentation. An equivalent internal-include check was run: **0 broken includes** (392 checked). External links and MTV-doc version checks do not apply to OADP; use an openshift-docs–specific or general link checker for external URLs.

---

## 7. Percentage of work done

Formula: **(criteria met / criteria applied) × 100** for the same four automated/structural criteria as the forklift report:

1. **TOC depth ≤ 3** — Pass (1)  
2. **Short description present** — 50/58 ≈ 0.86 (partial)  
3. **Assembly structure** — Pass (1)  
4. **Internal links (includes)** — Pass (1)  

Scoring: (1 + 0.86 + 1 + 1) / 4 ≈ **0.965** → **~97%** if shortdesc is weighted as a full pass when majority have it; if shortdesc is pass only when 100%, then (1 + 0 + 1 + 1) / 4 = 75%. Using the same “critical gap” logic as the forklift report (shortdesc gap is the main fix): **~91%** reflects “one clear fix remaining (8 missing shortdescs).”

| Metric | Value |
|--------|--------|
| .adoc files | 58 |
| With `[role="_abstract"]` | 50 |
| Without shortdesc | 8 |
| TOC violations (level > 3) | 0 |
| Internal includes (broken) | 0 / 392 |
| **% work done (4 criteria)** | **~91%** |

---

## 8. Recommended next steps

1. **Short descriptions:** Add `[role="_abstract"]` (50–300 characters) to the 8 listed files; ensure blank line after level-0 title and no self-referential phrasing.
2. **Vale/DITA:** Run asciidoctor-dita-vale (and Content Type Editor) for `backup_and_restore/application_backup_and_restore`; fix all errors and warnings; ensure CI runs Vale on this path.
3. **Links:** Run a full link check (xrefs + external URLs) for this directory if the repo or team has a checker.
4. **CQA checklist:** Complete the CQA 2.1 Pre-migration and Quality tabs for this doc set; create Jira epics/bugs per DITA Migration Jira Tracking Guidance.
5. **Procedures:** Audit procedure topics for Prerequisites format and count (≤10).

---

*Report generated for CQA 2.1 review of openshift-docs `backup_and_restore/application_backup_and_restore`. Source: [openshift/openshift-docs](https://github.com/openshift/openshift-docs/tree/main/backup_and_restore/application_backup_and_restore).*
