# Blocks

Reusable Shopify Liquid block templates for dynamic content within sections.

## Available Blocks

| Block | Description | Use Case |
|-------|-------------|----------|
| `block-media-text.liquid` | Media and text combination | Feature highlights, content blocks |
| `block-feature-item.liquid` | Feature item with icon/text | Feature lists, benefit highlights |

## Block Architecture

Blocks are designed to work within sections and provide:
- **Dynamic Content**: User-configurable through section settings
- **CSS Scoping**: Unique styling to prevent conflicts
- **Accessibility**: Proper ARIA labels and semantic HTML
- **Responsive Design**: Mobile-first approach

## CSS Scoping for Blocks

Blocks use both section and block IDs for unique styling:

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}
{% assign section_unique = section.id | replace: '_', '' | downcase %}
```

Apply nested scoped styles:
```css
.section-name-{{ section_unique }} .block-name-{{ unique }} {
  /* Block-specific styles */
}
```

## Block Implementation

Include blocks within section templates:

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'feature_item' %}
      {% render 'block-feature-item', block: block %}
    {% when 'media_text' %}
      {% render 'block-media-text', block: block %}
  {% endcase %}
{% endfor %}
```

For detailed implementation patterns, see [04-blocks-and-css-scoping.md](../../04-blocks-and-css-scoping.md).