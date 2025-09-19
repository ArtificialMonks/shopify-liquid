# Shopify Liquid Sections Documentation

This comprehensive guide covers everything you need to know about building custom Shopify Liquid sections for themes, based on official Shopify documentation, real-world examples, and best practices from the community.

## Table of Contents

1. [Quick Start Guide](./01-quick-start.md) - Get up and running in 6 steps
2. [Section Schema Deep Dive](./02-section-schema.md) - Understanding section configuration
3. [Block Types & Configuration](./03-blocks.md) - Building flexible block systems
4. [Liquid Syntax for Sections](./04-liquid-syntax.md) - Template code patterns
5. [Code Examples & Patterns](./05-code-examples.md) - Real-world section examples
6. [Best Practices & Performance](./06-best-practices.md) - Do's and don'ts
7. [Theme Editor Integration](./07-theme-editor.md) - Making sections editor-friendly
8. [Liquid Object Reference](./08-liquid-reference.md) - Complete object cheatsheet
9. [Troubleshooting Guide](./09-troubleshooting.md) - Common issues and solutions
10. [Advanced Techniques](./10-advanced.md) - Pro tips and advanced patterns

## What You'll Learn

By following this documentation, you'll be able to:

- **Create custom sections** that merchants can add, remove, and configure
- **Build flexible block systems** for dynamic content
- **Write clean, performant Liquid code** following best practices
- **Integrate with the theme editor** for the best merchant experience
- **Debug and troubleshoot** section issues effectively
- **Optimize for performance** and SEO

## Research Sources

This documentation is compiled from:

- ✅ **Official Shopify Dev Documentation** - Latest guidelines and APIs
- ✅ **Shopify Liquid Code Examples** - Real production patterns
- ✅ **Context7 Documentation** - In-depth Liquid syntax reference
- ✅ **GitHub Code Samples** - Community examples and gists
- ✅ **Performance Best Practices** - Theme Store requirements

## File Structure

Each documentation file is self-contained but builds upon previous concepts:

```
docs/shopify-liquid/
├── README.md                    # This overview file
├── 01-quick-start.md           # 6-step implementation guide
├── 02-section-schema.md        # Schema definitions and settings
├── 03-blocks.md                # Block types and configuration
├── 04-liquid-syntax.md         # Template syntax patterns
├── 05-code-examples.md         # Working examples with code
├── 06-best-practices.md        # Performance and guidelines
├── 07-theme-editor.md          # Editor integration
├── 08-liquid-reference.md      # Complete object reference
├── 09-troubleshooting.md       # Common problems and fixes
└── 10-advanced.md              # Advanced techniques
```

## Getting Started

If you're new to Shopify sections, start with the [Quick Start Guide](./01-quick-start.md) to build your first custom section in 6 steps.

If you're experienced with Liquid but new to sections, jump to [Section Schema Deep Dive](./02-section-schema.md) to understand the configuration system.

If you want to see working examples right away, check out [Code Examples & Patterns](./05-code-examples.md).

## Key Concepts

Think of Shopify sections like **modular building blocks** for themes:

- **Section** = The container (like a hero banner, product grid, or testimonials)
- **Blocks** = The content inside (individual slides, products, or testimonial cards)  
- **Settings** = The configuration options merchants can change
- **Schema** = The blueprint that defines how everything works

It's like having a **smart Lego system** where merchants can:
- Add or remove entire sections
- Customize the content within each section
- Rearrange blocks within sections
- Change colors, text, and images without touching code

Ready to dive in? Let's start building! 🚀
