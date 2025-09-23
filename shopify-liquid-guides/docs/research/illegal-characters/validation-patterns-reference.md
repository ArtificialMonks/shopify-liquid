# Validation Patterns Reference

**Complete technical reference for character encoding detection patterns and validation algorithms**

*Extracted from comprehensive research analysis and production validation systems*

---

## Overview

This reference contains all regex patterns, detection algorithms, and validation rules for identifying character encoding issues in Shopify Liquid themes. Used by the ultimate-validator.py and standalone character encoding validation tools.

---

## 🔍 JavaScript Character Violation Patterns

### Context Separation Detection
```python
JAVASCRIPT_CONTEXT_VIOLATIONS = [
    {
        'pattern': r'{%\s*javascript\s*%}[^{]*{{\s*[^}]*\s*}}',
        'message': 'CRITICAL: Liquid code inside {% javascript %} tag causes upload failure',
        'severity': 'CRITICAL',
        'domain': 'context_separation',
        'fix': 'Use data attributes or configuration objects'
    },
    {
        'pattern': r'{%\s*javascript\s*%}[^{]*{%\s*[^%]*\s*%}',
        'message': 'CRITICAL: Liquid tags inside {% javascript %} block',
        'severity': 'CRITICAL',
        'domain': 'context_separation',
        'fix': 'Move Liquid logic outside JavaScript block'
    }
]
```

### Template Literal and Arrow Function Conflicts
```python
JAVASCRIPT_SYNTAX_VIOLATIONS = [
    {
        'pattern': r'<script[^>]*>[^<]*`[^`]*\{\{[^}]*\}\}[^`]*`',
        'message': 'Template literals with Liquid interpolation cause parsing errors',
        'severity': 'ERROR',
        'domain': 'javascript_encoding',
        'fix': 'Use data attributes for Liquid data injection'
    },
    {
        'pattern': r'=>\s*\{\{[^}]*\}\}',
        'message': 'Arrow functions with Liquid cause syntax conflicts',
        'severity': 'ERROR',
        'domain': 'javascript_encoding',
        'fix': 'Use traditional function syntax or data attributes'
    },
    {
        'pattern': r'const\s+\w*\`[^`]*\{\{[^}]*\}\}[^`]*\`',
        'message': 'Template literal assignment with Liquid interpolation',
        'severity': 'ERROR',
        'domain': 'javascript_encoding',
        'fix': 'Use JSON data injection instead'
    }
]
```

### JavaScript Identifier Violations
```python
JAVASCRIPT_IDENTIFIER_VIOLATIONS = [
    {
        'pattern': r'const\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in JavaScript identifier',
        'severity': 'WARNING',
        'domain': 'javascript_encoding',
        'fix': 'Use ASCII-only variable names'
    },
    {
        'pattern': r'let\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in JavaScript identifier',
        'severity': 'WARNING',
        'domain': 'javascript_encoding',
        'fix': 'Use ASCII-only variable names'
    },
    {
        'pattern': r'var\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in JavaScript identifier',
        'severity': 'WARNING',
        'domain': 'javascript_encoding',
        'fix': 'Use ASCII-only variable names'
    },
    {
        'pattern': r'function\s+[^\x00-\x7F]+\s*\(',
        'message': 'Non-ASCII characters in function name',
        'severity': 'WARNING',
        'domain': 'javascript_encoding',
        'fix': 'Use ASCII-only function names'
    }
]
```

---

## 🎨 CSS Character Violation Patterns

### Critical CSS Parsing Issues
```python
CSS_CRITICAL_VIOLATIONS = [
    {
        'pattern': r'calc\([^)]*[–—×÷][^)]*\)',
        'message': 'CRITICAL: Unicode operators in calc() break CSS parsing',
        'severity': 'CRITICAL',
        'domain': 'css_conflicts',
        'fix': 'Replace with ASCII operators: - * /',
        'chars_detected': ['–', '—', '×', '÷']
    },
    {
        'pattern': r'[\u200B-\u200D\uFEFF]',
        'message': 'CRITICAL: Invisible/zero-width characters break CSS parsing',
        'severity': 'CRITICAL',
        'domain': 'css_conflicts',
        'fix': 'Remove invisible characters completely',
        'chars_detected': ['\u200B', '\u200C', '\u200D', '\uFEFF']
    }
]
```

### CSS Content Property Issues
```python
CSS_CONTENT_VIOLATIONS = [
    {
        'pattern': r'content:\s*["\'][""''–—]["\']',
        'message': 'Smart quotes/dashes in content property cause encoding errors',
        'severity': 'ERROR',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII quotes or Unicode escapes \\201C \\201D',
        'chars_detected': ['"', '"', ''', ''', '–', '—']
    },
    {
        'pattern': r'content:\s*["\'][^"\']*[""''–—][^"\']*["\']',
        'message': 'Mixed smart quotes in content property',
        'severity': 'ERROR',
        'domain': 'css_conflicts',
        'fix': 'Replace with ASCII quotes or proper Unicode escapes'
    }
]
```

### CSS Selector Violations
```python
CSS_SELECTOR_VIOLATIONS = [
    {
        'pattern': r'\.[^\x00-\x7F\s{]+\s*\{',
        'message': 'Non-ASCII characters in CSS selector',
        'severity': 'WARNING',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII-only class names'
    },
    {
        'pattern': r'#[^\x00-\x7F\s{]+\s*\{',
        'message': 'Non-ASCII characters in CSS ID selector',
        'severity': 'WARNING',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII-only ID names'
    },
    {
        'pattern': r'\[[^\]]*[^\x00-\x7F][^\]]*\]',
        'message': 'Non-ASCII characters in attribute selector',
        'severity': 'WARNING',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII-only attribute values'
    }
]
```

### CSS Variable and Property Issues
```python
CSS_PROPERTY_VIOLATIONS = [
    {
        'pattern': r'--[^\x00-\x7F\s:]+\s*:',
        'message': 'Non-ASCII characters in CSS custom property name',
        'severity': 'ERROR',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII-only custom property names'
    },
    {
        'pattern': r'font-family:[^;]*[""''][^;]*[""'']',
        'message': 'Smart quotes in font-family declaration',
        'severity': 'WARNING',
        'domain': 'css_conflicts',
        'fix': 'Use ASCII quotes around font names'
    }
]
```

---

## 📝 HTML Entity Violation Patterns

### Critical Liquid Parsing Issues
```python
HTML_ENTITY_CRITICAL_VIOLATIONS = [
    {
        'pattern': r'\{\{[^}]*&(amp|lt|gt|quot|#\d+);[^}]*\}\}',
        'message': 'CRITICAL: HTML entities in Liquid expressions break parsing',
        'severity': 'CRITICAL',
        'domain': 'html_entities',
        'fix': 'Replace HTML entities with actual characters',
        'entities_detected': ['&amp;', '&lt;', '&gt;', '&quot;']
    },
    {
        'pattern': r'\{\%[^%]*&(amp|lt|gt|quot|#\d+);[^%]*\%\}',
        'message': 'CRITICAL: HTML entities in Liquid tags break parsing',
        'severity': 'CRITICAL',
        'domain': 'html_entities',
        'fix': 'Use actual characters in Liquid tags'
    }
]
```

### Security-Critical XSS Patterns
```python
HTML_ENTITY_SECURITY_VIOLATIONS = [
    {
        'pattern': r'customer\.[^|}\s]+(?!\s*\|\s*escape)',
        'message': 'SECURITY: Unescaped customer data creates XSS vulnerability',
        'severity': 'CRITICAL',
        'domain': 'html_entities',
        'fix': 'Add | escape filter to customer data'
    },
    {
        'pattern': r'comment\.body[^|}\s]*(?!\s*\|\s*escape)',
        'message': 'SECURITY: Unescaped comment content creates XSS vulnerability',
        'severity': 'CRITICAL',
        'domain': 'html_entities',
        'fix': 'Add | escape filter to comment body'
    },
    {
        'pattern': r'form\.errors[^|}\s]*(?!\s*\|\s*escape)',
        'message': 'SECURITY: Unescaped form errors create XSS vulnerability',
        'severity': 'CRITICAL',
        'domain': 'html_entities',
        'fix': 'Add | escape filter to form errors'
    },
    {
        'pattern': r'\{\{\s*[^}]*\|\s*raw\s*\}\}',
        'message': 'SECURITY: Raw filter creates XSS vulnerability',
        'severity': 'ERROR',
        'domain': 'html_entities',
        'fix': 'Remove | raw filter unless absolutely necessary'
    }
]
```

### Schema JSON Entity Issues
```python
HTML_ENTITY_SCHEMA_VIOLATIONS = [
    {
        'pattern': r'"[^"]*&(amp|lt|gt|quot|#\d+);[^"]*":\s*["\'][^"\']*["\']',
        'message': 'HTML entities in JSON schema break parsing',
        'severity': 'ERROR',
        'domain': 'html_entities',
        'fix': 'Replace HTML entities with actual characters in schema'
    },
    {
        'pattern': r'"[^"]*[""''–—][^"]*":\s*["\'][^"\']*["\']',
        'message': 'Smart quotes in JSON schema break parsing',
        'severity': 'ERROR',
        'domain': 'html_entities',
        'fix': 'Replace smart quotes with ASCII quotes in schema'
    }
]
```

### Liquid Variable Encoding Issues
```python
HTML_ENTITY_VARIABLE_VIOLATIONS = [
    {
        'pattern': r'\{\%\s*assign\s+[^\x00-\x7F]+\s*=',
        'message': 'Non-ASCII characters in Liquid variable name',
        'severity': 'ERROR',
        'domain': 'html_entities',
        'fix': 'Use ASCII-only variable names'
    },
    {
        'pattern': r'\{\%\s*for\s+[^\x00-\x7F]+\s+in',
        'message': 'Non-ASCII characters in Liquid loop variable',
        'severity': 'ERROR',
        'domain': 'html_entities',
        'fix': 'Use ASCII-only loop variable names'
    }
]
```

---

## 💻 CLI Platform Violation Patterns

### Critical Platform Compatibility Issues
```python
CLI_PLATFORM_CRITICAL_VIOLATIONS = [
    {
        'pattern': r'^\ufeff',
        'message': 'CRITICAL: UTF-8 BOM detected - causes CLI upload failure',
        'severity': 'CRITICAL',
        'domain': 'cli_limitations',
        'fix': 'Save file as UTF-8 without BOM',
        'detection_method': 'file_start_bytes'
    },
    {
        'pattern': r'[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]',
        'message': 'CRITICAL: Control characters cause CLI parsing errors',
        'severity': 'CRITICAL',
        'domain': 'cli_limitations',
        'fix': 'Remove control characters (except tab, newline, CR)',
        'chars_detected': 'control_characters'
    }
]
```

### CLI Encoding Compatibility Issues
```python
CLI_PLATFORM_ENCODING_VIOLATIONS = [
    {
        'pattern': r'[""'']',
        'message': 'Smart quotes in code context cause encoding issues',
        'severity': 'WARNING',
        'domain': 'cli_limitations',
        'fix': 'Replace with ASCII quotes',
        'chars_detected': ['"', '"', ''', ''']
    },
    {
        'pattern': r'[–—]',
        'message': 'Typography dashes may cause platform encoding problems',
        'severity': 'WARNING',
        'domain': 'cli_limitations',
        'fix': 'Replace with ASCII hyphen',
        'chars_detected': ['–', '—']
    },
    {
        'pattern': r'[\u0080-\u009F]',
        'message': 'High control characters cause platform issues',
        'severity': 'ERROR',
        'domain': 'cli_limitations',
        'fix': 'Remove or replace high control characters'
    }
]
```

---

## 🔧 Advanced Detection Algorithms

### Context-Aware Pattern Validation
```python
class ContextAwareValidator:
    """Advanced validation with context understanding"""

    def validate_javascript_context(self, content):
        """Detect Liquid inside JavaScript contexts"""
        javascript_blocks = []

        # Find all {% javascript %} blocks
        js_pattern = r'{%\s*javascript\s*%}(.*?){%\s*endjavascript\s*%}'
        js_matches = re.finditer(js_pattern, content, re.DOTALL)

        for match in js_matches:
            js_content = match.group(1)
            start_pos = match.start()

            # Check for Liquid inside JavaScript
            liquid_in_js = re.findall(r'\{\{[^}]*\}\}|\{\%[^%]*\%\}', js_content)
            if liquid_in_js:
                javascript_blocks.append({
                    'type': 'liquid_in_javascript',
                    'position': start_pos,
                    'content': js_content,
                    'liquid_found': liquid_in_js,
                    'severity': 'CRITICAL'
                })

        return javascript_blocks

    def validate_css_calc_expressions(self, content):
        """Detect Unicode operators in CSS calc() expressions"""
        calc_violations = []

        # Find all calc() expressions
        calc_pattern = r'calc\(([^)]+)\)'
        calc_matches = re.finditer(calc_pattern, content)

        for match in calc_matches:
            calc_content = match.group(1)
            position = match.start()

            # Check for Unicode operators
            unicode_operators = ['–', '—', '×', '÷']
            found_operators = [op for op in unicode_operators if op in calc_content]

            if found_operators:
                calc_violations.append({
                    'type': 'unicode_calc_operators',
                    'position': position,
                    'expression': calc_content,
                    'operators_found': found_operators,
                    'severity': 'CRITICAL'
                })

        return calc_violations

    def validate_liquid_security(self, content):
        """Detect security vulnerabilities in Liquid expressions"""
        security_issues = []

        # Find unescaped user content patterns
        user_content_patterns = [
            r'\{\{\s*customer\.[^|}\s]+(?!\s*\|\s*escape)',
            r'\{\{\s*comment\.body[^|}\s]*(?!\s*\|\s*escape)',
            r'\{\{\s*form\.errors[^|}\s]*(?!\s*\|\s*escape)'
        ]

        for pattern in user_content_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                security_issues.append({
                    'type': 'unescaped_user_content',
                    'position': match.start(),
                    'expression': match.group(0),
                    'severity': 'CRITICAL'
                })

        return security_issues
```

### Binary File Analysis for BOM Detection
```python
class BinaryFileAnalyzer:
    """Analyze files at binary level for encoding issues"""

    def detect_bom(self, file_path):
        """Detect Byte Order Mark at file start"""
        with open(file_path, 'rb') as f:
            first_bytes = f.read(4)

        bom_signatures = {
            b'\xef\xbb\xbf': 'UTF-8 BOM',
            b'\xff\xfe': 'UTF-16 LE BOM',
            b'\xfe\xff': 'UTF-16 BE BOM',
            b'\xff\xfe\x00\x00': 'UTF-32 LE BOM',
            b'\x00\x00\xfe\xff': 'UTF-32 BE BOM'
        }

        for signature, bom_type in bom_signatures.items():
            if first_bytes.startswith(signature):
                return {
                    'bom_detected': True,
                    'bom_type': bom_type,
                    'severity': 'CRITICAL' if bom_type == 'UTF-8 BOM' else 'ERROR'
                }

        return {'bom_detected': False}

    def detect_control_characters(self, file_path):
        """Detect control characters in file content"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Check for control characters (excluding tab, newline, CR)
            control_chars = []
            allowed_control = {0x09, 0x0A, 0x0D}  # Tab, LF, CR

            for i, byte in enumerate(content):
                if byte < 0x20 and byte not in allowed_control:
                    control_chars.append({
                        'position': i,
                        'char_code': byte,
                        'char_name': f'\\x{byte:02x}'
                    })
                elif 0x7F <= byte <= 0x9F:
                    control_chars.append({
                        'position': i,
                        'char_code': byte,
                        'char_name': f'\\x{byte:02x}'
                    })

            return control_chars

        except Exception:
            return []
```

---

## 📊 Pattern Severity Classification

### Severity Level Definitions
```python
class SeverityLevels:
    """Character encoding issue severity classification"""

    CRITICAL = 'CRITICAL'  # Blocks theme upload
    ERROR = 'ERROR'        # Causes display/function issues
    WARNING = 'WARNING'    # Best practice violations
    INFO = 'INFO'          # Recommendations

    SEVERITY_WEIGHTS = {
        'CRITICAL': 1000,
        'ERROR': 100,
        'WARNING': 10,
        'INFO': 1
    }

    @classmethod
    def get_upload_blockers(cls):
        """Patterns that prevent theme upload"""
        return [
            'unicode_calc_operators',
            'liquid_in_javascript',
            'html_entities_in_liquid',
            'bom_detected',
            'control_characters'
        ]

    @classmethod
    def get_security_critical(cls):
        """Patterns that create security vulnerabilities"""
        return [
            'unescaped_user_content',
            'unescaped_customer_data',
            'raw_filter_usage',
            'script_context_injection'
        ]
```

### Pattern Integration Matrix
```python
PATTERN_INTEGRATION_MATRIX = {
    'javascript_encoding': {
        'patterns': JAVASCRIPT_CONTEXT_VIOLATIONS +
                   JAVASCRIPT_SYNTAX_VIOLATIONS +
                   JAVASCRIPT_IDENTIFIER_VIOLATIONS,
        'auto_fix': True,
        'requires_manual_review': ['context_separation']
    },
    'css_conflicts': {
        'patterns': CSS_CRITICAL_VIOLATIONS +
                   CSS_CONTENT_VIOLATIONS +
                   CSS_SELECTOR_VIOLATIONS +
                   CSS_PROPERTY_VIOLATIONS,
        'auto_fix': True,
        'requires_manual_review': []
    },
    'html_entities': {
        'patterns': HTML_ENTITY_CRITICAL_VIOLATIONS +
                   HTML_ENTITY_SECURITY_VIOLATIONS +
                   HTML_ENTITY_SCHEMA_VIOLATIONS +
                   HTML_ENTITY_VARIABLE_VIOLATIONS,
        'auto_fix': True,
        'requires_manual_review': ['security_vulnerabilities']
    },
    'cli_limitations': {
        'patterns': CLI_PLATFORM_CRITICAL_VIOLATIONS +
                   CLI_PLATFORM_ENCODING_VIOLATIONS,
        'auto_fix': True,
        'requires_manual_review': []
    }
}
```

---

## 🚀 Performance Optimization Patterns

### Efficient Pattern Compilation
```python
class OptimizedPatternValidator:
    """Performance-optimized pattern validation"""

    def __init__(self):
        # Pre-compile patterns for performance
        self.compiled_patterns = {}
        self._compile_all_patterns()

    def _compile_all_patterns(self):
        """Compile all regex patterns once"""
        all_patterns = (
            JAVASCRIPT_CONTEXT_VIOLATIONS +
            CSS_CRITICAL_VIOLATIONS +
            HTML_ENTITY_CRITICAL_VIOLATIONS +
            CLI_PLATFORM_CRITICAL_VIOLATIONS
        )

        for pattern_def in all_patterns:
            pattern_id = pattern_def.get('domain', '') + '_' + str(hash(pattern_def['pattern']))
            self.compiled_patterns[pattern_id] = {
                'regex': re.compile(pattern_def['pattern']),
                'definition': pattern_def
            }

    def fast_validate(self, content, pattern_domains=None):
        """High-performance validation with domain filtering"""
        issues = []

        for pattern_id, pattern_data in self.compiled_patterns.items():
            if pattern_domains and pattern_data['definition']['domain'] not in pattern_domains:
                continue

            matches = pattern_data['regex'].finditer(content)
            for match in matches:
                issues.append({
                    'pattern_id': pattern_id,
                    'position': match.start(),
                    'match': match.group(0),
                    'definition': pattern_data['definition']
                })

        return issues
```

---

## 📋 Pattern Usage Examples

### Integration with Ultimate Validator
```python
from validation_patterns_reference import *

class CharacterEncodingValidator:
    def __init__(self):
        self.pattern_validator = OptimizedPatternValidator()

    def validate_file_content(self, content, file_path):
        """Validate file content using all pattern categories"""
        all_issues = []

        # JavaScript patterns
        js_issues = self.pattern_validator.fast_validate(
            content,
            pattern_domains=['context_separation', 'javascript_encoding']
        )
        all_issues.extend(js_issues)

        # CSS patterns
        css_issues = self.pattern_validator.fast_validate(
            content,
            pattern_domains=['css_conflicts']
        )
        all_issues.extend(css_issues)

        # HTML entity patterns
        html_issues = self.pattern_validator.fast_validate(
            content,
            pattern_domains=['html_entities']
        )
        all_issues.extend(html_issues)

        # CLI platform patterns
        cli_issues = self.pattern_validator.fast_validate(
            content,
            pattern_domains=['cli_limitations']
        )
        all_issues.extend(cli_issues)

        return self._classify_and_sort_issues(all_issues)
```

### Standalone Pattern Testing
```python
def test_individual_pattern(pattern_definition, test_content):
    """Test a single pattern against content"""
    regex = re.compile(pattern_definition['pattern'])
    matches = list(regex.finditer(test_content))

    return {
        'pattern': pattern_definition['pattern'],
        'message': pattern_definition['message'],
        'matches_found': len(matches),
        'match_positions': [m.start() for m in matches],
        'matched_content': [m.group(0) for m in matches]
    }

# Example usage
test_content = 'calc(100% – 20px)'
result = test_individual_pattern(CSS_CRITICAL_VIOLATIONS[0], test_content)
print(f"Pattern found {result['matches_found']} issues")
```

---

*This reference serves as the complete technical foundation for character encoding validation across all Shopify Liquid development workflows.*