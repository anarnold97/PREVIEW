# **MTV Documentation JTBD Transformation**

**Subject:** Scaling the Migration Toolkit for Virtualization (MTV) Docs via JTBD and AI Automation

---

## **1\. Executive Summary**

This report outlines a strategic transition for the MTV documentation from a feature-focused structure to a **Jobs to be Done (JTBD)** framework. By leveraging AI-driven automation, a team of two writers can reorganize the entire repository into a task-based Table of Contents (TOC) that aligns with user motivations and prepares content for seamless integration into AEM.

---

## **2\. The JTBD Strategy**

Jobs to be Done (JTBD) is a framework that represents a user's true motivations and desired outcomes rather than just a list of product features.

* **The Core Formula:** Every topic is framed by the template: *"When \[situation\], I want to \[motivation\], so I can \[expected outcome\]"*.  
* **Timelessness:** While UI buttons and CLI commands change, the user's "job" (e.g., "Select a Migration Strategy") remains timeless.  
* **User Needs focus:** Each job is mapped to a specific documentation artifact—such as a checklist, comparison matrix, or YAML example—to ensure the user achieves their goal.

---

## **3\. Mapping the Transformation (The "Before and After")**

We have identified 17 core jobs within the MTV documentation that must be transformed from feature-centric chapters into outcome-oriented topics.

| Original Feature-Focused Title | New Job-Focused Title | User Need Artifact |
| :---- | :---- | :---- |
| Chapter 1: Planning a Migration | **Understand the Migration Process** | Step-by-step roadmap |
| Chapters 2 & 3: Migration Modes | **Select a Migration Strategy** | Comparison matrix (Cold/Warm/Live) |
| Chapter 4: Prerequisites | **Validate Target Environment** | Pre-flight hardware/network checklist |
| 4.11 VMware Prerequisites | **Ensure VMware is Ready** | Specific vSphere roles/versions |
| Chapter 5: Installing MTV | **Set up the Migration Toolkit** | Operator Hub installation steps |
| Chapter 8: Mapping Networks | **Define Network/Storage Pathways** | Namespace/storage bridging guide |
| Chapter 9: VMware vSphere | **Migrate from VMware vSphere** | Focused VMware execution guide |
| Chapter 10: RHV | **Migrate from RHV** | API/Credential requirements |
| Chapter 11: OpenStack | **Migrate from OpenStack** | Metadata/image format guidance |
| Chapter 12: OVA Files | **Migrate from OVA Files** | Instructions for hosting/pointing to OVA |
| Chapter 13: OpenShift | **Migrate between Clusters** | Cluster-to-cluster migration steps |
| Chapter 6: Web Console | **Run Migration using Web Console** | UI walkthrough with screenshots |
| Chapter 7: CLI | **Run Migration using CLI** | YAML examples and oc syntax |
| 6.4 Renaming VMs | **Rename VMs for OpenShift** | DNS-1123 naming restriction guide |
| 6.5 Target Power State | **Control Post-Migration Power** | Power-on toggle location guide |
| 5.4 Controller Settings | **Fine-Tune for Throughput** | max\_vm\_inflight parameter guide |
| (Scattered details) | **Troubleshoot Common Failures** | Centralized error code/log table |

---

## **4\. Automation: The "Context Injection" Script**

To scale this work for a two-person team, we utilize a Python script that pulls original .adoc files from the [MTV GitHub repository](https://github.com/kubev2v/forklift-documentation) and injects them into Claude with specific JTBD instructions.

Python

```
import anthropic
import os

client = anthropic.Anthropic(api_key="YOUR_CLAUDE_API_KEY")

# Mapping data for automation
migration_tasks = [
    {
        "before_file": "modules/con_planning-a-migration.adoc",
        "job_title": "Understand the Migration Process",
        "jtbd_statement": "When I am tasked with a migration, I want to see the end-to-end workflow so I can plan my timeline accurately.",
        "user_need": "High-level architectural overview and a step-by-step roadmap."
    },
    # Add all 17 mappings from Section 3 here...
]

def generate_jtbd_draft(task):
    repo_path = "./forklift-documentation/"
    with open(os.path.join(repo_path, task['before_file']), 'r') as f:
        source_content = f.read()

    prompt = f"""
    TARGET JOB: {task['job_title']}
    JTBD STATEMENT: {task['jtbd_statement']}
    USER NEED: {task['user_need']}
    
    ORIGINAL CONTENT: {source_content}
    
    TASK: Rewrite as a JTBD-focused DITA module. Lead with the statement. 
    Focus on the User Need. Remove feature-listing fluff.
    """
    return client.messages.create(model="claude-3-5-sonnet-20240620", messages=[{"role": "user", "content": prompt}])
```

---

## **5\. Quality Assurance: The "Style Guide" Script**

Writers run this script locally to maintain a consistent JTBD standard during their technical reviews.

Python

```
def jtbd_checklist():
    print("✅ JTBD DEFINITION OF DONE")
    print("1. Leads with 'When... I want to... So I can...'")
    print("2. Fulfills specific 'User Need' artifact (Checklist/Matrix)? ")
    print("3. No 'Walls of Text' - scannable?")
    print("4. Technically accurate vs source repo?")
    print("5. Does it focus on a TIMELESS job?")

if __name__ == "__main__":
    jtbd_checklist()
```

---

## **6\. Execution Plan & JIRA Roadmap**

The workload is split between two writers to ensure coverage of both infrastructure and execution paths.

| Ticket ID | Title | Writer Assignment | Definition of Done (DoD) |
| :---- | :---- | :---- | :---- |
| **MTV-01** | **Automated Extraction** | Writer A | 17 .adoc drafts generated with JTBD headers. |
| **MTV-02** | **Technical Review (CQA)** | Writers A & B | Content fulfills user need artifact; Vale checks pass. |
| **MTV-03** | **DITA Assembly** | Writer B | DITA map reflects job-focused TOC hierarchy. |

---

