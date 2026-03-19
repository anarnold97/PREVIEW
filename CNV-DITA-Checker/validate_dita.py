import subprocess
import os
import sys
from pathlib import Path

# --- Configuration ---
REPO_PATH = os.getcwd()  # Assumes you run this from the repo root
CONFIG_PATH = str(Path.home() / "dita.ini")
OUTPUT_FILE = "CNV-DITA-report.csv"
VALE_WORKERS = 8

def run_command(cmd, shell=False):
    """Utility to run shell commands and exit on failure."""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        print(f"Output: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Starting DITA Validation Workflow...")

    # 1. Sync Vale Config
    print("🔄 Syncing Vale configuration...")
    run_command(["vale", "--config", CONFIG_PATH, "sync"])

    # 2. Git Lifecycle
    print("🌿 Updating repository...")
    run_command(["git", "checkout", "main"])
    run_command(["git", "fetch", "upstream"])
    run_command(["git", "rebase", "upstream/main"])
    run_command(["git", "push", "origin", "main"])

    # 3. Find files and run Vale
    # We use a shell string here to maintain your specific find/xargs logic
    print(f"🔍 Running Vale validation on {VALE_WORKERS} cores...")
    
    # Constructing the command to pipe find into xargs
    find_cmd = f"find virt/ modules/virt-*.adoc -type f | xargs -n 1 -P {VALE_WORKERS} vale --config {CONFIG_PATH} --output line"
    
    try:
        # We catch the output directly to write to our specific CSV name
        report_data = subprocess.check_output(find_cmd, shell=True, text=True)
        
        with open(OUTPUT_FILE, "w") as f:
            f.write(report_data)
        
        print(f"✅ Validation complete. Report saved to: {OUTPUT_FILE}")
    
    except subprocess.CalledProcessError as e:
        # Vale returns non-zero exit codes if it finds alerts. 
        # We still want to save the output even if alerts were found.
        with open(OUTPUT_FILE, "w") as f:
            f.write(e.output)
        print(f"⚠️ Vale found issues (this is normal). Report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()