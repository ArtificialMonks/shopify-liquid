# Quick Start Guide

Build your first custom Shopify section in 6 steps. This guide gets you from zero to working section in under 15 minutes.

## Prerequisites

- Access to a Shopify theme development environment
- Basic HTML/CSS knowledge
- Text editor or VS Code with Shopify Liquid extension

## Step 1: Create the Section File

Create a new file in your theme's `sections/` folder:

**File:** `sections/hero-banner.liquid`

```liquid
{% comment %} Hero Banner Section {% endcomment %}
<section class="hero-banner" role="region" aria-label="{{ section.settings.heading | default: 'Hero banner' | escape }}">
  <div class="hero-banner__container">
    {% if section.settings.heading != blank %}
      <h1 class="hero-banner__heading">{{ section.settings.heading | escape }}</h1>
    {% endif %}

    {% if section.settings.subtext != blank %}
      <p class="hero-banner__subtext">{{ section.settings.subtext | escape }}</p>
    {% endif %}

    {% if section.settings.cta_text != blank and section.settings.cta_url != blank %}
      <a href="{{ section.settings.cta_url }}" class="hero-banner__cta btn">
        {{ section.settings.cta_text | escape }}
      </a>
    {% endif %}
  </div>
</section>

<style>
  .hero-banner {
    background: {{ section.settings.bg_color | default: '#f8f9fa' }};
    padding: {{ section.settings.padding_top }}px 20px {{ section.settings.padding_bottom }}px;
    text-align: {{ section.settings.text_align | default: 'center' }};
  }

  .hero-banner__container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .hero-banner__heading {
    font-size: {{ section.settings.heading_size }}px;
    color: {{ section.settings.heading_color | default: '#333' }};
    margin: 0 0 20px 0;
    line-height: 1.2;
  }

  .hero-banner__subtext {
    font-size: {{ section.settings.text_size }}px;
    color: {{ section.settings.text_color | default: '#666' }};
    margin: 0 0 30px 0;
    line-height: 1.5;
  }

  .hero-banner__cta {
    display: inline-block;
    background: {{ section.settings.cta_bg_color | default: '#007cba' }};
    color: {{ section.settings.cta_text_color | default: '#ffffff' }};
    padding: 12px 24px;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 600;
    transition: background-color 0.3s ease;
  }

  .hero-banner__cta:hover {
    background: {{ section.settings.cta_bg_color | default: '#007cba' | color_darken: 10 }};
  }

  @media (max-width: 768px) {
    .hero-banner {
      padding: {{ section.settings.padding_top_mobile }}px 16px {{ section.settings.padding_bottom_mobile }}px;
    }

    .hero-banner__heading {
      font-size: {{ section.settings.heading_size_mobile }}px;
    }

    .hero-banner__subtext {
      font-size: {{ section.settings.text_size_mobile }}px;
    }
  }
</style>

{% schema %}
{
  "name": "Hero Banner",
  "tag": "section",
  "class": "hero-section",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome to our store"
    },
    {
      "type": "textarea",
      "id": "subtext",
      "label": "Subtext",
      "default": "Discover our amazing products and exceptional service"
    },
    {
      "type": "text",
      "id": "cta_text",
      "label": "Button Text",
      "default": "Shop Now"
    },
    {
      "type": "url",
      "id": "cta_url",
      "label": "Button Link"
    },
    {
      "type": "header",
      "content": "Layout"
    },
    {
      "type": "select",
      "id": "text_align",
      "label": "Text Alignment",
      "options": [
        {"value": "left", "label": "Left"},
        {"value": "center", "label": "Center"},
        {"value": "right", "label": "Right"}
      ],
      "default": "center"
    },
    {
      "type": "header",
      "content": "Spacing"
    },
    {
      "type": "range",
      "id": "padding_top",
      "label": "Top Padding",
      "min": 0,
      "max": 200,
      "step": 10,
      "unit": "px",
      "default": 80
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "label": "Bottom Padding",
      "min": 0,
      "max": 200,
      "step": 10,
      "unit": "px",
      "default": 80
    },
    {
      "type": "header",
      "content": "Colors"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "default": "#f8f9fa"
    },
    {
      "type": "color",
      "id": "heading_color",
      "label": "Heading Color",
      "default": "#333333"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "default": "#666666"
    },
    {
      "type": "color",
      "id": "cta_bg_color",
      "label": "Button Background",
      "default": "#007cba"
    },
    {
      "type": "color",
      "id": "cta_text_color",
      "label": "Button Text Color",
      "default": "#ffffff"
    },
    {
      "type": "header",
      "content": "Typography"
    },
    {
      "type": "range",
      "id": "heading_size",
      "label": "Heading Size",
      "min": 24,
      "max": 72,
      "step": 2,
      "unit": "px",
      "default": 48
    },
    {
      "type": "range",
      "id": "text_size",
      "label": "Text Size",
      "min": 14,
      "max": 24,
      "step": 1,
      "unit": "px",
      "default": 18
    },
    {
      "type": "header",
      "content": "Mobile Responsive"
    },
    {
      "type": "range",
      "id": "padding_top_mobile",
      "label": "Mobile Top Padding",
      "min": 0,
      "max": 120,
      "step": 10,
      "unit": "px",
      "default": 60
    },
    {
      "type": "range",
      "id": "padding_bottom_mobile",
      "label": "Mobile Bottom Padding",
      "min": 0,
      "max": 120,
      "step": 10,
      "unit": "px",
      "default": 60
    },
    {
      "type": "range",
      "id": "heading_size_mobile",
      "label": "Mobile Heading Size",
      "min": 20,
      "max": 48,
      "step": 2,
      "unit": "px",
      "default": 32
    },
    {
      "type": "range",
      "id": "text_size_mobile",
      "label": "Mobile Text Size",
      "min": 12,
      "max": 20,
      "step": 1,
      "unit": "px",
      "default": 16
    }
  ],
  "presets": [
    {
      "name": "Hero Banner",
      "category": "Text"
    }
  ]
}
{% endschema %}
```

## Step 2: Understand the Structure

Every Shopify section has three parts:

### 1. HTML/Liquid Template
```liquid
<section class="hero-banner">
  {% if section.settings.heading != blank %}
    <h1>{{ section.settings.heading | escape }}</h1>
  {% endif %}
</section>
```

**Key Points:**
- Always escape user input with `| escape`
- Guard optional content with `{% if setting != blank %}`
- Use semantic HTML elements

### 2. CSS Styling
```liquid
<style>
  .hero-banner {
    background: {{ section.settings.bg_color }};
    padding: {{ section.settings.padding }}px;
  }
</style>
```

**Key Points:**
- Include CSS in `<style>` tags within the section
- Use Liquid variables for dynamic styling
- Include responsive breakpoints

### 3. Schema Configuration
```json
{% schema %}
{
  "name": "Hero Banner",
  "settings": [
    {"type": "text", "id": "heading", "label": "Heading"}
  ]
}
{% endschema %}
```

**Key Points:**
- Valid JSON only (no Liquid inside schema)
- Descriptive labels for merchant understanding
- Sensible defaults for immediate usability

## Step 3: Add to Template

Add your section to a template (e.g., `templates/index.json`):

```json
{
  "sections": {
    "hero": {
      "type": "hero-banner",
      "settings": {
        "heading": "Welcome to our store",
        "subtext": "Discover amazing products",
        "cta_text": "Shop Now",
        "cta_url": "/collections/all"
      }
    },
    "main": {
      "type": "main-page"
    }
  },
  "order": ["hero", "main"]
}
```

## Step 4: Test in Theme Editor

1. **Navigate to Theme Editor**: Online Store → Themes → Customize
2. **Add Section**: Click "Add section" and find "Hero Banner"
3. **Configure Settings**: Update text, colors, and spacing
4. **Preview**: Check desktop and mobile views
5. **Save**: Publish when satisfied

## Step 5: Add Blocks (Optional)

Enhance your section with repeatable blocks:

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'feature' %}
      <div class="feature" {{ block.shopify_attributes }}>
        <h3>{{ block.settings.title | escape }}</h3>
        <p>{{ block.settings.description | escape }}</p>
      </div>
  {% endcase %}
{% endfor %}
```

Add to schema:
```json
{
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        {"type": "text", "id": "title", "label": "Title"},
        {"type": "textarea", "id": "description", "label": "Description"}
      ]
    }
  ],
  "max_blocks": 6
}
```

## Step 6: Optimize and Deploy

### Performance Checklist
- ✅ Images use `image_url` with appropriate sizing
- ✅ CSS is scoped to avoid conflicts
- ✅ No JavaScript unless necessary
- ✅ Accessible markup with proper ARIA labels

### Deployment
1. **Test thoroughly** in development environment
2. **Check responsive design** on mobile/tablet
3. **Validate accessibility** with screen reader testing
4. **Deploy to live theme** or upload to Theme Store

## Common Patterns

### Conditional Content
```liquid
{% if section.settings.show_feature %}
  <div class="feature">Content here</div>
{% endif %}
```

### Dynamic Classes
```liquid
{% assign css_class = 'hero-banner' %}
{% if section.settings.large_text %}
  {% assign css_class = css_class | append: ' hero-banner--large' %}
{% endif %}

<section class="{{ css_class }}">
```

### Safe Image Handling
```liquid
{% if section.settings.background_image %}
  <img src="{{ section.settings.background_image | image_url: width: 1200 }}"
       alt="{{ section.settings.background_image.alt | escape }}"
       loading="lazy">
{% endif %}
```

## Troubleshooting

### Section Not Appearing
- Check file is in `sections/` folder
- Verify filename matches template reference
- Ensure valid JSON in schema

### Settings Not Working
- Confirm setting `id` matches Liquid variable
- Check for typos in setting names
- Validate JSON syntax with online validator

### CSS Not Applying
- Ensure CSS is inside `<style>` tags
- Check for syntax errors
- Verify Liquid variables have default values

## Next Steps

Now that you've built your first section:

1. **Learn CSS Scoping** → [Blocks & CSS Scoping](./04-blocks-and-css-scoping.md)
2. **Explore Examples** → [Code Library](./code-library/)
3. **Advanced Patterns** → [Sections & Schema](./03-sections-and-schema.md)
4. **Performance** → [Performance & Accessibility](./05-performance-and-accessibility.md)

## Key Takeaways

✅ **Every section needs**: HTML/Liquid, CSS, and Schema
✅ **Always escape user input** with `| escape` filter
✅ **Guard optional content** with conditional checks
✅ **Use semantic HTML** for accessibility
✅ **Test in theme editor** before deploying
✅ **Keep CSS scoped** to avoid conflicts

You now have a working, customizable hero banner section that merchants can easily configure through the theme editor!