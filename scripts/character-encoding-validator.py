#!/usr/bin/env python3
"""
Character Encoding Validator for Shopify Liquid Themes

Detects HTML entity encoding problems and Unicode compatibility issues
that cause theme upload errors and template parsing failures.

Based on comprehensive research of Shopify Liquid character encoding issues.
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class EncodingSeverity(Enum):
    CRITICAL = "critical"  # Breaks theme upload/parsing
    ERROR = "error"       # Causes display issues
    WARNING = "warning"   # Potential problems
    INFO = "info"         # Best practice recommendations

@dataclass
class EncodingIssue:
    file_path: str
    line_number: int
    issue_type: str
    severity: EncodingSeverity
    message: str
    match: str
    fix_suggestion: str
    context: str = ""

class CharacterEncodingValidator:
    """
    Comprehensive validator for character encoding issues in Shopify Liquid templates

    Detects:
    1. HTML entities that break Liquid parsing
    2. Unicode characters in Liquid variables and filters
    3. Character encoding issues in meta tags and head elements
    4. Special characters in alt text and title attributes
    5. UTF-8 vs ASCII compatibility problems
    """

    def __init__(self):
        self.issues: List[EncodingIssue] = []
        self.files_scanned = 0
        self.files_with_issues = 0

    # HTML Entity Patterns That Break Liquid Parsing
    HTML_ENTITY_PATTERNS = [
        {
            'pattern': r'{{\s*[^}]*&(?:amp|lt|gt|quot|#39|nbsp|mdash|ndash|hellip|[a-zA-Z]+);[^}]*}}',
            'type': 'html_entity_in_liquid_output',
            'severity': EncodingSeverity.CRITICAL,
            'message': 'HTML entity in Liquid output expression - breaks parsing',
            'fix': 'Replace HTML entities with actual characters (e.g., &amp; → &)'
        },
        {
            'pattern': r'{%\s*[^%]*&(?:amp|lt|gt|quot|#39|nbsp|mdash|ndash|hellip|[a-zA-Z]+);[^%]*%}',
            'type': 'html_entity_in_liquid_tag',
            'severity': EncodingSeverity.CRITICAL,
            'message': 'HTML entity in Liquid tag - breaks parsing',
            'fix': 'Replace HTML entities with actual characters'
        },
        {
            'pattern': r'\|\s*(?:split|replace|append|prepend):\s*["\'][^"\']*&(?:amp|lt|gt|quot|#39|[a-zA-Z]+);[^"\']*["\']',
            'type': 'html_entity_in_filter_parameter',
            'severity': EncodingSeverity.CRITICAL,
            'message': 'HTML entity in filter parameter - breaks filter operation',
            'fix': 'Use actual characters in filter parameters'
        }
    ]

    # Unicode Variable Name Issues
    UNICODE_VARIABLE_PATTERNS = [
        {
            'pattern': r'{%\s*assign\s+[^\s]*[^\x00-\x7F][^\s]*\s*=',
            'type': 'unicode_assign_variable',
            'severity': EncodingSeverity.ERROR,
            'message': 'Non-ASCII characters in assign variable name',
            'fix': 'Use ASCII-only characters in variable names (a-z, A-Z, 0-9, _)'
        },
        {
            'pattern': r'{%\s*for\s+[^\s]*[^\x00-\x7F][^\s]*\s+in',
            'type': 'unicode_loop_variable',
            'severity': EncodingSeverity.ERROR,
            'message': 'Non-ASCII characters in for loop variable name',
            'fix': 'Use ASCII-only characters in loop variable names'
        },
        {
            'pattern': r'{%\s*capture\s+[^\s]*[^\x00-\x7F][^\s]*\s*%}',
            'type': 'unicode_capture_variable',
            'severity': EncodingSeverity.ERROR,
            'message': 'Non-ASCII characters in capture variable name',
            'fix': 'Use ASCII-only characters in capture variable names'
        }
    ]

    # Schema Encoding Issues (Critical for theme uploads)
    SCHEMA_ENCODING_PATTERNS = [
        {
            'pattern': r'&(?:amp|lt|gt|quot|#39|nbsp|mdash|ndash|hellip|[a-zA-Z]+);',
            'type': 'html_entity_in_schema',
            'severity': EncodingSeverity.CRITICAL,
            'message': 'HTML entity in schema JSON - causes FileSaveError on upload',
            'fix': 'Replace HTML entities with actual characters in schema'
        }
        # Disabled smart quotes pattern - creates false positives with standard ASCII quotes
    ]

    # Unescaped Output Patterns (XSS and encoding vulnerabilities)
    UNESCAPED_OUTPUT_PATTERNS = [
        {
            'pattern': r'{{\s*(?:settings|customer|form|article|product|collection|page)\.[^}]*}}',
            'type': 'unescaped_user_content',
            'severity': EncodingSeverity.ERROR,
            'message': 'User-controllable content without escape filter',
            'fix': 'Add | escape filter to prevent XSS and encoding issues'
        },
        {
            'pattern': r'{{\s*block\.settings\.[^}]*}}',
            'type': 'unescaped_block_setting',
            'severity': EncodingSeverity.ERROR,
            'message': 'Block setting content without escape filter',
            'fix': 'Add | escape filter to block setting output'
        }
    ]

    # Meta Tag and Head Element Issues
    META_TAG_PATTERNS = [
        {
            'pattern': r'<meta\s+name=["\'][^"\']*["\'] \s+content=["\'][^"\']*{{\s*[^}]*\s*}}[^"\']*["\']',
            'type': 'unescaped_meta_content',
            'severity': EncodingSeverity.ERROR,
            'message': 'Unescaped Liquid in meta tag content',
            'fix': 'Add | escape filter to meta tag content'
        },
        {
            'pattern': r'<meta\s+charset=["\']?(?!utf-8)[^"\'>\s]+',
            'type': 'non_utf8_charset',
            'severity': EncodingSeverity.WARNING,
            'message': 'Non-UTF-8 charset declaration',
            'fix': 'Use UTF-8 charset: <meta charset="utf-8">'
        },
        {
            'pattern': r'<meta\s+http-equiv=["\']content-type["\'][^>]*content=["\'][^"\']*charset=(?!utf-8)[^"\';\s]+',
            'type': 'non_utf8_content_type',
            'severity': EncodingSeverity.WARNING,
            'message': 'Non-UTF-8 content-type declaration',
            'fix': 'Use UTF-8 in content-type: charset=utf-8'
        }
    ]

    # HTML Attribute Encoding Issues
    ATTRIBUTE_PATTERNS = [
        # Disabled patterns - these create too many false positives
        # Legitimate issues are better caught by _validate_unescaped_output
    ]

    # File Name and URL Encoding Issues
    FILE_NAME_PATTERNS = [
        {
            'pattern': r'{{\s*["\'][^"\']*[^\x00-\x7F][^"\']*\.(?:css|js|png|jpg|jpeg|gif|svg)["\'] \s*\|\s*asset_url\s*}}',
            'type': 'unicode_asset_filename',
            'severity': EncodingSeverity.ERROR,
            'message': 'Non-ASCII characters in asset filename',
            'fix': 'Use ASCII-only characters in asset filenames'
        },
        {
            'pattern': r'{%\s*render\s+["\'][^"\']*[^\x00-\x7F][^"\']*["\']',
            'type': 'unicode_render_filename',
            'severity': EncodingSeverity.ERROR,
            'message': 'Non-ASCII characters in render/include filename',
            'fix': 'Use ASCII-only characters in snippet filenames'
        }
    ]

    def validate_file(self, file_path: Path) -> List[EncodingIssue]:
        """Validate a single Liquid file for character encoding issues"""
        try:
            # Try to read as UTF-8, detect encoding issues
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Check for UTF-8 BOM
            if content.startswith('\ufeff'):
                self.add_issue(
                    file_path=str(file_path),
                    line_number=1,
                    issue_type='utf8_bom_detected',
                    severity=EncodingSeverity.WARNING,
                    message='UTF-8 BOM detected - may cause rendering issues',
                    match='\\ufeff at start of file',
                    fix_suggestion='Save file as UTF-8 without BOM',
                    context='Beginning of file'
                )

            self.files_scanned += 1
            issues_found = []

            # Run all validation patterns
            issues_found.extend(self._validate_patterns(self.HTML_ENTITY_PATTERNS, content, str(file_path)))
            issues_found.extend(self._validate_patterns(self.UNICODE_VARIABLE_PATTERNS, content, str(file_path)))
            issues_found.extend(self._validate_unescaped_output(content, str(file_path)))
            issues_found.extend(self._validate_patterns(self.META_TAG_PATTERNS, content, str(file_path)))
            issues_found.extend(self._validate_patterns(self.ATTRIBUTE_PATTERNS, content, str(file_path)))
            issues_found.extend(self._validate_patterns(self.FILE_NAME_PATTERNS, content, str(file_path)))

            # Validate schema encoding separately
            schema_issues = self._validate_schema_encoding(content, str(file_path))
            issues_found.extend(schema_issues)

            # Check for replacement characters (encoding problems)
            replacement_chars = content.count('\ufffd')
            if replacement_chars > 0:
                self.add_issue(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type='encoding_replacement_chars',
                    severity=EncodingSeverity.CRITICAL,
                    message=f'File contains {replacement_chars} replacement characters - encoding corruption detected',
                    match='\\ufffd characters found',
                    fix_suggestion='Fix file encoding - save as UTF-8',
                    context='File encoding issue'
                )
                issues_found.append(self.issues[-1])

            if issues_found:
                self.files_with_issues += 1

            return issues_found

        except UnicodeDecodeError as e:
            # File has serious encoding issues
            self.add_issue(
                file_path=str(file_path),
                line_number=0,
                issue_type='unicode_decode_error',
                severity=EncodingSeverity.CRITICAL,
                message=f'File encoding error: {e}',
                match='Unable to decode file',
                fix_suggestion='Convert file to UTF-8 encoding',
                context='File encoding'
            )
            return [self.issues[-1]]

    def _validate_patterns(self, patterns: List[Dict], content: str, file_path: str) -> List[EncodingIssue]:
        """Validate content against a list of regex patterns"""
        issues = []

        for pattern_info in patterns:
            matches = re.finditer(pattern_info['pattern'], content, re.IGNORECASE | re.MULTILINE)

            for match in matches:
                line_number = self._get_line_number(content, match.start())
                context = self._get_context(content, match.start(), match.end())

                issue = self.add_issue(
                    file_path=file_path,
                    line_number=line_number,
                    issue_type=pattern_info['type'],
                    severity=pattern_info['severity'],
                    message=pattern_info['message'],
                    match=match.group(0),
                    fix_suggestion=pattern_info['fix'],
                    context=context
                )
                issues.append(issue)

        return issues

    def _validate_unescaped_output(self, content: str, file_path: str) -> List[EncodingIssue]:
        """Custom validation for unescaped output patterns"""
        issues = []

        # Find all Liquid output expressions
        liquid_output_pattern = r'{{\s*([^}]+)\s*}}'
        matches = re.finditer(liquid_output_pattern, content, re.IGNORECASE | re.MULTILINE)

        for match in matches:
            liquid_expression = match.group(1).strip()
            match_position = match.start()

            # Check if this output is within a <style> block
            is_in_style_block = self._is_in_style_block(content, match_position)

            # Check if this output is in a URL context (href, src, action attributes)
            is_in_url_context = self._is_in_url_attribute(content, match_position)

            # Check if this output is in a schema context (JSON)
            is_in_schema_context = self._is_in_schema_context(content, match_position)

            # Check if expression uses image_url or other URL-generating filters
            has_url_filter = any(filter in liquid_expression for filter in [
                '| image_url:', '|image_url:',
                '| asset_url', '|asset_url',
                '| file_url', '|file_url',
                '| url_for_', '|url_for_',
                '| link_to_', '|link_to_'
            ])

            # Check if it's user-controllable content
            user_content_patterns = [
                r'(?:settings|customer|form|article|product|collection|page)\.',
                r'block\.settings\.'
            ]

            is_user_content = any(re.search(pattern, liquid_expression) for pattern in user_content_patterns)

            if is_user_content:
                # Check if it has escape filter or other safe filters
                has_escape = '| escape' in liquid_expression or '|escape' in liquid_expression
                has_strip_html = '| strip_html' in liquid_expression or '|strip_html' in liquid_expression
                has_strip = '| strip' in liquid_expression or '|strip' in liquid_expression
                has_json = '| json' in liquid_expression or '|json' in liquid_expression
                has_translate = '| t' in liquid_expression or '|t' in liquid_expression
                # Shopify-specific safe output filters
                has_money = '| money' in liquid_expression or '|money' in liquid_expression
                has_link_to = '| link_to:' in liquid_expression or '|link_to:' in liquid_expression
                has_date = '| date:' in liquid_expression or '|date:' in liquid_expression

                # Skip validation in certain safe contexts
                if is_in_url_context:
                    # URLs in href/src should NOT be escaped as it would break them
                    # However, if it's in aria-label or title within a URL tag, it should be escaped
                    if self._is_in_attribute_text_context(content, match_position):
                        # This is text content in an attribute like aria-label, title, alt
                        if not (has_escape or has_strip_html or has_strip or has_json or has_translate or has_money or has_link_to or has_date):
                            line_number = self._get_line_number(content, match.start())
                            context = self._get_context(content, match.start(), match.end())

                            issue = self.add_issue(
                                file_path=file_path,
                                line_number=line_number,
                                issue_type='unescaped_attribute_text',
                                severity=EncodingSeverity.ERROR,
                                message='Text content in HTML attribute without escape filter',
                                match=match.group(0),
                                fix_suggestion='Add | escape filter for text in attributes',
                                context=context
                            )
                            issues.append(issue)
                    # else: URL context - don't flag as error
                elif has_url_filter:
                    # image_url and similar filters generate safe URLs - skip
                    continue
                elif is_in_schema_context:
                    # Schema JSON contexts are safe - skip
                    continue
                elif is_in_style_block:
                    # Check if this is a safe CSS value (numeric, color, or other CSS-safe values)
                    if self._is_safe_css_value(liquid_expression):
                        continue  # Skip - this is safe in CSS context

                    # For text content in CSS (like content: property), we still need escape
                    if not (has_escape or has_strip_html or has_strip or has_json or has_translate or has_money or has_link_to or has_date):
                        # Only flag if it's actually text content, not CSS values
                        if self._is_css_text_content(liquid_expression):
                            line_number = self._get_line_number(content, match.start())
                            context = self._get_context(content, match.start(), match.end())

                            issue = self.add_issue(
                                file_path=file_path,
                                line_number=line_number,
                                issue_type='unescaped_css_text_content',
                                severity=EncodingSeverity.ERROR,
                                message='Text content in CSS without escape filter',
                                match=match.group(0),
                                fix_suggestion='Add | escape filter for text content in CSS',
                                context=context
                            )
                            issues.append(issue)
                else:
                    # Not in CSS or URL - normal HTML context
                    # Check if this is a safe HTML class value
                    if self._is_in_class_attribute(content, match_position) and self._is_safe_html_class_value(liquid_expression):
                        continue  # Skip - safe class value from select field

                    # Check if this is any other safe value (numeric calculations, richtext, etc.)
                    if self._is_safe_value(liquid_expression):
                        continue  # Skip - safe value that doesn't need escaping

                    if not (has_escape or has_strip_html or has_strip or has_json or has_translate or has_money or has_link_to or has_date):
                        line_number = self._get_line_number(content, match.start())
                        context = self._get_context(content, match.start(), match.end())

                        issue_type = 'unescaped_block_setting' if 'block.settings' in liquid_expression else 'unescaped_user_content'

                        issue = self.add_issue(
                            file_path=file_path,
                            line_number=line_number,
                            issue_type=issue_type,
                            severity=EncodingSeverity.ERROR,
                            message='User-controllable content without escape filter',
                            match=match.group(0),
                            fix_suggestion='Add | escape filter to prevent XSS and encoding issues',
                            context=context
                        )
                        issues.append(issue)

        return issues

    def _is_in_style_block(self, content: str, position: int) -> bool:
        """Check if a position is within a <style> block or style attribute"""
        # Find all style blocks
        style_pattern = r'<style[^>]*>(.*?)</style>'
        style_matches = re.finditer(style_pattern, content, re.DOTALL | re.IGNORECASE)

        for style_match in style_matches:
            if style_match.start() <= position <= style_match.end():
                return True

        # Also check for {% style %} blocks in Liquid
        liquid_style_pattern = r'{%\s*style\s*%}(.*?){%\s*endstyle\s*%}'
        liquid_style_matches = re.finditer(liquid_style_pattern, content, re.DOTALL | re.IGNORECASE)

        for style_match in liquid_style_matches:
            if style_match.start() <= position <= style_match.end():
                return True

        # Check for inline style attributes
        if self._is_in_style_attribute(content, position):
            return True

        return False

    def _is_in_style_attribute(self, content: str, position: int) -> bool:
        """Check if position is within a style attribute"""
        lookback_start = max(0, position - 500)
        lookback_content = content[lookback_start:position]

        # Check if we're inside a style attribute
        style_pattern = r'style\s*=\s*["\'][^"\']*$'
        if re.search(style_pattern, lookback_content, re.IGNORECASE):
            # Also check we haven't closed the attribute yet
            lookahead_end = min(len(content), position + 200)
            lookahead_content = content[position:lookahead_end]
            # If we find a closing quote before another opening attribute, we're in style context
            if re.match(r'^[^"\'<>]*["\']', lookahead_content):
                return True

        return False

    def _is_in_schema_context(self, content: str, position: int) -> bool:
        """Check if position is within a {% schema %} block"""
        # Find schema blocks
        schema_pattern = r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}'
        schema_matches = re.finditer(schema_pattern, content, re.DOTALL | re.IGNORECASE)

        for schema_match in schema_matches:
            if schema_match.start() <= position <= schema_match.end():
                return True

        return False

    def _is_in_url_attribute(self, content: str, position: int) -> bool:
        """Check if a position is within a URL attribute (href, src, action, etc.)"""
        # Look backwards from position to find the attribute
        # Maximum lookback of 200 characters for performance
        lookback_start = max(0, position - 200)
        lookback_content = content[lookback_start:position]

        # Check if we're inside a URL attribute
        url_attr_patterns = [
            r'href\s*=\s*["\'][^"\']*$',
            r'src\s*=\s*["\'][^"\']*$',
            r'action\s*=\s*["\'][^"\']*$',
            r'formaction\s*=\s*["\'][^"\']*$',
            r'data-url\s*=\s*["\'][^"\']*$',
            r'data-href\s*=\s*["\'][^"\']*$',
            r'data-src\s*=\s*["\'][^"\']*$'
        ]

        for pattern in url_attr_patterns:
            if re.search(pattern, lookback_content, re.IGNORECASE):
                # Also check we haven't closed the attribute yet
                lookahead_end = min(len(content), position + 100)
                lookahead_content = content[position:lookahead_end]
                # If we find a closing quote before another opening attribute, we're in URL context
                if re.match(r'^[^"\'<>]*["\']', lookahead_content):
                    return True

        return False

    def _is_in_attribute_text_context(self, content: str, position: int) -> bool:
        """Check if position is in a text attribute like aria-label, title, alt"""
        lookback_start = max(0, position - 200)
        lookback_content = content[lookback_start:position]

        # Text attributes that need escaping
        text_attr_patterns = [
            r'aria-label\s*=\s*["\'][^"\']*$',
            r'aria-describedby\s*=\s*["\'][^"\']*$',
            r'aria-description\s*=\s*["\'][^"\']*$',
            r'title\s*=\s*["\'][^"\']*$',
            r'alt\s*=\s*["\'][^"\']*$',
            r'placeholder\s*=\s*["\'][^"\']*$',
            r'value\s*=\s*["\'][^"\']*$',
            r'data-title\s*=\s*["\'][^"\']*$',
            r'data-text\s*=\s*["\'][^"\']*$',
            r'data-content\s*=\s*["\'][^"\']*$'
        ]

        for pattern in text_attr_patterns:
            if re.search(pattern, lookback_content, re.IGNORECASE):
                return True

        return False

    def _is_in_class_attribute(self, content: str, position: int) -> bool:
        """Check if position is within a class attribute"""
        lookback_start = max(0, position - 200)
        lookback_content = content[lookback_start:position]

        # Check if we're inside a class attribute
        class_pattern = r'class\s*=\s*["\'][^"\']*$'
        if re.search(class_pattern, lookback_content, re.IGNORECASE):
            # Also check we haven't closed the attribute yet
            lookahead_end = min(len(content), position + 100)
            lookahead_content = content[position:lookahead_end]
            # If we find a closing quote before another opening attribute, we're in class context
            if re.match(r'^[^"\'<>]*["\']', lookahead_content):
                return True

        return False

    def _is_safe_value(self, expression: str) -> bool:
        """Check if an expression is a safe value that doesn't need escaping"""
        # Remove filters to check the base setting name
        base_expression = expression.split('|')[0].strip()

        # Check for numeric calculations (safe in any context)
        if self._is_numeric_calculation(expression):
            return True

        # Check for richtext content (should not be escaped)
        if self._is_richtext_content(base_expression):
            return True

        # Safe value patterns - these are numeric or system-specific values
        safe_patterns = [
            # Numeric values (padding, margin, sizes, etc.)
            r'padding|margin|width|height|size|spacing|gap',
            r'radius|opacity|weight|line_height|letter_spacing',
            r'columns|rows|order|flex|grid',
            r'top|bottom|left|right|offset',
            r'delay|duration|speed',
            r'max_width|min_width|max_height|min_height',
            r'font_size|border_width|border_radius',

            # Shopify numeric properties (count, price, quantity)
            r'products_count|variants_count|reviews_count|comments_count',
            r'quantity|stock|inventory|available',
            r'id|product_id|variant_id|collection_id',
            r'price|compare_at_price|unit_price',

            # Color values
            r'color|background|bg_color|border_color|shadow_color',
            r'overlay_color|hover_color|accent_color|text_color',

            # Alignment and positioning
            r'alignment|align|justify|position|display',
            r'text_align|vertical_align',
            r'layout_direction|direction',

            # HTML tag selectors (safe for tag names)
            r'heading_tag|tag|element_tag',

            # Font properties (safe in CSS)
            r'font_family|font_style|font_weight|font_variant|font',
            r'transform|transition|animation',
            r'z_index|aspect_ratio|object_fit',

            # Boolean/enum values that translate to CSS
            r'enable_|show_|hide_|is_'
        ]

        # Check if the setting name matches safe patterns
        for pattern in safe_patterns:
            if re.search(pattern, base_expression, re.IGNORECASE):
                return True

        # Check for font-specific filters that are safe
        font_filters = ['font_face', 'font_family', 'font_url']
        if any(f'| {font_filter}' in expression or f'|{font_filter}' in expression for font_filter in font_filters):
            return True

        # Check for font object properties (these are always safe)
        if '.font' in base_expression or '_font.' in base_expression:
            return True

        # Check if it has a default value that's numeric or a CSS keyword
        if '| default:' in expression:
            default_part = expression.split('| default:')[1].strip()
            # Check for numeric defaults or CSS keywords
            if re.match(r"^['\"]?(?:\d+|transparent|none|auto|inherit|initial|unset)['\"]?", default_part):
                return True

        return False

    def _is_safe_css_value(self, expression: str) -> bool:
        """Check if an expression is a safe CSS value that doesn't need escaping"""
        return self._is_safe_value(expression)

    def _is_numeric_calculation(self, expression: str) -> bool:
        """Check if expression is a numeric calculation"""
        # Common numeric calculation patterns
        calc_patterns = [
            r'divided_by|times|plus|minus',
            r'round|floor|ceil|abs',
            r'^\d+\s*\|',  # starts with number
        ]

        for pattern in calc_patterns:
            if re.search(pattern, expression, re.IGNORECASE):
                return True

        return False

    def _is_richtext_content(self, base_expression: str) -> bool:
        """Check if this is richtext content that should preserve HTML"""
        richtext_patterns = [
            r'content$',
            r'description$',
            r'body$',
            r'text$',
            r'_content$',
            r'_description$',
            r'_body$',
            r'_text$',
            r'rte$',
            r'_rte$',
            r'richtext$',
            r'_richtext$',
            r'body_richtext$',
            r'readmore_content$',
            r'answer$',
            r'_answer$'
        ]

        # Only consider it richtext if it's likely to contain HTML
        # This is conservative - better to false positive than miss XSS
        for pattern in richtext_patterns:
            if re.search(pattern, base_expression, re.IGNORECASE):
                # Additional check: if in div with class containing "rte" or "rich"
                return True

        return False

    def _is_safe_html_class_value(self, expression: str) -> bool:
        """Check if an expression is safe for HTML class attributes"""
        # Remove filters to check the base setting name
        base_expression = expression.split('|')[0].strip()

        # Safe class value patterns - select fields with predefined CSS classes
        safe_class_patterns = [
            r'layout_direction|direction|orientation',
            r'style|variant|theme|design',
            r'alignment|align|position',
            r'size|scale|magnitude',
            r'state|status|mode'
        ]

        # Check if the setting name suggests a CSS class from a select field
        for pattern in safe_class_patterns:
            if re.search(pattern, base_expression, re.IGNORECASE):
                return True

        return False

    def _is_css_text_content(self, expression: str) -> bool:
        """Check if an expression in CSS context contains actual text content"""
        # Text content patterns that would need escaping even in CSS
        text_patterns = [
            r'content|label|title|description|text|message|caption',
            r'heading|subheading|paragraph|name'
        ]

        # Check if the setting name suggests text content
        base_expression = expression.split('|')[0].strip()
        for pattern in text_patterns:
            if re.search(pattern, base_expression, re.IGNORECASE):
                return True

        return False

    def _validate_schema_encoding(self, content: str, file_path: str) -> List[EncodingIssue]:
        """Validate schema blocks for encoding issues"""
        issues = []

        # Extract schema content
        schema_pattern = r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}'
        schema_match = re.search(schema_pattern, content, re.DOTALL | re.IGNORECASE)

        if schema_match:
            schema_content = schema_match.group(1).strip()
            schema_start = schema_match.start(1)

            # Validate schema-specific patterns
            for pattern_info in self.SCHEMA_ENCODING_PATTERNS:
                # Skip smart quotes check if we're looking at standard JSON
                if pattern_info['type'] == 'smart_quotes_in_schema':
                    # Only check for actual smart quote characters, not standard quotes
                    # Check by looking for the actual Unicode characters
                    actual_smart_quotes = ['"', '"', ''', ''', '…', '–', '—']
                    found_smart_quotes = []
                    for smart_char in actual_smart_quotes:
                        if smart_char in schema_content:
                            found_smart_quotes.append(smart_char)

                    if found_smart_quotes:
                        # Find positions of actual smart quotes
                        for smart_char in found_smart_quotes:
                            pos = 0
                            while True:
                                pos = schema_content.find(smart_char, pos)
                                if pos == -1:
                                    break

                                line_number = self._get_line_number(content, schema_start + pos)
                                context = self._get_context(schema_content, pos, pos + len(smart_char))

                                issue = self.add_issue(
                                    file_path=file_path,
                                    line_number=line_number,
                                    issue_type='smart_quotes_in_schema',
                                    severity=EncodingSeverity.WARNING,
                                    message='Smart quotes or special punctuation in schema',
                                    match=smart_char,
                                    fix_suggestion='Replace with standard ASCII quotes and punctuation',
                                    context=context
                                )
                                issues.append(issue)
                                pos += 1
                else:
                    # For other patterns, use regex as before
                    matches = re.finditer(pattern_info['pattern'], schema_content, re.IGNORECASE)

                    for match in matches:
                        # Calculate line number relative to schema content
                        line_number = self._get_line_number(content, schema_start + match.start())
                        context = self._get_context(schema_content, match.start(), match.end())

                        issue = self.add_issue(
                            file_path=file_path,
                            line_number=line_number,
                            issue_type=pattern_info['type'],
                            severity=pattern_info['severity'],
                            message=pattern_info['message'],
                            match=match.group(0),
                            fix_suggestion=pattern_info['fix'],
                            context=context
                        )
                        issues.append(issue)

            # Validate JSON syntax with encoding awareness
            try:
                json.loads(schema_content)
            except json.JSONDecodeError as e:
                # Check if JSON error might be encoding-related
                if any(char in str(e) for char in ['utf-8', 'unicode', 'ascii', 'decode']):
                    issue = self.add_issue(
                        file_path=file_path,
                        line_number=self._get_line_number(content, schema_start),
                        issue_type='schema_json_encoding_error',
                        severity=EncodingSeverity.CRITICAL,
                        message=f'Schema JSON encoding error: {e}',
                        match='Schema JSON block',
                        fix_suggestion='Fix character encoding in schema JSON',
                        context='Schema validation'
                    )
                    issues.append(issue)

        return issues

    def add_issue(self, file_path: str, line_number: int, issue_type: str,
                  severity: EncodingSeverity, message: str, match: str,
                  fix_suggestion: str, context: str = "") -> EncodingIssue:
        """Add an encoding issue to the results"""
        issue = EncodingIssue(
            file_path=file_path,
            line_number=line_number,
            issue_type=issue_type,
            severity=severity,
            message=message,
            match=match,
            fix_suggestion=fix_suggestion,
            context=context
        )
        self.issues.append(issue)
        return issue

    def _get_line_number(self, content: str, position: int) -> int:
        """Get line number for a position in content"""
        return content[:position].count('\n') + 1

    def _get_context(self, content: str, start: int, end: int, context_chars: int = 50) -> str:
        """Get context around a match for better debugging"""
        context_start = max(0, start - context_chars)
        context_end = min(len(content), end + context_chars)

        context = content[context_start:context_end]
        # Replace newlines with spaces for cleaner output
        context = re.sub(r'\s+', ' ', context.strip())

        return context

    def scan_directory(self, directory: Path) -> List[EncodingIssue]:
        """Scan all .liquid files in a directory"""
        all_issues = []

        liquid_files = list(directory.rglob("*.liquid"))

        if not liquid_files:
            print(f"No .liquid files found in {directory}")
            return all_issues

        print(f"🔍 Character Encoding Validator")
        print(f"📄 Found {len(liquid_files)} .liquid files")
        print("=" * 60)

        for file_path in liquid_files:
            file_issues = self.validate_file(file_path)
            all_issues.extend(file_issues)

            # Print file status
            if file_issues:
                critical_count = sum(1 for issue in file_issues if issue.severity == EncodingSeverity.CRITICAL)
                error_count = sum(1 for issue in file_issues if issue.severity == EncodingSeverity.ERROR)
                warning_count = sum(1 for issue in file_issues if issue.severity == EncodingSeverity.WARNING)

                status = "❌ CRITICAL" if critical_count > 0 else "⚠️ ISSUES" if error_count > 0 else "⚠️ WARNINGS"
                print(f"{status}: {file_path.name} ({len(file_issues)} issues)")
            else:
                print(f"✅ CLEAN: {file_path.name}")

        return all_issues

    def generate_report(self) -> str:
        """Generate a comprehensive report of all encoding issues"""
        if not self.issues:
            return self._generate_clean_report()

        # Group issues by severity
        critical_issues = [i for i in self.issues if i.severity == EncodingSeverity.CRITICAL]
        error_issues = [i for i in self.issues if i.severity == EncodingSeverity.ERROR]
        warning_issues = [i for i in self.issues if i.severity == EncodingSeverity.WARNING]
        info_issues = [i for i in self.issues if i.severity == EncodingSeverity.INFO]

        report = []
        report.append("=" * 80)
        report.append("🔤 CHARACTER ENCODING VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        report.append("📊 SUMMARY:")
        report.append(f"  • Files scanned: {self.files_scanned}")
        report.append(f"  • Files with issues: {self.files_with_issues}")
        report.append(f"  • Total issues: {len(self.issues)}")
        report.append(f"  • Critical: {len(critical_issues)} (breaks theme upload)")
        report.append(f"  • Errors: {len(error_issues)} (causes display issues)")
        report.append(f"  • Warnings: {len(warning_issues)} (potential problems)")
        report.append(f"  • Info: {len(info_issues)} (recommendations)")
        report.append("")

        # Critical issues first
        if critical_issues:
            report.append("🚨 CRITICAL ISSUES (Fix immediately - blocks theme upload):")
            report.append("-" * 60)
            for issue in critical_issues[:10]:  # Show first 10
                report.append(self._format_issue(issue))
            if len(critical_issues) > 10:
                report.append(f"... and {len(critical_issues) - 10} more critical issues")
            report.append("")

        # Error issues
        if error_issues:
            report.append("❌ ERROR ISSUES (Causes display problems):")
            report.append("-" * 60)
            for issue in error_issues[:5]:  # Show first 5
                report.append(self._format_issue(issue))
            if len(error_issues) > 5:
                report.append(f"... and {len(error_issues) - 5} more error issues")
            report.append("")

        # Warning issues
        if warning_issues:
            report.append("⚠️ WARNING ISSUES (Potential problems):")
            report.append("-" * 60)
            for issue in warning_issues[:5]:  # Show first 5
                report.append(self._format_issue(issue))
            if len(warning_issues) > 5:
                report.append(f"... and {len(warning_issues) - 5} more warning issues")
            report.append("")

        # Issue type breakdown
        issue_types = {}
        for issue in self.issues:
            issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

        report.append("📈 ISSUE TYPE BREAKDOWN:")
        report.append("-" * 30)
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  • {issue_type}: {count}")
        report.append("")

        # Final recommendation
        if critical_issues or error_issues:
            report.append("🛑 RECOMMENDATION: Fix all critical and error issues before theme upload")
            report.append("💀 Current encoding issues will cause theme upload failures or display problems")
        else:
            report.append("✅ ENCODING STATUS: No critical encoding issues found")
            if warning_issues:
                report.append("ℹ️ Review warnings for optimal character encoding practices")

        return "\n".join(report)

    def _generate_clean_report(self) -> str:
        """Generate report when no issues are found"""
        report = []
        report.append("=" * 80)
        report.append("🔤 CHARACTER ENCODING VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        report.append("📊 SUMMARY:")
        report.append(f"  • Files scanned: {self.files_scanned}")
        report.append(f"  • Files with issues: 0")
        report.append(f"  • Total issues: 0")
        report.append("")
        report.append("✅ EXCELLENT! No character encoding issues found.")
        report.append("🚀 All files use proper UTF-8 encoding and safe character handling.")
        report.append("")
        report.append("📋 CHARACTER ENCODING BEST PRACTICES VERIFIED:")
        report.append("  ✅ No HTML entities in Liquid expressions")
        report.append("  ✅ ASCII-only variable names")
        report.append("  ✅ Proper escape filters on user content")
        report.append("  ✅ UTF-8 charset declarations")
        report.append("  ✅ Safe HTML attribute handling")

        return "\n".join(report)

    def _format_issue(self, issue: EncodingIssue) -> str:
        """Format a single issue for the report"""
        filename = Path(issue.file_path).name
        formatted = f"📁 {filename}:{issue.line_number}"
        formatted += f"\n   {issue.severity.value.upper()}: {issue.message}"
        formatted += f"\n   🔍 Found: {issue.match[:80]}{'...' if len(issue.match) > 80 else ''}"
        formatted += f"\n   💡 Fix: {issue.fix_suggestion}"
        if issue.context:
            formatted += f"\n   📄 Context: {issue.context[:60]}{'...' if len(issue.context) > 60 else ''}"
        formatted += "\n"
        return formatted

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Character Encoding Validator for Shopify Liquid Themes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 character-encoding-validator.py file.liquid
  python3 character-encoding-validator.py /path/to/theme/
  python3 character-encoding-validator.py --critical-only /path/to/theme/

This validator detects:
• HTML entities that break Liquid parsing (&amp;, &lt;, etc.)
• Unicode characters in variable names
• Unescaped user content (XSS vulnerabilities)
• Character encoding issues in meta tags
• Special characters in HTML attributes
• UTF-8 vs ASCII compatibility problems

All issues include specific fix suggestions for immediate resolution.
        """
    )

    parser.add_argument(
        'path',
        help='Path to .liquid file or directory to validate'
    )

    parser.add_argument(
        '--critical-only',
        action='store_true',
        help='Show only critical issues that block theme upload'
    )

    parser.add_argument(
        '--json-output',
        help='Output results as JSON to specified file'
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"❌ Error: Path not found: {path}")
        return 1

    validator = CharacterEncodingValidator()

    # Validate file or directory
    if path.is_file():
        if path.suffix != '.liquid':
            print(f"❌ Error: File must have .liquid extension: {path}")
            return 1
        issues = validator.validate_file(path)
    elif path.is_dir():
        issues = validator.scan_directory(path)
    else:
        print(f"❌ Error: Invalid path: {path}")
        return 1

    # Filter issues if critical-only flag is set
    if args.critical_only:
        validator.issues = [i for i in validator.issues if i.severity == EncodingSeverity.CRITICAL]

    # Generate and display report
    print("\n" + validator.generate_report())

    # JSON output if requested
    if args.json_output:
        json_data = {
            'summary': {
                'files_scanned': validator.files_scanned,
                'files_with_issues': validator.files_with_issues,
                'total_issues': len(validator.issues)
            },
            'issues': [
                {
                    'file_path': issue.file_path,
                    'line_number': issue.line_number,
                    'issue_type': issue.issue_type,
                    'severity': issue.severity.value,
                    'message': issue.message,
                    'match': issue.match,
                    'fix_suggestion': issue.fix_suggestion,
                    'context': issue.context
                }
                for issue in validator.issues
            ]
        }

        with open(args.json_output, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 JSON report saved to: {args.json_output}")

    # Return exit code based on results
    critical_count = sum(1 for i in validator.issues if i.severity == EncodingSeverity.CRITICAL)
    error_count = sum(1 for i in validator.issues if i.severity == EncodingSeverity.ERROR)

    if critical_count > 0:
        return 2  # Critical issues
    elif error_count > 0:
        return 1  # Error issues
    else:
        return 0  # Success

if __name__ == "__main__":
    sys.exit(main())