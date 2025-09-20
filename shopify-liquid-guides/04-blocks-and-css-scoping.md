# Blocks & CSS Scoping

Learn the production-proven pattern for creating isolated, reusable blocks with scoped CSS that prevents style collisions and enables true modularity.

## The Problem: CSS Collisions

When you create multiple instances of the same block type, traditional CSS causes style conflicts:

```liquid
<!-- BAD: Style collisions inevitable -->
<style>
  .media-text { gap: 20px; }
  .media-text__title { color: blue; }
</style>

<div class="media-text"> <!-- First instance -->
<div class="media-text"> <!-- Second instance - same styles! -->
```

**Result**: All instances look identical, merchants can't customize individual blocks.

## The Solution: Instance-Scoped CSS

Generate unique CSS classes for each block instance using `block.id`:

```liquid
<!-- GOOD: Each block gets unique styles -->
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .media-text-{{ unique }} { gap: {{ block.settings.gap }}px; }
  .media-text__title-{{ unique }} { color: {{ block.settings.text_color }}; }
{% endstyle %}

<div class="media-text-{{ unique }}" {{ block.shopify_attributes }}>
  <h3 class="media-text__title-{{ unique }}">{{ block.settings.title | escape }}</h3>
</div>
```

**Result**: Each block instance has independent styling, fully customizable.

## Block Architecture Pattern

### 1. Generate Unique Suffix
```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}
```

This creates a clean suffix from Shopify's block ID (removes underscores, lowercase).

### 2. Scoped CSS Block
```liquid
{% style %}
  .component-{{ unique }} {
    /* Base component styles with settings */
    padding: {{ block.settings.padding }}px;
    background: {{ block.settings.bg_color }};
  }

  .component__element-{{ unique }} {
    /* Element styles */
    font-size: {{ block.settings.text_size }}px;
    color: {{ block.settings.text_color }};
  }

  /* Responsive styles in same block */
  @media (max-width: 749px) {
    .component-{{ unique }} {
      padding: {{ block.settings.padding_mobile }}px;
    }
  }
{% endstyle %}
```

### 3. Corresponding HTML Structure
```liquid
<div class="component-{{ unique }}" {{ block.shopify_attributes }}>
  <h3 class="component__element-{{ unique }}">{{ block.settings.title | escape }}</h3>
  <!-- More elements -->
</div>
```

### 4. Schema Definition
```json
{
  "type": "component",
  "name": "Component Name",
  "settings": [
    {"type": "text", "id": "title", "label": "Title"},
    {"type": "range", "id": "padding", "label": "Padding", "min": 0, "max": 100, "step": 4, "unit": "px", "default": 20},
    {"type": "color", "id": "bg_color", "label": "Background Color", "default": "#ffffff"}
  ]
}
```

## Complete Block Template

Here's a copy-paste template for any block type:

```liquid
{% comment %} Media + Text Block Template {% endcomment %}
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .media-text-{{ unique }} {
    display: flex;
    gap: {{ block.settings.gap }}px;
    padding: {{ block.settings.padding }}px;
    border-radius: {{ block.settings.radius }}px;
    background: {{ block.settings.bg_color }};
  }

  .media-text__media-{{ unique }} {
    flex: 1;
    overflow: hidden;
    border-radius: {{ block.settings.media_radius }}px;
  }

  .media-text__media-{{ unique }} img {
    width: 100%;
    height: auto;
    display: block;
  }

  .media-text__content-{{ unique }} {
    flex: 1;
    color: {{ block.settings.text_color }};
    font-size: {{ block.settings.text_size }}px;
    line-height: 1.6;
  }

  .media-text__title-{{ unique }} {
    margin: 0 0 {{ block.settings.title_margin }}px 0;
    font-size: {{ block.settings.title_size }}px;
    color: {{ block.settings.title_color }};
  }

  /* Layout variants */
  {% if block.settings.layout == 'media_left' %}
    .media-text-{{ unique }} { flex-direction: row; }
  {% else %}
    .media-text-{{ unique }} { flex-direction: row-reverse; }
  {% endif %}

  /* Responsive breakpoints */
  @media (max-width: 749px) {
    .media-text-{{ unique }} {
      flex-direction: column;
      gap: {{ block.settings.gap_mobile }}px;
      padding: {{ block.settings.padding_mobile }}px;
    }

    .media-text__content-{{ unique }} {
      font-size: {{ block.settings.text_size_mobile }}px;
    }

    .media-text__title-{{ unique }} {
      font-size: {{ block.settings.title_size_mobile }}px;
    }
  }
{% endstyle %}

<div class="media-text-{{ unique }}" {{ block.shopify_attributes }}>
  <div class="media-text__media-{{ unique }}">
    {% if block.settings.image %}
      <img
        src="{{ block.settings.image | image_url: width: 1200 }}"
        alt="{{ block.settings.image.alt | escape }}"
        loading="lazy"
        width="600"
        height="400">
    {% else %}
      <!-- Placeholder with aspect ratio -->
      <div class="media-text__placeholder-{{ unique }}"
           style="aspect-ratio: 16/9; background: #f4f4f4; display: flex; align-items: center; justify-content: center; color: #999;">
        <span>Add an image</span>
      </div>
    {% endif %}
  </div>

  <div class="media-text__content-{{ unique }}">
    {% if block.settings.title != blank %}
      <h3 class="media-text__title-{{ unique }}">{{ block.settings.title | escape }}</h3>
    {% endif %}

    {% if block.settings.content != blank %}
      <div class="media-text__text-{{ unique }}">{{ block.settings.content }}</div>
    {% endif %}

    {% if block.settings.cta_text != blank and block.settings.cta_url != blank %}
      <a href="{{ block.settings.cta_url }}" class="media-text__cta-{{ unique }}">
        {{ block.settings.cta_text | escape }}
      </a>
    {% endif %}
  </div>
</div>
```

## Schema for Block Template

```json
{
  "type": "media_text",
  "name": "Media + Text",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image"
    },
    {
      "type": "text",
      "id": "title",
      "label": "Title",
      "default": "Your Title Here"
    },
    {
      "type": "richtext",
      "id": "content",
      "label": "Content",
      "default": "<p>Add your content here.</p>"
    },
    {
      "type": "text",
      "id": "cta_text",
      "label": "Button Text"
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
      "id": "layout",
      "label": "Layout",
      "options": [
        {"value": "media_left", "label": "Media Left, Text Right"},
        {"value": "media_right", "label": "Text Left, Media Right"}
      ],
      "default": "media_left"
    },
    {
      "type": "range",
      "id": "gap",
      "label": "Gap Between Elements",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "default": 24
    },
    {
      "type": "range",
      "id": "padding",
      "label": "Padding",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "default": 20
    },
    {
      "type": "header",
      "content": "Styling"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "default": "#ffffff"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "default": "#333333"
    },
    {
      "type": "color",
      "id": "title_color",
      "label": "Title Color",
      "default": "#000000"
    },
    {
      "type": "range",
      "id": "text_size",
      "label": "Text Size",
      "min": 12,
      "max": 24,
      "step": 1,
      "unit": "px",
      "default": 16
    },
    {
      "type": "range",
      "id": "title_size",
      "label": "Title Size",
      "min": 16,
      "max": 48,
      "step": 2,
      "unit": "px",
      "default": 24
    },
    {
      "type": "header",
      "content": "Mobile Responsive"
    },
    {
      "type": "range",
      "id": "gap_mobile",
      "label": "Mobile Gap",
      "min": 0,
      "max": 60,
      "step": 4,
      "unit": "px",
      "default": 16
    },
    {
      "type": "range",
      "id": "padding_mobile",
      "label": "Mobile Padding",
      "min": 0,
      "max": 60,
      "step": 4,
      "unit": "px",
      "default": 16
    },
    {
      "type": "range",
      "id": "text_size_mobile",
      "label": "Mobile Text Size",
      "min": 12,
      "max": 20,
      "step": 1,
      "unit": "px",
      "default": 14
    },
    {
      "type": "range",
      "id": "title_size_mobile",
      "label": "Mobile Title Size",
      "min": 16,
      "max": 32,
      "step": 2,
      "unit": "px",
      "default": 20
    }
  ]
}
```

## Naming Conventions

### BEM + Unique Suffix
Use BEM (Block Element Modifier) methodology with unique suffixes:

```liquid
.block-{{ unique }}              <!-- Block -->
.block__element-{{ unique }}     <!-- Element -->
.block__element--modifier-{{ unique }} <!-- Modifier -->
```

### Examples
```liquid
.product-card-{{ unique }}           <!-- Product card block -->
.product-card__image-{{ unique }}    <!-- Image element -->
.product-card__title-{{ unique }}    <!-- Title element -->
.product-card__price-{{ unique }}    <!-- Price element -->
.product-card--featured-{{ unique }} <!-- Featured modifier -->
```

## Advanced Patterns

### Conditional Layouts
```liquid
{% style %}
  {% case block.settings.layout %}
    {% when 'stacked' %}
      .component-{{ unique }} { flex-direction: column; }
    {% when 'side_by_side' %}
      .component-{{ unique }} { flex-direction: row; }
    {% when 'overlay' %}
      .component-{{ unique }} { position: relative; }
      .component__content-{{ unique }} { position: absolute; bottom: 20px; left: 20px; }
  {% endcase %}
{% endstyle %}
```

### Dynamic State Classes
```liquid
{% assign state_class = '' %}
{% if block.settings.featured %}
  {% assign state_class = state_class | append: ' component--featured' %}
{% endif %}
{% if block.settings.large_text %}
  {% assign state_class = state_class | append: ' component--large' %}
{% endif %}

<div class="component-{{ unique }}{{ state_class }}" {{ block.shopify_attributes }}>
```

### CSS Custom Properties
```liquid
{% style %}
  .component-{{ unique }} {
    --gap: {{ block.settings.gap }}px;
    --padding: {{ block.settings.padding }}px;
    --text-color: {{ block.settings.text_color }};
    --bg-color: {{ block.settings.bg_color }};

    display: flex;
    gap: var(--gap);
    padding: var(--padding);
    color: var(--text-color);
    background: var(--bg-color);
  }
{% endstyle %}
```

## Best Practices

### Content Guards & Placeholders
```liquid
<!-- Always guard optional content -->
{% if block.settings.image %}
  <img src="{{ block.settings.image | image_url: width: 800 }}" alt="{{ block.settings.image.alt | escape }}">
{% else %}
  <!-- Provide meaningful placeholder -->
  <div class="placeholder" style="aspect-ratio: 16/9; background: #f4f4f4;">
    <span>Add an image</span>
  </div>
{% endif %}

{% if block.settings.title != blank %}
  <h3>{{ block.settings.title | escape }}</h3>
{% endif %}
```

### Performance Optimization
```liquid
<!-- Keep CSS concise - extract common patterns -->
{% style %}
  .media-text-{{ unique }} {
    /* Only dynamic values here */
    gap: {{ block.settings.gap }}px;
    padding: {{ block.settings.padding }}px;
  }
{% endstyle %}

<!-- Move static CSS to theme.css -->
<style>
  [class*="media-text-"] {
    display: flex;
    align-items: center;
    /* Common static styles */
  }
</style>
```

### Accessibility Considerations
```liquid
<!-- Proper heading hierarchy -->
{% assign heading_level = section.settings.heading_level | default: 'h3' %}
<{{ heading_level }} class="component__title-{{ unique }}">
  {{ block.settings.title | escape }}
</{{ heading_level }}>

<!-- ARIA labels for complex interactions -->
<div class="component-{{ unique }}"
     {{ block.shopify_attributes }}
     role="region"
     aria-label="{{ block.settings.title | escape }}">

<!-- Keyboard navigation support -->
{% if block.settings.link %}
  <a href="{{ block.settings.link }}" class="component__link-{{ unique }}"
     aria-label="{{ block.settings.link_text | default: block.settings.title | escape }}">
{% endif %}
```

## Common Block Patterns

### Feature Item
```liquid
{% assign u = block.id | replace: '_', '' | downcase %}
{% style %}
  .feature-{{ u }} { text-align: center; padding: {{ block.settings.padding }}px; }
  .feature__icon-{{ u }} img { width: {{ block.settings.icon_size }}px; }
  .feature__title-{{ u }} { margin: 8px 0; font-size: {{ block.settings.title_size }}px; }
{% endstyle %}

<div class="feature-{{ u }}" {{ block.shopify_attributes }}>
  {% if block.settings.icon %}
    <div class="feature__icon-{{ u }}">
      <img src="{{ block.settings.icon | image_url: width: 200 }}" alt="">
    </div>
  {% endif %}
  <h3 class="feature__title-{{ u }}">{{ block.settings.title | escape }}</h3>
  <p class="feature__text-{{ u }}">{{ block.settings.text }}</p>
</div>
```

### Testimonial Card
```liquid
{% assign u = block.id | replace: '_', '' | downcase %}
{% style %}
  .testimonial-{{ u }} {
    background: {{ block.settings.bg_color }};
    padding: {{ block.settings.padding }}px;
    border-radius: {{ block.settings.radius }}px;
  }
  .testimonial__quote-{{ u }} { font-style: italic; margin-bottom: 20px; }
  .testimonial__author-{{ u }} { font-weight: bold; }
{% endstyle %}

<div class="testimonial-{{ u }}" {{ block.shopify_attributes }}>
  <blockquote class="testimonial__quote-{{ u }}">
    "{{ block.settings.quote | escape }}"
  </blockquote>
  <cite class="testimonial__author-{{ u }}">{{ block.settings.author | escape }}</cite>
</div>
```

## Troubleshooting

### CSS Not Applying
- Check that `{{ unique }}` is properly generated
- Verify CSS class names match HTML class names exactly
- Ensure `{% style %}` block is before HTML markup

### Theme Editor Issues
- Always include `{{ block.shopify_attributes }}` on root element
- Check that block `type` in schema matches template file

### Performance Issues
- Extract static CSS to theme files
- Minimize dynamic CSS to only necessary properties
- Use CSS custom properties for repeated values

## Next Steps

Continue building with production-ready patterns:
- **[Performance & Accessibility](./05-performance-and-accessibility.md)** - Production optimization
- **[Code Library - Sections](./code-library/sections/)** - Complete scoped examples
- **[CSS Patterns](./code-library/css-patterns/)** - Advanced styling techniques
- **[Troubleshooting](./06-troubleshooting.md)** - Common CSS scoping issues

## Essential References

### Critical Implementation
- **[Schema Validation Guidelines](./schema-validation/schema-guidelines.md)** - **ALWAYS validate schemas**
- **[Theme Architecture](./docs/architecture/theme-overview.md)** - How CSS fits in theme structure

### Asset Management
- **[CSS Assets](./docs/assets/css-assets.md)** - Styling organization and optimization
- **[Asset Optimization](./docs/assets/)** - Performance patterns for all asset types
- **[Advanced Performance](./docs/advanced-features/advanced-performance.md)** - Cutting-edge optimization

### Configuration Integration
- **[Block Configuration](./docs/config/blocks-config.md)** - Schema patterns for styled components
- **[Section Groups](./docs/config/section-groups.md)** - Scoping in dynamic layouts

### Modern Development
- **[Advanced Features](./docs/advanced-features/)** - AI blocks, PWA, modern patterns
- **[Best Practices 2025](./docs/architecture/best-practices-2025.md)** - Current CSS standards