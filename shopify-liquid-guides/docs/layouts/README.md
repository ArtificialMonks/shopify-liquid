# Shopify Liquid Layouts Documentation

Layout files define the base HTML structure for your Shopify theme, providing the foundation that all other templates build upon. This documentation covers everything you need to know about creating, optimizing, and maintaining layout files.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[theme-liquid.md](./theme-liquid.md)** | Main layout file | Required objects, HTML structure, best practices |
| **[checkout-liquid.md](./checkout-liquid.md)** | Shopify Plus checkout | Checkout-specific objects, customization patterns |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working code samples | Complete layout examples, patterns, and templates |

## 🎯 Quick Start

### For Beginners
1. Start with **[theme-liquid.md](./theme-liquid.md)** to understand the basic structure
2. Review the **[examples/](./examples/)** for practical implementations
3. Reference **[checkout-liquid.md](./checkout-liquid.md)** if working with Shopify Plus

### For Experienced Developers
- Jump to **[examples/](./examples/)** for advanced patterns
- Reference specific files for implementation details
- Use as a reference while building custom layouts

## 🏗️ Layout Architecture Overview

### Required Files
Every Shopify theme must include:
- **`layout/theme.liquid`** - Base layout for all pages (required)
- **`layout/checkout.liquid`** - Checkout layout (Shopify Plus only)

### Key Concepts

#### Essential Liquid Objects
All layouts must include these required objects:
- `{{ content_for_header }}` - Shopify's required scripts and metadata
- `{{ content_for_layout }}` - Dynamic content area for templates

#### Section Integration
Modern layouts use section groups for dynamic areas:
```liquid
{% sections 'header-group' %}
{{ content_for_layout }}
{% sections 'footer-group' %}
```

#### Template Context
Access template information for styling and logic:
```liquid
<body class="template-{{ template.name }}{% if template.suffix %} template-{{ template.name }}-{{ template.suffix }}{% endif %}">
```

## 🚀 Common Patterns

### Basic Layout Structure
```liquid
<!DOCTYPE html>
<html lang="{{ shop.locale }}" dir="{{ localization.direction }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page_title }}</title>
  {{ content_for_header }}
</head>
<body class="template-{{ template.name }}">
  {% sections 'header-group' %}
  <main id="main-content" tabindex="-1">
    {{ content_for_layout }}
  </main>
  {% sections 'footer-group' %}
</body>
</html>
```

### Performance Optimization
```liquid
<!-- Critical CSS inline -->
<style>
  {{ 'critical.css' | asset_url | asset }}
</style>

<!-- Preload key resources -->
{{ 'theme.js' | asset_url | preload_tag: as: 'script' }}

<!-- Async non-critical CSS -->
{{ 'theme.css' | asset_url | stylesheet_tag: media: 'print', onload: "this.media='all'" }}
<noscript>{{ 'theme.css' | asset_url | stylesheet_tag }}</noscript>
```

### Accessibility Foundation
```liquid
<!-- Skip navigation -->
<a class="skip-link" href="#main-content">{{ 'accessibility.skip_to_content' | t }}</a>

<!-- Semantic structure -->
<main id="main-content" tabindex="-1" role="main">
  {{ content_for_layout }}
</main>
```

## 📊 Layout Best Practices

### 1. Performance First
- **Inline critical CSS** for above-the-fold content
- **Preload essential resources** with `preload_tag`
- **Defer non-critical JavaScript** with async/defer
- **Optimize fonts** with `font-display: swap`

### 2. Accessibility Standards
- **Semantic HTML structure** with proper landmarks
- **Skip navigation links** for keyboard users
- **Proper heading hierarchy** starting with h1
- **Focus management** for interactive elements

### 3. Mobile Optimization
- **Responsive viewport** meta tag
- **Touch-friendly** minimum target sizes (44px)
- **Mobile-first** CSS approach
- **Progressive enhancement** patterns

### 4. SEO Foundation
- **Structured data** implementation
- **Open Graph** and Twitter Card meta tags
- **Canonical URLs** for duplicate content
- **Proper title** and meta description structure

## 🔧 Advanced Patterns

### Conditional Layout Loading
Use different layouts based on template or conditions:
```liquid
<!-- In template files -->
{% layout 'custom-layout' %}

<!-- Conditional in layout -->
{% if template.name == 'product' %}
  <!-- Product-specific layout elements -->
{% endif %}
```

### Dynamic Asset Loading
Load assets conditionally based on template:
```liquid
{% case template.name %}
  {% when 'product' %}
    {{ 'product.css' | asset_url | stylesheet_tag }}
  {% when 'collection' %}
    {{ 'collection.css' | asset_url | stylesheet_tag }}
{% endcase %}
```

### Multi-Language Support
Handle internationalization in layouts:
```liquid
<html lang="{{ request.locale.iso_code }}" dir="{{ localization.direction }}">
<head>
  <!-- Hreflang links for SEO -->
  {% for locale in localization.available_locales %}
    <link rel="alternate" hreflang="{{ locale.iso_code }}" href="{{ request.url | localization_url: locale.iso_code }}">
  {% endfor %}
</head>
```

## 🛟 Common Issues & Solutions

### Missing Required Objects
**Problem**: Theme won't save without required objects
**Solution**: Always include `{{ content_for_header }}` and `{{ content_for_layout }}`

### Style Conflicts
**Problem**: CSS bleeding between templates
**Solution**: Use template-specific body classes: `template-{{ template.name }}`

### Performance Issues
**Problem**: Slow page loads
**Solution**: Implement critical CSS, resource hints, and async loading

### Mobile Problems
**Problem**: Layout breaks on mobile
**Solution**: Use mobile-first responsive design with proper viewport meta tag

## 📚 Related Documentation

- **[Architecture Overview](../architecture/theme-overview.md)** - Complete theme structure
- **[Templates Guide](../templates/)** - How templates work with layouts
- **[Assets Guide](../assets/)** - Resource optimization for layouts
- **[Best Practices](../architecture/best-practices-2025.md)** - 2025 development standards

---

This documentation provides comprehensive guidance for creating robust, performant, and accessible layout files that serve as the foundation for exceptional Shopify themes.