#!/usr/bin/env python3
"""
Comprehensive Schema Integrity Scanner
Finds undefined settings, invalid presets, and schema inconsistencies
"""

import json
import re
import sys
from pathlib import Path

def extract_schema_from_liquid(file_path):
    """Extract JSON schema from liquid file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find schema block
        schema_match = re.search(r'{% schema %}(.*?){% endschema %}', content, re.DOTALL)
        if not schema_match:
            return None, None

        schema_json = schema_match.group(1).strip()
        return json.loads(schema_json), content

    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None, None

def extract_liquid_settings_usage(content):
    """Extract all setting IDs used in Liquid code"""
    # Find all settings patterns: block.settings.ID, section.settings.ID
    # Exclude global settings.ID as those are theme-level settings
    patterns = [
        r'block\.settings\.([a-zA-Z_][a-zA-Z0-9_]*)',     # block.settings.ID
        r'section\.settings\.([a-zA-Z_][a-zA-Z0-9_]*)',   # section.settings.ID
    ]

    all_matches = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        all_matches.update(matches)

    return all_matches

def validate_schema_integrity(file_path):
    """Comprehensive schema validation"""
    print(f"🔍 Scanning: {file_path.name}")
    print("=" * 50)

    # Check file type - snippets and layouts don't need schemas
    if '/snippets/' in str(file_path):
        print("📄 Snippet file - schemas not required")
        print("✅ Snippet validation skipped (expected behavior)")
        return True

    if '/layouts/' in str(file_path) or '/layout/' in str(file_path) or file_path.name.endswith(('theme.liquid', 'checkout.liquid', 'gift_card.liquid')):
        print("🏗️  Layout file - schemas not required")
        print("✅ Layout validation skipped (expected behavior)")
        return True

    # Templates may not have schemas (legacy)
    if '/templates/' in str(file_path):
        schema, content = extract_schema_from_liquid(file_path)
        if not schema:
            print("📋 Template file without schema (legacy format)")
            print("✅ Template validation skipped (legacy behavior)")
            return True

    # Legacy files may have incomplete schemas
    is_legacy = '/legacy/' in str(file_path)
    if is_legacy:
        print("⚠️  Legacy file detected - relaxed validation mode")

    schema, content = extract_schema_from_liquid(file_path)
    if not schema:
        print("❌ No valid schema found")
        return False

    errors = []
    warnings = []

    # 1. Extract all defined settings
    defined_settings = {}
    for setting in schema.get('settings', []):
        setting_id = setting.get('id')
        if setting_id:
            defined_settings[setting_id] = setting

    print(f"📊 Found {len(defined_settings)} defined settings")

    # 2. Extract settings used in Liquid code
    used_settings = extract_liquid_settings_usage(content)
    print(f"📊 Found {len(used_settings)} settings used in Liquid")

    # 3. Check for undefined settings used in Liquid
    undefined_settings = used_settings - set(defined_settings.keys())

    # Check if undefined settings are actually block settings
    if undefined_settings and 'blocks' in schema:
        block_settings = set()
        for block in schema.get('blocks', []):
            for block_setting in block.get('settings', []):
                if block_setting.get('id'):
                    block_settings.add(block_setting.get('id'))

        # Remove block settings from undefined settings
        undefined_settings = undefined_settings - block_settings

    if undefined_settings:
        if is_legacy:
            warnings.extend([f"Legacy file: Setting '{s}' used but not defined in schema" for s in undefined_settings])
        else:
            errors.extend([f"Setting '{s}' used in Liquid but not defined in schema" for s in undefined_settings])

    # 4. Check for unused settings (potential cleanup)
    unused_settings = set(defined_settings.keys()) - used_settings
    if unused_settings:
        warnings.extend([f"Setting '{s}' defined but never used in Liquid" for s in unused_settings])

    # 5. Validate presets
    for preset_idx, preset in enumerate(schema.get('presets', [])):
        preset_name = preset.get('name', f'Preset {preset_idx + 1}')
        preset_settings = preset.get('settings', {})

        # Check for undefined settings in presets
        for setting_id in preset_settings.keys():
            if setting_id not in defined_settings:
                errors.append(f"Preset '{preset_name}' uses undefined setting '{setting_id}'")

        # Check richtext presets
        for setting_id, value in preset_settings.items():
            if setting_id in defined_settings:
                setting_def = defined_settings[setting_id]
                setting_type = setting_def.get('type')

                if setting_type == 'richtext' and isinstance(value, str) and value.strip():
                    # Must contain HTML tags
                    html_pattern = r'^<[a-zA-Z][^>]*>.*<\/[a-zA-Z][^>]*>$|^<[a-zA-Z][^>]*\/>$'
                    if not re.match(html_pattern, value.strip()):
                        errors.append(f"Preset '{preset_name}' richtext setting '{setting_id}' must contain HTML: '{value}'")

                elif setting_type == 'range':
                    # Check range values are within bounds
                    min_val = setting_def.get('min', 0)
                    max_val = setting_def.get('max', 100)
                    if not (min_val <= value <= max_val):
                        errors.append(f"Preset '{preset_name}' range setting '{setting_id}' value {value} outside range [{min_val}, {max_val}]")

                elif setting_type == 'select':
                    # Check select values are valid options
                    valid_options = [opt.get('value') for opt in setting_def.get('options', [])]
                    if value not in valid_options:
                        errors.append(f"Preset '{preset_name}' select setting '{setting_id}' value '{value}' not in valid options: {valid_options}")

    # 6. Validate range settings
    for setting_id, setting in defined_settings.items():
        if setting.get('type') == 'range':
            min_val = setting.get('min', 0)
            max_val = setting.get('max', 100)
            step = setting.get('step', 1)

            # Range validation formula: (max - min) / step <= 101
            if step > 0:
                range_calc = (max_val - min_val) / step
                if range_calc > 101:
                    errors.append(f"Range setting '{setting_id}' violates validation: ({max_val} - {min_val}) / {step} = {range_calc:.2f} > 101")

    # 7. Check for duplicate setting IDs
    setting_ids = [s.get('id') for s in schema.get('settings', []) if s.get('id')]
    duplicate_ids = [id for id in set(setting_ids) if setting_ids.count(id) > 1]
    if duplicate_ids:
        errors.extend([f"Duplicate setting ID: '{id}'" for id in duplicate_ids])

    # 8. Check for required fields
    for setting in schema.get('settings', []):
        setting_type = setting.get('type')
        setting_id = setting.get('id')

        # Header settings don't need IDs or labels
        if setting_type == 'header':
            if not setting.get('content'):
                warnings.append(f"Header setting missing 'content' field")
            continue

        # All other settings need IDs
        if not setting_id:
            errors.append(f"Non-header setting missing required 'id' field: {setting}")
        if not setting_type:
            errors.append(f"Setting '{setting_id or 'unknown'}' missing required 'type' field")
        if not setting.get('label'):
            warnings.append(f"Setting '{setting_id or 'unknown'}' missing 'label' field")

    # Report results
    print("\n📋 Validation Results")
    print("-" * 30)

    if errors:
        print(f"❌ Found {len(errors)} ERRORS:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    if warnings:
        print(f"⚠️  Found {len(warnings)} WARNINGS:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    if not errors and not warnings:
        print("✅ Schema integrity is perfect!")

    # Summary
    print(f"\n📊 Summary:")
    print(f"  • Settings defined: {len(defined_settings)}")
    print(f"  • Settings used: {len(used_settings)}")
    print(f"  • Presets: {len(schema.get('presets', []))}")
    print(f"  • Errors: {len(errors)}")
    print(f"  • Warnings: {len(warnings)}")

    # Legacy files pass if they have no critical errors (only warnings allowed)
    if is_legacy and len(errors) == 0:
        print("✅ Legacy file validation passed (warnings acceptable)")
        return True

    return len(errors) == 0

def scan_directory(directory_path):
    """Scan all .liquid files in a directory recursively"""
    liquid_files = list(directory_path.rglob("*.liquid"))

    if not liquid_files:
        print(f"❌ No .liquid files found in {directory_path}")
        return False

    print(f"📄 Found {len(liquid_files)} liquid files")

    total_errors = 0
    files_with_errors = 0

    for file_path in liquid_files:
        print(f"\n{'='*60}")
        success = validate_schema_integrity(file_path)
        if not success:
            files_with_errors += 1
            total_errors += 1

    print(f"\n{'='*60}")
    print("🎯 Directory Scan Summary")
    print("=" * 30)
    print(f"📁 Files scanned: {len(liquid_files)}")
    print(f"❌ Files with errors: {files_with_errors}")
    print(f"✅ Files passed: {len(liquid_files) - files_with_errors}")

    if files_with_errors == 0:
        print("🎉 All files passed schema integrity validation!")
        return True
    else:
        print(f"🚨 {files_with_errors} file(s) failed validation!")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive Schema Integrity Scanner for Shopify Liquid files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scan-schema-integrity.py                                    # Scan default video-system.liquid
  python3 scan-schema-integrity.py file.liquid                        # Scan single file
  python3 scan-schema-integrity.py path/to/blocks/                     # Scan directory
  python3 scan-schema-integrity.py shopify-liquid-guides/code-library/ # Scan entire code library
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to liquid file or directory to scan'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Scan entire code library'
    )

    args = parser.parse_args()

    print("🔍 Comprehensive Schema Integrity Scanner")
    print("=" * 50)

    # Determine target path
    if args.all:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        target_path = project_root / "shopify-liquid-guides" / "code-library"
        print(f"🌍 Scanning entire code library including /custom directories: {target_path}")
    elif args.path:
        target_path = Path(args.path)
    else:
        # Default to video-system.liquid
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        target_path = project_root / "shopify-liquid-guides" / "code-library" / "blocks" / "advanced" / "video-system.liquid"
        print(f"🎯 Scanning default file: {target_path.name}")

    if not target_path.exists():
        print(f"❌ Path not found: {target_path}")
        return 1

    # Scan file or directory
    if target_path.is_file():
        success = validate_schema_integrity(target_path)
        if success:
            print("\n🎉 Schema integrity validation PASSED!")
            return 0
        else:
            print("\n🚨 Schema integrity validation FAILED!")
            return 1
    elif target_path.is_dir():
        success = scan_directory(target_path)
        return 0 if success else 1
    else:
        print(f"❌ Invalid path: {target_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())