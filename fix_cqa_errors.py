#!/usr/bin/env python3
"""
Fix CQA 2.1 and DITA assessment errors and warnings in vm_networking .adoc files.
For each fix, the script shows what will change and asks: "Apply this fix? (y/n)".

Usage:
  cd virt/vm_networking && python3 fix_cqa_errors.py
  # or from repo root:
  python3 virt/vm_networking/fix_cqa_errors.py
  # or with explicit path:
  python3 fix_cqa_errors.py /path/to/virt/vm_networking

Fixes applied (when accepted):
  - Title typo and section ID typo in virt-accessing-vm-internal-fqdn.adoc
  - Trailing spaces in .adoc files
  - ID/context alignment (virt-configuring-physical-networks, virt-networking-overview)
  - Merge Additional resources in virt-exposing-vm-with-service.adoc (no content between includes)
  - Add [role="_abstract"] where missing (before first paragraph after toc::[])
"""

import os
import re
import sys
from pathlib import Path


def get_vm_networking_dir() -> Path:
    """Resolve vm_networking directory (script's parent or cwd)."""
    script_dir = Path(__file__).resolve().parent
    if (script_dir / "virt-networking-overview.adoc").exists():
        return script_dir
    cwd = Path.cwd()
    if (cwd.name == "vm_networking" and (cwd / "virt-networking-overview.adoc").exists()):
        return cwd
    if (cwd / "virt" / "vm_networking" / "virt-networking-overview.adoc").exists():
        return cwd / "virt" / "vm_networking"
    return script_dir


def ask(question: str, default: str = "y") -> bool:
    """Prompt and return True for y/yes, False for n/no."""
    d = default.lower()
    prompt = f"{question} (y/n) [{d}]: "
    while True:
        try:
            ans = input(prompt).strip().lower() or d
        except EOFError:
            return d == "y"
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer y or n.")


def apply_fix(path: Path, old: str, new: str, desc: str) -> bool:
    """Replace first occurrence of old with new in path. Return True if applied."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        print(f"  [SKIP] Pattern not found in {path.name}")
        return False
    if ask(desc):
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print("  Applied.")
        return True
    print("  Skipped.")
    return False


def fix_trailing_spaces(path: Path) -> bool:
    """Remove trailing spaces and trailing newlines from file. Return True if changed."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    new_lines = [line.rstrip() for line in lines]
    # Normalize final newline
    new_text = "\n".join(new_lines)
    if not new_text.endswith("\n"):
        new_text += "\n"
    if new_text != text:
        if ask(f"Remove trailing spaces and normalize newlines in {path.name}?"):
            path.write_text(new_text, encoding="utf-8")
            print("  Applied.")
            return True
    return False


def add_abstract(path: Path) -> bool:
    """
    If file has toc::[] and no [role="_abstract"], insert [role="_abstract"] and blank line
    before the first content paragraph (first non-empty, non-directive line after toc::[]).
    Skips leading ifdef/ifndef/endif to find the first real paragraph.
    """
    text = path.read_text(encoding="utf-8")
    if '[role="_abstract"]' in text:
        return False

    # Find toc::[]
    toc_match = re.search(r"toc::\[\]\s*\n", text)
    if not toc_match:
        return False

    after_toc = text[toc_match.end() :]
    lines = after_toc.split("\n")
    first_para_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            if first_para_lines:
                break
            i += 1
            continue
        if stripped.startswith("include::"):
            break
        if stripped.startswith("[NOTE]") or stripped.startswith("[IMPORTANT]") or stripped.startswith("[WARNING]"):
            break
        if stripped.startswith("endif::") or stripped.startswith("ifdef::") or stripped.startswith("ifndef::"):
            i += 1
            continue
        if stripped.startswith("[role="):
            break
        # First content line; take this paragraph (until blank or directive)
        first_para_lines.append(line)
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if next_line.strip() == "":
                break
            if next_line.strip().startswith("include::") or next_line.strip().startswith("["):
                break
            first_para_lines.append(next_line)
            i += 1
        break
    if not first_para_lines:
        return False

    first_para = "\n".join(first_para_lines)
    # Insert [role="_abstract"]\n\n before this paragraph
    marker = after_toc[: after_toc.index(first_para)]
    insert = marker + '[role="_abstract"]\n\n' + first_para
    rest = after_toc[after_toc.index(first_para) + len(first_para) :]
    new_after_toc = insert + rest
    new_text = text[: toc_match.end()] + new_after_toc

    if new_text == text:
        return False
    preview = first_para[:120] + "..." if len(first_para) > 120 else first_para
    if ask(f"Add [role=\"_abstract\"] before first paragraph in {path.name}?\n  Preview: {preview!r}"):
        path.write_text(new_text, encoding="utf-8")
        print("  Applied.")
        return True
    return False


def fix_exposing_vm_additional_resources(path: Path) -> bool:
    """
    Merge Additional resources in virt-exposing-vm-with-service: remove the block between
    includes (block title .Additional resources + MetalLB links) and add those links to
    the final == Additional resources section.
    """
    text = path.read_text(encoding="utf-8")
    old_between = """
include::modules/virt-about-services.adoc[leveloffset=+1]

// Hiding in ROSA/OSD as not supported
ifndef::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]
[role="_additional-resources"]
.Additional resources
* xref:../../networking/networking_operators/metallb-operator/metallb-operator-install.adoc#metallb-operator-install_metallb-operator-install[Installing the MetalLB Operator]
* xref:../../networking/ingress_load_balancing/metallb/metallb-configure-services.adoc#metallb-configure-services[Configuring services to use MetalLB]
endif::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]

include::modules/virt-dual-stack-support-services.adoc[leveloffset=+1]
"""
    new_between = """
include::modules/virt-about-services.adoc[leveloffset=+1]

include::modules/virt-dual-stack-support-services.adoc[leveloffset=+1]
"""
    if old_between not in text:
        return False

    # Also add MetalLB links to the final Additional resources section
    old_final = """ifndef::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]
[role="_additional-resources"]
[id="additional-resources_creating-service-vm"]
== Additional resources
* xref:../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-nodeport.adoc#configuring-ingress-cluster-traffic-nodeport[Configuring ingress cluster traffic using a NodePort]
* xref:../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-load-balancer.adoc#configuring-ingress-cluster-traffic-load-balancer[Configuring ingress cluster traffic using a load balancer]
endif::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]"""
    new_final = """ifndef::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]
[role="_additional-resources"]
[id="additional-resources_creating-service-vm"]
== Additional resources
* xref:../../networking/networking_operators/metallb-operator/metallb-operator-install.adoc#metallb-operator-install_metallb-operator-install[Installing the MetalLB Operator]
* xref:../../networking/ingress_load_balancing/metallb/metallb-configure-services.adoc#metallb-configure-services[Configuring services to use MetalLB]
* xref:../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-nodeport.adoc#configuring-ingress-cluster-traffic-nodeport[Configuring ingress cluster traffic using a NodePort]
* xref:../../networking/ingress_load_balancing/configuring_ingress_cluster_traffic/configuring-ingress-cluster-traffic-load-balancer.adoc#configuring-ingress-cluster-traffic-load-balancer[Configuring ingress cluster traffic using a load balancer]
endif::openshift-rosa,openshift-dedicated,openshift-rosa-hcp[]"""

    new_text = text.replace(old_between, new_between, 1).replace(old_final, new_final, 1)
    if new_text == text:
        return False
    if ask("Merge Additional resources in virt-exposing-vm-with-service (remove content between includes, single section at end)?"):
        path.write_text(new_text, encoding="utf-8")
        print("  Applied.")
        return True
    return False


def run_fixes(base: Path) -> None:
    base = base.resolve()
    if not base.is_dir():
        print(f"Not a directory: {base}", file=sys.stderr)
        sys.exit(1)

    fixes_applied = 0

    # --- 1. virt-accessing-vm-internal-fqdn: title double space ---
    f = base / "virt-accessing-vm-internal-fqdn.adoc"
    if f.exists():
        print("\n--- Fix: Title typo (double space) in virt-accessing-vm-internal-fqdn.adoc ---")
        text = f.read_text(encoding="utf-8")
        if "virtual machine  by" in text:
            if ask("Change 'virtual machine  by' to 'virtual machine by' in title?"):
                f.write_text(text.replace("virtual machine  by", "virtual machine by", 1), encoding="utf-8")
                print("  Applied.")
                fixes_applied += 1
        else:
            print("  [SKIP] Pattern not found.")

    # --- 2. virt-accessing-vm-internal-fqdn: section id typo ---
    f = base / "virt-accessing-vm-internal-fqdn.adoc"
    if f.exists():
        print("\n--- Fix: Section ID typo (accesing -> accessing) ---")
        if apply_fix(
            f,
            '[id="additional-resources_virt-accesing-vm-internal-fqdn"]',
            '[id="additional-resources_virt-accessing-vm-internal-fqdn"]',
            "Fix section id typo virt-accesing -> virt-accessing?",
        ):
            fixes_applied += 1

    # --- 3. virt-accessing-vm-internal-fqdn: trailing spaces (full file) ---
    f = base / "virt-accessing-vm-internal-fqdn.adoc"
    if f.exists():
        print("\n--- Fix: Trailing spaces in virt-accessing-vm-internal-fqdn.adoc ---")
        if fix_trailing_spaces(f):
            fixes_applied += 1

    # --- 4. virt-configuring-physical-networks: id and context with virt- prefix ---
    f = base / "virt-configuring-physical-networks.adoc"
    if f.exists():
        print("\n--- Fix: Align id/context with virt- prefix (virt-configuring-physical-networks) ---")
        text = f.read_text(encoding="utf-8")
        new_text = (
            text.replace('[id="configuring-physical-networks"]', '[id="virt-configuring-physical-networks"]')
            .replace(":context: configuring-physical-networks", ":context: virt-configuring-physical-networks")
        )
        if new_text != text and ask("Set id and context to virt-configuring-physical-networks to match filename?"):
            f.write_text(new_text, encoding="utf-8")
            print("  Applied.")
            fixes_applied += 1

    # --- 5. virt-configuring-physical-networks: trailing space on include line ---
    f = base / "virt-configuring-physical-networks.adoc"
    if f.exists():
        print("\n--- Fix: Trailing space in virt-configuring-physical-networks.adoc ---")
        if fix_trailing_spaces(f):
            fixes_applied += 1

    # --- 6. virt-networking-overview: id to match context ---
    f = base / "virt-networking-overview.adoc"
    if f.exists():
        print("\n--- Fix: Assembly id to match context (virt-networking -> virt-networking-overview) ---")
        if apply_fix(
            f,
            '[id="virt-networking"]',
            '[id="virt-networking-overview"]',
            "Change [id] to virt-networking-overview to match :context:?",
        ):
            fixes_applied += 1

    # --- 7. virt-exposing-vm-with-service: merge Additional resources ---
    f = base / "virt-exposing-vm-with-service.adoc"
    if f.exists():
        print("\n--- Fix: Merge Additional resources (no content between includes) ---")
        if fix_exposing_vm_additional_resources(f):
            fixes_applied += 1

    # --- 8. Add [role="_abstract"] to assemblies that lack it ---
    assemblies_without_abstract = [
        "virt-connecting-vm-to-default-pod-network.adoc",
        "virt-connecting-vm-to-ovn-secondary-network.adoc",
        "virt-accessing-vm-internal-fqdn.adoc",
        "virt-accessing-vm-secondary-network-fqdn.adoc",
        "virt-hot-plugging-network-interfaces.adoc",
        "virt-exposing-vm-with-service.adoc",
        "virt-connecting-vm-to-service-mesh.adoc",
        "virt-connecting-vm-to-secondary-udn.adoc",
        "virt-configuring-viewing-ips-for-vms.adoc",
        "virt-setting-interface-link-state.adoc",
        "virt-dedicated-network-live-migration.adoc",
        "virt-using-dpdk-with-sriov.adoc",
        "virt-connecting-vm-to-primary-udn.adoc",
    ]
    print("\n--- Fix: Add [role=\"_abstract\"] where missing ---")
    for name in assemblies_without_abstract:
        f = base / name
        if f.exists():
            print(f"\n  File: {name}")
            if add_abstract(f):
                fixes_applied += 1

    # --- 9. Trailing spaces in all .adoc files ---
    print("\n--- Fix: Trailing spaces in remaining .adoc files ---")
    for f in sorted(base.glob("*.adoc")):
        text = f.read_text(encoding="utf-8")
        if any(line != line.rstrip() for line in text.split("\n")):
            print(f"  File: {f.name}")
            if fix_trailing_spaces(f):
                fixes_applied += 1

    print(f"\n--- Done. Fixes applied: {fixes_applied} ---")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base = Path(sys.argv[1])
    else:
        base = get_vm_networking_dir()
    print(f"Using directory: {base}")
    run_fixes(base)
