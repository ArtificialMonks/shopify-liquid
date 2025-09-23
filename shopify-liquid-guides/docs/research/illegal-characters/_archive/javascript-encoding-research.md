# JavaScript Character Encoding Research - Shopify Liquid Upload Errors

## Research Summary

This document contains comprehensive research findings on JavaScript character encoding issues that cause Shopify theme upload errors.

## Critical Context Separation Rule

**Primary Issue**: Shopify's parser strictly separates Liquid and JavaScript contexts. Upload errors occur when mixing these contexts.

**Official Rule**: "Liquid code isn't supported within `{% javascript %}` and `{% stylesheet %}` tags"

## Problematic Patterns That Cause Upload Failures

### 1. Liquid Inside JavaScript Tags (CRITICAL ERROR)

**Failing Pattern**:
```liquid
{% javascript %}
  var themeColor = "{{ settings.theme_color }}";
  const productId = {{ product.id }};
{% endjavascript %}
```

**Error Messages**:
- "Invalid syntax in JavaScript block"
- "Liquid parsing error in script context"
- "Theme validation failed: StaticStylesheetAndJavascriptTags"

**Solution**: Use data attributes or configuration objects

### 2. Arrow Functions in Mixed Context

**Failing Pattern**:
```liquid
<script>
  const items = {{ collection.products | json }};
  items.forEach(item => {
    console.log(`Product: ${item.title}`);
  });
</script>
```

**Working Pattern**:
```liquid
<script>
  const items = {{ collection.products | json }};
  items.forEach(function(item) {
    console.log('Product: ' + item.title);
  });
</script>
```

### 3. Template Literals with Liquid Interpolation

**Failing Pattern**:
```liquid
{% javascript %}
  const message = `Welcome to {{ shop.name }}!`;
{% endjavascript %}
```

**Working Pattern**:
```liquid
<div data-shop-name="{{ shop.name }}"></div>
{% javascript %}
  const shopName = document.querySelector('[data-shop-name]').dataset.shopName;
  const message = `Welcome to ${shopName}!`;
{% endjavascript %}
```

## Unicode and Character Encoding Issues

### UTF-8 BOM Characters
- Files saved with UTF-8 BOM cause parsing errors
- Solution: Save files as UTF-8 without BOM

### Non-ASCII Characters in JavaScript Identifiers
**Failing**: `const café_config = { };`
**Working**: `const cafe_config = { };`

## Quote Escaping Issues

### Nested Quote Problems
**Failing**: `const message = "{{ product.title | replace: '"', '\"' }}";`
**Working**: `const message = {{ product.title | json }};`

## Detection Patterns for Automated Validation

```python
JAVASCRIPT_ENCODING_ISSUES = [
    {
        'pattern': r'{%\s*javascript\s*%}[^{]*{{\s*[^}]*\s*}}',
        'message': 'CRITICAL: Liquid code inside {% javascript %} tag',
        'severity': 'CRITICAL'
    },
    {
        'pattern': r'<script[^>]*>[^<]*{{\s*[^}]*\s*}}',
        'message': 'ERROR: Liquid interpolation in script tag',
        'severity': 'ERROR'
    },
    {
        'pattern': r'const\s+[^\x00-\x7F]+\s*=',
        'message': 'WARNING: Non-ASCII characters in JavaScript identifier',
        'severity': 'WARNING'
    }
]
```

## Character Substitution Mappings

| Problematic | Safe Alternative | Context |
|-------------|------------------|---------|
| `{{ liquid }}` in JS | `data-*` attributes | JavaScript blocks |
| `"` in Liquid strings | `| json` filter | Quote escaping |
| `café` | `cafe` | JavaScript identifiers |
| Template literals with Liquid | String concatenation | Mixed contexts |

## Best Practices

### Configuration Objects Pattern
```liquid
<script>
  window.theme = {
    shopName: {{ shop.name | json }},
    cartUrl: {{ routes.cart_url | json }}
  };
</script>

{% javascript %}
  const message = `Welcome to ${window.theme.shopName}!`;
{% endjavascript %}
```

### Data Attributes Pattern
```liquid
<div id="app" data-shop-name="{{ shop.name | escape }}">
</div>

{% javascript %}
  const app = document.getElementById('app');
  const shopName = app.dataset.shopName;
{% endjavascript %}
```