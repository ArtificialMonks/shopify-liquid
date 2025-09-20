# Settings Schema - Theme-Wide Configuration

The settings schema defines global theme customization options that merchants can modify through the theme editor. This guide covers schema structure, setting types, validation rules, and best practices for creating merchant-friendly configurations.

## 🎯 Settings Schema Overview

### Purpose and Function
Settings schema (`config/settings_schema.json`) enables:
- **Global theme customization** - Colors, fonts, layout options
- **Merchant control** - Store-specific branding and preferences
- **Theme editor interface** - Organized, user-friendly settings panels
- **Default value management** - Sensible defaults for new installations

### Schema Structure
```json
{
  "name": "theme_info",
  "theme_name": "Your Theme Name",
  "theme_version": "1.0.0",
  "theme_author": "Your Name",
  "theme_documentation_url": "https://...",
  "theme_support_url": "https://..."
}
```

## 🏗️ Setting Categories and Organization

### Typography Settings
```json
{
  "name": "Typography",
  "settings": [
    {
      "type": "header",
      "content": "Headings"
    },
    {
      "type": "font_picker",
      "id": "font_heading",
      "label": "Heading font",
      "default": "helvetica_n4",
      "info": "Used for all headings (H1-H6)"
    },
    {
      "type": "range",
      "id": "font_heading_scale",
      "label": "Heading size scale",
      "min": 100,
      "max": 150,
      "step": 5,
      "unit": "%",
      "default": 120,
      "info": "Adjusts all heading sizes proportionally"
    },
    {
      "type": "header",
      "content": "Body Text"
    },
    {
      "type": "font_picker",
      "id": "font_body",
      "label": "Body font",
      "default": "helvetica_n4",
      "info": "Used for all body text and navigation"
    },
    {
      "type": "range",
      "id": "font_size_base",
      "label": "Base font size",
      "min": 14,
      "max": 20,
      "step": 1,
      "unit": "px",
      "default": 16,
      "info": "Foundation size for all text scaling"
    }
  ]
}
```

### Color Settings
```json
{
  "name": "Colors",
  "settings": [
    {
      "type": "header",
      "content": "Brand Colors"
    },
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary color",
      "default": "#000000",
      "info": "Used for buttons, links, and brand elements"
    },
    {
      "type": "color",
      "id": "color_secondary",
      "label": "Secondary color",
      "default": "#666666",
      "info": "Used for accents and secondary elements"
    },
    {
      "type": "color",
      "id": "color_accent",
      "label": "Accent color",
      "default": "#ff6b35",
      "info": "Used for highlights and call-to-action elements"
    },
    {
      "type": "header",
      "content": "Background Colors"
    },
    {
      "type": "color",
      "id": "color_background",
      "label": "Background color",
      "default": "#ffffff",
      "info": "Main page background color"
    },
    {
      "type": "color",
      "id": "color_background_secondary",
      "label": "Secondary background",
      "default": "#f8f8f8",
      "info": "Used for sections and cards"
    }
  ]
}
```

### Layout Settings
```json
{
  "name": "Layout",
  "settings": [
    {
      "type": "header",
      "content": "Container"
    },
    {
      "type": "range",
      "id": "container_width",
      "label": "Container width",
      "min": 1000,
      "max": 1400,
      "step": 50,
      "unit": "px",
      "default": 1200,
      "info": "Maximum width for page content"
    },
    {
      "type": "select",
      "id": "container_style",
      "label": "Container style",
      "options": [
        { "value": "boxed", "label": "Boxed" },
        { "value": "full-width", "label": "Full width" },
        { "value": "fluid", "label": "Fluid" }
      ],
      "default": "boxed",
      "info": "How content is contained on the page"
    },
    {
      "type": "header",
      "content": "Spacing"
    },
    {
      "type": "range",
      "id": "spacing_base",
      "label": "Base spacing",
      "min": 8,
      "max": 32,
      "step": 4,
      "unit": "px",
      "default": 16,
      "info": "Foundation spacing used throughout the theme"
    }
  ]
}
```

### Product Settings
```json
{
  "name": "Products",
  "settings": [
    {
      "type": "header",
      "content": "Product Grid"
    },
    {
      "type": "range",
      "id": "products_per_page",
      "label": "Products per page",
      "min": 12,
      "max": 48,
      "step": 4,
      "default": 24,
      "info": "Number of products shown on collection pages"
    },
    {
      "type": "range",
      "id": "product_grid_columns_desktop",
      "label": "Desktop columns",
      "min": 2,
      "max": 5,
      "step": 1,
      "default": 4,
      "info": "Number of product columns on desktop"
    },
    {
      "type": "range",
      "id": "product_grid_columns_mobile",
      "label": "Mobile columns",
      "min": 1,
      "max": 2,
      "step": 1,
      "default": 2,
      "info": "Number of product columns on mobile"
    },
    {
      "type": "header",
      "content": "Product Images"
    },
    {
      "type": "select",
      "id": "product_image_ratio",
      "label": "Image aspect ratio",
      "options": [
        { "value": "natural", "label": "Natural" },
        { "value": "square", "label": "Square (1:1)" },
        { "value": "portrait", "label": "Portrait (3:4)" },
        { "value": "landscape", "label": "Landscape (4:3)" }
      ],
      "default": "natural",
      "info": "How product images are cropped"
    },
    {
      "type": "checkbox",
      "id": "product_image_hover",
      "label": "Show second image on hover",
      "default": true,
      "info": "Display second product image when hovering"
    }
  ]
}
```

## 🎨 Advanced Setting Patterns

### Feature Toggles
```json
{
  "name": "Features",
  "settings": [
    {
      "type": "header",
      "content": "Performance Features"
    },
    {
      "type": "checkbox",
      "id": "enable_lazy_loading",
      "label": "Enable lazy loading",
      "default": true,
      "info": "Improves page load speed by loading images on demand"
    },
    {
      "type": "checkbox",
      "id": "enable_preconnect",
      "label": "Enable resource preconnecting",
      "default": true,
      "info": "Preconnects to external resources for faster loading"
    },
    {
      "type": "header",
      "content": "User Experience Features"
    },
    {
      "type": "checkbox",
      "id": "enable_quick_add",
      "label": "Enable quick add to cart",
      "default": true,
      "info": "Allows adding products to cart from collection pages"
    },
    {
      "type": "checkbox",
      "id": "enable_cart_drawer",
      "label": "Enable cart drawer",
      "default": true,
      "info": "Shows cart in slide-out drawer instead of page"
    }
  ]
}
```

### Social Media Settings
```json
{
  "name": "Social Media",
  "settings": [
    {
      "type": "header",
      "content": "Social Links"
    },
    {
      "type": "url",
      "id": "social_facebook",
      "label": "Facebook URL",
      "info": "https://facebook.com/yourpage"
    },
    {
      "type": "url",
      "id": "social_instagram",
      "label": "Instagram URL",
      "info": "https://instagram.com/youraccount"
    },
    {
      "type": "url",
      "id": "social_twitter",
      "label": "Twitter URL",
      "info": "https://twitter.com/youraccount"
    },
    {
      "type": "header",
      "content": "Social Sharing"
    },
    {
      "type": "checkbox",
      "id": "enable_social_sharing",
      "label": "Enable social sharing",
      "default": true,
      "info": "Show social sharing buttons on product pages"
    },
    {
      "type": "image_picker",
      "id": "social_image",
      "label": "Default social image",
      "info": "Used when pages don't have specific social images"
    }
  ]
}
```

### SEO Settings
```json
{
  "name": "SEO",
  "settings": [
    {
      "type": "header",
      "content": "Meta Information"
    },
    {
      "type": "text",
      "id": "seo_title",
      "label": "Default SEO title",
      "info": "Appears in search results when page titles aren't set"
    },
    {
      "type": "textarea",
      "id": "seo_description",
      "label": "Default meta description",
      "info": "Appears in search results when page descriptions aren't set"
    },
    {
      "type": "header",
      "content": "Schema Markup"
    },
    {
      "type": "checkbox",
      "id": "enable_schema_org",
      "label": "Enable schema.org markup",
      "default": true,
      "info": "Adds structured data for better search results"
    },
    {
      "type": "select",
      "id": "schema_org_type",
      "label": "Organization type",
      "options": [
        { "value": "Organization", "label": "Organization" },
        { "value": "LocalBusiness", "label": "Local Business" },
        { "value": "Store", "label": "Store" }
      ],
      "default": "Organization"
    }
  ]
}
```

## 🔧 Setting Types Reference

### Input Settings
```json
{
  "type": "text",
  "id": "store_tagline",
  "label": "Store tagline",
  "default": "Welcome to our store",
  "placeholder": "Enter your tagline here"
}
```

```json
{
  "type": "textarea",
  "id": "footer_text",
  "label": "Footer text",
  "default": "© 2024 Your Store Name",
  "info": "Supports line breaks"
}
```

```json
{
  "type": "richtext",
  "id": "about_content",
  "label": "About us content",
  "default": "<p>Tell your story here</p>",
  "info": "Supports HTML formatting"
}
```

### Selection Settings
```json
{
  "type": "select",
  "id": "header_style",
  "label": "Header style",
  "options": [
    { "value": "minimal", "label": "Minimal" },
    { "value": "classic", "label": "Classic" },
    { "value": "modern", "label": "Modern" }
  ],
  "default": "classic"
}
```

```json
{
  "type": "radio",
  "id": "button_style",
  "label": "Button style",
  "options": [
    { "value": "rounded", "label": "Rounded" },
    { "value": "sharp", "label": "Sharp corners" },
    { "value": "pill", "label": "Pill shaped" }
  ],
  "default": "rounded"
}
```

### Resource Settings
```json
{
  "type": "image_picker",
  "id": "logo",
  "label": "Logo image",
  "info": "Recommended size: 200x60px"
}
```

```json
{
  "type": "video",
  "id": "hero_video",
  "label": "Hero video",
  "info": "MP4 format recommended"
}
```

```json
{
  "type": "collection",
  "id": "featured_collection",
  "label": "Featured collection"
}
```

### Measurement Settings
```json
{
  "type": "range",
  "id": "logo_width",
  "label": "Logo width",
  "min": 50,
  "max": 300,
  "step": 10,
  "unit": "px",
  "default": 150
}
```

```json
{
  "type": "color",
  "id": "button_color",
  "label": "Button color",
  "default": "#000000"
}
```

## 📊 Schema Validation Rules

### Required Properties
Every setting must include:
- **`type`** - Valid setting type
- **`id`** - Unique identifier (snake_case)
- **`label`** - User-friendly label

### Range Validation
```json
{
  "type": "range",
  "id": "valid_range",
  "min": 1,
  "max": 100,
  "step": 1
  // Valid: (100-1)/1 = 99 ≤ 101
}
```

### String Length Limits
- **Text inputs**: 255 characters maximum
- **Textarea**: 2048 characters maximum
- **URLs**: Valid URL format required

### File Type Restrictions
- **Images**: JPG, PNG, GIF, SVG, WebP
- **Videos**: MP4, WebM, MOV
- **Fonts**: WOFF, WOFF2, TTF, OTF

## 🚀 Performance Considerations

### Efficient Default Values
```json
{
  "type": "image_picker",
  "id": "default_product_image",
  "label": "Default product image",
  "info": "Used when products don't have images"
}
```

### Conditional Loading
```liquid
<!-- Use settings conditionally in templates -->
{% if settings.enable_animations %}
  {{ 'animations.css' | asset_url | stylesheet_tag }}
{% endif %}

{% if settings.enable_reviews %}
  {% section 'product-reviews' %}
{% endif %}
```

### Setting Impact Assessment
```json
{
  "type": "checkbox",
  "id": "enable_cart_ajax",
  "label": "Enable AJAX cart",
  "default": true,
  "info": "⚡ Improves performance by updating cart without page reload"
}
```

## 🚨 Common Schema Pitfalls

### 1. Invalid JSON Structure
**Problem**: Syntax errors break theme editor
```json
{
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome", // ❌ Trailing comma
    }
  ]
}
```

### 2. Range Step Violations
**Problem**: Exceeds 101 steps limit
```json
{
  "type": "range",
  "id": "invalid_range",
  "min": 0,
  "max": 1000,
  "step": 1
  // ❌ (1000-0)/1 = 1000 > 101
}
```

### 3. Missing Required Properties
**Problem**: Settings without proper structure
```json
{
  "type": "color",
  "label": "Primary color"
  // ❌ Missing required 'id' property
}
```

### 4. Inappropriate Setting Types
**Problem**: Wrong type for data
```json
{
  "type": "text",
  "id": "enable_feature"
  // ❌ Should use 'checkbox' for boolean values
}
```

## 🛠️ Development Workflow

### Schema Development Process
1. **Plan setting categories** - Group related settings logically
2. **Design merchant experience** - Consider ease of use
3. **Validate schema structure** - Check JSON syntax and rules
4. **Test with real data** - Verify setting behavior in templates
5. **Document setting purposes** - Provide clear info text

### Testing and Validation
```bash
# Validate JSON syntax
npx jsonlint config/settings_schema.json

# Run Theme Check
shopify theme check

# Test in development
shopify theme dev
```

### Schema Maintenance
- **Version control** - Track schema changes
- **Backward compatibility** - Handle setting migrations
- **Performance monitoring** - Monitor setting impact
- **Merchant feedback** - Iterate based on user needs

---

Settings schema is the foundation of theme customization. Well-designed schemas balance merchant flexibility with performance and usability, creating themes that are both powerful and approachable.