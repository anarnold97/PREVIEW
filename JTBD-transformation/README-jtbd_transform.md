# **README \- jtbd\_transform.py**

jtbd\_transform.py is an automation tool designed to refactor AsciiDoc documentation into a **Jobs To Be Done (JTBD)** format. It moves away from passive or wordy instructions to direct, task-oriented language while automating the Git branching and staging process.

## **Key Features**

* **Task-Oriented Transformation:** Converts "how-to" questions and "you can" statements into direct imperative commands (e.g., "Use," "Configure," "Migrate").  
* **Deep AsciiDoc Awareness:** Intelligently ignores technical syntax to prevent document corruption, including:  
  * Code blocks (\----, ....) and Admonition blocks (\====).  
  * Comments (//) and Include statements (include::).  
  * Conditionals (ifdef, ifndef, endif).  
  * Admonition headers (e.g., \[NOTE\], \[TIP\]).  
* **Automated Git Workflow:** \* Automatically locates the repository root.  
  * Creates a unique feature branch: jtbd-transformation-\<filename\>.  
  * Stages changes (git add) automatically for immediate review.  
* **Safety First:** Uses absolute path conversion and validates file existence before making modifications.

---

## **Getting Started**

### **Prerequisites**

* **Python 3.6+**  
* **Git:** Must be executed within a Git repository.  
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

The script accepts the file path as an argument or via interactive prompt:

Bash

```
# Argument-based execution
./jtbd_transform.py path/to/file.adoc

# Interactive execution
./jtbd_transform.py
```

---

## **Transformation Logic**

The script focuses on removing filler words to make instructions more actionable.

### **Conversion Examples**

| Category | Original Phrasing | JTBD/Task-Oriented Result |
| :---- | :---- | :---- |
| **Questions** | "How do I/you migrate VMs?" | "How to migrate VMs" |
| **Direct Tasks** | "You can use the CLI" | "Use the CLI" |
| **Configuration** | "You can configure the network" | "Configure the network" |
| **Installation** | "You can install the operator" | "Install the operator" |
| **Titles** | "= How do I set up X?" | "= How to set up X" |

### **Protected Elements**

To ensure the document still builds correctly, the following are **not** transformed:

* **Technical Blocks:** Content inside \----, ...., or \====.  
* **Directives:** include::, ifdef::, ifndef::, and endif::.  
* **Metadata:** Attributes starting with : or block tags starting with \[ (unless they are standard admonition headers).  
* **Internal Notes:** Lines starting with //.

---

## **Technical Workflow**

1. **Repo Root Discovery:** The script climbs the directory tree from the file's location until it finds a .git folder.  
2. **Branch Management:** It checks for existing branches with the same name and prompts for a switch or exit to prevent accidental overwrites.  
3. **Content Parsing:**  
   * Reads the file line-by-line.  
   * Uses state flags (in\_code\_block, in\_admonition\_block) to skip protected sections.  
   * Applies regex patterns to body text and titles while preserving blank lines and newlines.  
4. **Staging:** Runs git add on the transformed file relative to the repo root.

---

## **Next Steps After Running**

1. **Review:** Run git diff \--cached to see the exact text changes.  
2. **Commit:** git commit \-m "docs: transform \<filename\> to JTBD format".  
3. **Push:** git push origin jtbd-transformation-\<filename\>.

