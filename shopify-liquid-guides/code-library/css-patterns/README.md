# CSS Patterns

Production-ready CSS patterns and methodologies for Shopify Liquid development.

## Available Patterns

| Pattern | Description | Purpose |
|---------|-------------|---------|
| `scoped-blocks.css` | CSS scoping methodology for blocks | Prevent style collisions |
| `responsive-grid.css` | Responsive grid system patterns | Mobile-first layouts |
| `accessibility.css` | Accessibility-focused CSS patterns | WCAG 2.1 AA compliance |

## CSS Scoping Methodology

### The Problem
In Shopify themes, multiple sections and blocks can cause CSS conflicts when using generic class names.

### The Solution
Use unique IDs generated from Shopify's section and block IDs:

```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
```

### Implementation Pattern

```css
/* Traditional approach - prone to conflicts */
.hero-banner { /* styles */ }

/* Scoped approach - conflict-free */
.hero-banner-{{ unique }} { /* styles */ }
```

## Responsive Grid System

Mobile-first CSS Grid patterns optimized for Shopify themes:

```css
.product-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## Accessibility Patterns

WCAG 2.1 AA compliant CSS patterns:

- **Color Contrast**: Minimum 4.5:1 ratio for normal text
- **Focus Indicators**: Visible focus states for keyboard navigation
- **Screen Reader Support**: Proper hiding and showing of content
- **Reduced Motion**: Respects `prefers-reduced-motion` preference

## Integration with Liquid

CSS patterns are designed to work with:
- Section schema settings for color customization
- Block configurations for layout options
- Responsive breakpoints aligned with Shopify's image sizing
- Theme Store performance requirements

For implementation guidance, see [04-blocks-and-css-scoping.md](../../04-blocks-and-css-scoping.md) and [05-performance-and-accessibility.md](../../05-performance-and-accessibility.md).