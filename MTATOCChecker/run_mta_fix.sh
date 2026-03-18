#!/bin/bash

# Configuration
PYTHON_SCRIPT="fix_toc_by_new_modules.py"
REPORT_FILE="mta_toc_report.txt"
COMMIT_MSG_FILE="git_commit_msg.txt"
PR_TEMPLATE_FILE="PULL_REQUEST.md"

# Function to revert changes
cleanup_changes() {
    echo "--- Reverting all automated changes ---"
    git restore --staged documentation/modules/*.adoc 2>/dev/null
    git restore --staged documentation/doc-*/master.adoc 2>/dev/null
    git restore --staged documentation/doc-*/index.adoc 2>/dev/null
    git restore documentation/modules/*.adoc 2>/dev/null
    git restore documentation/doc-*/master.adoc 2>/dev/null
    git restore documentation/doc-*/index.adoc 2>/dev/null
    find documentation/modules/ -name "*-toc-sections.adoc" -delete
    rm -f "$COMMIT_MSG_FILE" "$REPORT_FILE" "$PR_TEMPLATE_FILE"
    echo "Cleanup complete."
}

if [[ "$1" == "--cleanup" || "$1" == "-c" ]]; then
    cleanup_changes
    exit 0
fi

if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Error: $PYTHON_SCRIPT not found."
    exit 1
fi

echo "--- Starting MTA TOC Fixer ---"
python3 "$PYTHON_SCRIPT" | tee "$REPORT_FILE"

if grep -q "No modules found" "$REPORT_FILE"; then
    echo "No changes necessary."
    rm -f "$REPORT_FILE"
    exit 0
fi

# 1. Generate Git Commit Message
{
    echo "docs: refactor modules to fix TOC depth"
    echo ""
    echo "Automated TOC depth correction for MTA documentation."
    echo "The following headings were moved to new modules to stay within Level 3:"
    grep "\[MOVE\] Heading:" "$REPORT_FILE" | sed "s/\[MOVE\] Heading: /- /"
    echo ""
    echo "Summary:"
    grep "Total Modules Split:" "$REPORT_FILE"
    grep "Total Files Modified:" "$REPORT_FILE"
} > "$COMMIT_MSG_FILE"

# 2. Generate GitHub Pull Request Template
{
    echo "## 📝 Description"
    echo "This PR addresses Table of Contents (TOC) depth issues where headings were reaching Level 4 or deeper, making them invisible in the Red Hat Customer Portal sidebar. Content has been refactored into sub-modules to maintain a maximum TOC depth of 3."
    echo ""
    echo "### 🛠 Automated Changes"
    echo "| Moved Heading | Source Module | New Target Module |"
    echo "| :--- | :--- | :--- |"
    # Parse the report into a Markdown table
    awk '/\[MOVE\] Heading:/ {heading=$3} /FROM:/ {from=$2} /TO:/ {to=$2; printf("| %s | `%s` | `%s` |\n", heading, from, to)}' "$REPORT_FILE"
    echo ""
    echo "### 📊 Impact Summary"
    grep "Total Modules Split:" "$REPORT_FILE" | sed 's/^/- **/' | sed 's/$/ **/'
    grep "Total Files Modified:" "$REPORT_FILE" | sed 's/^/- **/' | sed 's/$/ **/'
    echo ""
    echo "### ✅ Reviewer Checklist"
    echo "- [ ] Verified that the new sub-modules are correctly included in the assembly files."
    echo "- [ ] Confirmed that the build (Asciidoctor/Pantheon) completes without errors."
    echo "- [ ] Checked for any internal cross-references that may need updating."
} > "$PR_TEMPLATE_FILE"

# 3. Git Staging
git add documentation/modules/*.adoc
git add documentation/doc-*/master.adoc
git add documentation/doc-*/index.adoc

echo "--------------------------------------------------------"
echo "COMPLETED: Changes staged and PR Template generated."
echo "FILE CREATED: $PR_TEMPLATE_FILE"
echo "--------------------------------------------------------"

while true; do
    read -p "Did the build pass? Commit (y), Rollback/Cleanup (c), or Exit (n): " choice
    case $choice in
        [yY]* )
            git commit -F "$COMMIT_MSG_FILE"
            rm -f "$REPORT_FILE"
            echo "Done! Copy the contents of $PR_TEMPLATE_FILE for your Pull Request."
            break
            ;;
        [cC]* )
            cleanup_changes
            break
            ;;
        [nN]* )
            rm -f "$REPORT_FILE"
            break
            ;;
        * ) echo "Please answer y, c, or n.";;
    esac
done