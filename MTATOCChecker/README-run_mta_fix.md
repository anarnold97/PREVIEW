This README provides instructions for using the `run_mta_fix.sh` shell script. This script acts as a high-level automation wrapper for the `fix_toc_by_new_modules.py` Python tool, specifically optimized for the **Migration Toolkit for Applications (MTA)** documentation workflow.

---

# **MTA TOC Automation Wrapper (`run_mta_fix.sh`)**

The `run_mta_fix.sh` script streamlines the process of fixing Table of Contents (TOC) depth issues. It handles the execution of the Python logic, captures the transformation data, and automates the Git staging and commit process with a dynamically generated, descriptive commit message.

## **Core Functions**

* **Execution:** Runs the `fix_toc_by_new_modules.py` script.  
* **Logging:** Captures the full output of the migration into a temporary report.  
* **Git Staging:** Automatically runs `git add` on modified modules and updated assemblies.  
* **Message Generation:** Parses the report to list every moved heading in the Git commit body.  
* **Interactive Confirmation:** Prompts the user to review the changes before finalizing the commit.

---

## **Prerequisites**

1. **Environment:** A Linux or macOS terminal (Bash-compatible).  
2. **Tools:** \* Python 3.8+  
   * Git  
3. **Required Files:** Both `run_mta_fix.sh` and `fix_toc_by_new_modules.py` must be in the same directory (ideally the root of your local MTA documentation repository).

---

## **Installation & Setup**

Before running the script for the first time, you must grant it execution permissions:

Bash

```
chmod +x run_mta_fix.sh
```

---

## **Usage**

### **Standard Workflow**

To process the entire repository and generate a commit:

Bash

```
./run_mta_fix.sh
```

### **What Happens During Execution?**

1. **Validation:** The script checks if the Python "engine" (`fix_toc_by_new_modules.py`) is present.  
2. **Processing:** It executes the Python script. If no modules exceed the TOC level 3 limit, the script exits cleanly without making changes.  
3. **Parsing:** If changes are made, the script extracts the "Moved Headings" from the Python report.  
4. **Staging:** It stages all `.adoc` files in the `documentation/modules/` and `documentation/doc-*/` directories.  
5. **Review:** It displays the generated commit message and asks: `Do you want to commit these changes? (y/n)`.

---

## **Commit Message Structure**

The script generates a standardized, professional commit message based on the [Conventional Commits](https://www.conventionalcommits.org/) specification.

**Example Generated Message:**

Plaintext

```
docs: refactor modules to fix TOC depth

Automated TOC depth correction for MTA documentation.
The following headings were moved to new modules to stay within Level 3:
- 'Configuring the CLI for OpenShift'
- 'Advanced Analysis Rules'

Summary:
Total Modules Split: 2
Total Files Modified: 5
```

---

## **Troubleshooting & Files**

### **Temporary Files**

The script creates two temporary files during execution:

* `mta_toc_report.txt`: A temporary log of the Python script output.  
* `git_commit_msg.txt`: The draft commit message.

*Note: `mta_toc_report.txt` is automatically deleted on exit, but `git_commit_msg.txt` is preserved if you choose not to commit, allowing you to manually commit later.*

### **Error: "No modules found"**

If you see this message, it means your documentation already complies with the TOC depth requirements (all headings are reachable within the first 3 levels of the portal sidebar). No files were changed.

---

## **Best Practices**

* **Branching:** Always run this script on a feature branch (e.g., `git checkout -b fix-toc-depth`).  
* **Dry Run First:** If you are unsure, run the Python script manually with `--dry-run` before using the shell wrapper.  
* **Verification:** After the script finishes, run `git status` to verify the staged files.

