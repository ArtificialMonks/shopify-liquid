# Custom Sections Directory

**Custom-made Shopify Liquid section components for this repository**

## Purpose

This directory contains custom-made section components that are:
- **Repository-specific**: Built for this specific project's needs
- **Production-ready**: Fully validated and theme-store compliant  
- **Integration-focused**: Host sections that work with custom and theme blocks

## Structure

```
sections/custom/
├── README.md                           # This documentation
├── example-video-text-collection.liquid  # Example section using advanced video+text blocks
└── [future custom sections]            # Additional custom section templates
```

## Validation Requirements

All custom sections in this directory MUST:
- Pass `./scripts/validate-theme.sh development` validation
- Comply with schema guidelines (range steps ≤ 101, unique IDs, valid types)
- Follow CSS scoping methodology with `section.id` suffixes
- Include proper block integration patterns
- Use semantic HTML and accessibility features

## Integration Patterns

### Accepting Theme Blocks
```liquid
{% schema %}
{
  "blocks": [
    {"type": "@theme"}  // Accepts ALL theme blocks (essential, advanced, custom)
  ]
}
{% endschema %}
```

### Accepting Specific Blocks
```liquid
{% schema %}
{
  "blocks": [
    {"type": "advanced_video_text"},
    {"type": "text"},
    {"type": "image"}
  ]
}
{% endschema %}
```

### Rendering Blocks
```liquid
{% for block in section.blocks %}
  {% case block.type %}
    {% when 'advanced_video_text' %}
      {% render 'block-video-text', block: block, section: section %}
    {% else %}
      {% content_for 'blocks' %}  // Renders theme blocks directly
  {% endcase %}
{% endfor %}
```

## Development Guidelines

When creating custom sections:
1. Use section-level settings for container behavior (max-width, padding, background)
2. Delegate content to blocks for maximum flexibility
3. Apply consistent spacing systems between blocks
4. Include responsive design considerations
5. Test with various block combinations

## Reference Documentation

- **Section Architecture**: `../../docs/architecture/theme-overview.md`
- **Block Integration**: `../../04-blocks-and-css-scoping.md`  
- **Schema Guidelines**: `../../schema-validation/schema-guidelines.md`