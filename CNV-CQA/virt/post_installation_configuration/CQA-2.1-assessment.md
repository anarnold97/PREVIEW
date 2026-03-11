# CQA 2.1 — Content Quality Assessment

**Content location:** `virt/post_installation_configuration/`  
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
# All files in virt/post_installation_configuration (8 files, no subdirs):
vale --config=.vale-cqa.ini virt/post_installation_configuration/*.adoc
```

---

## 2. Vale results summary (RedHat + AsciiDocDITA)

**Scope:** `virt/post_installation_configuration/*.adoc` (8 files)

| Scope | Errors | Warnings | Suggestions | Files |
|-------|--------|----------|-------------|-------|
| `virt/post_installation_configuration/*.adoc` | 1 | 0 | 13 | 8 |

**CQA pre-migration:** Content does **not** yet pass the Vale asciidoctor-dita-vale check with no errors or warnings. The single error must be addressed before migration.

**Re-run:**

```bash
vale --config=.vale-cqa.ini virt/post_installation_configuration/*.adoc
```

---

## 2.1 TOC level check (CQA: no more than 3 levels)

**Script:** [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) (local copy: `virt/install/check_toc_level.py`)

**Requirement (CQA Pre-migration):** Content is not deeply nested in the TOC (recommended: no more than 3 levels).

**Command run (virt branch):**

```bash
python3 virt/install/check_toc_level.py virt
```

**Result:** **Meets** for `virt/post_installation_configuration/` — No TOC violations under `post_installation_configuration`. The virt branch reports 32 nodes with level > 3; all are under `creating_vms_advanced` or `managing_vms`.

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
python3 virt/install/check_broken_links.py virt/post_installation_configuration
```

**Result:** **6 issue(s)** in 8 files (all xref anchor not found; includes resolved successfully).

| Category          | Count | Notes |
|-------------------|--------|--------|
| **Anchor not found** | 6 | xref target file exists but specified `#anchor` does not match `[id="..."]` in source (build/context-generated IDs can cause false positives). |

**Issues:**

- **virt-post-install-network-config.adoc** (5 xrefs):
  - → `../../networking/networking_operators/k8s-nmstate-about-the-k8s-nmstate-operator.adoc#installing-the-kubernetes-nmstate-operator-web-console_k8s-nmstate-operator` — anchor not found.
  - → `../../networking/networking_operators/sr-iov-operator/installing-sriov-operator.adoc#installing-sr-iov-operator_installing-sriov-operator` — anchor not found.
  - → `../../networking/networking_operators/metallb-operator/metallb-operator-install.adoc#metallb-installing-using-web-console_metallb-operator-install` — anchor not found.
  - → `../../virt/vm_networking/virt-connecting-vm-to-linux-bridge.adoc#virt-attaching-vm-secondary-network-cli_virt-connecting-vm-to-linux-bridge` — anchor not found.
  - → `../../virt/vm_networking/virt-connecting-vm-to-sriov.adoc#virt-attaching-vm-to-sriov-network_virt-connecting-vm-to-sriov` — anchor not found.
- **virt-post-install-storage-config.adoc** (1 xref):
  - → `../../storage/dynamic-provisioning.adoc#defining-storage-classes_dynamic-provisioning` — anchor not found.

**Recommendation:** Re-run with `--validate-against` to check xrefs against published docs:

```bash
python3 virt/install/check_broken_links.py --validate-against https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/virtualization virt/post_installation_configuration
```

**Re-run (local check):**

```bash
python3 virt/install/check_broken_links.py virt/post_installation_configuration
```

---

## 2.3 DITA errors (Vale AsciiDocDITA)

All DITA-related Vale errors in the scanned **8** `virt/post_installation_configuration/` files (AsciiDocDITA package only). Fix these to pass the asciidoctor-dita-vale check for pre-migration.

| File | Line | Rule | Message |
|------|------|------|---------|
| virt-post-install-network-config.adoc | 42 | AsciiDocDITA.AssemblyContents | Content other than additional resources cannot follow include directives. |

**Total:** 1 DITA error (AssemblyContents) in 1 file.

---

## 3. Pre-migration checklist (CQA 2.1)

| Criterion | Status | Notes |
|-----------|--------|--------|
| Vale (RedHat + AsciiDocDITA) — no errors | Does not meet | 1 error (AssemblyContents) |
| Vale — no warnings | Meets | 0 warnings |
| TOC depth ≤ 3 levels | Meets | No violations under post_installation_configuration |
| No broken links | Does not meet | 6 xref anchor issues |

---

## 4. Breakdown by file (Vale: errors)

| File | Errors | Notes |
|------|--------|--------|
| virt-configuring-certificate-rotation.adoc | 0 | Suggestions only (ReadabilityGrade) |
| virt-configuring-higher-vm-workload-density.adoc | 0 | — |
| virt-node-placement-virt-components.adoc | 0 | — |
| virt-perf-optimization.adoc | 0 | Suggestions only (ReadabilityGrade) |
| virt-post-install-config.adoc | 0 | Suggestions only (ReadabilityGrade) |
| virt-post-install-network-config.adoc | 1 | AssemblyContents (line 42); 5 broken xrefs |
| virt-post-install-storage-config.adoc | 0 | Suggestions only; 1 broken xref |
| virt-self-validation-checkups.adoc | 0 | Suggestions only (ReadabilityGrade, SentenceLength, ProductCentricWriting) |
| **Total** | **1** error, **0** warnings, **13** suggestions | 8 files |

---

## 5. Quality notes

- **AssemblyContents:** In *virt-post-install-network-config.adoc* (line 42), ensure only “additional resources”–type content follows include directives (or restructure per AsciiDocDITA.AssemblyContents).
- **Broken xrefs:** Update or remove the six xrefs whose anchors are not present in the target files (or confirm against published build IDs). Five are in *virt-post-install-network-config.adoc*, one in *virt-post-install-storage-config.adoc*.
- **RedHat suggestions:** Address readability (Flesch–Kincaid grade), sentence-style headings, PascalCamelCase (e.g. MetalLB in backticks), sentence length, and product-centric writing where flagged.

---

## 6. Next steps

1. Fix the 1 DITA error (AssemblyContents in *virt-post-install-network-config.adoc*).
2. Resolve 6 broken xref anchors (or validate against published docs).
3. Work through Vale suggestions for style compliance as needed.
4. Re-run Vale and broken-links check to confirm clean results.

---

## 7. References

- CQA 2.1 pre-migration requirements (PDF)
- [Vale](https://vale.sh/) — `.vale-cqa.ini` at repo root
- [AsciiDocDITA Vale rules](https://github.com/jhradilek/asciidoctor-dita-vale/releases/latest/download/AsciiDocDITA.zip)
- [check_toc_level.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_toc_level.py) — TOC depth
- [check_broken_links.py](https://github.com/anarnold97/PREVIEW/blob/main/VIRT/check_broken_links.py) — xref/include validation
