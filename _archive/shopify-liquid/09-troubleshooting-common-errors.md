# Shopify Liquid Troubleshooting Guide

## Common Validation Errors and Solutions

### 1. Range Setting Decimal Digits Error

**Error Message:**
```
Invalid schema: setting with id="heading_letter_spacing" min must have 1 or less decimal digits
```

**Root Cause:**
Shopify's range settings have strict validation rules for decimal places:
- `min`, `max`, and `default` values can have **maximum 1 decimal place**
- `step` values can have **maximum 1 decimal place**
- Values like `1.05`, `0.75`, `0.125` are NOT allowed
- Values like `1.0`, `0.5`, `1.1` ARE allowed

**Solution:**

❌ **Wrong:**
```json
{
  "type": "range",
  "id": "heading_letter_spacing",
  "label": "Letter Spacing",
  "min": 0.05,      // 2 decimal places - NOT ALLOWED
  "max": 0.25,      // 2 decimal places - NOT ALLOWED
  "step": 0.05,     // 2 decimal places - NOT ALLOWED
  "default": 0.1,
  "unit": "em"
}
```

✅ **Correct:**
```json
{
  "type": "range",
  "id": "heading_letter_spacing",
  "label": "Letter Spacing",
  "min": 0.1,       // 1 decimal place - OK
  "max": 0.3,       // 1 decimal place - OK
  "step": 0.1,      // 1 decimal place - OK
  "default": 0.1,
  "unit": "em"
}
```

**Alternative Solutions:**

1. **Use integers with smaller units:**
```json
{
  "type": "range",
  "id": "heading_letter_spacing",
  "label": "Letter Spacing (in 0.01em)",
  "min": 5,         // Represents 0.05em
  "max": 25,        // Represents 0.25em
  "step": 5,        // Represents 0.05em steps
  "default": 10,    // Represents 0.10em
  "unit": ""        // No unit, handle in Liquid
}
```

Then in your Liquid:
```liquid
letter-spacing: {{ settings.heading_letter_spacing | times: 0.01 }}em;
```

2. **Use a number input instead of range:**
```json
{
  "type": "number",
  "id": "heading_letter_spacing",
  "label": "Letter Spacing",
  "placeholder": "0.1",
  "info": "Enter letter spacing in em units (e.g., 0.05)"
}
```

### 2. Liquid Syntax Ternary Operator Error

**Error Message:**
```
Liquid syntax error: Expected dotdot but found comparison
Expected end_of_string but found question
```

**Root Cause:**
Liquid doesn't support JavaScript-style ternary operators (`condition ? true : false`)

**Solution:**

❌ **Wrong:**
```liquid
{{ settings.show_button ? 'block' : 'none' }}
{{ value > 10 ? 'large' : 'small' }}
opacity: {{ settings.show_overlay ? '1' : '0' }};
```

✅ **Correct:**
```liquid
{% if settings.show_button %}block{% else %}none{% endif %}
{% if value > 10 %}large{% else %}small{% endif %}
opacity: {% if settings.show_overlay %}1{% else %}0{% endif %};
```

**Alternative with assign:**
```liquid
{% assign display_value = 'none' %}
{% if settings.show_button %}
  {% assign display_value = 'block' %}
{% endif %}
display: {{ display_value }};
```

### 3. Liquid Comparison Operator Errors

**Error Message:**
```
Liquid syntax error (line X): Expected dotdot but found comparison in "(src_type == 'mp4' and section.settings.mp4_file != blank)"
```

**Root Cause:**
Complex conditional logic needs proper Liquid syntax, not JavaScript-style comparisons in certain contexts.

**Solution:**

❌ **Wrong (in certain contexts):**
```liquid
{% if (src_type == 'mp4' and section.settings.mp4_file != blank) or (src_type == 'shopify' and section.settings.shopify_video != blank) %}
```

✅ **Correct:**
```liquid
{% if src_type == 'mp4' %}
  {% if section.settings.mp4_file != blank %}
    <!-- Handle MP4 -->
  {% endif %}
{% elsif src_type == 'shopify' %}
  {% if section.settings.shopify_video != blank %}
    <!-- Handle Shopify video -->
  {% endif %}
{% endif %}
```

**Or use proper parentheses:**
```liquid
{% assign has_mp4 = false %}
{% assign has_shopify = false %}

{% if src_type == 'mp4' and section.settings.mp4_file != blank %}
  {% assign has_mp4 = true %}
{% endif %}

{% if src_type == 'shopify' and section.settings.shopify_video != blank %}
  {% assign has_shopify = true %}
{% endif %}

{% if has_mp4 or has_shopify %}
  <!-- Handle video -->
{% endif %}
```

### 4. Mathematical Operations with Decimals

**Error Message:**
```
Liquid error: divided by 0
```

**Root Cause:**
When using filters like `times`, `divided_by`, ensure proper rounding for display values.

**Solution:**

❌ **Wrong:**
```liquid
{{ value | times: 0.8 }}px          // May produce 15.6px
{{ opacity | times: 0.5 }}          // May produce 0.35
```

✅ **Correct:**
```liquid
{{ value | times: 0.8 | round }}px  // Produces 16px
{{ opacity | times: 0.5 | round: 2 }} // Produces 0.35 (for opacity)
```

### 5. Common Schema Validation Rules

**Key Rules to Remember:**

1. **Range Settings:**
   - Max 1 decimal place for min, max, step, default
   - All values must be numbers (not strings)
   - Default is required

2. **Select Settings:**
   - Options must have both `value` and `label`
   - Default must match one of the option values

3. **Color Settings:**
   - Default must be a valid hex color with #
   - Example: `"default": "#000000"`

4. **URL Settings:**
   - Use `type: "url"` not `type: "text"` for links
   - Shopify will validate URL format

5. **Checkbox Settings:**
   - Default must be boolean (true/false)
   - Not "true" or "false" as strings

### 6. Best Practices to Avoid Errors

1. **Always validate your schema:**
```bash
# Use Shopify CLI to validate
shopify theme check
```

2. **Test in development first:**
```bash
# Push to development theme
shopify theme push --development
```

3. **Use proper Liquid filters:**
```liquid
{{ string | escape }}           // For HTML escaping
{{ string | strip_html }}       // Remove HTML tags
{{ number | round }}            // Round to integer
{{ number | round: 2 }}         // Round to 2 decimals
{{ string | handleize }}        // Create URL-safe strings
```

4. **Handle edge cases:**
```liquid
{% if collection.products.size > 0 %}
  <!-- Show products -->
{% else %}
  <!-- Show empty state -->
{% endif %}
```

5. **Use unless for negative conditions:**
```liquid
{% unless settings.hide_header %}
  <!-- Show header -->
{% endunless %}
```

### 7. Debugging Tips

1. **Use the Liquid comment tag to debug:**
```liquid
{% comment %}
  Debug info:
  Value: {{ settings.value }}
  Type: {{ settings.value.type }}
{% endcomment %}
```

2. **Output values for testing:**
```liquid
<!-- DEBUG: {{ variable | json }} -->
```

3. **Check if variables exist:**
```liquid
{% if variable != blank %}
  <!-- Variable has a value -->
{% endif %}
```

### 8. Common Fixes Summary

| Error Type | Quick Fix |
|------------|-----------|
| Decimal digits in range | Use max 1 decimal place or integers |
| Ternary operator | Use {% if %} blocks |
| Complex conditionals | Break into multiple if statements |
| Decimal calculations | Add \| round filter |
| Missing defaults | Always set default values |
| Type mismatches | Ensure correct data types |

## Need More Help?

- [Shopify Liquid Documentation](https://shopify.dev/docs/api/liquid)
- [Theme Inspector Chrome Extension](https://chrome.google.com/webstore/detail/shopify-theme-inspector)
- [Shopify Community Forums](https://community.shopify.com)
