### **MTV Content Migration Cross-Reference**

This table serves as the blueprint for the "Q4 task" to map existing content to jobs and prepare for implementation in AEM.

| New DITA Topic Reference | Job-Focused Title (The "After") | Original Feature-Focused Source (The "Before") | Specific User Needs to Extract |
| :---- | :---- | :---- | :---- |
| understand-migration-process.dita | Understand the Migration Process | Chapter 1: Planning a Migration | High-level architectural overview and a step-by-step roadmap. |
| select-migration-strategy.dita | Select a Migration Strategy | Chapters 2 & 3: Migration Modes | Comparison matrix of Cold, Warm, and Live migration pros/cons. |
| validate-target-environment.dita | Validate Target Environment | Chapter 4: Prerequisites | Pre-flight checklist for hardware, storage, and networking requirements. |
| ensure-vmware-ready.dita | Ensure VMware is Ready | 4.11. VMware Prerequisites | Specific vSphere user roles and software versions required for MTV. |
| setup-migration-toolkit.dita | Set up the Migration Toolkit | Chapter 5: Installing MTV | Simple installation steps for the OpenShift Operator Hub. |
| define-pathways.dita | Define Network/Storage Pathways | Chapter 8: Mapping Networks | How to bridge different network namespaces and storage classes. |
| migrate-from-vsphere.dita | Migrate from VMware vSphere | Chapter 9: VMware vSphere | Focused execution guide tailored specifically for VMware sources. |
| migrate-from-rhv.dita | Migrate from RHV | Chapter 10: RHV | Specific API and credential requirements for connecting to RHV. |
| migrate-from-openstack.dita | Migrate from OpenStack | Chapter 11: OpenStack | Guidance on handling OpenStack-specific image formats and metadata. |
| migrate-from-ova.dita | Migrate from OVA Files | Chapter 12: OVA Files | Instructions on where to host and how to point MTV to OVA files. |
| migrate-between-clusters.dita | Migrate between Clusters | Chapter 13: OpenShift | Cluster-to-cluster migration steps using the MTV interface. |
| run-migration-console.dita | Run Migration using Web Console | Chapter 6: Web Console | UI walkthrough with screenshots of the migration wizard. |
| run-migration-cli.dita | Run Migration using CLI | Chapter 7: CLI | YAML examples and command-line syntax for migration CRDs. |
| rename-vms.dita | Rename VMs for OpenShift | 6.4. Renaming VMs | Naming restrictions (DNS-1123) and how to apply overrides. |
| control-post-migration-power.dita | Control Post-Migration Power | 6.5. Target Power State | Location of the "Power on after migration" toggle in the plan. |
| fine-tune-throughput.dita | Fine-Tune for Throughput | 5.4. Controller Settings | How to edit the max\_vm\_inflight parameter for the MTV controller. |
| troubleshoot-failures.dita | Troubleshoot Common Failures | (Scattered details) | Centralized troubleshooting table with log locations and error resolutions.  |

