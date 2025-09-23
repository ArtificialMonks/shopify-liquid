#!/usr/bin/env python3
"""
Comprehensive escape filter fix script for all remaining legitimate issues
Handles all common patterns safely and efficiently
"""

import os
import re
import sys
from pathlib import Path

class ComprehensiveEscapeFixer:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.fixes_applied = []
        self.files_modified = 0

    def fix_all_escape_issues(self, content):
        """Fix all legitimate escape issues comprehensively"""
        fixes = 0
        original = content

        # Pattern 1: Simple text content in HTML (not richtext, not in URLs/CSS)
        text_patterns = [
            # Basic text fields that need escaping
            (r'{{\s*((?:section|block)\.settings\.(?:title|heading|name|label|caption|alt_text|meta_title|meta_description))\s*}}',
             r'{{ \1 | escape }}'),

            # Customer/user content
            (r'{{\s*(customer\.(?:first_name|last_name|name|email))\s*}}',
             r'{{ \1 | escape }}'),

            # Product content (non-richtext)
            (r'{{\s*(product\.(?:title|vendor|type|tags))\s*}}',
             r'{{ \1 | escape }}'),

            # Collection content (non-richtext)
            (r'{{\s*(collection\.(?:title|description))\s*}}',
             r'{{ \1 | escape }}'),

            # Article content (non-richtext)
            (r'{{\s*(article\.(?:title|summary|excerpt))\s*}}',
             r'{{ \1 | escape }}'),

            # Page content (non-richtext)
            (r'{{\s*(page\.(?:title|content))\s*}}',
             r'{{ \1 | escape }}'),
        ]

        # Pattern 2: Text in HTML attributes (aria-label, title, alt, placeholder)
        attribute_patterns = [
            # Aria-label with user content
            (r'aria-label=["\']([^"\']*){{\s*([^}]*(?:title|name|label|heading)[^}]*)\s*}}([^"\']*)["\']',
             r'aria-label="\1{{ \2 | escape }}\3"'),

            # Title attribute with user content
            (r'title=["\']([^"\']*){{\s*([^}]*(?:title|name|label|heading)[^}]*)\s*}}([^"\']*)["\']',
             r'title="\1{{ \2 | escape }}\3"'),

            # Alt attribute with user content
            (r'alt=["\']([^"\']*){{\s*([^}]*(?:title|name|label|heading|alt)[^}]*)\s*}}([^"\']*)["\']',
             r'alt="\1{{ \2 | escape }}\3"'),
        ]

        # Apply text content fixes
        for pattern, replacement in text_patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                count = len(re.findall(pattern, content, re.IGNORECASE))
                fixes += count
                content = new_content

        # Apply attribute fixes
        for pattern, replacement in attribute_patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                count = len(re.findall(pattern, content, re.IGNORECASE))
                fixes += count
                content = new_content

        # Pattern 3: Fix specific problem areas identified
        specific_fixes = [
            # Product descriptions in display context (not richtext editors)
            (r'{{\s*product\.description\s*\|\s*truncate:\s*\d+\s*}}',
             lambda m: m.group(0).replace('}', ' | escape }}')),
        ]

        for pattern, replacement in specific_fixes:
            if callable(replacement):
                def repl_func(match):
                    return replacement(match)
                new_content = re.sub(pattern, repl_func, content, flags=re.IGNORECASE)
                if new_content != content:
                    fixes += len(re.findall(pattern, content, re.IGNORECASE))
                    content = new_content

        if self.verbose and fixes > 0:
            print(f"  Applied {fixes} comprehensive escape fixes")

        return content, fixes

    def fix_file(self, file_path):
        """Fix all escape issues in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            if self.verbose:
                print(f"\nProcessing: {file_path}")

            # Apply comprehensive fixes
            content, fixes = self.fix_all_escape_issues(content)
            total_fixes += fixes

            # Only write if changes were made
            if content != original_content:
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                self.files_modified += 1
                self.fixes_applied.append({
                    'file': file_path,
                    'fixes': total_fixes
                })

                if self.verbose:
                    print(f"  ✅ Applied {total_fixes} comprehensive fixes")

                return True
            else:
                if self.verbose:
                    print(f"  No fixes needed")
                return False

        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            return False

    def fix_directory(self, directory):
        """Fix all Liquid files in a directory"""
        liquid_files = []

        # Find all .liquid files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.liquid'):
                    liquid_files.append(os.path.join(root, file))

        print(f"Found {len(liquid_files)} .liquid files to process")

        for file_path in liquid_files:
            self.fix_file(file_path)

        return self.files_modified

    def print_summary(self):
        """Print summary of fixes applied"""
        print("\n" + "="*60)
        print("🔧 COMPREHENSIVE ESCAPE FIX SUMMARY")
        print("="*60)

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files were actually modified")

        if self.fixes_applied:
            print(f"\n✅ Modified {self.files_modified} files:")
            for fix in self.fixes_applied:
                print(f"  📝 {fix['file']}: {fix['fixes']} escape filters added")
        else:
            print("\n✨ No escape issues found!")

        print("\n" + "="*60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Comprehensive escape filter fixer')
    parser.add_argument('path', help='File or directory path to fix')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    fixer = ComprehensiveEscapeFixer(dry_run=args.dry_run, verbose=args.verbose)

    if os.path.isfile(args.path):
        fixer.fix_file(args.path)
    elif os.path.isdir(args.path):
        fixer.fix_directory(args.path)
    else:
        print(f"Error: {args.path} is not a valid file or directory")
        sys.exit(1)

    fixer.print_summary()

    # Return exit code based on whether fixes were needed
    sys.exit(0 if not fixer.fixes_applied else 1)

if __name__ == '__main__':
    main()