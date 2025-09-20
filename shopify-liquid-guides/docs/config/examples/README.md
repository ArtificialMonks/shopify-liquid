# Configuration Examples

This directory contains practical examples of Shopify theme configuration files, including settings schemas, section groups, and block configurations. Each example demonstrates best practices for merchant customization and theme flexibility.

## 📁 Available Examples

### Settings Schema Examples
- **[complete-settings-schema.json](./complete-settings-schema.json)** - Comprehensive theme settings with all major categories
- **[minimal-settings-schema.json](./minimal-settings-schema.json)** - Essential settings for lightweight themes
- **[performance-focused-settings.json](./performance-focused-settings.json)** - Settings optimized for Core Web Vitals

### Section Group Examples
- **[header-group.json](./header-group.json)** - Complete header configuration with announcement, navigation, and search
- **[footer-group.json](./footer-group.json)** - Comprehensive footer with links, newsletter, and social media
- **[sidebar-group.json](./sidebar-group.json)** - Sidebar configuration for collection and product pages

### Block Configuration Examples
- **[common-blocks.json](./common-blocks.json)** - Essential block types (text, image, button, video)
- **[ecommerce-blocks.json](./ecommerce-blocks.json)** - E-commerce specific blocks (product, collection, testimonial)
- **[app-integration-blocks.json](./app-integration-blocks.json)** - App block patterns and integration examples

### Validation Examples
- **[schema-validation-tests.json](./schema-validation-tests.json)** - Common validation scenarios and solutions
- **[performance-optimized-config.json](./performance-optimized-config.json)** - Configuration patterns for optimal performance

## 🎯 Usage Guidelines

### Implementation Steps
1. **Choose appropriate example** - Select based on your theme's needs
2. **Copy and customize** - Adapt settings, IDs, and labels to your theme
3. **Validate configuration** - Check JSON syntax and Shopify requirements
4. **Test thoroughly** - Verify functionality across all templates

### Customization Tips
- **Update IDs and labels** - Make them specific to your theme
- **Adjust default values** - Set sensible defaults for your target audience
- **Add info text** - Provide clear guidance for merchants
- **Group logically** - Organize settings for easy navigation

### Performance Considerations
- **Limit setting complexity** - Avoid excessive nesting or too many options
- **Optimize defaults** - Choose performance-friendly default values
- **Include performance toggles** - Allow merchants to optimize for speed
- **Test setting combinations** - Verify all combinations work properly

## 📊 Configuration Best Practices

### Schema Organization
```json
{
  "name": "Theme Category",
  "settings": [
    {
      "type": "header",
      "content": "Section Title"
    },
    {
      "type": "paragraph",
      "content": "Brief explanation of these settings"
    },
    // Related settings grouped together
  ]
}
```

### Setting Design Principles
- **Intuitive labels** - Use clear, merchant-friendly language
- **Helpful info text** - Explain setting purpose and impact
- **Logical defaults** - Choose sensible starting values
- **Progressive disclosure** - Show advanced options when needed

### Validation Patterns
- **Range limits** - Ensure (max - min) / step ≤ 101
- **Required properties** - Include type, id, label for all settings
- **Valid JSON** - No trailing commas or syntax errors
- **Appropriate types** - Match setting type to expected data

## 🔧 Integration Examples

### Theme Settings Integration
```liquid
<!-- Using settings in templates -->
<div style="
  --color-primary: {{ settings.color_primary }};
  --font-heading: {{ settings.font_heading.family }};
  --container-width: {{ settings.container_width }}px;
">
  <!-- Theme content -->
</div>
```

### Section Group Integration
```liquid
<!-- Rendering section groups -->
{% sections 'header' %}

<main>
  {{ content_for_layout }}
</main>

{% sections 'footer' %}
```

### Block Configuration Integration
```liquid
<!-- Section with configurable blocks -->
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'text' %}
      {% render 'block-text', block: block %}
    {% when 'image' %}
      {% render 'block-image', block: block %}
    {% when '@app' %}
      {% render block %}
  {% endcase %}
{% endfor %}
```

## 🚨 Common Configuration Issues

### Validation Errors
- **Invalid JSON syntax** - Use validators to check structure
- **Missing required properties** - Ensure all settings have type, id, label
- **Range step violations** - Check that step divisions don't exceed 101
- **Invalid setting types** - Use correct types for expected data

### Performance Issues
- **Too many settings** - Limit settings to essential customization options
- **Complex default values** - Choose simple, fast-loading defaults
- **Heavy feature toggles** - Consider performance impact of optional features

### User Experience Problems
- **Unclear labels** - Use merchant-friendly language
- **Missing info text** - Explain setting purpose and effects
- **Poor organization** - Group related settings logically
- **Overwhelming options** - Prioritize essential settings

## 📚 Related Documentation

- **[Settings Schema Guide](../settings-schema.md)** - Complete settings schema documentation
- **[Section Groups Guide](../section-groups.md)** - Section group configuration patterns
- **[Block Configuration Guide](../blocks-config.md)** - Block schema and implementation
- **[Theme Architecture](../../architecture/)** - How configuration fits into theme structure

---

These configuration examples provide tested, production-ready patterns for creating flexible, merchant-friendly Shopify themes with optimal performance and user experience.