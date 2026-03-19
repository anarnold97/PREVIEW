

This script is a robust Python-based wrapper designed to automate documentation linting. It mimics a complex shell pipeline—specifically using find, xargs, and grep—but with better error handling and cross-platform compatibility.

It leverages asciidoctor-list-content to resolve included modules in AsciiDoc files and runs the **Vale** linter in parallel to generate a consolidated report.

---

## **Documentation Linter & Content Resolver**

### **Overview**

In complex AsciiDoc projects, a single .adoc file often "includes" many smaller modules. Simply linting the top-level files might miss content or context. This script:

1. **Discovers** all root .adoc files in a directory.  
2. **Resolves** all nested dependencies using list-content.  
3. **Filters** out administrative files (like attribute definitions).  
4. **Lints** the unique set of files using **Vale** across 8 parallel threads.  
5. **Aggregates** all findings into a single report.csv.

---

### **Prerequisites**

#### **1\. Tools & Engines**

* **Python 3.7+**: The core execution environment.  
* **Vale**: The syntax-aware linter. [Install Vale](https://www.google.com/search?q=https://vale.sh/docs/vale-cli/installation/).  
* **Asciidoctor List Content**: A Ruby gem used to find all include::\[\] references within your files.  
  Bash

```
gem install asciidoctor-list-content
```

* 

#### **2\. Configuration Files**

* **dita.ini**: This script expects a Vale configuration file (specifically named dita.ini by default) to be present in the working directory. This file defines your linting rules and styles.

---

### **Configuration**

Before running the script, you can modify the following variables at the top of the .py file:

| Variable | Description | Default Value |
| :---- | :---- | :---- |
| BASE\_DIR | The relative path to your documentation source. | "backup\_and\_restore/..." |
| VALE\_CONFIG | The name of your Vale configuration file. | "dita.ini" |
| OUTPUT\_CSV | The name of the generated report. | "report.csv" |
| MAX\_WORKERS | Number of parallel threads for Vale execution. | 8 |

---

### **How It Works**

#### **Step 1: Content Resolution**

The script performs a recursive search for all .adoc files. For every file found, it runs:

list-content \<file\_path\>

This ensures that if index.adoc includes module\_a.adoc, both are added to the linting queue. It uses a Python set to ensure each file is only linted once, even if it is included in multiple places.

#### **Step 2: Filtering**

It automatically excludes any files located in \_attributes/ directories. This prevents the linter from flagging errors in technical configuration files or variable definitions that aren't meant to be "prose."

#### **Step 3: Parallel Execution**

To handle large repositories quickly, the script uses concurrent.futures.ThreadPoolExecutor. With the default MAX\_WORKERS \= 8, it processes 8 files simultaneously, significantly reducing the time compared to a linear scan.

#### **Step 4: Reporting**

The output is captured in "line" format and saved to report.csv. Each line typically follows the Vale line format:

path/to/file.adoc:line:column:Style.Rule:Message

---

### **Usage**

1. Ensure your dita.ini and styles directory are in place.  
2. Place the script in your project root or adjust BASE\_DIR.  
3. Run the script:  
   Bash

```
python3 your_script_name.py
```

4. 

#### **Troubleshooting**

* **"Command not found"**: Ensure vale and list-content are in your system's $PATH.  
* **No files found**: Check the BASE\_DIR string. Ensure it matches your folder structure exactly.  
* **Empty report**: If Vale finds zero issues, the report.csv will be created but remain empty.

---

### **Performance Note**

Using ThreadPoolExecutor is ideal here because the script is **I/O bound** (waiting for external subprocesses to return). If you are running this on a machine with many cores, you can increase MAX\_WORKERS to further speed up the process.

