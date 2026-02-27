# fix_cqa_errors.py

A Python script that applies selected **CQA 2.1** and **DITA/AsciiDocDITA** fixes to the `.adoc` assembly files in the `vm_networking` directory. It does not read the assessment report; it uses built-in fix logic and prompts you to accept or skip each change.

## Requirements

- **Python 3.6+** (no extra packages)
- Run from the OpenShift docs repo (or pass the path to `virt/vm_networking`)

## Usage

From the `vm_networking` directory:

```bash
cd virt/vm_networking
python3 fix_cqa_errors.py
```

From the repo root:

```bash
python3 virt/vm_networking/fix_cqa_errors.py
```

With an explicit path:

```bash
python3 fix_cqa_errors.py /path/to/openshift-docs/virt/vm_networking
```

## Behavior

- The script **does not need** `CQA_and_DITA_Assessment_vm_networking.md` (or any report) to run.
- For **each fix** it:
  - Describes what it will change (and may show a short preview).
  - Asks: **Apply this fix? (y/n) [y]**.
- Answer **y** or press Enter to apply; **n** to skip. Only accepted fixes are written to disk.
- No “apply all” option; every fix is confirmed individually.

## Fixes applied (when you accept)

| Fix | Description |
|-----|-------------|
| **Title typo** | In `virt-accessing-vm-internal-fqdn.adoc`: `virtual machine  by` → `virtual machine by`. |
| **Section ID typo** | In `virt-accessing-vm-internal-fqdn.adoc`: `additional-resources_virt-accesing-vm-internal-fqdn` → `...virt-accessing...`. |
| **Trailing spaces** | Removes trailing spaces and normalizes newlines in `.adoc` files (prompted per file when needed). |
| **ID/context alignment** | In `virt-configuring-physical-networks.adoc`: sets `id` and `:context:` to `virt-configuring-physical-networks` to match the filename. |
| **Assembly ID** | In `virt-networking-overview.adoc`: `[id="virt-networking"]` → `[id="virt-networking-overview"]` to match `:context:`. |
| **Additional resources** | In `virt-exposing-vm-with-service.adoc`: removes the “Additional resources” block between `include::` directives and merges those links into the single `== Additional resources` section at the end. |
| **Short description** | Adds `[role="_abstract"]` and a blank line before the first content paragraph in assemblies that lack a short description (prompted per file, with a short preview of the paragraph). |

## Tips

- Ensure the repo is under version control so you can review or revert changes (e.g. `git diff`, `git checkout`).
- Run the script once, accept the fixes you want, then run Vale (e.g. asciidoctor-dita-vale) to confirm and catch any remaining issues.
