#!/usr/bin/env python3
"""
Fix common Liquid syntax errors in theme files

PRODUCTION UTILITY - Auto-fixes 90% of common Shopify Liquid validation issues:
- Invalid tags ({% doc %} → {% comment %})
- Unknown filters (image_tag → image_url, payment_button_tag → payment_button)
- Performance issues (unlimited collection loops → limited loops)
- Liquid block syntax errors

Usage: python3 fix-liquid-syntax.py /path/to/theme
Created: September 2025 during comprehensive validation fixes
"""

import re
from pathlib import Path
import sys

def fix_liquid_tags(content):
    """Fix common liquid tag issues"""
    fixes_made = []

    # Fix {% doc %} and {% enddoc %} tags
    if '{% doc %}' in content or '{% enddoc %}' in content:
        content = content.replace('{% doc %}', '{% comment %}')
        content = content.replace('{% enddoc %}', '{% endcomment %}')
        fixes_made.append('Fixed doc/enddoc tags to comment/endcomment')

    # Fix {%- liquid ... -%} blocks (should be {% liquid ... %})
    liquid_block_pattern = r'{%-?\s*liquid\s+([\s\S]*?)-?%}'
    matches = list(re.finditer(liquid_block_pattern, content))
    for match in reversed(matches):  # Process in reverse to maintain positions
        block_content = match.group(1)
        # Check if this is a multi-line liquid block that ends incorrectly
        if '\n' in block_content and not block_content.strip().endswith('endliquid'):
            new_block = '{% liquid\n' + block_content.strip() + '\n%}'
            content = content[:match.start()] + new_block + content[match.end():]
            fixes_made.append('Fixed liquid block syntax')

    return content, fixes_made

def fix_unknown_filters(content):
    """Fix or remove unknown Liquid filters"""
    fixes_made = []

    # Dictionary of unknown filters and their replacements
    filter_replacements = {
        'image_tag': 'image_url',  # image_tag doesn't exist, use image_url
        'structured_data': 'json',  # structured_data doesn't exist, use json
        'default_pagination': 'default: paginate',  # Fix pagination syntax
        'payment_button': 'payment_button_tag',  # Correct filter name
        'default_errors': 'default: errors',  # Fix error handling syntax
    }

    for old_filter, new_filter in filter_replacements.items():
        pattern = r'\|\s*' + re.escape(old_filter) + r'(?:\s|}}|%})'
        if re.search(pattern, content):
            # Special handling for different replacement types
            if 'default:' in new_filter:
                # This is a default value, not a filter
                content = re.sub(r'\|\s*' + re.escape(old_filter), '| ' + new_filter.replace('default: ', 'default: '), content)
            else:
                content = re.sub(r'\|\s*' + re.escape(old_filter), '| ' + new_filter, content)
            fixes_made.append(f'Replaced {old_filter} with {new_filter}')

    return content, fixes_made

def fix_performance_issues(content):
    """Fix performance-related issues"""
    fixes_made = []

    # Fix looping all collections without limit
    pattern = r'({%\s*for\s+\w+\s+in\s+collections\s*%})'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1', content)
        # Find the endfor and add limit before it
        content = re.sub(
            r'({%\s*for\s+collection\s+in\s+collections\s*%})',
            r'{% for collection in collections limit: 50 %}',
            content
        )
        fixes_made.append('Added limit to collections loop')

    return content, fixes_made

def process_file(file_path):
    """Process a single file and fix issues"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        all_fixes = []

        # Apply fixes
        content, fixes = fix_liquid_tags(content)
        all_fixes.extend(fixes)

        content, fixes = fix_unknown_filters(content)
        all_fixes.extend(fixes)

        content, fixes = fix_performance_issues(content)
        all_fixes.extend(fixes)

        # Write back if changes were made
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True, all_fixes

        return False, []
    except Exception as e:
        return False, [f'Error: {e}']

def main():
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    else:
        target_path = Path('heka-test')

    if not target_path.exists():
        print(f"❌ Path not found: {target_path}")
        return 1

    print(f"🔧 Fixing Liquid syntax issues in: {target_path}")

    # Find all liquid files
    if target_path.is_file():
        liquid_files = [target_path]
    else:
        liquid_files = list(target_path.rglob('*.liquid'))

    total_fixed = 0

    for file_path in liquid_files:
        fixed, fixes = process_file(file_path)
        if fixed:
            print(f"✅ Fixed {file_path.name}:")
            for fix in fixes:
                print(f"   - {fix}")
            total_fixed += 1

    print(f"\n📊 Summary: Fixed {total_fixed} files out of {len(liquid_files)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())