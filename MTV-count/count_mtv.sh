#!/bin/bash

# Define the base documentation path
DOC_BASE="documentation"
MODULES_DIR="$DOC_BASE/modules"

# Define the high-level guide folders
MTV_GUIDES=(
    "doc-Migrating_your_virtual_machines"
    "doc-Planning_your_migration"
    "doc-Release_notes"
)

if [ ! -d "$DOC_BASE" ]; then
    echo "Error: Directory '$DOC_BASE' not found. Please run from the repo root."
    exit 1
fi

echo "--- MTV (Forklift) Documentation Audit ---"

# 1. Count Assemblies
# We look for .adoc files in the main guide folders AND their /assemblies subfolders
TOTAL_ASSEMBLIES=0
echo "Scanning Assemblies..."

for guide in "${MTV_GUIDES[@]}"; do
    GUIDE_PATH="$DOC_BASE/$guide"
    if [ -d "$GUIDE_PATH" ]; then
        # Count .adoc files in the guide root and the assemblies/ sub-directory
        # We filter for the ASSEMBLY attribute to be precise
        count=$(grep -rl ":_mod-docs-content-type: ASSEMBLY" "$GUIDE_PATH" --include="*.adoc" 2>/dev/null | wc -l)
        TOTAL_ASSEMBLIES=$((TOTAL_ASSEMBLIES + count))
        printf "  %-40s : %d\n" "$guide" "$count"
    fi
done

echo "------------------------------------------"

# 2. Count Modules (Topics)
# All modules are located in documentation/modules
echo "Scanning Modules..."
if [ -d "$MODULES_DIR" ]; then
    # Count all .adoc files recursively within the modules directory
    TOTAL_MODULES=$(find "$MODULES_DIR" -name "*.adoc" | wc -l)
    
    # Optional: Breakdown by sub-folder in modules
    find "$MODULES_DIR" -maxdepth 1 -type d | while read -r sub; do
        if [ "$sub" != "$MODULES_DIR" ]; then
            sub_count=$(find "$sub" -name "*.adoc" | wc -l)
            printf "  - %-37s : %d\n" "${sub#$MODULES_DIR/}" "$sub_count"
        fi
    done
else
    TOTAL_MODULES=0
    echo "  [!] Modules directory not found."
fi

echo "------------------------------------------"
echo "TOTAL ASSEMBLIES: $TOTAL_ASSEMBLIES"
echo "TOTAL MODULES:    $TOTAL_MODULES"
echo "------------------------------------------"
