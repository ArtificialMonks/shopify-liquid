# Shopify Theme Best Practices 2025

Comprehensive best practices for Shopify theme development in 2025, covering performance, accessibility, maintainability, and Theme Store compliance.

## 🚀 Performance Best Practices

### Core Web Vitals Optimization

#### Largest Contentful Paint (LCP) < 2.5s
- **Optimize images**: Use `image_url` with appropriate sizing
- **Critical CSS**: Inline above-the-fold styles
- **Font loading**: Preload critical fonts with `font-display: swap`
- **Resource hints**: Use `preload_tag` for critical assets

```liquid
<!-- Critical font preloading -->
{{ 'theme-font.woff2' | asset_url | preload_tag: as: 'font', type: 'font/woff2', crossorigin: 'anonymous' }}

<!-- Optimized image loading -->
{{ product.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', sizes: '(min-width: 750px) 50vw, 100vw' }}
```

#### First Input Delay (FID) < 100ms
- **Defer non-critical JS**: Use `defer` or `async` attributes
- **Minimize JavaScript**: Keep bundles under 16KB minified
- **Progressive enhancement**: Build with HTML/CSS first

```liquid
<!-- Deferred JavaScript loading -->
{{ 'theme.js' | asset_url | script_tag: defer: true }}

<!-- Module loading for modern browsers -->
<script type="module" src="{{ 'theme.module.js' | asset_url }}" defer></script>
```

#### Cumulative Layout Shift (CLS) < 0.1
- **Reserve space**: Define dimensions for dynamic content
- **Stable layouts**: Avoid layout-shifting animations
- **Font fallbacks**: Use system font stacks as fallbacks

### Asset Optimization

#### Image Strategy
```liquid
<!-- Responsive images with art direction -->
<picture>
  <source media="(min-width: 750px)"
          srcset="{{ image | image_url: width: 800 }} 800w,
                  {{ image | image_url: width: 1200 }} 1200w">
  <img src="{{ image | image_url: width: 400 }}"
       srcset="{{ image | image_url: width: 400 }} 400w,
               {{ image | image_url: width: 600 }} 600w"
       sizes="100vw"
       loading="lazy"
       alt="{{ image.alt | escape }}">
</picture>
```

#### CSS Delivery
```liquid
<!-- Critical CSS inline -->
<style>
  {{ 'critical.css' | asset_url | asset }}
</style>

<!-- Non-critical CSS async -->
{{ 'theme.css' | asset_url | stylesheet_tag: media: 'print', onload: "this.media='all'" }}
<noscript>{{ 'theme.css' | asset_url | stylesheet_tag }}</noscript>
```

---

## ♿ Accessibility Best Practices (WCAG 2.1 AA)

### Semantic HTML Structure
```liquid
<!-- Proper heading hierarchy -->
<h1>{{ page_title }}</h1>
<section aria-labelledby="products-heading">
  <h2 id="products-heading">{{ section.settings.heading | escape }}</h2>
  {% for product in collection.products %}
    <article>
      <h3>{{ product.title | escape }}</h3>
    </article>
  {% endfor %}
</section>
```

### Keyboard Navigation
```liquid
<!-- Skip links -->
<a class="skip-link" href="#main-content">{{ 'accessibility.skip_to_content' | t }}</a>

<!-- Focus management -->
<button type="button"
        aria-expanded="false"
        aria-controls="mobile-menu"
        aria-label="{{ 'sections.header.menu' | t }}">
  <span aria-hidden="true">☰</span>
</button>
```

### Screen Reader Support
```liquid
<!-- Descriptive labels -->
<input type="search"
       id="search"
       name="q"
       placeholder="{{ 'general.search.placeholder' | t }}"
       aria-label="{{ 'general.search.title' | t }}">

<!-- Status announcements -->
<div role="status" aria-live="polite" class="sr-only">
  {{ cart.item_count }} {{ 'sections.cart.items_count' | t: count: cart.item_count }}
</div>
```

### Color and Contrast
- **Minimum contrast**: 4.5:1 for normal text, 3:1 for large text
- **Color independence**: Don't rely solely on color for information
- **Focus indicators**: Visible focus states for all interactive elements

---

## 🏗️ Architecture Best Practices

### CSS Scoping Strategy
```liquid
<!-- Section-level scoping -->
{% assign section_id = section.id | replace: '_', '' | downcase %}

{% style %}
  .section-{{ section_id }} {
    /* Section-specific styles */
  }

  @media (max-width: 749px) {
    .section-{{ section_id }} {
      /* Mobile-specific styles */
    }
  }
{% endstyle %}

<div class="section-{{ section_id }}" {{ section.shopify_attributes }}>
  <!-- Section content -->
</div>
```

### Block-level Isolation
```liquid
<!-- Block-level scoping for reusability -->
{% assign block_id = block.id | replace: '_', '' | downcase %}

{% style %}
  .block-{{ block_id }} {
    padding: {{ block.settings.padding }}px;
    background: {{ block.settings.background_color }};
  }
{% endstyle %}

<div class="block-{{ block_id }}" {{ block.shopify_attributes }}>
  <!-- Block content -->
</div>
```

### Component Organization
```
sections/
├── layout/
│   ├── header.liquid
│   └── footer.liquid
├── content/
│   ├── hero-banner.liquid
│   └── text-block.liquid
├── product/
│   ├── product-grid.liquid
│   └── featured-product.liquid
└── utility/
    ├── newsletter.liquid
    └── social-links.liquid
```

---

## 🔧 Development Workflow

### Schema Best Practices

#### Setting Organization
```json
{
  "name": "Hero Banner",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Welcome to our store"
    },
    {
      "type": "header",
      "content": "Appearance"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text color",
      "default": "#000000"
    }
  ]
}
```

#### Validation Rules
- **Range validation**: Ensure `(max - min) / step ≤ 101`
- **Required defaults**: Provide defaults for all range settings
- **Clear labels**: Use descriptive, user-friendly labels
- **Helper text**: Add `info` for complex settings

### Liquid Best Practices

#### Input Sanitization
```liquid
<!-- Always escape user input -->
<h2>{{ section.settings.heading | escape }}</h2>

<!-- Use appropriate filters -->
{{ product.price | money }}
{{ article.published_at | date: format: 'month_day_year' }}
{{ settings.custom_css | strip_html | strip_newlines }}
```

#### Performance Optimization
```liquid
<!-- Limit expensive operations -->
{% assign featured_products = collections.featured.products | limit: 12 %}

<!-- Cache complex calculations -->
{% assign discount_percentage = product.compare_at_price | minus: product.price | times: 100 | divided_by: product.compare_at_price %}

<!-- Use appropriate image sizes -->
{{ product.featured_image | image_url: width: 400 | image_tag }}
```

#### Error Handling
```liquid
<!-- Guard against missing data -->
{% if product.featured_image %}
  {{ product.featured_image | image_url: width: 400 | image_tag }}
{% else %}
  <div class="product-image-placeholder" aria-label="{{ 'products.product.no_image' | t }}">
    <!-- Placeholder content -->
  </div>
{% endif %}

<!-- Provide fallbacks -->
{{ product.title | default: 'Untitled Product' | escape }}
```

---

## 📱 Mobile-First Development

### Responsive Design Principles
```css
/* Mobile-first base styles */
.component {
  display: block;
  padding: 1rem;
}

/* Progressive enhancement */
@media (min-width: 750px) {
  .component {
    display: flex;
    padding: 2rem;
  }
}

@media (min-width: 990px) {
  .component {
    padding: 3rem;
  }
}
```

### Touch-Friendly Interfaces
- **Minimum touch targets**: 44px × 44px
- **Adequate spacing**: 8px minimum between targets
- **Gesture support**: Swipe, pinch, scroll behaviors

### Performance on Mobile
- **Reduce payload**: Smaller images and compressed assets
- **Prioritize content**: Show important content first
- **Minimize interactions**: Reduce required taps and inputs

---

## 🌐 Internationalization Best Practices

### Translation Implementation
```liquid
<!-- Use translation keys -->
<button type="submit">{{ 'general.search.submit' | t }}</button>

<!-- Variable interpolation -->
{{ 'products.product.vendor_html' | t: vendor: product.vendor }}

<!-- Pluralization -->
{{ 'sections.cart.items_count' | t: count: cart.item_count }}

<!-- HTML content (use _html suffix) -->
{{ 'general.payment.security_html' | t }}
```

### Multi-Currency Support
```liquid
<!-- Currency display -->
{{ product.price | money_with_currency }}

<!-- Localized formatting -->
{{ 'now' | date: format: 'month_day_year' }}
```

### RTL Language Support
```css
/* Logical properties for RTL support */
.component {
  margin-inline-start: 1rem;
  border-inline-end: 1px solid #ccc;
  text-align: start;
}

/* Direction-specific styles */
[dir="rtl"] .component {
  /* RTL-specific adjustments */
}
```

---

## 🛡️ Security Best Practices

### Content Security
```liquid
<!-- Sanitize all outputs -->
{{ user_content | escape }}
{{ settings.custom_html | strip_html }}

<!-- Validate URLs -->
{% if settings.external_link contains 'https://' %}
  <a href="{{ settings.external_link }}" target="_blank" rel="noopener">
{% endif %}
```

### Asset Security
- **HTTPS only**: All asset URLs use HTTPS
- **Subresource Integrity**: For external scripts
- **Content Security Policy**: Restrict resource loading

---

## 🏪 Theme Store Compliance

### Performance Requirements
- **Lighthouse score**: ≥60 average across key pages
- **JavaScript bundle**: ≤16KB minified
- **Image optimization**: Appropriate sizing and formats
- **Loading performance**: Meet Core Web Vitals thresholds

### Functionality Requirements
- **Theme editor**: All settings work correctly
- **Responsive design**: Works on all devices
- **Cross-browser**: Compatible with major browsers
- **Accessibility**: WCAG 2.1 AA compliance

### Code Quality Standards
```liquid
<!-- Semantic HTML -->
<main id="main-content" tabindex="-1">
  <section aria-labelledby="page-title">
    <h1 id="page-title">{{ page_title }}</h1>
  </section>
</main>

<!-- Clean, maintainable code -->
{% comment %} Component: Product card {% endcomment %}
{% assign price_class = 'price' %}
{% if product.compare_at_price > product.price %}
  {% assign price_class = 'price price--on-sale' %}
{% endif %}

<div class="product-card">
  <h3 class="product-card__title">{{ product.title | escape }}</h3>
  <div class="{{ price_class }}">{{ product.price | money }}</div>
</div>
```

---

## 🔄 Maintenance and Updates

### Version Control
- **Git workflows**: Feature branches and pull requests
- **Theme versioning**: Semantic versioning for releases
- **Backup strategy**: Regular theme backups
- **Rollback procedures**: Quick reversion capabilities

### Performance Monitoring
- **Regular audits**: Monthly Lighthouse audits
- **User monitoring**: Real user metrics (RUM)
- **Error tracking**: JavaScript error monitoring
- **Analytics integration**: Performance tracking

### Code Reviews
- **Accessibility checks**: Screen reader testing
- **Performance validation**: Speed and optimization
- **Code quality**: Standards compliance
- **Security review**: Vulnerability assessment

### Documentation
- **Component documentation**: Usage examples and guidelines
- **Configuration guide**: Setting explanations
- **Customization notes**: Modification instructions
- **Troubleshooting**: Common issues and solutions

---

These best practices ensure themes are performant, accessible, maintainable, and compliant with Shopify's evolving standards throughout 2025 and beyond.