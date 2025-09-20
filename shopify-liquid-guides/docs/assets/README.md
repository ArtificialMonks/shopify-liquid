# Shopify Assets Documentation

Assets are static files that support your theme's functionality - CSS, JavaScript, images, fonts, and other media. This documentation covers modern asset management, optimization strategies, and performance best practices for Shopify themes.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[css-assets.md](./css-assets.md)** | CSS organization and optimization | Styling strategies, preprocessing, performance |
| **[javascript-assets.md](./javascript-assets.md)** | JavaScript patterns | Modern JS, bundle optimization, async loading |
| **[image-assets.md](./image-assets.md)** | Image optimization | Responsive images, lazy loading, format selection |
| **[font-assets.md](./font-assets.md)** | Typography management | Web fonts, loading strategies, performance |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working asset configurations | Complete asset files, optimization examples |

## 🎯 Quick Start

### For Beginners
1. Start with **[css-assets.md](./css-assets.md)** to understand CSS organization
2. Review **[image-assets.md](./image-assets.md)** for responsive image patterns
3. Study **[examples/](./examples/)** for practical implementations

### For Experienced Developers
- Jump to **[javascript-assets.md](./javascript-assets.md)** for modern JS patterns
- Browse **[font-assets.md](./font-assets.md)** for typography optimization
- Reference **[examples/](./examples/)** for production-ready code

## 📊 Asset Types Overview

### CSS Assets
Styling and visual presentation:
- **`theme.css`** - Main stylesheet (Liquid preprocessing)
- **`section-*.css`** - Section-specific styles
- **`component.css`** - Reusable component styles
- **`critical.css`** - Above-the-fold critical CSS

### JavaScript Assets
Interactivity and dynamic behavior:
- **`theme.js`** - Main theme functionality
- **`section-*.js`** - Section-specific scripts
- **`vendor/`** - Third-party libraries
- **`modules/`** - ES6 modules for organization

### Image Assets
Visual content and media:
- **Product images** - High-quality product photos
- **Hero images** - Banner and promotional imagery
- **Icons** - SVG icons and UI elements
- **Placeholders** - Default images for missing content

### Font Assets
Typography resources:
- **Web fonts** - Custom typography files (WOFF2, WOFF)
- **Icon fonts** - Font-based icon systems
- **System fonts** - CSS font stack definitions

## 🚀 Asset Architecture Patterns

### CSS Organization
```css
/* theme.css.liquid - Main stylesheet */
@import url('critical.css');
@import url('layout.css');
@import url('components.css');
@import url('sections.css');
@import url('utilities.css');
```

### JavaScript Module Structure
```javascript
// theme.js - Main entry point
import { CartDrawer } from './modules/cart-drawer.js';
import { ProductForm } from './modules/product-form.js';
import { SearchOverlay } from './modules/search-overlay.js';

// Initialize theme functionality
document.addEventListener('DOMContentLoaded', () => {
  new CartDrawer();
  new ProductForm();
  new SearchOverlay();
});
```

### Responsive Image Patterns
```liquid
<!-- Responsive image with lazy loading -->
<img src="{{ image | image_url: width: 400 }}"
     srcset="{{ image | image_url: width: 400 }} 400w,
             {{ image | image_url: width: 800 }} 800w,
             {{ image | image_url: width: 1200 }} 1200w"
     sizes="(max-width: 749px) 100vw, 50vw"
     loading="lazy"
     alt="{{ image.alt | escape }}">
```

## 🎨 Asset Optimization Strategies

### Performance Priority
1. **Critical CSS** - Inline above-the-fold styles
2. **Lazy loading** - Defer below-the-fold assets
3. **Bundle optimization** - Minimize HTTP requests
4. **Compression** - Enable gzip/brotli compression
5. **Caching** - Leverage browser and CDN caching

### Modern Asset Pipeline
- **CSS preprocessing** - Use Liquid for dynamic values
- **JavaScript bundling** - Combine modules efficiently
- **Image optimization** - WebP format with fallbacks
- **Font optimization** - WOFF2 with system font fallbacks

### Loading Strategies
```html
<!-- Critical CSS inline -->
<style>{{ 'critical.css' | asset_url | asset_content }}</style>

<!-- Non-critical CSS async -->
<link rel="preload" href="{{ 'theme.css' | asset_url }}" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- JavaScript with proper defer -->
<script src="{{ 'theme.js' | asset_url }}" defer></script>
```

## 🔧 Development Workflow

### 1. Asset Organization
- Group assets by functionality and type
- Use consistent naming conventions
- Implement modular architecture
- Maintain separation of concerns

### 2. Optimization Process
- Compress images before upload
- Minify CSS and JavaScript
- Implement lazy loading patterns
- Test performance impact

### 3. Performance Monitoring
- Use Core Web Vitals metrics
- Monitor asset loading times
- Test on various devices
- Optimize based on analytics

## 🚨 Common Pitfalls

### 1. Large Asset Sizes
**Problem**: Slow loading due to unoptimized assets
**Solution**: Implement compression and optimization workflows

### 2. Render-Blocking Resources
**Problem**: CSS/JS blocking page rendering
**Solution**: Use async loading and critical CSS patterns

### 3. Too Many HTTP Requests
**Problem**: Multiple small assets causing latency
**Solution**: Bundle related assets and use sprite sheets

### 4. Missing Fallbacks
**Problem**: Modern formats without legacy support
**Solution**: Progressive enhancement with fallback assets

## 📊 Best Practices

### 1. File Organization
- **Logical grouping** - Group related assets together
- **Clear naming** - Use descriptive, consistent names
- **Version control** - Track asset changes properly

### 2. Performance Standards
- **Image optimization** - Always compress and resize appropriately
- **CSS efficiency** - Remove unused styles, use shorthand
- **JavaScript minimization** - Bundle and minify production code

### 3. Accessibility Compliance
- **Alt text** - Provide meaningful image descriptions
- **Focus indicators** - Maintain visible focus states
- **Color contrast** - Ensure sufficient contrast ratios

---

Assets are the foundation of theme performance and user experience. Proper asset management directly impacts Core Web Vitals, conversion rates, and merchant success on Shopify.
