#!/bin/bash

# 1. Define the Guide folders (Assemblies)
MTA_GUIDES=(
    "docs/cli-guide"
    "docs/developer-lightspeed-guide"
    "docs/install-guide"
    "docs/intellij-idea-plugin-guide"
    "docs/release-notes"
    "docs/rules-development-guide"
    "docs/vs-code-extension-guide"
    "docs/web-console-guide"
)

# 2. Define the Topic subdirectories (Modules)
MTA_TOPIC_SUBS=(
    "docs/topics/mta-cli"
    "docs/topics/mta-install"
    "docs/topics/mta-intellij-plugin"
    "docs/topics/mta-ui"
    "docs/topics/release-notes-topics"
    "docs/topics/rules-development"
)

echo "--- MTA Documentation File Count ---"

# Count Assemblies
TOTAL_ASSEMBLIES=0
echo "Scanning Assembly Guides..."
for guide in "${MTA_GUIDES[@]}"; do
    if [ -d "$guide" ]; then
        # Count all .adoc files in these specific guide folders
        count=$(find "$guide" -name "*.adoc" | wc -l)
        TOTAL_ASSEMBLIES=$((TOTAL_ASSEMBLIES + count))
        printf "  %-35s : %d\n" "$guide" "$count"
    fi
done

echo "------------------------------------"

# Count Modules (Topics)
TOTAL_TOPICS=0
echo "Scanning Topic Subdirectories..."
for topic_dir in "${MTA_TOPIC_SUBS[@]}"; do
    if [ -d "$topic_dir" ]; then
        # Count all .adoc files recursively within these topic subfolders
        count=$(find "$topic_dir" -name "*.adoc" | wc -l)
        TOTAL_TOPICS=$((TOTAL_TOPICS + count))
        printf "  %-35s : %d\n" "$topic_dir" "$count"
    fi
done

echo "------------------------------------"
echo "TOTAL ASSEMBLIES: $TOTAL_ASSEMBLIES"
echo "TOTAL MODULES (TOPICS): $TOTAL_TOPICS"
echo "------------------------------------"
