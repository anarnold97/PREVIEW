import subprocess
import concurrent.futures
from pathlib import Path

# Configuration
BASE_DIR = "backup_and_restore/application_backup_and_restore"
VALE_CONFIG = "dita.ini"
OUTPUT_CSV = "report.csv"
MAX_WORKERS = 8  # Replicates the -P 8 in xargs

def get_content_files(base_dir):
    """Finds all .adoc files and uses list-content to resolve included modules."""
    print(f"Finding .adoc files in {base_dir}...")
    adoc_files = list(Path(base_dir).rglob("*.adoc"))
    
    all_files = set()
    
    # Run list-content on each discovered file
    for file_path in adoc_files:
        try:
            # Call the ruby gem asciidoctor-list-content
            result = subprocess.run(
                ["list-content", str(file_path)], 
                capture_output=True, 
                text=True, 
                check=True
            )
            # Add output files to our set to ensure uniqueness (replicates sort -u)
            for line in result.stdout.splitlines():
                if line.strip():
                    all_files.add(line.strip())
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to list content for {file_path}. Is asciidoctor-list-content installed?")
            # Fallback to just analyzing the file itself if list-content fails
            all_files.add(str(file_path))
        except FileNotFoundError:
            print("Error: 'list-content' command not found. Please install asciidoctor-list-content.")
            exit(1)
            
    return all_files

def filter_files(file_list):
    """Filters out any files located in _attributes/ directories."""
    # Replicates grep -v _attributes/
    filtered = [f for f in file_list if "_attributes/" not in f]
    print(f"Total files to analyze after filtering out attributes: {len(filtered)}")
    return filtered

def run_vale(file_path):
    """Runs vale on a single file using the specified dita.ini configuration."""
    try:
        result = subprocess.run(
            ["vale", "--config", VALE_CONFIG, "--output", "line", file_path],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running vale on {file_path}: {str(e)}"

def main():
    # 1. Get all files and included modules
    all_files = get_content_files(BASE_DIR)
    
    # 2. Filter out attributes
    target_files = filter_files(all_files)
    
    if not target_files:
        print("No files found to process. Check your BASE_DIR path.")
        return

    # 3. Run Vale concurrently (8 workers)
    print(f"Running vale on {len(target_files)} files using {MAX_WORKERS} threads...")
    all_results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Map the run_vale function to all target files
        results = executor.map(run_vale, target_files)
        
        for res in results:
            if res:  # Only add if vale produced output (i.e., found issues)
                all_results.append(res)

    # 4. Write results to CSV
    print(f"Writing results to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, "w", encoding="utf-8") as csv_file:
        for line in all_results:
            # Some vale calls might return multiple lines
            for sub_line in line.splitlines():
                csv_file.write(sub_line + "\n")
                
    print("Done! Check report.csv for the results.")

if __name__ == "__main__":
    main()