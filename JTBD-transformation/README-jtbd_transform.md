# **JTBD Transform: AsciiDoc Stylist**

jtbd_transform.py is a specialized automation tool designed to refactor AsciiDoc documentation. It converts subjective, person-centric phrasing into impersonal, action-oriented language consistent with the **Jobs To Be Done (JTBD)** framework.

Beyond text transformation, the script automates the Git workflow, ensuring your changes are isolated in a dedicated feature branch and staged for review.

## **Key Features**

* **Smart Transformation:** Replaces first/second-person pronouns with impersonal task statements and cleans up gerunds.  
* **Deep AsciiDoc Awareness:** Intelligently ignores code blocks, admonition blocks, attributes, include statements, and conditional tags to prevent breaking technical syntax.  
* **Automated Git Workflow:** \* Detects the repository root automatically.  
  * Creates a unique branch based on the filename: `jtbd-transformation-\<filename\>`.  
  * Handles branch name collisions with interactive prompts.  
  * Stages changes (git add) automatically.  
* **Regex-Powered Refactoring:** Handles complex patterns including question-to-statement conversion and user-centric phrase mapping (e.g., "allows you to" → "allows users to").

---

## **Getting Started**

### **Prerequisites**

* **Python 3.6+**  
* **Git** (The script must be executed within a Git repository).  
* **Local Fork:** Ensure you are working on a local branch of your project.

### **Installation**

1. Save `jtbd_transform.py` to your local machine.  
2. Make the script executable:  
   Bash

```bash
chmod +x jtbd_transform.py
```

3. 

### **Usage**

You can now pass the file path directly as an argument or enter it when prompted:

Bash

```
# Pass path as an argument
./jtbd_transform.py path/to/file.adoc

# Or run interactively
./jtbd_transform.py
```

**Process Flow:**

1. **Input:** Path to the .adoc file (converted to absolute path for reliability).  
2. **Validation:** Verifies the file exists and confirms if it lacks a .adoc extension.  
3. **Branching:** Checks out a new branch. If the branch exists, it asks to switch/reuse.  
4. **Transformation:** Rewrites the file content while preserving technical markers.  
5. **Staging:** Adds the file to the Git index for immediate review.

---

## **Transformation Logic**

The script applies a series of regex patterns to ensure the documentation focuses on the *task*, not the *actor*.

### **Conversion Examples**

| Category | Original Phrasing | JTBD/Impersonal Result |
| :---- | :---- | :---- |
| **Questions** | "How do I migrate VMs?" | "How to migrate VMs" |
| **Inquiry** | "Can I use warm migration?" | "Whether to use warm migration" |
| **Complex Phrases** | "Allows you to scale..." | "Allows users to scale..." |
| **Directives** | "You should configure the network" | "To configure the network" |
| **Possessives** | "Your migration plan" | "The migration plan" |
| **Gerunds** | "To Migrating the data" | "Migrating the data" |

### **Protected Elements**

The script is highly "syntax-safe" and explicitly ignores:

* **Code Blocks:** Lines between `----` or `....` delimiters.  
* **Admonition Blocks:** Lines contained within `====` delimiters.  
* **Directives:** `include::`, `ifdef::`, `ifndef::`, and `endif::`.  
* **Metadata:** Attributes starting with : or block tags starting with `\[`.  
* **Comments:** Lines starting with //.

---

## **Technical Workflow**

1. **Repo Root Discovery:** Traverses upward from the file path to locate the .git directory.  
2. **Safety First:** Uses subprocess with `check=True` to ensure Git commands succeed before proceeding.  
3. **Content Parsing:** \* Reads the file line-by-line.  
   * Toggles in\_code\_block and in\_admonition\_block flags to skip technical content.  
   * Applies a multi-pass regex filter to titles and body text separately.  
4. **Cleanup:** Performs whitespace normalization while strictly preserving newlines.

---

## **Next Steps After Running**

Once the script finishes, your file is staged. You should:

1. **Review:** git diff \--cached to verify the transformation.  
2. **Commit:** git commit \-m "docs: transform \<filename\> to JTBD format".  
3. **Push:** git push origin jtbd-transformation-\<filename\>.

