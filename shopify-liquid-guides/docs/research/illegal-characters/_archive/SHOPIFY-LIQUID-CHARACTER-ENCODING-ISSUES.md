# 🔤 Shopify Liquid Character Encoding Issues & Solutions

**Comprehensive Guide to HTML Entity Encoding Problems and Unicode Compatibility Issues in Shopify Liquid Templates**

*Updated: January 2025 - Based on comprehensive research and validation analysis*

---

## 🚨 **Critical Character Encoding Problems**

### **1. HTML Entity Encoding Issues That Break Liquid Parsing**

#### **Problem: HTML Entities in Liquid Variables**
```liquid
❌ BREAKS LIQUID PARSING:
{{ product.title | replace: '&amp;', '&' }}
{{ settings.custom_text | append: '&nbsp;' }}
{{ collection.description | truncate: 50, '&hellip;' }}

✅ CORRECT PATTERNS:
{{ product.title | replace: '&', '&' }}
{{ settings.custom_text | append: ' ' }}
{{ collection.description | truncate: 50, '...' }}
```

**Why This Breaks:**
- Liquid parser expects plain text in variable operations
- HTML entities (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`) confuse the parser
- Results in `Liquid Error` or `Template Parse Error`

#### **Problem: HTML Entities in Liquid Filters**
```liquid
❌ PARSING ERRORS:
{{ 'Hello &amp; World' | split: '&amp;' }}
{{ product.tags | join: ' &middot; ' }}
{{ text | replace: '&lt;', '<' }}

✅ SAFE ALTERNATIVES:
{{ 'Hello & World' | split: '&' }}
{{ product.tags | join: ' • ' }}
{{ text | replace: '<', '' }}
```

#### **Problem: HTML Entities in Schema JSON**
```json
❌ INVALID SCHEMA (Causes FileSaveError):
{
  "name": "Text &amp; Media",
  "settings": [
    {
      "label": "Heading &mdash; Optional",
      "default": "Welcome &amp; Enjoy"
    }
  ]
}

✅ VALID SCHEMA:
{
  "name": "Text & Media",
  "settings": [
    {
      "label": "Heading — Optional",
      "default": "Welcome & Enjoy"
    }
  ]
}
```

### **2. Unicode Character Compatibility Issues**

#### **Problem: Non-ASCII Characters in Variable Names**
```liquid
❌ CAUSES PARSING ERRORS:
{% assign ñame = 'value' %}
{% assign café = product.title %}
{% for tést in collection.products %}

✅ ASCII-ONLY VARIABLE NAMES:
{% assign name = 'value' %}
{% assign cafe = product.title %}
{% for test in collection.products %}
```

#### **Problem: Unicode in Liquid Logic**
```liquid
❌ UNICODE COMPARISON ISSUES:
{% if product.title contains 'café' %}
{% unless customer.name == 'José' %}

✅ SAFE PATTERNS:
{% if product.title contains 'cafe' %}
{% unless customer.name == 'Jose' %}

✅ OR USE FILTERS:
{% if product.title | downcase contains 'café' | downcase %}
```

#### **Problem: Unicode in File Names and URLs**
```liquid
❌ UNICODE IN ASSET REFERENCES:
{{ 'café-styles.css' | asset_url }}
{% render 'ñav-menu' %}

✅ ASCII-SAFE NAMING:
{{ 'cafe-styles.css' | asset_url }}
{% render 'nav-menu' %}
```

### **3. Character Encoding in Meta Tags and Head Elements**

#### **Problem: Inconsistent Character Set Declaration**
```liquid
❌ MISSING OR WRONG CHARSET:
<meta http-equiv="Content-Type" content="text/html">
<meta charset="ISO-8859-1">

✅ CORRECT UTF-8 DECLARATION:
<meta charset="utf-8">
```

#### **Problem: Unicode in Meta Content**
```liquid
❌ UNESCAPED UNICODE IN META:
<meta name="description" content="{{ page.description }}">
<meta property="og:title" content="{{ product.title }}">

✅ PROPERLY ESCAPED:
<meta name="description" content="{{ page.description | escape }}">
<meta property="og:title" content="{{ product.title | escape }}">
```

#### **Problem: Language and Locale Issues**
```liquid
❌ WRONG LANGUAGE ATTRIBUTES:
<html lang="en" dir="ltr">
<!-- Content in Spanish/French but lang still "en" -->

✅ DYNAMIC LANGUAGE HANDLING:
<html lang="{{ localization.language.iso_code }}" dir="{{ localization.language.direction }}">
```

### **4. Special Characters in Alt Text and Title Attributes**

#### **Problem: Unescaped Special Characters**
```liquid
❌ BREAKS HTML ATTRIBUTES:
<img alt="{{ product.title }}" title="{{ product.description }}">
<input placeholder="{{ 'Search "products"' }}">

✅ PROPERLY ESCAPED:
<img alt="{{ product.title | escape }}" title="{{ product.description | escape }}">
<input placeholder="{{ 'Search products' }}">
```

#### **Problem: Quote Characters in Attributes**
```liquid
❌ ATTRIBUTE PARSING ERRORS:
<div title="{{ block.settings.text }}">
<!-- If text contains: She said "Hello world" -->

✅ ESCAPE ALL ATTRIBUTE VALUES:
<div title="{{ block.settings.text | escape }}">
```

#### **Problem: Newlines and Special Whitespace**
```liquid
❌ BREAKS ATTRIBUTE VALUES:
<button aria-label="{{ section.settings.description }}">
<!-- If description contains line breaks -->

✅ STRIP WHITESPACE:
<button aria-label="{{ section.settings.description | strip | escape }}">
```

### **5. UTF-8 vs ASCII Compatibility Problems**

#### **Problem: UTF-8 BOM (Byte Order Mark)**
```
❌ UTF-8 BOM CAUSES ISSUES:
EF BB BF at start of .liquid files
Results in: Unexpected character at beginning of template

✅ UTF-8 WITHOUT BOM:
Save all .liquid files as UTF-8 without BOM
```

#### **Problem: Mixed Character Encodings**
```liquid
❌ MIXED ENCODING ISSUES:
<!-- File saved as Windows-1252 -->
{{ 'Price: £19.99' | money }}
<!-- Displays as: Price: Â£19.99 -->

✅ CONSISTENT UTF-8:
<!-- All files UTF-8 encoded -->
{{ 'Price: £19.99' | money }}
<!-- Displays correctly: Price: £19.99 -->
```

#### **Problem: ASCII-Only Filter Issues**
```liquid
❌ UNICODE BREAKS SOME FILTERS:
{{ 'café-product' | handleize }}
<!-- May not handle accents correctly -->

✅ NORMALIZE BEFORE FILTERING:
{{ 'cafe-product' | handleize }}
<!-- Or use Unicode-aware handling -->
```

---

## 🛠️ **Systematic Fix Strategies**

### **Strategy 1: Input Sanitization**

#### **HTML Entity Prevention**
```liquid
{% comment %} Clean HTML entities from user input {% endcomment %}
{% assign clean_text = user_input
  | replace: '&amp;', '&'
  | replace: '&lt;', '<'
  | replace: '&gt;', '>'
  | replace: '&quot;', '"'
  | replace: '&#39;', "'" %}
```

#### **Unicode Normalization**
```liquid
{% comment %} Normalize Unicode for safe processing {% endcomment %}
{% assign safe_handle = product.title
  | replace: 'á', 'a'
  | replace: 'é', 'e'
  | replace: 'í', 'i'
  | replace: 'ó', 'o'
  | replace: 'ú', 'u'
  | handleize %}
```

### **Strategy 2: Output Escaping**

#### **Universal Escape Pattern**
```liquid
{% comment %} Always escape user-controllable content {% endcomment %}
<h1>{{ page.title | escape }}</h1>
<p>{{ article.content | strip_html | truncate: 160 | escape }}</p>
<input value="{{ form.email.value | escape }}">
<div data-product="{{ product.title | escape }}">
```

#### **Attribute-Safe Output**
```liquid
{% comment %} Special handling for HTML attributes {% endcomment %}
{% assign safe_title = product.title | escape | replace: '"', '&quot;' %}
<img alt="{{ safe_title }}" title="{{ safe_title }}">
```

### **Strategy 3: Character Set Management**

#### **Template Header Pattern**
```liquid
{% comment %} Standard UTF-8 template header {% endcomment %}
<!DOCTYPE html>
<html lang="{{ localization.language.iso_code }}" dir="{{ localization.language.direction }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Rest of head content -->
</head>
```

#### **Content-Type Headers**
```liquid
{% comment %} Ensure proper content type {% endcomment %}
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
```

### **Strategy 4: Schema Validation**

#### **Safe Schema Pattern**
```json
{
  "name": "Safe Schema Example",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Default text without special characters",
      "info": "Avoid HTML entities and special quotes"
    },
    {
      "type": "textarea",
      "id": "description",
      "label": "Description",
      "placeholder": "Enter description here..."
    }
  ]
}
```

---

## 🔍 **Automated Validation Patterns**

### **Character Encoding Validator**

```python
import re
from typing import List, Dict, Tuple

class CharacterEncodingValidator:
    """Validate Shopify Liquid templates for character encoding issues"""

    def __init__(self):
        self.issues = []

    # HTML Entity Patterns That Break Liquid
    HTML_ENTITY_IN_LIQUID = [
        {
            'pattern': r'{{\s*[^}]*&(?:amp|lt|gt|quot|#39);[^}]*}}',
            'message': 'HTML entity in Liquid output - breaks parsing',
            'severity': 'CRITICAL',
            'fix': 'Replace HTML entities with actual characters'
        },
        {
            'pattern': r'{%\s*[^%]*&(?:amp|lt|gt|quot|#39);[^%]*%}',
            'message': 'HTML entity in Liquid tag - breaks parsing',
            'severity': 'CRITICAL',
            'fix': 'Replace HTML entities with actual characters'
        }
    ]

    # Unicode Variable Name Issues
    UNICODE_VARIABLE_PATTERNS = [
        {
            'pattern': r'{%\s*assign\s+[^\s]*[^\x00-\x7F][^\s]*\s*=',
            'message': 'Non-ASCII characters in variable name',
            'severity': 'ERROR',
            'fix': 'Use ASCII-only characters in variable names'
        },
        {
            'pattern': r'{%\s*for\s+[^\s]*[^\x00-\x7F][^\s]*\s+in',
            'message': 'Non-ASCII characters in loop variable',
            'severity': 'ERROR',
            'fix': 'Use ASCII-only characters in loop variables'
        }
    ]

    # Unescaped Output Patterns
    UNESCAPED_OUTPUT_PATTERNS = [
        {
            'pattern': r'{{\s*(?:settings|customer|form|article|product|collection|page)\.[^}]*(?<!\|\s*escape)\s*}}',
            'message': 'User content output without escape filter',
            'severity': 'ERROR',
            'fix': 'Add | escape filter to prevent XSS and encoding issues'
        }
    ]

    # Meta Tag Encoding Issues
    META_TAG_PATTERNS = [
        {
            'pattern': r'<meta\s+name="[^"]*"\s+content="\s*{{\s*[^}]*\s*}}\s*">',
            'message': 'Unescaped Liquid in meta content',
            'severity': 'WARNING',
            'fix': 'Add | escape filter to meta content'
        },
        {
            'pattern': r'<meta\s+charset=["\']?(?!utf-8)[^"\'>\s]+',
            'message': 'Non-UTF-8 charset declaration',
            'severity': 'WARNING',
            'fix': 'Use UTF-8 charset: <meta charset="utf-8">'
        }
    ]

    # Attribute Encoding Issues
    ATTRIBUTE_PATTERNS = [
        {
            'pattern': r'(?:alt|title|placeholder|aria-label)="\s*{{\s*[^}]*(?<!\|\s*escape)\s*}}\s*"',
            'message': 'Unescaped Liquid in HTML attribute',
            'severity': 'ERROR',
            'fix': 'Add | escape filter to attribute values'
        }
    ]

    def validate_file(self, file_path: str, content: str) -> List[Dict]:
        """Validate a single file for character encoding issues"""
        issues = []

        # Check HTML entities in Liquid
        for pattern_info in self.HTML_ENTITY_IN_LIQUID:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'type': 'html_entity_in_liquid',
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'match': match.group(0),
                    'fix': pattern_info['fix']
                })

        # Check Unicode in variable names
        for pattern_info in self.UNICODE_VARIABLE_PATTERNS:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'type': 'unicode_variable_name',
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'match': match.group(0),
                    'fix': pattern_info['fix']
                })

        # Check unescaped output
        for pattern_info in self.UNESCAPED_OUTPUT_PATTERNS:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'type': 'unescaped_output',
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'match': match.group(0),
                    'fix': pattern_info['fix']
                })

        # Check meta tag issues
        for pattern_info in self.META_TAG_PATTERNS:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'type': 'meta_tag_encoding',
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'match': match.group(0),
                    'fix': pattern_info['fix']
                })

        # Check attribute issues
        for pattern_info in self.ATTRIBUTE_PATTERNS:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'file': file_path,
                    'line': self._get_line_number(content, match.start()),
                    'type': 'attribute_encoding',
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'match': match.group(0),
                    'fix': pattern_info['fix']
                })

        return issues

    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a position in content"""
        return content[:position].count('\n') + 1

    def validate_schema_encoding(self, schema_content: str, file_path: str) -> List[Dict]:
        """Validate JSON schema for encoding issues"""
        issues = []

        # Check for HTML entities in schema
        html_entity_pattern = r'&(?:amp|lt|gt|quot|#39|[a-zA-Z]+);'
        matches = re.finditer(html_entity_pattern, schema_content)

        for match in matches:
            issues.append({
                'file': file_path,
                'line': self._get_line_number(schema_content, match.start()),
                'type': 'html_entity_in_schema',
                'severity': 'CRITICAL',
                'message': f'HTML entity {match.group(0)} in schema - will cause FileSaveError',
                'match': match.group(0),
                'fix': 'Replace HTML entity with actual character'
            })

        # Check for curly quotes and special characters
        special_char_pattern = r'[""''…–—]'
        matches = re.finditer(special_char_pattern, schema_content)

        for match in matches:
            issues.append({
                'file': file_path,
                'line': self._get_line_number(schema_content, match.start()),
                'type': 'special_char_in_schema',
                'severity': 'WARNING',
                'message': f'Special character {match.group(0)} in schema - may cause encoding issues',
                'match': match.group(0),
                'fix': 'Replace with ASCII equivalent'
            })

        return issues
```

### **Integration with Ultimate Validator**

```python
# Add to ultimate-validator.py

def validate_character_encoding(self, content: str, file_path: str):
    """
    CRITICAL: Validate character encoding issues that cause theme upload failures
    """
    encoding_validator = CharacterEncodingValidator()
    encoding_issues = encoding_validator.validate_file(file_path, content)

    for issue in encoding_issues:
        severity_map = {
            'CRITICAL': Severity.CRITICAL,
            'ERROR': Severity.ERROR,
            'WARNING': Severity.WARNING
        }

        self.add_issue(
            file_path=file_path,
            line=issue['line'],
            issue_type=issue['type'],
            severity=severity_map[issue['severity']],
            message=f"Character encoding issue: {issue['message']}",
            suggestion=issue['fix']
        )

    # Validate schema encoding separately
    schema_match = re.search(r'{% schema %}(.*?){% endschema %}', content, re.DOTALL)
    if schema_match:
        schema_content = schema_match.group(1).strip()
        schema_issues = encoding_validator.validate_schema_encoding(schema_content, file_path)

        for issue in schema_issues:
            self.add_issue(
                file_path=file_path,
                line=issue['line'],
                issue_type=issue['type'],
                severity=severity_map[issue['severity']],
                message=f"Schema encoding issue: {issue['message']}",
                suggestion=issue['fix']
            )
```

---

## 📋 **Common Upload Error Messages**

### **Theme Upload Errors Caused by Character Encoding**

#### **Error: "Template contains invalid characters"**
```
Cause: Non-UTF-8 characters or BOM in .liquid files
Solution: Save all files as UTF-8 without BOM
```

#### **Error: "FileSaveError: Invalid schema"**
```
Cause: HTML entities in schema JSON (&amp;, &lt;, etc.)
Solution: Replace HTML entities with actual characters
```

#### **Error: "Liquid Error: undefined method"**
```
Cause: Unicode characters in variable names
Solution: Use ASCII-only variable names
```

#### **Error: "Template parse error"**
```
Cause: HTML entities breaking Liquid syntax
Solution: Remove entities from Liquid expressions
```

#### **Error: "Encoding error in asset"**
```
Cause: Non-ASCII characters in asset file names
Solution: Rename files with ASCII-only characters
```

### **Browser Display Issues**

#### **Symptoms: Garbled Text (â€™, Ã¡, etc.)**
```
Cause: Character encoding mismatch
Solution: Ensure UTF-8 throughout entire theme
```

#### **Symptoms: Missing Characters**
```
Cause: Font doesn't support Unicode characters
Solution: Use web fonts with Unicode support
```

#### **Symptoms: HTML Entities Displayed as Text**
```
Cause: Double-escaping of content
Solution: Remove unnecessary escape filters
```

---

## 🎯 **Prevention Best Practices**

### **Development Environment Setup**

#### **VS Code Configuration**
```json
{
  "files.encoding": "utf8",
  "files.insertFinalNewline": true,
  "files.trimFinalNewlines": true,
  "files.trimTrailingWhitespace": true,
  "[liquid]": {
    "files.encoding": "utf8"
  }
}
```

#### **Git Configuration**
```gitconfig
[core]
    autocrlf = false
    safecrlf = true

[i18n]
    commitencoding = utf-8
    logoutputencoding = utf-8
```

### **File Naming Conventions**

#### **ASCII-Only File Names**
```
✅ GOOD:
- nav-menu.liquid
- product-card.liquid
- hero-banner.liquid

❌ AVOID:
- nav-menú.liquid
- café-styles.css
- résumé-section.liquid
```

### **Content Guidelines**

#### **Safe Content Patterns**
```liquid
{% comment %} Always escape user content {% endcomment %}
{{ content | escape }}

{% comment %} Strip HTML before escaping {% endcomment %}
{{ content | strip_html | escape }}

{% comment %} Handle quotes in attributes {% endcomment %}
{{ content | escape | replace: '"', '&quot;' }}

{% comment %} Normalize whitespace {% endcomment %}
{{ content | strip | escape }}
```

#### **Translation Key Safety**
```json
{
  "sections": {
    "hero": {
      "heading": "Welcome & Explore",
      "description": "Discover our collection — handcrafted with care"
    }
  }
}
```

---

## 🔧 **Automated Fixes**

### **Character Encoding Fix Script**

```python
#!/usr/bin/env python3
"""
Automated Character Encoding Fix Script for Shopify Liquid Themes
"""

import re
import os
from pathlib import Path

class EncodingFixer:
    def __init__(self):
        self.fixes_applied = 0

    def fix_html_entities_in_liquid(self, content: str) -> str:
        """Remove HTML entities from Liquid expressions"""
        # Fix entities in Liquid output
        content = re.sub(
            r'({{\s*[^}]*?)&amp;([^}]*}})',
            r'\1&\2',
            content
        )
        content = re.sub(
            r'({{\s*[^}]*?)&lt;([^}]*}})',
            r'\1<\2',
            content
        )
        content = re.sub(
            r'({{\s*[^}]*?)&gt;([^}]*}})',
            r'\1>\2',
            content
        )
        content = re.sub(
            r'({{\s*[^}]*?)&quot;([^}]*}})',
            r'\1"\2',
            content
        )
        content = re.sub(
            r'({{\s*[^}]*?)&#39;([^}]*}})',
            r"\1'\2",
            content
        )

        # Fix entities in Liquid tags
        content = re.sub(
            r'({%\s*[^%]*?)&amp;([^%]*%})',
            r'\1&\2',
            content
        )

        return content

    def add_escape_filters(self, content: str) -> str:
        """Add escape filters to unescaped user content"""
        patterns = [
            # Settings content
            (r'({{ settings\.[^}]*?)(?<!\| escape) }}', r'\1 | escape }}'),
            # Customer data
            (r'({{ customer\.[^}]*?)(?<!\| escape) }}', r'\1 | escape }}'),
            # Form data
            (r'({{ form\.[^}]*?)(?<!\| escape) }}', r'\1 | escape }}'),
            # Product/collection content
            (r'({{ (?:product|collection|article|page)\.[^}]*?)(?<!\| escape) }}', r'\1 | escape }}'),
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        return content

    def fix_meta_charset(self, content: str) -> str:
        """Ensure UTF-8 charset in meta tags"""
        # Replace any existing charset with UTF-8
        content = re.sub(
            r'<meta\s+charset=["\']?[^"\'>\s]+["\']?\s*>',
            '<meta charset="utf-8">',
            content,
            flags=re.IGNORECASE
        )

        # Replace content-type meta tags
        content = re.sub(
            r'<meta\s+http-equiv=["\']?content-type["\']?\s+content=["\'][^"\']*["\'][^>]*>',
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
            content,
            flags=re.IGNORECASE
        )

        return content

    def fix_schema_entities(self, content: str) -> str:
        """Fix HTML entities in schema blocks"""
        def fix_schema_block(match):
            schema_content = match.group(1)

            # Replace common HTML entities
            schema_content = schema_content.replace('&amp;', '&')
            schema_content = schema_content.replace('&lt;', '<')
            schema_content = schema_content.replace('&gt;', '>')
            schema_content = schema_content.replace('&quot;', '"')
            schema_content = schema_content.replace('&#39;', "'")
            schema_content = schema_content.replace('&mdash;', '—')
            schema_content = schema_content.replace('&ndash;', '–')
            schema_content = schema_content.replace('&hellip;', '…')

            return f'{{% schema %}}{schema_content}{{% endschema %}}'

        return re.sub(
            r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}',
            fix_schema_block,
            content,
            flags=re.DOTALL
        )

    def fix_file(self, file_path: Path) -> bool:
        """Fix encoding issues in a single file"""
        try:
            # Read file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                original_content = f.read()

            # Apply fixes
            content = original_content
            content = self.fix_html_entities_in_liquid(content)
            content = self.add_escape_filters(content)
            content = self.fix_meta_charset(content)
            content = self.fix_schema_entities(content)

            # Check if any changes were made
            if content != original_content:
                # Write back with UTF-8 encoding
                with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(content)

                print(f"✅ Fixed: {file_path}")
                self.fixes_applied += 1
                return True
            else:
                print(f"ℹ️  No issues: {file_path}")
                return False

        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
            return False

    def fix_directory(self, directory: Path) -> int:
        """Fix encoding issues in all .liquid files in directory"""
        liquid_files = list(directory.rglob("*.liquid"))

        if not liquid_files:
            print(f"No .liquid files found in {directory}")
            return 0

        print(f"Found {len(liquid_files)} .liquid files")
        print("=" * 50)

        for file_path in liquid_files:
            self.fix_file(file_path)

        print("=" * 50)
        print(f"Applied fixes to {self.fixes_applied} files")

        return self.fixes_applied

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fix character encoding issues in Shopify Liquid themes"
    )
    parser.add_argument(
        'path',
        help='Path to .liquid file or directory containing .liquid files'
    )

    args = parser.parse_args()
    path = Path(args.path)

    fixer = EncodingFixer()

    if path.is_file():
        fixer.fix_file(path)
    elif path.is_dir():
        fixer.fix_directory(path)
    else:
        print(f"❌ Path not found: {path}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
```

---

## 📚 **Reference Materials**

### **Official Shopify Documentation**
- [Liquid Filters](https://shopify.dev/docs/api/liquid/filters) - Official filter reference
- [Liquid Objects](https://shopify.dev/docs/api/liquid/objects) - Official object reference
- [Theme Check](https://shopify.dev/docs/themes/tools/theme-check) - Official validation tool

### **Character Encoding Standards**
- [Unicode Standard](https://unicode.org/standard/standard.html) - Unicode specification
- [UTF-8 Specification](https://tools.ietf.org/html/rfc3629) - UTF-8 encoding standard
- [HTML Entity Reference](https://html.spec.whatwg.org/multipage/named-characters.html) - Official HTML entities

### **Shopify Theme Store Requirements**
- [Theme Store Requirements](https://shopify.dev/docs/themes/store/requirements) - Official store requirements
- [Performance Standards](https://shopify.dev/docs/themes/best-practices/performance) - Performance guidelines
- [Accessibility Guidelines](https://shopify.dev/docs/themes/best-practices/accessibility) - Accessibility requirements

---

## 🎯 **Quick Reference Checklist**

### **Pre-Upload Validation**
- [ ] All .liquid files saved as UTF-8 without BOM
- [ ] No HTML entities in Liquid expressions
- [ ] All user content uses `| escape` filter
- [ ] Meta charset set to UTF-8
- [ ] ASCII-only variable names
- [ ] ASCII-only file names
- [ ] Schema JSON contains no HTML entities
- [ ] All HTML attributes properly escaped

### **Common Fix Commands**
```bash
# Run encoding fixes
python3 fix-encoding-issues.py /path/to/theme

# Validate encoding after fixes
python3 ultimate-validator.py --encoding-check /path/to/theme

# Check specific file
python3 ultimate-validator.py file.liquid
```

### **Emergency Fixes**
```liquid
{% comment %} Quick escape pattern {% endcomment %}
{{ content | escape }}

{% comment %} Safe attribute pattern {% endcomment %}
alt="{{ title | escape }}"

{% comment %} Schema safety {% endcomment %}
"default": "Text without & entities"
```

---

*This comprehensive guide covers all major character encoding issues that can cause Shopify theme upload failures and provides systematic solutions for prevention and remediation.*