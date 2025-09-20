# Asset Examples

This directory contains practical examples of optimized asset implementations for Shopify themes. Each example demonstrates best practices for performance, accessibility, and maintainability.

## 📁 Available Examples

### CSS Examples
- **[critical-css.css](./critical-css.css)** - Above-the-fold critical styles for fast rendering
- **[component-scoped.css](./component-scoped.css)** - Scoped CSS patterns to prevent style conflicts
- **[responsive-utilities.css](./responsive-utilities.css)** - Utility classes for responsive design

### JavaScript Examples
- **[theme-core.js](./theme-core.js)** - Minimal theme initialization with lazy loading
- **[section-scripts.js](./section-scripts.js)** - Section-specific JavaScript patterns
- **[performance-optimized.js](./performance-optimized.js)** - Performance-focused JS implementation

### Image Examples
- **[responsive-images.liquid](./responsive-images.liquid)** - Complete responsive image implementations
- **[lazy-loading.liquid](./lazy-loading.liquid)** - Advanced lazy loading patterns
- **[webp-fallbacks.liquid](./webp-fallbacks.liquid)** - WebP implementation with fallbacks

### Font Examples
- **[font-loading.liquid](./font-loading.liquid)** - Optimized font loading strategies
- **[variable-fonts.css](./variable-fonts.css)** - Variable font implementation
- **[system-fonts.css](./system-fonts.css)** - System font stacks for performance

## 🎯 Usage Guidelines

### Copy-Paste Ready
All examples are production-ready and can be copied directly into your theme:

1. **CSS files** → Copy to `assets/` directory
2. **JavaScript files** → Copy to `assets/` directory
3. **Liquid files** → Copy patterns into your templates/sections
4. **Configuration** → Adapt settings to your theme's schema

### Integration Steps
1. Review the example code and comments
2. Adapt variable names and selectors to match your theme
3. Test thoroughly across different devices and browsers
4. Validate with Theme Check for Shopify compliance

### Performance Considerations
- All examples prioritize Core Web Vitals optimization
- JavaScript examples stay under the 16KB recommendation
- CSS examples use efficient selectors and modern features
- Image examples implement proper responsive and lazy loading

---

These examples represent current best practices for Shopify theme asset optimization as of 2024-2025.