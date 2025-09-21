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
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Import Liquid syntax validator
try:
    import importlib.util
    import sys
    import os

    # Load the liquid-syntax-validator.py module
    script_dir = os.path.dirname(os.path.abspath(__file__))
    validator_path = os.path.join(script_dir, "liquid-syntax-validator.py")

    spec = importlib.util.spec_from_file_location("liquid_syntax_validator", validator_path)
    liquid_syntax_validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(liquid_syntax_validator)

    ShopifyLiquidSyntaxValidator = liquid_syntax_validator.ShopifyLiquidSyntaxValidator
    LiquidErrorSeverity = liquid_syntax_validator.LiquidErrorSeverity
    LIQUID_VALIDATOR_AVAILABLE = True
except Exception as e:
    LIQUID_VALIDATOR_AVAILABLE = False
    print(f"⚠️  Liquid syntax validator not available: {e}. Enhanced validation disabled.")

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

    def format_theme_check_style(self) -> str:
        """
        Format issue in official Theme Check style for consistency
        """
        # Get relative file path for cleaner output
        rel_path = self.file_path.split('shopify-liquid')[-1].lstrip('/')

        # Theme Check style severity icons
        severity_icons = {
            Severity.CRITICAL: "❌",
            Severity.ERROR: "❌",
            Severity.WARNING: "⚠️",
            Severity.INFO: "ℹ️"
        }

        icon = severity_icons.get(self.severity, "•")

        # Format: icon file:line issue_type message
        if self.line > 0:
            location = f"{rel_path}:{self.line}"
        else:
            location = f"{rel_path}"

        formatted = f"{icon} {location}\n   {self.issue_type.upper()}: {self.message}"

        if self.suggestion:
            formatted += f"\n   💡 {self.suggestion}"

        return formatted

    def format_compact_style(self) -> str:
        """
        Format issue in compact style for summary reports
        """
        rel_path = self.file_path.split('/')[-1]  # Just filename
        return f"{self.severity.value}: {rel_path}:{self.line} - {self.message}"

class ShopifyLiquidValidator:
    """
    Ultimate Shopify Liquid validator - ZERO TOLERANCE for broken code

    Implements official Shopify Theme Check compatible file type detection
    and validation rules based on the comprehensive research findings.
    """

    # OFFICIAL SHOPIFY FILE TYPE PATTERNS - Based on Theme Check Ruby Implementation
    # Source: Theme Check file_system_file.rb regex patterns
    FILE_TYPE_PATTERNS = [
        (re.compile(r'^layout/.*\.liquid$'), 'layout'),
        (re.compile(r'^templates/.*\.liquid$'), 'template_liquid'),
        (re.compile(r'^templates/.*\.json$'), 'template_json'),
        (re.compile(r'^sections/.*\.liquid$'), 'section'),
        (re.compile(r'^blocks/.*\.liquid$'), 'theme_block'),
        (re.compile(r'^snippets/.*\.liquid$'), 'snippet'),
        (re.compile(r'^assets/.*\.(css|js|png|jpg|jpeg|gif|svg|webp|woff|woff2|ttf|otf|eot)$'), 'asset'),
        (re.compile(r'^config/.*\.json$'), 'config'),
        (re.compile(r'^locales/.*\.json$'), 'locale'),
    ]

    # Special wrapper sections with unique validation requirements
    WRAPPER_SECTIONS = ['apps.liquid', '_blocks.liquid']

    # File types that MUST have schema blocks
    SCHEMA_REQUIRED_TYPES = ['section', 'theme_block', 'wrapper_section']

    # File types that MUST NOT have schema blocks
    SCHEMA_FORBIDDEN_TYPES = ['layout', 'template_liquid', 'template_json', 'snippet', 'asset', 'config', 'locale']

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
            'pattern': r'<link\s+[^>]*rel=["\']stylesheet["\'][^>]*href=["\']https?://(?!cdn\.shopify\.com|fonts\.googleapis\.com|fonts\.shopifycdn\.com)',
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

        # Initialize Liquid syntax validator if available
        self.liquid_validator = None
        if LIQUID_VALIDATOR_AVAILABLE:
            self.liquid_validator = ShopifyLiquidSyntaxValidator()

    def detect_file_type(self, file_path: Path, content: str) -> str:
        """
        Official Theme Check compatible file type detection
        Based on Theme Check Ruby implementation patterns
        """
        # Normalize path for pattern matching - remove absolute path prefix
        path_str = str(file_path)

        # Find the theme root (look for key directories)
        theme_dirs = ['layout', 'templates', 'sections', 'blocks', 'snippets', 'assets', 'config', 'locales']
        relative_path = path_str

        for theme_dir in theme_dirs:
            if f'/{theme_dir}/' in path_str:
                # Extract path from theme directory onwards
                relative_path = path_str[path_str.find(f'/{theme_dir}/') + 1:]
                break
            elif path_str.endswith(f'/{theme_dir}'):
                # Handle case where file is directly in theme directory
                relative_path = theme_dir
                break

        filename = file_path.name

        # Special wrapper sections first (highest priority)
        if filename in self.WRAPPER_SECTIONS:
            return 'wrapper_section'

        # Apply directory-based patterns in priority order
        for pattern, file_type in self.FILE_TYPE_PATTERNS:
            if pattern.match(relative_path):
                return file_type

        return 'unknown'

    def is_legacy_template(self, file_path: Path, content: str) -> bool:
        """
        Detect legacy .liquid template files that don't require schemas
        These are valid Shopify files that predate JSON templates
        """
        if file_path.suffix != '.liquid':
            return False

        # Legacy templates don't have schema tags
        has_schema = bool(re.search(r'{% schema %}', content))
        if has_schema:
            return False

        # Check for template-specific patterns
        legacy_patterns = [
            r'{% layout\s+',                    # Layout tag usage
            r'{{ content_for_layout }}',        # Layout content
            r'{% paginate\s+',                 # Pagination (common in templates)
            r'{{ collection\.products }}',      # Collection template patterns
            r'{{ product\. }}',                # Product template patterns
            r'{{ blog\.articles }}',           # Blog template patterns
        ]

        return any(re.search(pattern, content) for pattern in legacy_patterns)

    def should_have_schema(self, file_type: str, file_path: Path, content: str) -> bool:
        """
        Determine if a file should have a schema block based on official rules
        """
        if file_type in self.SCHEMA_REQUIRED_TYPES:
            return True
        elif file_type in self.SCHEMA_FORBIDDEN_TYPES:
            return False
        elif file_type == 'unknown':
            # For unknown files, check if they're legacy templates
            return not self.is_legacy_template(file_path, content)
        else:
            return False

    def validate_app_blocks(self, schema: dict, file_path: str, file_type: str):
        """
        CRITICAL: Validate @app block restrictions per official Shopify Theme Check rules
        Source: AppBlockMissingSchema validation rule
        """
        for block in schema.get('blocks', []):
            block_type = block.get('type')

            # @app blocks cannot have 'limit' parameter (Theme Store violation)
            if block_type == '@app':
                if 'limit' in block:
                    self.add_issue(
                        file_path=file_path,
                        line=0,
                        issue_type="app_block_limit",
                        severity=Severity.CRITICAL,
                        message="@app blocks cannot have 'limit' parameter",
                        suggestion="Remove 'limit' parameter from @app block - app blocks are managed by app developers"
                    )

                # @app blocks should not have explicit settings (apps provide their own)
                if block.get('settings'):
                    self.add_issue(
                        file_path=file_path,
                        line=0,
                        issue_type="app_block_settings",
                        severity=Severity.WARNING,
                        message="@app blocks should not define settings",
                        suggestion="App blocks receive settings from the app - remove settings array"
                    )

    def validate_wrapper_section(self, schema: dict, file_path: str, filename: str):
        """
        CRITICAL: Validate wrapper sections (apps.liquid, _blocks.liquid) requirements
        These have special validation rules per official Shopify documentation
        """
        block_types = [block.get('type') for block in schema.get('blocks', [])]

        # Determine required block types based on wrapper type
        if filename == 'apps.liquid':
            required_types = ['@app']
            section_name = 'apps.liquid'
        elif filename == '_blocks.liquid':
            required_types = ['@app', '@theme']
            section_name = '_blocks.liquid'
        else:
            return  # Not a recognized wrapper section

        # Validate required block types are present
        for required_type in required_types:
            if required_type not in block_types:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="wrapper_missing_block_type",
                    severity=Severity.CRITICAL,
                    message=f"{section_name} must include {required_type} block type",
                    suggestion=f"Add block with type: '{required_type}' to support {required_type} functionality"
                )

        # Wrapper sections must have presets
        if not schema.get('presets'):
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="wrapper_missing_presets",
                severity=Severity.CRITICAL,
                message=f"{section_name} must define presets",
                suggestion="Add presets array to enable section in theme editor"
            )

        # Wrapper sections cannot have 'templates' attribute (they're global)
        if 'templates' in schema:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="wrapper_invalid_templates",
                severity=Severity.CRITICAL,
                message=f"{section_name} cannot define 'templates' attribute",
                suggestion="Remove 'templates' - wrapper sections are available globally"
            )

    def validate_block_nesting_depth(self, content: str, file_path: str):
        """
        HIGH: Validate block nesting doesn't exceed 8 levels (Shopify limit)
        Tracks nesting through content_for blocks and for loops
        """
        lines = content.split('\n')
        nesting_stack = []
        max_nesting = 0

        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()

            # Track opening tags that create nesting
            opening_patterns = [
                (r'{%\s*for\s+', 'for'),
                (r'{%\s*if\s+', 'if'),
                (r'{%\s*unless\s+', 'unless'),
                (r'{%\s*case\s+', 'case'),
                (r'{%\s*capture\s+', 'capture'),
                (r'{%\s*tablerow\s+', 'tablerow'),
                (r'{%\s*paginate\s+', 'paginate'),
                (r'{%\s*content_for\s+', 'content_for'),
            ]

            # Track closing tags
            closing_patterns = [
                (r'{%\s*endfor\s*%}', 'for'),
                (r'{%\s*endif\s*%}', 'if'),
                (r'{%\s*endunless\s*%}', 'unless'),
                (r'{%\s*endcase\s*%}', 'case'),
                (r'{%\s*endcapture\s*%}', 'capture'),
                (r'{%\s*endtablerow\s*%}', 'tablerow'),
                (r'{%\s*endpaginate\s*%}', 'paginate'),
                (r'{%\s*endcontent_for\s*%}', 'content_for'),
            ]

            # Check for opening tags
            for pattern, tag_type in opening_patterns:
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    nesting_stack.append((tag_type, line_num))
                    max_nesting = max(max_nesting, len(nesting_stack))

            # Check for closing tags
            for pattern, tag_type in closing_patterns:
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    if nesting_stack and nesting_stack[-1][0] == tag_type:
                        nesting_stack.pop()

        # Validate nesting depth
        if max_nesting > 8:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="excessive_nesting",
                severity=Severity.ERROR,
                message=f"Block nesting depth ({max_nesting}) exceeds Shopify limit of 8 levels",
                suggestion="Reduce nesting by extracting complex logic into snippets or simplifying conditional logic"
            )

    def validate_static_block_ids(self, all_schemas: Dict[str, dict]):
        """
        HIGH: Validate static block IDs are unique across entire theme
        Per Shopify Theme Check UniqueStaticBlockId rule
        """
        static_block_ids = {}

        for file_path, schema in all_schemas.items():
            for block in schema.get('blocks', []):
                block_id = block.get('id')
                if block_id:  # Only validate explicit IDs (static blocks)
                    if block_id in static_block_ids:
                        self.add_issue(
                            file_path=file_path,
                            line=0,
                            issue_type="duplicate_static_block_id",
                            severity=Severity.CRITICAL,
                            message=f"Static block ID '{block_id}' is already used in {static_block_ids[block_id]}",
                            suggestion=f"Change block ID to a unique value - static block IDs must be unique across the entire theme"
                        )
                    else:
                        static_block_ids[block_id] = file_path

    def validate_template_restrictions(self, schema: dict, file_path: str, file_type: str):
        """
        HIGH: Validate template restrictions (enabled_on/disabled_on) per Theme Check rules
        """
        enabled_on = schema.get('enabled_on', {})
        disabled_on = schema.get('disabled_on', {})

        # Validate templates attribute structure
        if enabled_on:
            valid_templates = [
                'index', 'product', 'collection', 'blog', 'article', 'page',
                'password', 'gift_card', 'customers/order', 'customers/account',
                'customers/register', 'customers/login', 'customers/addresses',
                'cart', 'search', '404'
            ]

            # Check for invalid template names
            for template in enabled_on.get('templates', []):
                if template not in valid_templates and not template.startswith('customers/'):
                    self.add_issue(
                        file_path=file_path,
                        line=0,
                        issue_type="invalid_template_name",
                        severity=Severity.ERROR,
                        message=f"Invalid template name '{template}' in enabled_on",
                        suggestion=f"Use valid template names: {', '.join(valid_templates[:8])}..."
                    )

        if disabled_on:
            # Same validation for disabled_on
            for template in disabled_on.get('templates', []):
                if template not in valid_templates and not template.startswith('customers/'):
                    self.add_issue(
                        file_path=file_path,
                        line=0,
                        issue_type="invalid_template_name",
                        severity=Severity.ERROR,
                        message=f"Invalid template name '{template}' in disabled_on",
                        suggestion=f"Use valid template names: {', '.join(valid_templates[:8])}..."
                    )

        # Validate conflicting restrictions
        if enabled_on and disabled_on:
            enabled_templates = set(enabled_on.get('templates', []))
            disabled_templates = set(disabled_on.get('templates', []))
            conflicts = enabled_templates.intersection(disabled_templates)

            if conflicts:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="conflicting_template_restrictions",
                    severity=Severity.ERROR,
                    message=f"Templates cannot be both enabled and disabled: {', '.join(conflicts)}",
                    suggestion="Remove conflicting templates from either enabled_on or disabled_on"
                )

        # Sections cannot use templates attribute (only app blocks)
        if file_type == 'section' and (enabled_on or disabled_on):
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="section_template_restriction",
                severity=Severity.WARNING,
                message="Regular sections should not use enabled_on/disabled_on",
                suggestion="Template restrictions are primarily for app blocks - consider if this is needed"
            )

    def validate_required_layout_objects(self, content: str, file_path: str, file_type: str):
        """
        HIGH: Validate layout files contain required objects (RequiredLayoutThemeObject rule)
        """
        if file_type != 'layout':
            return

        required_objects = [
            ('{{ content_for_header }}', 'content_for_header'),
            ('{{ content_for_layout }}', 'content_for_layout')
        ]

        for obj_pattern, obj_name in required_objects:
            if obj_pattern not in content:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="missing_required_layout_object",
                    severity=Severity.ERROR,
                    message=f"Layout missing required object: {obj_name}",
                    suggestion=f"Add {obj_pattern} to layout file - required for theme functionality"
                )

    def validate_hardcoded_routes(self, content: str, file_path: str):
        """
        HIGH: Validate against hardcoded routes (should use routes object)
        """
        hardcoded_routes = [
            (r'"/cart"', 'Use {{ routes.cart_url }}'),
            (r'"/search"', 'Use {{ routes.search_url }}'),
            (r'"/account"', 'Use {{ routes.account_url }}'),
            (r'"/collections"', 'Use {{ routes.collections_url }}'),
            (r'"/products"', 'Use {{ routes.all_products_collection_url }}'),
        ]

        for pattern, suggestion in hardcoded_routes:
            if re.search(pattern, content):
                line_num = self.find_line_number(content, pattern.strip('"'))
                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="hardcoded_route",
                    severity=Severity.WARNING,
                    message=f"Hardcoded route found: {pattern}",
                    suggestion=suggestion
                )

    def validate_deprecated_filters(self, content: str, file_path: str):
        """
        HIGH: Validate against deprecated Liquid filters
        """
        deprecated_filters = [
            ('| img_url', '| image_url'),
            ('| asset_img_url', '| image_url'),
            ('| collection_img_url', '| image_url'),
            ('| article_img_url', '| image_url'),
            ('| blog_img_url', '| image_url'),
        ]

        for old_filter, new_filter in deprecated_filters:
            if old_filter in content:
                line_num = self.find_line_number(content, old_filter)
                self.add_issue(
                    file_path=file_path,
                    line=line_num,
                    issue_type="deprecated_filter",
                    severity=Severity.WARNING,
                    message=f"Deprecated filter: {old_filter}",
                    suggestion=f"Use {new_filter} instead"
                )

    def validate_parser_blocking_javascript(self, content: str, file_path: str):
        """
        HIGH: Validate JavaScript uses defer or async attributes
        """
        script_pattern = r'<script\s+(?![^>]*(?:defer|async))[^>]*src=[^>]*>'
        matches = re.finditer(script_pattern, content, re.IGNORECASE)

        for match in matches:
            line_num = self.find_line_number(content, match.group())
            self.add_issue(
                file_path=file_path,
                line=line_num,
                issue_type="parser_blocking_javascript",
                severity=Severity.ERROR,
                message="JavaScript without defer or async attribute blocks rendering",
                suggestion="Add defer or async attribute to script tag"
            )

    def validate_asset_size_limits(self, file_path: str, file_type: str):
        """
        MEDIUM: Validate asset file sizes against Theme Store limits
        """
        if file_type != 'asset':
            return

        try:
            file_size = Path(file_path).stat().st_size
            file_ext = Path(file_path).suffix.lower()

            size_limits = {
                '.css': 100 * 1024,  # 100KB
                '.js': 10 * 1024,    # 10KB for app blocks, higher for themes
                '.jpg': 2 * 1024 * 1024,  # 2MB
                '.jpeg': 2 * 1024 * 1024,  # 2MB
                '.png': 2 * 1024 * 1024,  # 2MB
                '.gif': 2 * 1024 * 1024,  # 2MB
                '.svg': 100 * 1024,  # 100KB
            }

            if file_ext in size_limits and file_size > size_limits[file_ext]:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="asset_size_limit",
                    severity=Severity.WARNING,
                    message=f"Asset size ({file_size // 1024}KB) exceeds recommended limit ({size_limits[file_ext] // 1024}KB)",
                    suggestion="Optimize asset size for better performance"
                )
        except OSError:
            # File doesn't exist, skip size validation
            pass

    def validate_missing_assets(self, content: str, file_path: str):
        """
        HIGH: Validate referenced assets exist (MissingAsset rule)
        """
        asset_patterns = [
            (r"['\"]([^'\"]+\.css)['\"]", 'CSS'),
            (r"['\"]([^'\"]+\.js)['\"]", 'JavaScript'),
            (r"['\"]([^'\"]+\.(?:jpg|jpeg|png|gif|svg|webp))['\"]", 'Image'),
            (r"\|\s*asset_url\s*['\"]([^'\"]+)['\"]", 'Asset'),
        ]

        for pattern, asset_type in asset_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                asset_name = match.group(1)
                # Check if asset file exists in assets directory
                # This is a simplified check - in practice, you'd check the actual assets directory
                if not self.asset_exists(asset_name, file_path):
                    line_num = self.find_line_number(content, match.group())
                    self.add_issue(
                        file_path=file_path,
                        line=line_num,
                        issue_type="missing_asset",
                        severity=Severity.ERROR,
                        message=f"Referenced {asset_type.lower()} asset not found: {asset_name}",
                        suggestion=f"Ensure {asset_name} exists in assets directory"
                    )

    def asset_exists(self, asset_name: str, current_file_path: str) -> bool:
        """
        Helper method to check if asset exists
        """
        # Find the theme root by looking for assets directory
        current_path = Path(current_file_path)

        # Walk up the directory tree to find the theme root
        for parent in current_path.parents:
            assets_dir = parent / 'assets'
            if assets_dir.exists():
                asset_path = assets_dir / asset_name
                return asset_path.exists()

        # If we can't find assets directory, assume asset exists to avoid false positives
        return True

    def validate_schema_json_format(self, schema_content: str, file_path: str):
        """
        HIGH: Enhanced schema JSON validation with specific error messages
        """
        try:
            schema = json.loads(schema_content)
        except json.JSONDecodeError as e:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="invalid_schema_json",
                severity=Severity.CRITICAL,
                message=f"Invalid JSON in schema: {e}",
                suggestion="Fix JSON syntax errors in schema block"
            )
            return

        # Validate required schema properties
        if 'name' not in schema:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="missing_schema_name",
                severity=Severity.ERROR,
                message="Schema missing required 'name' property",
                suggestion="Add 'name' property to schema"
            )

        # Validate settings array structure
        if 'settings' in schema and not isinstance(schema['settings'], list):
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="invalid_settings_format",
                severity=Severity.ERROR,
                message="Schema 'settings' must be an array",
                suggestion="Change 'settings' to array format"
            )

    def validate_shopify_edge_cases(self, content: str, file_path: str, file_type: str):
        """
        MEDIUM: Comprehensive edge case validation for Shopify-specific scenarios
        """
        # Edge case 1: Invalid Liquid tag combinations
        self.validate_liquid_tag_combinations(content, file_path)

        # Edge case 2: Schema placement validation
        self.validate_schema_placement(content, file_path, file_type)

        # Edge case 3: Customer-specific template validation
        self.validate_customer_templates(content, file_path, file_type)

        # Edge case 4: Checkout-specific validation
        self.validate_checkout_specific(content, file_path, file_type)

        # Edge case 5: Gift card template validation
        self.validate_gift_card_template(content, file_path, file_type)

        # Edge case 6: JSON template structure validation
        self.validate_json_template_structure(content, file_path, file_type)

    def validate_liquid_tag_combinations(self, content: str, file_path: str):
        """
        Validate problematic Liquid tag combinations
        """
        # Invalid: Schema inside conditional blocks
        schema_in_conditional = re.search(r'{%\s*(?:if|unless|case|for)\s+[^%]*%}[^{]*{%\s*schema\s*%}', content, re.DOTALL)
        if schema_in_conditional:
            self.add_issue(
                file_path=file_path,
                line=self.find_line_number(content, '{% schema %}'),
                issue_type="schema_in_conditional",
                severity=Severity.CRITICAL,
                message="Schema block cannot be inside conditional Liquid tags",
                suggestion="Move schema block outside of if/unless/case/for statements"
            )

        # Invalid: Multiple schema blocks
        schema_count = len(re.findall(r'{%\s*schema\s*%}', content))
        if schema_count > 1:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="multiple_schema_blocks",
                severity=Severity.CRITICAL,
                message=f"Found {schema_count} schema blocks - only one allowed per file",
                suggestion="Combine all schema definitions into a single schema block"
            )

        # Warning: Complex nested liquid blocks
        nested_blocks = re.findall(r'{%\s*for\s+[^%]*%}[^{]*{%\s*for\s+[^%]*%}', content)
        if len(nested_blocks) > 3:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="excessive_nested_loops",
                severity=Severity.WARNING,
                message=f"Found {len(nested_blocks)} nested for loops - consider refactoring",
                suggestion="Extract complex logic into snippets for better maintainability"
            )

    def validate_schema_placement(self, content: str, file_path: str, file_type: str):
        """
        Validate schema block placement and format
        """
        if file_type not in self.SCHEMA_REQUIRED_TYPES:
            return

        schema_pattern = r'{%\s*schema\s*%}(.*?){%\s*endschema\s*%}'
        schema_match = re.search(schema_pattern, content, re.DOTALL)

        if schema_match:
            schema_content = schema_match.group(1).strip()

            # Schema should be at end of file (best practice)
            schema_position = schema_match.start()
            content_after_schema = content[schema_match.end():].strip()

            if content_after_schema and len(content_after_schema) > 50:
                self.add_issue(
                    file_path=file_path,
                    line=self.find_line_number(content, '{% schema %}'),
                    issue_type="schema_not_at_end",
                    severity=Severity.WARNING,
                    message="Schema block should typically be at the end of the file",
                    suggestion="Move schema block to end of file for better organization"
                )

            # Validate JSON formatting in schema
            try:
                json.loads(schema_content)
            except json.JSONDecodeError as e:
                self.add_issue(
                    file_path=file_path,
                    line=self.find_line_number(content, '{% schema %}'),
                    issue_type="malformed_schema_json",
                    severity=Severity.CRITICAL,
                    message=f"Malformed JSON in schema: {e}",
                    suggestion="Fix JSON syntax errors in schema block"
                )

    def validate_customer_templates(self, content: str, file_path: str, file_type: str):
        """
        Validate customer-specific templates have required elements
        """
        if 'customers' not in file_path:
            return

        customer_template_requirements = {
            'customers/order': ['{{ order.', '{% paginate'],
            'customers/account': ['{{ customer.', 'addresses'],
            'customers/addresses': ['{{ address.', 'form'],
            'customers/login': ['customer_login_form', 'customer_register_link'],
            'customers/register': ['customer_register_form', 'customer_login_link'],
        }

        for template_path, required_elements in customer_template_requirements.items():
            if template_path in file_path:
                for element in required_elements:
                    if element not in content:
                        self.add_issue(
                            file_path=file_path,
                            line=0,
                            issue_type="missing_customer_element",
                            severity=Severity.WARNING,
                            message=f"Customer template missing recommended element: {element}",
                            suggestion=f"Consider adding {element} for complete customer functionality"
                        )

    def validate_checkout_specific(self, content: str, file_path: str, file_type: str):
        """
        Validate checkout-specific template requirements
        """
        if 'checkout' not in file_path:
            return

        # Checkout templates have special requirements
        if file_type == 'layout' and 'checkout.liquid' in file_path:
            required_checkout_elements = [
                '{{ content_for_header }}',
                '{{ checkout_html_classes }}',
                '{{ checkout_stylesheets }}',
                '{{ checkout_scripts }}'
            ]

            for element in required_checkout_elements:
                if element not in content:
                    self.add_issue(
                        file_path=file_path,
                        line=0,
                        issue_type="missing_checkout_element",
                        severity=Severity.ERROR,
                        message=f"Checkout layout missing required element: {element}",
                        suggestion=f"Add {element} to checkout.liquid for proper functionality"
                    )

    def validate_gift_card_template(self, content: str, file_path: str, file_type: str):
        """
        Validate gift card template requirements
        """
        if 'gift_card' not in file_path:
            return

        gift_card_elements = [
            '{{ gift_card.',
            '{{ shop.name }}',
            'qr_code'
        ]

        for element in gift_card_elements:
            if element not in content:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="missing_gift_card_element",
                    severity=Severity.WARNING,
                    message=f"Gift card template missing recommended element: {element}",
                    suggestion=f"Consider adding {element} for complete gift card functionality"
                )

    def validate_json_template_structure(self, content: str, file_path: str, file_type: str):
        """
        Validate JSON template structure and references
        """
        if file_type != 'template_json':
            return

        try:
            template_data = json.loads(content)
        except json.JSONDecodeError as e:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="invalid_json_template",
                severity=Severity.CRITICAL,
                message=f"Invalid JSON in template: {e}",
                suggestion="Fix JSON syntax errors in template file"
            )
            return

        # Validate required structure
        required_keys = ['sections', 'order']
        for key in required_keys:
            if key not in template_data:
                self.add_issue(
                    file_path=file_path,
                    line=0,
                    issue_type="missing_template_key",
                    severity=Severity.ERROR,
                    message=f"JSON template missing required key: {key}",
                    suggestion=f"Add '{key}' to template structure"
                )

        # Validate section references exist
        if 'sections' in template_data:
            for section_id, section_config in template_data['sections'].items():
                if 'type' in section_config:
                    section_type = section_config['type']
                    # This would need to check if the section file actually exists
                    # For now, we'll do a basic validation
                    if not section_type or section_type.strip() == '':
                        self.add_issue(
                            file_path=file_path,
                            line=0,
                            issue_type="empty_section_type",
                            severity=Severity.ERROR,
                            message=f"Section '{section_id}' has empty type",
                            suggestion="Specify a valid section type"
                        )

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
        """
        Validate schema integrity using official Theme Check compatible file type detection
        """
        path_obj = Path(file_path)
        file_type = self.detect_file_type(path_obj, content)

        # Extract schema
        schema_match = re.search(r'{% schema %}(.*?){% endschema %}', content, re.DOTALL)
        has_schema = bool(schema_match)
        should_have = self.should_have_schema(file_type, path_obj, content)

        # Validate schema requirements based on official rules
        if should_have and not has_schema:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="missing_schema",
                severity=Severity.ERROR,
                message=f"{file_type.replace('_', ' ').title()} requires schema block"
            )
            return
        elif not should_have and has_schema:
            self.add_issue(
                file_path=file_path,
                line=0,
                issue_type="unexpected_schema",
                severity=Severity.WARNING,
                message=f"{file_type.replace('_', ' ').title()} should not have schema block"
            )
            return
        elif not has_schema:
            # No schema and none required - skip validation
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

        # CRITICAL: Validate @app blocks (Theme Store requirement)
        self.validate_app_blocks(schema, file_path, file_type)

        # CRITICAL: Validate wrapper sections (apps.liquid, _blocks.liquid)
        if file_type == 'wrapper_section':
            self.validate_wrapper_section(schema, file_path, path_obj.name)

        # HIGH: Validate block nesting depth (8-level maximum per Shopify limits)
        self.validate_block_nesting_depth(content, file_path)

        # HIGH: Validate template restrictions (enabled_on/disabled_on)
        self.validate_template_restrictions(schema, file_path, file_type)

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

        # NEW: Official Theme Check validation rules
        path_obj = Path(file_path_str)
        file_type = self.detect_file_type(path_obj, content)

        self.validate_required_layout_objects(content, file_path_str, file_type)
        self.validate_hardcoded_routes(content, file_path_str)
        self.validate_deprecated_filters(content, file_path_str)
        self.validate_parser_blocking_javascript(content, file_path_str)
        self.validate_asset_size_limits(file_path_str, file_type)
        self.validate_missing_assets(content, file_path_str)

        # NEW: Comprehensive edge case validation
        self.validate_shopify_edge_cases(content, file_path_str, file_type)

        # NEW: Comprehensive Liquid syntax validation
        if self.liquid_validator and file_type in ['section', 'layout', 'template_liquid', 'snippet', 'theme_block']:
            self.validate_liquid_syntax_comprehensive(content, file_path_str)

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

    def validate_liquid_syntax_comprehensive(self, content: str, file_path: str):
        """
        CRITICAL: Comprehensive Liquid syntax validation using python-liquid parser

        Integrates the dedicated Liquid syntax validator to catch all syntax issues
        that could cause theme failures or deployment problems.
        """
        if not self.liquid_validator:
            return

        # Run comprehensive validation
        validation_result = self.liquid_validator.validate_content(
            content, file_path, validation_level='comprehensive'
        )

        # Convert Liquid validation issues to our issue format
        for liquid_issue in self.liquid_validator.issues:
            # Map Liquid severity to our severity
            severity_mapping = {
                LiquidErrorSeverity.CRITICAL: Severity.CRITICAL,
                LiquidErrorSeverity.ERROR: Severity.ERROR,
                LiquidErrorSeverity.WARNING: Severity.WARNING,
                LiquidErrorSeverity.INFO: Severity.INFO
            }

            mapped_severity = severity_mapping.get(liquid_issue.severity, Severity.ERROR)

            self.add_issue(
                file_path=file_path,
                line=liquid_issue.line_number,
                issue_type=f"liquid_{liquid_issue.error_type}",
                severity=mapped_severity,
                message=f"Liquid {liquid_issue.error_type}: {liquid_issue.message}",
                suggestion=liquid_issue.suggestion or "Fix Liquid syntax error",
                pattern=liquid_issue.context or ""
            )

        # Clear the liquid validator issues to avoid memory buildup
        self.liquid_validator.clear_issues()

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