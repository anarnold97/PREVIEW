# **CQA 2.1 Shortdesc Fixer**

The cqa\_shortdesc\_fixer.py script scans your documentation repository to identify files missing the \[role="\_abstract"\] attribute or files where the existing abstract is too short or too long. It can automatically generate descriptions based on the topic title, apply overrides from a CSV, and truncate or pad existing text to meet standards.

## **Features**

* **Missing Abstract Detection:** Identifies .adoc files lacking a \[role="\_abstract"\] block.  
* **Automatic Generation:** Derives a compliant short description from the document's Level 1 title (\= Title).  
* **Length Enforcement:** \* **Minimum:** Pads descriptions shorter than **50 characters** using a default suffix.  
  * **Maximum:** Truncates descriptions longer than **300 characters** at the nearest word boundary.  
* **Manual Overrides:** Supports a shortdesc\_overrides.csv file for providing custom descriptions for specific files.  
* **Smart Insertion:** Places new abstracts correctly after the title and any initial document attributes (like :context:).  
* **Dry Run Mode:** Preview all intended changes without modifying files.

---

## **Installation & Requirements**

* **Python Version:** Python 3.6+  
* **Dependencies:** Uses standard library only (pathlib, re, argparse, csv).  
* **Permissions:** Ensure you have write permissions for the documentation files.

---

## **Usage**

### **Basic Command**

Run the script from the root of your repository (or pass the path to the repo):

Bash

```
python3 cqa_shortdesc_fixer.py /path/to/your/repo
```

### **Previewing Changes (Recommended)**

To see which files would be modified without actually changing them, use the \--dry-run flag:

Bash

```
python3 cqa_shortdesc_fixer.py --dry-run
```

### **Using Overrides**

If you want to specify a high-quality manual description instead of the auto-generated title-based one, create a file named shortdesc\_overrides.csv in your repository root:

**Format:** relative/path/to/file.adoc,Your custom short description text.

---

## **Logic and Standards**

The script follows these CQA 2.1 constraints:

| Constraint | Value | Action |
| :---- | :---- | :---- |
| **Minimum Length** | 50 chars | Appends: *" Use this when writing or matching rules."* |
| **Maximum Length** | 300 chars | Truncates at word boundary and appends "…" |
| **Placement** | Post-Title | Inserted after the \= title and any attribute headers. |
| **Exclusions** | website/ | The script automatically skips files in the website directory. |

### **Abstract Structure**

The script ensures the following structure is present:

AsciiDoc

```
= Topic Title
:context: some-context

[role="_abstract"]
This is the short description that meets the length requirements of 50-300 characters.
```

---

## **How it Handles Existing Content**

1. **If Abstract is missing:** It creates one using the CSV override or the topic title.  
2. **If Abstract is \> 300 chars:** It truncates the text to \~297 characters \+ ….  
3. **If Abstract is \< 50 chars:** It appends a standard functional suffix until the length requirement is met.

## **Contributing**

When modifying the script, ensure that the RE\_TITLE and RE\_ROLE\_ABSTRACT regex patterns remain compatible with standard AsciiDoc syntax.

