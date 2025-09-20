# Shopify Liquid Development Guide

**The complete reference for building production-ready Shopify sections, blocks, and CSS patterns.**

This unified guide combines the best practices, code examples, and CSS methodologies for modern Shopify theme development. Perfect for developers who need both conceptual understanding and copy-paste ready code.

## Quick Navigation

### 📚 Learning Path (Start Here)
1. **[Fundamentals](./01-fundamentals.md)** - Liquid syntax, objects, and core concepts
2. **[Quick Start](./02-quick-start.md)** - Build your first section in 6 steps
3. **[Sections & Schema](./03-sections-and-schema.md)** - Section creation and configuration
4. **[Blocks & CSS Scoping](./04-blocks-and-css-scoping.md)** - Reusable blocks with isolated CSS
5. **[Performance & Accessibility](./05-performance-and-accessibility.md)** - Best practices and optimization
6. **[Troubleshooting](./06-troubleshooting.md)** - Common issues and solutions

### 🔍 Schema Validation
- **[Schema Guidelines](./schema-validation/schema-guidelines.md)** - Comprehensive validation rules and error prevention

### 🔧 Code Library (Copy & Paste Ready)
- **[Sections](./code-library/sections/)** - Complete section templates
- **[Blocks](./code-library/blocks/)** - Reusable block components
- **[Snippets](./code-library/snippets/)** - Utility components
- **[CSS Patterns](./code-library/css-patterns/)** - Styling methodologies
- **[Schema Validation](./schema-validation/)** - Validation guidelines and error prevention

### 💡 Working Examples
- **[Complete Implementations](./examples/)** - Full page layouts and JSON templates

### 📚 Comprehensive Documentation (All File Types)
- **[Complete Shopify Architecture Guide](./docs/)** - Exhaustive coverage of all 7 Shopify file types
  - **[Layouts Guide](./docs/layouts/)** - Theme foundation, required objects, HTML structure
  - **[Templates Guide](./docs/templates/)** - All template types, JSON vs Liquid, metaobjects
  - **[Assets Guide](./docs/assets/)** - Resource optimization, CDN delivery, performance
  - **[Config Guide](./docs/config/)** - Settings schema, configuration management
  - **[Locales Guide](./docs/locales/)** - Internationalization, translations, multi-language
  - **[Section Groups Guide](./docs/section-groups/)** - Online Store 2.0 dynamic layouts

### 📋 Repository Reference
- **[Complete File Structure](../STRUCTURE.md)** - Detailed file tree and navigation guide
- **[AI Assistant Project Guide](../.claude/project-guide.md)** - Comprehensive development workflows for Claude agents

## What Makes This Guide Different

### Complete Shopify Theme Coverage
This guide provides **comprehensive coverage of all 7 Shopify theme file types** - the only resource that covers the complete architecture:

- **Layouts** (`layout/`) - Theme foundation and HTML structure
- **Templates** (`templates/`) - Page-specific content and routing
- **Sections** (`sections/`) - Modular content components
- **Blocks** (`blocks/`) - Reusable content elements
- **Assets** (`assets/`) - Resources, styles, scripts, and media
- **Config** (`config/`) - Settings, schema, and configuration
- **Locales** (`locales/`) - Translations and internationalization

Plus **advanced features** like section groups, metaobject templates, and Online Store 2.0 patterns.

### Production-Ready Code
Every example is tested, follows Shopify best practices, and can be used immediately in production themes.

### CSS-First Approach
- **Scoped CSS methodology** - No style collisions between blocks
- **Responsive patterns** - Mobile-first, accessible designs
- **Performance optimized** - Minimal CSS footprint with maximum flexibility

### Developer Experience
- **Single source of truth** - No conflicting information
- **Progressive learning** - From basics to advanced patterns
- **Real-world examples** - Not just toy implementations

## Key Concepts

Think of Shopify sections like **smart building blocks**:

- **Section** = The container (hero banner, testimonials, product grid)
- **Blocks** = The content inside (individual slides, testimonial cards, products)
- **CSS Scoping** = Unique styles per block instance (no conflicts)
- **Schema** = The blueprint that defines settings and behavior

It's like having a **modular component system** where merchants can:
- Add/remove sections with the theme editor
- Customize content and styling without code
- Rearrange blocks within sections
- Get consistent, professional results

## CSS Methodology Highlights

This guide uses a **block-scoped CSS pattern** that ensures style isolation:

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .component-{{ unique }} { /* base styles */ }
  .component__element-{{ unique }} { /* element styles */ }
  @media (max-width: 749px) {
    .component-{{ unique }} { /* responsive styles */ }
  }
{% endstyle %}

<div class="component-{{ unique }}" {{ block.shopify_attributes }}>
  <!-- markup here -->
</div>
```

**Benefits:**
- ✅ **No style collisions** - Each block instance has unique CSS
- ✅ **Repeatable components** - Same block type can appear multiple times
- ✅ **Theme editor friendly** - Visual editing works perfectly
- ✅ **Maintainable** - Clear naming and organization

## Getting Started

### For Beginners
Start with **[Fundamentals](./01-fundamentals.md)** to learn Liquid basics, then follow the **[Quick Start](./02-quick-start.md)** guide.

### For Experienced Developers
Jump to **[Blocks & CSS Scoping](./04-blocks-and-css-scoping.md)** for advanced patterns, or browse the **[Code Library](./code-library/)** for immediate solutions.

### For CSS Developers
Focus on **[CSS Patterns](./code-library/css-patterns/)** and the scoping methodology in **[Blocks & CSS Scoping](./04-blocks-and-css-scoping.md)**.

## Code Standards

All code in this guide follows these standards:

### Liquid Best Practices
- Always escape user input: `{{ text | escape }}`
- Guard optional settings: `{% if setting != blank %}`
- Use semantic HTML and ARIA labels
- Optimize images with responsive sizing

### Schema Validation Requirements
- Follow the comprehensive **[Schema Guidelines](./schema-validation/schema-guidelines.md)**
- Validate all JSON syntax before deployment
- Use correct setting types and ranges
- Implement proper range step calculations: `(max - min) / step ≤ 101`
- Avoid invalid attributes like `enabled_on` in sections

### CSS Standards
- Mobile-first responsive design
- BEM naming with unique suffixes
- Minimal specificity and !important usage
- Accessibility-first focus management

### Performance Requirements
- Lazy load images below the fold
- Use `image_url` with appropriate sizing
- Keep JavaScript minimal and progressive
- Follow Theme Store performance guidelines

## Documentation Philosophy

This guide prioritizes:
1. **Practical utility** over theoretical completeness
2. **Working examples** over abstract explanations
3. **Production quality** over quick demos
4. **Clear patterns** over one-off solutions

## Support & Contribution

Found an issue or want to improve something? This documentation is designed to evolve with the Shopify platform and community best practices.

---

**Ready to build amazing Shopify sections?** Start with [Fundamentals](./01-fundamentals.md) or jump to the [Code Library](./code-library/) for immediate solutions.