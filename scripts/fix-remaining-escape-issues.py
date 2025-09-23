#!/usr/bin/env python3
"""
Automated fix script for remaining legitimate escape filter issues
Only fixes issues identified as legitimate by our enterprise-grade validator
"""

import os
import re
import sys
import json
from pathlib import Path

class EscapeFilterFixer:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.fixes_applied = []
        self.files_modified = 0

    def fix_legitimate_unescaped_content(self, content):
        """Fix only legitimate unescaped content issues"""
        fixes = 0
        original = content

        # Pattern 1: Text content in HTML context (not URL, CSS, or schema)
        # Look for settings output without escape that should have it
        patterns_to_fix = [
            # Basic text content patterns
            (r'{{\s*(block\.settings\.(?:title|heading|description|text|body|content|label|caption|name))\s*}}',
             r'{{ \1 | escape }}'),
            (r'{{\s*(section\.settings\.(?:title|heading|description|text|body|content|label|caption|name))\s*}}',
             r'{{ \1 | escape }}'),

            # Text in aria-label, title, alt attributes (but not in href/src)
            (r'(?:aria-label|title|alt|placeholder)=["\'][^"\']*{{\s*([^}]*(?:settings\.[^}]*name|settings\.[^}]*title|settings\.[^}]*label))\s*}}[^"\']*["\']',
             lambda m: m.group(0).replace(f'{{{{ {m.group(1)} }}}}', f'{{{{ {m.group(1)} | escape }}}}')),
        ]

        for pattern, replacement in patterns_to_fix:
            if callable(replacement):
                # Custom replacement function
                def repl_func(match):
                    return replacement(match)
                new_content = re.sub(pattern, repl_func, content, flags=re.IGNORECASE)
            else:
                # Simple string replacement
                new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

            if new_content != content:
                fixes += re.subn(pattern, replacement if not callable(replacement) else repl_func, content, flags=re.IGNORECASE)[1]
                content = new_content

        if self.verbose and fixes > 0:
            print(f"  Added {fixes} escape filters to text content")

        return content, fixes

    def fix_file(self, file_path):
        """Fix legitimate escape issues in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            if self.verbose:
                print(f"\nProcessing: {file_path}")

            # Apply fixes
            content, fixes = self.fix_legitimate_unescaped_content(content)
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
                    print(f"  ✅ Applied {total_fixes} escape filter fixes")

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
        print("🔧 ESCAPE FILTER FIX SUMMARY")
        print("="*60)

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files were actually modified")

        if self.fixes_applied:
            print(f"\n✅ Modified {self.files_modified} files:")
            for fix in self.fixes_applied:
                print(f"  📝 {fix['file']}: {fix['fixes']} escape filters added")
        else:
            print("\n✨ No legitimate escape issues found!")

        print("\n" + "="*60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix legitimate unescaped content issues')
    parser.add_argument('path', help='File or directory path to fix')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    fixer = EscapeFilterFixer(dry_run=args.dry_run, verbose=args.verbose)

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