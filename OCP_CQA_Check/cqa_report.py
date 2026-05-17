#!/usr/bin/env python3
"""
CQA Full Directory Assessment & Readability Tool (cqa_report.py)

This script runs a complete CQA validation on a specific directory within 
OpenShift Virt or OADP, resolves included modules, runs Vale, and 
calculates the Flesch-Kincaid reading age of the content.
"""

import subprocess
import json
import sys
import os
import re

# Try importing textstat for reading age, provide a friendly error if missing
try:
    import textstat
except ImportError:
    print("\033[91mError: The 'textstat' library is missing.\033[0m")
    print("Please install it by running: \033[96mpip install textstat\033[0m")
    sys.exit(1)

# ==========================================
# Terminal Formatting Constants
# ==========================================
RED = '\033[91m'      
YELLOW = '\033[93m'   
GREEN = '\033[92m'    
CYAN = '\033[96m'     
BOLD = '\033[1m'      
RESET = '\033[0m'     

# ==========================================
# Repository Paths
# ==========================================
DIR_VIRT = "virt/"
DIR_OADP = "backup_and_restore/application_backup_and_restore/"
DIR_MODULES = "modules/"

INCLUDE_RE = re.compile(r'include::(.*?\.adoc)')

def prompt_user_selection():
    print(f"\n{BOLD}=== OpenShift CQA Directory Assessment ==={RESET}")
    print("Which documentation set would you like to assess?")
    print(f"  {CYAN}1.{RESET} Virt (/virt)")
    print(f"  {CYAN}2.{RESET} OADP (/backup_and_restore/application_backup_and_restore)")
    
    # 1. Ask for the top-level doc set
    while True:
        choice = input(f"\nEnter {CYAN}1{RESET} or {CYAN}2{RESET}: ").strip()
        if choice == '1':
            base_dir = DIR_VIRT
            doc_name = "Virt"
            break
        elif choice == '2':
            base_dir = DIR_OADP
            doc_name = "OADP"
            break
        else:
            print(f"{RED}Invalid choice. Please enter 1 or 2.{RESET}")

    # 2. Ask for the specific subdirectory
    print(f"\n{CYAN}Enter a specific subdirectory to scan within {doc_name}.{RESET}")
    print(f"For example, type '{BOLD}install{RESET}' to scan {base_dir}install")
    print(f"Or just press {BOLD}Enter{RESET} to scan ALL of {doc_name}.")
    
    sub_dir = input(f"\nSubdirectory path: ").strip()

    if sub_dir:
        # Strip leading slashes to prevent os.path.join from treating it as an absolute path
        sub_dir = sub_dir.lstrip('/')
        target_path = os.path.join(base_dir, sub_dir)
    else:
        target_path = base_dir

    # Normalize the path to make it look clean (removes trailing slashes)
    target_path = os.path.normpath(target_path)
    
    print(f"\n{GREEN}Target directory set to: {BOLD}{target_path}{RESET}")
    return target_path, doc_name

def find_assembly_files(target_dir):
    assemblies = []
    if not os.path.exists(target_dir):
        print(f"{RED}Error: Directory '{target_dir}' does not exist.{RESET}")
        sys.exit(1)

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".adoc"):
                assemblies.append(os.path.join(root, file))
    return assemblies

def get_included_modules(assembly_files):
    included_modules = set()
    for assembly in assembly_files:
        try:
            with open(assembly, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = INCLUDE_RE.findall(content)
                for match in matches:
                    filename = os.path.basename(match.replace('{modulesdir}/', ''))
                    module_path = os.path.join(DIR_MODULES, filename)
                    if os.path.exists(module_path):
                        included_modules.add(module_path)
                    else:
                        rel_path = os.path.normpath(os.path.join(os.path.dirname(assembly), match))
                        if os.path.exists(rel_path):
                            included_modules.add(rel_path)
        except Exception as e:
            print(f"{YELLOW}Warning: Could not read {assembly} ({e}){RESET}")
    return list(included_modules)

def clean_asciidoc_for_readability(text):
    """
    Strips code blocks, URLs, and attributes from AsciiDoc text so they 
    don't artificially inflate the reading age calculation.
    """
    # Remove AsciiDoc code blocks (---- to ----)
    text = re.sub(r'----.*?----', '', text, flags=re.DOTALL)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    # Remove AsciiDoc attributes like {product-title}
    text = re.sub(r'\{[^\}]+\}', '', text)
    # Remove include statements
    text = re.sub(r'include::.*?\[.*?\]', '', text)
    return text

def assess_readability(files):
    """
    Calculates the Flesch-Kincaid Grade Level for each file.
    Flags files that require a high school senior or college reading level (>12).
    """
    high_complexity_files = []
    total_score = 0
    valid_files = 0

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                
            clean_text = clean_asciidoc_for_readability(raw_text)
            
            # Skip empty files or files that were mostly code blocks
            if len(clean_text.strip()) < 50:
                continue
                
            grade_level = textstat.flesch_kincaid_grade(clean_text)
            
            total_score += grade_level
            valid_files += 1
            
            # Standard tech writing goal is Grade 8-10. We flag anything > 12 (College level).
            if grade_level > 12:
                high_complexity_files.append((filepath, grade_level))
                
        except Exception:
            continue

    avg_grade = (total_score / valid_files) if valid_files > 0 else 0
    # Sort the hardest to read files to the top
    high_complexity_files.sort(key=lambda x: x[1], reverse=True)
    
    return avg_grade, high_complexity_files

def run_vale(files):
    if not files:
        return {}
    if not os.path.exists("vale-cqa.ini"):
        print(f"{RED}Error: 'vale-cqa.ini' not found in the current directory.{RESET}")
        sys.exit(1)
        
    print(f"{CYAN}Running Vale & Readability assessments... (This may take a minute){RESET}")
    cmd = ["vale", "--config=vale-cqa.ini", "--output=JSON"] + files
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return json.loads(result.stdout)
    except FileNotFoundError:
        print(f"{RED}Error: Vale is not installed or not in your system PATH.{RESET}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{RED}Error: Failed to parse Vale output.{RESET}")
        return {}

def print_full_cqa_report(vale_results, avg_grade, high_complexity_files, total_assemblies, total_modules):
    required_blockers = []     
    important_warnings = []    
    
    for filepath, violations in vale_results.items():
        for v in violations:
            rule = v.get("Check", "Unknown")
            message = v.get("Message", "")
            line = v.get("Line", 0)
            severity = v.get("Severity", "")
            match_text = v.get("Match", "")

            if match_text:
                issue = f"  {CYAN}{filepath}:{line}{RESET} [{rule}] {message} -> {BOLD}'{match_text}'{RESET}"
            else:
                issue = f"  {CYAN}{filepath}:{line}{RESET} [{rule}] {message}"

            if "AsciiDocDITA" in rule or severity == "error":
                required_blockers.append(issue)
            elif "RedHat" in rule or severity in ["warning", "suggestion"]:
                important_warnings.append(issue)

    print(f"\n{BOLD}=== 📝 FULL CQA DIRECTORY REPORT ==={RESET}")
    print(f"Scanned {total_assemblies} Assemblies and {total_modules} Included Modules.\n")
    
    # --- Section 1: Migration Blockers ---
    print(f"{BOLD}{RED}🛑 REQUIRED / NON-NEGOTIABLE (Migration Blockers){RESET}")
    if required_blockers:
        for blocker in required_blockers:
            print(blocker)
        print(f"\n{RED}Total Blockers: {len(required_blockers)}{RESET}")
    else:
        print(f"  {GREEN}✅ None found!{RESET}")
    print("\n" + "-"*80 + "\n")

    # --- Section 2: Style & Quality ---
    print(f"{BOLD}{YELLOW}⚠️  IMPORTANT / NEGOTIABLE (Style & Quality){RESET}")
    if important_warnings:
        for warning in important_warnings:
            print(warning)
        print(f"\n{YELLOW}Total Style Warnings: {len(important_warnings)}{RESET}")
    else:
        print(f"  {GREEN}✅ None found!{RESET}")
    print("\n" + "-"*80 + "\n")

    # --- Section 3: Readability ---
    print(f"{BOLD}{CYAN}📖 READABILITY & COMPLEXITY (Flesch-Kincaid Grade Level){RESET}")
    
    # Color-code the average score
    if avg_grade <= 10:
        grade_color = GREEN
    elif avg_grade <= 12:
        grade_color = YELLOW
    else:
        grade_color = RED
        
    print(f"Average Reading Grade Level: {BOLD}{grade_color}{avg_grade:.1f}{RESET} (Target: 8.0 - 10.0)")
    
    if high_complexity_files:
        print(f"\n{YELLOW}The following files exceed a Grade 12 reading level and may be too complex:{RESET}")
        for filepath, grade in high_complexity_files:
            print(f"  {CYAN}{filepath}{RESET} -> {RED}Grade {grade:.1f}{RESET}")
    else:
        print(f"\n  {GREEN}✅ All files are written at an accessible reading level!{RESET}")
        
    print("\n" + "="*80 + "\n")
    return len(required_blockers) == 0

if __name__ == "__main__":
    target_path, name = prompt_user_selection()
    
    print(f"\n{CYAN}Scanning {target_path} for assembly files...{RESET}")
    assemblies = find_assembly_files(target_path)
    
    if not assemblies:
        print(f"{YELLOW}No .adoc files found in {target_path}.{RESET}")
        sys.exit(0)
    
    print(f"{CYAN}Parsing assemblies for included modules...{RESET}")
    modules = get_included_modules(assemblies)
    print(f"{GREEN}Found {len(assemblies)} assemblies and {len(modules)} included modules.{RESET}")
    
    # Combine assemblies and modules into one list for processing
    all_files_to_check = assemblies + modules
    
    # Run Vale
    vale_json = run_vale(all_files_to_check)
    
    # Run Readability Assessment
    avg_grade, hard_files = assess_readability(all_files_to_check)
    
    # Output Final Report
    passed = print_full_cqa_report(vale_json, avg_grade, hard_files, len(assemblies), len(modules))
    
    if not passed:
        sys.exit(1)
    else:
        sys.exit(0)