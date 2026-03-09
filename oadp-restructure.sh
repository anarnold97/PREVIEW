#!/bin/bash
#
# oadp-restructure.sh
# Automates the OADP JTBD (Jobs-to-be-Done) restructure for application_backup_and_restore.
#
# PURPOSE
#   Creates the new JTBD directory layout and moves/renames assemblies so the OADP docs
#   align with the structure defined in the OADP JTBD plan (see References below).
#   Uses "git mv" so file history is preserved.
#
# USAGE
#   Run from the root of the openshift-docs repository (the directory that contains
#   backup_and_restore/). Do not run from backup_and_restore/ or application_backup_and_restore/.
#
#   ./scripts/oadp-restructure.sh
#
# PREREQUISITES
#   - Git working tree clean or with only intended changes (recommended: run on a branch).
#   - You have write access to the repo; script runs "git mv" and modifies the tree.
#
# SYMLINK NOTE (openshift-docs layout)
#   This script assumes images, modules, snippets, and _attributes live inside
#   application_backup_and_restore (so symlinks use ../ or ../../). If in your repo
#   they live at repository root, symlink targets may need to be ../../../modules etc.
#   from application_backup_and_restore/getting-started/. Adjust the ln -sf targets
#   in "Task 2.2" and the "Special handling" blocks if your layout differs.
#
# REFERENCES
#   - OADP JTBD structure (authoritative): see docs/OADP-JTBD-Automation-Strategy-Report.md
#   - PREVIEW source: https://github.com/anarnold97/PREVIEW/blob/main/oadp-restructure.sh
#   - Issue: 750884295_49516a534bc44e9daeb9c96dbd50f2d9-090326-1412-6482
#

# Base directory for OADP documentation (relative to repo root).
# All created dirs and moves are under this path.
BASE_DIR="backup_and_restore/application_backup_and_restore"

# Ensure we are in the repository root that contains application_backup_and_restore.
if [ ! -d "$BASE_DIR" ]; then
  echo "Error: Directory $BASE_DIR not found."
  echo "Please run this script from the root of the documentation repository."
  exit 1
fi

echo "--- Starting Phase 2: Create New Directory Structure ---"

# Change into OADP base so relative paths for mkdir/ln/pushd are correct.
cd "$BASE_DIR" || exit

# -----------------------------------------------------------------------------
# Task 2.1: Create new JTBD directories
# These match the planned IA: getting-started, installing subdirs, platforms, etc.
# backing_up_and_restoring is kept; we only add new siblings and subdirs.
# -----------------------------------------------------------------------------
echo "Creating new directories..."
mkdir -p getting-started
mkdir -p installing/backup-storage
mkdir -p installing/volume-snapshots
mkdir -p migrating
mkdir -p platforms/rosa
mkdir -p platforms/aws-sts
mkdir -p platforms/virtualization
mkdir -p reference
mkdir -p backing_up_and_restoring

# -----------------------------------------------------------------------------
# Task 2.2: Symlinks in top-level new directories
# AsciiDoc includes (e.g. include::modules/..., include::_attributes/...) resolve
# relative to the assembly. New dirs are one level down, so we link ../images,
# ../modules, ../snippets, ../_attributes so that existing include paths still work.
# -----------------------------------------------------------------------------
echo "Creating symlinks in new top-level directories..."
DIRS=("getting-started" "migrating" "platforms/rosa" "platforms/aws-sts" "platforms/virtualization" "reference")

for dir in "${DIRS[@]}"; do
  echo "  Linking resources in $dir..."
  pushd "$dir" > /dev/null
  ln -sf ../images images
  ln -sf ../modules modules
  ln -sf ../snippets snippets
  ln -sf ../_attributes _attributes
  popd > /dev/null
done

# Symlinks for installing/backup-storage (two levels under application_backup_and_restore).
echo "Creating symlinks in nested installing/backup-storage..."
pushd installing/backup-storage > /dev/null
ln -sf ../../images images
ln -sf ../../modules modules
ln -sf ../../snippets snippets
ln -sf ../../_attributes _attributes
popd > /dev/null

# Symlinks for installing/volume-snapshots (same depth as backup-storage).
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

# -----------------------------------------------------------------------------
# move_file src dest
# Moves a file with "git mv" so history is preserved. Paths are relative to
# application_backup_and_restore (BASE_DIR). dest can be a directory (trailing /)
# or a full path including new filename (for renames).
# -----------------------------------------------------------------------------
move_file() {
  local src="$1"
  local dest="$2"

  if [ -f "$src" ]; then
    echo "Moving $src -> $dest"
    cd ../.. || exit
    git mv "$BASE_DIR/$src" "$BASE_DIR/$dest"
    cd "$BASE_DIR" || exit
  else
    echo "Warning: Source file $src not found. Skipping."
  fi
}

# Task 4.1: Get-started assemblies (intro and features/plugins).
move_file "oadp-intro.adoc" "getting-started/"
move_file "oadp-features-plugins.adoc" "getting-started/"

# Task 4.2: Reference content (API, Velero CLI, release notes).
move_file "oadp-api.adoc" "reference/oadp-api.adoc"
move_file "troubleshooting/velero-cli-tool.adoc" "reference/velero-cli-tool.adoc"
move_file "release-notes/oadp-1-5-release-notes.adoc" "reference/oadp-1-5-release-notes.adoc"
move_file "release-notes/oadp-upgrade-notes-1-5.adoc" "reference/oadp-upgrade-notes-1-5.adoc"

# Task 4.3: Platform-specific docs (ROSA, AWS STS, OpenShift Virtualization).
move_file "oadp-rosa/oadp-rosa-backing-up-applications.adoc" "platforms/rosa/oadp-rosa-backing-up-applications.adoc"
move_file "oadp-use-cases/oadp-rosa-backup-restore.adoc" "platforms/rosa/oadp-rosa-backup-restore.adoc"
move_file "aws-sts/oadp-aws-sts.adoc" "platforms/aws-sts/oadp-aws-sts.adoc"
move_file "installing/installing-oadp-kubevirt.adoc" "platforms/virtualization/installing-oadp-kubevirt.adoc"

# Task 4.4: Use case moved into backing_up_and_restoring and renamed (shorter filename).
move_file "oadp-use-cases/oadp-usecase-restore-different-namespace.adoc" "backing_up_and_restoring/oadp-restore-different-namespace.adoc"

echo "--- Phase 4 Complete ---"
echo "Structure created and files moved. Please verify with 'git status'."
