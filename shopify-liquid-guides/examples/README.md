# Examples

Complete JSON template examples demonstrating real-world Shopify theme implementations.

## Available Examples

| Template | Description | Sections Included |
|----------|-------------|-------------------|
| `complete-homepage.json` | Full homepage layout | Hero, products, testimonials, FAQ, newsletter |
| `product-page-sections.json` | Product page with enhanced features | Product details, recommendations, reviews, shipping info |
| `collection-layout.json` | Collection page with filtering | Banner, product grid, features, related collections, FAQ |

## Template Structure

Each JSON template includes:
- **Section Configuration**: Complete settings and block definitions
- **Section Order**: Logical flow for user experience
- **Real Content Examples**: Actual copy and configuration values
- **Responsive Settings**: Mobile and desktop optimized layouts

## Usage

### Direct Implementation
Copy JSON templates directly to your theme's `templates/` directory:

```bash
cp complete-homepage.json themes/your-theme/templates/index.json
```

### Section Extraction
Extract individual sections for reuse:

```json
{
  "sections": {
    "hero": {
      "type": "hero-richtext-cta",
      "settings": {
        // Extract this section configuration
      }
    }
  }
}
```

### Customization Base
Use as starting point for custom layouts:
1. Copy template JSON
2. Modify section settings
3. Adjust section order
4. Add/remove sections as needed

## Content Strategy

Templates demonstrate:
- **Progressive Disclosure**: Important content first, details below
- **Social Proof**: Customer testimonials and reviews
- **Conversion Optimization**: Strategic CTA placement
- **Accessibility**: Proper heading hierarchy and semantic structure

## Integration

Templates work with sections from:
- [code-library/sections/](../code-library/sections/) - Section templates
- [code-library/blocks/](../code-library/blocks/) - Block components
- [code-library/snippets/](../code-library/snippets/) - Utility functions

For implementation guidance, see [02-quick-start.md](../02-quick-start.md) and [03-sections-and-schema.md](../03-sections-and-schema.md).