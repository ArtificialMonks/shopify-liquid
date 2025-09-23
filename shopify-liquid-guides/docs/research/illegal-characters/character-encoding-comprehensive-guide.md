# Character Encoding Comprehensive Guide

**Complete reference for preventing and fixing character encoding issues in Shopify Liquid themes**

*Consolidated from comprehensive research analysis of JavaScript, CSS, HTML entity, and CLI platform issues*

---

## Executive Summary

Character encoding issues are the leading cause of Shopify theme upload failures, development errors, and security vulnerabilities. This guide provides a complete solution covering all critical domains:

- **JavaScript Context Separation** - Preventing Liquid/JavaScript mixing that breaks parsing
- **CSS Character Conflicts** - Eliminating Unicode operators and selector issues
- **HTML Entity Problems** - Fixing entity encoding in Liquid expressions
- **CLI Platform Limitations** - Resolving cross-platform encoding differences

**Zero Tolerance Approach**: Any character encoding issue can cause theme upload failure, security vulnerabilities, or deployment errors.

---

## 🚨 Critical Character Violations (Upload Blockers)

### 1. JavaScript Context Separation Violations

**Context separation is STRICTLY enforced** - Liquid code cannot exist inside JavaScript blocks.

#### Problem Patterns
```liquid
❌ CRITICAL - Liquid inside {% javascript %} blocks:
{% javascript %}
  var themeColor = "{{ settings.primary_color }}";
  var productData = {{ product | json }};
{% endjavascript %}
```

**Why This Breaks:**
- Liquid parser processes before JavaScript
- Creates syntax conflicts between contexts
- Breaks theme upload validation

#### Solution Patterns
```liquid
✅ CORRECT - Data attributes approach:
<div data-theme-color="{{ settings.primary_color | escape }}"
     data-product='{{ product | json | escape }}'
     id="theme-data"></div>

{% javascript %}
  const themeData = document.getElementById('theme-data');
  const themeColor = themeData.dataset.themeColor;
  const productData = JSON.parse(themeData.dataset.product);
{% endjavascript %}
```

#### Template Literal Conflicts
```javascript
❌ BREAKS PARSING:
const message = `Hello {{ customer.first_name }}`;

✅ SAFE ALTERNATIVE:
<script>
  window.customerName = {{ customer.first_name | json }};
</script>
{% javascript %}
  const message = `Hello ${window.customerName}`;
{% endjavascript %}
```

### 2. CSS Character Conflicts (Upload Blockers)

#### Unicode Operators in calc() Expressions
```css
❌ CRITICAL - Unicode operators break CSS parsing:
.component {
  width: calc(100% – 20px);    /* Em dash (U+2013) */
  height: calc(50vh — 40px);   /* Em dash (U+2014) */
  margin: calc(var(--space) × 2);  /* Multiplication (U+00D7) */
  padding: calc(100% ÷ 3);     /* Division (U+00F7) */
}

✅ SAFE - ASCII operators only:
.component {
  width: calc(100% - 20px);    /* ASCII hyphen */
  height: calc(50vh - 40px);   /* ASCII hyphen */
  margin: calc(var(--space) * 2);  /* ASCII asterisk */
  padding: calc(100% / 3);     /* ASCII slash */
}
```

#### Smart Quotes in Content Properties
```css
❌ BREAKS ENCODING:
.quote::before { content: """; }  /* Smart quote (U+201C) */
.quote::after { content: """; }   /* Smart quote (U+201D) */
.separator { content: "—"; }      /* Em dash (U+2014) */

✅ SAFE ALTERNATIVES:
.quote::before { content: '"'; }     /* ASCII quote */
.quote::after { content: '"'; }      /* ASCII quote */
.separator { content: '\2014'; }     /* Unicode escape */
```

#### Non-ASCII CSS Selectors
```css
❌ INVALID SELECTORS:
.café-menu { }        /* Accented characters */
.naïve-approach { }   /* Diacritical marks */
.component-测试 { }    /* CJK characters */

✅ ASCII-ONLY SELECTORS:
.cafe-menu { }
.naive-approach { }
.component-test { }
```

### 3. HTML Entity Encoding Violations

#### HTML Entities in Liquid Expressions
```liquid
❌ CRITICAL - HTML entities break Liquid parsing:
{{ product.title | replace: '&amp;', '&' }}
{{ settings.text | append: '&nbsp;' }}
{{ description | truncate: 50, '&hellip;' }}

✅ CORRECT - Use actual characters:
{{ product.title | replace: '&', '&' }}
{{ settings.text | append: ' ' }}
{{ description | truncate: 50, '...' }}
```

#### HTML Entities in Schema JSON
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

### 4. CLI Platform Violations

#### UTF-8 BOM (Byte Order Mark)
```
❌ CRITICAL - BOM causes immediate upload failure:
﻿/* BOM at file start breaks CLI parsing */

✅ SAFE - UTF-8 without BOM:
/* Clean file start with no BOM */
```

**Detection Command:**
```bash
# Detect BOM in files
file -bi *.liquid | grep -v "charset=utf-8"
hexdump -C file.liquid | head -1
```

#### Control Characters
```
❌ BREAKS CLI PARSING:
Files containing \x00-\x1F or \x7F-\x9F characters

✅ CLEAN FILES:
Only printable UTF-8 characters (except tab, newline, carriage return)
```

---

## 🔐 Security-Critical Character Issues

### XSS Prevention Through Character Escaping

#### Unescaped User Content
```liquid
❌ SECURITY VULNERABILITY:
{{ customer.name }}
{{ comment.body }}
{{ form.errors }}

✅ SECURE - Always escape user content:
{{ customer.name | escape }}
{{ comment.body | escape }}
{{ form.errors | escape }}
```

#### Raw Filter Security Issues
```liquid
❌ XSS VULNERABILITY:
{{ settings.custom_html | raw }}
{{ page.content | raw }}

✅ SECURE - Avoid raw filter unless absolutely necessary:
{{ settings.custom_html }}  <!-- Auto-escaped -->
{{ page.content }}           <!-- Auto-escaped -->
```

#### Script Context Security
```liquid
❌ CRITICAL XSS RISK:
<script>
  var userName = "{{ customer.name }}";
</script>

✅ SECURE APPROACH:
<div data-user-name="{{ customer.name | escape }}"></div>
<script>
  var userName = document.querySelector('[data-user-name]').dataset.userName;
</script>
```

---

## 🛡️ Detection Patterns and Validation

### JavaScript Character Encoding Issues
```python
JAVASCRIPT_CHARACTER_VIOLATIONS = [
    {
        'pattern': r'{%\s*javascript\s*%}[^{]*{{\s*[^}]*\s*}}',
        'message': 'CRITICAL: Liquid code inside {% javascript %} tag',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'<script[^>]*>[^<]*`[^`]*\{\{[^}]*\}\}[^`]*`',
        'message': 'Template literals with Liquid interpolation',
        'severity': 'ERROR'
    },
    {
        'pattern': r'const\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in JavaScript identifier',
        'severity': 'WARNING'
    }
]
```

### CSS Character Conflict Detection
```python
CSS_CHARACTER_VIOLATIONS = [
    {
        'pattern': r'calc\([^)]*[–—×÷][^)]*\)',
        'message': 'CRITICAL: Unicode operators in calc() break parsing',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'content:\s*["\'][""''–—]["\']',
        'message': 'Smart quotes/dashes in content property',
        'severity': 'ERROR'
    },
    {
        'pattern': r'\.[^\x00-\x7F\s{]+\s*\{',
        'message': 'Non-ASCII characters in CSS selector',
        'severity': 'WARNING'
    },
    {
        'pattern': r'[\u200B-\u200D\uFEFF]',
        'message': 'CRITICAL: Invisible characters break parsing',
        'severity': 'CRITICAL'
    }
]
```

### HTML Entity Violation Detection
```python
HTML_ENTITY_VIOLATIONS = [
    {
        'pattern': r'\{\{[^}]*&(amp|lt|gt|quot|#\d+);[^}]*\}\}',
        'message': 'CRITICAL: HTML entities in Liquid expressions',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'\{\%\s*assign\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in Liquid variable name',
        'severity': 'ERROR'
    },
    {
        'pattern': r'customer\.[^|}\s]+(?!\s*\|\s*escape)',
        'message': 'SECURITY: Unescaped customer data creates XSS vulnerability',
        'severity': 'CRITICAL'
    }
]
```

### CLI Platform Limitation Detection
```python
CLI_PLATFORM_VIOLATIONS = [
    {
        'pattern': r'^\ufeff',
        'message': 'CRITICAL: UTF-8 BOM causes CLI upload failure',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'[\u0000-\u001F\u007F-\u009F]',
        'message': 'Control characters cause CLI parsing errors',
        'severity': 'ERROR'
    },
    {
        'pattern': r'[""'']',
        'message': 'Smart quotes in code context',
        'severity': 'WARNING'
    }
]
```

---

## 🔧 Automated Character Fixing

### JavaScript Context Fixes
```python
def fix_javascript_characters(content):
    """Fix JavaScript character encoding issues"""

    # Move Liquid out of {% javascript %} blocks
    js_liquid_pattern = r'({%\s*javascript\s*%})(.*?)(\{\{[^}]*\}\})(.*?)({%\s*endjavascript\s*%})'

    def replace_js_liquid(match):
        js_start, before_liquid, liquid_code, after_liquid, js_end = match.groups()

        # Convert to data attribute approach
        var_match = re.search(r'settings\.(\w+)', liquid_code)
        if var_match:
            setting_name = var_match.group(1)
            data_attr = f'data-{setting_name.replace("_", "-")}'

            return f'''<div {data_attr}="{liquid_code}"></div>
{js_start}
{before_liquid}document.querySelector('[{data_attr}]').dataset.{setting_name}{after_liquid}
{js_end}'''

    return re.sub(js_liquid_pattern, replace_js_liquid, content, flags=re.DOTALL)
```

### CSS Character Fixes
```python
def fix_css_characters(content):
    """Fix CSS character encoding issues"""

    # Fix Unicode operators in calc()
    content = re.sub(r'(calc\([^)]*?)–([^)]*?\))', r'\1-\2', content)  # En dash
    content = re.sub(r'(calc\([^)]*?)—([^)]*?\))', r'\1-\2', content)  # Em dash
    content = re.sub(r'(calc\([^)]*?)×([^)]*?\))', r'\1*\2', content)  # Multiplication
    content = re.sub(r'(calc\([^)]*?)÷([^)]*?\))', r'\1/\2', content)  # Division

    # Fix smart quotes in content properties
    content = re.sub(r'content:\s*["\']"([^"\']*)"["\']', r'content: "\1"', content)
    content = re.sub(r'content:\s*["\']"([^"\']*)"["\']', r'content: "\1"', content)

    # Remove invisible characters
    invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
    for char in invisible_chars:
        content = content.replace(char, '')

    return content
```

### HTML Entity Fixes
```python
def fix_html_entities(content):
    """Fix HTML entity encoding issues"""

    # Fix HTML entities in Liquid expressions
    content = re.sub(r'(\{\{[^}]*?)&amp;([^}]*?\}\})', r'\1&\2', content)
    content = re.sub(r'(\{\{[^}]*?)&lt;([^}]*?\}\})', r'\1<\2', content)
    content = re.sub(r'(\{\{[^}]*?)&gt;([^}]*?\}\})', r'\1>\2', content)
    content = re.sub(r'(\{\{[^}]*?)&quot;([^}]*?\}\})', r'\1"\2', content)

    # Add escape filters to unescaped user content
    user_content_patterns = [
        r'(\{\{\s*customer\.[^|}\s]+)(\s*\}\})',
        r'(\{\{\s*comment\.body[^|}\s]*)(\s*\}\})',
        r'(\{\{\s*form\.errors[^|}\s]*)(\s*\}\})',
    ]

    for pattern in user_content_patterns:
        content = re.sub(pattern, r'\1 | escape\2', content)

    return content
```

### CLI Platform Fixes
```python
def fix_cli_platform_characters(content):
    """Fix CLI platform compatibility issues"""

    # Remove BOM if present
    if content.startswith('\ufeff'):
        content = content[1:]

    # Replace smart quotes
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")

    # Replace typography dashes
    content = content.replace('—', '-').replace('–', '-')

    # Remove control characters (except tab, newline, carriage return)
    control_chars = ''.join(chr(i) for i in range(0x00, 0x20) if i not in [0x09, 0x0A, 0x0D])
    for char in control_chars:
        content = content.replace(char, '')

    return content
```

---

## 📋 Character Substitution Reference

### Critical Character Replacements (Upload Blockers)

| Problematic Character | Safe Replacement | Context | Severity |
|----------------------|------------------|---------|----------|
| `–` (en dash U+2013) | `-` (ASCII hyphen) | CSS calc() | CRITICAL |
| `—` (em dash U+2014) | `-` or `\2014` | CSS content | CRITICAL |
| `×` (multiplication U+00D7) | `*` (ASCII asterisk) | CSS calc() | CRITICAL |
| `÷` (division U+00F7) | `/` (ASCII slash) | CSS calc() | CRITICAL |
| `"` (left quote U+201C) | `"` (ASCII quote) | All contexts | ERROR |
| `"` (right quote U+201D) | `"` (ASCII quote) | All contexts | ERROR |
| `'` (left quote U+2018) | `'` (ASCII apostrophe) | All contexts | ERROR |
| `'` (right quote U+2019) | `'` (ASCII apostrophe) | All contexts | ERROR |
| `&amp;` | `&` | Liquid expressions | CRITICAL |
| `&lt;` | `<` | Liquid expressions | CRITICAL |
| `&gt;` | `>` | Liquid expressions | CRITICAL |
| `\uFEFF` (BOM) | Remove entirely | File start | CRITICAL |

### Security-Critical Replacements

| Vulnerable Pattern | Safe Replacement | Security Risk |
|-------------------|------------------|---------------|
| `{{ customer.name }}` | `{{ customer.name \| escape }}` | XSS |
| `{{ comment.body }}` | `{{ comment.body \| escape }}` | XSS |
| `{{ form.errors }}` | `{{ form.errors \| escape }}` | XSS |
| `\| raw` filter | Remove `\| raw` | XSS |

---

## 🚀 Implementation and Validation

### Development Workflow Integration
```bash
# Character encoding validation during development
./scripts/validate-theme.sh development --encoding

# Pre-commit character validation
git config core.hooksPath ./scripts/git-hooks
```

### Production Deployment Validation
```bash
# Upload readiness validation
./scripts/validate-theme.sh production --encoding

# Platform compatibility check
./scripts/validate-platform-encoding.sh --all-platforms
```

### Ultimate Quality Assurance
```bash
# Zero tolerance character validation
./scripts/validate-theme.sh ultimate --encoding

# Comprehensive security audit
./scripts/validate-theme.sh ultimate --security
```

---

## 📚 Platform-Specific Considerations

### Windows Development
```batch
:: Set UTF-8 code page
chcp 65001

:: Configure Git for Windows
git config core.autocrlf true
git config core.quotepath false

:: Remove BOM from files
powershell "$content = Get-Content 'file.liquid' -Raw; Set-Content 'file.liquid' -Value $content.TrimStart([char]0xFEFF) -Encoding UTF8NoBOM"
```

### macOS Development
```bash
# Set UTF-8 locale
export LC_ALL=en_US.UTF-8

# Configure Git for Unicode handling
git config core.precomposeunicode true
git config core.quotepath false

# Remove invisible characters
sed -i '' 's/\xE2\x80\x8B//g' *.liquid  # Zero-width space
sed -i '' 's/\xEF\xBB\xBF//g' *.liquid  # BOM removal
```

### Linux Development
```bash
# Ensure UTF-8 environment
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Character encoding validation
file -bi *.liquid | grep -v "charset=utf-8"

# Smart quote replacement
sed -i 's/"/"/g; s/"/"/g; s/'/'"'"'/g; s/'/'"'"'/g' *.liquid
```

---

## ✅ Character Validation Checklist

### Pre-Development Setup
- [ ] Configure editor for UTF-8 without BOM
- [ ] Set up Git with proper character handling
- [ ] Install character validation pre-commit hooks
- [ ] Configure platform-specific locale settings

### During Development
- [ ] Use ASCII-only characters in code contexts
- [ ] Escape all user content with | escape filter
- [ ] Avoid Unicode operators in CSS calc() expressions
- [ ] Keep Liquid and JavaScript contexts separate
- [ ] Use data attributes for cross-context communication

### Pre-Upload Validation
- [ ] Run character encoding validation
- [ ] Check for BOM characters in all files
- [ ] Validate HTML entity usage
- [ ] Test on target platform
- [ ] Confirm security character escaping

### Post-Upload Verification
- [ ] Verify theme functions correctly
- [ ] Test international character display
- [ ] Confirm no encoding errors in browser
- [ ] Validate security functionality
- [ ] Check cross-platform compatibility

---

*This comprehensive guide consolidates research from four critical domains to ensure zero character-related theme deployment failures through systematic detection, prevention, and automated fixing.*