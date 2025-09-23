#!/usr/bin/env python3
"""
Final batch fixer for remaining character encoding issues
"""

import os
import re
import subprocess

def fix_remaining_files():
    # Get the current issues
    result = subprocess.run(['python3', 'scripts/character-encoding-validator.py', '.'],
                          capture_output=True, text=True)

    if 'Total issues: 0' in result.stderr:
        print("✅ No issues found!")
        return

    # Files to check and fix
    files_to_fix = [
        'shopify-liquid-guides/code-library/sections/enhanced/feature-grid.liquid',
        'shopify-liquid-guides/code-library/sections/enhanced/logo-list.liquid',
        'shopify-liquid-guides/code-library/sections/enhanced/video.liquid',
        'shopify-liquid-guides/code-library/sections/enhanced/contact-form.liquid'
    ]

    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            continue

        print(f"Fixing {file_path}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Common fix patterns for remaining issues
            fixes = [
                # Form errors
                (r'{{\s*form\.errors\s*\|\s*default:\s*[\'\"]*[\'\"]*\s*}}',
                 r'{{ form.errors | default: "" | escape }}'),

                # Block/section settings (but not richtext patterns)
                (r'{{\s*(block|section)\.settings\.([a-zA-Z_]+)\s*}}(?!\s*\|)(?![^{]*(?:richtext|rte|content|body|description|answer))',
                 r'{{ \1.settings.\2 | escape }}'),

                # Title/heading/label patterns
                (r'{{\s*(block|section)\.settings\.(title|heading|label|name|caption)\s*}}(?!\s*\|)',
                 r'{{ \1.settings.\2 | escape }}'),
            ]

            for pattern, replacement in fixes:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    print(f"  Applied fix: {pattern[:50]}...")

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ Updated {file_path}")
            else:
                print(f"  ℹ️ No changes needed for {file_path}")

        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_remaining_files()