# Code Library

Production-ready Shopify Liquid components, sections, and CSS patterns. All code follows best practices and is ready to copy into your theme.

**📋 Complete Repository Structure**: See [../../STRUCTURE.md](../../STRUCTURE.md) for detailed file tree and navigation guide.

## 📁 Sections

Complete section templates with schema and styling:

- **[hero-banner.liquid](./sections/hero-banner.liquid)** - Minimal hero section template
- **[hero-richtext-cta.liquid](./sections/hero-richtext-cta.liquid)** - Rich text hero with CTA button
- **[testimonial-carousel.liquid](./sections/testimonial-carousel.liquid)** - Accessible testimonial carousel

## 🧩 Blocks

Reusable block components with scoped CSS:

- **[block-media-text.liquid](./blocks/block-media-text.liquid)** - Media and text block with layout options
- **[block-feature-item.liquid](./blocks/block-feature-item.liquid)** - Feature item with icon, title, and text

## 📦 Snippets

Utility components and helpers:

- **[responsive-image.liquid](./snippets/responsive-image.liquid)** - Responsive image with srcset
- **[metafield-render.liquid](./snippets/metafield-render.liquid)** - Metafield rendering utility

## 🎨 CSS Patterns

Styling methodologies and patterns:

- **[scoped-blocks.css](./css-patterns/scoped-blocks.css)** - Complete CSS scoping methodology
- **[responsive-grid.css](./css-patterns/responsive-grid.css)** - Responsive grid patterns
- **[accessibility.css](./css-patterns/accessibility.css)** - Accessibility-first CSS

## Usage Guidelines

### Copy & Paste Ready
All code is production-tested and follows Shopify best practices. You can copy any file directly into your theme.

### CSS Scoping
Block components use the unique ID scoping pattern:
```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}
{% style %}
  .component-{{ unique }} { /* styles */ }
{% endstyle %}
```

### Schema Standards
- Clear, descriptive labels
- Helpful info text for complex settings
- Sensible defaults for immediate usability
- Logical grouping with header sections

### Performance Optimized
- Responsive images with proper sizing
- Lazy loading for below-the-fold content
- Minimal CSS footprint
- Accessible markup patterns

## Integration Examples

### Adding a Block to Your Section
1. Copy the block file to your theme
2. Add the block schema to your section's `{% schema %}` blocks array
3. Handle the block in your section's markup:

```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'media_text' %}
      {% render 'block-media-text', block: block %}
  {% endcase %}
{% endfor %}
```

### Using Snippets
Include snippets with the render tag:
```liquid
{% render 'responsive-image', image: product.featured_image, sizes: '(min-width: 750px) 400px, 100vw' %}
```

## Code Standards & Validation

All code follows these standards:
- ✅ Always escape user input with `| escape`
- ✅ Guard optional settings with `{% if setting != blank %}`
- ✅ Use semantic HTML and ARIA labels
- ✅ Mobile-first responsive design
- ✅ Performance-optimized images
- ✅ Theme editor compatibility with `{{ block.shopify_attributes }}`
- ✅ **100% Theme Store compliance** - Validated with automated workflow

### Validation Workflow
Before using any code library component:

```bash
# Quick validation for development
./scripts/validate-theme.sh development

# Complete validation workflow
./scripts/validate-theme.sh all

# Auto-fix common issues
./scripts/validate-theme.sh auto-fix
```

📖 **[Complete Validation Setup](../../THEME-CHECK-SETUP.md)** - Ultimate validation automation guide