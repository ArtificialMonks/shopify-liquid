# 🛡️ Comprehensive Shopify Liquid Validation Framework

**Progressive Validation System for Development, Production, and Ultimate Quality Assurance**

*Updated: January 2025 - Based on comprehensive research synthesis*

---

## 🎯 **Validation Levels Overview**

### **Development Level** (Fast Feedback)
- **Purpose**: Catch critical issues during development
- **Tolerance**: Warning for UX issues, Error for breaking issues
- **Command**: `./scripts/validate-theme.sh development`

### **Production Level** (Theme Store Ready)
- **Purpose**: Ensure Theme Store compliance
- **Tolerance**: Error for all compliance violations
- **Command**: `./scripts/validate-theme.sh production`

### **Ultimate Level** (Zero Tolerance)
- **Purpose**: Comprehensive validation with zero tolerance
- **Tolerance**: Error for any suboptimal patterns
- **Command**: `./scripts/validate-theme.sh ultimate`

---

## 🚨 **CRITICAL VALIDATION CHECKS (All Levels)**

### **1. Liquid Syntax & Structure**
- [ ] ✅ **Valid Liquid tags only** - No `{% doc %}`, `{% endraw %}` without `{% raw %}`
- [ ] ✅ **Proper tag pairing** - All opening tags have corresponding closing tags
- [ ] ✅ **Liquid block endings** - End with `%}`, not `-%}`
- [ ] ✅ **Nesting depth limit** - Maximum 8 levels (Shopify platform limit)
- [ ] ✅ **Schema placement** - Must be at root level, not nested in conditionals

### **2. Filter Validation (Critical)**
- [ ] ✅ **No hallucinated filters** - Only use [official Shopify filters](https://shopify.dev/docs/api/liquid/filters)
- [ ] ✅ **Filter parameters** - Required parameters provided, correct data types
- [ ] ✅ **Deprecated filter warnings** - Replace `img_url` with `image_url`

**Critical Filter Replacements:**
```liquid
❌ {{ image | image_tag }}        → ✅ {{ image | image_url }}
❌ {{ form | payment_button_tag }} → ✅ {{ form | payment_button }}
❌ {{ data | structured_data }}    → ✅ {{ data | json }}
❌ {{ products | color_extract }}   → ✅ Use color_brightness, color_lighten
```

### **3. Performance Anti-Patterns (CRITICAL)**
- [ ] ✅ **No collections.all.products** - PERFORMANCE KILLER (causes timeouts)
- [ ] ✅ **Loop limits enforced** - All loops have pagination or limits ≤50 items
- [ ] ✅ **No nested loop complexity** - Avoid O(n³) patterns
- [ ] ✅ **Image size limits** - Maximum 3000px width for performance
- [ ] ✅ **Asset size compliance** - JavaScript ≤16KB, CSS ≤100KB

**Performance Validation Patterns:**
```python
# Automated detection patterns
CRITICAL_PERFORMANCE_KILLERS = [
    r'{% for product in collections\.all\.products %}',  # BREAKS THEMES
    r'collections\.all\.products\.size',                  # SLOW EVALUATION
    r'{% for [^}]+ %}\s*{% for [^}]+ %}\s*{% for [^}]+ %}', # TRIPLE NESTING
]
```

### **4. Security Validation (ERROR LEVEL)**
- [ ] ✅ **Content escaping** - All user content uses `| escape` filter
- [ ] ✅ **Form input sanitization** - Proper validation patterns and maxlength
- [ ] ✅ **URL parameter safety** - Validate before use, prevent injection
- [ ] ✅ **No raw HTML output** - Remove `| raw` filter from user content

### **5. Schema Configuration (Context-Aware)**
- [ ] ✅ **Range step validation** - Ensure `(max - min) / step ≤ 101`
- [ ] ✅ **Context-specific rules** - `enabled_on` only in app blocks, not sections
- [ ] ✅ **Valid setting types** - Use `video` not `file` for video uploads
- [ ] ✅ **Unique setting IDs** - Descriptive and collision-free identifiers

---

## 📊 **PROGRESSIVE VALIDATION CRITERIA**

### **Level 1: Development Validation**

#### **Basic Syntax & Structure**
```yaml
# Fast validation with quick feedback
validations:
  liquid_syntax: ERROR
  tag_pairing: ERROR
  basic_performance: WARNING
  filter_existence: ERROR
  object_references: ERROR
```

#### **UX-Focused Validation**
```python
def validate_range_ux(setting):
    """UX assessment for range settings"""
    steps = (max_val - min_val) / step

    if steps > 101:  # Technical requirement
        return {'level': 'error', 'message': f'Range exceeds 101 steps ({steps})'}
    if steps > 50:   # UX assessment
        return {'level': 'warning', 'message': f'Range has {steps} steps - consider larger step size'}
```

### **Level 2: Production Validation**

#### **Theme Store Compliance**
```yaml
# Theme Store submission requirements
compliance_checks:
  performance_score: 60        # Minimum Lighthouse score
  accessibility_score: 90     # WCAG 2.1 AA compliance
  javascript_size: 16384      # 16KB max minified
  external_assets: false      # Must use Shopify CDN
  semantic_html: required     # Proper heading hierarchy
```

#### **Security Requirements**
```python
# Security validation patterns
SECURITY_PATTERNS = [
    {
        'pattern': r'settings\.[^|]+(?!\s*\|\s*escape)',
        'severity': 'ERROR',
        'message': 'User content must be escaped',
        'wcag': 'N/A',
        'fix': 'Add | escape filter'
    }
]
```

### **Level 3: Ultimate Validation**

#### **Zero Tolerance Quality**
```yaml
# Comprehensive validation with zero tolerance
ultimate_checks:
  code_complexity: ERROR      # No over-engineering patterns
  performance_optimization: ERROR  # All performance best practices
  accessibility_complete: ERROR    # Full WCAG compliance
  security_hardened: ERROR         # Comprehensive security patterns
  schema_template_integration: ERROR # Schema settings properly used
```

#### **Cross-Domain Integration Validation**
```python
def validate_schema_template_integration(schema, liquid_content):
    """Validate schema settings are properly used in templates"""
    defined_settings = {s.get('id') for s in schema.get('settings', [])}
    used_settings = extract_used_settings(liquid_content)

    undefined = used_settings - defined_settings
    if undefined:
        return {'level': 'error', 'message': f'Settings used but not defined: {undefined}'}
```

---

## 🔐 **SECURITY VALIDATION FRAMEWORK**

### **XSS Prevention (Automated)**
```python
# Automated security validation
SECURITY_VALIDATIONS = [
    {
        'pattern': r'customer\.[^|]+(?!\s*\|\s*escape)',
        'message': 'Customer data must be escaped',
        'severity': 'ERROR'
    },
    {
        'pattern': r'form\.[^|]+(?!\s*\|\s*escape)',
        'message': 'Form data must be escaped',
        'severity': 'ERROR'
    },
    {
        'pattern': r'settings\.[^|]*\|\s*raw',
        'message': 'Raw HTML output creates XSS vulnerability',
        'severity': 'ERROR'
    }
]
```

### **Content Security Policy Validation**
```liquid
{% comment %} CSP-compliant theme.liquid {% endcomment %}
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self' *.shopifycdn.com;
  script-src 'self' 'unsafe-inline' *.shopify.com;
  style-src 'self' 'unsafe-inline' fonts.googleapis.com;
  img-src 'self' data: *.shopifycdn.com;
">
```

### **Manual Security Review Checkpoints**
- [ ] All user-configurable text uses `| escape` filter
- [ ] URL parameters validated before use
- [ ] Form inputs have proper maxlength and pattern validation
- [ ] Custom CSS settings don't allow `<script>` injection
- [ ] External scripts loaded only from allowed domains

---

## ♿ **ACCESSIBILITY VALIDATION FRAMEWORK**

### **WCAG 2.1 AA Compliance (Automated)**
```python
# Automated accessibility validation
ACCESSIBILITY_VALIDATIONS = [
    {
        'pattern': r'<h([1-6])[^>]*>',
        'validator': 'validate_heading_hierarchy',
        'wcag': '1.3.1',
        'severity': 'ERROR'
    },
    {
        'pattern': r'<input[^>]+>',
        'validator': 'validate_input_labels',
        'wcag': '3.3.2',
        'severity': 'ERROR'
    }
]
```

### **Color Contrast Validation**
```python
def validate_color_contrast(css_content):
    """Validate color contrast ratios meet WCAG AA (4.5:1)"""
    # Calculate contrast ratios for color combinations
    # Flag ratios below 4.5:1 as errors
```

### **Manual Accessibility Review**
- [ ] Single h1 element per page
- [ ] Heading levels follow logical sequence
- [ ] All images have appropriate alt text
- [ ] Form inputs have programmatically associated labels
- [ ] Focus indicators visible (2px minimum outline)
- [ ] Skip links provided for main content
- [ ] ARIA landmarks properly used

---

## 🚀 **AUTOMATED VALIDATION IMPLEMENTATION**

### **Validation Pipeline Integration**
```bash
#!/bin/bash
# Enhanced validation workflow

# Level 1: Development (Fast feedback)
echo "🔍 Development validation..."
./scripts/validate-liquid-syntax.py --level development || exit 1

# Level 2: Production (Theme Store ready)
if [ "$VALIDATION_LEVEL" = "production" ]; then
    echo "🏪 Production validation..."
    ./scripts/validate-theme-store-compliance.py || exit 1
    ./scripts/validate-performance-thresholds.py || exit 1
fi

# Level 3: Ultimate (Zero tolerance)
if [ "$VALIDATION_LEVEL" = "ultimate" ]; then
    echo "🎯 Ultimate validation..."
    ./scripts/validate-security-patterns.py --strict || exit 1
    ./scripts/validate-accessibility-compliance.py --wcag-aa || exit 1
    ./scripts/validate-cross-domain-integration.py || exit 1
fi
```

### **Context-Aware Schema Validation**
```python
def validate_schema_context(file_path, schema):
    """Context-aware validation based on file type"""
    if '/sections/' in str(file_path):
        return validate_section_schema(schema)
    elif schema.get('target') == 'section':
        return validate_app_block_schema(schema)
    else:
        return validate_theme_block_schema(schema)
```

### **Performance Metrics Integration**
```python
# Theme Store performance calculation
def calculate_theme_score(scores):
    """Official Theme Store score calculation"""
    weighted_score = (
        (scores['product_page'] * 31) +
        (scores['collection_page'] * 33) +
        (scores['home_page'] * 13)
    ) / 77
    return {
        'score': round(weighted_score),
        'minimum': 60,
        'passed': weighted_score >= 60
    }
```

---

## 📋 **VALIDATION COMMAND REFERENCE**

### **Development Workflow**
```bash
# Quick development validation
./scripts/validate-theme.sh development

# Auto-fix common issues
./scripts/fix-liquid-syntax.py ./path/to/theme

# Individual file validation
python3 ./scripts/ultimate-validator.py ./path/to/file.liquid
```

### **Production Deployment**
```bash
# Theme Store readiness check
./scripts/validate-theme.sh production

# Performance validation
lighthouse --only-categories=performance --output=json "${THEME_URL}"

# Accessibility validation
lighthouse --only-categories=accessibility --output=json "${THEME_URL}"
```

### **Ultimate Quality Assurance**
```bash
# Zero tolerance validation
./scripts/validate-theme.sh ultimate

# Security audit
./scripts/security-validator.py --comprehensive

# Cross-domain validation
./scripts/validate-integration.py --all-domains
```

---

## ⚡ **PERFORMANCE OPTIMIZATION THRESHOLDS**

### **Critical Performance Limits**
```yaml
# Shopify platform limits
platform_constraints:
  variant_limit: 250           # product.variants max return
  pagination_limit: 25000      # paginate max items
  loop_iteration_limit: 50     # for loops without pagination
  nested_loop_warning: 3       # performance degradation threshold

# Asset size requirements
asset_limits:
  javascript_bundle: 16384     # 16KB minified (Theme Store)
  css_file: 102400            # 100KB max per file
  image_width: 3000           # Maximum image width for performance
```

### **Core Web Vitals Thresholds**
```yaml
# Theme Store requirements
core_web_vitals:
  first_contentful_paint: 2.5   # seconds max
  largest_contentful_paint: 4.0 # seconds max
  cumulative_layout_shift: 0.25 # max score
  performance_score: 60         # Lighthouse minimum
```

---

## 🎯 **IMPLEMENTATION ROADMAP**

### **Phase 1: Critical Validation (Week 1)**
1. ✅ Implement performance anti-pattern detection
2. ✅ Add security escape pattern validation
3. ✅ Create basic accessibility validation
4. ✅ Integrate with existing validation scripts

### **Phase 2: Production Compliance (Week 2)**
1. ✅ Theme Store compliance validation
2. ✅ Performance threshold enforcement
3. ✅ WCAG 2.1 AA validation framework
4. ✅ Context-aware schema validation

### **Phase 3: Ultimate Quality (Week 3)**
1. ✅ Cross-domain integration validation
2. ✅ Advanced security pattern detection
3. ✅ Performance optimization suggestions
4. ✅ Automated accessibility testing integration

---

## 📚 **VALIDATION RESOURCES**

### **Official Documentation**
- **Shopify Filters**: [shopify.dev/docs/api/liquid/filters](https://shopify.dev/docs/api/liquid/filters)
- **Shopify Objects**: [shopify.dev/docs/api/liquid/objects](https://shopify.dev/docs/api/liquid/objects)
- **Theme Check**: [github.com/Shopify/theme-check](https://github.com/Shopify/theme-check)
- **WCAG Guidelines**: [www.w3.org/WAI/WCAG21/quickref/](https://www.w3.org/WAI/WCAG21/quickref/)

### **Internal Documentation**
- **Schema Guidelines**: `./shopify-liquid-guides/schema-validation/schema-guidelines.md`
- **Performance Research**: `./shopify-liquid-guides/docs/liquid-research/performance-optimization-validation.md`
- **Security Framework**: `./shopify-liquid-guides/docs/liquid-research/security-accessibility-validation.md`
- **Syntax Validation**: `./shopify-liquid-guides/docs/liquid-research/syntax-structure-validation.md`

---

## 🔥 **CRITICAL SUCCESS METRICS**

### **Validation Effectiveness**
- **Development Efficiency**: 50% reduction in validation errors
- **Theme Store Approval Rate**: 95% first-submission approval
- **Performance Score**: Average 75+ (above 60 minimum)
- **Security Compliance**: 100% XSS vulnerability detection

### **Developer Experience**
- **Validation Speed**: <5 seconds for development level
- **False Positive Rate**: <5% incorrect warnings
- **Automation Coverage**: 80% of issues caught automatically
- **Manual Review Efficiency**: Clear, actionable guidance

---

*Keep this comprehensive checklist as your single source of truth for Shopify Liquid validation across all development stages!*

---

## 📋 **Common Error Patterns**

### **❌ Invalid Liquid Tags**
```liquid
{% doc %}...{% enddoc %}           <!-- WRONG: doesn't exist -->
{% comment %}...{% endcomment %}   <!-- CORRECT: standard tag -->
```

### **❌ Unknown Filters**
```liquid
{{ image | image_tag }}           <!-- WRONG: doesn't exist -->
{{ image | image_url }}           <!-- CORRECT: valid filter -->

{{ form | payment_button_tag }}   <!-- WRONG: doesn't exist -->
{{ form | payment_button }}       <!-- CORRECT: valid filter -->

{{ data | structured_data }}      <!-- WRONG: doesn't exist -->
{{ data | json }}                 <!-- CORRECT: valid filter -->
```

### **❌ Performance Issues**
```liquid
{% for collection in collections %}              <!-- WRONG: unlimited -->
{% for collection in collections limit: 50 %}   <!-- CORRECT: limited -->

{% for product in collections.all.products %}   <!-- WRONG: breaks themes -->
{% for product in collection.products %}        <!-- CORRECT: specific collection -->
```

### **❌ Liquid Block Errors**
```liquid
{%- liquid
  assign var = 'value'
-%}                                <!-- WRONG: invalid ending -->

{% liquid
  assign var = 'value'
%}                                 <!-- CORRECT: proper ending -->
```

### **❌ Object Reference Errors**
```liquid
{{ form.errors | default: errors }}    <!-- WRONG: 'errors' undefined -->
{{ form.errors | default: '' }}        <!-- CORRECT: valid fallback -->
```

---

## 🎯 **Required Translation Keys**

### **Minimum Required in `locales/en.default.json`**
```json
{
  "general": {
    "accessibility": {
      "close": "Close"
    },
    "search": {
      "placeholder": "Search",
      "submit": "Search"
    }
  },
  "products": {
    "product": {
      "add_to_cart": "Add to cart",
      "choose_options": "Choose options",
      "sold_out": "Sold out",
      "sale": "Sale",
      "price_from": "From",
      "view_product": "View product"
    }
  },
  "sections": {
    "gallery": {
      "view_portfolio": "View portfolio",
      "empty_title": "Gallery is empty",
      "empty_description": "Add some content"
    }
  }
}
```

---

## 🚀 **Validation Workflow**

### **Development Process**
1. **Write/Edit** Liquid code
2. **Run Auto-Fix**: `./scripts/fix-liquid-syntax.py`
3. **Check Syntax**: `shopify theme check`
4. **Test Locally**: Preview in Shopify CLI
5. **Final Validation**: Theme Check passes with 0 errors

### **Pre-Commit Checklist**
- [ ] Auto-fix script run
- [ ] Theme Check passes
- [ ] All translation keys exist
- [ ] Performance limits in place
- [ ] No undefined objects referenced

---

## 📚 **Quick Reference Links**

- **Official Shopify Filters**: [shopify.dev/docs/api/liquid/filters](https://shopify.dev/docs/api/liquid/filters)
- **Official Shopify Objects**: [shopify.dev/docs/api/liquid/objects](https://shopify.dev/docs/api/liquid/objects)
- **Theme Check Rules**: [github.com/Shopify/theme-check](https://github.com/Shopify/theme-check)
- **Schema Guidelines**: `./shopify-liquid-guides/schema-validation/schema-guidelines.md`
- **Error Fix Documentation**: `./error-fix.md`

---

*Keep this checklist handy during development to prevent common validation errors!*