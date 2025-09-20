# Shopify Config Documentation

Configuration files control theme behavior, store settings, and merchant customization options. This documentation covers all config file types, validation patterns, and best practices for theme configuration management.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[settings-schema.md](./settings-schema.md)** | Theme settings configuration | Global settings, merchant customization options |
| **[section-groups.md](./section-groups.md)** | Section group configurations | Header, footer, aside group settings |
| **[blocks-config.md](./blocks-config.md)** | Block-level configurations | App blocks, theme blocks, dynamic blocks |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working configuration files | Complete config examples, validation patterns |

## 🎯 Quick Start

### For Beginners
1. Start with **[settings-schema.md](./settings-schema.md)** to understand theme-wide settings
2. Review **[examples/](./examples/)** for practical implementations
3. Study **[section-groups.md](./section-groups.md)** for advanced configurations

### For Experienced Developers
- Jump to **[blocks-config.md](./blocks-config.md)** for dynamic block patterns
- Browse **[examples/](./examples/)** for production-ready configurations
- Reference specific files for validation rules and schema patterns

## 📋 Config File Types Overview

### Theme Configuration
Core theme behavior and settings:
- **`settings_schema.json`** - Global theme settings (required)
- **`settings_data.json`** - Store-specific setting values (auto-generated)

### Section Group Configuration
Layout area configurations:
- **Header groups** - Navigation, announcements, utility sections
- **Footer groups** - Links, social media, legal sections
- **Aside groups** - Sidebar content, filters, widgets

### Block Configuration
Component-level settings:
- **Static blocks** - Fixed block configurations
- **Dynamic blocks** - Merchant-customizable blocks
- **App blocks** - Third-party app integrations

## 🏗️ Configuration Architecture

### Settings Schema Structure
```json
{
  "name": "Theme Settings",
  "settings": [
    {
      "type": "header",
      "content": "Typography"
    },
    {
      "type": "font_picker",
      "id": "font_heading",
      "label": "Heading font",
      "default": "helvetica_n4"
    },
    {
      "type": "range",
      "id": "font_size_base",
      "label": "Base font size",
      "min": 14,
      "max": 20,
      "step": 1,
      "unit": "px",
      "default": 16
    }
  ]
}
```

### Section Group Configuration
```json
{
  "name": "Header",
  "type": "header",
  "sections": {
    "announcement": {
      "type": "announcement-bar",
      "settings": {
        "text": "Free shipping on orders over $50",
        "show_banner": true
      }
    },
    "header": {
      "type": "header",
      "settings": {
        "logo_width": 150,
        "enable_sticky": true
      }
    }
  }
}
```

### Block Configuration Patterns
```json
{
  "type": "text",
  "name": "Text Block",
  "settings": [
    {
      "type": "richtext",
      "id": "content",
      "label": "Text content",
      "default": "<p>Add your text here</p>"
    },
    {
      "type": "select",
      "id": "text_size",
      "label": "Text size",
      "options": [
        { "value": "small", "label": "Small" },
        { "value": "medium", "label": "Medium" },
        { "value": "large", "label": "Large" }
      ],
      "default": "medium"
    }
  ]
}
```

## 🚀 Configuration Best Practices

### Schema Validation
- **Valid JSON only** - No Liquid syntax in schema
- **Consistent naming** - Use snake_case for IDs
- **Proper data types** - Match setting type to expected value
- **Logical grouping** - Group related settings with headers

### Setting Organization
```json
{
  "settings": [
    {
      "type": "header",
      "content": "Colors"
    },
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary color",
      "default": "#000000"
    },
    {
      "type": "color",
      "id": "color_secondary",
      "label": "Secondary color",
      "default": "#666666"
    },
    {
      "type": "header",
      "content": "Typography"
    },
    {
      "type": "font_picker",
      "id": "font_body",
      "label": "Body font"
    }
  ]
}
```

### Performance Considerations
- **Minimal settings** - Only include necessary customization options
- **Efficient defaults** - Choose sensible default values
- **Conditional logic** - Use Liquid conditionals in templates based on settings
- **Setting validation** - Validate ranges and limits appropriately

## 🎨 Advanced Configuration Patterns

### Conditional Settings Display
```json
{
  "type": "checkbox",
  "id": "enable_custom_colors",
  "label": "Enable custom colors",
  "default": false
},
{
  "type": "color",
  "id": "custom_primary",
  "label": "Custom primary color",
  "default": "#000000",
  "info": "Only used when custom colors are enabled"
}
```

### Dynamic Setting Options
```json
{
  "type": "select",
  "id": "collection_source",
  "label": "Collection to display",
  "options": [
    { "value": "featured", "label": "Featured products" },
    { "value": "new", "label": "New arrivals" },
    { "value": "sale", "label": "Sale items" }
  ],
  "default": "featured"
},
{
  "type": "collection",
  "id": "custom_collection",
  "label": "Custom collection",
  "info": "Used when 'Custom' is selected above"
}
```

### Responsive Configuration
```json
{
  "type": "header",
  "content": "Desktop Layout"
},
{
  "type": "range",
  "id": "columns_desktop",
  "label": "Columns on desktop",
  "min": 2,
  "max": 6,
  "step": 1,
  "default": 4
},
{
  "type": "header",
  "content": "Mobile Layout"
},
{
  "type": "range",
  "id": "columns_mobile",
  "label": "Columns on mobile",
  "min": 1,
  "max": 2,
  "step": 1,
  "default": 1
}
```

## 🔧 Configuration Management Workflow

### 1. Schema Development
- Design settings with merchant needs in mind
- Group related settings logically
- Provide clear labels and helpful info text
- Set appropriate defaults for new installations

### 2. Validation and Testing
- Validate JSON syntax before deployment
- Test all setting combinations
- Verify responsive behavior
- Check accessibility compliance

### 3. Documentation and Training
- Document setting purposes and effects
- Provide clear usage guidelines
- Train merchants on customization options
- Maintain setting compatibility across updates

## 📊 Setting Types Reference

### Basic Input Types
```json
{
  "type": "text",
  "id": "heading_text",
  "label": "Heading",
  "default": "Welcome to our store"
},
{
  "type": "textarea",
  "id": "description",
  "label": "Description",
  "default": "Add your description here"
},
{
  "type": "richtext",
  "id": "content",
  "label": "Rich text content",
  "default": "<p>Add formatted content</p>"
}
```

### Selection Types
```json
{
  "type": "select",
  "id": "layout_style",
  "label": "Layout style",
  "options": [
    { "value": "grid", "label": "Grid" },
    { "value": "list", "label": "List" },
    { "value": "carousel", "label": "Carousel" }
  ],
  "default": "grid"
},
{
  "type": "radio",
  "id": "text_alignment",
  "label": "Text alignment",
  "options": [
    { "value": "left", "label": "Left" },
    { "value": "center", "label": "Center" },
    { "value": "right", "label": "Right" }
  ],
  "default": "left"
}
```

### Resource Types
```json
{
  "type": "product",
  "id": "featured_product",
  "label": "Featured product"
},
{
  "type": "collection",
  "id": "featured_collection",
  "label": "Featured collection"
},
{
  "type": "blog",
  "id": "featured_blog",
  "label": "Featured blog"
},
{
  "type": "page",
  "id": "about_page",
  "label": "About page"
}
```

## 🚨 Common Configuration Pitfalls

### 1. Invalid JSON Syntax
**Problem**: Malformed JSON breaks theme editor
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

**Solution**: Validate JSON syntax
```json
{
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome"
    }
  ]
}
```

### 2. Range Validation Errors
**Problem**: Invalid step configuration
```json
{
  "type": "range",
  "id": "columns",
  "min": 1,
  "max": 12,
  "step": 5 // ❌ (12-1)/5 = 2.2 (must be integer)
}
```

**Solution**: Ensure (max - min) / step ≤ 101
```json
{
  "type": "range",
  "id": "columns",
  "min": 1,
  "max": 12,
  "step": 1 // ✅ (12-1)/1 = 11
}
```

### 3. Missing Required Properties
**Problem**: Settings without required properties
```json
{
  "type": "color",
  "label": "Primary color" // ❌ Missing 'id'
}
```

**Solution**: Include all required properties
```json
{
  "type": "color",
  "id": "color_primary",
  "label": "Primary color",
  "default": "#000000"
}
```

### 4. Inappropriate Setting Types
**Problem**: Using wrong setting type for data
```json
{
  "type": "file",
  "id": "video_upload" // ❌ Use 'video' type for videos
}
```

**Solution**: Use appropriate setting types
```json
{
  "type": "video",
  "id": "video_upload"
}
```

## 🛠️ Development Tools

### JSON Validation
```bash
# Validate settings_schema.json
npx jsonlint settings_schema.json

# Theme Check validation
shopify theme check
```

### Schema Testing
```liquid
<!-- Test setting values in development -->
<div style="background: {{ settings.color_primary }};">
  <h1 style="font-family: {{ settings.font_heading.family }};">
    {{ settings.heading_text | default: 'Default Heading' }}
  </h1>
</div>
```

## 📚 Related Documentation

- **[Theme Architecture](../architecture/theme-overview.md)** - How configs fit into theme structure
- **[Section Schema](../sections/)** - Section-specific configuration patterns
- **[Block Schema](../blocks/)** - Block-level configuration options

---

Configuration files are the foundation of merchant customization in Shopify themes. Proper schema design enables flexible, user-friendly themes while maintaining performance and reliability.