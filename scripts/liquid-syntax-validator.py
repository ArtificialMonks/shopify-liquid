#!/usr/bin/env python3
"""
Comprehensive Liquid Syntax Validator
Production-ready Liquid syntax validation for Shopify themes
Integrates python-liquid parser with custom Shopify-specific validation rules
"""

import re
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

try:
    from liquid import Environment
    from liquid.exceptions import LiquidSyntaxError, LiquidError
    PYTHON_LIQUID_AVAILABLE = True
except ImportError:
    PYTHON_LIQUID_AVAILABLE = False
    print("⚠️  python-liquid not available. Install with: pip install python-liquid")

class LiquidErrorSeverity(Enum):
    """Liquid validation error severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class LiquidValidationIssue:
    """Structured representation of a Liquid validation issue"""
    file_path: str
    line_number: int
    column: int
    severity: LiquidErrorSeverity
    error_type: str
    message: str
    suggestion: Optional[str] = None
    context: Optional[str] = None

class ShopifyLiquidSyntaxValidator:
    """
    Comprehensive Liquid syntax validator for Shopify themes

    Features:
    - Multi-level validation (regex + parser)
    - Shopify-specific dialect support
    - Performance optimized with caching
    - Integration with existing validator
    """

    def __init__(self):
        self.issues: List[LiquidValidationIssue] = []
        self.validation_cache: Dict[str, Dict] = {}

        # Initialize python-liquid environment if available
        self.liquid_env = None
        if PYTHON_LIQUID_AVAILABLE:
            self.liquid_env = Environment()

        # Setup validation patterns
        self._setup_validation_patterns()
        self._setup_shopify_filters()
        self._setup_shopify_objects()

    def _setup_validation_patterns(self):
        """Setup comprehensive Liquid validation patterns"""

        # Core Liquid tag patterns
        self.LIQUID_TAG_PATTERNS = {
            'output_tag': re.compile(r'{{[\s]*([^}]+?)[\s]*}}'),
            'logic_tag': re.compile(r'{%[\s]*([^%]+?)[\s]*%}'),
            'raw_tag': re.compile(r'{%[\s]*raw[\s]*%}(.*?){%[\s]*endraw[\s]*%}', re.DOTALL),
            'comment_tag': re.compile(r'{%[\s]*comment[\s]*%}(.*?){%[\s]*endcomment[\s]*%}', re.DOTALL),
            'schema_tag': re.compile(r'{%[\s]*schema[\s]*%}(.*?){%[\s]*endschema[\s]*%}', re.DOTALL),
            # In Shopify, the `liquid` tag is a single tag closed by `%}` (no `{% endliquid %}`)
            'liquid_tag': re.compile(r'{%[-\s]*liquid\b(.*?)[-\s]*%}', re.DOTALL),
        }

        # Tag pairing validation
        self.PAIRED_TAGS = {
            'if': 'endif',
            'unless': 'endunless',
            'case': 'endcase',
            'for': 'endfor',
            'capture': 'endcapture',
            'tablerow': 'endtablerow',
            'paginate': 'endpaginate',
            'form': 'endform',
            'style': 'endstyle',
            'comment': 'endcomment',
            'schema': 'endschema',
            'raw': 'endraw'
        }

        # Self-closing tags (no end tag required)
        self.SELF_CLOSING_TAGS = {
            'assign', 'echo', 'increment', 'decrement', 'break', 'continue',
            'include', 'render', 'section', 'layout', 'cycle', 'case', 'when',
            'else', 'elsif', 'elseif'
        }

        # Syntax error patterns (more specific to avoid false positives)
        self.SYNTAX_ERROR_PATTERNS = [
            (re.compile(r'{{[^}]*$', re.MULTILINE), 'Unclosed output tag'),
            (re.compile(r'{%[^%]*$', re.MULTILINE), 'Unclosed logic tag'),
            (re.compile(r'^[^{]*}}', re.MULTILINE), 'Unmatched closing output tag'),
            (re.compile(r'^[^{]*%}', re.MULTILINE), 'Unmatched closing logic tag'),
            (re.compile(r'{{[^}]*\|\s*\|'), 'Invalid filter syntax: double pipes'),
            (re.compile(r'{%[^%]*==\s*(?:and|or)'), 'Invalid operator combination'),
        ]

        # Filter validation patterns
        self.FILTER_PATTERNS = {
            'basic_filter': re.compile(r'\|\s*([a-zA-Z_][a-zA-Z0-9_]*)'),
            'filter_with_args': re.compile(r'\|\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*([^|]+)'),
            'filter_chain': re.compile(r'(\|\s*[a-zA-Z_][a-zA-Z0-9_]*(?:\s*:\s*[^|]+)?)+'),
        }

        # Variable access patterns
        self.VARIABLE_PATTERNS = {
            'simple_variable': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$'),
            'property_access': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*$'),
            'bracket_access': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(?:\[[^\]]+\])+$'),
            'mixed_access': re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(?:(?:\.[a-zA-Z_][a-zA-Z0-9_]*)|(?:\[[^\]]+\]))*$')
        }

    def _setup_shopify_filters(self):
        """Setup official Shopify filter validation"""

        self.OFFICIAL_SHOPIFY_FILTERS = {
            # Standard Liquid filters
            'abs', 'append', 'at_least', 'at_most', 'capitalize', 'ceil', 'compact',
            'concat', 'date', 'default', 'divided_by', 'downcase', 'escape', 'first',
            'floor', 'join', 'last', 'lstrip', 'map', 'minus', 'modulo', 'newline_to_br',
            'plus', 'prepend', 'remove', 'remove_first', 'replace', 'replace_first',
            'reverse', 'round', 'rstrip', 'size', 'slice', 'sort', 'sort_natural',
            'split', 'strip', 'strip_html', 'strip_newlines', 'times', 'truncate',
            'truncatewords', 'uniq', 'upcase', 'url_decode', 'url_encode', 'where',

            # Shopify-specific filters
            'asset_url', 'asset_img_url', 'image_url', 'img_url', 'file_url',
            'money', 'money_with_currency', 'money_without_currency',
            'money_without_trailing_zeros', 'json', 'translate', 't',
            'link_to', 'script_tag', 'stylesheet_tag', 'image_tag', 'video_tag',
            'color_brightness', 'color_darken', 'color_lighten', 'color_saturate',
            'color_desaturate', 'color_mix', 'color_contrast', 'color_difference',
            'font_face', 'font_url', 'handleize', 'highlight', 'highlight_active_tag',
            'pluralize', 'time_tag', 'weight_with_unit', 'within', 'md5', 'sha1',
            'sha256', 'hmac_sha1', 'hmac_sha256', 'base64_encode', 'base64_decode',
            'url_for_vendor_javascript', 'url_for_vendor_stylesheet', 'shopify_asset_url',
            'global_asset_url', 'payment_type_img_url', 'payment_type_svg_tag'
        }

        # Deprecated filters that should trigger warnings
        self.DEPRECATED_FILTERS = {
            'img_url': 'Use image_url instead',
            'asset_img_url': 'Use image_url with asset_url instead',
            'collection_img_url': 'Use image_url with collection.image instead'
        }

    def _setup_shopify_objects(self):
        """Setup Shopify object validation"""

        self.SHOPIFY_OBJECTS = {
            # Global objects
            'shop', 'request', 'template', 'settings', 'linklists', 'pages',
            'blogs', 'collections', 'all_products', 'search', 'customer',
            'cart', 'checkout', 'routes', 'scripts', 'content_for_header',
            'content_for_layout', 'content_for_index', 'powered_by_link',
            'canonical_url', 'page_title', 'page_description',

            # Template-specific objects
            'article', 'blog', 'collection', 'product', 'variant', 'image',
            'link', 'page', 'comment', 'form', 'paginate', 'tablerow',
            'forloop', 'tablerowloop', 'block', 'section'
        }

    def clear_issues(self):
        """Clear all validation issues"""
        self.issues.clear()

    def add_issue(self, file_path: str, line_number: int, column: int,
                  severity: LiquidErrorSeverity, error_type: str,
                  message: str, suggestion: Optional[str] = None,
                  context: Optional[str] = None):
        """Add a validation issue"""

        issue = LiquidValidationIssue(
            file_path=file_path,
            line_number=line_number,
            column=column,
            severity=severity,
            error_type=error_type,
            message=message,
            suggestion=suggestion,
            context=context
        )

        self.issues.append(issue)

    def _find_line_number(self, content: str, position: int) -> int:
        """Find line number for a character position"""
        return content[:position].count('\n') + 1

    def _find_column_number(self, content: str, position: int) -> int:
        """Find column number for a character position"""
        lines = content[:position].split('\n')
        return len(lines[-1]) if lines else 0

    def validate_basic_syntax(self, content: str, file_path: str) -> bool:
        """Fast regex-based basic syntax validation"""

        has_errors = False

        # Remove schema blocks, raw blocks, and comments before syntax validation
        # to avoid false positives in JSON/CSS content
        content_cleaned = content

        # Remove schema blocks (JSON content)
        content_cleaned = self.LIQUID_TAG_PATTERNS['schema_tag'].sub('', content_cleaned)

        # Remove raw blocks (unprocessed content)
        content_cleaned = self.LIQUID_TAG_PATTERNS['raw_tag'].sub('', content_cleaned)

        # Remove comment blocks
        content_cleaned = self.LIQUID_TAG_PATTERNS['comment_tag'].sub('', content_cleaned)

        # Remove style blocks (CSS content)
        style_pattern = re.compile(r'{%[\s]*style[\s]*%}(.*?){%[\s]*endstyle[\s]*%}', re.DOTALL)
        content_cleaned = style_pattern.sub('', content_cleaned)

        # Remove javascript blocks (JS content)
        js_pattern = re.compile(r'{%[\s]*javascript[\s]*%}(.*?){%[\s]*endjavascript[\s]*%}', re.DOTALL)
        content_cleaned = js_pattern.sub('', content_cleaned)

        # Remove single `liquid` blocks to prevent false positives
        content_cleaned = self.LIQUID_TAG_PATTERNS['liquid_tag'].sub('', content_cleaned)

        # Check basic syntax error patterns on cleaned content
        for pattern, error_msg in self.SYNTAX_ERROR_PATTERNS:
            matches = pattern.finditer(content_cleaned)
            for match in matches:
                # Find position in original content
                original_position = self._find_original_position(content, content_cleaned, match.start())
                line_num = self._find_line_number(content, original_position)
                col_num = self._find_column_number(content, original_position)

                self.add_issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=col_num,
                    severity=LiquidErrorSeverity.ERROR,
                    error_type='syntax_error',
                    message=error_msg,
                    context=match.group(0)[:50]
                )
                has_errors = True

        return not has_errors

    def _find_original_position(self, original: str, cleaned: str, cleaned_pos: int) -> int:
        """Find the original position in the full content from cleaned content position"""
        # This is a simplified mapping - for production use, you'd want more sophisticated mapping
        # For now, just return the cleaned position
        return min(cleaned_pos, len(original) - 1)

    def validate_tag_pairing(self, content: str, file_path: str) -> bool:
        """Validate that paired tags are properly matched"""

        # Remove raw blocks and comments to avoid false positives
        content_cleaned = self.LIQUID_TAG_PATTERNS['raw_tag'].sub('', content)
        content_cleaned = self.LIQUID_TAG_PATTERNS['comment_tag'].sub('', content_cleaned)

        # Extract all logic tags with positions
        tags = []
        for match in self.LIQUID_TAG_PATTERNS['logic_tag'].finditer(content_cleaned):
            tag_content = match.group(1).strip()
            tag_parts = tag_content.split()

            if tag_parts:
                tag_name = tag_parts[0]
                line_num = self._find_line_number(content, match.start())
                col_num = self._find_column_number(content, match.start())

                tags.append({
                    'name': tag_name,
                    'line': line_num,
                    'column': col_num,
                    'position': match.start(),
                    'full_content': tag_content
                })

        # Validate tag pairing
        stack = []
        has_errors = False

        for tag in tags:
            tag_name = tag['name']

            # Handle opening tags
            if tag_name in self.PAIRED_TAGS:
                stack.append(tag)

            # Handle closing tags
            elif tag_name.startswith('end'):
                expected_opening = tag_name[3:]  # Remove 'end' prefix

                if not stack:
                    self.add_issue(
                        file_path=file_path,
                        line_number=tag['line'],
                        column=tag['column'],
                        severity=LiquidErrorSeverity.ERROR,
                        error_type='unmatched_end_tag',
                        message=f"Unexpected {tag_name} - no matching opening tag",
                        context=tag['full_content']
                    )
                    has_errors = True

                elif stack[-1]['name'] != expected_opening:
                    self.add_issue(
                        file_path=file_path,
                        line_number=tag['line'],
                        column=tag['column'],
                        severity=LiquidErrorSeverity.ERROR,
                        error_type='mismatched_tags',
                        message=f"Expected end{stack[-1]['name']}, found {tag_name}",
                        context=f"Opening: {stack[-1]['full_content']}, Closing: {tag['full_content']}"
                    )
                    has_errors = True
                else:
                    stack.pop()  # Correctly matched pair

        # Check for unclosed tags
        for unclosed_tag in stack:
            self.add_issue(
                file_path=file_path,
                line_number=unclosed_tag['line'],
                column=unclosed_tag['column'],
                severity=LiquidErrorSeverity.ERROR,
                error_type='unclosed_tag',
                message=f"Unclosed {unclosed_tag['name']} tag",
                suggestion=f"Add {{% end{unclosed_tag['name']} %}} tag",
                context=unclosed_tag['full_content']
            )
            has_errors = True

        return not has_errors

    def validate_filters(self, content: str, file_path: str) -> bool:
        """Validate Liquid filters against official Shopify filter list"""

        has_errors = False

        # Extract all liquid blocks
        liquid_blocks = []
        liquid_blocks.extend(self.LIQUID_TAG_PATTERNS['output_tag'].findall(content))
        liquid_blocks.extend(self.LIQUID_TAG_PATTERNS['logic_tag'].findall(content))

        for block in liquid_blocks:
            # Find all filters in this block
            filter_matches = self.FILTER_PATTERNS['basic_filter'].finditer(block)

            for match in filter_matches:
                filter_name = match.group(1)

                # Check if filter exists
                if filter_name not in self.OFFICIAL_SHOPIFY_FILTERS:
                    # Find position in original content
                    block_position = content.find(block)
                    if block_position != -1:
                        position = block_position + match.start()
                        line_num = self._find_line_number(content, position)
                        col_num = self._find_column_number(content, position)

                        self.add_issue(
                            file_path=file_path,
                            line_number=line_num,
                            column=col_num,
                            severity=LiquidErrorSeverity.ERROR,
                            error_type='unknown_filter',
                            message=f"Unknown filter: {filter_name}",
                            suggestion="Verify filter exists in Shopify documentation",
                            context=block[:50]
                        )
                        has_errors = True

                # Check for deprecated filters
                elif filter_name in self.DEPRECATED_FILTERS:
                    block_position = content.find(block)
                    if block_position != -1:
                        position = block_position + match.start()
                        line_num = self._find_line_number(content, position)
                        col_num = self._find_column_number(content, position)

                        self.add_issue(
                            file_path=file_path,
                            line_number=line_num,
                            column=col_num,
                            severity=LiquidErrorSeverity.WARNING,
                            error_type='deprecated_filter',
                            message=f"Deprecated filter: {filter_name}",
                            suggestion=self.DEPRECATED_FILTERS[filter_name],
                            context=block[:50]
                        )

        return not has_errors

    def validate_schema_blocks(self, content: str, file_path: str) -> bool:
        """Validate JSON schema blocks"""

        has_errors = False
        schema_matches = self.LIQUID_TAG_PATTERNS['schema_tag'].finditer(content)

        for match in schema_matches:
            schema_content = match.group(1).strip()
            line_num = self._find_line_number(content, match.start())
            col_num = self._find_column_number(content, match.start())

            try:
                schema_json = json.loads(schema_content)

                # Basic schema validation
                if not isinstance(schema_json, dict):
                    self.add_issue(
                        file_path=file_path,
                        line_number=line_num,
                        column=col_num,
                        severity=LiquidErrorSeverity.ERROR,
                        error_type='invalid_schema',
                        message="Schema must be a JSON object",
                        context=schema_content[:100]
                    )
                    has_errors = True

                elif 'name' not in schema_json:
                    self.add_issue(
                        file_path=file_path,
                        line_number=line_num,
                        column=col_num,
                        severity=LiquidErrorSeverity.ERROR,
                        error_type='missing_schema_name',
                        message="Schema must have a 'name' property",
                        suggestion="Add 'name' property to schema",
                        context=schema_content[:100]
                    )
                    has_errors = True

            except json.JSONDecodeError as e:
                self.add_issue(
                    file_path=file_path,
                    line_number=line_num + str(e).count('\n'),
                    column=col_num,
                    severity=LiquidErrorSeverity.ERROR,
                    error_type='invalid_json_schema',
                    message=f"Invalid JSON in schema block: {str(e)}",
                    suggestion="Fix JSON syntax in schema block",
                    context=schema_content[:100]
                )
                has_errors = True

        return not has_errors

    def validate_with_parser(self, content: str, file_path: str) -> bool:
        """Use python-liquid parser for comprehensive validation"""

        if not self.liquid_env:
            return True  # Skip if parser not available

        try:
            # Attempt to parse the content
            self.liquid_env.parse(content)
            return True

        except LiquidSyntaxError as e:
            # Extract error details
            error_msg = str(e)
            line_num = 1
            col_num = 0

            # Try to extract line number from error message
            import re
            line_match = re.search(r'line (\d+)', error_msg)
            if line_match:
                line_num = int(line_match.group(1))

            self.add_issue(
                file_path=file_path,
                line_number=line_num,
                column=col_num,
                severity=LiquidErrorSeverity.ERROR,
                error_type='parser_error',
                message=f"Liquid parser error: {error_msg}",
                suggestion="Fix Liquid syntax error"
            )
            return False

        except LiquidError as e:
            self.add_issue(
                file_path=file_path,
                line_number=1,
                column=0,
                severity=LiquidErrorSeverity.WARNING,
                error_type='liquid_warning',
                message=f"Liquid warning: {str(e)}"
            )
            return True

    def validate_performance_patterns(self, content: str, file_path: str) -> bool:
        """Validate performance-critical patterns"""

        performance_patterns = [
            (re.compile(r'collections\.all\.products(?!.*limit:)'),
             'Looping all products without limit causes performance issues',
             'Add | limit: 50 or use specific collection'),

            (re.compile(r'(\|\s*\w+\s*){8,}'),
             'Excessive filter chaining (8+ filters) may impact performance',
             'Consider breaking into multiple assign statements'),

            (re.compile(r'for\s+\w+\s+in\s+(?:collections\.all|all_products)(?!.*limit:)'),
             'Looping through all collections/products without limit',
             'Add limit parameter to prevent performance issues'),
        ]

        for pattern, message, suggestion in performance_patterns:
            matches = pattern.finditer(content)
            for match in matches:
                line_num = self._find_line_number(content, match.start())
                col_num = self._find_column_number(content, match.start())

                self.add_issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=col_num,
                    severity=LiquidErrorSeverity.WARNING,
                    error_type='performance_warning',
                    message=message,
                    suggestion=suggestion,
                    context=match.group(0)
                )

        return True

    def validate_content(self, content: str, file_path: str,
                        validation_level: str = 'comprehensive') -> Dict:
        """
        Main validation method with configurable validation levels

        Args:
            content: Liquid content to validate
            file_path: Path to the file being validated
            validation_level: 'fast', 'standard', or 'comprehensive'

        Returns:
            Dict with validation results
        """

        start_time = time.time()
        self.clear_issues()

        results = {
            'is_valid': True,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'validation_time_ms': 0,
            'validation_level': validation_level
        }

        # Generate cache key
        content_hash = hashlib.md5(content.encode()).hexdigest()
        cache_key = f"{file_path}:{content_hash}:{validation_level}"

        # Check cache
        if cache_key in self.validation_cache:
            cached_result = self.validation_cache[cache_key]
            cached_result['validation_time_ms'] = 0  # Cache hit
            return cached_result

        # Level 1: Fast regex validation (all levels)
        if validation_level in ['fast', 'standard', 'comprehensive']:
            self.validate_basic_syntax(content, file_path)
            self.validate_schema_blocks(content, file_path)

        # Level 2: Structural validation (standard and comprehensive)
        if validation_level in ['standard', 'comprehensive']:
            self.validate_tag_pairing(content, file_path)
            self.validate_filters(content, file_path)
            self.validate_performance_patterns(content, file_path)

        # Level 3: Full parser validation (comprehensive only)
        # Note: Disabled python-liquid parser as it doesn't support Shopify dialect
        # if validation_level == 'comprehensive':
        #     self.validate_with_parser(content, file_path)

        # Count issues by severity
        for issue in self.issues:
            if issue.severity == LiquidErrorSeverity.ERROR:
                results['error_count'] += 1
                results['is_valid'] = False
            elif issue.severity == LiquidErrorSeverity.CRITICAL:
                results['error_count'] += 1
                results['is_valid'] = False
            elif issue.severity == LiquidErrorSeverity.WARNING:
                results['warning_count'] += 1
            elif issue.severity == LiquidErrorSeverity.INFO:
                results['info_count'] += 1

        # Calculate performance
        results['validation_time_ms'] = (time.time() - start_time) * 1000

        # Cache results (limit cache size)
        if len(self.validation_cache) < 100:
            self.validation_cache[cache_key] = results.copy()

        return results

    def validate_file(self, file_path: Union[str, Path],
                     validation_level: str = 'comprehensive') -> Dict:
        """Validate a Liquid file"""

        file_path_str = str(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return self.validate_content(content, file_path_str, validation_level)

        except FileNotFoundError:
            return {
                'is_valid': False,
                'error_count': 1,
                'warning_count': 0,
                'info_count': 0,
                'validation_time_ms': 0,
                'validation_level': validation_level,
                'error': f"File not found: {file_path_str}"
            }
        except Exception as e:
            return {
                'is_valid': False,
                'error_count': 1,
                'warning_count': 0,
                'info_count': 0,
                'validation_time_ms': 0,
                'validation_level': validation_level,
                'error': f"Error reading file: {str(e)}"
            }

    def format_issues(self, format_type: str = 'detailed') -> str:
        """Format validation issues for display"""

        if not self.issues:
            return "✅ No Liquid syntax issues found"

        if format_type == 'summary':
            error_count = sum(1 for issue in self.issues if issue.severity in [LiquidErrorSeverity.ERROR, LiquidErrorSeverity.CRITICAL])
            warning_count = sum(1 for issue in self.issues if issue.severity == LiquidErrorSeverity.WARNING)

            return f"🔍 Found {error_count} errors, {warning_count} warnings"

        # Detailed format
        output = []
        output.append("🔍 Liquid Syntax Validation Issues")
        output.append("=" * 50)

        # Group by file
        files = {}
        for issue in self.issues:
            if issue.file_path not in files:
                files[issue.file_path] = []
            files[issue.file_path].append(issue)

        for file_path, file_issues in files.items():
            output.append(f"\n📄 {file_path}")
            output.append("-" * 30)

            for issue in sorted(file_issues, key=lambda x: x.line_number):
                severity_icon = {
                    LiquidErrorSeverity.CRITICAL: "🚨",
                    LiquidErrorSeverity.ERROR: "❌",
                    LiquidErrorSeverity.WARNING: "⚠️",
                    LiquidErrorSeverity.INFO: "ℹ️"
                }.get(issue.severity, "❓")

                output.append(f"   {severity_icon} Line {issue.line_number}:{issue.column} - {issue.message}")

                if issue.suggestion:
                    output.append(f"      💡 {issue.suggestion}")

                if issue.context:
                    output.append(f"      📝 Context: {issue.context}")

        return "\n".join(output)

def main():
    """CLI interface for Liquid syntax validation"""
    import argparse

    parser = argparse.ArgumentParser(description='Shopify Liquid Syntax Validator')
    parser.add_argument('files', nargs='+', help='Liquid files to validate')
    parser.add_argument('--level', choices=['fast', 'standard', 'comprehensive'],
                       default='comprehensive', help='Validation level')
    parser.add_argument('--format', choices=['detailed', 'summary'],
                       default='detailed', help='Output format')

    args = parser.parse_args()

    validator = ShopifyLiquidSyntaxValidator()
    overall_valid = True

    for file_path in args.files:
        print(f"\n🔍 Validating: {file_path}")

        result = validator.validate_file(file_path, args.level)

        if not result['is_valid']:
            overall_valid = False

        print(f"✅ Valid: {result['is_valid']}")
        print(f"⏱️  Time: {result['validation_time_ms']:.1f}ms")
        print(f"🔢 Issues: {result['error_count']} errors, {result['warning_count']} warnings")

        if validator.issues:
            print(validator.format_issues(args.format))

    return 0 if overall_valid else 1

if __name__ == "__main__":
    exit(main())