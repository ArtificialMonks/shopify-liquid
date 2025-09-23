#!/usr/bin/env python3
"""
Final Codebase Escape Fixer - Fix all remaining character encoding issues
Targets the specific 23 errors identified in the full codebase scan
"""

import os
import re
import sys
from pathlib import Path

def apply_escape_fixes():
    """Apply escape filter fixes to all remaining problematic files"""

    # Define the specific fixes needed based on the validation report
    fixes = [
        # advanced-video-carousel.liquid - 4 issues with filter_type
        {
            'file': 'shopify-liquid-guides/code-library/sections/advanced-video-carousel.liquid',
            'patterns': [
                (r'filter-\{\{\s*block\.settings\.filter_type\s*\}\}', r'filter-{{ block.settings.filter_type | escape }}'),
            ]
        },

        # section-advanced-video-text.liquid - 2 issues
        {
            'file': 'shopify-liquid-guides/code-library/sections/section-advanced-video-text.liquid',
            'patterns': [
                (r'data-animate="\{\{\s*section\.settings\.anim_enable\s*\}\}"', r'data-animate="{{ section.settings.anim_enable | escape }}"'),
                (r'\{\{\s*section\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ section.settings.\1 | escape }}'),
            ]
        },

        # block-media-text.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/blocks/block-media-text.liquid',
            'patterns': [
                (r'\{\{\s*block\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ block.settings.\1 | escape }}'),
            ]
        },

        # block-video-text.liquid (different from heka-test version) - 3 issues
        {
            'file': 'shopify-liquid-guides/code-library/blocks/block-video-text.liquid',
            'patterns': [
                (r'\{\{\s*block\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ block.settings.\1 | escape }}'),
            ]
        },

        # meta-tags.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/snippets/meta-tags.liquid',
            'patterns': [
                (r'\{\{\s*(?:page|product|collection)\.(?!price|id|url)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ page.\1 | escape }}'),
            ]
        },

        # faq-accordion.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/sections/faq-accordion.liquid',
            'patterns': [
                (r'\{\{\s*block\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ block.settings.\1 | escape }}'),
            ]
        },

        # rich-text.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/sections/rich-text.liquid',
            'patterns': [
                (r'\{\{\s*section\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ section.settings.\1 | escape }}'),
            ]
        },

        # newsletter.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/sections/newsletter.liquid',
            'patterns': [
                (r'\{\{\s*section\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ section.settings.\1 | escape }}'),
            ]
        },

        # feature-grid.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/sections/feature-grid.liquid',
            'patterns': [
                (r'\{\{\s*block\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ block.settings.\1 | escape }}'),
            ]
        },

        # logo-list.liquid - 1 issue
        {
            'file': 'shopify-liquid-guides/code-library/sections/logo-list.liquid',
            'patterns': [
                (r'\{\{\s*block\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ block.settings.\1 | escape }}'),
            ]
        },

        # video.liquid - 2 issues
        {
            'file': 'shopify-liquid-guides/code-library/sections/video.liquid',
            'patterns': [
                (r'\{\{\s*section\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ section.settings.\1 | escape }}'),
            ]
        },

        # contact-form.liquid - 3 issues
        {
            'file': 'shopify-liquid-guides/code-library/sections/contact-form.liquid',
            'patterns': [
                (r'\{\{\s*form\.errors\s*\|\s*default:\s*\'\'?\s*\}\}', r'{{ form.errors | default: \'\' | escape }}'),
                (r'\{\{\s*section\.settings\.(?!richtext)([a-zA-Z_]+)\s*\}\}(?!\s*\|)', r'{{ section.settings.\1 | escape }}'),
            ]
        },
    ]

    fixed_files = []
    total_fixes = 0

    for fix_config in fixes:
        file_path = fix_config['file']

        # Handle different possible file locations
        possible_paths = [
            file_path,
            file_path.replace('shopify-liquid-guides/code-library/', ''),
            f"shopify-liquid-guides/code-library/{file_path}",
        ]

        # Find the actual file
        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break

        if not actual_path:
            print(f"⚠️ File not found: {file_path}")
            continue

        try:
            with open(actual_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            file_fixes = 0

            for pattern, replacement in fix_config['patterns']:
                matches = list(re.finditer(pattern, content))
                if matches:
                    content = re.sub(pattern, replacement, content)
                    file_fixes += len(matches)

            if file_fixes > 0:
                with open(actual_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"✅ Fixed {file_fixes} issues in {actual_path}")
                fixed_files.append(actual_path)
                total_fixes += file_fixes
            else:
                print(f"ℹ️ No issues found in {actual_path}")

        except Exception as e:
            print(f"❌ Error processing {actual_path}: {e}")

    print(f"\n🎯 SUMMARY:")
    print(f"  • Files processed: {len(fixes)}")
    print(f"  • Files fixed: {len(fixed_files)}")
    print(f"  • Total fixes applied: {total_fixes}")

    return total_fixes

if __name__ == "__main__":
    print("🔧 Final Codebase Escape Fixer")
    print("=" * 50)

    total_fixes = apply_escape_fixes()

    if total_fixes > 0:
        print(f"\n✅ Applied {total_fixes} escape filter fixes across the codebase")
        print("🚀 Ready for final validation")
    else:
        print("\n⚠️ No fixes were applied - check file paths and patterns")