# Shopify Liquid Sections - Complete Official Documentation

## 🎯 What Are Shopify Sections?

Sections are **modular content areas** that merchants can add, remove, reorder, and customize through the theme editor. They're the building blocks of modern Shopify themes and are essential for Online Store 2.0 themes.

## 📁 File Structure

```
theme/
├── sections/           ← Sections go here
│   ├── header.liquid
│   ├── hero.liquid
│   ├── product-grid.liquid
│   └── footer.liquid
├── templates/
│   └── index.json     ← References sections
└── ...
```

## 🏗️ Section Architecture

### Basic Section Structure
```liquid
<!-- sections/hero.liquid -->
<section class="hero-section">
  <div class="container">
    {% if section.settings.heading != blank %}
      <h1>{{ section.settings.heading | escape }}</h1>
    {% endif %}

    {% if section.settings.text != blank %}
      <p>{{ section.settings.text | escape }}</p>
    {% endif %}

    {% if section.blocks.size > 0 %}
      <div class="hero-blocks">
        {% for block in section.blocks %}
          {% case block.type %}
            {% when 'button' %}
              <a href="{{ block.settings.url }}" class="btn">
                {{ block.settings.label | escape }}
              </a>
            {% when 'text' %}
              <p>{{ block.settings.content | escape }}</p>
          {% endcase %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
</section>

{% schema %}
{
  "name": "Hero Section",
  "tag": "section",
  "class": "hero",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome to our store"
    },
    {
      "type": "textarea",
      "id": "text",
      "label": "Text"
    }
  ],
  "blocks": [
    {
      "type": "button",
      "name": "Button",
      "settings": [
        {
          "type": "text",
          "id": "label",
          "label": "Button label",
          "default": "Click me"
        },
        {
          "type": "url",
          "id": "url",
          "label": "Button URL"
        }
      ]
    },
    {
      "type": "text",
      "name": "Text Block",
      "settings": [
        {
          "type": "richtext",
          "id": "content",
          "label": "Content"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Hero Section",
      "settings": {
        "heading": "Hero Title"
      },
      "blocks": [
        {
          "type": "button",
          "settings": {
            "label": "Shop Now",
            "url": "/collections/all"
          }
        }
      ]
    }
  ]
}
{% endschema %}
```

## 📋 Section Schema

### Complete Schema Structure
```json
{
  "name": "Section Name",
  "tag": "section",
  "class": "custom-class",
  "limit": 1,
  "settings": [],
  "blocks": [],
  "max_blocks": 50,
  "presets": [],
  "default": {},
  "locales": {},
  "enabled_on": {},
  "disabled_on": {}
}
```

### Schema Attributes Explained

#### **`name`** (Required)
Display name in theme editor
```json
{"name": "Product Grid"}
```

#### **`tag`** (Optional)
HTML wrapper element
```json
{"tag": "section"}  // Options: section, article, aside, div, footer, header
```

#### **`class`** (Optional)
CSS class for wrapper element
```json
{"class": "product-grid-section"}
```

#### **`limit`** (Optional)
Maximum instances per template
```json
{"limit": 1}  // Only values: 1 or 2
```

#### **`settings`** (Optional)
Section-level configuration options
```json
{
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Section Heading"
    }
  ]
}
```

#### **`blocks`** (Optional)
Block types this section can contain
```json
{
  "blocks": [
    {"type": "@theme"},     // All theme blocks
    {"type": "@app"},       // All app blocks
    {"type": "custom"},     // Specific section block
    {
      "type": "product",
      "name": "Product",
      "settings": []
    }
  ]
}
```

#### **`max_blocks`** (Optional)
Maximum blocks per section (default: 50)
```json
{"max_blocks": 20}
```

#### **`presets`** (Optional)
Pre-configured section variations
```json
{
  "presets": [
    {
      "name": "Default Grid",
      "settings": {
        "columns": 3
      },
      "blocks": [
        {"type": "product"}
      ]
    }
  ]
}
```

#### **`default`** (Optional)
Default configuration for static sections
```json
{
  "default": {
    "settings": {
      "show_vendor": true
    }
  }
}
```

#### **`enabled_on`** / **`disabled_on`** (Optional)
Template/group restrictions
```json
{
  "enabled_on": {
    "templates": ["product", "collection"],
    "groups": ["header", "footer"]
  }
}
```

## 🔄 Section Types

### 1. **Dynamic Sections** (JSON Templates)
Can be added, removed, and reordered by merchants
```liquid
<!-- Added via JSON templates -->
{
  "sections": {
    "hero": {
      "type": "hero-banner",
      "settings": {
        "heading": "Welcome"
      }
    }
  },
  "order": ["hero", "featured-products"]
}
```

### 2. **Static Sections** (Liquid Templates)
Included directly in Liquid files
```liquid
<!-- In templates/product.liquid -->
{% section 'product-info' %}
{% section 'related-products' %}
```

## 🎨 Working with Blocks in Sections

### Section-Defined Blocks
```liquid
<!-- Defined in section schema -->
{% schema %}
{
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        {
          "type": "text",
          "id": "title",
          "label": "Feature Title"
        }
      ]
    }
  ]
}
{% endschema %}

<!-- Rendered in section template -->
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'feature' %}
      <div class="feature" {{ block.shopify_attributes }}>
        <h3>{{ block.settings.title | escape }}</h3>
      </div>
  {% endcase %}
{% endfor %}
```

### Theme Block Support
```liquid
<!-- Accept all theme blocks -->
{% schema %}
{
  "blocks": [
    {"type": "@theme"},
    {"type": "@app"}
  ]
}
{% endschema %}

<!-- Render theme blocks -->
<div class="section-blocks">
  {% content_for 'blocks' %}
</div>
```

## 🔧 Liquid Objects in Sections

### Section Object
```liquid
{{ section.id }}              <!-- Unique section ID -->
{{ section.settings.title }}  <!-- Section setting values -->
{{ section.blocks.size }}     <!-- Number of blocks -->
{{ section.location }}         <!-- template or section_group -->
```

### Block Object (when looping)
```liquid
{% for block in section.blocks %}
  {{ block.id }}              <!-- Unique block ID -->
  {{ block.type }}            <!-- Block type -->
  {{ block.settings.title }}  <!-- Block settings -->
  {{ block.shopify_attributes }} <!-- Theme editor attributes -->
{% endfor %}
```

## 📱 Theme Editor Integration

### JavaScript Events
```javascript
// Section loaded/reloaded
document.addEventListener('shopify:section:load', function(event) {
  const sectionId = event.detail.sectionId;
  // Re-initialize JavaScript for this section
});

// Section unloaded
document.addEventListener('shopify:section:unload', function(event) {
  // Clean up JavaScript for this section
});

// Block selected
document.addEventListener('shopify:block:select', function(event) {
  const blockId = event.detail.blockId;
  // Handle block selection
});
```

### Required Attributes
```liquid
<!-- For blocks in sections -->
<div {{ block.shopify_attributes }}>
  <!-- Block content -->
</div>
```

## 🎯 Section Best Practices

### 1. **Design for Flexibility**
```liquid
<!-- Good: Flexible layout -->
<section class="content-section">
  {% if section.settings.heading != blank %}
    <h2>{{ section.settings.heading | escape }}</h2>
  {% endif %}

  {% if section.blocks.size > 0 %}
    <div class="content-grid" style="--columns: {{ section.settings.columns }}">
      {% for block in section.blocks %}
        <!-- Render blocks -->
      {% endfor %}
    </div>
  {% endif %}
</section>
```

### 2. **Handle Empty States**
```liquid
{% if section.blocks.size > 0 %}
  <!-- Content with blocks -->
{% else %}
  <div class="empty-state">
    <p>Add blocks to customize this section</p>
  </div>
{% endif %}
```

### 3. **Responsive Design**
```json
{
  "settings": [
    {
      "type": "range",
      "id": "desktop_columns",
      "label": "Desktop Columns",
      "min": 1,
      "max": 4,
      "default": 3
    },
    {
      "type": "range",
      "id": "mobile_columns",
      "label": "Mobile Columns",
      "min": 1,
      "max": 2,
      "default": 1
    }
  ]
}
```

### 4. **Performance Optimization**
```liquid
<!-- Lazy load images -->
{% if section.settings.image %}
  <img
    src="{{ section.settings.image | image_url: width: 800 }}"
    srcset="{{ section.settings.image | image_url: width: 400 }} 400w,
            {{ section.settings.image | image_url: width: 800 }} 800w"
    sizes="(min-width: 750px) 50vw, 100vw"
    loading="lazy"
    alt="{{ section.settings.image.alt | escape }}"
  >
{% endif %}
```

## 🚀 Advanced Section Features

### 1. **Conditional Rendering**
```liquid
{% if template.name == 'product' %}
  <!-- Product-specific content -->
{% elsif template.name == 'collection' %}
  <!-- Collection-specific content -->
{% endif %}
```

### 2. **Dynamic Data Sources**
```liquid
{% case section.settings.data_source %}
  {% when 'featured_products' %}
    {% assign products = collections.featured.products %}
  {% when 'best_sellers' %}
    {% assign products = collections.best-sellers.products %}
{% endcase %}

{% for product in products limit: section.settings.limit %}
  <!-- Render product -->
{% endfor %}
```

### 3. **Section Groups Integration**
```liquid
<!-- Used in header/footer section groups -->
{% schema %}
{
  "name": "Navigation",
  "enabled_on": {
    "groups": ["header"]
  }
}
{% endschema %}
```

## 📊 Section vs Block vs App Block Comparison

| Feature | Sections | Section Blocks | Theme Blocks | App Blocks |
|---------|----------|----------------|-------------|------------|
| **File Location** | `/sections` | Inside sections | `/blocks` | App-provided |
| **Schema** | Own `{% schema %}` | In section schema | Own `{% schema %}` | App-defined |
| **Reusability** | Template level | Section-specific | Cross-section | Cross-section |
| **Can be added via Editor** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **JSON Template Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Max per template** | 25 | N/A | N/A | N/A |
| **Nesting** | Can contain blocks | ❌ No | ✅ Yes | ✅ Yes (in theme blocks) |

## 🔍 Common Section Patterns

### 1. **Hero Section**
```liquid
<section class="hero">
  <div class="hero__background">
    {% if section.settings.image %}
      <img src="{{ section.settings.image | image_url }}" alt="">
    {% endif %}
  </div>

  <div class="hero__content">
    <h1>{{ section.settings.heading | escape }}</h1>
    <p>{{ section.settings.subheading | escape }}</p>

    {% for block in section.blocks %}
      {% case block.type %}
        {% when 'button' %}
          <a href="{{ block.settings.url }}" class="btn">
            {{ block.settings.label | escape }}
          </a>
      {% endcase %}
    {% endfor %}
  </div>
</section>
```

### 2. **Product Grid Section**
```liquid
<section class="product-grid">
  <div class="container">
    {% if section.settings.heading != blank %}
      <h2>{{ section.settings.heading | escape }}</h2>
    {% endif %}

    <div class="grid grid--{{ section.settings.columns }}">
      {% case section.settings.data_source %}
        {% when 'collection' %}
          {% assign products = section.settings.collection.products %}
        {% when 'manual' %}
          {% assign products = section.settings.products %}
      {% endcase %}

      {% for product in products limit: section.settings.limit %}
        <div class="grid__item">
          {% render 'product-card', product: product %}
        </div>
      {% endfor %}
    </div>
  </div>
</section>
```

### 3. **Flexible Content Section**
```liquid
<section class="flexible-content">
  <div class="container">
    {% for block in section.blocks %}
      <div class="content-block" {{ block.shopify_attributes }}>
        {% case block.type %}
          {% when 'text' %}
            {% render 'block-text', block: block %}
          {% when 'image' %}
            {% render 'block-image', block: block %}
          {% when 'video' %}
            {% render 'block-video', block: block %}
        {% endcase %}
      </div>
    {% endfor %}
  </div>
</section>
```

## 🛠️ Debugging Sections

### Common Issues
1. **Section not appearing**: Check presets and JSON template
2. **Blocks not working**: Verify block schema and rendering
3. **Theme editor errors**: Check shopify_attributes usage
4. **JavaScript not working**: Listen for section events

### Validation Checklist
- [ ] Valid JSON in schema
- [ ] Required attributes present
- [ ] Presets defined for dynamic sections
- [ ] Block rendering implemented
- [ ] shopify_attributes added to blocks
- [ ] Responsive design implemented
- [ ] Accessibility considerations

This comprehensive guide covers everything you need to know about Shopify sections, from basic structure to advanced patterns and best practices!