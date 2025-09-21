# Custom Blocks Directory

**Custom-made Shopify Liquid block components for this repository**

## Purpose

This directory contains custom-made block components that are:
- **Repository-specific**: Built for this specific project's needs
- **Production-ready**: Fully validated and theme-store compliant  
- **Validation-compliant**: Pass all repository validation standards

## Structure

```
blocks/custom/
├── README.md                    # This documentation
├── advanced_video_text.liquid   # Advanced video + text positioning block
└── [future custom blocks]       # Additional custom components
```

## Validation Requirements

All custom blocks in this directory MUST:
- Pass `./scripts/validate-theme.sh integrity` validation
- Comply with schema guidelines (range steps ≤ 101, unique IDs, valid types)
- Follow CSS scoping methodology with `block.id` suffixes
- Include comprehensive accessibility features (WCAG 2.1 AA)
- Use only Shopify-standard setting types

## Integration

Custom blocks can be used in sections via:
```liquid
{% schema %}
{
  "blocks": [
    {"type": "@theme"}  // Accepts all theme blocks including custom ones
  ]
}
{% endschema %}
```

## Development Guidelines

When creating custom blocks:
1. Follow the patterns established in `../essential/` and `../advanced/` directories
2. Use unique CSS class scoping: `block.id | replace: '_', '' | downcase`
3. Validate with `python3 scripts/scan-schema-integrity.py [file]`
4. Include comprehensive documentation headers
5. Test across multiple viewport sizes and accessibility tools

## Reference Documentation

- **CSS Scoping**: `../../04-blocks-and-css-scoping.md`
- **Schema Guidelines**: `../../schema-validation/schema-guidelines.md`
- **Repository Rules**: `/WARP.md` and `/CLAUDE.md`