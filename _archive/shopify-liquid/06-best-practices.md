# Best Practices & Performance

Building great Shopify sections isn't just about functionality - it's about creating **fast, accessible, maintainable code** that provides an excellent merchant and customer experience. This guide covers essential practices for professional section development.

> 🎯 **Goal**: Build sections that load fast, work everywhere, and delight users.

---

## Performance Best Practices

### 1. Image Optimization

Images are often the largest assets on your pages. Optimize them properly:

#### ✅ Do This: Responsive Images

```liquid
<!-- Use responsive image parameters -->
<img 
  src="{{ product.featured_image | image_url: width: 800 }}"
  srcset="{{ product.featured_image | image_url: width: 400 }} 400w,
          {{ product.featured_image | image_url: width: 800 }} 800w,
          {{ product.featured_image | image_url: width: 1200 }} 1200w"
  sizes="(max-width: 768px) 400px, 800px"
  alt="{{ product.featured_image.alt | escape }}"
  loading="lazy"
  width="800"
  height="600"
>
```

#### ❌ Avoid This: Oversized Images

```liquid
<!-- Never load full-size images when smaller will do -->
<img src="{{ product.featured_image }}" alt="Product">

<!-- This loads the original image, potentially 4K+ resolution -->
```

#### Best Practices
- **Always specify width/height** parameters
- **Use `loading="lazy"`** for below-the-fold images
- **Provide `alt` attributes** for accessibility
- **Use appropriate sizes** - don't load 2000px images for 300px containers

### 2. JavaScript Performance

Keep JavaScript minimal and efficient:

#### ✅ Do This: Minimal, Scoped JavaScript

```liquid
{% javascript %}
// Wrap in IIFE to avoid global namespace pollution
(function() {
  'use strict';
  
  // Only run if elements exist
  const toggles = document.querySelectorAll('[data-faq-toggle]');
  if (!toggles.length) return;
  
  // Use event delegation for better performance
  document.addEventListener('click', function(e) {
    if (!e.target.matches('[data-faq-toggle]')) return;
    
    // Actual toggle logic here
    toggleFAQ(e.target);
  });
  
  function toggleFAQ(button) {
    // Implementation
  }
})();
{% endjavascript %}
```

#### ❌ Avoid This: Bloated JavaScript

```javascript
// Global variables
var faqButtons = document.querySelectorAll('.faq-button');
var modals = document.querySelectorAll('.modal');
var sliders = $('.slider'); // Don't assume jQuery exists
var someGlobalVar = true;

// Heavy DOM manipulation
for (var i = 0; i < faqButtons.length; i++) {
  faqButtons[i].addEventListener('click', function() {
    // Lots of DOM queries inside event handler
    var content = document.querySelector('#content-' + this.id);
    var overlay = document.querySelector('.overlay');
    // ... heavy operations
  });
}
```

#### JavaScript Guidelines
- **Keep total JS under 16KB** for theme store approval
- **Use IIFEs** to avoid global namespace pollution
- **Check element existence** before adding listeners
- **Use event delegation** for dynamic content
- **Minimize DOM queries** - cache selectors
- **Don't assume jQuery** exists in themes

### 3. CSS Optimization

Write efficient, maintainable CSS:

#### ✅ Do This: Organized, Scoped CSS

```liquid
<style>
  /* Use CSS custom properties for dynamic values */
  .hero-section {
    --bg-color: {{ section.settings.background_color | default: '#ffffff' }};
    --text-color: {{ section.settings.text_color | default: '#333333' }};
    --spacing: {{ section.settings.padding | default: 60 }}px;
    
    background-color: var(--bg-color);
    color: var(--text-color);
    padding: var(--spacing) 0;
  }
  
  /* Mobile-first responsive design */
  .hero-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  
  @media (min-width: 768px) {
    .hero-content {
      flex-direction: row;
      align-items: center;
    }
  }
  
  /* Specific selectors to avoid conflicts */
  .hero-section .btn-primary {
    background: var(--text-color);
    color: var(--bg-color);
  }
</style>
```

#### ❌ Avoid This: Global, Conflicting CSS

```css
/* Too generic - will conflict with theme CSS */
.button { background: red; }
.text { font-size: 16px; }
h2 { margin: 0; }

/* Hard-coded values that can't be customized */
.hero { 
  background: #ff0000;
  padding: 50px;
}

/* Desktop-first (mobile unfriendly) */
@media (max-width: 768px) {
  .hero { padding: 20px; }
}
```

#### CSS Guidelines
- **Use CSS custom properties** for dynamic values
- **Scope selectors** to your section class
- **Write mobile-first** media queries
- **Avoid `!important`** unless absolutely necessary
- **Use semantic class names** that describe purpose
- **Keep CSS within `<style>` blocks** in sections

### 4. Liquid Performance

Write efficient Liquid code:

#### ✅ Do This: Efficient Liquid

```liquid
<!-- Cache expensive operations -->
{% assign featured_products = collections.featured.products | limit: 6 %}

<!-- Check existence before complex operations -->
{% if section.blocks.size > 0 %}
  {% for block in section.blocks %}
    <!-- Block content -->
  {% endfor %}
{% endif %}

<!-- Use appropriate filters -->
{{ product.price | money_without_currency }}

<!-- Limit loops appropriately -->
{% for product in collection.products limit: 12 %}
  <!-- Product display -->
{% endfor %}
```

#### ❌ Avoid This: Inefficient Liquid

```liquid
<!-- Don't repeat expensive operations -->
{% for i in (1..collections.featured.products.size) %}
  {{ collections.featured.products[forloop.index0].title }}
{% endfor %}

<!-- Don't loop without limits -->
{% for product in collections.all.products %}
  <!-- Could be thousands of products! -->
{% endfor %}

<!-- Don't nest expensive operations -->
{% for collection in collections %}
  {% for product in collection.products %}
    {% for variant in product.variants %}
      <!-- Triple nested loop - performance killer -->
    {% endfor %}
  {% endfor %}
{% endfor %}
```

---

## Accessibility Best Practices

Make your sections usable by everyone:

### 1. Semantic HTML

Use the right HTML elements for their intended purpose:

#### ✅ Do This: Semantic Structure

```liquid
<section class="testimonials-section" aria-labelledby="testimonials-heading">
  <div class="container">
    <h2 id="testimonials-heading">{{ section.settings.title | escape }}</h2>
    
    <div class="testimonials-grid" role="list">
      {% for block in section.blocks %}
        <article class="testimonial-card" role="listitem">
          <blockquote>
            <p>"{{ block.settings.quote | escape }}"</p>
            <footer>
              <cite>{{ block.settings.author | escape }}</cite>
            </footer>
          </blockquote>
        </article>
      {% endfor %}
    </div>
  </div>
</section>
```

#### ❌ Avoid This: Generic Divs

```liquid
<div class="section">
  <div class="title">Customer Reviews</div>
  <div class="cards">
    <div class="card">
      <div class="quote">"Great product!"</div>
      <div class="author">John</div>
    </div>
  </div>
</div>
```

### 2. Keyboard Navigation

Ensure all interactive elements are keyboard accessible:

#### ✅ Do This: Keyboard Friendly

```liquid
<button type="button" 
        class="faq-toggle"
        aria-expanded="false"
        aria-controls="faq-answer-{{ forloop.index }}"
        data-faq-toggle>
  {{ block.settings.question | escape }}
</button>

<div id="faq-answer-{{ forloop.index }}" 
     class="faq-answer" 
     aria-hidden="true">
  {{ block.settings.answer }}
</div>
```

```javascript
// Support keyboard navigation
toggle.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    this.click();
  }
});
```

### 3. Screen Reader Support

Use ARIA attributes appropriately:

#### ✅ Do This: ARIA Support

```liquid
<!-- Descriptive labels -->
<img src="{{ image | image_url }}" 
     alt="{{ image.alt | escape | default: 'Product image' }}"
     loading="lazy">

<!-- Proper form labels -->
<label for="newsletter-email">Email Address</label>
<input type="email" 
       id="newsletter-email" 
       name="email"
       required
       aria-describedby="email-help">
<div id="email-help">We'll never share your email</div>

<!-- Live regions for dynamic content -->
<div aria-live="polite" id="cart-status">
  Item added to cart
</div>
```

### 4. Color Contrast

Ensure sufficient contrast for readability:

#### ✅ Do This: Accessible Colors

```liquid
<style>
  .section-title {
    /* Ensure 4.5:1 contrast ratio minimum */
    color: {{ section.settings.text_color | default: '#333333' }};
    background: {{ section.settings.background_color | default: '#ffffff' }};
  }
  
  .btn-primary {
    /* High contrast for buttons */
    background: #0066cc;
    color: white;
    border: 2px solid transparent;
  }
  
  .btn-primary:focus {
    /* Visible focus indicator */
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }
</style>
```

---

## Code Organization

Keep your code maintainable:

### 1. Section Structure

Organize sections consistently:

```liquid
<!-- 1. CSS Styles at the top -->
<style>
  /* Component styles here */
</style>

<!-- 2. HTML Structure -->
<div class="my-section" id="section-{{ section.id }}">
  <!-- Section content -->
</div>

<!-- 3. Schema at the bottom -->
{% schema %}
{
  "name": "My Section",
  "settings": [...]
}
{% endschema %}

<!-- 4. JavaScript at the very bottom -->
{% javascript %}
// Component JavaScript
{% endjavascript %}
```

### 2. Liquid Code Organization

Keep Liquid clean and readable:

#### ✅ Do This: Well-Organized Liquid

```liquid
<!-- Cache complex calculations -->
{% assign total_products = collection.products.size %}
{% assign products_per_row = section.settings.products_per_row | default: 4 %}
{% assign show_pagination = total_products > section.settings.products_to_show %}

<!-- Use meaningful variable names -->
{% if section.settings.show_section and total_products > 0 %}
  <div class="products-grid products-grid--{{ products_per_row }}-per-row">
    {% for product in collection.products limit: section.settings.products_to_show %}
      {% render 'product-card', product: product %}
    {% endfor %}
  </div>
  
  {% if show_pagination %}
    {% render 'pagination', paginate: paginate %}
  {% endif %}
{% endif %}
```

#### ❌ Avoid This: Messy Liquid

```liquid
{% if section.settings.show_section %}{% if collection.products.size > 0 %}<div class="products-grid products-grid--{{ section.settings.products_per_row | default: 4 }}-per-row">{% for product in collection.products limit: section.settings.products_to_show %}{% render 'product-card', product: product %}{% endfor %}</div>{% if collection.products.size > section.settings.products_to_show %}{% render 'pagination', paginate: paginate %}{% endif %}{% endif %}{% endif %}
```

### 3. Schema Organization

Structure schemas logically:

#### ✅ Do This: Organized Schema

```json
{
  "name": "Hero Section",
  "tag": "section",
  "class": "hero-section",
  "settings": [
    {
      "type": "header",
      "content": "Content Settings"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Main Heading",
      "default": "Welcome"
    },
    {
      "type": "richtext", 
      "id": "description",
      "label": "Description"
    },
    {
      "type": "header",
      "content": "Visual Settings"
    },
    {
      "type": "image_picker",
      "id": "background_image",
      "label": "Background Image"
    },
    {
      "type": "color",
      "id": "text_color", 
      "label": "Text Color",
      "default": "#333333"
    }
  ],
  "presets": [
    {
      "name": "Hero Section",
      "category": "Image",
      "settings": {
        "heading": "Welcome to Our Store"
      }
    }
  ]
}
```

---

## SEO Best Practices

Optimize sections for search engines:

### 1. Structured Data

Add appropriate schema markup:

```liquid
<!-- Product structured data -->
{% if template contains 'product' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": {{ product.title | json }},
  "description": {{ product.description | strip_html | json }},
  "image": {{ product.featured_image | image_url | json }},
  "brand": {
    "@type": "Brand", 
    "name": {{ product.vendor | json }}
  },
  "offers": {
    "@type": "Offer",
    "price": {{ product.price | divided_by: 100.0 }},
    "priceCurrency": {{ cart.currency.iso_code | json }},
    "availability": "{% if product.available %}InStock{% else %}OutOfStock{% endif %}"
  }
}
</script>
{% endif %}
```

### 2. Semantic Headings

Use proper heading hierarchy:

#### ✅ Do This: Proper Heading Structure

```liquid
<!-- Page title (usually h1 in theme) -->
<h1>{{ page.title }}</h1>

<!-- Section title (h2) -->
<h2>{{ section.settings.title }}</h2>

<!-- Subsection titles (h3) -->
{% for block in section.blocks %}
  <h3>{{ block.settings.heading }}</h3>
  <!-- Block content -->
{% endfor %}
```

#### ❌ Avoid This: Heading Soup

```liquid
<!-- Multiple h1s on same page -->
<h1>Main Title</h1>
<h1>Section Title</h1>

<!-- Skipping heading levels -->
<h2>Section Title</h2>
<h5>Subsection Title</h5>

<!-- Using headings for styling -->
<h3 style="font-size: 12px;">Small text</h3>
```

### 3. Meta Information

Optimize meta content:

```liquid
<!-- In theme.liquid head -->
{% if template contains 'product' %}
  <meta property="og:title" content="{{ product.title | escape }}">
  <meta property="og:description" content="{{ product.description | strip_html | truncate: 160 | escape }}">
  <meta property="og:image" content="{{ product.featured_image | image_url: width: 1200 }}">
  <meta property="og:type" content="product">
{% endif %}
```

---

## Security Best Practices

Protect against common vulnerabilities:

### 1. Input Sanitization

Always sanitize user input:

#### ✅ Do This: Escaped Output

```liquid
<!-- Escape all user-controlled content -->
<h2>{{ section.settings.title | escape }}</h2>
<p>{{ customer.name | escape }}</p>

<!-- Rich text doesn't need escaping -->
<div class="content">{{ section.settings.rich_text }}</div>

<!-- Sanitize URLs -->
<a href="{{ section.settings.link | url }}">
  {{ section.settings.link_text | escape }}
</a>
```

#### ❌ Avoid This: Unescaped Output

```liquid
<!-- Never output user content without escaping -->
<h2>{{ section.settings.title }}</h2>
<script>var title = "{{ section.settings.title }}";</script>
```

### 2. Safe Liquid Filters

Use appropriate filters for different contexts:

```liquid
<!-- For HTML content -->
{{ user_input | escape }}

<!-- For HTML attributes -->
<div class="{{ user_input | handle }}">

<!-- For URLs -->
<a href="{{ user_url | url }}">

<!-- For JavaScript strings -->
<script>
var data = {{ user_data | json }};
</script>

<!-- For CSS values (be very careful) -->
<style>
.dynamic { 
  color: {{ user_color | default: '#000000' }};
}
</style>
```

---

## Testing Checklist

Before deploying your sections:

### Functionality Testing
- [ ] All settings work as expected
- [ ] Blocks can be added/removed/reordered
- [ ] Section shows/hides correctly
- [ ] Links and buttons work
- [ ] Forms submit properly

### Performance Testing
- [ ] Images load with appropriate sizes
- [ ] JavaScript is under 16KB
- [ ] No console errors
- [ ] Fast loading on mobile
- [ ] Lighthouse score > 60

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader friendly
- [ ] Sufficient color contrast
- [ ] Proper ARIA attributes
- [ ] Semantic HTML structure

### Browser Testing
- [ ] Works in Chrome, Firefox, Safari, Edge
- [ ] Mobile responsive
- [ ] Touch interactions work
- [ ] No layout breaking at different screen sizes

### Theme Editor Testing
- [ ] Section appears in correct categories
- [ ] All settings update live preview
- [ ] Blocks work properly in editor
- [ ] Presets work correctly
- [ ] No JavaScript errors in editor

---

## Performance Monitoring

Track your section performance:

### Core Web Vitals
Monitor these key metrics:
- **Largest Contentful Paint (LCP)** - < 2.5s
- **First Input Delay (FID)** - < 100ms  
- **Cumulative Layout Shift (CLS)** - < 0.1

### Tools to Use
- **PageSpeed Insights** - Google's performance tool
- **GTmetrix** - Detailed performance analysis
- **WebPageTest** - Advanced performance testing
- **Lighthouse** - Built into Chrome DevTools

---

## Common Performance Pitfalls

### ❌ Avoid These Mistakes

1. **Loading too many products** - Limit collections to 50 items max
2. **Not lazy loading images** - Use `loading="lazy"` 
3. **Oversized images** - Always specify width parameters
4. **Global CSS conflicts** - Scope your CSS properly
5. **Heavy JavaScript** - Keep under 16KB total
6. **Too many API calls** - Cache results when possible
7. **Blocking resources** - Use async/defer for scripts
8. **Font loading issues** - Preload critical fonts

---

## Next Steps

Ready to take your sections to the next level?

- **[Theme Editor Integration](./07-theme-editor.md)** - Make your sections editor-friendly
- **[Troubleshooting Guide](./09-troubleshooting.md)** - Debug common issues  
- **[Advanced Techniques](./10-advanced.md)** - Pro-level section development

Remember: **Performance is a feature**. Fast, accessible sections create better experiences for merchants and customers alike! 🚀
