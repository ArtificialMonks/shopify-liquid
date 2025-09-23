#!/usr/bin/env python3
"""
CSS CHARACTER ENCODING PATTERNS
Detection patterns and utilities for CSS character encoding validation.

This module provides regex patterns and utilities for detecting CSS character
encoding issues that cause Shopify theme upload failures.
"""

import re
from typing import Dict, List, Tuple

# CSS Character Encoding Detection Patterns
CSS_CHARACTER_PATTERNS = {
    'bom_detection': {
        'pattern': r'^\uFEFF',
        'message': 'CSS FILE CONTAINS BOM: File starts with Byte Order Mark',
        'severity': 'CRITICAL',
        'suggestion': 'Save file as UTF-8 without BOM',
        'category': 'encoding'
    },

    'illegal_selector_chars': {
        'pattern': r'[.#][^{\s]*[^\w\-_.#:()[\]>+~\s][^{\s]*\s*{',
        'message': 'ILLEGAL CSS SELECTOR: Contains invalid characters',
        'severity': 'CRITICAL',
        'suggestion': 'Use only alphanumeric, hyphen, underscore in selectors',
        'category': 'selector'
    },

    'unicode_calc_operators': {
        'pattern': r'calc\([^)]*[–—×÷−][^)]*\)',
        'message': 'INVALID CALC OPERATOR: Unicode math operators not allowed',
        'severity': 'CRITICAL',
        'suggestion': 'Use ASCII operators: + - * / in calc() expressions',
        'category': 'calc'
    },

    'raw_unicode_content': {
        'pattern': r'content\s*:\s*["\'][^"\']*[^\x00-\x7F][^"\']*["\']',
        'message': 'RAW UNICODE IN CONTENT: Use escaped Unicode sequences',
        'severity': 'ERROR',
        'suggestion': 'Replace with \\[Unicode-hex] escape sequences',
        'category': 'content'
    },

    'non_ascii_css_vars': {
        'pattern': r'--[^:]*[^\x00-\x7F][^:]*:',
        'message': 'NON-ASCII CSS VARIABLE: Variable names must be ASCII',
        'severity': 'ERROR',
        'suggestion': 'Use ASCII characters only in CSS variable names',
        'category': 'variables'
    },

    'malformed_unicode_escapes': {
        'pattern': r'\\[^0-9a-fA-F\r\n\f"\'\\]',
        'message': 'INVALID ESCAPE SEQUENCE: Malformed Unicode escape',
        'severity': 'ERROR',
        'suggestion': 'Use valid escape sequences: \\[0-9a-fA-F]{1,6}',
        'category': 'escapes'
    },

    'unescaped_font_quotes': {
        'pattern': r'font-family:[^;]*["\'][^"\']*["\'][^"\']*["\']',
        'message': 'UNESCAPED QUOTES IN FONT: Font family has unescaped quotes',
        'severity': 'WARNING',
        'suggestion': 'Properly escape or remove extra quotes in font names',
        'category': 'fonts'
    },

    'zero_width_characters': {
        'pattern': r'[\u200B-\u200D\uFEFF]',
        'message': 'INVISIBLE CHARACTERS: Zero-width or invisible characters found',
        'severity': 'ERROR',
        'suggestion': 'Remove invisible characters that may cause parsing issues',
        'category': 'invisible'
    },

    'incomplete_unicode_escapes': {
        'pattern': r'\\[0-9a-fA-F]{1,3}(?![0-9a-fA-F])',
        'message': 'INCOMPLETE UNICODE ESCAPE: Unicode escape sequence too short',
        'severity': 'WARNING',
        'suggestion': 'Complete Unicode escape sequences or pad with zeros',
        'category': 'escapes'
    },

    'unicode_in_comments': {
        'pattern': r'/\*[^*]*[^\x00-\x7F][^*]*\*/',
        'message': 'UNICODE IN COMMENTS: Non-ASCII characters in CSS comments',
        'severity': 'INFO',
        'suggestion': 'Consider using ASCII characters in comments for better compatibility',
        'category': 'comments'
    }
}

# Character replacement mappings for auto-fixing
UNICODE_OPERATOR_FIXES = {
    '–': '-',   # En-dash to hyphen
    '—': '-',   # Em-dash to hyphen
    '×': '*',   # Multiplication sign to asterisk
    '÷': '/',   # Division sign to slash
    '−': '-',   # Unicode minus to hyphen
    '⁄': '/',   # Fraction slash to regular slash
}

# Smart quote and punctuation fixes
UNICODE_PUNCTUATION_FIXES = {
    ''': "'",   # Left single quote
    ''': "'",   # Right single quote
    '"': '"',   # Left double quote
    '"': '"',   # Right double quote
    '…': '...',  # Horizontal ellipsis
    '–': '-',   # En-dash
    '—': '-',   # Em-dash
}

# Common Unicode character replacements for content properties
UNICODE_CONTENT_CHARS = {
    '→': '\\2192',  # Right arrow
    '←': '\\2190',  # Left arrow
    '↑': '\\2191',  # Up arrow
    '↓': '\\2193',  # Down arrow
    '★': '\\2605',  # Black star
    '☆': '\\2606',  # White star
    '♠': '\\2660',  # Spade suit
    '♣': '\\2663',  # Club suit
    '♥': '\\2665',  # Heart suit
    '♦': '\\2666',  # Diamond suit
    '✓': '\\2713',  # Check mark
    '✗': '\\2717',  # Ballot X
    '●': '\\25CF',  # Black circle
    '○': '\\25CB',  # White circle
    '■': '\\25A0',  # Black square
    '□': '\\25A1',  # White square
    '•': '\\2022',  # Bullet
    '‚': '\\201A',  # Single low-9 quotation mark
    '„': '\\201E',  # Double low-9 quotation mark
    '‹': '\\2039',  # Single left-pointing angle quotation mark
    '›': '\\203A',  # Single right-pointing angle quotation mark
}

# CSS property patterns that commonly have character encoding issues
PROBLEMATIC_CSS_PROPERTIES = [
    'content',
    'font-family',
    'quotes',
    'speak-as',
    'string-set'
]

def get_css_character_patterns() -> Dict:
    """Get all CSS character encoding detection patterns"""
    return CSS_CHARACTER_PATTERNS

def get_patterns_by_category(category: str) -> Dict:
    """Get patterns filtered by category"""
    return {
        name: pattern for name, pattern in CSS_CHARACTER_PATTERNS.items()
        if pattern.get('category') == category
    }

def get_patterns_by_severity(severity: str) -> Dict:
    """Get patterns filtered by severity level"""
    return {
        name: pattern for name, pattern in CSS_CHARACTER_PATTERNS.items()
        if pattern.get('severity') == severity
    }

def detect_encoding_issues(css_content: str) -> List[Dict]:
    """
    Detect all character encoding issues in CSS content.

    Returns:
        List of dictionaries containing issue details
    """
    issues = []

    for pattern_name, pattern_info in CSS_CHARACTER_PATTERNS.items():
        matches = re.finditer(pattern_info['pattern'], css_content, re.MULTILINE)

        for match in matches:
            line_num = css_content[:match.start()].count('\n') + 1
            column = match.start() - css_content.rfind('\n', 0, match.start())

            issues.append({
                'pattern_name': pattern_name,
                'line': line_num,
                'column': column,
                'match_text': match.group(0),
                'message': pattern_info['message'],
                'severity': pattern_info['severity'],
                'suggestion': pattern_info['suggestion'],
                'category': pattern_info['category'],
                'start_pos': match.start(),
                'end_pos': match.end()
            })

    return issues

def fix_unicode_operators(css_content: str) -> str:
    """Fix Unicode operators in CSS content"""
    for unicode_char, ascii_char in UNICODE_OPERATOR_FIXES.items():
        css_content = css_content.replace(unicode_char, ascii_char)
    return css_content

def fix_unicode_punctuation(css_content: str) -> str:
    """Fix Unicode punctuation characters"""
    for unicode_char, ascii_char in UNICODE_PUNCTUATION_FIXES.items():
        css_content = css_content.replace(unicode_char, ascii_char)
    return css_content

def escape_unicode_in_content(css_content: str) -> str:
    """Convert raw Unicode characters in content properties to escaped form"""
    def escape_content_property(match):
        property_value = match.group(0)

        for unicode_char, escape_seq in UNICODE_CONTENT_CHARS.items():
            property_value = property_value.replace(unicode_char, escape_seq)

        return property_value

    # Match content properties
    content_pattern = r'content\s*:\s*["\'][^"\']*["\']'
    return re.sub(content_pattern, escape_content_property, css_content)

def remove_bom(css_content: str) -> str:
    """Remove BOM (Byte Order Mark) from CSS content"""
    return css_content.lstrip('\uFEFF')

def remove_invisible_characters(css_content: str) -> str:
    """Remove invisible/zero-width characters"""
    invisible_chars = [
        '\u200B',  # Zero-width space
        '\u200C',  # Zero-width non-joiner
        '\u200D',  # Zero-width joiner
        '\uFEFF',  # Zero-width no-break space (BOM)
        '\u2060',  # Word joiner
    ]

    for char in invisible_chars:
        css_content = css_content.replace(char, '')

    return css_content

def sanitize_css_selectors(css_content: str) -> str:
    """Sanitize CSS selectors by removing problematic characters"""
    def fix_selector(match):
        selector = match.group(0)

        # Replace problematic characters in selectors
        fixes = {
            '–': '-',  # En-dash
            '—': '-',  # Em-dash
            ''': '',   # Left single quote
            ''': '',   # Right single quote
            '"': '',   # Left double quote
            '"': ''    # Right double quote
        }

        for bad_char, good_char in fixes.items():
            selector = selector.replace(bad_char, good_char)

        return selector

    # Match CSS selectors (basic pattern)
    selector_pattern = r'[.#][^{\s]*[^\w\-_.#:()[\]>+~\s][^{\s]*\s*{'
    return re.sub(selector_pattern, fix_selector, css_content)

def validate_css_variable_names(css_content: str) -> List[str]:
    """Validate CSS custom property names for ASCII compliance"""
    invalid_vars = []

    var_pattern = r'--([^:]+):'
    for match in re.finditer(var_pattern, css_content):
        var_name = match.group(1)

        # Check for non-ASCII characters
        if re.search(r'[^\x00-\x7F]', var_name):
            invalid_vars.append(var_name)

    return invalid_vars

def get_comprehensive_fix_report(css_content: str) -> Dict:
    """
    Generate a comprehensive report of all fixable character encoding issues.

    Returns:
        Dictionary with original content, fixed content, and detailed changes
    """
    original_content = css_content
    fixed_content = css_content
    changes = []

    # Apply fixes in order
    fixes_applied = [
        ('Remove BOM', remove_bom),
        ('Remove invisible characters', remove_invisible_characters),
        ('Fix Unicode operators', fix_unicode_operators),
        ('Fix Unicode punctuation', fix_unicode_punctuation),
        ('Escape Unicode in content', escape_unicode_in_content),
        ('Sanitize CSS selectors', sanitize_css_selectors)
    ]

    for fix_name, fix_function in fixes_applied:
        before_fix = fixed_content
        fixed_content = fix_function(fixed_content)

        if before_fix != fixed_content:
            changes.append({
                'fix_name': fix_name,
                'characters_changed': len(before_fix) - len(fixed_content),
                'description': f'Applied {fix_name.lower()}'
            })

    return {
        'original_content': original_content,
        'fixed_content': fixed_content,
        'changes_applied': changes,
        'total_changes': len(changes),
        'content_modified': original_content != fixed_content
    }

# Regex patterns for integration with existing validators
INTEGRATION_PATTERNS = {
    'ultimate_validator_patterns': [
        {
            'pattern': r'^\uFEFF',
            'message': 'CSS FILE CONTAINS BOM: File starts with Byte Order Mark',
            'severity': 'CRITICAL',
            'suggestion': 'Save file as UTF-8 without BOM'
        },
        {
            'pattern': r'calc\([^)]*[–—×÷−][^)]*\)',
            'message': 'INVALID CALC OPERATOR: Unicode math operators not allowed',
            'severity': 'CRITICAL',
            'suggestion': 'Use ASCII operators: + - * / in calc() expressions'
        },
        {
            'pattern': r'content\s*:\s*["\'][^"\']*[^\x00-\x7F][^"\']*["\']',
            'message': 'RAW UNICODE IN CONTENT: Use escaped Unicode sequences',
            'severity': 'ERROR',
            'suggestion': 'Replace with \\[Unicode-hex] escape sequences'
        },
        {
            'pattern': r'--[^:]*[^\x00-\x7F][^:]*:',
            'message': 'NON-ASCII CSS VARIABLE: Variable names must be ASCII',
            'severity': 'ERROR',
            'suggestion': 'Use ASCII characters only in CSS variable names'
        }
    ]
}

def get_integration_patterns() -> List[Dict]:
    """Get patterns formatted for integration with existing validators"""
    return INTEGRATION_PATTERNS['ultimate_validator_patterns']

# Test cases for validation
TEST_CASES = {
    'bom_test': '\uFEFFbody { margin: 0; }',
    'unicode_calc': '.width { width: calc(100%–20px); }',
    'unicode_content': '.arrow::before { content: "→"; }',
    'unicode_variable': ':root { --color-primário: blue; }',
    'invisible_chars': 'body { margin: 0​; }',  # Contains zero-width space
    'illegal_selector': '.my-section—invalid { color: red; }',
    'font_quotes': 'font-family: "Times "New" Roman", serif;'
}

def run_pattern_tests() -> bool:
    """Run tests on all patterns to ensure they work correctly"""
    test_results = []

    for test_name, test_content in TEST_CASES.items():
        issues = detect_encoding_issues(test_content)
        test_results.append({
            'test_name': test_name,
            'content': test_content,
            'issues_found': len(issues),
            'passed': len(issues) > 0
        })

    all_passed = all(result['passed'] for result in test_results)

    print("🧪 CSS Character Encoding Pattern Tests:")
    for result in test_results:
        status = "✅" if result['passed'] else "❌"
        print(f"  {status} {result['test_name']}: {result['issues_found']} issues")

    return all_passed

if __name__ == "__main__":
    # Run pattern tests
    print("Testing CSS character encoding detection patterns...")
    if run_pattern_tests():
        print("✅ All pattern tests passed!")
    else:
        print("❌ Some pattern tests failed!")