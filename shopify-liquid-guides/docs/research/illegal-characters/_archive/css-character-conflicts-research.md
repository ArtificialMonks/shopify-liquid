# CSS Character Conflicts Research - Shopify Theme Upload Errors

## Research Summary

Comprehensive investigation of CSS character encoding issues that cause Shopify theme upload failures.

## Critical CSS Character Issues

### 1. Unicode Operators in calc() Expressions

**Failing Pattern**:
```css
.component {
  width: calc(100% – 20px);  /* Em dash causes parsing error */
  height: calc(50vh ÷ 2);    /* Division symbol breaks CSS */
}
```

**Working Pattern**:
```css
.component {
  width: calc(100% - 20px);  /* ASCII hyphen */
  height: calc(50vh / 2);    /* ASCII division */
}
```

### 2. Raw Unicode Characters in Content Properties

**Failing Pattern**:
```css
.quote::before {
  content: """;  /* Smart quote breaks parsing */
}
.separator::after {
  content: "—";  /* Em dash causes encoding error */
}
```

**Working Pattern**:
```css
.quote::before {
  content: '"';  /* ASCII quote */
}
.separator::after {
  content: '\2014';  /* Unicode escape */
}
```

### 3. Non-ASCII Characters in CSS Selectors

**Failing Pattern**:
```css
.café-menu { }     /* Accented characters */
.naïve-approach { } /* Diacritical marks */
```

**Working Pattern**:
```css
.cafe-menu { }
.naive-approach { }
```

### 4. BOM (Byte Order Mark) Issues

**Problem**: CSS files saved with UTF-8 BOM cause parsing failures
**Solution**: Save CSS files as UTF-8 without BOM

### 5. Invisible/Zero-Width Characters

**Failing Pattern**:
```css
.component​ {  /* Zero-width space in selector */
  display: flex;
}
```

**Detection**: These characters are invisible but break CSS parsing

## Character Encoding Detection Patterns

```python
CSS_CHARACTER_ISSUES = [
    {
        'pattern': r'calc\([^)]*[–—×÷][^)]*\)',
        'message': 'Unicode operators in calc() break CSS parsing',
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
        'message': 'Invisible/zero-width characters detected',
        'severity': 'ERROR'
    }
]
```

## Safe Character Replacements

| Problematic Character | Safe Replacement | CSS Context |
|----------------------|------------------|-------------|
| `–` (en dash) | `-` | calc() expressions |
| `—` (em dash) | `-` or `\2014` | content property |
| `"` (smart quote) | `"` or `\201C` | content property |
| `×` (multiplication) | `*` | calc() expressions |
| `÷` (division) | `/` | calc() expressions |
| `café` | `cafe` | Class names |

## Font-Family Encoding Issues

**Failing Pattern**:
```css
font-family: "Times New Roman", "Helvetica Neue";
```

**Working Pattern**:
```css
font-family: 'Times New Roman', 'Helvetica Neue';
```

## CSS Custom Properties Issues

**Failing Pattern**:
```css
:root {
  --café-color: #brown;  /* Non-ASCII in variable name */
}
```

**Working Pattern**:
```css
:root {
  --cafe-color: #brown;
}
```

## Validation and Auto-Fix Strategies

### Detection Script Integration
```python
def validate_css_character_encoding(content, file_path):
    issues = []

    # Check for Unicode operators in calc()
    calc_unicode = re.findall(r'calc\([^)]*[–—×÷][^)]*\)', content)
    if calc_unicode:
        issues.append({
            'type': 'unicode_calc_operators',
            'severity': 'CRITICAL',
            'message': 'Unicode operators in calc() expressions'
        })

    return issues
```

### Automated Character Fixes
```python
def fix_css_characters(content):
    # Fix Unicode operators in calc()
    content = re.sub(r'(calc\([^)]*?)–([^)]*?\))', r'\1-\2', content)
    content = re.sub(r'(calc\([^)]*?)—([^)]*?\))', r'\1-\2', content)
    content = re.sub(r'(calc\([^)]*?)×([^)]*?\))', r'\1*\2', content)
    content = re.sub(r'(calc\([^)]*?)÷([^)]*?\))', r'\1/\2', content)

    # Fix smart quotes in content
    content = re.sub(r'content:\s*["\']"([^"\']*)"["\']', r'content: "\1"', content)
    content = re.sub(r'content:\s*["\']"([^"\']*)"["\']', r'content: "\1"', content)

    return content
```

## Prevention Best Practices

1. **Use ASCII-only characters** in CSS selectors and variable names
2. **Escape Unicode characters** properly in content properties
3. **Save files as UTF-8 without BOM**
4. **Use standard operators** (`-`, `/`, `*`) in calc() expressions
5. **Validate character encoding** before theme upload
6. **Use proper text editors** that handle encoding correctly