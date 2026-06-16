#!/usr/bin/env python3

import os
import sys
import re
import argparse
import subprocess
from datetime import datetime
import pandas as pd

# --- Hardcoded fallback attributes --------------------------------------------
DEFAULT_ATTRS = [
    "attribute-missing=drop", "experimental", "openshift-enterprise",
    "product-title=OpenShift Container Platform", "product-version=4.17",
    "ocp-short=OCP", "oc-first=OpenShift CLI (oc)",
    "VirtProductName=OpenShift Virtualization", "VirtVersion=4.17",
    "oadp-short=OADP", "oadp-first=OpenShift API for Data Protection (OADP)",
    "project-short=MTV", "project-full=Migration Toolkit for Virtualization",
    "ProductShortName=MTA", "ProductName=migration toolkit for applications",
    "aws-short=AWS", "ibm-name=IBM", "ibm-z-name=IBM Z",
    "ibm-linuxone-name=IBM LinuxONE", "ibm-cloud-title=IBM Cloud",
    "op-system-base=RHEL", "op-system-base-full=Red Hat Enterprise Linux",
    "op-system-first=Red Hat Enterprise Linux CoreOS (RHCOS)",
    "op-system=RHCOS", "sno=single-node OpenShift",
    "rh-storage=OpenShift Data Foundation",
    "rh-storage-first=Red Hat OpenShift Data Foundation",
    "pipelines-shortname=Red Hat OpenShift Pipelines",
    "mtv-first=Migration Toolkit for Virtualization (MTV)",
    "rh-rhacm-first=Red Hat Advanced Cluster Management",
    "HCOCliKind=HyperConverged", "CNVNamespace=openshift-cnv"
]

KNOWN_ATTR_PATHS = [
    "_attributes/common-attributes.adoc",             # openshift-docs
    "documentation/modules/common-attributes.adoc",   # forklift
    "docs/topics/templates/document-attributes.adoc"  # mta-documentation
    "common/global/rhoso_attributes.adoc"             # RHOSO (docs-Red_Hat_Enterprise_Linux_OpenStack_Platform)
]

def check_dependencies():
    for cmd, install_msg in [
        ("asciidoctor", "gem install asciidoctor"),
        ("xmllint", "apt install libxml2-utils OR brew install libxml2"),
        ("git", "https://git-scm.com")
    ]:
        if subprocess.run(["which", cmd], capture_output=True).returncode != 0:
            print(f"Error: '{cmd}' is required but not found.")
            print(f"  Install: {install_msg}")
            sys.exit(1)

def get_git_root(search_dir):
    try:
        res = subprocess.run(["git", "-C", search_dir, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def parse_attrs_file(filepath, ifdef_tags, current_attrs):
    if not os.path.isfile(filepath):
        print(f"Warning: Attributes file '{filepath}' not found.", file=sys.stderr)
        return
    
    print(f"Loading attributes from: {filepath}")
    cond_stack = []
    
    def tag_active(tag):
        return tag in ifdef_tags

    def is_active():
        return all(cond_stack) if cond_stack else True

    attr_pattern = re.compile(r'^:([a-zA-Z][a-zA-Z0-9_-]*):(?:\s+(.*))?')
    ifdef_pattern = re.compile(r'^ifdef::([^\[]+)\[\]')
    ifndef_pattern = re.compile(r'^ifndef::([^\[]+)\[\]')

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            m_ifdef = ifdef_pattern.match(line)
            if m_ifdef:
                cond_stack.append(tag_active(m_ifdef.group(1)))
                continue
                
            m_ifndef = ifndef_pattern.match(line)
            if m_ifndef:
                cond_stack.append(not tag_active(m_ifndef.group(1)))
                continue
                
            if line.startswith("ifeval::"):
                cond_stack.append(False)  # Expressions cannot be evaluated statically
                continue
                
            if line.startswith("endif::"):
                if cond_stack:
                    cond_stack.pop()
                continue
                
            if is_active():
                m_attr = attr_pattern.match(line)
                if m_attr:
                    key = m_attr.group(1)
                    val = m_attr.group(2) or ""
                    current_attrs.append(f"{key}={val}")

def auto_discover_attrs(git_root, ifdef_tags, current_attrs):
    if not git_root:
        print("Warning: Not inside a git repo — skipping attribute auto-discovery.", file=sys.stderr)
        return
    for rel_path in KNOWN_ATTR_PATHS:
        candidate = os.path.join(git_root, rel_path)
        if os.path.isfile(candidate):
            parse_attrs_file(candidate, ifdef_tags, current_attrs)
            return
    print(f"Warning: No known attributes file found under '{git_root}'. Use --attrs to specify one.", file=sys.stderr)

def collect_scan_files(search_dir, git_root):
    seen = set()
    queue = []

    # --- Primary files
    for root_dir, _, files in os.walk(search_dir):
        for file in files:
            if file.endswith(".adoc"):
                path = os.path.abspath(os.path.join(root_dir, file))
                seen.add(path)
                queue.append(path)
    
    primary_count = len(queue)
    queue.sort()

    # --- Follow includes (BFS)
    include_pattern = re.compile(r'include::([^\[]+\.adoc)\[')
    i = 0
    while i < len(queue):
        filepath = queue[i]
        filedir = os.path.dirname(filepath)
        i += 1

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        for match in include_pattern.finditer(content):
            inc_path = match.group(1)
            
            # Skip unresolved attribute references
            if "{" in inc_path:
                continue

            resolved = ""
            
            # Step 1: git-root-relative
            if git_root and os.path.isfile(os.path.join(git_root, inc_path)):
                resolved = os.path.join(git_root, inc_path)
            
            # Step 2: file-relative
            if not resolved:
                abs_candidate = os.path.normpath(os.path.join(filedir, inc_path))
                if os.path.isfile(abs_candidate):
                    resolved = abs_candidate
            
            if resolved and resolved not in seen:
                seen.add(resolved)
                queue.append(resolved)
                
    queue.sort()
    module_count = len(queue) - primary_count
    return queue, primary_count, module_count

def display_path(filepath, git_root, search_dir):
    if git_root and filepath.startswith(git_root):
        return os.path.relpath(filepath, git_root)
    elif filepath.startswith(search_dir):
        return os.path.relpath(filepath, search_dir)
    return filepath

def extract_raw_abstract(filepath):
    lines = []
    in_abstract = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if '[role="_abstract"]' in line:
                    in_abstract = True
                    continue
                if in_abstract:
                    if not line.strip():  # blank line ends the block
                        break
                    lines.append(line)
    except Exception:
        pass
    return "".join(lines)

def main():
    check_dependencies()

    parser = argparse.ArgumentParser(description="AsciiDoc Short Description Validator")
    parser.add_argument("search_dir", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--attrs", action="append", default=[], help="Additional AsciiDoc attributes file")
    parser.add_argument("--ifdef-tag", action="append", default=[], help="Tag for ifdef parsing")
    parser.add_argument("--no-auto-attrs", action="store_true", help="Disable automatic attributes discovery")
    args = parser.parse_args()

    search_dir = os.path.abspath(args.search_dir)
    if not os.path.isdir(search_dir):
        print(f"Error: Directory '{search_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    git_root = get_git_root(search_dir)

    # Compile attributes
    asciidoctor_attrs = DEFAULT_ATTRS.copy()
    user_attrs = []
    
    if not args.no_auto_attrs:
        auto_discover_attrs(git_root, args.ifdef_tag, user_attrs)
    for attr_file in args.attrs:
        parse_attrs_file(attr_file, args.ifdef_tag, user_attrs)
        
    asciidoctor_attrs.extend(user_attrs)
    attr_args = []
    for a in asciidoctor_attrs:
        attr_args.extend(["-a", a])

    print(f"Collecting files from '{display_path(search_dir, git_root, search_dir)}'...")
    files_to_scan, primary_count, module_count = collect_scan_files(search_dir, git_root)
    total_files = len(files_to_scan)
    
    if total_files == 0:
        print(f"No .adoc files found in '{search_dir}'.", file=sys.stderr)
        sys.exit(0)

    print(f"Scope: {primary_count} files in target directory + {module_count} included modules = {total_files} total")
    print("Scanning...")

    # Data collections for Excel
    results = {
        "ok": 0, "no_abstract": 0, "cond_count": 0,
        "too_short": [], "too_long": [], "conditionals": [], 
        "colon": [], "self_ref": []
    }

    self_ref_regex = re.compile(
        r'^(This (topic|section|module|document|chapter|guide|page|procedure|reference|concept|assembly|book|content|article|information|table|list|figure|example)|The following )', 
        re.IGNORECASE
    )

    for idx, filepath in enumerate(files_to_scan, 1):
        pct = (idx * 100) // total_files
        print(f"\r[{pct:3d}%] {idx}/{total_files}: {os.path.basename(filepath)[:55]:<55}", end="", flush=True)

        relpath = display_path(filepath, git_root, search_dir)

        # 1. Render via asciidoctor
        cmd_ascii = ["asciidoctor"] + attr_args + ["-S", "safe", "-o", "-", filepath]
        res_ascii = subprocess.run(cmd_ascii, capture_output=True)
        html_output = res_ascii.stdout

        # 2. Extract abstract via xmllint
        cmd_xml = ["xmllint", "--html", "--xpath", 'normalize-space(//div[contains(@class,"_abstract")][1]/p)', "-"]
        res_xml = subprocess.run(cmd_xml, input=html_output, capture_output=True)
        text = res_xml.stdout.decode('utf-8').strip()

        if not text:
            results["no_abstract"] += 1
            continue

        length = len(text)
        first_120 = text[:120]

        # 3. Check for conditional syntax in raw text
        raw_abstract = extract_raw_abstract(filepath)
        if re.search(r'(ifdef|ifndef|ifeval|endif)::', raw_abstract):
            results["cond_count"] += 1
            results["conditionals"].append({
                "File": relpath, 
                "Note": "Conditional syntax — length may vary by build target"
            })

        # 4. Length checks
        if length < 50:
            results["too_short"].append({"Length": length, "File": relpath})
        elif length > 300:
            results["too_long"].append({"Length": length, "File": relpath})
        else:
            results["ok"] += 1

        # 5. Colon check
        if text.rstrip().endswith(":"):
            results["colon"].append({"File": relpath, "Abstract (first 120 chars)": first_120})

        # 6. Self-referential check
        if self_ref_regex.match(text):
            results["self_ref"].append({"File": relpath, "Abstract (first 120 chars)": first_120})

    print() # clear progress bar line

    # --- Excel Report Generation ---
    date_str = datetime.today().strftime('%Y-%m-%d')
    report_file = f"shortdesc-validation-report-{date_str}.xlsx"
    
    files_with_abstract = total_files - results["no_abstract"]
    def pct_str(count):
        return f"{(count * 100 // files_with_abstract)}%" if files_with_abstract > 0 else "0%"

    summary_data = [
        {"Metric": "Files checked", "Count": total_files, "% of files with abstract": "—"},
        {"Metric": "No [role=\"_abstract\"] (skipped)", "Count": results["no_abstract"], "% of files with abstract": "—"},
        {"Metric": "Files with abstract", "Count": files_with_abstract, "% of files with abstract": "100%"},
        {"Metric": "OK (50–300 chars)", "Count": results["ok"], "% of files with abstract": pct_str(results["ok"])},
        {"Metric": "Too short (<50 chars)", "Count": len(results["too_short"]), "% of files with abstract": pct_str(len(results["too_short"]))},
        {"Metric": "Too long (>300 chars)", "Count": len(results["too_long"]), "% of files with abstract": pct_str(len(results["too_long"]))},
        {"Metric": "Contains conditionals", "Count": results["cond_count"], "% of files with abstract": "—"},
        {"Metric": "Ends with colon", "Count": len(results["colon"]), "% of files with abstract": "—"},
        {"Metric": "Self-referential / introductory", "Count": len(results["self_ref"]), "% of files with abstract": "—"}
    ]

    # Create DataFrames
    df_summary = pd.DataFrame(summary_data)
    df_short = pd.DataFrame(results["too_short"]).sort_values(by="Length", ascending=True) if results["too_short"] else pd.DataFrame(columns=["Length", "File"])
    df_long = pd.DataFrame(results["too_long"]).sort_values(by="Length", ascending=False) if results["too_long"] else pd.DataFrame(columns=["Length", "File"])
    df_cond = pd.DataFrame(results["conditionals"]) if results["conditionals"] else pd.DataFrame(columns=["File", "Note"])
    df_colon = pd.DataFrame(results["colon"]) if results["colon"] else pd.DataFrame(columns=["File", "Abstract (first 120 chars)"])
    df_selfref = pd.DataFrame(results["self_ref"]) if results["self_ref"] else pd.DataFrame(columns=["File", "Abstract (first 120 chars)"])

    # Write to Excel
    print("Generating Excel report...")
    with pd.ExcelWriter(report_file, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        if not df_short.empty: df_short.to_excel(writer, sheet_name='Too Short', index=False)
        if not df_long.empty: df_long.to_excel(writer, sheet_name='Too Long', index=False)
        if not df_cond.empty: df_cond.to_excel(writer, sheet_name='Conditionals', index=False)
        if not df_colon.empty: df_colon.to_excel(writer, sheet_name='Ends with Colon', index=False)
        if not df_selfref.empty: df_selfref.to_excel(writer, sheet_name='Self-Referential', index=False)

    # Adjust column widths for better readability
    workbook = writer.book
    for sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min((max_length + 2), 80) # Cap width at 80
            worksheet.column_dimensions[column_letter].width = adjusted_width

    # Terminal summary
    print("\nResults:")
    print(f"  OK (50-300 chars) : {results['ok']}")
    print(f"  Too short (<50)   : {len(results['too_short'])}")
    print(f"  Too long  (>300)  : {len(results['too_long'])}")
    print(f"  Conditionals      : {results['cond_count']}")
    print(f"  Ends with colon   : {len(results['colon'])}")
    print(f"  Self-referential  : {len(results['self_ref'])}")
    print(f"  No abstract       : {results['no_abstract']}\n")
    print(f"Report exported to: {report_file}")

if __name__ == "__main__":
    main()
