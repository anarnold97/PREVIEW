# PREVIEW

Automation scripts and utilities for **Red Hat documentation Content Quality Assurance (CQA)**, validation, and restructuring across multiple product lines — plus a set of beginner-friendly **programming tutorials**.

## 📚 Tutorials

In addition to the documentation QA tooling, this repository hosts two hands-on courses for beginners:

### [C++ tutorial](./C%2B%2B%20tutorial/) — *A Beginner's Introduction to C++*

A friendly, self-paced C++ course designed for absolute beginners (including children). Fifteen numbered lessons (Markdown files) build one idea at a time — from displaying your first message, through variables, user input, decisions, arithmetic, and loops, up to project exercises. The finale uses nested loops to print the times tables from 1 to 12.

- 📖 Start with [00-introduction.md](./C%2B%2B%20tutorial/00-introduction.md) and the [course README](./C%2B%2B%20tutorial/README.md)
- 🛠️ Practice online with the [Programiz C++ compiler](https://www.programiz.com/cpp-programming/online-compiler/) — no installation needed; it includes a step-by-step visualization feature that helps explain loops
- 💡 Includes three projects with solutions (`04-project`, `09-project`/`09-solution`, `15-project`/`15-solution`)

### [python-tutorial](./python-tutorial/) — *Python Lessons from the People Who Build Software*

Twelve Python lessons (`python-01.md` – `python-12.md`) created by technology professionals with ~40 years of combined experience. Beyond syntax, the lessons share the history of computing and how software development works in practice: testing ideas, finding bugs, collaborating, and learning from mistakes.

- 📖 Start with the [tutorial README](./python-tutorial/README.md)
- 👥 Written as a dialogue between Andy (developer perspective) and Mary (trainer perspective), drawing on careers spanning systems administration, SRE, startups, and big tech
- 🎯 Aimed at curious beginners who want to understand not just how to write code, but how software gets made

## Overview

This repository contains a collection of Python scripts, shell scripts, DITA maps, and HTML previews used to automate documentation QA tasks for Red Hat products, including:

- **MTA** — Migration Toolkit for Applications
- **MTV** — Migration Toolkit for Virtualization
- **CNV** — OpenShift Virtualization
- **OADP** — OpenShift API for Data Protection
- **OCP** — OpenShift Container Platform
- **MMS** — MMS documentation

Tasks covered include content quality checks, DITA structure validation, link checking, Jobs-To-Be-Done (JTBD) validation and mapping, word/element counting, TOC verification, release notes generation, and doc tree restructuring.

## Repository Structure

| Directory / File | Description |
| --- | --- |
| `C++ tutorial/` | Beginner C++ course: 15 lessons plus projects and solutions |
| `python-tutorial/` | Beginner Python course: 12 lessons |
| `CNV-CQA/virt/` | CQA checks for CNV (OpenShift Virtualization) documentation |
| `CNV-DITA-Checker/` | DITA structure checker for CNV docs |
| `Common_Content/` | Shared content assets |
| `DITA/` | DITA-related processing scripts and outputs |
| `JTBD/`, `JTBD-transformation/` | Jobs-To-Be-Done validation and transformation scripts |
| `LINK-Checker/`, `MTALinkChecker/`, `MTVLinkChecker/`, `OpenShiftLinkCheck/` | Link-checking utilities for various products |
| `MMS-CQA/` | CQA checks for MMS documentation |
| `MTA-count/`, `MTV-count/`, `OADP-count/`, `VIRT-count/` | Word/element counting scripts per product |
| `MTA-JTBD/`, `MTV-JTBD-plan/` | JTBD planning artifacts for MTA and MTV |
| `MTATOCChecker/`, `MTVTOCChecker/` | Table of Contents (TOC) checkers for MTA and MTV |
| `MTV-CQA/` | CQA checks for MTV documentation |
| `OADP-DITA-Checker/` | DITA structure checker for OADP docs |
| `OADP-JTBD/` | JTBD validation for OADP |
| `OADPReleaseNotesAutomation/`, `ReleaseNotesAutomation/` | Release notes generation automation |
| `OCP_CQA_Check/` | CQA checks for OCP documentation |
| `SHORT-DESCRIPTION/`, `ShortDescription/` | Short description validation and fixing utilities |
| `VIRT/` | Virtualization-related scripts and previews |
| `images/` | Image assets used by scripts or previews |
| `cqa_fix_shortdesc.py` | Fixes missing/enforces CQA 2.1 short descriptions in `.adoc` files |
| `cqa_jtbd_validate.py` | Validates JTBD mappings |
| `fix_cqa_errors.py` | Applies CQA shortdesc fixes to AsciiDoc topics |
| `jtbd-mapping.yaml` | JTBD mapping configuration |
| `oadp_release_notes_automation.py` | Automates OADP release notes generation |
| `oadp-restructure.sh` | Shell script for restructuring OADP doc trees |
| `openshift_virt_restructure.ditamap` | Draft DITA map for OpenShift Virtualization restructuring |
| `OADP-proposed.yml` | Proposed OADP configuration |
| `*.html` | HTML preview files (MTA, dev-lightspeed, migrating, planning) |

## Key Scripts

### `cqa_fix_shortdesc.py` / `fix_cqa_errors.py`

Applies CQA 2.1 shortdesc fixes to AsciiDoc (`.adoc`) topics. The scripts:

- Detect topics missing a `[role="_abstract"]` shortdesc after the `= Title` line
- Apply overrides from `shortdesc_overrides.csv` where available
- Respect topic attributes (`:attribute:` lines) and comment markers (`//`)
- Can operate on a single `.adoc` file, a directory tree (e.g. `website/`), or a filtered subset

**Prerequisites:** Python 3. No additional packages required.

**Usage** (run a dry run first — recommended):

```bash
# Preview proposed changes without writing files
python3 cqa_fix_shortdesc.py --dry-run <path>

# Apply fixes
python3 cqa_fix_shortdesc.py <path>
```

<!-- TODO: confirm exact flags against the script -->

### `cqa_jtbd_validate.py`

Validates JTBD mappings against `jtbd-mapping.yaml`.

<!-- TODO: usage -->

### `oadp_release_notes_automation.py`

Automates OADP release notes generation.

<!-- TODO: usage -->

### `oadp-restructure.sh`

Shell script for restructuring the OADP documentation tree.

<!-- TODO: usage -->

## Requirements

- Python 3 (standard library only for the main fix scripts)
- Bash (for shell utilities)
- Individual subdirectories may have their own requirements — see comments at the top of each script

## Contributing

Scripts are organized per product line; tutorials live in their own directories. When adding a new utility or lesson:

1. Place product-specific scripts in the matching product directory
2. Add shared/reusable logic to `Common_Content/` or the repo root
3. Add tutorial lessons to the relevant tutorial directory, following its numbering scheme
4. Update the structure table above
