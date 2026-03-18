# **MTA TOC Fixer**

This suite provides a professional automation workflow for the **Migration Toolkit for Applications (MTA)** documentation team. It identifies and resolves Table of Contents (TOC) depth issues, ensuring all sub-headings are visible within the Red Hat Customer Portal sidebar.

---

## **The Core Problem: "Invisible" Headings**

The Red Hat Customer Portal sidebar generally supports a **maximum TOC depth of 3**.

In the MTA "Assembly-Module" architecture, a module is often included with a leveloffset=+2. This means:

1. A Document Title (\=) becomes Level 2\.  
2. A Section Heading (\==) becomes **Level 4**.

Because Level 4 headings are suppressed in the sidebar, users cannot see or navigate to these sub-sections easily. This script "surges" through your files, finds these violations, and refactors the content into smaller, properly-leveled modules.

---

## **Suite Components**

| File | Role |
| :---- | :---- |
| fix\_toc\_by\_new\_modules.py | **The Engine:** Performs the file analysis, content extraction, and header promotion logic. |
| run\_mta\_fix.sh | **The Workflow:** Handles Git staging, commit message generation, PR template creation, and provides a safety "cleanup" mode. |

---

## **Installation & Setup**

1. **Locate your Repo:** Open your local clone of the mta-documentation repository.  
2. **Deploy Scripts:** Place both fix\_toc\_by\_new\_modules.py and run\_mta\_fix.sh in the repository root.  
3. **Set Permissions:**  
   Bash

```
chmod +x run_mta_fix.sh
```

4. 

---

## **Standard Usage Workflow**

### **Step 1: Initialize**

Before starting, ensure you are on a fresh feature branch:

Bash

```
git checkout -b fix-toc-issue-xyz
```

### **Step 2: Execute the Workflow**

Run the wrapper script:

Bash

```
./run_mta_fix.sh
```

The script will:

* Scan for master.adoc and index.adoc files.  
* Calculate effective heading levels.  
* Create new \*-toc-sections.adoc modules.  
* Update assembly includes with leveloffset=+1.  
* **Stage all changes in Git.**

### **Step 3: The Verification Pause**

The script will pause and ask if the build passed. **Do not close the script yet.**

1. Open a new terminal tab.  
2. Run your local documentation build:  
   Bash

```
# Example:
asciidoctor documentation/doc-installing-mta/master.adoc
```

3.   
4. Check the output. Ensure the new sections appear correctly in the TOC.

### **Step 4: Finalize or Rollback**

Return to the script and choose your path:

* **y (Commit):** Generates the commit message and finalizes the work.  
* **c (Cleanup):** Wipes all changes if the build failed (see [Cleanup](https://www.google.com/search?q=%23-cleanup--rollback)).  
* **n (Exit):** Keeps the changes staged but exits without committing.

---

## **Cleanup & Rollback**

If a refactor goes wrong or you want to start over, the suite provides a "Nuke" option to return the repository to its original state.

**To trigger an immediate rollback:**

Bash

```
./run_mta_fix.sh --cleanup
# OR
./run_mta_fix.sh -c
```

**Actions performed during cleanup:**

1. **Unstages** all modified files from Git.  
2. **Restores** original content to modified modules and assemblies.  
3. **Deletes** all generated \*-toc-sections.adoc files from the modules folder.  
4. **Removes** the temporary PR template and report logs.

---

## **Understanding the Outputs**

### **1\. The Git Commit Message**

The script generates a standardized message listing every heading that was moved. This provides a clear audit trail for the maintainers.

### **2\. The GitHub PR Template (PULL\_REQUEST.md)**

A formatted Markdown file is created in your root directory. It contains:

* A **Description** of why the TOC depth was changed.  
* A **Transformation Table** (Heading | Source | Target).  
* An **Impact Summary** (Total modules split).  
* A **Reviewer Checklist**.

**Pro Tip:** Copy the contents of PULL\_REQUEST.md directly into your GitHub PR description to make life easier for your reviewers\!

---

## **Best Practices**

* **Always Build Locally:** Never commit automated changes without running a local asciidoctor or pantheon build first.  
* **Grep for Cross-References:** While the script updates includes, it doesn't change xref: or \<\< \>\> IDs. If you moved a heading that had a specific ID, ensure no other files are pointing to the "old" location if the ID wasn't unique.  
* **Review index.adoc:** MTA guides are transitioning to index.adoc as the primary anchor. The script supports both, but always double-check your specific guide's entry point.

