#!/usr/bin/env python3
"""
Fix character encoding issues in Shopify Liquid themes
Automatically fixes HTML entities, adds escape filters, and removes smart quotes
"""

import os
import sys
import re
import argparse
from pathlib import Path

class CharacterEncodingFixer:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.fixes_applied = []
        self.files_modified = 0

    def fix_html_entities_in_liquid(self, content):
        """Fix HTML entities in Liquid/HTML content (not in schema)"""
        fixes = 0
        original = content

        # Fix HTML entities in title tags and other HTML contexts
        # Replace &ndash; with –
        content = re.sub(r'&ndash;', '–', content)
        # Replace &mdash; with —
        content = re.sub(r'&mdash;', '—', content)
        # Replace &nbsp; with space
        content = re.sub(r'&nbsp;', ' ', content)
        # Replace &amp; with & (but not in schema)
        content = re.sub(r'&amp;(?![^{]*\{% endschema %\})', '&', content)
        # Replace &quot; with "
        content = re.sub(r'&quot;', '"', content)
        # Replace &lt; with <
        content = re.sub(r'&lt;', '<', content)
        # Replace &gt; with >
        content = re.sub(r'&gt;', '>', content)

        if content != original:
            fixes = len(re.findall(r'&[a-z]+;', original))
            if self.verbose:
                print(f"  Fixed {fixes} HTML entities")

        return content, fixes

    def add_escape_filters_to_css(self, content):
        """Add escape filters to user-controllable content in CSS"""
        fixes = 0
        original = content

        # Pattern to find unescaped settings in CSS style blocks
        # Match {{ section.settings.* }} or {{ block.settings.* }} without escape filter
        css_pattern = r'(<style[^>]*>)(.*?)(</style>)'

        def fix_css_block(match):
            nonlocal fixes
            style_open = match.group(1)
            css_content = match.group(2)
            style_close = match.group(3)

            # Settings that are safe without escape (numeric values, colors)
            safe_settings = [
                'padding', 'margin', 'width', 'height', 'size', 'spacing',
                'opacity', 'weight', 'line_height', 'letter_spacing'
            ]

            # Pattern to find unescaped settings
            setting_pattern = r'\{\{\s*(section|block)\.settings\.(\w+)([^}]*)\}\}'

            def check_and_fix_setting(setting_match):
                nonlocal fixes
                full_match = setting_match.group(0)
                object_type = setting_match.group(1)
                setting_name = setting_match.group(2)
                filters = setting_match.group(3)

                # Check if it's a safe numeric/color setting
                is_safe = any(safe in setting_name.lower() for safe in safe_settings)

                # Check if escape filter already exists
                has_escape = 'escape' in filters

                # For CSS values, we generally don't need escape filter for:
                # - Numeric values (padding, margin, etc.)
                # - Color values
                # - Alignment values
                # But we DO need it for any user-generated text content

                if not has_escape and not is_safe:
                    # For CSS context, we actually shouldn't add escape to most values
                    # as they're CSS properties, not HTML content
                    # Only add escape if it's clearly text content
                    if any(text_ind in setting_name.lower() for text_ind in ['text', 'content', 'label', 'title', 'name']):
                        fixes += 1
                        return f'{{{{ {object_type}.settings.{setting_name}{filters} | escape }}}}'

                return full_match

            fixed_css = re.sub(setting_pattern, check_and_fix_setting, css_content)
            return style_open + fixed_css + style_close

        content = re.sub(css_pattern, fix_css_block, content, flags=re.DOTALL)

        if self.verbose and fixes > 0:
            print(f"  Added {fixes} escape filters to CSS")

        return content, fixes

    def fix_smart_quotes(self, content):
        """Replace smart quotes with standard ASCII quotes"""
        fixes = 0
        original = content

        # Smart quotes replacements
        replacements = {
            '"': '"',  # Left double quote
            '"': '"',  # Right double quote
            ''': "'",  # Left single quote
            ''': "'",  # Right single quote
            '…': '...',  # Ellipsis
            '–': '-',  # En dash (in code contexts)
            '—': '-',  # Em dash (in code contexts)
        }

        for smart, ascii_char in replacements.items():
            if smart in content:
                count = content.count(smart)
                content = content.replace(smart, ascii_char)
                fixes += count

        if self.verbose and fixes > 0:
            print(f"  Fixed {fixes} smart quotes/characters")

        return content, fixes

    def fix_file(self, file_path):
        """Fix all character encoding issues in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            if self.verbose:
                print(f"\nProcessing: {file_path}")

            # Apply fixes in order
            content, fixes = self.fix_html_entities_in_liquid(content)
            total_fixes += fixes

            content, fixes = self.add_escape_filters_to_css(content)
            total_fixes += fixes

            content, fixes = self.fix_smart_quotes(content)
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
                    print(f"  ✅ Applied {total_fixes} fixes")

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
        print("🔧 CHARACTER ENCODING FIX SUMMARY")
        print("="*60)

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files were actually modified")

        if self.fixes_applied:
            print(f"\n✅ Modified {self.files_modified} files:")
            for fix in self.fixes_applied:
                print(f"  📝 {fix['file']}: {fix['fixes']} fixes")
        else:
            print("\n✨ No character encoding issues found!")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description='Fix character encoding issues in Shopify Liquid themes')
    parser.add_argument('path', help='File or directory path to fix')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without modifying files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    fixer = CharacterEncodingFixer(dry_run=args.dry_run, verbose=args.verbose)

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