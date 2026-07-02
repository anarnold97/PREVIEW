import subprocess
from pathlib import Path

def convert_adoc_to_dita():
    print("=== AsciiDoc to DITA XML Converter ===\n")
    
    # 1. Ask the user for the input file path
    input_str = input("Enter the full path to the input .adoc file: ").strip()
    input_path = Path(input_str).resolve()

    # Validate the input file
    if not input_path.exists() or not input_path.is_file():
        print(f"\nError: Could not find file at '{input_path}'")
        return

    if input_path.suffix.lower() != '.adoc':
        print("\nWarning: The file doesn't have an .adoc extension. Proceeding anyway...")

    # 2. Ask the user for the export directory
    output_dir_str = input("Enter the export directory path (leave blank to use the input directory): ").strip()
    
    if output_dir_str:
        output_dir = Path(output_dir_str).resolve()
        # Create the directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent

    # 3. Construct the new file name
    # .stem extracts the root file name (e.g., 'document' from 'document.adoc')
    # You can change '.dita' to '.xml' below if you prefer a standard XML extension
    output_path = output_dir / f"{input_path.stem}.dita" 

    print(f"\n[Ready to Convert]")
    print(f"Source:      {input_path}")
    print(f"Destination: {output_path}\n")

    # 4. Define the conversion command
    # NOTE: Uncomment and modify the command that matches the tool you have installed.
    
    # --- Option A: Using Pandoc ---
    # Pandoc doesn't natively output strict DITA, but DocBook XML is very close.
    command = [
        "pandoc", 
        str(input_path), 
        "-f", "asciidoc", 
        "-t", "docbook", 
        "-o", str(output_path)
    ]
    
    # --- Option B: Using Asciidoctor (with dita-topic plugin) ---
    # command = [
    #     "asciidoctor", 
    #     "-r", "dita-topic", 
    #     "-b", "dita-topic", 
    #     str(input_path), 
    #     "-o", str(output_path)
    # ]

    # 5. Execute the conversion
    try:
        print("Running conversion...")
        subprocess.run(command, check=True)
        print(f"\nSuccess! DITA XML successfully exported to:\n{output_path}")
    except FileNotFoundError:
        print("\nError: Conversion tool not found.")
        print("Please ensure your chosen tool (Pandoc, Asciidoctor, etc.) is installed and added to your system PATH.")
    except subprocess.CalledProcessError as e:
        print(f"\nError during conversion: {e}")

if __name__ == "__main__":
    convert_adoc_to_dita()
