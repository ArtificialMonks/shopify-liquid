# Sections & Schema

Master Shopify section creation and schema configuration. Learn how to build flexible, merchant-friendly sections that integrate seamlessly with the theme editor.

## Section Architecture

### The Three Components

Every Shopify section consists of:

1. **Template Logic** - HTML/Liquid that renders content
2. **Styling** - CSS that controls appearance
3. **Schema** - JSON that defines settings and behavior

```liquid
<!-- 1. Template Logic -->
<section class="custom-section">
  {% if section.settings.title != blank %}
    <h2>{{ section.settings.title | escape }}</h2>
  {% endif %}
</section>

<!-- 2. Styling -->
<style>
  .custom-section {
    padding: {{ section.settings.padding }}px;
    background: {{ section.settings.bg_color }};
  }
</style>

<!-- 3. Schema -->
{% schema %}
{
  "name": "Custom Section",
  "settings": [
    {"type": "text", "id": "title", "label": "Section Title"},
    {"type": "color", "id": "bg_color", "label": "Background Color"},
    {"type": "range", "id": "padding", "min": 0, "max": 100, "default": 20}
  ]
}
{% endschema %}
```

## Schema Fundamentals

### Basic Schema Structure

```json
{
  "name": "Section Name",
  "tag": "section",
  "class": "css-class-name",
  "limit": 1,
  "settings": [],
  "blocks": [],
  "presets": [],
  "enabled_on": {},
  "disabled_on": {}
}
```

### Setting Types Reference

#### Text Inputs
```json
{
  "type": "text",
  "id": "heading",
  "label": "Heading",
  "default": "Default text",
  "info": "Help text for merchants",
  "placeholder": "Enter text here"
}
```

```json
{
  "type": "textarea",
  "id": "description",
  "label": "Description",
  "default": "Default description"
}
```

```json
{
  "type": "richtext",
  "id": "content",
  "label": "Rich Text Content",
  "default": "<p>Default rich text content</p>"
}
```

#### Selection Inputs
```json
{
  "type": "select",
  "id": "layout",
  "label": "Layout Style",
  "options": [
    {"value": "grid", "label": "Grid Layout"},
    {"value": "list", "label": "List Layout"},
    {"value": "carousel", "label": "Carousel Layout"}
  ],
  "default": "grid"
}
```

```json
{
  "type": "radio",
  "id": "alignment",
  "label": "Text Alignment",
  "options": [
    {"value": "left", "label": "Left"},
    {"value": "center", "label": "Center"},
    {"value": "right", "label": "Right"}
  ],
  "default": "center"
}
```

#### Boolean Inputs
```json
{
  "type": "checkbox",
  "id": "show_border",
  "label": "Show border",
  "default": true
}
```

#### Numeric Inputs
```json
{
  "type": "range",
  "id": "columns",
  "label": "Number of columns",
  "min": 1,
  "max": 6,
  "step": 1,
  "default": 3,
  "unit": "columns"
}
```

```json
{
  "type": "number",
  "id": "item_count",
  "label": "Items to show",
  "default": 6
}
```

#### Visual Inputs
```json
{
  "type": "color",
  "id": "text_color",
  "label": "Text Color",
  "default": "#333333"
}
```

```json
{
  "type": "color_background",
  "id": "bg_gradient",
  "label": "Background Gradient"
}
```

```json
{
  "type": "image_picker",
  "id": "background_image",
  "label": "Background Image"
}
```

#### Link Inputs
```json
{
  "type": "url",
  "id": "button_link",
  "label": "Button Link"
}
```

```json
{
  "type": "collection",
  "id": "featured_collection",
  "label": "Featured Collection"
}
```

```json
{
  "type": "product",
  "id": "featured_product",
  "label": "Featured Product"
}
```

#### Organization
```json
{
  "type": "header",
  "content": "Layout Settings"
}
```

```json
{
  "type": "paragraph",
  "content": "This section displays featured products in a grid layout."
}
```

## Section Placement Control

### Enabled On Specific Templates
```json
{
  "enabled_on": {
    "templates": ["index", "collection", "product"]
  }
}
```

### Disabled On Specific Areas
```json
{
  "disabled_on": {
    "groups": ["header", "footer"],
    "templates": ["cart", "search"]
  }
}
```

### Template-Specific Sections
```json
{
  "enabled_on": {
    "templates": ["product"]
  },
  "disabled_on": {
    "groups": ["*"]
  }
}
```

## Blocks: Repeatable Content

### Basic Block Configuration
```json
{
  "blocks": [
    {
      "type": "testimonial",
      "name": "Testimonial",
      "settings": [
        {"type": "textarea", "id": "quote", "label": "Quote"},
        {"type": "text", "id": "author", "label": "Author"},
        {"type": "image_picker", "id": "photo", "label": "Author Photo"}
      ]
    }
  ],
  "max_blocks": 12
}
```

### Handling Blocks in Template
```liquid
{% if section.blocks.size > 0 %}
  <div class="testimonials-grid">
    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'testimonial' %}
          <div class="testimonial" {{ block.shopify_attributes }}>
            <blockquote>{{ block.settings.quote | escape }}</blockquote>
            <cite>{{ block.settings.author | escape }}</cite>
          </div>
      {% endcase %}
    {% endfor %}
  </div>
{% endif %}
```

### Multiple Block Types
```json
{
  "blocks": [
    {
      "type": "image",
      "name": "Image",
      "settings": [
        {"type": "image_picker", "id": "image", "label": "Image"},
        {"type": "text", "id": "caption", "label": "Caption"}
      ]
    },
    {
      "type": "text",
      "name": "Text Block",
      "settings": [
        {"type": "richtext", "id": "content", "label": "Content"}
      ]
    },
    {
      "type": "video",
      "name": "Video",
      "settings": [
        {"type": "url", "id": "video_url", "label": "Video URL"}
      ]
    }
  ]
}
```

## Presets: Default Configurations

### Basic Preset
```json
{
  "presets": [
    {
      "name": "Featured Products",
      "category": "Product"
    }
  ]
}
```

### Preset with Default Settings
```json
{
  "presets": [
    {
      "name": "Hero Banner",
      "category": "Image",
      "settings": {
        "heading": "Welcome to our store",
        "subtext": "Discover amazing products",
        "bg_color": "#f8f9fa",
        "text_align": "center"
      }
    }
  ]
}
```

### Preset with Default Blocks
```json
{
  "presets": [
    {
      "name": "Testimonials",
      "category": "Text",
      "blocks": [
        {
          "type": "testimonial",
          "settings": {
            "quote": "Amazing service and quality!",
            "author": "Sarah Johnson"
          }
        },
        {
          "type": "testimonial",
          "settings": {
            "quote": "Fast shipping and great products.",
            "author": "Mike Chen"
          }
        }
      ]
    }
  ]
}
```

## Advanced Schema Patterns

### Conditional Settings
```liquid
{% if section.settings.layout == 'custom' %}
  {% assign custom_spacing = section.settings.custom_spacing %}
{% else %}
  {% assign custom_spacing = 20 %}
{% endif %}
```

```json
{
  "settings": [
    {
      "type": "select",
      "id": "layout",
      "label": "Layout",
      "options": [
        {"value": "standard", "label": "Standard"},
        {"value": "custom", "label": "Custom"}
      ]
    },
    {
      "type": "range",
      "id": "custom_spacing",
      "label": "Custom Spacing",
      "min": 0,
      "max": 100,
      "default": 20,
      "info": "Only applies when Custom layout is selected"
    }
  ]
}
```

### Grouped Settings
```json
{
  "settings": [
    {
      "type": "header",
      "content": "Content Settings"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "richtext",
      "id": "content",
      "label": "Content"
    },
    {
      "type": "header",
      "content": "Layout Settings"
    },
    {
      "type": "select",
      "id": "columns",
      "label": "Columns"
    },
    {
      "type": "range",
      "id": "spacing",
      "label": "Spacing"
    },
    {
      "type": "header",
      "content": "Style Settings"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color"
    }
  ]
}
```

### Responsive Settings
```json
{
  "settings": [
    {
      "type": "header",
      "content": "Desktop Settings"
    },
    {
      "type": "range",
      "id": "columns_desktop",
      "label": "Desktop Columns",
      "min": 1,
      "max": 6,
      "default": 4
    },
    {
      "type": "range",
      "id": "spacing_desktop",
      "label": "Desktop Spacing",
      "min": 0,
      "max": 80,
      "default": 30
    },
    {
      "type": "header",
      "content": "Mobile Settings"
    },
    {
      "type": "range",
      "id": "columns_mobile",
      "label": "Mobile Columns",
      "min": 1,
      "max": 3,
      "default": 1
    },
    {
      "type": "range",
      "id": "spacing_mobile",
      "label": "Mobile Spacing",
      "min": 0,
      "max": 40,
      "default": 20
    }
  ]
}
```

## Real-World Examples

### Product Grid Section
```liquid
<section class="product-grid">
  <div class="container">
    {% if section.settings.heading != blank %}
      <h2 class="section-heading">{{ section.settings.heading | escape }}</h2>
    {% endif %}

    {% assign collection = collections[section.settings.collection] %}
    {% if collection.products.size > 0 %}
      <div class="product-grid__items" style="grid-template-columns: repeat({{ section.settings.columns }}, 1fr);">
        {% for product in collection.products limit: section.settings.products_to_show %}
          <div class="product-card">
            <a href="{{ product.url }}">
              {% if product.featured_image %}
                <img src="{{ product.featured_image | image_url: width: 400 }}"
                     alt="{{ product.title | escape }}"
                     loading="lazy">
              {% endif %}
              <h3>{{ product.title | escape }}</h3>
              <p class="price">{{ product.price | money }}</p>
            </a>
          </div>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</section>

{% schema %}
{
  "name": "Product Grid",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Section Heading",
      "default": "Featured Products"
    },
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "label": "Products to show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 8
    },
    {
      "type": "range",
      "id": "columns",
      "label": "Columns",
      "min": 2,
      "max": 5,
      "step": 1,
      "default": 4
    }
  ],
  "presets": [
    {
      "name": "Product Grid",
      "category": "Product"
    }
  ]
}
{% endschema %}
```

### Image with Text Overlay
```liquid
<section class="image-overlay"
         style="background-image: url('{{ section.settings.bg_image | image_url: width: 1200 }}');">
  <div class="image-overlay__content">
    {% if section.settings.heading != blank %}
      <h2 class="image-overlay__heading">{{ section.settings.heading | escape }}</h2>
    {% endif %}

    {% if section.settings.text != blank %}
      <div class="image-overlay__text">{{ section.settings.text }}</div>
    {% endif %}

    {% if section.settings.button_text != blank and section.settings.button_url != blank %}
      <a href="{{ section.settings.button_url }}" class="image-overlay__button">
        {{ section.settings.button_text | escape }}
      </a>
    {% endif %}
  </div>
</section>

{% schema %}
{
  "name": "Image with Text Overlay",
  "settings": [
    {
      "type": "header",
      "content": "Image"
    },
    {
      "type": "image_picker",
      "id": "bg_image",
      "label": "Background Image"
    },
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "richtext",
      "id": "text",
      "label": "Text"
    },
    {
      "type": "text",
      "id": "button_text",
      "label": "Button Text"
    },
    {
      "type": "url",
      "id": "button_url",
      "label": "Button Link"
    },
    {
      "type": "header",
      "content": "Style"
    },
    {
      "type": "select",
      "id": "text_position",
      "label": "Text Position",
      "options": [
        {"value": "center", "label": "Center"},
        {"value": "left", "label": "Left"},
        {"value": "right", "label": "Right"}
      ],
      "default": "center"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "default": "#ffffff"
    },
    {
      "type": "color",
      "id": "overlay_color",
      "label": "Overlay Color",
      "default": "#000000"
    },
    {
      "type": "range",
      "id": "overlay_opacity",
      "label": "Overlay Opacity",
      "min": 0,
      "max": 100,
      "step": 10,
      "unit": "%",
      "default": 30
    }
  ],
  "presets": [
    {
      "name": "Image with Text Overlay",
      "category": "Image"
    }
  ]
}
{% endschema %}
```

## Best Practices

### Schema Design
✅ **Use clear, descriptive labels**
✅ **Provide helpful info text for complex settings**
✅ **Set sensible defaults for immediate usability**
✅ **Group related settings with headers**
✅ **Keep max_blocks reasonable (≤50)**
✅ **Use appropriate input types for data**

### Template Implementation
✅ **Always escape user input** with `| escape`
✅ **Guard optional content** with `{% if setting != blank %}`
✅ **Use semantic HTML** elements
✅ **Include `{{ block.shopify_attributes }}`** on block elements
✅ **Provide fallbacks** for missing content
✅ **Optimize images** with appropriate sizing

### Performance Considerations
✅ **Minimize Liquid logic** complexity
✅ **Use efficient loops** and avoid nested iterations
✅ **Optimize image requests** with `image_url` parameters
✅ **Keep CSS scoped** to avoid conflicts
✅ **Test with many blocks** to ensure performance

## Common Pitfalls

❌ **Invalid JSON in schema** - Breaks theme editor
❌ **Missing escape filters** - Security vulnerability
❌ **No content guards** - Displays empty elements
❌ **Hardcoded values** - Reduces flexibility
❌ **Missing shopify_attributes** - Breaks theme editor functionality
❌ **Complex nested logic** - Hard to maintain

## Next Steps

- **[Blocks & CSS Scoping](./04-blocks-and-css-scoping.md)** - Advanced component patterns
- **[Performance & Accessibility](./05-performance-and-accessibility.md)** - Optimization strategies
- **[Code Library](./code-library/sections/)** - Production-ready examples
- **[Troubleshooting](./06-troubleshooting.md)** - Common issues and solutions