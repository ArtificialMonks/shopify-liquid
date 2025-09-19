# Section Schema Deep Dive

The schema is the **brain** of your Shopify section - it defines what merchants can customize and how your section behaves in the theme editor. Think of it as the **control panel** for your section.

## What is a Schema?

A schema is **JSON configuration** that tells Shopify:
- What settings to show in the theme editor
- What blocks merchants can add
- How the section should behave
- Where it can be used

It's like creating a **custom form** that generates the exact controls your section needs.

---

## Basic Schema Structure

Every schema has this fundamental structure:

```json
{% schema %}
{
  "name": "Section Name",
  "tag": "section", 
  "class": "my-section",
  "settings": [...],
  "blocks": [...],
  "presets": [...],
  "max_blocks": 10,
  "enabled_on": {...},
  "disabled_on": {...},
  "locales": {...}
}
{% endschema %}
```

🎯 **Key Point**: The schema must be **valid JSON** and placed at the very end of your `.liquid` file.

---

## Core Schema Properties

### `name` (Required)
The display name in the theme editor.

```json
{
  "name": "Hero Banner"
}
```

### `tag` (Optional)
The HTML wrapper element. Default is `div`.

```json
{
  "tag": "section"
}
```
**Generates**: `<section id="shopify-section-123">...content...</section>`

### `class` (Optional)
Additional CSS classes for the wrapper.

```json
{
  "class": "hero-section full-width"
}
```

### `limit` (Optional)
Maximum times this section can be used.

```json
{
  "limit": 1
}
```
**Use case**: Header/footer sections that should only appear once.

---

## Settings: The Control Panel

Settings create the input fields merchants see. Here are all the types available:

### Text Input Settings

```json
{
  "type": "text",
  "id": "heading",
  "label": "Section Heading",
  "default": "Welcome to Our Store",
  "placeholder": "Enter your heading...",
  "info": "This appears as the main heading"
}
```

```json
{
  "type": "textarea", 
  "id": "description",
  "label": "Description",
  "default": "Tell your story here"
}
```

```json
{
  "type": "richtext",
  "id": "rich_content",
  "label": "Rich Text Content", 
  "default": "<p>Formatted <strong>text</strong> with HTML</p>"
}
```

### Media Settings

```json
{
  "type": "image_picker",
  "id": "background_image",
  "label": "Background Image"
}
```

```json
{
  "type": "video",
  "id": "hero_video", 
  "label": "Hero Video"
}
```

```json
{
  "type": "video_url",
  "id": "youtube_video",
  "label": "YouTube/Vimeo URL",
  "accept": ["youtube", "vimeo"]
}
```

### Selection Settings

```json
{
  "type": "select",
  "id": "layout",
  "label": "Layout Style",
  "default": "left",
  "options": [
    {"value": "left", "label": "Image Left"},
    {"value": "right", "label": "Image Right"}, 
    {"value": "center", "label": "Centered"}
  ]
}
```

```json
{
  "type": "radio",
  "id": "alignment",
  "label": "Text Alignment",
  "default": "center",
  "options": [
    {"value": "left", "label": "Left"},
    {"value": "center", "label": "Center"},
    {"value": "right", "label": "Right"}
  ]
}
```

```json
{
  "type": "checkbox",
  "id": "show_overlay",
  "label": "Show overlay",
  "default": true
}
```

### Range Settings

```json
{
  "type": "range", 
  "id": "opacity",
  "label": "Background Opacity",
  "min": 0,
  "max": 100,
  "step": 5,
  "unit": "%",
  "default": 50
}
```

### Color Settings

```json
{
  "type": "color",
  "id": "text_color",
  "label": "Text Color",
  "default": "#000000"
}
```

```json
{
  "type": "color_background",
  "id": "section_background",
  "label": "Section Background"
}
```

### Link Settings

```json
{
  "type": "url",
  "id": "button_link",
  "label": "Button URL"
}
```

```json
{
  "type": "page",
  "id": "page_link",
  "label": "Choose Page"
}
```

```json
{
  "type": "product",
  "id": "featured_product", 
  "label": "Featured Product"
}
```

```json
{
  "type": "collection",
  "id": "featured_collection",
  "label": "Featured Collection"
}
```

### Font Settings

```json
{
  "type": "font_picker",
  "id": "heading_font",
  "label": "Heading Font",
  "default": "helvetica_n4"
}
```

### Organization Settings

```json
{
  "type": "header",
  "content": "Layout Settings"
}
```

```json
{
  "type": "paragraph", 
  "content": "These settings control how your content appears."
}
```

---

## Accessing Settings in Liquid

Once you define settings in your schema, access them like this:

```liquid
<!-- Text settings -->
<h2>{{ section.settings.heading }}</h2>
<p>{{ section.settings.description }}</p>

<!-- Image settings -->
{% if section.settings.background_image %}
  <img src="{{ section.settings.background_image | image_url: width: 1200 }}" 
       alt="{{ section.settings.background_image.alt }}">
{% endif %}

<!-- Boolean settings -->
{% if section.settings.show_overlay %}
  <div class="overlay"></div>
{% endif %}

<!-- Select/radio settings -->
<div class="layout-{{ section.settings.layout }}">
  Content here
</div>

<!-- Range settings -->
<div style="opacity: {{ section.settings.opacity }}%;">
  Content with opacity
</div>

<!-- Color settings -->
<div style="color: {{ section.settings.text_color }};">
  Colored text
</div>
```

---

## Advanced Schema Features

### Conditional Settings

Show/hide settings based on other settings:

```json
{
  "type": "checkbox",
  "id": "show_button",
  "label": "Show Button",
  "default": false
},
{
  "type": "text",
  "id": "button_text",
  "label": "Button Text", 
  "default": "Click Here",
  "conditional": {
    "field": "show_button",
    "equals": true
  }
}
```

### Setting Validation

```json
{
  "type": "text",
  "id": "email",
  "label": "Contact Email",
  "placeholder": "contact@example.com",
  "pattern": "^[^@]+@[^@]+\\.[^@]+$",
  "error": "Please enter a valid email address"
}
```

### Setting Groups

Organize related settings:

```json
{
  "type": "group",
  "label": "Button Settings",
  "settings": [
    {
      "type": "text", 
      "id": "button_text",
      "label": "Button Text"
    },
    {
      "type": "url",
      "id": "button_url", 
      "label": "Button Link"
    }
  ]
}
```

---

## Presets: Quick Setup Templates

Presets let merchants quickly add your section with smart defaults:

```json
{
  "presets": [
    {
      "name": "Hero Banner",
      "category": "Image",
      "settings": {
        "heading": "Welcome to Our Store",
        "show_button": true,
        "button_text": "Shop Now"
      },
      "blocks": [
        {
          "type": "slide"
        },
        {
          "type": "slide"  
        }
      ]
    },
    {
      "name": "Simple Hero",
      "category": "Text", 
      "settings": {
        "heading": "Simple Header",
        "show_button": false
      }
    }
  ]
}
```

🎯 **Pro Tip**: Create multiple presets for different use cases (e.g., "E-commerce Hero", "Blog Hero", "Landing Page Hero").

---

## Section Restrictions

### Enable/Disable on Templates

```json
{
  "enabled_on": {
    "templates": ["index", "product", "collection"],
    "groups": ["header", "footer", "aside"]
  }
}
```

```json
{
  "disabled_on": {
    "templates": ["cart", "checkout"],
    "groups": ["footer"]
  }
}
```

**Available templates**: `index`, `product`, `collection`, `blog`, `article`, `page`, `cart`, `search`, `404`, `list-collections`

**Available groups**: `header`, `footer`, `aside`

---

## Localization Support

Support multiple languages:

```json
{
  "locales": {
    "en": {
      "name": "Hero Section"
    },
    "fr": {
      "name": "Section Héros" 
    },
    "es": {
      "name": "Sección Hero"
    }
  }
}
```

---

## Complete Example Schema

Here's a comprehensive schema showing most features:

```json
{% schema %}
{
  "name": "Advanced Hero Section",
  "tag": "section",
  "class": "hero-section",
  "limit": 1,
  "settings": [
    {
      "type": "header",
      "content": "Content Settings"
    },
    {
      "type": "text",
      "id": "heading", 
      "label": "Main Heading",
      "default": "Welcome to Our Store"
    },
    {
      "type": "richtext",
      "id": "subheading",
      "label": "Subheading",
      "default": "<p>Discover amazing products</p>"
    },
    {
      "type": "header",
      "content": "Visual Settings"
    },
    {
      "type": "image_picker",
      "id": "background_image",
      "label": "Background Image"
    },
    {
      "type": "range",
      "id": "overlay_opacity",
      "label": "Overlay Opacity", 
      "min": 0,
      "max": 100,
      "step": 10,
      "unit": "%",
      "default": 50
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "default": "#ffffff"
    },
    {
      "type": "header",
      "content": "Layout Options"
    },
    {
      "type": "select",
      "id": "height",
      "label": "Section Height",
      "default": "medium",
      "options": [
        {"value": "small", "label": "Small (400px)"},
        {"value": "medium", "label": "Medium (600px)"},
        {"value": "large", "label": "Large (800px)"},
        {"value": "fullscreen", "label": "Full Screen"}
      ]
    },
    {
      "type": "checkbox",
      "id": "show_button",
      "label": "Show Call-to-Action Button",
      "default": true
    },
    {
      "type": "text",
      "id": "button_text",
      "label": "Button Text",
      "default": "Shop Now"
    },
    {
      "type": "url", 
      "id": "button_url",
      "label": "Button Link"
    }
  ],
  "presets": [
    {
      "name": "Hero Section",
      "category": "Image"
    }
  ],
  "enabled_on": {
    "templates": ["index", "collection", "product"]
  }
}
{% endschema %}
```

---

## Best Practices

### ✅ Do This

1. **Use descriptive labels** - "Button Text" not "Text"
2. **Provide helpful defaults** - save merchants time
3. **Group related settings** with headers
4. **Add info text** for complex settings
5. **Use appropriate input types** - `url` for links, `color` for colors
6. **Test all settings** - make sure they work in Liquid

### ❌ Avoid This

1. **Too many settings** - overwhelms merchants
2. **Poor setting names** - `id: "thing1"` is unclear
3. **Missing presets** - section won't appear in editor
4. **Invalid JSON** - breaks the entire section
5. **Unused settings** - confuses merchants
6. **No default values** - creates blank sections

---

## Debugging Schema Issues

**Schema not loading?**
```liquid
<!-- Check JSON syntax -->
{% comment %}
Use a JSON validator to check your schema
{% endcomment %}
```

**Settings not appearing?**
- Verify setting `id` values are unique
- Check that brackets and commas are correct
- Ensure you're inside the `settings` array

**Liquid errors?**
- Make sure `section.settings.your_id` matches schema `id`
- Check for typos in setting names
- Verify data types (text vs. boolean vs. number)

---

## Next Steps

Now that you understand schemas, let's explore [Block Types & Configuration](./03-blocks.md) to create sections with dynamic, repeatable content!
