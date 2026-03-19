# **OpenShift Virtualization DITA Validation Script (`validate_dita.py`)**

This script automates the Vale validation workflow for the OpenShift Virtualization (`virt`) documentation. Instead of running a series of manual Git and Vale commands, this Python utility handles the synchronization, repository updates, parallel execution, and report generation in a single run.

## **📌 Overview**

The `validate_dita.py` script performs the following tasks sequentially:

1. **Syncs Vale Configuration:** Ensures your local `~/dita.ini` is up-to-date with remote packages/vocabularies.  
2. **Manages the Git Lifecycle:** Checks out the `main` branch, fetches the latest changes from the official upstream repository, rebases your local branch, and pushes the updated state to your personal origin.  
3. **Executes Parallel Validation:** Uses `find` and `xargs` to locate all virtualization-related AsciiDoc files and runs Vale against them using 8 CPU cores for maximum speed.  
4. **Generates a CSV Report:** Captures all Vale output (including style alerts and errors) and saves it safely to `CNV-DITA-report.csv`.

---

## **⚙️ Prerequisites**

Before running this script, ensure your local environment meets the following requirements:

* **Python 3:** Installed and accessible via the `python3` command.  
* **Vale:** Installed and accessible in your system's PATH.  
* **Configuration File:** A valid Vale configuration file must exist at `~/dita.ini`.  
* **Git Remotes:** Your local `openshift-docs` clone must have the following remotes configured:  
  * `upstream`: Pointing to the official repository (`https://github.com/openshift/openshift-docs`).  
  * `origin`: Pointing to your personal fork of the repository.

---

## **🚀 Installation & Setup**

1. Download or copy the `validate_dita.py` script.  
2. Place the script directly into the **root directory** of your local `openshift-docs` repository.

---

## **💻 Usage**

To run the validation workflow, open your terminal, navigate to your `openshift-docs` root directory, and execute the script:

Bash

```
python3 validate_dita.py
```

### **What to Expect During Execution**

When you trigger the script, it will print its progress to the terminal:

1. `🚀 Starting DITA Validation Workflow...`  
2. `🔄 Syncing Vale configuration...` (Runs `vale sync`)  
3. `🌿 Updating repository...` (Runs the Git checkout, fetch, rebase, and push commands)  
4. `🔍 Running Vale validation on 8 cores...` (Spawns the parallel Vale processes)  
5. `✅ Validation complete. Report saved...` (or a `⚠️` warning if Vale found style violations, which is normal behavior).

---

## **📊 Output File (`CNV-DITA-report.csv`)**

Upon completion, the script generates a file named `CNV-DITA-report.csv` in the root of the repository.

Because Vale is instructed to use `--output line`, the resulting CSV file will contain a line-by-line breakdown of every DITA/style violation found in the `virt/` directory and `modules/virt-*.adoc` files. You can open this file in any spreadsheet application (like Excel or Google Sheets) or parse it further with other tools.

---

## **🛠️ Troubleshooting & Notes**

* **"Vale found issues (this is normal)" Message:** Vale returns a non-zero exit code to the system whenever it detects a style warning or error. The Python script is specifically designed to catch this "failure." It will still write the full output to your CSV file and exit gracefully.  
* **Git Rebase Conflicts:** If your local `main` branch has diverged from `upstream/main` in a way that causes merge conflicts, the script will halt during the Git update phase and print an error. You will need to resolve the conflicts manually using `git rebase --continue` before running the script again.  
* **Missing Files/Directories:** The script assumes the standard OpenShift docs directory structure. If `virt/` or `modules/` do not exist in your current working directory, the `find` command will return empty results.

