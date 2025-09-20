# Shopify Liquid Blocks - Complete Official Documentation

## 🎯 Key Discovery: Blocks CAN Be Saved Separately!

**IMPORTANT CORRECTION**: Based on official Shopify documentation research, there are **THREE types of blocks** in Shopify themes, and **Theme Blocks** are indeed standalone files that can be saved separately.

## 📚 Types of Blocks in Shopify

### 1. **Theme Blocks** (Standalone Files)
- **Location**: `/blocks` folder in theme root
- **File Extension**: `.liquid`
- **Schema**: Has its own `{% schema %}` tag
- **Reusability**: Can be used across multiple sections
- **Nesting**: Can contain other blocks (hierarchical)

### 2. **Section Blocks** (Defined Within Sections)
- **Location**: Defined within section files
- **Schema**: Defined in section's `{% schema %}` blocks array
- **Reusability**: Only within the section where defined
- **Nesting**: Cannot be nested (single level only)

### 3. **App Blocks** (Provided by Apps)
- **Location**: Provided by installed apps
- **Purpose**: Allow app functionality in themes
- **Type**: `@app` in schema

## 🏗️ Theme Blocks - The Standalone Files

### File Structure
```
theme/
├── blocks/           ← Theme blocks go here!
│   ├── text.liquid
│   ├── image.liquid
│   └── group.liquid
├── sections/
│   └── custom.liquid
└── ...
```

### Basic Theme Block Example
```liquid
<!-- blocks/text.liquid -->
<div class="text-block" {{ block.shopify_attributes }}>
  {% if block.settings.heading != blank %}
    <h3>{{ block.settings.heading | escape }}</h3>
  {% endif %}

  {% if block.settings.text != blank %}
    <div>{{ block.settings.text }}</div>
  {% endif %}
</div>

{% schema %}
{
  "name": "Text",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "richtext",
      "id": "text",
      "label": "Text"
    }
  ],
  "presets": [
    {
      "name": "Text",
      "settings": {
        "text": "Add your text here"
      }
    }
  ]
}
{% endschema %}
```

## 🔗 Using Theme Blocks in Sections

### Section That Accepts Theme Blocks
```liquid
<!-- sections/custom.liquid -->
<section class="custom-section">
  <div class="container">
    {% content_for 'blocks' %}
  </div>
</section>

{% schema %}
{
  "name": "Custom Section",
  "blocks": [
    {"type": "@theme"},  // Accepts ALL theme blocks
    {"type": "@app"}     // Also accepts app blocks
  ],
  "presets": [
    {"name": "Custom Section"}
  ]
}
{% endschema %}
```

### Targeted Block Support
```liquid
{% schema %}
{
  "name": "Text Only Section",
  "blocks": [
    {"type": "text"},      // Only accepts text theme blocks
    {"type": "heading"}    // Only accepts heading theme blocks
  ]
}
{% endschema %}
```

## 🎨 Theme Block Schema

### Complete Schema Structure
```json
{
  "name": "Block Name",
  "tag": "div",
  "class": "custom-class",
  "settings": [
    {
      "type": "text",
      "id": "title",
      "label": "Title"
    }
  ],
  "blocks": [
    {"type": "@theme"},
    {"type": "@app"}
  ],
  "presets": [
    {
      "name": "Default",
      "settings": {
        "title": "Default Title"
      },
      "blocks": [
        {
          "type": "text",
          "settings": {
            "text": "Nested content"
          }
        }
      ]
    }
  ]
}
```

### Schema Attributes
- **`name`**: Display name in theme editor
- **`tag`**: HTML wrapper tag (optional)
- **`class`**: CSS class for wrapper (optional)
- **`settings`**: Block configuration options
- **`blocks`**: Child blocks this block can contain
- **`presets`**: Pre-configured variations

## 🔄 Nested Blocks (Theme Blocks Only)

Theme blocks can contain other blocks, creating hierarchy:

```liquid
<!-- blocks/group.liquid -->
<div class="group-block" {{ block.shopify_attributes }}>
  <h2>{{ block.settings.heading | escape }}</h2>

  <div class="group-content">
    {% content_for 'blocks' %}
  </div>
</div>

{% schema %}
{
  "name": "Group",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Group Heading"
    }
  ],
  "blocks": [
    {"type": "@theme"},
    {"type": "@app"}
  ],
  "presets": [
    {
      "name": "Text Group",
      "settings": {
        "heading": "Content Group"
      },
      "blocks": [
        {
          "type": "text",
          "settings": {
            "text": "First text block"
          }
        },
        {
          "type": "text",
          "settings": {
            "text": "Second text block"
          }
        }
      ]
    }
  ]
}
{% endschema %}
```

## 🔧 Static Blocks

Theme blocks can be rendered statically for more control:

```liquid
<!-- Static rendering in sections -->
<section>
  <header>
    {% content_for "block", type: "heading", id: "main-heading" %}
  </header>

  <main>
    {% content_for 'blocks' %}  <!-- Dynamic blocks -->
  </main>

  <footer>
    {% content_for "block", type: "text", id: "footer-text" %}
  </footer>
</section>
```

**Static vs Dynamic Blocks:**
| Static Blocks | Dynamic Blocks |
|---------------|----------------|
| Can be hidden/customized | Can be hidden/customized |
| Cannot be reordered | Can be reordered |
| Cannot be removed | Can be removed/duplicated |
| Don't count toward max_blocks | Count toward max_blocks |

## 💡 Liquid Objects in Theme Blocks

### Available Objects
- **`block`**: Current block's settings and properties
- **`section`**: Parent section's settings and properties
- **Global objects**: `shop`, `product`, `collection`, etc.

### Key Block Properties
```liquid
{{ block.id }}              <!-- Unique block ID -->
{{ block.type }}            <!-- Block type name -->
{{ block.settings.title }}  <!-- Block setting values -->
{{ block.shopify_attributes }} <!-- Required for theme editor -->
```

### Cannot Access
- Variables from parent section
- Parameters passed like snippets
- Variables from other blocks

## 🎯 Block Targeting

Restrict which blocks can be used in specific contexts:

```json
{
  "blocks": [
    {"type": "text"},           // Specific theme block
    {"type": "image"},          // Specific theme block
    {"type": "@app"},           // All app blocks
    {"type": "@theme"}          // All theme blocks
  ]
}
```

## 📱 Theme Editor Integration

### Required Attributes
```liquid
<div {{ block.shopify_attributes }}>
  <!-- Block content -->
</div>
```

### Presets for Theme Editor
Blocks need presets to appear in the theme editor's block picker:
```json
{
  "presets": [
    {
      "name": "Simple Text",
      "settings": {
        "text": "Default text"
      }
    },
    {
      "name": "Highlighted Text",
      "settings": {
        "text": "Important message",
        "highlight": true
      }
    }
  ]
}
```

## 🚀 Best Practices

### 1. **Use Theme Blocks When:**
- Need reusability across sections
- Want hierarchical nesting
- Building complex layouts
- Creating design systems

### 2. **File Organization:**
```
blocks/
├── layout/
│   ├── container.liquid
│   ├── column.liquid
│   └── row.liquid
├── content/
│   ├── text.liquid
│   ├── heading.liquid
│   └── image.liquid
└── interactive/
    ├── button.liquid
    └── form.liquid
```

### 3. **Naming Conventions:**
- Use descriptive names: `product-card.liquid`
- Group by functionality: `layout-container.liquid`
- Be consistent across theme

### 4. **Schema Design:**
- Always include presets
- Use clear labels and info text
- Group related settings
- Provide sensible defaults

## 🔍 Debugging Theme Blocks

### Common Issues
1. **Block not appearing**: Check presets are defined
2. **Settings not working**: Verify schema JSON syntax
3. **Nesting issues**: Ensure parent accepts `@theme` blocks
4. **Theme editor errors**: Check `shopify_attributes` usage

### Validation
- JSON schema must be valid
- Block types must match file names
- Presets are required for theme editor visibility

## 📊 Comparison: Theme Blocks vs Section Blocks vs App Blocks

| Feature | Theme Blocks | Section Blocks | App Blocks |
|---------|-------------|----------------|------------|
| **File Location** | `/blocks` folder | Inside section files | Provided by apps |
| **Schema Tag** | `{% schema %}` | In section's blocks array | App-defined |
| **Reusability** | Across multiple sections | Single section only | Across multiple sections |
| **Nesting** | ✅ Yes | ❌ No | ✅ Yes (in theme blocks) |
| **Can Save Separately** | ✅ Yes | ❌ No | ❌ No (app-managed) |
| **Access to** | `block`, `section` objects | `block` object | `block` object |
| **Use Case** | Design systems, layouts | Simple section-specific content | App functionality |

## 🎬 Real-World Example: Video Block

```liquid
<!-- blocks/video.liquid -->
<div class="video-block" {{ block.shopify_attributes }}>
  {% if block.settings.heading != blank %}
    <h3 class="video-block__heading">{{ block.settings.heading | escape }}</h3>
  {% endif %}

  <div class="video-block__container">
    {% if block.settings.video_url contains 'youtube' %}
      <iframe src="{{ block.settings.video_url }}" frameborder="0" allowfullscreen></iframe>
    {% elsif block.settings.video_file %}
      <video controls>
        <source src="{{ block.settings.video_file }}" type="video/mp4">
      </video>
    {% endif %}
  </div>

  {% if block.settings.caption != blank %}
    <p class="video-block__caption">{{ block.settings.caption | escape }}</p>
  {% endif %}
</div>

{% schema %}
{
  "name": "Video",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "video_url",
      "id": "video_url",
      "label": "Video URL",
      "accept": ["youtube", "vimeo"]
    },
    {
      "type": "video",
      "id": "video_file",
      "label": "Video File"
    },
    {
      "type": "text",
      "id": "caption",
      "label": "Caption"
    }
  ],
  "presets": [
    {
      "name": "Video"
    }
  ]
}
{% endschema %}
```

This comprehensive documentation shows that **theme blocks are indeed standalone files** that can be saved separately in the `/blocks` folder and have their own schema tags. They're a powerful feature for creating reusable, nestable components in Shopify themes!