#!/bin/bash

# Configuration
PYTHON_SCRIPT="fix_toc_by_new_modules.py"
REPORT_FILE="mta_toc_report.txt"
COMMIT_MSG_FILE="git_commit_msg.txt"

# 1. Check if the Python script exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "Error: $PYTHON_SCRIPT not found in the current directory."
    exit 1
fi

echo "--- Starting MTA TOC Fixer ---"

# 2. Run the Python script and capture output to both console and file
python3 "$PYTHON_SCRIPT" | tee "$REPORT_FILE"

# 3. Check if any changes were actually made
if grep -q "No modules found" "$REPORT_FILE"; then
    echo "No changes were necessary. Exiting."
    rm "$REPORT_FILE"
    exit 0
fi

# 4. Generate the Git Commit Message
echo "docs: refactor modules to fix TOC depth" > "$COMMIT_MSG_FILE"
echo "" >> "$COMMIT_MSG_FILE"
echo "Automated TOC depth correction for MTA documentation." >> "$COMMIT_MSG_FILE"
echo "The following headings were moved to new modules to stay within Level 3:" >> "$COMMIT_MSG_FILE"

# Extract the moved headings from the report and format them for the commit
grep "\[MOVE\] Heading:" "$REPORT_FILE" | sed "s/\[MOVE\] Heading: /- /" >> "$COMMIT_MSG_FILE"

echo "" >> "$COMMIT_MSG_FILE"
echo "Summary:" >> "$COMMIT_MSG_FILE"
grep "Total Modules Split:" "$REPORT_FILE" >> "$COMMIT_MSG_FILE"
grep "Total Files Modified:" "$REPORT_FILE" >> "$COMMIT_MSG_FILE"

# 5. Git Operations
echo "--- Staging changes in Git ---"
git add documentation/modules/*.adoc
git add documentation/doc-*/master.adoc
git add documentation/doc-*/index.adoc

echo "--- Commit Message Generated ---"
cat "$COMMIT_MSG_FILE"
echo "-------------------------------"

# 6. Prompt for commit
read -p "Do you want to commit these changes? (y/n): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    git commit -F "$COMMIT_MSG_FILE"
    echo "Changes committed successfully."
else
    echo "Changes staged but not committed. Commit message saved to $COMMIT_MSG_FILE."
fi

# Cleanup
rm "$REPORT_FILE"