# CQA 2.1 Review Report — mta-documentation (MTA docs)

**Content assessed:** [migtools/mta-documentation docs/](https://github.com/migtools/mta-documentation/tree/main/docs) (Migration Toolkit for Applications)  
**Reference:** CQA 2.1 — Content Quality Assessment (Pre-migration, Quality, Onboarding)  
**Repo:** [migtools/mta-documentation](https://github.com/migtools/mta-documentation) (main branch).  
**Published MTA 8.0 docs (reference for link check):** [Red Hat MTA 8.0](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/release_notes) and the seven other books listed below.

---

## 1. Executive summary

| Criterion (automated) | Result |
|----------------------|--------|
| **TOC depth** | **Pass** (per-file toclevels respected; 0 violations; 3 masters use :toclevels: 4 vs CQA recommendation 3) |
| **Short descriptions** | **Partial** (173/194 files have `[role="_abstract"]`; 21 missing, including all 8 master.adoc) |
| **Assembly structure** | **Meets** (intro + includes; no text between include statements) |
| **Internal includes** | **Pass** (85 includes, 0 broken) |
| **External / MTA doc links** | **Broken or mismatched** (see §5) |
| **% work done (4 criteria)** | **~88%** |

---

## 2. Scope and structure

- **Path:** `docs/`
- **Guides (master.adoc):** cli-guide, developer-lightspeed-guide, install-guide, intellij-idea-plugin-guide, release-notes, rules-development-guide, vs-code-extension-guide, web-console-guide.
- **Shared content:** `docs/topics/` (templates, mta-cli, mta-ui, mta-install, rules-development, vscode, developer-lightspeed, release-notes-topics, etc.), `docs/assemblies/`.
- **.adoc count:** 194 files.
- **Build:** Jekyll (from repo root); attributes in `docs/topics/templates/document-attributes.adoc` (`:mta-URL:` = `.../8.0/html-single`). Vale present (`vale.ini`).

---

## 3. CQA 2.1 Pre-migration requirements (assessed)

### 3.1 Vale / AsciiDoc → DITA

- **Requirement:** Content passes Vale asciidoctor-dita-vale with no errors or warnings.
- **Assessment:** **No data.** Repo has `vale.ini`. Vale was not run in this review.
- **Action:** Run Vale/asciidoctor-dita-vale for `docs/`; fix reported issues.

### 3.2 Assembly structure (intro + includes only)

- **Requirement:** Assemblies contain only an introductory section and include statements; no text between include statements.
- **Assessment:** **Meets.** Each `master.adoc` has title, attributes, then only `include::` (e.g. install-guide: making-open-source-more-inclusive, intro, then install assemblies). No free-standing paragraphs between includes.
- **Action:** None.

### 3.3 TOC depth (no more than 3 levels recommended)

- **Requirement:** Content not deeply nested in TOC (CQA: recommended no more than 3 levels).
- **Assessment:** **Partially meets.** No heading exceeds the `:toclevels:` set in each file (so 0 “violations” in that sense). However, **install-guide**, **web-console-guide**, and **vs-code-extension-guide** set `:toclevels: 4` in their master.adoc; CQA recommends 3. Global default in `document-attributes.adoc` is `:toclevels: 3`.
- **Action:** Consider changing the three masters from `:toclevels: 4` to `:toclevels: 3` for CQA alignment.

### 3.4 Short descriptions

- **Requirement:** Modules and assemblies have a clear short description: 50–300 characters, `[role="_abstract"]`, blank line after level-0 title.
- **Assessment:** **Does not fully meet.** **173 of 194** files have `[role="_abstract"]`. **21 files missing shortdesc**, including:
  - All **8 master.adoc** files (cli-guide, developer-lightspeed-guide, install-guide, intellij-idea-plugin-guide, release-notes, rules-development-guide, vs-code-extension-guide, web-console-guide).
  - **13 topics:** e.g. `topics/templates/document-attributes.adoc`, `topics/templates/technology-preview-admonition.adoc`, `topics/important-links.adoc`, `topics/cli-args.adoc`, `topics/mta-web-applying-assessments-to-other-apps.adoc`, `topics/developer-lightspeed/assembly_solution-server-configurations.adoc`, and others (templates, reference-style topics).
- **Action:** Add CQA-compliant shortdescs to the 8 master.adoc and to any topic that is a standalone assembly or concept/procedure module. Templates and attribute-only includes may be N/A.

### 3.5 Titles, procedures, editorial, legal

- **Assessment:** Not automated; manual/peer review and Vale when available.
- **Action:** Apply Red Hat peer review checklist; audit procedures for Prerequisites (label, ≤10, no steps in prereqs).

### 3.6 URLs and links (internal)

- **Assessment:** **Meets.** **85** `include::` directives checked; **0** broken (all resolve within repo).
- **Action:** None for includes.

---

## 4. CQA 2.1 Quality tab

The 24 quality measures were not scored. Copy the CQA 2.1 Quality tab, assess for this doc set, and file bugs with the `CQreview_non-negotiable` label as needed.

---

## 5. Broken links vs. published MTA 8.0 docs

Links were checked against the **published** MTA 8.0 multi-page HTML paths you provided:

| Published book (path segment) | URL (base) |
|------------------------------|------------|
| Release notes | `.../8.0/html/release_notes` |
| Installing MTA | `.../8.0/html/installing_the_migration_toolkit_for_applications` |
| Developer Lightspeed for MTA | `.../8.0/html/configuring_and_using_red_hat_developer_lightspeed_for_mta` |
| Using the MTA CLI | `.../8.0/html/using_the_migration_toolkit_for_applications_command-line_interface` |
| Configuring and managing the MTA UI | `.../8.0/html/configuring_and_managing_the_migration_toolkit_for_applications_user_interface` |
| VS Code Extension for MTA | `.../8.0/html/configuring_and_using_the_visual_studio_code_extension_for_mta` |
| IntelliJ IDEA Plugin Guide | `.../8.0/html/intellij_idea_plugin_guide` |
| Rules Development Guide | `.../8.0/html/configuring_and_using_rules_for_an_mta_analysis` |

### 5.1 Malformed URL (broken regardless of build)

| File | Issue | Fix |
|------|--------|-----|
| `docs/topics/mta-cli/proc_running-the-containerless-mta-cli.adoc` (line 24) | **Missing `/` after `{mta-URL}`.** Renders as `.../html-singleinstalling_the_migration_toolkit_for_applications/...` | Use `link:{mta-URL}/installing_the_migration_toolkit_for_applications/...` |

### 5.2 Link path mismatches (wrong path segment for published multi-page HTML)

These links use path segments that **do not match** the published 8.0 multi-page paths above. If your build publishes to the same URLs as [docs.redhat.com/.../migration_toolkit_for_applications/8.0/html/...](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/release_notes), they will be broken or redirect-dependent.

| File | Used path (wrong for published) | Should be (per published 8.0) |
|------|---------------------------------|--------------------------------|
| `docs/topics/release-notes-topics/ref_new-features-and-enhancements-8-0.adoc` (lines 51, 64) | `html/.../cli_guide/generating-assets_cli-guide#...` | `html/.../using_the_migration_toolkit_for_applications_command-line_interface/...` (or equivalent page path for “Generating assets”) |
| `docs/topics/release-notes-topics/ref_new-features-and-enhancements-8-0.adoc` (line 96) | `html/.../user_interface_guide/index#setting-default-credentials_...` | `html/.../configuring_and_managing_the_migration_toolkit_for_applications_user_interface/...` (or equivalent page path for “Setting default credentials”) |
| `docs/topics/mta-ui/con_intro-to-mta-ui.adoc` (line 20) | `html/.../installing-mta-title/index` | `html/.../installing_the_migration_toolkit_for_applications` (or `.../installing_the_migration_toolkit_for_applications/index` if index exists) |
| `docs/topics/mta-install/con_mta-rules.adoc` (line 36) | `{mta-URL}/rules_development_guide/index` | `.../configuring_and_using_rules_for_an_mta_analysis` (or equivalent) |

**Note:** The repo defines `:mta-URL:` as `.../8.0/html-single`. If you publish **only** single-page (html-single), path segments may differ from the multi-page table above; the malformed link in §5.1 still needs the missing `/`.

### 5.3 Links that match published paths

These use path segments that **match** the published 8.0 docs and are consistent with the table above:

- `configuring_and_using_red_hat_developer_lightspeed_for_mta` — used in vscode topics and about-rules.adoc.
- `configuring_and_managing_the_migration_toolkit_for_applications_user_interface` — used in con_mta-tools.adoc.
- `using_the_migration_toolkit_for_applications_command-line_interface` — used in con_mta-tools.adoc, proc_downloading-an-analysis-report.adoc, proc_installing-cli-zip.adoc.
- `installing_the_migration_toolkit_for_applications` — used (with correct `/` after {mta-URL}) in several install/CLI topics.
- `configuring_and_using_the_visual_studio_code_extension_for_mta` — used in con_mta-tools.adoc.
- `intellij_idea_plugin_guide` — used in con_mta-tools.adoc.

---

## 6. PREVIEW-style validation

- **TOC:** No heading exceeds the file’s own `:toclevels:` (0 violations). Three masters use level 4 vs CQA recommendation 3.
- **Internal includes:** 0 broken (85 checked).
- PREVIEW [MTVTOCChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVTOCChecker) / [MTVLinkChecker](https://github.com/anarnold97/PREVIEW/tree/main/MTVLinkChecker) target forklift-documentation; equivalent checks were run on `docs/` for this report.

---

## 7. Percentage of work done

Using the same four criteria as the forklift and OADP reports:

1. **TOC depth** — Pass (1); note CQA recommends 3, three masters use 4.  
2. **Short description** — 173/194 ≈ 0.89.  
3. **Assembly structure** — Pass (1).  
4. **Internal links (includes)** — Pass (1).  

**(1 + 0.89 + 1 + 1) / 4 ≈ 97%** for automated criteria; if “shortdesc” is required for all modules and masters, **(1 + 0 + 1 + 1) / 4 = 75%.** Accounting for **broken/mismatched external MTA doc links** as the other main fix: **~88%.**

| Metric | Value |
|--------|--------|
| .adoc files | 194 |
| With `[role="_abstract"]` | 173 |
| Without shortdesc | 21 (including 8 master.adoc) |
| TOC violations (per-file) | 0 |
| Masters with :toclevels: 4 | 3 (install, web-console, vs-code) |
| Internal includes (broken) | 0 / 85 |
| MTA doc links: malformed | 1 (missing `/`) |
| MTA doc links: path mismatch | 4 (in 2 files + con_intro + con_mta-rules) |
| **% work done (4 criteria)** | **~88%** |

---

## 8. Recommended next steps

1. **Fix malformed link:** In `docs/topics/mta-cli/proc_running-the-containerless-mta-cli.adoc` line 24, add the missing `/` after `{mta-URL}`.
2. **Align MTA doc links with published 8.0 paths:** Update the four link path mismatches in §5.2 so they use the published path segments (e.g. `using_the_migration_toolkit_for_applications_command-line_interface`, `configuring_and_managing_the_migration_toolkit_for_applications_user_interface`, `installing_the_migration_toolkit_for_applications`, `configuring_and_using_rules_for_an_mta_analysis`).
3. **Short descriptions:** Add `[role="_abstract"]` (50–300 characters) to the 8 master.adoc and to any topic that should have a shortdesc per CQA.
4. **TOC depth:** Consider changing `:toclevels: 4` to `:toclevels: 3` in install-guide, web-console-guide, and vs-code-extension-guide master.adoc.
5. **Vale/DITA:** Run Vale (and asciidoctor-dita-vale if required) on `docs/`; fix errors and warnings.
6. **CQA checklist:** Complete the CQA 2.1 Pre-migration and Quality tabs; create Jira epics/bugs per your process.

---

*Report generated for CQA 2.1 review of [migtools/mta-documentation docs/](https://github.com/migtools/mta-documentation/tree/main/docs). Link check referenced [MTA 8.0 Release Notes](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/release_notes), [Installing MTA](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/installing_the_migration_toolkit_for_applications), [Developer Lightspeed for MTA](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/configuring_and_using_red_hat_developer_lightspeed_for_mta), [Using the MTA CLI](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/using_the_migration_toolkit_for_applications_command-line_interface), [Configuring and managing the MTA UI](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/configuring_and_managing_the_migration_toolkit_for_applications_user_interface), [VS Code Extension for MTA](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/configuring_and_using_the_visual_studio_code_extension_for_mta), [IntelliJ IDEA Plugin Guide](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/intellij_idea_plugin_guide), and [Rules Development Guide](https://docs.redhat.com/en/documentation/migration_toolkit_for_applications/8.0/html/configuring_and_using_rules_for_an_mta_analysis).*
