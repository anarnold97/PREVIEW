# AsciiDoc to DITA XML Converter

A lightweight Python script that converts AsciiDoc (`.adoc`) files into DITA-valid XML format. It prompts the user for the input file and output directory, automatically handles the file path formatting, and retains the root filename while swapping the extension.

## Features
- **Interactive Prompts**: Asks the user for input and output paths at runtime.
- **Path Resolution**: Safely handles file paths across different operating systems (Windows, macOS, Linux) using Python's native `pathlib`.
- **Smart Naming**: Automatically extracts the base name of your AsciiDoc file and applies the `.dita` or `.xml` extension for the output.
- **Customizable Engine**: Configured out-of-the-box to use Pandoc, but easily adaptable for Asciidoctor.

## Prerequisites

To use this script, you will need:
1. **Python 3.6 or higher**: Installed on your system.
2. **A Conversion Tool**: Since Python does not parse AsciiDoc natively, this script acts as a wrapper. You must have one of the following installed and added to your system's PATH:
   - [Pandoc](https://pandoc.org/installing.html) (Default in the script)
   - [Asciidoctor](https://asciidoctor.org/) (Requires modifying the script's command variable)

## Installation

1. Download the script file and save it as `adoc_to_dita.py`.
2. Ensure your chosen conversion tool (e.g., Pandoc) is installed and accessible from your command line.

## Usage

1. Open your terminal or command prompt.
2. Navigate to the directory containing `adoc_to_dita.py`.
3. Run the script:
   ```bash
   python adoc_to_dita.py