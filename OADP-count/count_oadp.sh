#!/bin/bash

# Define the base OADP path and the root modules directory
OADP_BASE_DIR="backup_and_restore/application_backup_and_restore"
MODULES_ROOT="modules"

# Check if we are in the correct root directory
if [ ! -d "$OADP_BASE_DIR" ]; then
    echo "Error: Directory '$OADP_BASE_DIR' not found."
    echo "Please run this script from the root of the 'openshift-docs' repository."
    exit 1
fi

echo "--- Analyzing OADP Documentation Structure ---"

# 1. Count Assemblies 
# Searches all subdirectories for files containing the ASSEMBLY content-type attribute
ASSEMBLY_LIST=$(grep -rl ":_mod-docs-content-type: ASSEMBLY" "$OADP_BASE_DIR" --include="*.adoc")
ASSEMBLY_COUNT=$(echo "$ASSEMBLY_LIST" | grep -v '^$' | wc -l)

# 2. Identify Unique Modules referenced within those Assemblies
# We look for 'include::modules/' patterns recursively in all files within the OADP folder
# We then extract the filename and ensure we only count unique occurrences
MODULE_COUNT=$(grep -rh "include::modules/" "$OADP_BASE_DIR" --include="*.adoc" | \
               sed -E 's/.*include::modules\/([^\[ ]+).*/\1/' | \
               sort -u | \
               grep -v '^$' | \
               wc -l)

echo "Total Assemblies found: $ASSEMBLY_COUNT"
echo "Unique Modules used:    $MODULE_COUNT"
echo "--------------------------------------------"

# Optional: List top-level categories found
echo "Sub-directories scanned:"
ls -d "$OADP_BASE_DIR"/*/ | sed 's|.*/||' | column
