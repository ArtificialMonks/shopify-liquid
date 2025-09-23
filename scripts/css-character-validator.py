#!/usr/bin/env python3
"""
CSS CHARACTER ENCODING VALIDATOR
Specialized validator for CSS character encoding issues that break Shopify theme uploads.

This validator detects and reports:
- Illegal characters in CSS selectors
- Unicode character encoding problems
- Invalid calc() expressions with problematic operators
- Font-family declarations with encoding issues
- CSS content properties with illegal characters
- BOM and invisible character issues

Usage:
  python3 css-character-validator.py path/to/css/files/
  python3 css-character-validator.py --file specific.css
  python3 css-character-validator.py --fix path/to/css/  # Auto-fix issues
"""

import re
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class CSSCharacterIssue:
    file_path: str
    line: int
    column: int
    issue_type: str
    severity: Severity
    message: str
    suggestion: str
    pattern: str
    original_text: str = ""
    fixed_text: str = ""

class CSSCharacterValidator:
    """
    Comprehensive CSS character encoding validator for Shopify theme compatibility.

    Detects character encoding issues that cause theme upload failures and provides
    automatic fixes for common problems.
    """

    def __init__(self, auto_fix: bool = False):
        self.issues: List[CSSCharacterIssue] = []
        self.files_scanned = 0
        self.files_fixed = 0
        self.auto_fix = auto_fix

        # Validation patterns for different types of character issues
        self.validation_patterns = self._get_validation_patterns()

    def _get_validation_patterns(self) -> List[Dict]:
        """Define validation patterns for CSS character encoding issues"""
        return [
            {
                'name': 'bom_detection',
                'pattern': r'^\uFEFF',
                'message': 'CSS FILE CONTAINS BOM: File starts with Byte Order Mark',
                'severity': Severity.CRITICAL,
                'suggestion': 'Save file as UTF-8 without BOM',
                'fix_function': self._fix_bom
            },
            {
                'name': 'illegal_selector_chars',
                'pattern': r'[.#][^{\s]*[^\w\-_.#:()[\]>+~\s][^{\s]*\s*{',
                'message': 'ILLEGAL CSS SELECTOR: Contains invalid characters',
                'severity': Severity.CRITICAL,
                'suggestion': 'Use only alphanumeric, hyphen, underscore in selectors',
                'fix_function': self._fix_selector_chars
            },
            {
                'name': 'unicode_calc_operators',
                'pattern': r'calc\([^)]*[–—×÷−][^)]*\)',
                'message': 'INVALID CALC OPERATOR: Unicode math operators not allowed',
                'severity': Severity.CRITICAL,
                'suggestion': 'Use ASCII operators: + - * / in calc() expressions',
                'fix_function': self._fix_calc_operators
            },
            {
                'name': 'raw_unicode_content',
                'pattern': r'content\s*:\s*["\'][^"\']*[^\x00-\x7F][^"\']*["\']',
                'message': 'RAW UNICODE IN CONTENT: Use escaped Unicode sequences',
                'severity': Severity.ERROR,
                'suggestion': 'Replace with \\[Unicode-hex] escape sequences',
                'fix_function': self._fix_unicode_content
            },
            {
                'name': 'non_ascii_css_vars',
                'pattern': r'--[^:]*[^\x00-\x7F][^:]*:',
                'message': 'NON-ASCII CSS VARIABLE: Variable names must be ASCII',
                'severity': Severity.ERROR,
                'suggestion': 'Use ASCII characters only in CSS variable names',
                'fix_function': self._fix_css_variable_names
            },
            {
                'name': 'malformed_unicode_escapes',
                'pattern': r'\\[^0-9a-fA-F\r\n\f"\'\\]',
                'message': 'INVALID ESCAPE SEQUENCE: Malformed Unicode escape',
                'severity': Severity.ERROR,
                'suggestion': 'Use valid escape sequences: \\[0-9a-fA-F]{1,6}',
                'fix_function': self._fix_malformed_escapes
            },
            {
                'name': 'unescaped_font_quotes',
                'pattern': r'font-family:[^;]*["\'][^"\']*["\'][^"\']*["\']',
                'message': 'UNESCAPED QUOTES IN FONT: Font family has unescaped quotes',
                'severity': Severity.WARNING,
                'suggestion': 'Properly escape or remove extra quotes in font names',
                'fix_function': self._fix_font_quotes
            },
            {
                'name': 'unicode_outside_strings',
                'pattern': r'[^\x00-\x7F]',
                'message': 'RAW UNICODE CHARACTER: Unicode character found',
                'severity': Severity.WARNING,
                'suggestion': 'Escape Unicode characters or use ASCII alternatives',
                'fix_function': self._fix_unicode_outside_strings
            },
            {
                'name': 'zero_width_characters',
                'pattern': r'[\u200B-\u200D\uFEFF]',
                'message': 'INVISIBLE CHARACTERS: Zero-width or invisible characters found',
                'severity': Severity.ERROR,
                'suggestion': 'Remove invisible characters that may cause parsing issues',
                'fix_function': self._fix_invisible_chars
            }
        ]

    def validate_css_file(self, file_path: Path) -> bool:
        """Validate a single CSS file for character encoding issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            self._add_issue(
                file_path=str(file_path),
                line=0,
                column=0,
                issue_type="encoding_error",
                severity=Severity.CRITICAL,
                message="FILE ENCODING ERROR: Cannot read file as UTF-8",
                suggestion="Convert file to UTF-8 encoding",
                pattern="",
                original_text=""
            )
            return False
        except Exception as e:
            self._add_issue(
                file_path=str(file_path),
                line=0,
                column=0,
                issue_type="file_error",
                severity=Severity.CRITICAL,
                message=f"FILE READ ERROR: {str(e)}",
                suggestion="Check file permissions and path",
                pattern="",
                original_text=""
            )
            return False

        self.files_scanned += 1
        original_content = content

        # Run all validation patterns
        for pattern_info in self.validation_patterns:
            content = self._validate_pattern(content, str(file_path), pattern_info)

        # If auto-fix is enabled and content was modified, write back
        if self.auto_fix and content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_fixed += 1
                print(f"✅ Fixed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to write fixed file {file_path}: {e}")

        # Return True if no critical issues found
        file_issues = [i for i in self.issues if i.file_path == str(file_path)]
        critical_issues = [i for i in file_issues if i.severity in [Severity.CRITICAL, Severity.ERROR]]

        return len(critical_issues) == 0

    def _validate_pattern(self, content: str, file_path: str, pattern_info: Dict) -> str:
        """Validate content against a specific pattern and optionally fix issues"""
        pattern = pattern_info['pattern']
        matches = list(re.finditer(pattern, content, re.MULTILINE))

        # Process matches in reverse order for auto-fixing
        for match in reversed(matches):
            line_num = content[:match.start()].count('\n') + 1
            column = match.start() - content.rfind('\n', 0, match.start())

            original_text = match.group(0)
            fixed_text = original_text

            # Apply fix if auto-fix is enabled
            if self.auto_fix and 'fix_function' in pattern_info:
                try:
                    fixed_text = pattern_info['fix_function'](original_text)
                    if fixed_text != original_text:
                        # Replace in content
                        content = content[:match.start()] + fixed_text + content[match.end():]
                except Exception as e:
                    print(f"Warning: Failed to auto-fix {pattern_info['name']} in {file_path}: {e}")
                    fixed_text = original_text

            self._add_issue(
                file_path=file_path,
                line=line_num,
                column=column,
                issue_type=pattern_info['name'],
                severity=pattern_info['severity'],
                message=pattern_info['message'],
                suggestion=pattern_info['suggestion'],
                pattern=original_text[:50] + "..." if len(original_text) > 50 else original_text,
                original_text=original_text,
                fixed_text=fixed_text
            )

        return content

    def _add_issue(self, file_path: str, line: int, column: int, issue_type: str,
                   severity: Severity, message: str, suggestion: str, pattern: str,
                   original_text: str, fixed_text: str = ""):
        """Add a validation issue to the results"""
        self.issues.append(CSSCharacterIssue(
            file_path=file_path,
            line=line,
            column=column,
            issue_type=issue_type,
            severity=severity,
            message=message,
            suggestion=suggestion,
            pattern=pattern,
            original_text=original_text,
            fixed_text=fixed_text
        ))

    # Fix functions for auto-repair
    def _fix_bom(self, text: str) -> str:
        """Remove BOM character"""
        return text.lstrip('\uFEFF')

    def _fix_selector_chars(self, text: str) -> str:
        """Fix illegal characters in CSS selectors"""
        # Replace common problematic characters
        fixes = {
            '–': '-',  # En-dash
            '—': '-',  # Em-dash
            ''': '',   # Left single quote
            ''': '',   # Right single quote
            '"': '',   # Left double quote
            '"': ''    # Right double quote
        }

        for bad_char, good_char in fixes.items():
            text = text.replace(bad_char, good_char)

        return text

    def _fix_calc_operators(self, text: str) -> str:
        """Fix Unicode operators in calc() expressions"""
        unicode_operators = {
            '–': '-',  # En-dash to hyphen
            '—': '-',  # Em-dash to hyphen
            '×': '*',  # Multiplication sign to asterisk
            '÷': '/',  # Division sign to slash
            '−': '-',  # Unicode minus to hyphen
        }

        for unicode_char, ascii_char in unicode_operators.items():
            text = text.replace(unicode_char, ascii_char)

        return text

    def _fix_unicode_content(self, text: str) -> str:
        """Convert raw Unicode in content properties to escaped form"""
        def escape_unicode_chars(match):
            quote_char = match.group(1) if match.group(1) else '"'
            content_value = match.group(2)

            escaped_value = ''
            for char in content_value:
                if ord(char) > 127:
                    escaped_value += f'\\{ord(char):04X}'
                else:
                    escaped_value += char

            return f'content: {quote_char}{escaped_value}{quote_char}'

        # Match content properties with quotes
        pattern = r'content\s*:\s*(["\'])([^"\']*)\1'
        return re.sub(pattern, escape_unicode_chars, text)

    def _fix_css_variable_names(self, text: str) -> str:
        """Fix non-ASCII characters in CSS variable names"""
        def fix_variable_name(match):
            var_name = match.group(1)
            # Replace non-ASCII chars with ASCII equivalents or remove them
            ascii_name = ''
            for char in var_name:
                if ord(char) <= 127:
                    ascii_name += char
                else:
                    # Basic transliteration for common characters
                    replacements = {
                        'á': 'a', 'à': 'a', 'ä': 'a', 'â': 'a',
                        'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
                        'í': 'i', 'ì': 'i', 'ï': 'i', 'î': 'i',
                        'ó': 'o', 'ò': 'o', 'ö': 'o', 'ô': 'o',
                        'ú': 'u', 'ù': 'u', 'ü': 'u', 'û': 'u',
                        'ñ': 'n', 'ç': 'c'
                    }
                    ascii_name += replacements.get(char.lower(), '')

            return f'--{ascii_name}:'

        pattern = r'--([^:]*[^\x00-\x7F][^:]*):'
        return re.sub(pattern, fix_variable_name, text)

    def _fix_malformed_escapes(self, text: str) -> str:
        """Fix malformed Unicode escape sequences"""
        # Remove invalid escape sequences
        return re.sub(r'\\[^0-9a-fA-F\r\n\f"\'\\]', '', text)

    def _fix_font_quotes(self, text: str) -> str:
        """Fix unescaped quotes in font-family declarations"""
        def fix_font_family(match):
            font_decl = match.group(0)
            # Remove extra quotes, keeping only outer quotes for each font name
            # This is a simple fix - more complex cases may need manual review
            return re.sub(r'(["\'])[^"\']*["\'][^"\']*(["\'])', r'\1font-name\2', font_decl)

        pattern = r'font-family:[^;]*["\'][^"\']*["\'][^"\']*["\'][^;]*'
        return re.sub(pattern, fix_font_family, text)

    def _fix_unicode_outside_strings(self, text: str) -> str:
        """Remove or escape Unicode characters outside of string values"""
        # This is a conservative fix that only removes common problematic chars
        problematic_chars = ['–', '—', ''', ''', '"', '"']
        for char in problematic_chars:
            text = text.replace(char, '')
        return text

    def _fix_invisible_chars(self, text: str) -> str:
        """Remove invisible/zero-width characters"""
        invisible_chars = [
            '\u200B',  # Zero-width space
            '\u200C',  # Zero-width non-joiner
            '\u200D',  # Zero-width joiner
            '\uFEFF',  # Zero-width no-break space (BOM)
        ]

        for char in invisible_chars:
            text = text.replace(char, '')

        return text

    def scan_directory(self, directory_path: Path) -> bool:
        """Scan all CSS files in a directory"""
        css_files = []

        # Find all CSS files recursively
        for file_path in directory_path.rglob("*.css"):
            # Skip archived files
            if '_archive' not in str(file_path):
                css_files.append(file_path)

        if not css_files:
            print(f"❌ No CSS files found in {directory_path}")
            return False

        print(f"🔍 CSS CHARACTER ENCODING VALIDATOR")
        print(f"📄 Found {len(css_files)} CSS files")
        if self.auto_fix:
            print(f"🔧 Auto-fix mode enabled")
        print("=" * 60)

        success_count = 0
        for i, file_path in enumerate(css_files, 1):
            print(f"[{i}/{len(css_files)}] {file_path.name}")
            if self.validate_css_file(file_path):
                success_count += 1
                print("  ✅ PASSED")
            else:
                print("  ❌ FAILED")

        return self.generate_report(success_count, len(css_files))

    def generate_report(self, success_count: int = None, total_files: int = None) -> bool:
        """Generate final validation report"""
        print("\n" + "=" * 60)
        print("🎯 CSS CHARACTER ENCODING REPORT")
        print("=" * 60)

        if total_files:
            print(f"📊 SCAN SUMMARY:")
            print(f"  • Files scanned: {total_files}")
            print(f"  • Files passed: {success_count}")
            print(f"  • Files failed: {total_files - success_count}")
            if self.auto_fix:
                print(f"  • Files fixed: {self.files_fixed}")

        # Group issues by severity
        critical_issues = [i for i in self.issues if i.severity == Severity.CRITICAL]
        error_issues = [i for i in self.issues if i.severity == Severity.ERROR]
        warning_issues = [i for i in self.issues if i.severity == Severity.WARNING]

        print(f"\n📈 ISSUE SUMMARY:")
        print(f"  • Critical issues: {len(critical_issues)}")
        print(f"  • Error issues: {len(error_issues)}")
        print(f"  • Warning issues: {len(warning_issues)}")

        # Show detailed issues
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
            self._show_issues(critical_issues[:10])

        if error_issues:
            print(f"\n⚠️ ERROR ISSUES ({len(error_issues)}):")
            self._show_issues(error_issues[:5])

        # Issue type breakdown
        if self.issues:
            issue_types = {}
            for issue in self.issues:
                issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

            print(f"\n🔍 ISSUE BREAKDOWN:")
            for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {issue_type}: {count}")

        # Final verdict
        total_critical = len(critical_issues) + len(error_issues)

        if total_critical == 0:
            print(f"\n✅ ALL CSS CHARACTER ENCODING CHECKS PASSED!")
            print(f"🚀 CSS files are ready for Shopify theme upload")
            return True
        else:
            print(f"\n🚨 CSS CHARACTER ENCODING VALIDATION FAILED!")
            print(f"❌ {total_critical} critical/error issue(s) found")
            if self.auto_fix:
                print(f"🔧 Run with --fix to automatically repair issues")
            else:
                print(f"🔧 Some issues were automatically fixed")
            return False

    def _show_issues(self, issues: List[CSSCharacterIssue]):
        """Display detailed issue information"""
        for issue in issues:
            filename = Path(issue.file_path).name
            print(f"❌ {filename}:{issue.line}:{issue.column}")
            print(f"   {issue.message}")
            print(f"   💡 {issue.suggestion}")
            if issue.fixed_text and issue.fixed_text != issue.original_text:
                print(f"   🔧 Fixed: {issue.original_text[:30]}... → {issue.fixed_text[:30]}...")
            print()

def main():
    parser = argparse.ArgumentParser(
        description="CSS Character Encoding Validator for Shopify Themes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 css-character-validator.py .                    # Validate current directory
  python3 css-character-validator.py --file style.css    # Validate single file
  python3 css-character-validator.py --fix ./assets/     # Auto-fix issues
  python3 css-character-validator.py --all               # Validate code library

This validator identifies CSS character encoding issues that cause
Shopify theme upload failures:
- BOM characters and encoding problems
- Illegal characters in CSS selectors
- Unicode operators in calc() expressions
- Raw Unicode in content properties
- Non-ASCII CSS variable names
- Malformed escape sequences
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to CSS file or directory to validate'
    )

    parser.add_argument(
        '--file',
        help='Validate a specific CSS file'
    )

    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix detected issues'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate entire code library'
    )

    args = parser.parse_args()

    validator = CSSCharacterValidator(auto_fix=args.fix)

    # Determine target path
    if args.all:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        target_path = project_root / "shopify-liquid-guides"
    elif args.file:
        target_path = Path(args.file)
    elif args.path:
        target_path = Path(args.path)
    else:
        target_path = Path.cwd()

    if not target_path.exists():
        print(f"❌ Path not found: {target_path}")
        return 1

    # Validate file or directory
    if target_path.is_file() and target_path.suffix == '.css':
        success = validator.validate_css_file(target_path)
        validator.generate_report()
        return 0 if success else 1
    elif target_path.is_dir():
        success = validator.scan_directory(target_path)
        return 0 if success else 1
    else:
        print(f"❌ Invalid path or not a CSS file: {target_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())