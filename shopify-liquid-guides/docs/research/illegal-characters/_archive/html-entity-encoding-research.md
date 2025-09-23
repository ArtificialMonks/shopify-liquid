# HTML Entity Encoding Research - Shopify Liquid Upload Errors

## Research Summary

Investigation of HTML entity encoding problems and Unicode compatibility issues in Shopify Liquid templates that cause upload errors.

## Critical HTML Entity Issues

### 1. HTML Entities in Liquid Expressions

**Failing Pattern**:
```liquid
{% if customer.name == 'John &amp; Jane' %}
  {{ 'Hello ' &gt; customer.name }}
{% endif %}
```

**Error Messages**:
- "Liquid parsing error: unexpected character"
- "Invalid Liquid syntax in template"
- "Theme validation failed: malformed expression"

**Working Pattern**:
```liquid
{% if customer.name == 'John & Jane' %}
  {{ 'Hello ' | append: customer.name }}
{% endif %}
```

### 2. HTML Entities in Schema JSON

**Failing Pattern**:
```json
{
  "name": "Product &amp; Service Grid",
  "settings": [
    {
      "label": "Title &gt; Subtitle"
    }
  ]
}
```

**Working Pattern**:
```json
{
  "name": "Product & Service Grid",
  "settings": [
    {
      "label": "Title > Subtitle"
    }
  ]
}
```

### 3. Unicode Characters in Liquid Variables

**Failing Pattern**:
```liquid
{% assign café_items = collection.products %}
{% assign naïve_calculation = price | times: 1.2 %}
```

**Working Pattern**:
```liquid
{% assign cafe_items = collection.products %}
{% assign naive_calculation = price | times: 1.2 %}
```

## Character Encoding Issues

### UTF-8 vs ASCII Compatibility Problems

**Problematic Characters in Code Context**:
- Smart quotes: `"` `"` `'` `'`
- Em/en dashes: `—` `–`
- Mathematical symbols: `×` `÷` `±`
- Accented characters: `café` `naïve` `résumé`

### BOM (Byte Order Mark) Issues

**Problem**: Files with UTF-8 BOM cause parsing failures
**Detection**: Files starting with `EF BB BF` bytes
**Solution**: Save as UTF-8 without BOM

## Security and XSS Issues

### 1. Unescaped User Content

**Failing Pattern**:
```liquid
<div>{{ customer.name }}</div>
<span title="{{ product.title }}">
```

**Working Pattern**:
```liquid
<div>{{ customer.name | escape }}</div>
<span title="{{ product.title | escape }}">
```

### 2. Raw HTML Output Vulnerabilities

**Failing Pattern**:
```liquid
{{ settings.custom_html | raw }}
{{ customer.note | raw }}
```

**Working Pattern**:
```liquid
{{ settings.custom_html }}  <!-- Already trusted admin content -->
{{ customer.note | escape }}  <!-- User content must be escaped -->
```

## Detection Patterns for Validation

```python
HTML_ENTITY_ISSUES = [
    {
        'pattern': r'&(amp|lt|gt|quot|#\d+);',
        'message': 'HTML entities in Liquid context cause parsing errors',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'\{\{\s*[^}]*[^\x00-\x7F][^}]*\}\}',
        'message': 'Non-ASCII characters in Liquid expression',
        'severity': 'ERROR'
    },
    {
        'pattern': r'\{\%\s*assign\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in Liquid variable name',
        'severity': 'ERROR'
    },
    {
        'pattern': r'customer\.[^|}\s]+(?!\s*\|\s*escape)',
        'message': 'Unescaped customer data creates XSS vulnerability',
        'severity': 'ERROR'
    }
]
```

## Character Substitution Mappings

| Problematic | Safe Alternative | Context |
|-------------|------------------|---------|
| `&amp;` | `&` | Liquid expressions |
| `&lt;` | `<` | Liquid expressions |
| `&gt;` | `>` | Liquid expressions |
| `"` `"` | `"` | Schema JSON |
| `—` | `-` | Schema labels |
| `café` | `cafe` | Variable names |

## Validation Integration

### Enhanced Character Encoding Validator

```python
def validate_html_entity_encoding(content, file_path):
    """Validate HTML entity and character encoding issues"""
    issues = []

    # Check for HTML entities in Liquid expressions
    liquid_entities = re.findall(r'\{\{[^}]*&[a-z]+;[^}]*\}\}', content)
    if liquid_entities:
        issues.append({
            'type': 'html_entities_in_liquid',
            'severity': 'CRITICAL',
            'message': 'HTML entities in Liquid expressions break parsing'
        })

    # Check for unescaped user content
    unescaped_user = re.findall(r'customer\.[^|}\s]+(?!\s*\|\s*escape)', content)
    if unescaped_user:
        issues.append({
            'type': 'unescaped_user_content',
            'severity': 'ERROR',
            'message': 'User content must be escaped to prevent XSS'
        })

    return issues
```

### Automated Fix Strategies

```python
def fix_html_entities(content):
    """Automatically fix common HTML entity issues"""

    # Fix HTML entities in Liquid contexts
    content = re.sub(r'&amp;', '&', content)
    content = re.sub(r'&lt;', '<', content)
    content = re.sub(r'&gt;', '>', content)
    content = re.sub(r'&quot;', '"', content)

    # Fix smart quotes in schema
    content = re.sub(r'"([^"]*)"', r'"\1"', content)
    content = re.sub(r''([^']*)'', r"'\1'", content)

    # Add escape filters to user content (basic detection)
    content = re.sub(
        r'(\{\{\s*customer\.[^|}\s]+)(\s*\}\})',
        r'\1 | escape\2',
        content
    )

    return content
```

## UTF-8 Charset Validation

### Proper Meta Tag Declaration

**Failing Pattern**:
```html
<meta charset="ISO-8859-1">
<meta charset="windows-1252">
```

**Working Pattern**:
```html
<meta charset="utf-8">
```

### File Encoding Standards

**Requirements**:
- All `.liquid` files must be UTF-8 encoded
- No BOM (Byte Order Mark) characters
- Consistent line endings (LF preferred)

## Best Practices Summary

1. **Never use HTML entities** in Liquid expressions or schema JSON
2. **Always escape user content** with `| escape` filter
3. **Use ASCII characters only** in Liquid variable names
4. **Save files as UTF-8 without BOM**
5. **Validate character encoding** before theme upload
6. **Use proper meta charset declaration** (`utf-8`)
7. **Test with international characters** to ensure compatibility

## Prevention Checklist

- [ ] No HTML entities in Liquid expressions
- [ ] All user content escaped with `| escape`
- [ ] ASCII-only characters in variable names
- [ ] UTF-8 without BOM file encoding
- [ ] Proper charset meta tag declaration
- [ ] No raw HTML output from user content
- [ ] Schema JSON uses ASCII quotes and characters