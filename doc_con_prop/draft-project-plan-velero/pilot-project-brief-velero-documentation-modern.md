# Pilot Project Brief: Velero Documentation Modernization

**Target:** Velero (CNCF Project)  
**Proposed By:** MFH & AA  
**Date:** October 30, 2026  
**Status:** Draft for Discussion

## 1. The Problem

Velero's documentation is already Markdown-based and lives in the project repo, but it suffers from:

*   **Structural Drift:** Content has grown organically. Navigation, headings, and cross-references are inconsistent across the installation and configuration guides.
*   **Discoverability:** Users struggle to locate specific troubleshooting steps or the correct configuration path for their environment.
*   **Lack of AI Readiness:** Content is not optimised for LLM retrieval (RAG). No consistent metadata, no chunk-friendly structure, no semantic anchors.
*   **Weak Validation:** No automated checking of code samples, internal links, or build integrity on PRs.
*   **Maintenance Friction:** Contributors lack a clear content model, so new material compounds the inconsistency.

## 2. The Objective

To transform a defined subset of Velero's documentation into a **structured, validated, AI-ready asset** — and to leave behind a pipeline the maintainers can run themselves.

**Success Criteria (Definition of Done):**

1.  **Restructured:** A documented content model applied to the Installation & Configuration guide, with consistent headings, navigation, and cross-referencing.
2.  **Validated:** A GitHub Actions workflow that lints Markdown, checks internal links, and validates code samples on every PR.
3.  **AI-Optimised:** Front-matter/metadata schema defined and applied; content chunked for effective retrieval.
4.  **Published:** A built documentation site (existing Velero hosting or a preview deployment) reflecting the new structure.
5.  **Transferred:** A contributor guide explaining the content model and pipeline, so the maintainers own it after we leave.
6.  **Case Study:** A public write-up of the before/after and the methodology.

## 3. Scope

One bounded module, to guarantee completion:

*   **Module:** Installation, Configuration, and Basic Backup/Restore.
*   **Deliverables:**
    *   Refactored Markdown source, conforming to the agreed content model.
    *   CI workflow (lint, link check, sample validation, build).
    *   Metadata schema and applied front-matter.
    *   Contributor guide.
    *   Optional: one short how-to screencast, if capacity allows.

**Explicitly out of scope:** full-site rewrite, versioned docs migration, translation, theme redesign.

## 4. Division of Labour

**Principle:** Both partners work across the full stack. Neither is confined to "words" or "code." Every deliverable carries both our names, so every deliverable is open to both of us.

The split below identifies **who builds** and **who inspects** in each area. It is not a boundary. Either partner may build, review, or amend anything.

*   **Content Model & Editorial Standards**
    *   *Builder:* MFH
    *   *Inspector:* AA
    *   *Notes:* MFH leads structure and voice. AA reviews for procedural accuracy and technical correctness. Either may raise changes at any stage.
*   **Pipeline & Automation**
    *   *Builder:* AA
    *   *Inspector:* MFH
    *   *Notes:* AA builds the lint, link-check, validation, and deploy workflows. MFH reviews the implementation, tests it against her own requirements, and signs off before anything is merged. If MFH wants to write or rewrite any part of the pipeline herself, she does.
*   **Metadata & AI Readiness**
    *   *Builder:* MFH
    *   *Inspector:* AA
    *   *Notes:* MFH defines the schema and retrieval strategy. AA implements tagging and indexing. Both review the output.
*   **Repository Hygiene & Release**
    *   *Builder:* AA
    *   *Inspector:* MFH
    *   *Notes:* AA manages branching and CI configuration. MFH approves merges to main.

**Working Rule:** Nothing merges to main without both partners having seen it. "Seen" means reviewed and either approved or amended — not merely notified.

**Deadlock Rule:** If the builder and inspector cannot agree, the matter is parked for 24 hours. If still unresolved, it goes to a joint call. If still unresolved, the decision defaults to MFH.

## 5. Value Proposition

**For Velero:**
*   A cleaner, more maintainable documentation set with a model contributors can follow.
*   Automated validation reducing review burden on maintainers.
*   Content prepared for AI-assisted support tooling.
*   Zero cost.

**For the Practice:**
*   A public, verifiable artefact demonstrating the methodology.
*   A case study for enterprise conversations.
*   A low-risk environment to refine the workflow before paid engagements.
*   Credibility within the Kubernetes and CNCF ecosystem.

## 6. Resources & Timeline

*   **Duration:** 4 weeks, part-time (~5–8 hrs/week each).
*   **Cost:** Nil. Pro bono.
*   **Risk:** Low. If upstream declines the contribution, the work, the pipeline, and the case study remain ours.

## 7. Decisions Required

1.  Confirm Velero as the pilot target, or nominate an alternative.
2.  Approve outreach to maintainers (draft to be reviewed by MFH before sending).
3.  Agree kickoff date and repository setup.

---
*Draft for discussion. Scope, target, and timeline subject to MFH's direction.*
