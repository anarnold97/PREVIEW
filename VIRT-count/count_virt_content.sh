#!/bin/bash

# Define the base Virt path and the root modules directory
VIRT_BASE_DIR="virt"
MODULES_ROOT="modules"

# Check if we are in the root of the openshift-docs repo
if [ ! -d "$VIRT_BASE_DIR" ] || [ ! -d "$MODULES_ROOT" ]; then
    echo "Error: Directory structure not found."
    echo "Please run this script from the root of the 'openshift-docs' repository."
    exit 1
fi

echo "--- Analyzing OpenShift Virtualization (Virt) Documentation ---"

# 1. Count Assemblies 
# Finds all .adoc files in 'virt/' and subfolders containing the ASSEMBLY attribute
ASSEMBLY_LIST=$(grep -rl ":_mod-docs-content-type: ASSEMBLY" "$VIRT_BASE_DIR" --include="*.adoc")
ASSEMBLY_COUNT=$(echo "$ASSEMBLY_LIST" | grep -v '^$' | wc -l)

# 2. Identify Unique Modules referenced
# Searches for 'include::modules/' in all Virt adoc files.
# Extracts the filename, sorts them, and removes duplicates.
MODULE_LIST=$(grep -rh "include::modules/" "$VIRT_BASE_DIR" --include="*.adoc" | \
               sed -E 's/.*include::modules\/([^\[ ]+).*/\1/' | \
               sort -u | \
               grep -v '^$')

MODULE_COUNT=$(echo "$MODULE_LIST" | wc -l)

# 3. Output Results
echo "Total Assemblies found: $ASSEMBLY_COUNT"
echo "Unique Modules used:    $MODULE_COUNT"
echo "--------------------------------------------------------"

# Optional: Display a count per sub-directory to see the distribution
echo "Assembly count by category:"
find "$VIRT_BASE_DIR" -maxdepth 1 -type d | while read -r dir; do
    if [ "$dir" != "$VIRT_BASE_DIR" ]; then
        count=$(grep -rl ":_mod-docs-content-type: ASSEMBLY" "$dir" --include="*.adoc" 2>/dev/null | wc -l)
        printf "  %-35s : %d\n" "${dir#$VIRT_BASE_DIR/}" "$count"
    fi
done
