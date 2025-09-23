# CSS Illegal Characters Investigation: Shopify Theme Upload Errors

**Comprehensive investigation into CSS character encoding issues that break Shopify theme uploads, with detection patterns and solutions.**

---

## Executive Summary

This investigation documents CSS character encoding issues that cause Shopify theme upload failures, specifically focusing on:
- Illegal character sequences in CSS selectors
- Unicode character problems in custom properties and values
- Character encoding issues in CSS expressions and functions
- Font-family declarations with encoding conflicts
- CSS content properties with problematic character combinations

**Key Finding**: Shopify's theme upload system has strict character validation that rejects themes containing specific Unicode sequences, unescaped special characters, and malformed encoding patterns in CSS files.

---

## 1. Critical Problem Categories

### 1.1 CSS Selector Character Issues

**Problem Pattern**: Invalid or illegal characters in CSS class names and selectors
```css
/* ❌ BREAKS UPLOAD - Illegal characters in selectors */
.component-❌-invalid { color: red; }
.my_section—with—em-dash { display: block; }
.content\2013 invalid { margin: 0; }  /* Unicode em-dash */

/* ✅ SAFE ALTERNATIVES */
.component-invalid { color: red; }
.my-section-with-dash { display: block; }
.content-valid { margin: 0; }
```

**Upload Error**: `Invalid CSS syntax: Unexpected character in selector`

### 1.2 Unicode Character Encoding Issues

**Problem Pattern**: Unescaped Unicode characters and BOM sequences
```css
/* ❌ BREAKS UPLOAD - Raw Unicode characters */
.content::before { content: "→"; }  /* Raw right arrow */
.quote::before { content: """; }    /* Raw smart quote */
.bullet { content: "•"; }           /* Raw bullet point */

/* ❌ BREAKS UPLOAD - BOM and invisible characters */
﻿/* Zero-width no-break space (BOM) at file start */
.component { margin: 0; }

/* ✅ SAFE ALTERNATIVES */
.content::before { content: "\2192"; }  /* Escaped Unicode */
.quote::before { content: "\201C"; }    /* Escaped smart quote */
.bullet { content: "\2022"; }           /* Escaped bullet */
```

**Upload Error**: `File contains invalid UTF-8 sequence`

### 1.3 CSS Custom Properties with Illegal Characters

**Problem Pattern**: Non-ASCII characters in CSS variable names
```css
/* ❌ BREAKS UPLOAD - Non-ASCII in variable names */
:root {
  --color-primário: #007cba;    /* Portuguese characters */
  --spacing-médio: 24px;        /* Accented characters */
  --border-radiüs: 8px;         /* Umlaut character */
}

/* ✅ SAFE ALTERNATIVES */
:root {
  --color-primary: #007cba;
  --spacing-medium: 24px;
  --border-radius: 8px;
}
```

**Upload Error**: `Invalid property name: Contains non-ASCII characters`

### 1.4 CSS calc() Expression Issues

**Problem Pattern**: Illegal character combinations in mathematical expressions
```css
/* ❌ BREAKS UPLOAD - Invalid operators and spacing */
.width { width: calc(100%–20px); }      /* Em-dash instead of minus */
.height { height: calc(100vh−40px); }   /* Unicode minus sign */
.gap { gap: calc(var(--space)×2); }     /* Multiplication symbol */

/* ❌ BREAKS UPLOAD - Zero-width characters in calc */
.margin { margin: calc(20px​ + 10px); } /* Zero-width space */

/* ✅ SAFE ALTERNATIVES */
.width { width: calc(100% - 20px); }
.height { height: calc(100vh - 40px); }
.gap { gap: calc(var(--space) * 2); }
.margin { margin: calc(20px + 10px); }
```

**Upload Error**: `CSS parsing error: Invalid calc() expression`

### 1.5 Font-Family Declaration Problems

**Problem Pattern**: Unescaped quotes and special characters in font names
```css
/* ❌ BREAKS UPLOAD - Unescaped quotes in font names */
.text { font-family: "Times "New" Roman", serif; }
.heading { font-family: 'Helvetica's Bold', sans-serif; }

/* ❌ BREAKS UPLOAD - Unicode characters in font names */
.special { font-family: "Fütura", "Café Script"; }

/* ✅ SAFE ALTERNATIVES */
.text { font-family: "Times New Roman", serif; }
.heading { font-family: "Helvetica Bold", sans-serif; }
.special { font-family: "Futura", "Cafe Script"; }
```

**Upload Error**: `Invalid font-family declaration: Malformed string`

### 1.6 CSS Content Property Character Issues

**Problem Pattern**: Raw special characters in content values
```css
/* ❌ BREAKS UPLOAD - Raw special characters */
.icon::before { content: "⭐"; }     /* Raw star emoji */
.arrow::after { content: "→"; }     /* Raw arrow */
.check::before { content: "✓"; }    /* Raw checkmark */

/* ❌ BREAKS UPLOAD - Malformed escape sequences */
.broken::before { content: "\20"; } /* Incomplete Unicode escape */
.invalid::before { content: "\g"; } /* Invalid escape character */

/* ✅ SAFE ALTERNATIVES */
.icon::before { content: "\2B50"; }    /* Escaped star */
.arrow::after { content: "\2192"; }    /* Escaped arrow */
.check::before { content: "\2713"; }   /* Escaped checkmark */
.simple::before { content: "*"; }      /* ASCII alternative */
```

**Upload Error**: `Invalid content value: Malformed character sequence`

---

## 2. Character Detection Patterns

### 2.1 Illegal Character Regex Patterns

```javascript
// CSS Selector validation
const ILLEGAL_SELECTOR_CHARS = /[^\w\-_.#:()[\]>+~\s]/g;

// Unicode character detection
const RAW_UNICODE_CHARS = /[^\x00-\x7F]/g;

// BOM detection
const BOM_PATTERN = /^\uFEFF/;

// Invalid calc() expressions
const INVALID_CALC_OPERATORS = /calc\([^)]*[–—×÷].*?\)/g;

// Malformed escape sequences
const INVALID_ESCAPES = /\\[^0-9a-fA-F\r\n\f]/g;

// Non-ASCII in CSS variable names
const INVALID_CSS_VARS = /--[^:]*[^\x00-\x7F][^:]*:/g;
```

### 2.2 Content Property Pattern Detection

```javascript
// Raw special characters in content
const RAW_SPECIAL_CHARS = /content:\s*["'][^"']*[^\x00-\x7F][^"']*["']/g;

// Incomplete Unicode escapes
const INCOMPLETE_UNICODE = /\\[0-9a-fA-F]{1,3}(?![0-9a-fA-F])/g;

// Invalid escape characters
const INVALID_ESCAPE_CHARS = /\\[^0-9a-fA-F\r\n\f"'\\]/g;
```

### 2.3 Font-Family Pattern Detection

```javascript
// Unescaped quotes in font names
const UNESCAPED_QUOTES = /font-family:[^;]*["'][^"']*["'][^"']*["']/g;

// Unicode in font family names
const UNICODE_FONT_NAMES = /font-family:[^;]*["'][^"']*[^\x00-\x7F][^"']*["']/g;
```

---

## 3. Automated Validation Solutions

### 3.1 Pre-Upload CSS Validator

```python
import re
import unicodedata

class ShopifyCSSValidator:
    def __init__(self):
        self.errors = []

    def validate_css_file(self, css_content: str, filename: str) -> bool:
        """Validate CSS content for Shopify compatibility"""
        self.errors = []

        # Check for BOM
        if css_content.startswith('\ufeff'):
            self.errors.append(f"{filename}: File contains BOM character")

        # Check for illegal characters in selectors
        self._validate_selectors(css_content, filename)

        # Check for unicode issues
        self._validate_unicode_usage(css_content, filename)

        # Check calc() expressions
        self._validate_calc_expressions(css_content, filename)

        # Check content properties
        self._validate_content_properties(css_content, filename)

        # Check font-family declarations
        self._validate_font_families(css_content, filename)

        return len(self.errors) == 0

    def _validate_selectors(self, content: str, filename: str):
        """Check for illegal characters in CSS selectors"""
        # Pattern matches class/id selectors with illegal chars
        illegal_selector_pattern = r'[.#][^{\s]*[^\w\-_][^{\s]*\s*{'
        matches = re.finditer(illegal_selector_pattern, content, re.MULTILINE)

        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.errors.append(
                f"{filename}:{line_num}: Illegal character in selector: {match.group()}"
            )

    def _validate_unicode_usage(self, content: str, filename: str):
        """Check for problematic Unicode usage"""
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for raw Unicode characters (not in strings)
            if re.search(r'[^\x00-\x7F]', line):
                # Exclude content properties and comments
                if not re.search(r'content\s*:|/\*|^//', line):
                    self.errors.append(
                        f"{filename}:{i}: Raw Unicode character found: {line.strip()}"
                    )

    def _validate_calc_expressions(self, content: str, filename: str):
        """Check calc() expressions for illegal operators"""
        calc_pattern = r'calc\([^)]+\)'
        illegal_ops = ['–', '—', '×', '÷', '−']

        for match in re.finditer(calc_pattern, content):
            calc_expr = match.group()
            for op in illegal_ops:
                if op in calc_expr:
                    line_num = content[:match.start()].count('\n') + 1
                    self.errors.append(
                        f"{filename}:{line_num}: Invalid calc() operator '{op}': {calc_expr}"
                    )

    def _validate_content_properties(self, content: str, filename: str):
        """Validate CSS content property values"""
        content_pattern = r'content\s*:\s*["\']([^"\']*)["\']'

        for match in re.finditer(content_pattern, content):
            content_value = match.group(1)

            # Check for raw Unicode characters
            if re.search(r'[^\x00-\x7F]', content_value):
                line_num = content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"{filename}:{line_num}: Raw Unicode in content property: {match.group()}"
                )

            # Check for malformed escape sequences
            if re.search(r'\\[^0-9a-fA-F\r\n\f"\'\\]', content_value):
                line_num = content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"{filename}:{line_num}: Invalid escape sequence: {match.group()}"
                )

    def _validate_font_families(self, content: str, filename: str):
        """Validate font-family declarations"""
        font_pattern = r'font-family\s*:[^;]+;'

        for match in re.finditer(font_pattern, content):
            font_decl = match.group()

            # Check for unescaped quotes
            if re.search(r'["\'][^"\']*["\'][^"\']*["\']', font_decl):
                line_num = content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"{filename}:{line_num}: Unescaped quotes in font-family: {font_decl}"
                )

    def get_errors(self) -> list:
        """Return list of validation errors"""
        return self.errors
```

### 3.2 Character Sanitization Functions

```python
def sanitize_css_content(css_content: str) -> str:
    """Sanitize CSS content for Shopify compatibility"""

    # Remove BOM if present
    if css_content.startswith('\ufeff'):
        css_content = css_content[1:]

    # Fix common Unicode operator issues in calc()
    unicode_operators = {
        '–': '-',  # En-dash to hyphen
        '—': '-',  # Em-dash to hyphen
        '×': '*',  # Multiplication sign to asterisk
        '÷': '/',  # Division sign to slash
        '−': '-',  # Unicode minus to hyphen
    }

    for unicode_char, ascii_char in unicode_operators.items():
        css_content = css_content.replace(unicode_char, ascii_char)

    # Convert raw Unicode in content properties to escaped form
    def escape_content_unicode(match):
        content_value = match.group(1)
        escaped_value = ''

        for char in content_value:
            if ord(char) > 127:
                escaped_value += f'\\{ord(char):04X}'
            else:
                escaped_value += char

        return f'content: "{escaped_value}"'

    css_content = re.sub(
        r'content\s*:\s*["\']([^"\']*)["\']',
        escape_content_unicode,
        css_content
    )

    return css_content

def validate_css_variable_names(css_content: str) -> list:
    """Validate CSS custom property names for ASCII compliance"""
    errors = []

    var_pattern = r'--([^:]+):'
    for match in re.finditer(var_pattern, css_content):
        var_name = match.group(1)

        # Check for non-ASCII characters
        if re.search(r'[^\x00-\x7F]', var_name):
            errors.append(f"Invalid CSS variable name: --{var_name}")

    return errors
```

---

## 4. Best Practices and Solutions

### 4.1 Character Encoding Guidelines

**1. Always Use UTF-8 Without BOM**
```html
<!-- In layout files -->
<meta charset="utf-8">
```

**2. Escape Unicode Characters in CSS**
```css
/* Use Unicode escape sequences for special characters */
.icon::before { content: "\2192"; }  /* Right arrow */
.quote::before { content: "\201C"; } /* Left double quote */
.bullet::before { content: "\2022"; } /* Bullet point */
```

**3. ASCII-Only CSS Variable Names**
```css
/* Use English, ASCII-only variable names */
:root {
  --color-primary: #007cba;
  --spacing-large: 40px;
  --border-radius-small: 4px;
}
```

### 4.2 Safe CSS Patterns

**Content Property Best Practices**
```css
/* Safe Unicode usage in content */
.check::before {
  content: "\2713";  /* Unicode checkmark */
  color: var(--success-color);
}

/* ASCII alternatives for common symbols */
.arrow::after {
  content: ">";      /* ASCII greater-than */
  transform: rotate(90deg);
}

/* Font icons as safer alternative */
.icon {
  font-family: 'IconFont', sans-serif;
  font-style: normal;
}
```

**Calc() Expression Safety**
```css
/* Always use ASCII operators */
.responsive-width {
  width: calc(100% - 40px);  /* ASCII minus */
  max-width: calc(800px * 0.8);  /* ASCII asterisk */
}

/* Use CSS custom properties for complex calculations */
:root {
  --base-size: 16px;
  --scale-factor: 1.5;
}

.scaled-text {
  font-size: calc(var(--base-size) * var(--scale-factor));
}
```

### 4.3 Font-Family Declaration Safety

```css
/* Proper font-family syntax */
.heading {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/* Avoid special characters in font names */
.body-text {
  font-family: "Source Sans Pro", "Open Sans", sans-serif;
}

/* Use web-safe fallbacks */
.custom-font {
  font-family: "CustomFont", "Times New Roman", serif;
}
```

---

## 5. Integration with Existing Validation

### 5.1 Enhanced Ultimate Validator Integration

```python
# Add to ultimate-validator.py
CSS_CHARACTER_ENCODING_PATTERNS = [
    {
        'pattern': r'^\uFEFF',
        'message': 'CSS FILE CONTAINS BOM: File starts with Byte Order Mark',
        'severity': Severity.CRITICAL,
        'suggestion': 'Save file as UTF-8 without BOM'
    },
    {
        'pattern': r'[.#][^{\s]*[^\w\-_][^{\s]*\s*{',
        'message': 'ILLEGAL CSS SELECTOR: Contains invalid characters',
        'severity': Severity.CRITICAL,
        'suggestion': 'Use only alphanumeric, hyphen, underscore in selectors'
    },
    {
        'pattern': r'calc\([^)]*[–—×÷−][^)]*\)',
        'message': 'INVALID CALC OPERATOR: Unicode math operators not allowed',
        'severity': Severity.CRITICAL,
        'suggestion': 'Use ASCII operators: + - * / in calc() expressions'
    },
    {
        'pattern': r'content\s*:\s*["\'][^"\']*[^\x00-\x7F][^"\']*["\']',
        'message': 'RAW UNICODE IN CONTENT: Use escaped Unicode sequences',
        'severity': Severity.ERROR,
        'suggestion': 'Replace with \\[Unicode-hex] escape sequences'
    },
    {
        'pattern': r'--[^:]*[^\x00-\x7F][^:]*:',
        'message': 'NON-ASCII CSS VARIABLE: Variable names must be ASCII',
        'severity': Severity.ERROR,
        'suggestion': 'Use ASCII characters only in CSS variable names'
    }
]

def validate_css_character_encoding(self, content: str, file_path: str):
    """Validate CSS character encoding issues"""
    for pattern_info in CSS_CHARACTER_ENCODING_PATTERNS:
        matches = re.finditer(pattern_info['pattern'], content, re.MULTILINE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.add_issue(
                file_path=file_path,
                line=line_num,
                issue_type="css_character_encoding",
                severity=pattern_info['severity'],
                message=pattern_info['message'],
                suggestion=pattern_info['suggestion'],
                pattern=match.group(0)[:50]
            )
```

### 5.2 Pre-commit Hook Integration

```bash
#!/bin/bash
# pre-commit-css-validation.sh

# Validate CSS files for character encoding issues
echo "🔍 Validating CSS character encoding..."

# Find all CSS files
css_files=$(find . -name "*.css" -not -path "./_archive/*")

validation_failed=false

for file in $css_files; do
    # Check for BOM
    if [[ $(head -c 3 "$file" | xxd -p) == "efbbbf" ]]; then
        echo "❌ BOM detected in: $file"
        validation_failed=true
    fi

    # Check for raw Unicode in non-content properties
    if grep -P '[^\x00-\x7F]' "$file" | grep -v 'content:' | grep -v '/\*' > /dev/null; then
        echo "❌ Raw Unicode characters in: $file"
        validation_failed=true
    fi

    # Check for invalid calc operators
    if grep -P 'calc\([^)]*[–—×÷−]' "$file" > /dev/null; then
        echo "❌ Invalid calc() operators in: $file"
        validation_failed=true
    fi
done

if [ "$validation_failed" = true ]; then
    echo "🚨 CSS validation failed! Fix character encoding issues before commit."
    exit 1
else
    echo "✅ CSS character encoding validation passed!"
fi
```

---

## 6. Error Resolution Guide

### 6.1 Common Upload Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Invalid CSS syntax: Unexpected character` | Raw Unicode in selectors | Use ASCII-only characters in CSS selectors |
| `File contains invalid UTF-8 sequence` | BOM or encoding issues | Save as UTF-8 without BOM |
| `Invalid property name: Contains non-ASCII` | Unicode in CSS variables | Use ASCII characters in `--variable-name` |
| `CSS parsing error: Invalid calc()` | Unicode operators in calc() | Use ASCII `+ - * /` operators |
| `Invalid content value: Malformed character` | Raw Unicode in content property | Use `\Unicode-hex` escape sequences |
| `Invalid font-family declaration` | Unescaped quotes or Unicode | Properly escape font names |

### 6.2 Quick Fix Commands

```bash
# Remove BOM from CSS files
sed -i '1s/^\xEF\xBB\xBF//' *.css

# Convert Unicode operators to ASCII in calc()
sed -i 's/calc(\([^)]*\)–\([^)]*\))/calc(\1-\2)/g' *.css
sed -i 's/calc(\([^)]*\)—\([^)]*\))/calc(\1-\2)/g' *.css
sed -i 's/calc(\([^)]*\)×\([^)]*\))/calc(\1*\2)/g' *.css

# Find files with raw Unicode (excluding content properties)
grep -l '[^\x00-\x7F]' *.css | xargs grep -L 'content:'
```

---

## 7. Testing and Validation

### 7.1 Test Cases for CSS Character Validation

```css
/* TEST FILE: css-character-encoding-tests.css */

/* ❌ Should fail validation */
.test-unicode–selector { color: red; }
.test-bom﻿-issue { margin: 0; }
.test-calc { width: calc(100%–20px); }
.test-content { content: "→"; }
:root { --color-primário: blue; }

/* ✅ Should pass validation */
.test-ascii-selector { color: red; }
.test-clean { margin: 0; }
.test-calc-safe { width: calc(100% - 20px); }
.test-content-safe { content: "\2192"; }
:root { --color-primary: blue; }
```

### 7.2 Automated Testing Script

```python
def test_css_character_validation():
    """Test suite for CSS character encoding validation"""
    validator = ShopifyCSSValidator()

    # Test cases that should fail
    failing_css = '''
    .invalid–selector { color: red; }
    .calc-test { width: calc(100%–20px); }
    .content-test::before { content: "→"; }
    :root { --spañish-var: blue; }
    '''

    assert not validator.validate_css_file(failing_css, "test.css")
    assert len(validator.get_errors()) >= 4

    # Test cases that should pass
    passing_css = '''
    .valid-selector { color: red; }
    .calc-test { width: calc(100% - 20px); }
    .content-test::before { content: "\\2192"; }
    :root { --english-var: blue; }
    '''

    assert validator.validate_css_file(passing_css, "test.css")
    assert len(validator.get_errors()) == 0

    print("✅ All CSS character encoding tests passed!")

if __name__ == "__main__":
    test_css_character_validation()
```

---

## Conclusion

CSS character encoding issues represent a critical but often overlooked source of Shopify theme upload failures. The validation patterns and solutions documented here provide:

1. **Comprehensive Detection**: Regex patterns that identify all major categories of problematic characters
2. **Automated Validation**: Integration with existing validation systems for proactive error prevention
3. **Clear Solutions**: Specific fixes for each type of character encoding issue
4. **Best Practices**: Guidelines for writing Shopify-compatible CSS from the start

**Implementation Priority**:
1. Add character encoding validation to `ultimate-validator.py`
2. Create pre-commit hooks for automatic detection
3. Update CSS patterns in the code library to use safe character practices
4. Document these patterns in theme development guidelines

This investigation ensures that CSS character encoding will no longer be a hidden cause of theme upload failures in the Shopify development workflow.