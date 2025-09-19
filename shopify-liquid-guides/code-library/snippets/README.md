# Snippets

Utility Shopify Liquid snippets for common functionality and reusable components.

## Available Snippets

| Snippet | Description | Parameters |
|---------|-------------|------------|
| `responsive-image.liquid` | Responsive image with lazy loading | `image`, `alt`, `sizes`, `class` |
| `metafield-render.liquid` | Safe metafield rendering with fallbacks | `object`, `namespace`, `key`, `fallback` |

## Snippet Usage

### Responsive Image

Renders optimized images with proper lazy loading and responsive sizing:

```liquid
{% render 'responsive-image',
   image: product.featured_image,
   alt: product.title,
   sizes: '(min-width: 768px) 50vw, 100vw',
   class: 'product-image' %}
```

### Metafield Rendering

Safely renders metafields with proper fallbacks:

```liquid
{% render 'metafield-render',
   object: product,
   namespace: 'custom',
   key: 'description',
   fallback: 'No custom description available' %}
```

## Design Principles

All snippets follow these principles:
- **Parameter Validation**: Check for required parameters
- **Graceful Degradation**: Handle missing data elegantly
- **Performance Optimized**: Minimal rendering overhead
- **Accessibility Ready**: Proper ARIA labels and semantic HTML

## Integration

Snippets are designed to work seamlessly with:
- Section templates
- Block templates
- Product and collection pages
- Theme customization settings

For implementation examples, see the main guide sections and [code-library examples](../README.md).