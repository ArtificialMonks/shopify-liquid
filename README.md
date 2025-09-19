# Shopify Liquid Development Guide

Complete documentation and code library for professional Shopify Liquid theme development.

## 📚 What's Inside

This repository provides everything you need for Shopify theme development:

- **Complete Learning Path**: From fundamentals to advanced patterns
- **Production-Ready Code**: Copy-paste sections, blocks, and snippets
- **CSS Scoping Methodology**: Prevent style conflicts in complex themes
- **Accessibility Compliance**: WCAG 2.1 AA patterns and examples
- **VS Code Integration**: Full development environment setup

## 🚀 Quick Start

1. **Learn the Basics**: Start with [shopify-liquid-guides/](./shopify-liquid-guides/)
2. **Copy Production Code**: Browse [code-library/](./shopify-liquid-guides/code-library/)
3. **Use Complete Examples**: Implement [JSON templates](./shopify-liquid-guides/examples/)
4. **Set Up Your Editor**: Configure [VS Code extension](./shopify-liquid-guides/docs/shopify-extension/)

## 📁 Repository Structure

```
├── README.md                          # This file
├── STRUCTURE.md                       # Complete file tree documentation
├── CLAUDE.md                          # AI assistant instructions
├── .vscode/                           # VS Code workspace configuration
├── .theme-check.yml                   # Theme Check linting rules
└── shopify-liquid-guides/             # Main documentation
    ├── 01-fundamentals.md             # Liquid syntax and basics
    ├── 02-quick-start.md              # Implementation walkthrough
    ├── 03-sections-and-schema.md      # Section development
    ├── 04-blocks-and-css-scoping.md   # CSS methodology
    ├── 05-performance-and-accessibility.md # Optimization
    ├── 06-troubleshooting.md          # Common issues
    ├── code-library/                  # Production-ready code
    ├── examples/                      # Complete JSON templates
    └── docs/                          # Tool documentation
```

See [STRUCTURE.md](./STRUCTURE.md) for complete file tree.

## 🎯 Key Features

### CSS Scoping Methodology
Prevent style conflicts using unique section/block IDs:

```liquid
{% assign unique = section.id | replace: '_', '' | downcase %}
<div class="hero-banner-{{ unique }}">
```

### Production-Ready Templates
Complete sections with schema, accessibility, and responsive design:

- Hero banners with rich text and CTAs
- Product grids with filtering
- Testimonial carousels
- FAQ accordions
- And more...

### VS Code Integration
Optimized development environment with:
- Intelligent code completion
- Real-time error detection
- Auto-formatting on save
- Theme Check integration

## 🛠 Development Setup

This repository is pre-configured for optimal Shopify development:

1. **VS Code Settings**: `.vscode/settings.json` with Shopify Liquid extension configuration
2. **Theme Check**: `.theme-check.yml` with documentation-optimized rules
3. **File Associations**: Proper Liquid syntax highlighting
4. **Extension Recommendations**: Essential VS Code extensions

## 📖 Learning Path

Follow this progression for mastery:

1. **[Fundamentals](./shopify-liquid-guides/01-fundamentals.md)** - Liquid syntax, objects, filters
2. **[Quick Start](./shopify-liquid-guides/02-quick-start.md)** - Build your first section
3. **[Sections & Schema](./shopify-liquid-guides/03-sections-and-schema.md)** - Advanced configurations
4. **[CSS Scoping](./shopify-liquid-guides/04-blocks-and-css-scoping.md)** - Prevent style conflicts
5. **[Performance](./shopify-liquid-guides/05-performance-and-accessibility.md)** - Optimization & accessibility
6. **[Troubleshooting](./shopify-liquid-guides/06-troubleshooting.md)** - Debug common issues

## 🤝 Philosophy

This guide follows a **CSS-first, production-ready** approach:

- Every example is copy-paste ready for real themes
- CSS scoping prevents style conflicts
- Accessibility is built-in, not an afterthought
- Performance optimization is standard practice
- Schema configurations follow Shopify best practices

## 🔗 External Resources

- [Shopify Liquid Reference](https://shopify.dev/api/liquid)
- [Theme Store Requirements](https://shopify.dev/themes/store/requirements)
- [Shopify CLI](https://shopify.dev/themes/tools/cli)
- [Theme Check](https://shopify.dev/themes/tools/theme-check)

## 📝 Contributing

This is a living documentation project. To contribute:

1. Follow the established patterns and methodology
2. Ensure all code examples are production-ready
3. Include accessibility considerations
4. Test with the VS Code extension configuration
5. Update relevant README files

---

**Start your Shopify development journey**: Begin with [shopify-liquid-guides/README.md](./shopify-liquid-guides/README.md)