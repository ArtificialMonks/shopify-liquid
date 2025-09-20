# CSS Assets - Organization and Optimization

CSS assets are the foundation of your theme's visual presentation. This guide covers modern CSS organization patterns, optimization strategies, and performance best practices for Shopify themes.

## 🎯 CSS Asset Types

### Core CSS Files
- **`theme.css.liquid`** - Main stylesheet with Liquid preprocessing
- **`critical.css`** - Above-the-fold critical styles
- **`base.css`** - Reset, typography, layout foundations
- **`components.css`** - Reusable component styles
- **`sections.css`** - Section-specific styles

### Specialized CSS Files
- **`print.css`** - Print-specific styles
- **`admin.css`** - Theme editor customizations
- **`vendor/`** - Third-party CSS libraries

## 🏗️ CSS Organization Patterns

### File Structure
```
assets/
├── theme.css.liquid          # Main entry point
├── critical.css              # Critical path CSS
├── base.css                  # Foundation styles
├── components.css            # Reusable components
├── sections.css              # Section-specific styles
├── utilities.css             # Utility classes
└── vendor/
    ├── normalize.css         # CSS reset
    └── swiper.css           # Third-party libraries
```

### CSS Architecture
```css
/* theme.css.liquid - Main stylesheet */
/* ==========================================================================
   Critical Styles (inline these for performance)
   ========================================================================== */
@import url('critical.css');

/* ==========================================================================
   Base Styles
   ========================================================================== */
@import url('base.css');

/* ==========================================================================
   Layout Styles
   ========================================================================== */
@import url('layout.css');

/* ==========================================================================
   Component Styles
   ========================================================================== */
@import url('components.css');

/* ==========================================================================
   Section Styles
   ========================================================================== */
@import url('sections.css');

/* ==========================================================================
   Utility Classes
   ========================================================================== */
@import url('utilities.css');

/* ==========================================================================
   Theme-specific customizations with Liquid
   ========================================================================== */
:root {
  --color-primary: {{ settings.color_primary }};
  --color-secondary: {{ settings.color_secondary }};
  --font-heading: {{ settings.font_heading.family }}, {{ settings.font_heading.fallback_families }};
  --font-body: {{ settings.font_body.family }}, {{ settings.font_body.fallback_families }};
}
```

## 🎨 CSS Preprocessing with Liquid

### Dynamic CSS Variables
```css
/* theme.css.liquid - Dynamic theming */
:root {
  /* Colors from theme settings */
  --color-primary: {{ settings.color_primary }};
  --color-secondary: {{ settings.color_secondary }};
  --color-accent: {{ settings.color_accent }};

  /* Typography from theme settings */
  --font-heading-family: {{ settings.font_heading.family }}, {{ settings.font_heading.fallback_families }};
  --font-body-family: {{ settings.font_body.family }}, {{ settings.font_body.fallback_families }};
  --font-heading-weight: {{ settings.font_heading.weight }};
  --font-body-weight: {{ settings.font_body.weight }};

  /* Spacing from theme settings */
  --spacing-small: {{ settings.spacing_small }}px;
  --spacing-medium: {{ settings.spacing_medium }}px;
  --spacing-large: {{ settings.spacing_large }}px;

  /* Responsive breakpoints */
  --screen-sm: 576px;
  --screen-md: 768px;
  --screen-lg: 992px;
  --screen-xl: 1200px;
}
```

### Conditional Styles
```css
/* theme.css.liquid - Conditional styling */
{% if settings.enable_rounded_buttons %}
.btn {
  border-radius: {{ settings.button_border_radius }}px;
}
{% endif %}

{% if settings.enable_shadows %}
.card {
  box-shadow: 0 {{ settings.shadow_blur }}px {{ settings.shadow_spread }}px rgba(0, 0, 0, {{ settings.shadow_opacity }});
}
{% endif %}

{% case settings.layout_style %}
  {% when 'boxed' %}
    .container {
      max-width: {{ settings.container_width }}px;
      margin: 0 auto;
    }
  {% when 'full-width' %}
    .container {
      max-width: 100%;
    }
{% endcase %}
```

### Section-Specific Styles
```css
/* Section-scoped CSS with unique identifiers */
{% assign unique = section.id | replace: '_', '' | downcase %}

.hero-{{ unique }} {
  background-color: {{ section.settings.background_color }};
  padding: {{ section.settings.padding_top }}px 0 {{ section.settings.padding_bottom }}px;
  text-align: {{ section.settings.text_alignment }};
}

.hero__heading-{{ unique }} {
  font-size: {{ section.settings.heading_size }}px;
  color: {{ section.settings.heading_color }};
  margin-bottom: {{ section.settings.heading_margin }}px;
}

@media (max-width: 749px) {
  .hero__heading-{{ unique }} {
    font-size: {{ section.settings.heading_size | times: 0.8 }}px;
  }
}
```

## 🚀 Performance Optimization

### Critical CSS Strategy
```html
<!-- theme.liquid - Critical CSS inline -->
<style>
  {{ 'critical.css' | asset_url | asset_content }}
</style>

<!-- Non-critical CSS async -->
<link rel="preload"
      href="{{ 'theme.css' | asset_url }}"
      as="style"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript>
  <link rel="stylesheet" href="{{ 'theme.css' | asset_url }}">
</noscript>
```

### CSS Optimization Techniques
```css
/* Efficient CSS patterns */

/* Use CSS custom properties for theming */
:root {
  --primary-color: #000;
  --secondary-color: #666;
}

/* Avoid deep nesting (max 3 levels) */
.card .card__content .card__title {
  /* Good: 3 levels maximum */
}

/* Use efficient selectors */
.btn-primary { /* Good: class selector */ }
#main-nav .nav-item { /* Avoid: ID + class */ }

/* Minimize reflows with transform */
.element {
  transform: translateX(100px); /* Good: uses GPU */
  left: 100px; /* Avoid: triggers reflow */
}

/* Use shorthand properties */
.element {
  margin: 10px 20px; /* Good: shorthand */
  /* Avoid: margin-top: 10px; margin-right: 20px; etc. */
}
```

### Responsive Design Patterns
```css
/* Mobile-first responsive design */
.hero {
  padding: 2rem 1rem;
  font-size: 1.5rem;
}

@media (min-width: 768px) {
  .hero {
    padding: 4rem 2rem;
    font-size: 2rem;
  }
}

@media (min-width: 1024px) {
  .hero {
    padding: 6rem 3rem;
    font-size: 2.5rem;
  }
}

/* Container queries for component-based responsive design */
@container hero-container (min-width: 500px) {
  .hero__title {
    font-size: 2rem;
  }
}

/* CSS Grid for modern layouts */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}
```

## 🎯 Component-Based CSS

### BEM Methodology
```css
/* Block Element Modifier naming */
.product-card { /* Block */ }
.product-card__image { /* Element */ }
.product-card__title { /* Element */ }
.product-card--featured { /* Modifier */ }
.product-card__price--sale { /* Element + Modifier */ }

/* Example implementation */
.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.product-card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-card__title {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 1rem 0 0.5rem;
}

.product-card--featured {
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
```

### Utility Classes
```css
/* Spacing utilities */
.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

/* Text utilities */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

/* Display utilities */
.d-none { display: none; }
.d-block { display: block; }
.d-flex { display: flex; }
.d-grid { display: grid; }

/* Responsive utilities */
@media (max-width: 767px) {
  .d-md-none { display: none; }
  .text-md-center { text-align: center; }
}
```

## 🔧 Advanced CSS Patterns

### CSS Custom Properties for Theming
```css
/* Dynamic theming system */
[data-theme="light"] {
  --bg-primary: #ffffff;
  --text-primary: #000000;
  --border-color: #e5e5e5;
}

[data-theme="dark"] {
  --bg-primary: #000000;
  --text-primary: #ffffff;
  --border-color: #333333;
}

.card {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
```

### CSS Logical Properties
```css
/* Modern CSS logical properties for internationalization */
.content {
  padding-inline: 1rem; /* Instead of padding-left/right */
  margin-block: 2rem;   /* Instead of margin-top/bottom */
  border-inline-start: 2px solid blue; /* Instead of border-left */
}
```

### Container Queries
```css
/* Component-based responsive design */
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}

@container sidebar (min-width: 300px) {
  .widget {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

## 📊 CSS Performance Metrics

### Critical Metrics
- **First Contentful Paint (FCP)** - Time to first rendered content
- **Largest Contentful Paint (LCP)** - Time to main content render
- **Cumulative Layout Shift (CLS)** - Visual stability measurement
- **CSS file size** - Keep under 50KB for main stylesheet

### Optimization Checklist
- [ ] Remove unused CSS (PurgeCSS or similar)
- [ ] Minify CSS for production
- [ ] Use efficient selectors (avoid deep nesting)
- [ ] Implement critical CSS strategy
- [ ] Optimize font loading (preload, font-display)
- [ ] Use CSS containment for performance
- [ ] Minimize layout thrashing

## 🛠️ Development Tools

### CSS Preprocessing
```css
/* Using CSS custom properties instead of Sass variables */
:root {
  --spacing-unit: 1rem;
  --spacing-xs: calc(var(--spacing-unit) * 0.25);
  --spacing-sm: calc(var(--spacing-unit) * 0.5);
  --spacing-md: var(--spacing-unit);
  --spacing-lg: calc(var(--spacing-unit) * 2);
  --spacing-xl: calc(var(--spacing-unit) * 3);
}
```

### CSS Validation
Use Theme Check for Shopify-specific CSS validation:
```yaml
# .theme-check.yml
CSSOptimization:
  enabled: true
  severity: suggestion

UnusedAssignment:
  enabled: true
  severity: error
```

## 🚨 Common Pitfalls

### 1. Overuse of !important
**Problem**: Makes CSS unmaintainable
```css
/* Bad */
.button {
  background: blue !important;
}

/* Good */
.button.button--primary {
  background: blue;
}
```

### 2. Inefficient Selectors
**Problem**: Poor performance
```css
/* Bad */
div > div > div > .content {
  color: black;
}

/* Good */
.page-content {
  color: black;
}
```

### 3. Missing Fallbacks
**Problem**: Breaks on older browsers
```css
/* Bad */
.grid {
  display: grid;
}

/* Good */
.grid {
  display: flex; /* Fallback */
  display: grid;
}
```

---

CSS assets form the visual foundation of your Shopify theme. Proper organization, optimization, and modern techniques ensure fast loading times and maintainable code.