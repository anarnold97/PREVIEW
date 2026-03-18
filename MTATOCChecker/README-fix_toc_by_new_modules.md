This README provides a comprehensive guide for the fix\_toc\_by\_new\_modules.py script, specifically tailored for the **Migration Toolkit for Applications (MTA)** documentation repository.

---

# **MTA TOC Fixer: Module Depth Surgeon**

fix\_toc\_by\_new\_modules.py is a specialized automation tool designed to manage Table of Contents (TOC) depth in AsciiDoc-based documentation. It identifies content that would be rendered at an unreachable depth (Level 4+) on the Red Hat Customer Portal and refactors it into separate, manageable modules.

## **The Problem: "Deep TOC" Syndrome**

The Red Hat Customer Portal and many documentation HTML templates typically only display the TOC sidebar down to **Level 3**.

In the MTA "Assembly-Module" architecture, a module often starts with a Level 2 heading (\==). However, if that module is included in a master.adoc with a leveloffset=+2, that heading effectively becomes **Level 4**. Any sub-sections within that module effectively "disappear" from the sidebar navigation, making them difficult for users to find.

## **The Solution**

Instead of manually renaming dozens of headers or changing leveloffset (which might break other books sharing the same module), this script performs "surgical splitting":

1. **Identifies** the exact line where the effective TOC level exceeds 3\.  
2. **Extracts** that section and everything following it into a **new module** (e.g., original-toc-sections.adoc).  
3. **Promotes** the first violating heading to a Document Title (\=) in the new file.  
4. **Trims** the original module so it ends cleanly before the split.  
5. **Updates** all calling assemblies (master.adoc or index.adoc) to include the new module immediately after the original, ensuring the reader sees no break in the text flow.

---

## **Features**

* **Context-Aware Depth Calculation:** Recursively calculates the "effective level" by tracking leveloffset across multiple nested includes.  
* **MTA Entry Point Support:** Automatically scans for both master.adoc and index.adoc files.  
* **Smart Trimming:** Automatically removes dangling AsciiDoc attributes (like \[id="..."\] or \[phone-only\]) that would otherwise be left at the bottom of the original file.  
* **Safe Execution:** Includes a \--dry-run mode to preview all changes without touching a single file.  
* **Detailed Reporting:** Generates a migration summary showing exactly which headings moved, where they went, and which assemblies were updated.

---

## **Usage**

### **Prerequisites**

* Python 3.8 or higher.  
* A local clone of the [MTA Documentation](https://github.com/migtools/mta-documentation) repository.

### **Commands**

**1\. Run a Dry Run (Recommended First Step)**

See what the script *would* do without making any changes.

Bash

```
python3 fix_toc_by_new_modules.py --dry-run
```

**2\. Process the Entire Repo**

Bash

```
python3 fix_toc_by_new_modules.py
```

**3\. Process a Specific Guide Only**

If you only want to fix the TOC for the "CLI Guide":

Bash

```
python3 fix_toc_by_new_modules.py documentation/doc-using-the-cli/
```

---

## **Technical Details**

### **The Refactoring Logic**

When the script finds a violation, it transforms the structure as follows:

| Component | Before Refactor | After Refactor |
| :---- | :---- | :---- |
| **Original Module** | Contains Section A, B, and C (too deep). | Contains Section A and B only. |
| **New Module** | Does not exist. | Contains Section C (Promoted to title \=). |
| **Assembly File** | include::module.adoc\[leveloffset=+2\] | include::module.adoc\[leveloffset=+2\]  include::module-toc-sections.adoc\[leveloffset=+1\] |

### **Summary Report Output**

Upon completion, the script prints a detailed audit log:

**\[MOVE\] Heading: 'Customizing Rules for MTA'**

**FROM:** documentation/modules/mta-rules-logic.adoc

**TO:** documentation/modules/mta-rules-logic-toc-sections.adoc

**AFFECTED ASSEMBLIES:**

* documentation/doc-rules-guide/master.adoc

---

## **Safety & Best Practices**

* **Git Branch:** Always run this script on a fresh Git branch.  
* **Build Check:** After running the script, perform a local build (e.g., asciidoctor master.adoc) to ensure no cross-references were broken.  
* **Manual Cleanup:** While the script handles 95% of the work, check for any "See Section X" references in the text that might now point to the new file.

