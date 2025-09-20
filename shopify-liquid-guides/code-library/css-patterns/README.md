# CSS Patterns

Production-ready CSS patterns and methodologies for Shopify Liquid development.

## Available Patterns

| Pattern | Description | Purpose |
|---------|-------------|---------|
| `scoped-blocks.css` | CSS scoping methodology for blocks | Prevent style collisions |
| `responsive-grid.css` | Responsive grid system patterns | Mobile-first layouts |
| `accessibility.css` | Accessibility-focused CSS patterns | WCAG 2.1 AA compliance |
| `performance-optimization.css` | Core Web Vitals optimization patterns | Theme Store performance requirements |

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

## Implementation References

### Critical Guidelines
- **[Schema Validation](../../schema-validation/schema-guidelines.md)** - **ESSENTIAL: Validate all schema configurations**
- **[CSS Scoping Guide](../../04-blocks-and-css-scoping.md)** - Complete scoping methodology
- **[Performance & Accessibility](../../05-performance-and-accessibility.md)** - Production optimization

### Asset Management
- **[CSS Assets Documentation](../../docs/assets/css-assets.md)** - Styling organization and optimization
- **[Asset Optimization](../../docs/assets/)** - Complete asset management strategy
- **[Advanced Performance](../../docs/advanced-features/advanced-performance.md)** - Cutting-edge optimization

### Architecture Integration
- **[Theme Architecture](../../docs/architecture/theme-overview.md)** - How CSS fits in theme structure
- **[Best Practices 2025](../../docs/architecture/best-practices-2025.md)** - Current CSS standards
- **[Block Configuration](../../docs/config/blocks-config.md)** - Schema patterns for styled components