# **AsciiDoc Short Description Validator**

This script scans AsciiDoc (.adoc) files to validate the length, formatting, and content of \[role="\_abstract"\] paragraphs (short descriptions).

Crucially, it measures the length of the abstract **after** attribute expansion and HTML rendering, ensuring you get an accurate character count of the final output rather than the raw source text. The results are exported to a comprehensive Excel spreadsheet (.xlsx) with categorized sheets for different types of warnings and errors.

## **Features**

* **Accurate Rendering:** Uses asciidoctor to render the AsciiDoc to HTML before measuring lengths.  
* **Recursive Include Resolution:** Automatically scans the target directory and seamlessly follows include:: directives (handling both git-root-relative and file-relative paths) so only modules actively used by your assemblies are checked.  
* **Attribute Auto-Discovery:** Automatically searches the Git repository root for known common attribute files to apply during rendering.  
* **Categorized Excel Reporting:** Outputs a cleanly formatted .xlsx file with separate sheets for each error type.

## **Validation Rules**

The script checks for the following conditions:

1. **Length Range:** Abstracts must be between **50 and 300 characters** (rendered).  
2. **No Conditionals:** Abstracts should not contain ifdef::, ifndef::, or ifeval:: directives, as this causes the rendered length to vary unpredictably depending on the build target.  
3. **No Trailing Colons:** Abstracts should be complete sentences summarizing the content, not introductory fragments ending in a colon (:).  
4. **No Self-Referential Language:** Abstracts should describe what the reader will learn or accomplish, rather than referring to the document itself (e.g., avoids phrases like *"This topic describes..."* or *"The following table..."*).

## **Prerequisites**

The following prerequisites are required:

### **System Dependencies**

The script relies on a few underlying system tools to process the AsciiDoc files and handle XML parsing:

* **asciidoctor:** gem install asciidoctor  
* **xmllint:** apt install libxml2-utils (Ubuntu/Debian) or brew install libxml2 (macOS)  
* **git:** Required for path resolution and attribute auto-discovery.

### **Python Dependencies**

Ensure you have Python 3 installed along with the following packages for Excel generation:

Bash

```
pip install pandas openpyxl
```

## **Usage**

Run the script from your terminal, pointing it to the directory you want to scan. If no directory is provided, it defaults to the current working directory (.).

Bash

```
python validate_shortdescs.py [DIRECTORY] [OPTIONS]
```

### **Options**

| Option | Description |
| :---- | :---- |
| DIRECTORY | The directory to scan. All .adoc files in this directory (and any modules they include) will be processed. |
| \--attrs FILE | Path to an additional AsciiDoc attributes file to parse. Can be specified multiple times. |
| \--ifdef-tag TAG | When parsing attributes files, treats TAG as defined (includes ifdef::TAG\[\] blocks, excludes ifndef::TAG\[\]). Can be specified multiple times. |
| \--no-auto-attrs | Disables the automatic discovery of known repository attribute files. |

### **Example**

Bash

```
python validate_shortdescs.py ./backup_and_restore --ifdef-tag openshift-enterprise
```

## **Output**

The script generates an Excel workbook named shortdesc-validation-report-YYYY-MM-DD.xlsx in your current directory.

The workbook contains the following sheets, depending on the errors found during the scan:

* **Summary:** A high-level overview of the total files scanned and the percentage of files passing/failing each rule.  
* **Too Short:** Files with an abstract under 50 characters (sorted shortest to longest).  
* **Too Long:** Files with an abstract over 300 characters (sorted longest to shortest).  
* **Conditionals:** Files containing conditional syntax inside the \[role="\_abstract"\] block.  
* **Ends with Colon:** Files where the abstract ends with a colon.  
* **Self-Referential:** Files where the abstract opens with introductory or self-referential phrasing.

