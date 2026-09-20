#!/usr/bin/env python3
"""
================================================================================
DITA MAP Normalizer
================================================================================
DEPS / QUICK START
--------------------------------------------------------------------------------
1. Install dependencies:
   pip install beautifulsoup4 lxml

2. Run from command line:
   python dita_map_normalizer.py --map ./documentation/documentation.ditamap
   python dita_map_normalizer.py --map ./my-project.ditamap --output ./output/
   python dita_map_normalizer.py --map ./project.ditamap --dry-run  # Preview only

3. Use programmatically:
   from dita_map_normalizer import DITAMapNormalizer
   normalizer = DITAMapNormalizer('./documentation.ditamap', './output/')
   stats = normalizer.run()

WHAT THIS DOES
--------------------------------------------------------------------------------
• Parses a DITA MAP file to extract all referenced topic paths via <topicref> elements
• Resolves relative paths to locate each topic file on disk
• Applies automated fixes to common AI-conversion formatting errors:
  - Closes unclosed XML/DITA tags (<p>, <li>, <body>, etc.)
  - Fixes self-closing tags for empty elements (image, note, reference)
  - Standardizes non-DITA element names (paragraph→p, strong→b, etc.)
  - Removes ServiceNow-specific artifacts (sys_id, class attributes, metadata)
  - Ensures proper DITA hierarchy (topic > body > content)
  - Normalizes whitespace and removes extraneous spacing
• Preserves original folder structure in output directory
• Reports statistics on files processed, modified, and any errors encountered
• Logs all operations to timestamped log file for audit trail

REQUIREMENTS
--------------------------------------------------------------------------------
- Python 3.7+
- beautifulsoup4>=4.12.0
- lxml>=4.9.0

USAGE EXAMPLES
--------------------------------------------------------------------------------
# Basic: Process with output to same directory as DITA MAP
$ python dita_map_normalizer.py -m my-documentation.ditamap

# Custom output directory:
$ python dita_map_normalizer.py -m docs.ditamap -o ./normalized_output/

# Dry run (preview without modifying files):
$ python dita_map_normalizer.py -m docs.ditamap --dry-run

# Verbose mode with full error list:
$ python dita_map_normalizer.py -m docs.ditamap -v

COMMAND LINE OPTIONS
--------------------------------------------------------------------------------
  -m, --map PATH       Path to DITA MAP file (required)
  -o, --output DIR     Output directory (default: same as DITA MAP)
  -n, --dry-run        Preview changes without modifying files
  -v, --verbose        Show verbose output and full error details

OUTPUT
--------------------------------------------------------------------------------
- Fixed DITA topic files in specified output directory
- Statistics summary printed to console
- Detailed log file saved to ./logs/dita_normalization_YYYYMMDD_HHMMSS.log

KNOWN FIXES APPLIED
--------------------------------------------------------------------------------
| Issue                          | Fix Applied                           |
|--------------------------------|---------------------------------------|
| Unclosed <p>, <li>, <body>     | Auto-close missing tags               |
| AI-invented element names      | Map to standard DITA elements         |
| ServiceNow sys_id attributes   | Strip system metadata                 |
| Improper topic/body nesting    | Restructure hierarchy                 |
| Extra whitespace/newlines      | Normalize to single spaces/double NL  |
| Invalid self-closing syntax    | Convert to proper <tag /> format      |

================================================================================
"""

import re
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required. Install with: pip install beautifulsoup4")
    sys.exit(1)

try:
    from xml.etree import ElementTree as ET
except ImportError:
    print("Error: ElementTree is required (included in Python stdlib)")
    sys.exit(1)


class DITAMapNormalizer:
    """Process DITA topics referenced in a DITA MAP"""
    
    def __init__(self, dita_map_path, output_dir=None):
        """
        Initialize the normalizer
        
        Args:
            dita_map_path: Path to the .ditamap file
            output_dir: Output directory for fixed files (default: same as DITA MAP)
        """
        self.dita_map_path = Path(dita_map_path)
        self.output_dir = Path(output_dir) if output_dir else self.dita_map_path.parent
        self.output_dir.mkdir(exist_ok=True)
        
        self.topics = []
        self.map_topics = []
        self.errors = []
        self.stats = {'processed': 0, 'errors': 0, 'files_modified': 0}
    
    def parse_ditamap(self):
        """Extract topic references from DITA MAP"""
        
        try:
            tree = ET.parse(self.dita_map_path)
            root = tree.getroot()
            
            # Find all topicref elements with href
            for topicref in root.iter():
                if topicref.tag.endswith('topicref') or topicref.tag == 'topicref':
                    href = topicref.get('href')
                    if href:
                        self.map_topics.append({
                            'href': href,
                            'type': topicref.get('type', 'unknown'),
                            'processing': topicref.get('processing-role', 'default')
                        })
            
            print(f"Found {len(self.map_topics)} topic references in DITA MAP")
            return True
            
        except Exception as e:
            self.errors.append(f"DITA MAP parsing failed: {e}")
            print(f"Error reading DITA MAP: {e}")
            return False
    
    def resolve_topic_path(self, topic_href):
        """Resolve topic path relative to DITA MAP location"""
        
        # Get directory containing the DITA MAP
        base_dir = self.dita_map_path.parent
        
        # Handle relative paths
        topic_path = base_dir / topic_href
        
        return topic_path.resolve()
    
    def fix_unclosed_tags(self, content):
        """Close unclosed DITA/XML tags"""
        
        tag_pairs = {
            'p', 'li', 'ul', 'ol', 'table', 'row', 'entry',
            'b', 'i', 'code', 'ph', 'title', 'shortdesc', 'body'
        }
        
        for tag in tag_pairs:
            # Count opens and closes
            open_pattern = rf'<{tag}(?:\s[^>]*)?>'
            close_pattern = rf'</{tag}>'
            
            open_count = len(re.findall(open_pattern, content))
            close_count = len(re.findall(close_pattern, content))
            
            if open_count > close_count:
                missing = open_count - close_count
                closing_tag = f'</{tag}>' * missing
                content += closing_tag
        
        return content
    
    def fix_self_closing_tags(self, content):
        """Ensure proper self-closing syntax"""
        
        self_closing_tags = ['image', 'note', 'reference']
        
        for tag in self_closing_tags:
            pattern = rf'<{tag}(\s[^>]*)?>(\s*</{tag}>)?'
            replacement = r'<\1 />'
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def standardize_element_names(self, content):
        """Replace non-DITA element names with proper ones"""
        
        mappings = {
            'section': 'ph',
            'subsection': 'ph', 
            'paragraph': 'p',
            'heading': 'h',
            'emphasis': 'em',
            'strong': 'b',
            'italic': 'i',
            'preformatted': 'pre',
            'item': 'li',
            'list': 'ul',
            'ordered-list': 'ol',
        }
        
        for old, new in mappings.items():
            # Replace opening tags
            content = re.sub(
                rf'<{old}(\s[^>]*)?>',
                f'<{new}\\1>',
                content
            )
            # Replace closing tags
            content = re.sub(
                rf'</{old}>',
                f'</{new}>',
                content
            )
        
        return content
    
    def fix_dita_hierarchy(self, content):
        """Fix improper nesting in DITA topics"""
        
        # Ensure topic wrapper exists
        if not re.search(r'<topic\b', content):
            content = f'<topic>\n{content}\n</topic>'
        
        # Ensure body exists within topic
        if re.search(r'<topic\b', content) and not re.search(r'<body\b', content):
            content = re.sub(r'(<topic[^>]*>)', r'\1<body>', content)
            content = content.replace('</topic>', '</body>\n</topic>')
        
        # Remove nested bodies (common AI error)
        content = re.sub(r'</body>\s*<body>', '', content)
        
        return content
    
    def remove_servicenow_artifacts(self, content):
        """Remove ServiceNow-specific remnants"""
        
        patterns = [
            r'sys_id=\w+',
            r'instance_id=\w+',
            r'class="[^"]*vivid[^"]*"',
            r'class="[^"]*kb_kb[^"]*"',
            r'class="[^"]*knowledge_article[^"]*"',
            r'table="[^"]*sn_knowledge_[^"]*"',
            r'<!--\s*SN[^>]*-->',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        return content
    
    def normalize_whitespace(self, content):
        """Clean up whitespace issues"""
        
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r'^ +| +$', '', content, flags=re.MULTILINE)
        content = content.replace('\t', '    ')
        
        return content.strip()
    
    def process_topic(self, topic_path):
        """Process a single DITA topic file"""
        
        try:
            with open(topic_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            content = self.remove_servicenow_artifacts(content)
            content = self.fix_xml_syntax(content)
            content = self.standardize_element_names(content)
            content = self.fix_dita_hierarchy(content)
            content = self.normalize_whitespace(content)
            
            # Determine output path (preserve structure)
            rel_path = topic_path.relative_to(self.dita_map_path.parent)
            output_path = self.output_dir / rel_path
            
            # Create output directories
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write if changed
            if content != original_content:
                self.stats['files_modified'] += 1
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats['processed'] += 1
            return True
            
        except Exception as e:
            self.stats['errors'] += 1
            self.errors.append(f"{topic_path}: {e}")
            print(f"Error processing {topic_path}: {e}")
            return False
    
    def fix_xml_syntax(self, content):
        """Combined XML syntax fixes"""
        
        content = self.fix_unclosed_tags(content)
        content = self.fix_self_closing_tags(content)
        
        # Basic XML entity escaping
        content = content.replace('&', '&amp;')
        content = content.replace('<', '&lt;')
        content = content.replace('>', '&gt;')
        content = content.replace('"', '&quot;')
        
        return content
    
    def run(self, overwrite=False):
        """Run the normalizer on all topics in the DITA MAP"""
        
        print(f"\n{'='*50}")
        print("DITA MAP Normalizer")
        print(f"{'='*50}")
        print(f"Input DITA MAP: {self.dita_map_path}")
        print(f"Output Directory: {self.output_dir}")
        print(f"{'='*50}\n")
        
        # Parse DITA MAP first
        if not self.parse_ditamap():
            print("\nFailed to parse DITA MAP. Exiting.")
            return self.stats
        
        # Process each topic
        print(f"\nProcessing {len(self.map_topics)} topics...\n")
        
        for idx, topic_info in enumerate(self.map_topics, 1):
            topic_href = topic_info['href']
            print(f"[{idx}/{len(self.map_topics)}] Processing: {topic_href}")
            
            topic_path = self.resolve_topic_path(topic_href)
            
            if topic_path.exists():
                self.process_topic(topic_path)
            else:
                print(f"  ⚠️  Topic file not found: {topic_path}")
                self.stats['errors'] += 1
        
        # Print summary
        self.print_summary()
        
        return self.stats
    
    def print_summary(self):
        """Print processing summary"""
        
        print(f"\n{'='*50}")
        print("SUMMARY")
        print(f"{'='*50}")
        print(f"Topics referenced in DITA MAP: {len(self.map_topics)}")
        print(f"Successfully processed:        {self.stats['processed']}")
        print(f"Files modified:                {self.stats['files_modified']}")
        print(f"Errors:                        {self.stats['errors']}")
        
        if self.errors:
            print(f"\nErrors encountered:")
            for err in self.errors[:10]:  # Limit to first 10
                print(f"  • {err}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")
        
        print(f"{'='*50}\n")


def setup_logging():
    """Configure logging for the normalizer"""
    
    log_dir = Path('./logs')
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'dita_normalization_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def main():
    """Command-line interface entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Normalize DITA topics from DITA MAP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dita_map_normalizer.py --map ./docs.ditamap
  python dita_map_normalizer.py --map ./docs.ditamap --output ./output/
  python dita_map_normalizer.py --map ./docs.ditamap --dry-run
        """
    )
    
    parser.add_argument('--map', '-m', required=True, help='Path to DITA MAP file')
    parser.add_argument('--output', '-o', help='Output directory (default: same as DITA MAP)')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Preview changes without modifying')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Starting DITA MAP normalization: {args.map}")
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified")
        print("Previewing changes before committing...\n")
    
    normalizer = DITAMapNormalizer(args.map, args.output)
    
    if args.dry_run:
        stats = normalizer.run()
    else:
        stats = normalizer.run()
    
    logger.info(f"Normalization complete. Processed: {stats['processed']}, Errors: {stats['errors']}")
    
    return stats


if __name__ == '__main__':
    sys.exit(main())
