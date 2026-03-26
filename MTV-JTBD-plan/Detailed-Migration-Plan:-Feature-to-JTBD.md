## **Detailed Migration Plan: Feature-to-JTBD**

The migration is divided into four distinct phases to ensure technical accuracy and user-centricity.

### 

### ---

### 

### **Phase 1: Foundation & Data Mapping**

* **Inventory Audit:** Utilize the `MTV-JTBD.yml` file to finalize the mapping of 17 core jobs against the existing `.adoc` source files.  
* **DITA Architecture:** Initialize the `mtv_jtbd_migration_master_map` to define the new navigation hierarchy.

### 

### ---

### 

### **Phase 2: Automated Content Transformation**

* **Context Injection:** Execute the Python transformation script to pass original source content through an LLM (Claude 3.5 Sonnet) with JTBD-specific prompts.  
* **Module Generation:** Convert transformed text into 17 individual `.dita` modules, each leading with a standard JTBD statement: *"When \[situation\], I want to \[motivation\], so I can \[outcome\]."*

---

### **Phase 3: Technical Review & "Artifact" Alignment**

* **User Need Validation:** Writers manually review each module to ensure it provides the specific artifact required (e.g., the "Comparison Matrix" for selecting a strategy or the "Pre-flight Checklist" for validating environments).  
* **Peer Review:** A "Two-Pass" system where Writer A checks technical accuracy against the source repo while Writer B checks JTBD style compliance.

### 

### ---

###  **Phase 4: Integration & Build**

* **DITA Assembly:** Nest the validated topics into the master map.  
* **AEM Integration:** Upload the DITA map to the Adobe Experience Manager (AEM) environment for final rendering.

---

## **2\. Automation Strategy**

Automation is used to handle the "heavy lifting" of restructuring prose and verifying style standards.

### 

### ---

### 

### **What Can Be Automated**

1. **Bulk Transformation:** Converting 17+ chapters of feature descriptions into task-based DITA modules.  
2. **Style Compliance:** Checking for the presence of JTBD headers and scannable formatting (bullet points/tables).  
3. **Metadata Injection:** Automatically adding the "User Needs Statement" to the short description of DITA files to improve searchability.

### 

### ---

###   **Transformation Pseudo-code (Bulk Processor)**

This script expands on the context injection logic to process the entire YAML mapping in one batch.

Python

```
import anthropic
import yaml

# Initialize AI Client
client = anthropic.Anthropic(api_key="KEY")

def process_bulk_migration(yaml_file):
    # Load the 17 job mappings
    with open(yaml_file, 'r') as f:
        mapping_data = yaml.safe_load(f)

    for job in mapping_data['mtv_documentation_transformation']:
        # 1. Fetch source content from GitHub local clone
        source_text = fetch_original_adoc(job['original_reference'])
        
        # 2. Construct the prompt
        prompt = f"""
        REWRITE TASK: Convert this feature documentation into a JTBD DITA task.
        JTBD STATEMENT: {job['jtbd_statement']}
        REQUIRED ARTIFACT: {job['user_needs_statement']}
        SOURCE: {source_text}
        
        RULES: Lead with the JTBD statement. Use <task> or <reference> DITA tags. 
        Focus on the outcome, not just the button location.
        """
        
        # 3. Call AI and save result as .dita
        transformed_xml = client.messages.create(model="claude-3-5-sonnet", content=prompt)
        save_to_dita_repo(job['job_focused_title'], transformed_xml)

if __name__ == "__main__":
    process_bulk_migration("MTV-JTBD.yml")
```

---

## **3\. Collaboration & JIRA Strategy**

To balance the workload, **Writer A** focuses on infrastructure and automation, while **Writer B** focuses on execution workflows and post-migration performance.

---

### **JIRA Ticket: MTV-01 — Automated JTBD Extraction**

* **Description:** Set up the Python environment and run the bulk transformation script to generate the 17 initial DITA drafts.  
* **Tasks:**  
  * Configure `anthropic` API access.  
  * Map all 17 `.adoc` source files in the local repository.  
  * Run extraction and verify 17 files exist in the `/drafts` folder.  
* **Acceptance Criteria:**  
  * 17 DITA drafts generated.  
  * Each file includes the "When... I want to... So I can..." header.

### 

### ---

### 

### **JIRA Ticket: MTV-02 — Technical Review (Source Provider Readiness)**

* **Description:** Manually review and edit the "Readying" jobs (VMware, RHV, OpenStack) to ensure credential and API requirements are 100% accurate.  
* **Tasks:**  
  * Review `ensure-vmware-ready.dita` against vSphere 7.0/8.0 docs.  
  * Review `migrate-from-openstack.dita` for metadata accuracy.  
  * Verify the "Pre-flight checklist" artifact is technically sound.  
* **Acceptance Criteria:**  
  * Passes the `jtbd_checklist()` script.  
  * Verified by the Engineering lead for technical correctness.

### 

### ---

### 

### **JIRA Ticket: MTV-03 — DITA Mapping & AEM Integration**

* **Description:** Finalize the TOC hierarchy and ensure the DITA map reflects the job-based user journey.  
* **Tasks:**  
  * Assemble `mtv_jtbd_migration_master_map`.  
  * Validate all `href` links to ensure no broken references.  
  * Trigger an AEM build and verify the "After" navigation state.  
* **Acceptance Criteria:**  
  * DITA map builds without errors.  
  * Navigation reflects 17 jobs instead of original chapter numbers.

---

