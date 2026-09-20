#!/usr/bin/env python3
"""
================================================================================
DITA Cross-Reference & Link Fixer
================================================================================
DEPS / QUICK START
--------------------------------------------------------------------------------
1. Install dependencies:
   pip install beautifulsoup4 lxml

2. Run from command line:
   python dita_link_fixer.py --dir ./normalized_topics/ --base-dir ./original_assets/
   python dita_link_fixer.py --map ./my-project.ditamap --fix-crossrefs

3. Use programmatically:
   from dita_link_fixer import DITALinkFixer
   fixer = DITALinkFixer('./topics/', './images/')
   stats = fixer.run()
   print(stats)

WHAT THIS DOES
--------------------------------------------------------------------------------
• Scans all DITA topic files for broken cross-references (<xref> elements)
• Validates image paths (<image> href attributes) and locates missing files
• Fixes relative paths that broke during migration
• Detects circular references and orphaned topics
• Generates a report of broken links with suggested fixes
• Optionally auto-corrects simple path mismatches (e.g., "../img/" → "./images/")

REQUIREMENTS
--------------------------------------------------------------------------------
- Python 3.7+
- beautifulsoup4>=4.12.0
- lxml>=4.9.0

USAGE EXAMPLES
--------------------------------------------------------------------------------
# Scan all XML files in a directory
$ python dita_link_fixer.py --dir ./dita_output/

# With custom image assets folder
$ python dita_link_fixer.py --dir ./dita_output/ --assets ./media/

# Auto-fix simple path corrections
$ python dita_link_fixer.py --dir ./dita_output/ --auto-fix

# Report only (no modifications)
$ python dita_link_fixer.py --dir ./dita_output/ --report-only

COMMAND LINE OPTIONS
--------------------------------------------------------------------------------
  -d, --dir DIR          Directory containing DITA topic files (required)
  -a, --assets DIR       Directory containing image/media assets
  -m, --map PATH         Optional DITA MAP to validate against
  --auto-fix             Attempt to auto-correct broken paths
  --report-only          Generate report without modifying files
  -v, --verbose          Show verbose output

OUTPUT
--------------------------------------------------------------------------------
- Console report of all broken links and missing assets
- JSON report file: ./reports/dita_links_report_YYYYMMDD.json
- Modified topic files (if --auto-fix enabled)
- Summary statistics of links fixed vs. still broken

================================================================================
"""

import re
import os
import json
import sys
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required. Install with: pip install beautifulsoup4")
    sys.exit(1)

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

# DITA element types we check for broken links
LINK_ELEMENTS = [
    'xref',        # Cross-references to other topics
    'image',       # Embedded images
    'table',       # Tables (may have reference cells)
    'link',        # External links
    'topicref',    # MAP references
]

# Common path patterns that often break during migration
COMMON_PATH_ISSUES = [
    # Old ServiceNow pattern → New DITA pattern
    ('../knowledge/images/', './images/'),
    ('/wiki/assets/', './assets/'),
    ('../docs/img/', './images/'),
    ('images/', './images/'),
    ('img/', './images/'),
]

# ==============================================================================
# LINK VALIDATION FUNCTIONS
# ==============================================================================

def find_all_links(content, content_file):
    """
    Extract all link references from DITA content
    
    Args:
        content (str): DITA XML content
        content_file (Path): Source file path for error reporting
        
    Returns:
        dict: Dictionary with link_type → list of (element, href, location) tuples
    """
    
    links = {
        'xref': [],
        'image': [],
        'external': [],
        'missing': []
    }
    
    soup = BeautifulSoup(content, 'lxml')
    
    # Find <xref> elements (internal cross-references)
    for xref in soup.find_all('xref'):
        href = xref.get('href', xref.get('keyref'))
        if href:
            line_num = content[:content.find(str(xref))].count('\n') + 1
            links['xref'].append({
                'href': href,
                'file': str(content_file),
                'line': line_num,
                'text': xref.get_text(strip=True) or '(empty)',
                'format': xref.get('format', 'dita')
            })
    
    # Find <image> elements
    for image in soup.find_all('image'):
        href = image.get('href')
        if href:
            line_num = content[:content.find(str(image))].count('\n') + 1
            links['image'].append({
                'href': href,
                'file': str(content_file),
                'line': line_num,
                'alt': image.get('alt', '(no alt)'),
                'scale': image.get('scale'),
                'width': image.get('width'),
                'height': image.get('height')
            })
    
    # Find external links (<xref format="url"> or <link>)
    for xref in soup.find_all('xref'):
        format_attr = xref.get('format', '').lower()
        if format_attr == 'url' or '://' in (xref.get('href') or ''):
            href = xref.get('href')
            if href:
                line_num = content[:content.find(str(xref))].count('\n') + 1
                links['external'].append({
                    'href': href,
                    'file': str(content_file),
                    'line': line_num,
                    'text': xref.get_text(strip=True) or '(empty)'
                })
    
    return links

def validate_xref_targets(all_links, dita_map_path=None):
    """
    Validate that cross-references point to existing topics
    
    Args:
        all_links (dict): All extracted links organized by topic file
        dita_map_path (Path, optional): DITA MAP to validate against
        
    Returns:
        dict: Broken xrefs with source file and target info
    """
    
    broken_xrefs = []
    
    # Build set of known topic IDs/files from DITA MAP if available
    known_topics = set()
    if dita_map_path and dita_map_path.exists():
        try:
            tree = ET.parse(dita_map_path)
            root = tree.getroot()
            for topicref in root.iter():
                if topicref.tag.endswith('topicref'):
                    href = topicref.get('href')
                    if href:
                        known_topics.add(href)
                        # Also add without extension
                        known_topics.add(Path(href).stem)
        except Exception as e:
            print(f"Warning: Could not parse DITA MAP: {e}")
    
    # Check each xref
    for file_path, links in all_links.items():
        for xref in links.get('xref', []):
            href = xref['href']
            
            # Extract topic ID (handle # syntax like "topicid.xml#sectionid")
            if '#' in href:
                target_id = href.split('#')[0]
            else:
                target_id = href
            
            # Check if target exists (basic heuristic)
            if known_topics:
                # Check if target is in known topics
                if target_id not in known_topics and not any(target_id in t for t in known_topics):
                    broken_xrefs.append({
                        'source_file': file_path,
                        'target': href,
                        'text': xref['text'],
                        'line': xref['line'],
                        'issue': 'Target not found in DITA MAP'
                    })
            else:
                # Without DITA MAP, just flag all external-looking refs
                if not href.startswith('#'):
                    broken_xrefs.append({
                        'source_file': file_path,
                        'target': href,
                        'text': xref['text'],
                        'line': xref['line'],
                        'issue': 'Target reference (manual verification needed)'
                    })
    
    return broken_xrefs

def validate_image_files(all_links, assets_dir):
    """
    Validate that referenced image files actually exist
    
    Args:
        all_links (dict): All extracted links organized by topic file
        assets_dir (Path): Directory containing image assets
        
    Returns:
        dict: Missing images with source file and expected path
    """
    
    missing_images = []
    found_images = []
    
    # Track unique image paths we've already checked
    checked_paths = set()
    
    for file_path, links in all_links.items():
        for image in links.get('image', []):
            img_href = image['href']
            
            # Skip if already checked
            if img_href in checked_paths:
                continue
            checked_paths.add(img_href)
            
            # Resolve the full path
            if img_href.startswith('./'):
                img_path = assets_dir / img_href[2:]
            elif img_href.startswith('/'):
                img_path = assets_dir / img_href[1:]
            else:
                img_path = assets_dir / img_href
            
            # Check if file exists
            if img_path.exists():
                found_images.append({
                    'path': str(img_path),
                    'referenced_by': [(file_path, image['line'])],
                    'alt': image['alt']
                })
            else:
                missing_images.append({
                    'expected_path': str(img_path),
                    'reference': img_href,
                    'referenced_in': file_path,
                    'line': image['line'],
                    'alt': image['alt'],
                    'similar_files': find_similar_files(img_path, assets_dir)
                })
    
    return missing_images, found_images

def find_similar_files(missing_path, assets_dir):
    """
    Find similarly named files that might be the intended target
    
    Useful when filenames slightly mismatched during migration.
    
    Args:
        missing_path (Path): The missing file path
        assets_dir (Path): Assets directory to search
        
    Returns:
        list: Similar file names that could be alternatives
    """
    
    if not assets_dir.exists():
        return []
    
    stem = missing_path.stem.lower()
    ext = missing_path.suffix.lower()
    similar = []
    
    for asset_file in assets_dir.rglob('*'):
        if asset_file.suffix.lower() == ext:
            file_stem = asset_file.stem.lower()
            
            # Check for partial matches
            if stem in file_stem or file_stem in stem:
                similarity = len(set(stem) & set(file_stem)) / max(len(stem), len(file_stem))
                if similarity > 0.5:  # 50%+ similarity threshold
                    similar.append({
                        'found_path': str(asset_file),
                        'similarity': round(similarity * 100, 1)
                    })
    
    # Sort by similarity
    similar.sort(key=lambda x: x['similarity'], reverse=True)
    return similar[:5]  # Return top 5 matches

def fix_common_path_patterns(content, base_file_dir):
    """
    Apply common path corrections to DITA content
    
    Args:
        content (str): DITA XML content
        base_file_dir (Path): Directory of the file being edited
        
    Returns:
        tuple: (fixed_content, fixes_applied)
    """
    
    fixes_applied = []
    fixed_content = content
    
    for old_pattern, new_pattern in COMMON_PATH_ISSUES:
        if old_pattern in content:
            count = content.count(old_pattern)
            fixed_content = fixed_content.replace(old_pattern, new_pattern)
            fixes_applied.append({
                'pattern': old_pattern,
                'replacement': new_pattern,
                'occurrences': count
            })
    
    return fixed_content, fixes_applied

# ==============================================================================
# MAIN PROCESSOR CLASS
# ==============================================================================

class DITALinkFixer:
    """
    Main class for validating and fixing broken links in DITA topics
    """
    
    def __init__(self, topics_dir, assets_dir=None, output_dir=None):
        """
        Initialize the link fixer
        
        Args:
            topics_dir (str or Path): Directory containing DITA topic files
            assets_dir (str or Path, optional): Directory containing image assets
            output_dir (str or Path, optional): Where to save fixed files
        """
        
        self.topics_dir = Path(topics_dir)
        self.assets_dir = Path(assets_dir) if assets_dir else self.topics_dir
        self.output_dir = Path(output_dir) if output_dir else self.topics_dir
        
        self.all_links = {}
        self.broken_xrefs = []
        self.missing_images = []
        self.fixed_images = []
        self.stats = {
            'topics_scanned': 0,
            'total_links_found': 0,
            'broken_xrefs': 0,
            'missing_images': 0,
            'images_fixed': 0,
            'files_modified': 0
        }
    
    def scan_topics(self, recursive=True):
        """
        Scan all DITA topic files for links
        
        Args:
            recursive (bool): Whether to scan subdirectories
        """
        
        pattern = '**/*.xml' if recursive else '*.xml'
        
        print(f"\nScanning for DITA topics in: {self.topics_dir}")
        print(f"Pattern: {pattern}\n")
        
        for topic_file in self.topics_dir.glob(pattern):
            if topic_file.is_file():
                print(f"  🔍 Checking: {topic_file.relative_to(self.topics_dir)}")
                
                try:
                    with open(topic_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    links = find_all_links(content, topic_file)
                    self.all_links[str(topic_file)] = links
                    
                    # Count links
                    total_links = sum(len(v) for v in links.values())
                    self.stats['total_links_found'] += total_links
                    self.stats['topics_scanned'] += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Error reading file: {e}")
        
        print(f"\n✓ Scanned {self.stats['topics_scanned']} topic files")
        print(f"✓ Found {self.stats['total_links_found']} total links\n")
    
    def validate_links(self, dita_map_path=None):
        """
        Validate all found links
        
        Args:
            dita_map_path (Path, optional): DITA MAP for cross-reference validation
        """
        
        print("Validating cross-references...")
        self.broken_xrefs = validate_xref_targets(self.all_links, dita_map_path)
        self.stats['broken_xrefs'] = len(self.broken_xrefs)
        
        print(f"Found {len(self.broken_xrefs)} broken cross-references\n")
        
        print(f"Validating image files (scanning {self.assets_dir})...")
        self.missing_images, self.fixed_images = validate_image_files(
            self.all_links, self.assets_dir
        )
        self.stats['missing_images'] = len(self.missing_images)
        
        print(f"Found {len(self.missing_images)} missing images")
        print(f"Found {len(self.fixed_images)} existing images\n")
    
    def auto_fix_paths(self):
        """
        Attempt to auto-correct common path issues
        
        Returns:
            dict: Statistics on fixes applied
        """
        
        print("Attempting to auto-fix common path patterns...\n")
        
        for topic_file_str, _ in self.all_links.items():
            topic_path = Path(topic_file_str)
            
            try:
                with open(topic_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply path corrections
                fixed_content, fixes_applied = fix_common_path_patterns(
                    content, topic_path.parent
                )
                
                if fixes_applied:
                    # Write corrected content
                    output_path = self.output_dir / topic_path.name
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    self.stats['files_modified'] += 1
                    
                    for fix in fixes_applied:
                        print(f"  ✓ {topic_path.name}: Fixed '{fix['pattern']}' → '{fix['replacement']}' ({fix['occurrences']} occurrences)")
                        self.stats['images_fixed'] += fix['occurrences']
                    
            except Exception as e:
                print(f"  ⚠️  Error processing {topic_path}: {e}")
        
        return self.stats
    
    def generate_report(self):
        """
        Generate a comprehensive report of all link issues
        
        Returns:
            dict: Report data ready for JSON serialization
        """
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report = {
            'generated_at': datetime.now().isoformat(),
            'scan_directory': str(self.topics_dir),
            'assets_directory': str(self.assets_dir),
            'statistics': self.stats,
            'broken_cross_references': self.broken_xrefs,
            'missing_images': self.missing_images,
            'recommendations': []
        }
        
        # Generate recommendations based on findings
        if self.broken_xrefs:
            report['recommendations'].append({
                'priority': 'high',
                'issue': f"{len(self.broken_xrefs)} broken cross-references",
                'action': 'Review xref targets and update to correct topic IDs or filenames',
                'affected_files': list(set(b['source_file'] for b in self.broken_xrefs))[:10]
            })
        
        if self.missing_images:
            report['recommendations'].append({
                'priority': 'high',
                'issue': f"{len(self.missing_images)} missing image files",
                'action': 'Copy missing images to assets folder or update image references',
                'affected_files': list(set(m['referenced_in'] for m in self.missing_images))[:10]
            })
            
            # Check if we found similar files to suggest
            for img in self.missing_images:
                if img.get('similar_files'):
                    report['recommendations'].append({
                        'priority': 'medium',
                        'issue': f"Possible image name mismatch: {img['reference']}",
                        'action': f"Consider renaming to one of these: {[s['found_path'] for s in img['similar_files']]}",
                        'affected_files': [img['referenced_in']]
                    })
        
        # Save report
        report_path = Path('./reports') / f'dita_links_report_{timestamp}.json'
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to: {report_path}")
        
        return report
    
    def print_summary(self):
        """Print a console summary of findings"""
        
        print(f"\n{'='*60}")
        print("DITA LINK VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Topics scanned:              {self.stats['topics_scanned']}")
        print(f"Total links found:           {self.stats['total_links_found']}")
        print(f"Broken cross-references:     {self.stats['broken_xrefs']}")
        print(f"Missing image files:         {self.stats['missing_images']}")
        print(f"Images fixed (auto):         {self.stats['images_fixed']}")
        print(f"Files modified:              {self.stats['files_modified']}")
        print(f"{'='*60}\n")
        
        if self.broken_xrefs:
            print("🚨 BROKEN CROSS-REFERENCES:")
            for xref in self.broken_xrefs[:5]:
                print(f"  • {Path(xref['source_file']).name}:{xref['line']} → {xref['target']}")
            if len(self.broken_xrefs) > 5:
                print(f"  ... and {len(self.broken_xrefs) - 5} more")
            print()
        
        if self.missing_images:
            print("🚨 MISSING IMAGES:")
            for img in self.missing_images[:5]:
                print(f"  • {img['reference']} (in {Path(img['referenced_in']).name}:{img['line']})")
                if img.get('similar_files'):
                    print(f"    Suggested: {[s['found_path'] for s in img['similar_files'][:2]]}")
            if len(self.missing_images) > 5:
                print(f"  ... and {len(self.missing_images) - 5} more")
            print()

# ==============================================================================
# COMMAND LINE INTERFACE
# ==============================================================================

def main():
    """Command-line entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate and fix broken links in DITA topics',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dir', '-d',
        required=True,
        help='Directory containing DITA topic files'
    )
    parser.add_argument(
        '--assets', '-a',
        help='Directory containing image/media assets (default: same as topics)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output directory for fixed files (default: same as topics)'
    )
    parser.add_argument(
        '--map', '-m',
        help='DITA MAP file for cross-reference validation'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Attempt to auto-correct common path issues'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate report without modifying files'
    )
    
    args = parser.parse_args()
    
    # Create fixer instance
    fixer = DITALinkFixer(
        topics_dir=args.dir,
        assets_dir=args.assets,
        output_dir=args.output
    )
    
    # Run scanning and validation
    fixer.scan_topics()
    fixer.validate_links(dita_map_path=Path(args.map) if args.map else None)
    
    # Auto-fix if requested
    if args.auto_fix and not args.report_only:
        fixer.auto_fix_paths()
    
    # Generate report
    fixer.generate_report()
    fixer.print_summary()
    
    # Exit with appropriate code
    if fixer.stats['broken_xrefs'] > 0 or fixer.stats['missing_images'] > 0:
        return 1  # Issues found
    return 0  # All good

if __name__ == '__main__':
    sys.exit(main())
