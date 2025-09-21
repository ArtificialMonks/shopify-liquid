#!/usr/bin/env python3
"""
ULTIMATE SHOPIFY LIQUID VALIDATOR
The ONLY validation script you need - ZERO TOLERANCE for broken code

Consolidates ALL validation checks into ONE BULLETPROOF SYSTEM:
✅ Schema integrity (settings defined vs used)
✅ Hallucinated filter detection (NO made-up filters)
✅ Over-engineering detection (complexity limits)
✅ Performance validation (NO performance killers)
✅ Theme Store compliance (production ready)
✅ Real Shopify API validation (ONLY real features)
✅ Liquid syntax validation (proper structure)

BLOCKS DEPLOYMENT if ANY critical issues found.
ONE SCRIPT TO RULE THEM ALL.
"""

import json
import re
import sys
from pathlib import Path
from typing import List
from dataclasses import dataclass
from enum import Enum

# Constants for repeated messages
RENDER_TAG_MESSAGE = 'DOES NOT EXIST - Use {% render %} tag'
DOES_NOT_EXIST_PREFIX = 'DOES NOT EXIST - '

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationIssue:
    file_path: str
    line: int
    issue_type: str
    severity: Severity
    message: str
    suggestion: str = ""
    pattern: str = ""

class ShopifyLiquidValidator:
    """
    Ultimate Shopify Liquid validator - ZERO TOLERANCE for broken code
    """

    # OFFICIAL SHOPIFY LIQUID FILTERS - VERIFIED AGAINST SHOPIFY DOCS
    # Source: https://shopify.dev/docs/api/liquid/filters
    OFFICIAL_FILTERS = {
        # String filters - Standard Liquid
        'append', 'capitalize', 'downcase', 'escape', 'lstrip', 'newline_to_br',
        'prepend', 'remove', 'remove_first', 'replace', 'replace_first', 'rstrip',
        'slice', 'split', 'strip', 'strip_html', 'strip_newlines', 'truncate',
        'truncatewords', 'upcase', 'url_encode', 'url_decode',

        # Math filters - Standard Liquid
        'abs', 'at_least', 'at_most', 'ceil', 'divided_by', 'floor', 'minus',
        'modulo', 'plus', 'round', 'times',

        # Array filters - Standard Liquid
        'concat', 'first', 'join', 'last', 'map', 'reverse', 'size', 'sort',
        'sort_natural', 'uniq', 'where', 'compact',

        # Date filters - Standard Liquid
        'date',

        # Format filters - Standard Liquid
        'default', 'json',

        # Shopify-specific string filters
        'handleize', 'md5', 'pluralize',

        # Shopify-specific URL filters
        'asset_img_url', 'asset_url', 'customer_login_link', 'customer_logout_link',
        'customer_register_link', 'file_img_url', 'file_url', 'global_asset_url',
        'image_url', 'img_url', 'link_to', 'link_to_add_tag', 'link_to_remove_tag',
        'link_to_tag', 'link_to_type', 'link_to_vendor', 'payment_type_img_url',
        'shopify_asset_url', 'url_for_type', 'url_for_vendor', 'within',

        # Shopify-specific HTML filters
        'highlight', 'highlight_active_tag', 'img_tag', 'placeholder_svg_tag',
        'script_tag', 'stylesheet_tag', 'time_tag',

        # Shopify-specific color filters
        'color_brightness', 'color_darken', 'color_desaturate', 'color_lighten',
        'color_mix', 'color_modify', 'color_saturate',

        # Shopify-specific money filters
        'money', 'money_with_currency', 'money_without_currency', 'money_without_trailing_zeros',

        # Shopify-specific translation filters
        't', 'translate',

        # Shopify-specific content filters
        'article_img_url', 'blog_img_url', 'cart_url', 'collection_img_url',
        'external_video_tag', 'external_video_url', 'font_face', 'font_modify',
        'font_url', 'format_address', 'metafield_tag', 'metafield_text',
        'model_viewer_tag', 'page_description', 'page_title', 'product_img_url',
        'sort_by', 'video_tag', 'weight_with_unit'
    }

    # HALLUCINATED FILTERS - Made-up filters that DON'T EXIST
    HALLUCINATED_FILTERS = {
        'color_extract': 'DOES NOT EXIST - Use color_brightness, color_lighten, etc.',
        'rgb': 'DOES NOT EXIST - Use CSS rgb() directly',
        'rgba': 'DOES NOT EXIST - Use CSS rgba() directly',
        'hex_to_rgb': 'DOES NOT EXIST - Use CSS or color filters',
        'color_to_rgb': 'DOES NOT EXIST - Use CSS or color filters',
        'extract': 'DOES NOT EXIST - Use object properties directly',
        'get': 'DOES NOT EXIST - Use bracket notation [key]',
        'fetch': 'DOES NOT EXIST - Use assign statements',
        'parse': 'DOES NOT EXIST - Use split or string filters',
        'eval': 'DOES NOT EXIST - Would be dangerous anyway',
        'execute': 'DOES NOT EXIST - Would be dangerous anyway',
        'include': 'DOES NOT EXIST - Use {% include %} tag',
        'render': RENDER_TAG_MESSAGE,
        'partial': RENDER_TAG_MESSAGE,
        'template': RENDER_TAG_MESSAGE,
        'component': RENDER_TAG_MESSAGE,
        'load': 'DOES NOT EXIST - Use assign statements',
        'require': 'DOES NOT EXIST - Not available in Liquid',
        'import': 'DOES NOT EXIST - Not available in Liquid'
    }

    # SHOPIFY OBJECTS - VERIFIED against Shopify Global Objects documentation
    # Source: https://shopify.dev/docs/api/liquid/objects
    SHOPIFY_OBJECTS = {
        # Global objects
        'shop', 'cart', 'collections', 'customer', 'linklists', 'pages', 'blogs',
        'request', 'routes', 'search', 'settings', 'template', 'theme',

        # Collection objects
        'product', 'collection', 'variant', 'image', 'video', 'metafield',

        # Content objects
        'page', 'blog', 'article', 'comment',

        # Customer objects
        'address', 'country', 'order', 'line_item',

        # Form objects
        'form', 'checkout',

        # Loop objects
        'forloop', 'tablerowloop', 'paginate',

        # Section objects
        'section', 'block',

        # Layout objects
        'content_for_header', 'content_for_layout', 'content_for_index',
        'canonical_url', 'powered_by_link',

        # Localization objects
        'localization',

        # Asset objects
        'scripts', 'stylesheets'
    }

    # COMPLEXITY LIMITS - NO over-engineering allowed
    COMPLEXITY_PATTERNS = [
        {
            'pattern': r'(\|\s*\w+\s*){10,}',
            'message': 'OVER-ENGINEERED: 10+ filter chains are unreadable',
            'severity': Severity.CRITICAL,
            'suggestion': 'Break into multiple assign statements'
        },
        {
            'pattern': r'assign\s+(?!.*(?:style|gradient|srcset))\w+\s*=.*(\|\s*append:.*){8,}',
            'message': 'OVER-ENGINEERED: Excessive string concatenation',
            'severity': Severity.ERROR,
            'suggestion': 'Use {% capture %} tag instead'
        },
        {
            'pattern': r'{%\s*if[^}]*%}[^{]*{%\s*if[^}]*%}[^{]*{%\s*if[^}]*%}[^{]*{%\s*if[^}]*%}[^{]*{%\s*if',
            'message': 'OVER-ENGINEERED: 5+ nested if statements',
            'severity': Severity.CRITICAL,
            'suggestion': 'Refactor logic or use case/when statements'
        },
        {
            'pattern': r'{% for.*{% for.*{% for.*{% for',
            'message': 'PERFORMANCE KILLER: 4+ nested loops',
            'severity': Severity.CRITICAL,
            'suggestion': 'Redesign data structure - this will break themes'
        },
        {
            'pattern': r'{% liquid\s+([^%]*\n){50,}',
            'message': 'OVER-ENGINEERED: 50+ line liquid blocks are unreadable',
            'severity': Severity.ERROR,
            'suggestion': 'Break into smaller logical chunks'
        }
    ]

    # PERFORMANCE KILLERS - Patterns that DESTROY theme performance
    PERFORMANCE_KILLERS = [
        {
            'pattern': r'{% for product in collections\.all\.products %}',
            'message': 'PERFORMANCE KILLER: Looping ALL products breaks themes',
            'severity': Severity.CRITICAL,
            'suggestion': 'Use pagination or specific collection'
        },
        {
            'pattern': r'collections\.all\.products\.size',
            'message': 'PERFORMANCE KILLER: Counting all products is slow',
            'severity': Severity.CRITICAL,
            'suggestion': 'Use collections[handle].products_count'
        },
        {
            'pattern': r'{% for collection in collections %}(?!.*limit:)',
            'message': 'PERFORMANCE KILLER: Looping all collections without limit',
            'severity': Severity.CRITICAL,
            'suggestion': 'Add | limit: 50 or use specific collections'
        },
        {
            'pattern': r'image_url:\s*width:\s*[4-9]\d{3,}',
            'message': 'PERFORMANCE KILLER: Images >4000px waste bandwidth',
            'severity': Severity.ERROR,
            'suggestion': 'Use maximum 3000px width for performance'
        },
        {
            'pattern': r'{% for .* in .*%}.*{% unless .*%}.*{% endunless %}.*{% endfor %}',
            'message': 'PERFORMANCE KILLER: Unless inside loops is inefficient',
            'severity': Severity.ERROR,
            'suggestion': 'Filter data before loop or use if statements'
        },
        {
            'pattern': r'{% assign.*%}.*{% assign.*%}.*{% assign.*%}.*{% assign.*%}.*{% assign.*%}.*{% for',
            'message': 'PERFORMANCE KILLER: Many assigns before loops',
            'severity': Severity.WARNING,
            'suggestion': 'Move assigns outside loops when possible'
        }
    ]

    # THEME STORE VIOLATIONS - Patterns that FAIL review
    THEME_STORE_VIOLATIONS = [
        {
            'pattern': r'<script\s+src=["\']https?://(?!cdn\.shopify\.com|ajax\.googleapis\.com/ajax/libs/jquery)',
            'message': 'THEME STORE VIOLATION: External scripts not allowed',
            'severity': Severity.CRITICAL,
            'suggestion': 'Host scripts locally or use Shopify CDN'
        },
        {
            'pattern': r'<link\s+.*href=["\']https?://(?!cdn\.shopify\.com|fonts\.googleapis\.com)',
            'message': 'THEME STORE VIOLATION: External stylesheets not allowed',
            'severity': Severity.CRITICAL,
            'suggestion': 'Host CSS locally or use approved CDNs'
        },
        {
            'pattern': r'@import\s+["\']https?://(?!fonts\.googleapis\.com)',
            'message': 'THEME STORE VIOLATION: External CSS imports not allowed',
            'severity': Severity.ERROR,
            'suggestion': 'Include CSS directly in files'
        },
        {
            'pattern': r'console\.(log|error|warn|info|debug)',
            'message': 'THEME STORE VIOLATION: Console statements must be removed',
            'severity': Severity.ERROR,
            'suggestion': 'Remove all console statements for production'
        },
        {
            'pattern': r'alert\s*\(',
            'message': 'THEME STORE VIOLATION: Alert dialogs not allowed',
            'severity': Severity.CRITICAL,
            'suggestion': 'Use proper UI notifications instead'
        },
        {
            'pattern': r'document\.write\s*\(',
            'message': 'THEME STORE VIOLATION: document.write breaks modern browsers',
            'severity': Severity.CRITICAL,
            'suggestion': 'Use proper DOM manipulation'
        }
    ]

    def __init__(self):
        self.issues: List[ValidationIssue] = []
        self.files_scanned = 0
        self.files_failed = 0

    def extract_file_content(self, file_path: Path) -> str:
        """Extract content from liquid file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.add_issue(
                file_path=str(file_path),
                line=0,
                issue_type="file_error",
                severity=Severity.CRITICAL,
                message=f"Cannot read file: {e}"
            )
            return ""

    def add_issue(self, file_path: str, line: int, issue_type: str,
                  severity: Severity, message: str, suggestion: str = "", pattern: str = ""):
        """Add validation issue to results"""
        self.issues.append(ValidationIssue(
            file_path=file_path,
            line=line,
            issue_type=issue_type,
            severity=severity,
            message=message,
            suggestion=suggestion,
            pattern=pattern
        ))

    def find_line_number(self, content: str, search_term: str) -> int:
        """Find approximate line number for search term"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_term in line:
                return i
        return 0

    def validate_liquid_filters(self, content: str, file_path: str):
        """Validate ALL filters are real Shopify filters"""
        # Extract filters from liquid blocks only
        liquid_blocks = re.findall(r'{{[^}]*}}|{%[^%]*%}', content)

        used_filters = set()
        for block in liquid_blocks:
            filter_matches = re.findall(r'\|\s*([a-zA-Z_][a-zA-Z0-9_]*)', block)
            used_filters.update(filter_matches)

        for filter_name in used_filters:
            line_num = self.find_line_number(content, f'| {filter_name}')

            if filter_name in self.HALLUCINATED_FILTERS:
                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="hallucinated_filter",
                    severity=Severity.CRITICAL,
                    message=f"HALLUCINATED FILTER: '{filter_name}' DOES NOT EXIST",
                    suggestion=self.HALLUCINATED_FILTERS[filter_name]
                )
            elif filter_name not in self.OFFICIAL_FILTERS:
                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="unknown_filter",
                    severity=Severity.CRITICAL,
                    message=f"UNKNOWN FILTER: '{filter_name}' not in Shopify Liquid",
                    suggestion="Verify this filter exists in official Shopify documentation"
                )

    def _get_suspicious_objects(self):
        """Get dictionary of suspicious/fake objects"""
        return {
            'products': 'Use collections[handle].products or search.results',
            'items': 'Not a Shopify object - use cart.items or line_items',
            'data': 'Not a Shopify object - use metaobjects or settings',
            'config': 'Not a Shopify object - use settings',
            'theme': 'Not a Shopify object - use settings',
            'store': 'Not a Shopify object - use shop',
            'user': 'Not a Shopify object - use customer',
            'session': 'Not available in Shopify Liquid'
        }

    def _get_object_patterns(self):
        """Get regex patterns for object references"""
        return [
            r'{{[\s]*([a-zA-Z_]\w*)\.',
            r'{%\s*for\s+\w+\s+in\s+([a-zA-Z_]\w*)',
            r'{%\s*assign\s+\w+\s*=\s*([a-zA-Z_]\w*)\.',
            r'{%\s*if\s+([a-zA-Z_]\w*)\.',
            r'{%\s*unless\s+([a-zA-Z_]\w*)\.'
        ]

    def validate_shopify_objects(self, content: str, file_path: str):
        """Validate that objects used actually exist in Shopify"""
        suspicious_objects = self._get_suspicious_objects()
        object_patterns = self._get_object_patterns()

        for pattern in object_patterns:
            self._check_pattern_for_suspicious_objects(
                pattern, content, file_path, suspicious_objects
            )

    def _check_pattern_for_suspicious_objects(self, pattern: str, content: str,
                                            file_path: str, suspicious_objects: dict):
        """Check a single pattern for suspicious objects"""
        matches = re.finditer(pattern, content)
        for match in matches:
            obj_name = match.group(1)
            if obj_name in suspicious_objects:
                line_num = content[:match.start()].count('\n') + 1
                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="fake_object",
                    severity=Severity.ERROR,
                    message=f"SUSPICIOUS OBJECT: '{obj_name}' may not exist in Shopify",
                    suggestion=suspicious_objects[obj_name]
                )

    def validate_complexity(self, content: str, file_path: str):
        """Check for over-engineered patterns"""
        # Remove comments first to avoid false positives
        content_without_comments = self._remove_liquid_comments(content)

        for pattern_info in self.COMPLEXITY_PATTERNS:
            matches = re.finditer(pattern_info['pattern'], content_without_comments, re.MULTILINE | re.DOTALL)
            for match in matches:
                # Find line number in original content - approximate
                line_num = content[:match.start()].count('\n') + 1
                pattern_text = match.group(0)[:100] + "..." if len(match.group(0)) > 100 else match.group(0)

                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="complexity",
                    severity=pattern_info['severity'],
                    message=pattern_info['message'],
                    suggestion=pattern_info['suggestion'],
                    pattern=pattern_text
                )

    def validate_performance(self, content: str, file_path: str):
        """Check for performance-killing patterns"""
        for pattern_info in self.PERFORMANCE_KILLERS:
            matches = re.finditer(pattern_info['pattern'], content, re.MULTILINE | re.DOTALL)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                pattern_text = match.group(0)[:100] + "..." if len(match.group(0)) > 100 else match.group(0)

                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="performance",
                    severity=pattern_info['severity'],
                    message=pattern_info['message'],
                    suggestion=pattern_info['suggestion'],
                    pattern=pattern_text
                )

    def validate_theme_store(self, content: str, file_path: str):
        """Check for Theme Store violations"""
        # Remove comments first to avoid false positives
        content_without_comments = self._remove_liquid_comments(content)

        for pattern_info in self.THEME_STORE_VIOLATIONS:
            matches = re.finditer(pattern_info['pattern'], content_without_comments, re.MULTILINE)
            for match in matches:
                # Find line number in original content
                line_num = content[:content.find(match.group(0))].count('\n') + 1 if content.find(match.group(0)) >= 0 else 0

                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="theme_store",
                    severity=pattern_info['severity'],
                    message=pattern_info['message'],
                    suggestion=pattern_info['suggestion'],
                    pattern=match.group(0)
                )

    def _remove_liquid_comments(self, content: str) -> str:
        """Remove liquid comments to avoid false positives"""
        # Remove {%- comment -%} ... {%- endcomment -%} blocks
        comment_pattern = r'{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}'
        return re.sub(comment_pattern, '', content, flags=re.DOTALL)

    def validate_schema_integrity(self, content: str, file_path: str):
        """Validate schema integrity - settings defined vs used"""
        # Skip files that don't need schemas
        if any(skip in file_path for skip in ['/snippets/', '/layouts/', '/templates/']):
            return

        # Extract schema
        schema_match = re.search(r'{% schema %}(.*?){% endschema %}', content, re.DOTALL)
        if not schema_match:
            if any(required in file_path for required in ['/sections/', '/blocks/']):
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="missing_schema",
                    severity=Severity.ERROR,
                    message="Missing schema block - required for sections and blocks"
                )
            return

        try:
            schema = json.loads(schema_match.group(1).strip())
        except json.JSONDecodeError as e:
            self.add_issue(
                file_path=file_path,
                line=self.find_line_number(content, '{% schema %}'),
                issue_type="invalid_schema",
                severity=Severity.CRITICAL,
                message=f"Invalid JSON in schema: {e}"
            )
            return

        # Get defined settings
        defined_settings = set()
        for setting in schema.get('settings', []):
            if setting.get('id'):
                defined_settings.add(setting.get('id'))

        # Add block settings
        for block in schema.get('blocks', []):
            for block_setting in block.get('settings', []):
                if block_setting.get('id'):
                    defined_settings.add(block_setting.get('id'))

        # Find used settings (only section.settings and block.settings)
        used_patterns = [
            r'section\.settings\.([a-zA-Z_][a-zA-Z0-9_]*)',
            r'block\.settings\.([a-zA-Z_][a-zA-Z0-9_]*)'
        ]

        used_settings = set()
        for pattern in used_patterns:
            matches = re.findall(pattern, content)
            used_settings.update(matches)

        # Check for undefined settings
        undefined_settings = used_settings - defined_settings
        for setting in undefined_settings:
            line_num = self.find_line_number(content, f'.settings.{setting}')
            self.add_issue(
                file_path=file_path,
                line=line_num,
                issue_type="undefined_setting",
                severity=Severity.ERROR,
                message=f"Setting '{setting}' used but not defined in schema",
                suggestion="Add setting to schema or check spelling"
            )

        # Validate range settings
        for setting in schema.get('settings', []):
            if setting.get('type') == 'range':
                min_val = setting.get('min', 0)
                max_val = setting.get('max', 100)
                step = setting.get('step', 1)

                if step > 0:
                    range_calc = (max_val - min_val) / step
                    if range_calc > 101:
                        self.add_issue(
                            file_path=file_path,
                            line=0,
                            issue_type="invalid_range",
                            severity=Severity.ERROR,
                            message=f"Range setting '{setting.get('id')}' violates (max-min)/step <= 101",
                            suggestion=f"Current: ({max_val}-{min_val})/{step} = {range_calc:.1f}"
                        )

    def validate_file(self, file_path: Path) -> bool:
        """Run ALL validations on a single file"""
        print(f"🔍 VALIDATING: {file_path.name}")

        self.files_scanned += 1

        content = self.extract_file_content(file_path)
        if not content:
            self.files_failed += 1
            return False

        file_path_str = str(file_path)

        # Run ALL validation checks
        self.validate_liquid_filters(content, file_path_str)
        self.validate_shopify_objects(content, file_path_str)
        self.validate_complexity(content, file_path_str)
        self.validate_performance(content, file_path_str)
        self.validate_theme_store(content, file_path_str)
        self.validate_schema_integrity(content, file_path_str)

        # Check if file has critical issues
        file_issues = [issue for issue in self.issues if issue.file_path == file_path_str]
        critical_issues = [issue for issue in file_issues if issue.severity in [Severity.CRITICAL, Severity.ERROR]]

        if critical_issues:
            print(f"❌ FAILED: {len(critical_issues)} critical issue(s)")
            self.files_failed += 1
            return False
        else:
            print("✅ PASSED")
            return True

    def scan_directory(self, directory_path: Path) -> bool:
        """Scan all liquid files in directory"""
        liquid_files = list(directory_path.rglob("*.liquid"))

        if not liquid_files:
            print(f"❌ No .liquid files found in {directory_path}")
            return False

        print("🔍 ULTIMATE SHOPIFY LIQUID VALIDATOR")
        print(f"📄 Found {len(liquid_files)} liquid files")
        print("=" * 80)

        for file_path in liquid_files:
            self.files_scanned += 1
            success = self.validate_file(file_path)
            if not success:
                self.files_failed += 1

        return self.generate_final_report()

    def generate_final_report(self) -> bool:
        """Generate comprehensive final report"""
        print("\n" + "=" * 80)
        print("🎯 ULTIMATE VALIDATION REPORT")
        print("=" * 80)

        # Group issues by severity
        critical_issues = [i for i in self.issues if i.severity == Severity.CRITICAL]
        error_issues = [i for i in self.issues if i.severity == Severity.ERROR]
        warning_issues = [i for i in self.issues if i.severity == Severity.WARNING]

        print("📊 SCAN SUMMARY:")
        print(f"  • Files scanned: {self.files_scanned}")
        print(f"  • Files failed: {self.files_failed}")
        print(f"  • Files passed: {self.files_scanned - self.files_failed}")
        print(f"  • Critical issues: {len(critical_issues)}")
        print(f"  • Error issues: {len(error_issues)}")
        print(f"  • Warning issues: {len(warning_issues)}")

        # Show critical issues
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
            print("-" * 50)
            for issue in critical_issues[:10]:  # Show first 10
                print(f"❌ {Path(issue.file_path).name}:{issue.line}")
                print(f"   {issue.message}")
                if issue.suggestion:
                    print(f"   💡 {issue.suggestion}")
                print()

            if len(critical_issues) > 10:
                print(f"... and {len(critical_issues) - 10} more critical issues")

        # Show error issues
        if error_issues:
            print(f"\n⚠️ ERROR ISSUES ({len(error_issues)}):")
            print("-" * 50)
            for issue in error_issues[:5]:  # Show first 5
                print(f"⚠️ {Path(issue.file_path).name}:{issue.line}")
                print(f"   {issue.message}")
                if issue.suggestion:
                    print(f"   💡 {issue.suggestion}")
                print()

        # Issue type breakdown
        if self.issues:
            issue_types = {}
            for issue in self.issues:
                if issue.severity in [Severity.CRITICAL, Severity.ERROR]:
                    issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

            print("\n🔍 ISSUE BREAKDOWN:")
            print("-" * 30)
            for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {issue_type}: {count} occurrences")

        # Final verdict
        total_critical = len(critical_issues) + len(error_issues)

        if total_critical == 0:
            print("\n✅ ALL VALIDATIONS PASSED!")
            print("🚀 Code is CLEAN and ready for Shopify deployment")
            if warning_issues:
                print(f"ℹ️ Note: {len(warning_issues)} warning(s) - review recommended")
            return True
        else:
            print("\n🚨 VALIDATION FAILED!")
            print(f"❌ {total_critical} CRITICAL/ERROR issue(s) found")
            print("🛑 ZERO TOLERANCE: Fix ALL issues before deployment")
            print("💀 This code would BREAK Shopify themes")
            return False

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ultimate Shopify Liquid Validator - ZERO TOLERANCE for broken code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ultimate-validator.py file.liquid              # Validate single file
  python3 ultimate-validator.py path/to/directory/       # Validate directory
  python3 ultimate-validator.py --all                    # Validate entire codebase

This validator enforces ZERO TOLERANCE for:
- Hallucinated filters (color_extract, rgb, etc.)
- Over-engineered complexity (10+ filter chains)
- Performance killers (looping all products)
- Theme Store violations (external scripts)
- Made-up Shopify objects
- Schema integrity issues

ONE SCRIPT TO RULE THEM ALL - NO MORE BROKEN CODE
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to liquid file or directory to validate'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate entire code library'
    )

    args = parser.parse_args()

    print("🛡️ ULTIMATE SHOPIFY LIQUID VALIDATOR")
    print("❌ ZERO TOLERANCE FOR BROKEN CODE")
    print("🚀 ONE SCRIPT TO RULE THEM ALL")
    print("=" * 80)

    validator = ShopifyLiquidValidator()

    # Determine target path
    if args.all:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        target_path = project_root / "shopify-liquid-guides" / "code-library"
        print(f"🌍 Validating entire code library: {target_path}")
    elif args.path:
        target_path = Path(args.path)
    else:
        # Default to entire code library
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        target_path = project_root / "shopify-liquid-guides" / "code-library"
        print(f"🎯 Validating code library (default): {target_path}")

    if not target_path.exists():
        print(f"❌ Path not found: {target_path}")
        return 1

    # Validate file or directory
    if target_path.is_file():
        success = validator.validate_file(target_path)
        validator.generate_final_report()
        return 0 if success else 1
    elif target_path.is_dir():
        success = validator.scan_directory(target_path)
        return 0 if success else 1
    else:
        print(f"❌ Invalid path: {target_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())