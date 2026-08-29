# PREVIEW

Automation scripts and utilities for Red Hat documentation Content Quality Assurance (CQA), validation, and restructuring across multiple product lines.

## Overview

This repository contains a collection of Python scripts, shell scripts, DITA maps, and HTML previews used to automate documentation QA tasks for the following Red Hat products:

- **MTA** – Migration Toolkit for Applications
- **MTV** – Migration Toolkit for Virtualization
- **OADP** – OpenShift API for Data Protection
- **CNV** – Container Native Virtualization
- **MMS** – Managed Monitoring Service
- **OCP** – OpenShift Container Platform

## Repository Structure

| Directory / File                          | Description                                                                 |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| `CNV-CQA/virt/`                           | CQA checks for CNV (OpenShift Virtualization) documentation                 |
| `CNV-DITA-Checker/`                       | DITA structure checker for CNV docs                                         |
| `Common_Content/`                         | Shared content assets                                                       |
| `DITA/`                                   | DITA-related processing scripts and outputs                                 |
| `JTBD/`, `JTBD-transformation/`          | Jobs-To-Be-Done validation and transformation scripts                       |
| `LINK-Checker/`, `MTALinkChecker/`, `MTVLinkChecker/`, `OpenShiftLinkCheck/` | Link-checking utilities for various products |
| `MMS-CQA/`                                | CQA checks for MMS documentation                                            |
| `MTA-count/`, `MTV-count/`, `OADP-count/`, `VIRT-count/` | Word/element counting scripts per product               |
| `MTA-JTBD/`, `MTV-JTBD-plan/`            | JTBD planning artifacts for MTA and MTV                                     |
| `MTATOCChecker/`, `MTVTOCChecker/`       | Table of Contents (TOC) checkers for MTA and MTV                            |
| `MTV-CQA/`                                | CQA checks for MTV documentation                                            |
| `OADP-DITA-Checker/`                      | DITA structure checker for OADP docs                                        |
| `OADP-JTBD/`                              | JTBD validation for OADP                                                    |
| `OADPReleaseNotesAutomation/`, `ReleaseNotesAutomation/` | Release notes generation automation                          |
| `OCP_CQA_Check/`                          | CQA checks for OCP documentation                                            |
| `SHORT-DESCRIPTION/`, `ShortDescription/` | Short description validation and fixing utilities                          |
| `VIRT/`                                   | Virtualization-related scripts and previews                                 |
| `images/`                                 | Image assets used by scripts or previews                                    |
| `cqa_fix_shortdesc.py`                    | Fixes missing/enforces CQA 2.1 short descriptions in `.adoc` files         |
| `cqa_jtbd_validate.py`                    | Validates JTBD mappings                                                     |
| `fix_cqa_errors.py`                       | Applies CQA shortdesc fixes to AsciiDoc topics                             |
| `jtbd-mapping.yaml`                       | JTBD mapping configuration                                                  |
| `oadp_release_notes_automation.py`        | Automates OADP release notes generation                                     |
| `oadp-restructure.sh`                     | Shell script for restructuring OADP doc trees                               |
| `openshift_virt_restructure.ditamap`      | Draft DITA map for OpenShift Virtualization restructuring                  |
| `OADP-proposed.yml`                       | Proposed OADP configuration                                                 |
| `*.html`                                  | HTML preview files (MTA, dev-lightspeed, migrating, planning)              |

## Key Scripts

### `fix_cqa_errors.py` / `cqa_fix_shortdesc.py`

Applies **CQA 2.1 shortdesc** fixes to AsciiDoc (`.adoc`) topics. Specifically, it:

1. **Finds topics without a shortdesc** – Scans the repository for `.adoc` files lacking a `[role="_abstract"]` block.
2. **Adds missing shortdescs** – For each file, derives a short description from the `= Title` (or uses a custom override from `shortdesc_overrides.csv`).
3. **Enforces length** – Ensures short descriptions are between 50–300 characters.
4. **Respects structure** – Inserts the abstract after the `= Title` line and any `:attribute:` lines or `//` comments.
5. **Skips `website/`** – Ignores any `.adoc` under a `website` directory.

#### Prerequisites

Python 3. No additional packages required.

#### Usage

**Dry run (recommended first):**

```bash
python3 fix_cqa_errors.py --repo /path/to/mta-docs --dry-run