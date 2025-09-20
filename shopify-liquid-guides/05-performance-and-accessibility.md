# Performance & Accessibility

Master optimization techniques and accessibility standards for production-ready Shopify themes. This guide combines performance best practices with WCAG 2.1 AA compliance patterns.

## Performance Fundamentals

### Core Performance Principles

1. **Minimize HTTP Requests** - Reduce the number of external resources
2. **Optimize Images** - Use appropriate sizing and lazy loading
3. **Efficient Liquid** - Write performant template logic
4. **Scoped CSS** - Prevent style conflicts and reduce specificity
5. **Progressive Enhancement** - Build core functionality first, enhance with JavaScript

### Shopify Performance Targets

**Theme Store Requirements:**
- ✅ **Lighthouse Performance Score**: >70
- ✅ **First Contentful Paint**: <2.5s
- ✅ **Largest Contentful Paint**: <4s
- ✅ **Cumulative Layout Shift**: <0.25
- ✅ **Time to Interactive**: <7s

## Image Optimization

### Responsive Image Pattern
```liquid
{% comment %} Optimal responsive image implementation {% endcomment %}
{% if image %}
  <img
    src="{{ image | image_url: width: 800 }}"
    srcset="
      {{ image | image_url: width: 400 }} 400w,
      {{ image | image_url: width: 600 }} 600w,
      {{ image | image_url: width: 800 }} 800w,
      {{ image | image_url: width: 1000 }} 1000w,
      {{ image | image_url: width: 1200 }} 1200w
    "
    sizes="(min-width: 1200px) 800px, (min-width: 750px) 600px, 100vw"
    alt="{{ image.alt | escape }}"
    loading="lazy"
    width="{{ image.width | default: 800 }}"
    height="{{ image.height | default: 600 }}"
  >
{% endif %}
```

### Image Sizing Guidelines
```liquid
{% comment %} Choose appropriate sizes based on usage {% endcomment %}

{% comment %} Hero images - Large, above fold {% endcomment %}
{{ hero_image | image_url: width: 1200 }}

{% comment %} Product thumbnails - Small, in grids {% endcomment %}
{{ product.featured_image | image_url: width: 300 }}

{% comment %} Product detail images - Medium to large {% endcomment %}
{{ product.featured_image | image_url: width: 800 }}

{% comment %} Collection banners - Large, full width {% endcomment %}
{{ collection.image | image_url: width: 1600 }}

{% comment %} Blog thumbnails - Medium {% endcomment %}
{{ article.image | image_url: width: 600 }}
```

### Lazy Loading Implementation
```liquid
{% comment %} Above-the-fold images (load immediately) {% endcomment %}
<img src="{{ hero_image | image_url: width: 1200 }}"
     alt="{{ hero_image.alt | escape }}"
     width="1200"
     height="600"
     fetchpriority="high">

{% comment %} Below-the-fold images (lazy load) {% endcomment %}
<img src="{{ product_image | image_url: width: 400 }}"
     alt="{{ product.title | escape }}"
     loading="lazy"
     width="400"
     height="400">
```

### Placeholder Prevention
```liquid
{% comment %} Prevent layout shift with aspect ratios {% endcomment %}
<div class="image-container" style="aspect-ratio: {{ image.width }}/{{ image.height }};">
  {% if image %}
    <img src="{{ image | image_url: width: 800 }}"
         alt="{{ image.alt | escape }}"
         loading="lazy"
         style="width: 100%; height: 100%; object-fit: cover;">
  {% else %}
    <div class="image-placeholder" aria-hidden="true">
      {{ 'image' | placeholder_svg_tag: 'placeholder-svg' }}
    </div>
  {% endif %}
</div>
```

## Liquid Performance

### Efficient Loops
```liquid
{% comment %} BAD: Heavy nested loops {% endcomment %}
{% for product in collections.all.products %}
  {% for variant in product.variants %}
    {% for option in variant.options %}
      <!-- Expensive operation -->
    {% endfor %}
  {% endfor %}
{% endfor %}

{% comment %} GOOD: Targeted collections with limits {% endcomment %}
{% for product in collections.featured.products limit: 8 %}
  {% if product.available %}
    <!-- Process only available products -->
  {% endif %}
{% endfor %}
```

### Pagination for Large Collections
```liquid
{% comment %} Always paginate collections >50 items {% endcomment %}
{% paginate collection.products by 24 %}
  <div class="product-grid">
    {% for product in collection.products %}
      <div class="product-card">
        <!-- Product content -->
      </div>
    {% endfor %}
  </div>

  {% if paginate.pages > 1 %}
    <nav class="pagination" aria-label="Pagination">
      {{ paginate | default_pagination }}
    </nav>
  {% endif %}
{% endpaginate %}
```

### Conditional Loading
```liquid
{% comment %} Load expensive content only when needed {% endcomment %}
{% if section.settings.show_related_products %}
  {% assign related_products = product.related_products | limit: 4 %}
  {% if related_products.size > 0 %}
    <div class="related-products">
      {% for related in related_products %}
        <!-- Related product content -->
      {% endfor %}
    </div>
  {% endif %}
{% endif %}
```

### Variable Assignment Optimization
```liquid
{% comment %} BAD: Repeated calculations {% endcomment %}
{% for product in collection.products %}
  <div class="product" data-price="{{ product.price | money_without_currency | remove: ',' }}">
    <span class="price">{{ product.price | money_without_currency | remove: ',' }}</span>
  </div>
{% endfor %}

{% comment %} GOOD: Calculate once, reuse {% endcomment %}
{% for product in collection.products %}
  {% assign clean_price = product.price | money_without_currency | remove: ',' %}
  <div class="product" data-price="{{ clean_price }}">
    <span class="price">{{ clean_price }}</span>
  </div>
{% endfor %}
```

## CSS Performance

### Scoped CSS Strategy
```liquid
{% comment %} Scope CSS to prevent conflicts and reduce specificity {% endcomment %}
{% assign unique = section.id | default: 'default' %}

{% style %}
  .hero-section-{{ unique }} {
    /* Component-specific styles */
    padding: {{ section.settings.padding }}px;
    background: {{ section.settings.bg_color }};
  }

  .hero-section-{{ unique }} .hero__title {
    /* Scoped child elements */
    font-size: {{ section.settings.title_size }}px;
    color: {{ section.settings.title_color }};
  }

  /* Responsive within scoped block */
  @media (max-width: 749px) {
    .hero-section-{{ unique }} {
      padding: {{ section.settings.padding_mobile }}px;
    }
  }
{% endstyle %}
```

### CSS Custom Properties
```liquid
{% comment %} Use CSS custom properties for dynamic values {% endcomment %}
{% style %}
  .component-{{ unique }} {
    --component-gap: {{ section.settings.gap }}px;
    --component-bg: {{ section.settings.bg_color }};
    --component-text: {{ section.settings.text_color }};
    --component-radius: {{ section.settings.border_radius }}px;

    display: flex;
    gap: var(--component-gap);
    background: var(--component-bg);
    color: var(--component-text);
    border-radius: var(--component-radius);
  }
{% endstyle %}
```

### Minimize CSS Output
```liquid
{% comment %} BAD: Verbose, repeated styles {% endcomment %}
{% style %}
  .section-{{ section.id }} .item-1 { background: {{ section.settings.color1 }}; }
  .section-{{ section.id }} .item-2 { background: {{ section.settings.color2 }}; }
  .section-{{ section.id }} .item-3 { background: {{ section.settings.color3 }}; }
{% endstyle %}

{% comment %} GOOD: Efficient, reusable styles {% endcomment %}
{% style %}
  .section-{{ section.id }} {
    --color-1: {{ section.settings.color1 }};
    --color-2: {{ section.settings.color2 }};
    --color-3: {{ section.settings.color3 }};
  }
  .section-{{ section.id }} .item-1 { background: var(--color-1); }
  .section-{{ section.id }} .item-2 { background: var(--color-2); }
  .section-{{ section.id }} .item-3 { background: var(--color-3); }
{% endstyle %}
```

## Accessibility Fundamentals

### WCAG 2.1 AA Compliance

#### Semantic HTML Structure
```liquid
<!-- Use proper heading hierarchy -->
<main>
  <section aria-labelledby="section-{{ section.id }}-heading">
    <h2 id="section-{{ section.id }}-heading">{{ section.settings.title | escape }}</h2>

    <article>
      <h3>{{ block.settings.item_title | escape }}</h3>
      <p>{{ block.settings.description | escape }}</p>
    </article>
  </section>
</main>
```

#### Descriptive Alt Text
```liquid
{% comment %} Informative images {% endcomment %}
{% if product.featured_image %}
  <img src="{{ product.featured_image | image_url: width: 400 }}"
       alt="{{ product.featured_image.alt | default: product.title | escape }}"
       loading="lazy">
{% endif %}

{% comment %} Decorative images {% endcomment %}
<img src="{{ decoration_image | image_url: width: 200 }}"
     alt=""
     role="presentation">

{% comment %} Complex images (charts, diagrams) {% endcomment %}
<img src="{{ infographic | image_url: width: 800 }}"
     alt="{{ section.settings.chart_description | escape }}"
     longdesc="{{ section.settings.detailed_description }}">
```

#### Focus Management
```liquid
{% comment %} Visible focus indicators {% endcomment %}
{% style %}
  .btn-{{ unique }}:focus {
    outline: 2px solid {{ section.settings.accent_color | default: '#007cba' }};
    outline-offset: 2px;
  }

  .card-{{ unique }}:focus-within {
    box-shadow: 0 0 0 2px {{ section.settings.accent_color | default: '#007cba' }};
  }
{% endstyle %}

{% comment %} Skip links for keyboard navigation {% endcomment %}
<a href="#main-content" class="skip-link">Skip to main content</a>
```

#### Form Accessibility
```liquid
<form class="contact-form">
  <div class="form-group">
    <label for="name-{{ section.id }}">
      Name
      <span class="required" aria-label="required">*</span>
    </label>
    <input type="text"
           id="name-{{ section.id }}"
           name="contact[name]"
           required
           aria-describedby="name-error-{{ section.id }}"
           autocomplete="name">
    <div id="name-error-{{ section.id }}" class="error-message" aria-live="polite"></div>
  </div>

  <div class="form-group">
    <label for="email-{{ section.id }}">
      Email
      <span class="required" aria-label="required">*</span>
    </label>
    <input type="email"
           id="email-{{ section.id }}"
           name="contact[email]"
           required
           aria-describedby="email-help-{{ section.id }}"
           autocomplete="email">
    <div id="email-help-{{ section.id }}" class="help-text">
      We'll never share your email with anyone else.
    </div>
  </div>

  <button type="submit" class="btn btn-primary">
    Send Message
  </button>
</form>
```

### Color Contrast Requirements

#### Minimum Contrast Ratios (WCAG AA)
- **Normal text**: 4.5:1
- **Large text (18px+)**: 3:1
- **Interactive elements**: 3:1

```liquid
{% comment %} Ensure sufficient contrast {% endcomment %}
{% style %}
  .text-on-background-{{ unique }} {
    background: {{ section.settings.bg_color | default: '#ffffff' }};
    color: {{ section.settings.text_color | default: '#333333' }};
    /* Ensure 4.5:1 contrast ratio */
  }

  .button-{{ unique }} {
    background: {{ section.settings.button_bg | default: '#007cba' }};
    color: {{ section.settings.button_text | default: '#ffffff' }};
    /* Ensure 4.5:1 contrast ratio */
  }

  .button-{{ unique }}:hover {
    background: {{ section.settings.button_bg | default: '#007cba' | color_darken: 10 }};
    /* Maintain contrast on hover */
  }
{% endstyle %}
```

### ARIA Labels and Landmarks
```liquid
<section class="testimonials-{{ unique }}"
         role="region"
         aria-labelledby="testimonials-heading-{{ unique }}">

  <h2 id="testimonials-heading-{{ unique }}">
    {{ section.settings.heading | escape }}
  </h2>

  <div class="testimonials-carousel"
       role="group"
       aria-label="Customer testimonials carousel"
       aria-live="polite">

    {% for block in section.blocks %}
      <blockquote class="testimonial"
                  {{ block.shopify_attributes }}
                  role="article"
                  aria-label="Testimonial by {{ block.settings.author | escape }}">
        <p>{{ block.settings.quote | escape }}</p>
        <cite>{{ block.settings.author | escape }}</cite>
      </blockquote>
    {% endfor %}
  </div>

  {% if section.blocks.size > 1 %}
    <div class="carousel-controls" role="group" aria-label="Carousel controls">
      <button type="button"
              class="carousel-prev"
              aria-label="Previous testimonial">
        <span aria-hidden="true">‹</span>
      </button>
      <button type="button"
              class="carousel-next"
              aria-label="Next testimonial">
        <span aria-hidden="true">›</span>
      </button>
    </div>
  {% endif %}
</section>
```

## Responsive Design

### Mobile-First CSS
```liquid
{% style %}
  /* Base styles (mobile) */
  .grid-{{ unique }} {
    display: grid;
    gap: {{ section.settings.gap_mobile | default: 16 }}px;
    grid-template-columns: 1fr;
  }

  /* Tablet and up */
  @media (min-width: 750px) {
    .grid-{{ unique }} {
      gap: {{ section.settings.gap_tablet | default: 24 }}px;
      grid-template-columns: repeat({{ section.settings.columns_tablet | default: 2 }}, 1fr);
    }
  }

  /* Desktop and up */
  @media (min-width: 990px) {
    .grid-{{ unique }} {
      gap: {{ section.settings.gap_desktop | default: 32 }}px;
      grid-template-columns: repeat({{ section.settings.columns_desktop | default: 3 }}, 1fr);
    }
  }
{% endstyle %}
```

### Container Queries (Progressive Enhancement)
```liquid
{% style %}
  .card-container-{{ unique }} {
    container-type: inline-size;
  }

  .card-{{ unique }} {
    padding: 16px;
  }

  /* Container query for larger containers */
  @container (min-width: 300px) {
    .card-{{ unique }} {
      padding: 24px;
      display: flex;
      align-items: center;
    }
  }

  /* Fallback for browsers without container query support */
  @supports not (container-type: inline-size) {
    @media (min-width: 750px) {
      .card-{{ unique }} {
        padding: 24px;
        display: flex;
        align-items: center;
      }
    }
  }
{% endstyle %}
```

## JavaScript Performance

### Minimal JavaScript Approach
```liquid
{% comment %} Use CSS for animations when possible {% endcomment %}
{% style %}
  .accordion-content-{{ unique }} {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }

  .accordion-content-{{ unique }}.open {
    max-height: 500px;
  }
{% endstyle %}

{% comment %} Minimal JavaScript for interaction {% endcomment %}
{% javascript %}
document.addEventListener('DOMContentLoaded', function() {
  const toggles = document.querySelectorAll('.accordion-toggle-{{ unique }}');

  toggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const content = this.nextElementSibling;
      const isOpen = content.classList.contains('open');

      // Close all other accordions
      document.querySelectorAll('.accordion-content-{{ unique }}').forEach(item => {
        item.classList.remove('open');
      });

      // Toggle current accordion
      if (!isOpen) {
        content.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
      } else {
        this.setAttribute('aria-expanded', 'false');
      }
    });
  });
});
{% endjavascript %}
```

### Progressive Enhancement
```liquid
{% comment %} Ensure functionality works without JavaScript {% endcomment %}
<details class="accordion-item-{{ unique }}">
  <summary class="accordion-toggle-{{ unique }}"
           role="button"
           aria-expanded="false">
    {{ block.settings.title | escape }}
  </summary>
  <div class="accordion-content-{{ unique }}">
    {{ block.settings.content }}
  </div>
</details>

{% comment %} Enhance with JavaScript {% endcomment %}
{% javascript %}
// Convert details/summary to custom accordion for better control
document.addEventListener('DOMContentLoaded', function() {
  const details = document.querySelectorAll('.accordion-item-{{ unique }}');

  details.forEach(detail => {
    const summary = detail.querySelector('summary');
    const content = detail.querySelector('.accordion-content-{{ unique }}');

    // Replace details/summary with div structure
    const wrapper = document.createElement('div');
    wrapper.className = 'accordion-enhanced-{{ unique }}';

    const button = document.createElement('button');
    button.textContent = summary.textContent;
    button.className = 'accordion-toggle-enhanced-{{ unique }}';
    button.setAttribute('aria-expanded', 'false');

    wrapper.appendChild(button);
    wrapper.appendChild(content);
    detail.parentNode.replaceChild(wrapper, detail);

    // Add click handler
    button.addEventListener('click', function() {
      const isOpen = content.classList.contains('open');
      content.classList.toggle('open');
      button.setAttribute('aria-expanded', !isOpen);
    });
  });
});
{% endjavascript %}
```

## Performance Monitoring

### Core Web Vitals Tracking
```liquid
{% comment %} Monitor performance in production {% endcomment %}
{% javascript %}
// Track Core Web Vitals
function trackWebVitals() {
  if ('PerformanceObserver' in window) {
    // Largest Contentful Paint
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      const lastEntry = entries[entries.length - 1];
      console.log('LCP:', lastEntry.startTime);
    }).observe({entryTypes: ['largest-contentful-paint']});

    // First Input Delay
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        console.log('FID:', entry.processingStart - entry.startTime);
      }
    }).observe({entryTypes: ['first-input']});

    // Cumulative Layout Shift
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          console.log('CLS:', entry.value);
        }
      }
    }).observe({entryTypes: ['layout-shift']});
  }
}

// Initialize tracking after page load
window.addEventListener('load', trackWebVitals);
{% endjavascript %}
```

## Testing and Validation

### Performance Testing Checklist
- ✅ **Lighthouse audit** (Performance >70)
- ✅ **WebPageTest** analysis
- ✅ **GTmetrix** scoring
- ✅ **Network throttling** testing
- ✅ **Mobile device** testing

### Accessibility Testing Tools
- ✅ **axe DevTools** browser extension
- ✅ **WAVE** web accessibility evaluator
- ✅ **Lighthouse accessibility** audit
- ✅ **Screen reader** testing (NVDA, JAWS, VoiceOver)
- ✅ **Keyboard navigation** testing

### Manual Testing Scenarios
```liquid
{% comment %} Test cases for your sections {% endcomment %}
<!--
1. Empty content states:
   - No image provided
   - No text content
   - No blocks added

2. Maximum content states:
   - Maximum blocks limit
   - Very long text content
   - Large images

3. Edge cases:
   - Special characters in text
   - Very short/long product titles
   - Missing alt text

4. Responsive breakpoints:
   - 320px (small mobile)
   - 768px (tablet)
   - 1024px (desktop)
   - 1440px (large desktop)

5. Accessibility scenarios:
   - Keyboard navigation only
   - Screen reader usage
   - High contrast mode
   - Zoom to 200%
-->
```

## Best Practices Summary

### Performance Best Practices
✅ **Optimize all images** with appropriate sizing and lazy loading
✅ **Use pagination** for collections >50 items
✅ **Scope CSS** to prevent conflicts and reduce specificity
✅ **Minimize Liquid complexity** with efficient loops and conditions
✅ **Progressive enhancement** for JavaScript functionality
✅ **Monitor Core Web Vitals** in production

### Accessibility Best Practices
✅ **Semantic HTML** with proper heading hierarchy
✅ **Descriptive alt text** for all meaningful images
✅ **Sufficient color contrast** (4.5:1 minimum)
✅ **Keyboard navigation** support for all interactive elements
✅ **Focus indicators** visible and high contrast
✅ **ARIA labels** for complex interactions
✅ **Form accessibility** with proper labels and error handling

### Testing Best Practices
✅ **Regular Lighthouse audits** during development
✅ **Cross-device testing** on real devices
✅ **Screen reader testing** for accessibility
✅ **Performance monitoring** in production
✅ **Edge case testing** with empty and maximum content states

## Next Steps

Complete your learning journey:
- **[Troubleshooting](./06-troubleshooting.md)** - Debug performance and accessibility issues
- **[Code Library](./code-library/)** - See optimized examples in action
- **[Advanced Features](./docs/advanced-features/)** - Modern performance patterns

## Essential References

### Performance Architecture
- **[Advanced Performance](./docs/advanced-features/advanced-performance.md)** - Cutting-edge optimization
- **[Asset Optimization](./docs/assets/)** - Complete asset management strategy
- **[CSS Assets](./docs/assets/css-assets.md)** - Styling performance patterns
- **[Image Assets](./docs/assets/image-assets.md)** - Responsive image optimization

### Core Web Vitals Implementation
- **[JavaScript Assets](./docs/assets/javascript-assets.md)** - Modern JS patterns and bundling
- **[Font Assets](./docs/assets/font-assets.md)** - Typography loading strategies
- **[Theme Architecture](./docs/architecture/theme-overview.md)** - Performance-first structure

### Accessibility Standards
- **[Best Practices 2025](./docs/architecture/best-practices-2025.md)** - Current accessibility standards
- **[Schema Validation](./schema-validation/schema-guidelines.md)** - Accessible schema patterns
- **[CSS Patterns](./code-library/css-patterns/accessibility.css)** - WCAG compliance patterns

### Advanced Features
- **[Progressive Web App](./docs/advanced-features/progressive-web-app.md)** - App-like performance
- **[AI-Generated Blocks](./docs/advanced-features/ai-generated-blocks.md)** - Automated optimization
- **[Section Groups](./docs/section-groups/)** - Dynamic layout performance