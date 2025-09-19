# Sections

Production-ready Shopify Liquid section templates with complete schema configurations.

## Available Sections

| Section | Description | Key Features |
|---------|-------------|--------------|
| `hero-banner.liquid` | Simple hero banner with heading/subtext | Accessibility, responsive, schema-ready |
| `hero-richtext-cta.liquid` | Feature-rich hero with rich text and CTA | Blocks support, background colors, alignment |
| `testimonial-carousel.liquid` | Customer testimonials carousel | Multiple testimonials, star ratings, responsive |
| `faq-accordion.liquid` | Collapsible FAQ section | Accessible accordion, rich text answers |
| `product-grid-paginate.liquid` | Product grid with pagination | Collection integration, responsive grid |

## Usage

Each section includes:
- Complete Liquid template with proper HTML structure
- JSON schema for theme customization
- CSS scoping using unique block IDs
- WCAG 2.1 AA accessibility compliance
- Responsive design patterns

## CSS Scoping Methodology

All sections use unique ID generation to prevent style collisions:

```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
```

Apply scoped styles:
```css
.section-name-{{ unique }} {
  /* Your styles here */
}
```

## Schema Patterns

Sections follow Shopify's schema conventions:
- Setting validation and proper types
- Block configurations for dynamic content
- Preset templates for quick setup
- Professional naming and descriptions

For implementation guidance, see [03-sections-and-schema.md](../../03-sections-and-schema.md).