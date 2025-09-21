# Shopify Theme Asset Dependency Mapping

**Comprehensive guide to managing theme file dependencies and preventing missing asset errors**

## Overview

Asset dependencies in Shopify themes create a web of interconnected files that must be properly managed to prevent runtime errors. This guide provides tools and methodologies for mapping, tracking, and validating all theme dependencies.

## Common Dependency Patterns

### Section Dependencies

```liquid
<!-- sections/header.liquid -->
{% render 'icon-svg', icon: 'menu' %}    <!-- Requires: snippets/icon-svg.liquid -->
{% render 'navigation-menu' %}           <!-- Requires: snippets/navigation-menu.liquid -->

{{ 'header.css' | asset_url | stylesheet_tag }}  <!-- Requires: assets/header.css -->
```

### Block Dependencies

```liquid
<!-- blocks/video-text.liquid -->
{% render 'responsive-image', image: block.settings.image %}  <!-- Snippet dependency -->
{% render 'video-player', video: block.settings.video %}     <!-- Snippet dependency -->

{{ 'video-block.js' | asset_url | script_tag }}  <!-- Asset dependency -->
```

### Snippet Dependencies

```liquid
<!-- snippets/product-card.liquid -->
{% render 'price-display', product: product %}     <!-- Nested snippet -->
{% render 'product-media', product: product %}     <!-- Nested snippet -->
{{ 'product-card.css' | asset_url | stylesheet_tag }}  <!-- Asset dependency -->
```

## Dependency Mapping System

### JSON Dependency Manifest

Each major component should have a corresponding dependency manifest:

```json
{
  "component_name": "advanced_video_text",
  "component_type": "block",
  "file_path": "blocks/advanced_video_text.liquid",
  "dependencies": {
    "required_snippets": [
      {
        "name": "block-video-text",
        "path": "snippets/block-video-text.liquid",
        "description": "Main implementation logic for video+text block"
      }
    ],
    "optional_snippets": [
      {
        "name": "responsive-image",
        "path": "snippets/responsive-image.liquid",
        "description": "Enhanced image rendering with srcset support"
      }
    ],
    "required_assets": [],
    "optional_assets": [
      {
        "name": "video-player.js",
        "path": "assets/video-player.js",
        "description": "Enhanced video controls and functionality"
      }
    ],
    "schema_dependencies": [
      {
        "setting_id": "video_file",
        "type": "video",
        "required": true,
        "description": "Main video content"
      },
      {
        "setting_id": "video_poster",
        "type": "image_picker",
        "required": false,
        "description": "Video poster image"
      }
    ],
    "translation_keys": [
      "sections.video_text.name",
      "sections.video_text.settings.heading.label"
    ]
  },
  "version": "1.0.0",
  "last_updated": "2025-01-21"
}
```

### Dependency Validation Script

```python
#!/usr/bin/env python3
"""
Shopify Theme Dependency Validator
Validates all theme dependencies against manifest files
"""

import json
import os
import sys
from pathlib import Path

def validate_dependencies(theme_path, manifest_path):
    """Validate theme dependencies against manifest files"""

    theme_dir = Path(theme_path)
    manifest_dir = Path(manifest_path)

    errors = []
    warnings = []

    # Load all dependency manifests
    manifests = []
    for manifest_file in manifest_dir.glob('*.json'):
        with open(manifest_file) as f:
            manifests.append(json.load(f))

    for manifest in manifests:
        component_name = manifest['component_name']

        # Check required snippets
        for snippet in manifest['dependencies'].get('required_snippets', []):
            snippet_path = theme_dir / snippet['path']
            if not snippet_path.exists():
                errors.append(f"Missing required snippet: {snippet['path']} for {component_name}")

        # Check optional snippets
        for snippet in manifest['dependencies'].get('optional_snippets', []):
            snippet_path = theme_dir / snippet['path']
            if not snippet_path.exists():
                warnings.append(f"Missing optional snippet: {snippet['path']} for {component_name}")

        # Check required assets
        for asset in manifest['dependencies'].get('required_assets', []):
            asset_path = theme_dir / asset['path']
            if not asset_path.exists():
                errors.append(f"Missing required asset: {asset['path']} for {component_name}")

        # Check translation keys
        locale_file = theme_dir / 'locales' / 'en.default.json'
        if locale_file.exists():
            with open(locale_file) as f:
                translations = json.load(f)

            for key in manifest['dependencies'].get('translation_keys', []):
                if not check_translation_key(translations, key):
                    warnings.append(f"Missing translation key: {key} for {component_name}")

    return errors, warnings

def check_translation_key(translations, key):
    """Check if a nested translation key exists"""
    keys = key.split('.')
    current = translations

    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 validate-dependencies.py <theme_path> <manifest_path>")
        sys.exit(1)

    theme_path = sys.argv[1]
    manifest_path = sys.argv[2]

    errors, warnings = validate_dependencies(theme_path, manifest_path)

    if errors:
        print("❌ DEPENDENCY ERRORS:")
        for error in errors:
            print(f"  • {error}")
        print()

    if warnings:
        print("⚠️  DEPENDENCY WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
        print()

    if not errors and not warnings:
        print("✅ All dependencies validated successfully!")

    sys.exit(1 if errors else 0)
```

## Safe Theme Integration Process

### Step 1: Dependency Analysis

Before copying any section/block to a new theme:

1. **Generate Dependency Report**
   ```bash
   python3 scripts/analyze-dependencies.py sections/video-text.liquid
   ```

2. **Check Existing Dependencies**
   ```bash
   python3 scripts/validate-dependencies.py /path/to/target/theme manifests/
   ```

### Step 2: Safe Copy Process

```bash
#!/bin/bash
# Safe theme component copy script

COMPONENT_FILE="$1"
TARGET_THEME="$2"
MANIFEST_DIR="manifests"

# 1. Parse component type and name
COMPONENT_TYPE=$(dirname "$COMPONENT_FILE")
COMPONENT_NAME=$(basename "$COMPONENT_FILE" .liquid)

# 2. Find dependency manifest
MANIFEST_FILE="$MANIFEST_DIR/${COMPONENT_NAME}-dependencies.json"

if [[ ! -f "$MANIFEST_FILE" ]]; then
    echo "⚠️  No dependency manifest found for $COMPONENT_NAME"
    echo "   Creating basic analysis..."
    # Auto-generate basic manifest
fi

# 3. Copy all dependencies
echo "📋 Copying dependencies for $COMPONENT_NAME..."

# Copy main component
cp "$COMPONENT_FILE" "$TARGET_THEME/$COMPONENT_TYPE/"

# Copy required snippets
jq -r '.dependencies.required_snippets[].path' "$MANIFEST_FILE" | while read -r snippet; do
    if [[ -f "$snippet" ]]; then
        cp "$snippet" "$TARGET_THEME/snippets/"
        echo "✅ Copied required snippet: $snippet"
    else
        echo "❌ Missing required snippet: $snippet"
    fi
done

# Copy optional snippets (with confirmation)
jq -r '.dependencies.optional_snippets[].path' "$MANIFEST_FILE" | while read -r snippet; do
    if [[ -f "$snippet" ]]; then
        read -p "Copy optional snippet $snippet? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp "$snippet" "$TARGET_THEME/snippets/"
            echo "✅ Copied optional snippet: $snippet"
        fi
    fi
done

# 4. Validate target theme
echo "🔍 Validating target theme..."
python3 scripts/validate-dependencies.py "$TARGET_THEME" "$MANIFEST_DIR"
```

## Dependency Manifests Library

### Header Dependencies

```json
{
  "component_name": "header",
  "component_type": "section",
  "file_path": "sections/header.liquid",
  "dependencies": {
    "required_snippets": [
      {
        "name": "icon-svg",
        "path": "snippets/icon-svg.liquid",
        "description": "SVG icon rendering system"
      }
    ],
    "optional_snippets": [
      {
        "name": "navigation-menu",
        "path": "snippets/navigation-menu.liquid",
        "description": "Enhanced navigation with dropdowns"
      }
    ],
    "required_assets": [
      {
        "name": "header.css",
        "path": "assets/header.css",
        "description": "Header styling and layout"
      }
    ],
    "translation_keys": [
      "general.accessibility.skip_to_content",
      "general.search.placeholder",
      "layout.header.menu"
    ]
  }
}
```

### Footer Dependencies

```json
{
  "component_name": "footer",
  "component_type": "section",
  "file_path": "sections/footer.liquid",
  "dependencies": {
    "required_snippets": [
      {
        "name": "icon-svg",
        "path": "snippets/icon-svg.liquid",
        "description": "Social media and payment icons"
      }
    ],
    "optional_snippets": [
      {
        "name": "newsletter-form",
        "path": "snippets/newsletter-form.liquid",
        "description": "Newsletter signup form"
      }
    ],
    "required_assets": [
      {
        "name": "footer.css",
        "path": "assets/footer.css",
        "description": "Footer styling and responsive layout"
      }
    ],
    "translation_keys": [
      "layout.footer.newsletter_heading",
      "layout.footer.social_media",
      "layout.footer.payment_methods"
    ]
  }
}
```

### Video-Text Block Dependencies

```json
{
  "component_name": "advanced_video_text",
  "component_type": "block",
  "file_path": "blocks/advanced_video_text.liquid",
  "dependencies": {
    "required_snippets": [
      {
        "name": "block-video-text",
        "path": "snippets/block-video-text.liquid",
        "description": "Main implementation with enhanced features"
      }
    ],
    "optional_snippets": [
      {
        "name": "responsive-image",
        "path": "snippets/responsive-image.liquid",
        "description": "Optimized image rendering for video posters"
      }
    ],
    "required_assets": [],
    "schema_dependencies": [
      {
        "setting_id": "video_file",
        "type": "video",
        "required": true
      },
      {
        "setting_id": "heading",
        "type": "text",
        "required": false
      },
      {
        "setting_id": "layout_style",
        "type": "select",
        "required": false
      }
    ],
    "translation_keys": [
      "sections.video_text.name",
      "sections.video_text.settings.content.content",
      "sections.video_text.settings.layout.content"
    ]
  }
}
```

## Automated Dependency Discovery

### Liquid File Parser

```python
import re
from pathlib import Path

class LiquidDependencyParser:
    def __init__(self):
        self.render_pattern = r"{% render ['\"]([^'\"]+)['\"]"
        self.asset_pattern = r"['\"]([^'\"]+\.(css|js|png|jpg|jpeg|svg|woff|woff2))['\"] \| asset_url"
        self.setting_pattern = r"(\w+\.settings\.\w+)"

    def parse_file(self, file_path):
        """Parse a Liquid file for dependencies"""
        with open(file_path, 'r') as f:
            content = f.read()

        dependencies = {
            'snippets': self.find_snippets(content),
            'assets': self.find_assets(content),
            'settings': self.find_settings(content)
        }

        return dependencies

    def find_snippets(self, content):
        """Find all rendered snippets"""
        matches = re.findall(self.render_pattern, content)
        return list(set(matches))

    def find_assets(self, content):
        """Find all referenced assets"""
        matches = re.findall(self.asset_pattern, content)
        return list(set([match[0] for match in matches]))

    def find_settings(self, content):
        """Find all referenced settings"""
        matches = re.findall(self.setting_pattern, content)
        return list(set(matches))

# Usage example
parser = LiquidDependencyParser()
deps = parser.parse_file('sections/header.liquid')
print(f"Snippets: {deps['snippets']}")
print(f"Assets: {deps['assets']}")
print(f"Settings: {deps['settings']}")
```

## Best Practices

### 🎯 **Proactive Dependency Management**

1. **Create manifests for all major components**
2. **Validate dependencies before copying**
3. **Use automated discovery tools**
4. **Maintain up-to-date documentation**

### 🔧 **Development Workflow Integration**

1. **Pre-commit hooks validate dependencies**
2. **CI/CD pipelines check for missing assets**
3. **Development tools auto-suggest dependencies**
4. **Theme packages include manifest files**

### 📊 **Monitoring and Maintenance**

1. **Regular dependency audits**
2. **Automated manifest updates**
3. **Dependency change tracking**
4. **Performance impact analysis**

---

*This dependency mapping system prevents the common "missing snippet" and "asset not found" errors that plague Shopify theme development while providing clear documentation for component integration.*