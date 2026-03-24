# **JTBD Mapping Script for MTA Documentation**

This script (jtbd\_apply\_mapping.py) automates the integration of **Jobs-to-be-Done (JTBD)** methodology into your MTA documentation (AsciiDoc files). It aligns technical content with user outcomes by injecting metadata and optimizing short descriptions for better searchability and clarity.

---

## **Features & Internal Logic**

The script operates as a **transformation pipeline** that parses the structure of your AsciiDoc files to find specific metadata locations and apply updates.

### **1\. Metadata Injection**

The script looks for the :\_(mod-docs-)?content-type: attribute (standard in Red Hat-style docs).

* **If found:** It inserts a JTBD comment block immediately after that line.  
* **If not found:** It prepends the block to the top of the file.

**Example Injected Block:**

AsciiDoc

```
:_mod-docs-content-type: ASSEMBLY
// JTBD job: migration-analysis
// Statement: When migrating an app, I want to analyze the source code so I can estimate effort.
// Persona: Developer
```

### **2\. Short Description (shortdesc) Algorithm**

The script prioritizes "Outcome-based" writing by updating the \[role="\_abstract"\] paragraph. It follows a specific fallback logic to generate the text:

| Priority | Source | Transformation / Rule |
| :---- | :---- | :---- |
| **1** | shortdesc\_focus | Uses the explicit string from the YAML mapping. |
| **2** | outcomes | Combines the first two outcome strings from the YAML. |
| **3** | statement | Converts "so I can \[action\]" into "So you can \[action\]." |
| **4** | **Min Length** | If \< 50 chars, appends: *"See the section for steps and options."* |
| **5** | **Max Length** | If \> 300 chars, truncates at the nearest word and adds a period. |

---

## **Configuration: jtbd-mapping.yaml**

The script expects a mapping file located at docs/jtbd-mapping.yaml. The YAML structure should follow this pattern:

YAML

```
jobs:
  - id: migration-analysis
    statement: "When migrating an app, I want to analyze the source code so I can estimate effort."
    persona: "Developer"
    outcomes:
      - "Identify potential migration issues."
      - "Generate a detailed transformation report."
    assemblies:
      - path: "assemblies/assembly_analyzing-code.adoc"
        shortdesc_focus: "Learn how to analyze your source code to identify migration risks."
    topics:
      - "modules/con_analysis-overview.adoc"
```

---

## **Usage**

Run the script from the root of your documentation repository. **Note:** Requires pip install pyyaml.

### **Common Commands**

| Command | Description |
| :---- | :---- |
| python scripts/jtbd\_apply\_mapping.py | Updates all assemblies listed in the mapping. |
| python scripts/jtbd\_apply\_mapping.py \--dry-run | Preview changes without modifying files. |
| python scripts/jtbd\_apply\_mapping.py \--report | Lists job-to-path mappings for a compliance audit. |
| python scripts/jtbd\_apply\_mapping.py \--topics | Also adds Job ID comments to the end of topic files. |
| python scripts/jtbd\_apply\_mapping.py \--mapping \<path\> | Specify a custom path to the YAML mapping file. |

---

## **RegEx & Pattern Matching**

The script uses Regular Expressions to ensure it doesn't break AsciiDoc formatting:

* **RE\_ROLE\_ABSTRACT**: Identifies the abstract role attribute.  
* **RE\_FIRST\_PARAGRAPH**: Captures the text immediately following the abstract role until it hits a double newline.  
* **JTBD\_BLOCK\_RE**: Ensures that if the script is run multiple times, it replaces the old JTBD block rather than duplicating it.

