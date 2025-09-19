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

### 🔧 Code Library (Copy & Paste Ready)
- **[Sections](./code-library/sections/)** - Complete section templates
- **[Blocks](./code-library/blocks/)** - Reusable block components
- **[Snippets](./code-library/snippets/)** - Utility components
- **[CSS Patterns](./code-library/css-patterns/)** - Styling methodologies

### 💡 Working Examples
- **[Complete Implementations](./examples/)** - Full page layouts and JSON templates

### 📋 Repository Reference
- **[Complete File Structure](../STRUCTURE.md)** - Detailed file tree and navigation guide

## What Makes This Guide Different

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