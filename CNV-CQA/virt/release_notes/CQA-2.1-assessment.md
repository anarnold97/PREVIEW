# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/release_notes/`  
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
# All files in virt/release_notes (12 files, no subdirs):
vale --config=.vale-cqa.ini virt/release_notes/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/release_notes/*.adoc` (12 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/release_notes/*.adoc` | 22 | 0 | 12 | 12 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. All errors must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/release_notes/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/release_notes/` — No TOC violations under `release_notes`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/release_notes
```

**Result:** **Meets** — No broken links or xrefs found (12 files scanned).

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/release_notes
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **12** `virt/release_notes/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-4-11-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-11-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-12-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-12-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-13-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-13-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-14-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-14-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-15-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-15-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-16-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-16-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-17-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-18-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-18-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-19-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-19-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-20-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-4-20-release-notes.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |
| virt-4-21-release-notes.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-release-notes-placeholder.adoc | 3 | AsciiDocDITA.ShortDescription | Assign [role="_abstract"] |
| virt-release-notes-placeholder.adoc | 6 | AsciiDocDITA.AuthorLine | Author lines are not supported for topics. |

**Total:** 22 errors (12 ShortDescription, 10 AuthorLine) across 12 files. **virt-4-17** and **virt-4-21** have only ShortDescription; the other 10 files have both ShortDescription and AuthorLine.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 22 errors (DITA) |
| Vale — no warnings | Meets | 0 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under release_notes |
| No broken links | Meets | No issues found |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| virt-4-11-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-12-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-13-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-14-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-15-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-16-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-17-release-notes.adoc | 1 | ShortDescription only |
| virt-4-18-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-19-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-20-release-notes.adoc | 2 | ShortDescription, AuthorLine |
| virt-4-21-release-notes.adoc | 1 | ShortDescription only |
| virt-release-notes-placeholder.adoc | 2 | ShortDescription, AuthorLine |
| **Total** | **22** errors, **0** warnings, **12** suggestions | 12 files |

---

## 5. Quality notes

- **ShortDescription:** Add `[role="_abstract"]` to the first paragraph (short description) in each release-notes topic per DITA convention (all 12 files, line 3).
- **AuthorLine:** Remove or convert the author line at line 6 in the 10 affected files. DITA topics do not support author lines; use metadata or prolog instead if author information is required.
- **RedHat suggestions:** Address sentence-style capitalization in headings (“release notes”, “release notes placeholder”) where flagged (12 suggestions).

---

## 6. Next steps

1. Fix all 22 DITA errors: add ShortDescription in all 12 files; remove or replace author lines in 10 files.
2. Work through Vale suggestions (sentence-style headings) as needed for style compliance.
3. Re-run Vale to confirm no errors or warnings.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
