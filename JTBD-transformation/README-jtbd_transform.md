# **JTBD Transform: AsciiDoc Stylist**

jtbd\_transform.py is a specialized automation tool designed to refactor AsciiDoc documentation. It converts subjective, person-centric phrasing into impersonal, action-oriented language consistent with the **Jobs To Be Done (JTBD)** framework.

Beyond text transformation, the script automates the Git workflow, ensuring your changes are isolated in a dedicated feature branch and staged for review.

## **Key Features**

* **Smart Transformation:** Replaces first/second-person pronouns with impersonal task statements.  
* **AsciiDoc Aware:** Intelligently ignores code blocks (\----, ....), attributes (:attr:), and block metadata (\[...\]) to prevent breaking technical syntax.  
* **Automated Git Workflow:** \* Detects the repository root automatically.  
  * Creates a unique branch based on the filename: jtbd-transformation-\<filename\>.  
  * Handles branch name collisions with interactive prompts.  
  * Stages changes (git add) automatically.  
* **Regex-Powered Refactoring:** Handles complex patterns including question-to-statement conversion and gerund cleanup (e.g., "To Migrating" → "Migrating").

---

## 

## **Getting Started**

### **Prerequisites**

* **Python 3.6+**  
* **Git** (The script must be executed within a Git repository).  
* **Local Fork:** Ensure you are working on a local branch of your project.

### **Installation**

1. Save jtbd\_transform.py to your local machine.  
2. Make the script executable:  
   Bash

```
chmod +x jtbd_transform.py
```

3. 

### **Usage**

Run the script and follow the interactive prompts:

Bash

```
./jtbd_transform.py
```

**Process Flow:**

1. **Input:** Provide the path to the .adoc file.  
2. **Validation:** The script verifies the file exists and is an AsciiDoc file.  
3. **Branching:** It checks out a new branch. If the branch exists, it asks if you'd like to reuse it.  
4. **Transformation:** It rewrites the file content.  
5. **Staging:** It adds the file to the Git index.

---

## **Dry Run Mode**

Before making any changes to your Git state, you can preview the transformations directly in the terminal:

Bash

```
./jtbd_transform.py path/to/file.adoc --dry-run
```

**What Dry Run does:**

* Generates a **Unified Diff** (`-` for removed lines, `+` for added lines).  
* Does **not** create a new branch.  
* Does **not** overwrite the original file.  
* Does **not** require a Git repository (useful for quick local testing).

---

## **Transformation Logic**

The script applies a series of regex patterns to ensure the documentation focuses on the *task*, not the *actor*.

### **Conversion Examples**

| Category | Original Phrasing | JTBD/Impersonal Result |
| :---- | :---- | :---- |
| **Questions** | "How do I migrate VMs?" | "How to migrate VMs" |
| **Inquiry** | "Can I use warm migration?" | "Whether to use warm migration" |
| **Intent** | "I want to install the operator" | "To install the operator" |
| **Directives** | "You should configure the network" | "To configure the network" |
| **Possessives** | "Your migration plan" | "The migration plan" |
| **Gerunds** | "To Migrating the data" | "Migrating the data" |

### **Protected Elements**

The script is designed to be "syntax-safe." It will **not** modify text inside:

* **Code Blocks:** Lines between \---- or .... delimiters.  
* **Attributes:** Lines starting with : (e.g., :description: ...).  
* **Block Tags:** Lines starting with \[ (e.g., \[id="target"\]).

---

## 

## **Technical Workflow (Under the Hood)**

1. **Repo Root Discovery:** The script traverses upward from the file path to find the .git directory.  
2. **Safety First:** It uses subprocess with check=True to ensure Git commands succeed before proceeding.  
3. **Content Parsing:** \* It reads the file line-by-line.  
   * It toggles an in\_code\_block flag to bypass technical snippets.  
   * It applies a multi-pass regex filter to titles and body text separately.  
4. **Cleanup:** It performs whitespace normalization to remove accidental double-spaces introduced during regex replacement.

**Visual Indicators:**

* \<span style="color:green"\>**Green (+)**\</span\>: New JTBD-style phrasing.  
* \<span style="color:red"\>**Red (-)**\</span\>: Original subjective/person-centric phrasing.  
* \<span style="color:cyan"\>**Cyan (@@)**\</span\>: Chunk headers (line numbers and context).

---

## 

## **Next Steps After Running**

Once the script finishes, your file is staged. You should:

1. **Review:** git diff \--cached to verify the transformation.  
2. **Commit:** git commit \-m "docs: transform \<filename\> to JTBD format"  
3. **Push:** git push origin jtbd-transformation-\<filename\>

---

