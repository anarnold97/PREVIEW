#!/bin/bash

# setup_migration.sh
# Automates the OADP JTBD Restructure Plan.


# Base directory for OADP documentation as defined in the plan
BASE_DIR="backup_and_restore/application_backup_and_restore"

# Check if we are in the correct root directory
if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Directory $BASE_DIR not found."
    echo "Please run this script from the root of the documentation repository."
    exit 1
fi

echo "--- Starting Phase 2: Create New Directory Structure ---"

# Navigate to base directory to create internal structure
cd "$BASE_DIR" || exit

# Task 2.1: Create new directories
echo "Creating new directories..."
mkdir -p getting-started
mkdir -p installing/backup-storage
mkdir -p installing/volume-snapshots
mkdir -p migrating
mkdir -p platforms/rosa
mkdir -p platforms/aws-sts
mkdir -p platforms/virtualization
mkdir -p reference
# Ensure backing_up_and_restoring exists target
mkdir -p backing_up_and_restoring

# Task 2.2: Create symlinks in new directories
echo "Creating symlinks in new top-level directories..."
# List of top-level new directories requiring standard symlinks
DIRS=("getting-started" "migrating" "platforms/rosa" "platforms/aws-sts" "platforms/virtualization" "reference")

for dir in "${DIRS[@]}"; do
    echo "  Linking resources in $dir..."
    # pushd/popd ensures we return to base for the next iteration
    pushd "$dir" > /dev/null
    ln -sf ../images images
    ln -sf ../modules modules
    ln -sf ../snippets snippets
    ln -sf ../_attributes _attributes
    popd > /dev/null
done

# Special handling for nested directory 
echo "Creating symlinks in nested installing/backup-storage..."
pushd installing/backup-storage > /dev/null
ln -sf ../../images images
ln -sf ../../modules modules
ln -sf ../../snippets snippets
ln -sf ../../_attributes _attributes
popd > /dev/null

# Special handling for nested directory
echo "Creating symlinks in nested installing/volume-snapshots..."
pushd installing/volume-snapshots > /dev/null
ln -sf ../../images images
ln -sf ../../modules modules
ln -sf ../../snippets snippets
ln -sf ../../_attributes _attributes
popd > /dev/null

echo "--- Phase 2 Complete ---"
echo ""
echo "--- Starting Phase 4: Move and Reorganize Files ---"

# Helper function to move files using git mv to preserve history
move_file() {
    local src="$1"
    local dest="$2"
    
    if [ -f "$src" ]; then
        echo "Moving $src -> $dest"
        # Temporarily go back to repo root to run git mv command
        cd ../.. 
        git mv "$BASE_DIR/$src" "$BASE_DIR/$dest"
        # Return to BASE_DIR for next operation
        cd "$BASE_DIR" || exit
    else
        echo "Warning: Source file $src not found. Skipping."
    fi
}

# Task 4.1: Move introduction files to getting-started
move_file "oadp-intro.adoc" "getting-started/"
move_file "oadp-features-plugins.adoc" "getting-started/"

# Task 4.2: Move reference files to reference
move_file "oadp-api.adoc" "reference/oadp-api.adoc"
move_file "troubleshooting/velero-cli-tool.adoc" "reference/velero-cli-tool.adoc"

# Moving specific release notes files listed in the plan
move_file "release-notes/oadp-1-5-release-notes.adoc" "reference/oadp-1-5-release-notes.adoc"
move_file "release-notes/oadp-upgrade-notes-1-5.adoc" "reference/oadp-upgrade-notes-1-5.adoc"

# Task 4.3: Move platform-specific files 
move_file "oadp-rosa/oadp-rosa-backing-up-applications.adoc" "platforms/rosa/oadp-rosa-backing-up-applications.adoc"
move_file "oadp-use-cases/oadp-rosa-backup-restore.adoc" "platforms/rosa/oadp-rosa-backup-restore.adoc"
move_file "aws-sts/oadp-aws-sts.adoc" "platforms/aws-sts/oadp-aws-sts.adoc"
move_file "installing/installing-oadp-kubevirt.adoc" "platforms/virtualization/installing-oadp-kubevirt.adoc"

# Task 4.4: Move use case file to backing_up_and_restoring/ 
# Note: Renaming from 'oadp-usecase-restore-different-namespace.adoc' to 'oadp-restore-different-namespace.adoc'
move_file "oadp-use-cases/oadp-usecase-restore-different-namespace.adoc" "backing_up_and_restoring/oadp-restore-different-namespace.adoc"

echo "--- Phase 4 Complete ---"
echo "Structure created and files moved. Please verify with 'git status'."