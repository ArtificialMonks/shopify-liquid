# Quick Start Guide

Build your first custom Shopify section in 6 steps using modern development patterns. This guide implements **CSS scoping methodology** and **schema validation** from the start.

## Prerequisites

- Access to a Shopify theme development environment
- Basic HTML/CSS knowledge
- VS Code with Shopify Liquid extension (recommended)
- **CRITICAL**: Review [Schema Validation Guidelines](./schema-validation/schema-guidelines.md) first

## Step 1: Create the Section File

Create a new file in your theme's `sections/` folder:

**File:** `sections/hero-banner.liquid`

```liquid
{% comment %}
  Hero Banner Section
  Uses CSS scoping methodology to prevent style conflicts
{% endcomment %}

{% assign unique = section.id | replace: '_', '' | downcase %}

<section class="hero-banner-{{ unique }}" role="region" aria-label="{{ section.settings.heading | default: 'Hero banner' | escape }}">
  {% style %}
    .hero-banner-{{ unique }} {
      background: {{ section.settings.bg_color | default: '#f8f9fa' }};
      padding: {{ section.settings.padding_top }}px 20px {{ section.settings.padding_bottom }}px;
      text-align: {{ section.settings.text_align | default: 'center' }};
    }

    .hero-banner__container-{{ unique }} {
      max-width: 1200px;
      margin: 0 auto;
    }

    .hero-banner__heading-{{ unique }} {
      font-size: {{ section.settings.heading_size }}px;
      color: {{ section.settings.heading_color | default: '#333' }};
      margin: 0 0 20px 0;
      line-height: 1.2;
    }

    .hero-banner__subtext-{{ unique }} {
      font-size: {{ section.settings.text_size }}px;
      color: {{ section.settings.text_color | default: '#666' }};
      margin: 0 0 30px 0;
      line-height: 1.5;
    }

    .hero-banner__cta-{{ unique }} {
      display: inline-block;
      background: {{ section.settings.cta_bg_color | default: '#007cba' }};
      color: {{ section.settings.cta_text_color | default: '#ffffff' }};
      padding: 12px 24px;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 600;
      transition: background-color 0.3s ease;
    }

    .hero-banner__cta-{{ unique }}:hover {
      opacity: 0.9;
    }

    @media (max-width: 768px) {
      .hero-banner-{{ unique }} {
        padding: {{ section.settings.padding_top_mobile }}px 16px {{ section.settings.padding_bottom_mobile }}px;
      }

      .hero-banner__heading-{{ unique }} {
        font-size: {{ section.settings.heading_size_mobile }}px;
      }

      .hero-banner__subtext-{{ unique }} {
        font-size: {{ section.settings.text_size_mobile }}px;
      }
    }
  {% endstyle %}

  <div class="hero-banner__container-{{ unique }}">
    {% if section.settings.heading != blank %}
      <h1 class="hero-banner__heading-{{ unique }}">{{ section.settings.heading | escape }}</h1>
    {% endif %}

    {% if section.settings.subtext != blank %}
      <p class="hero-banner__subtext-{{ unique }}">{{ section.settings.subtext | escape }}</p>
    {% endif %}

    {% if section.settings.cta_text != blank and section.settings.cta_url != blank %}
      <a href="{{ section.settings.cta_url }}" class="hero-banner__cta-{{ unique }}">
        {{ section.settings.cta_text | escape }}
      </a>
    {% endif %}
  </div>
</section>

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
      "label": "Top Padding (Desktop)",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "px",
      "default": 60
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "label": "Bottom Padding (Desktop)",
      "min": 0,
      "max": 100,
      "step": 5,
      "unit": "px",
      "default": 60
    },
    {
      "type": "range",
      "id": "padding_top_mobile",
      "label": "Top Padding (Mobile)",
      "min": 0,
      "max": 80,
      "step": 5,
      "unit": "px",
      "default": 40
    },
    {
      "type": "range",
      "id": "padding_bottom_mobile",
      "label": "Bottom Padding (Mobile)",
      "min": 0,
      "max": 80,
      "step": 5,
      "unit": "px",
      "default": 40
    },
    {
      "type": "header",
      "content": "Typography"
    },
    {
      "type": "range",
      "id": "heading_size",
      "label": "Heading Size (Desktop)",
      "min": 24,
      "max": 72,
      "step": 2,
      "unit": "px",
      "default": 48
    },
    {
      "type": "range",
      "id": "heading_size_mobile",
      "label": "Heading Size (Mobile)",
      "min": 20,
      "max": 48,
      "step": 2,
      "unit": "px",
      "default": 32
    },
    {
      "type": "range",
      "id": "text_size",
      "label": "Text Size (Desktop)",
      "min": 14,
      "max": 24,
      "step": 1,
      "unit": "px",
      "default": 18
    },
    {
      "type": "range",
      "id": "text_size_mobile",
      "label": "Text Size (Mobile)",
      "min": 14,
      "max": 20,
      "step": 1,
      "unit": "px",
      "default": 16
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
    }
  ],
  "presets": [
    {
      "name": "Hero Banner",
      "settings": {
        "heading": "Welcome to our store",
        "subtext": "Discover our amazing products and exceptional service",
        "cta_text": "Shop Now"
      }
    }
  ]
}
{% endschema %}
```

## Step 2: Understanding CSS Scoping

This section uses **CSS scoping methodology** to prevent style conflicts:

```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
```

Every CSS class gets the unique identifier:
- `.hero-banner-{{ unique }}` - Base component
- `.hero-banner__heading-{{ unique }}` - BEM element with unique suffix

**Why this matters:**
- Prevents style conflicts when section is used multiple times
- Enables true component modularity
- Follows established [CSS Scoping methodology](./04-blocks-and-css-scoping.md)

## Step 3: Schema Validation

The schema follows our [Schema Validation Guidelines](./schema-validation/schema-guidelines.md):

**Range Validation Example:**
```json
{
  "type": "range",
  "id": "padding_top",
  "min": 0,
  "max": 100,
  "step": 5
}
```

**Validation check:** `(100 - 0) / 5 = 20 ≤ 101` ✅

## Step 4: Add Section to Theme

1. Upload the `hero-banner.liquid` file to your theme's `sections/` folder
2. Go to **Online Store → Themes → Customize**
3. Add the "Hero Banner" section to your homepage
4. Configure the settings and save

## Step 5: Test Responsiveness

Test across devices to ensure:
- Mobile padding settings work correctly
- Font sizes scale appropriately
- Text alignment is consistent
- Colors have proper contrast

## Step 6: Customize Further

Now you can:
- Add image background support
- Include additional blocks
- Extend color options
- Add animation effects

## Key Concepts Learned

### CSS Scoping Methodology
```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
<div class="component-{{ unique }}">
  {% style %}
    .component-{{ unique }} { /* styles */ }
  {% endstyle %}
</div>
```

### Schema Validation
- All ranges validated: `(max - min) / step ≤ 101`
- Descriptive labels and helpful defaults
- Logical setting grouping with headers

### Production-Ready Patterns
- User input escaped: `{{ text | escape }}`
- Conditional rendering: `{% if setting != blank %}`
- Responsive design: Mobile-specific settings
- Accessibility: Proper ARIA labels and semantic HTML

## Next Steps

Now that you've built your first section:

- **[Sections & Schema](./03-sections-and-schema.md)** - Deep dive into schema configuration
- **[CSS Scoping Methodology](./04-blocks-and-css-scoping.md)** - Master conflict prevention
- **[Performance & Accessibility](./05-performance-and-accessibility.md)** - Production optimization
- **[Code Library](./code-library/sections/)** - See advanced examples

## Essential References

- **[Schema Validation](./schema-validation/schema-guidelines.md)** - CRITICAL for all development
- **[Theme Architecture](./docs/architecture/theme-overview.md)** - Understanding theme structure
- **[CSS Assets](./docs/assets/css-assets.md)** - Styling organization patterns
- **[Best Practices 2025](./docs/architecture/best-practices-2025.md)** - Current standards

## Troubleshooting

**Section not appearing?**
- Check file is in correct `sections/` folder
- Verify JSON schema syntax (no trailing commas)
- Ensure range calculations are valid

**Styles conflicting?**
- Verify unique ID generation: `{{ unique }}`
- Check all classes use unique suffix
- Review [CSS Scoping guide](./04-blocks-and-css-scoping.md)

**Schema errors?**
- Validate against [Schema Guidelines](./schema-validation/schema-guidelines.md)
- Check range step calculations
- Verify setting types are correct