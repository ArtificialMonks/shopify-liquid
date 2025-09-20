# theme.liquid - Main Layout File

The `theme.liquid` file is the foundation of every Shopify theme, providing the base HTML structure that wraps all other templates. This file is **required** and must include specific Liquid objects to function properly.

## 🎯 Purpose and Role

The `theme.liquid` file serves as:
- **HTML skeleton** for all non-checkout pages
- **Global wrapper** containing shared elements
- **Asset loader** for stylesheets and scripts
- **Metadata container** for SEO and tracking
- **Section group host** for header/footer areas

## 📋 Required Elements

### Essential Liquid Objects
Every `theme.liquid` file **must** include these objects:

#### 1. content_for_header
```liquid
<head>
  {{ content_for_header }}
</head>
```
- **Location**: Inside `<head>` tag
- **Purpose**: Loads Shopify's required scripts (hCaptcha, app scripts, analytics)
- **Critical**: Theme won't save without this object
- **Warning**: Never modify or parse this object's content

#### 2. content_for_layout
```liquid
<body>
  {{ content_for_layout }}
</body>
```
- **Location**: Inside `<body>` tag
- **Purpose**: Renders template-specific content dynamically
- **Critical**: Theme won't save without this object
- **Content**: Includes sections and blocks from Online Store 2.0 themes

## 🏗️ Basic Structure

### Minimal Required Structure
```liquid
<!DOCTYPE html>
<html lang="{{ shop.locale }}">
<head>
  <meta charset="utf-8">
  <title>{{ page_title }}</title>
  {{ content_for_header }}
</head>
<body class="template-{{ template.name }}">
  {{ content_for_layout }}
</body>
</html>
```

### Production-Ready Structure
```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}" dir="{{ localization.direction }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page_title }}{% if current_tags %} &ndash; {{ 'general.meta.tags' | t: tags: meta_tags }}{% endif %}{% if current_page != 1 %} &ndash; {{ 'general.meta.page' | t: page: current_page }}{% endif %}{% unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless %}</title>

  {% if page_description %}
    <meta name="description" content="{{ page_description | escape }}">
  {% endif %}

  <link rel="canonical" href="{{ canonical_url }}">

  {% if settings.favicon %}
    <link rel="icon" type="image/png" href="{{ settings.favicon | image_url: width: 32, height: 32 }}">
  {% endif %}

  {% comment %} Preconnect to required origins {% endcomment %}
  <link rel="preconnect" href="https://cdn.shopify.com" crossorigin>

  {% comment %} Preload critical resources {% endcomment %}
  {{ 'theme.css' | asset_url | preload_tag: as: 'style', onload: "this.onload=null;this.rel='stylesheet'" }}

  {% comment %} Critical CSS inline {% endcomment %}
  <style>
    {{ 'critical.css' | asset_url | asset }}
  </style>

  {{ content_for_header }}

  {% comment %} Theme CSS {% endcomment %}
  {{ 'theme.css' | asset_url | stylesheet_tag }}

  {% comment %} Conditional assets {% endcomment %}
  {% case template.name %}
    {% when 'product' %}
      {{ 'product.css' | asset_url | stylesheet_tag }}
    {% when 'collection' %}
      {{ 'collection.css' | asset_url | stylesheet_tag }}
  {% endcase %}
</head>
<body class="template-{{ template.name }}{% if template.suffix %} template-{{ template.name }}-{{ template.suffix }}{% endif %}">
  {% comment %} Skip link for accessibility {% endcomment %}
  <a class="skip-link" href="#main-content">{{ 'accessibility.skip_to_content' | t }}</a>

  {% comment %} Header section group {% endcomment %}
  {% sections 'header-group' %}

  {% comment %} Main content area {% endcomment %}
  <main id="main-content" tabindex="-1" role="main">
    {{ content_for_layout }}
  </main>

  {% comment %} Footer section group {% endcomment %}
  {% sections 'footer-group' %}

  {% comment %} Theme JavaScript {% endcomment %}
  {{ 'theme.js' | asset_url | script_tag: defer: true }}
</body>
</html>
```

## 🎨 Available Liquid Objects

### Global Objects
Access these objects anywhere in `theme.liquid`:

#### Template Context
```liquid
{{ template.name }}        <!-- Template type (product, collection, etc.) -->
{{ template.suffix }}      <!-- Alternative template suffix -->
{{ template.directory }}   <!-- Template directory -->
```

#### Shop Information
```liquid
{{ shop.name }}            <!-- Store name -->
{{ shop.url }}             <!-- Store URL -->
{{ shop.locale }}          <!-- Store locale -->
{{ shop.currency }}        <!-- Store currency -->
```

#### Page Metadata
```liquid
{{ page_title }}           <!-- Current page title -->
{{ page_description }}     <!-- Current page description -->
{{ canonical_url }}        <!-- Canonical URL for SEO -->
```

#### Customer Context
```liquid
{{ customer }}             <!-- Current customer object -->
{{ customer.first_name }}  <!-- Customer details if logged in -->
```

#### Cart Information
```liquid
{{ cart.item_count }}      <!-- Number of items in cart -->
{{ cart.total_price }}     <!-- Cart total price -->
```

## 🚀 Advanced Patterns

### Performance Optimization

#### Critical CSS Inline
```liquid
<head>
  <style>
    {{ 'critical.css' | asset_url | asset }}
  </style>

  {% comment %} Non-critical CSS async {% endcomment %}
  {{ 'theme.css' | asset_url | stylesheet_tag: media: 'print', onload: "this.media='all'" }}
  <noscript>{{ 'theme.css' | asset_url | stylesheet_tag }}</noscript>
</head>
```

#### Resource Preloading
```liquid
<head>
  {% comment %} Preload critical resources {% endcomment %}
  {{ 'theme.js' | asset_url | preload_tag: as: 'script' }}
  {{ 'hero-image.jpg' | asset_url | preload_tag: as: 'image' }}

  {% comment %} Preload fonts {% endcomment %}
  {{ 'theme-font.woff2' | asset_url | preload_tag: as: 'font', type: 'font/woff2', crossorigin: 'anonymous' }}
</head>
```

#### Script Optimization
```liquid
<body>
  {% comment %} Defer non-critical JavaScript {% endcomment %}
  {{ 'theme.js' | asset_url | script_tag: defer: true }}

  {% comment %} Async third-party scripts {% endcomment %}
  {{ 'analytics.js' | asset_url | script_tag: async: true }}

  {% comment %} Module loading for modern browsers {% endcomment %}
  <script type="module" src="{{ 'theme.module.js' | asset_url }}" defer></script>
</body>
```

### SEO Enhancement

#### Structured Data
```liquid
<head>
  {% comment %} Organization schema {% endcomment %}
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": {{ shop.name | json }},
      "url": {{ shop.url | json }}
    }
  </script>

  {% comment %} Breadcrumb schema {% endcomment %}
  {% if template.name == 'product' or template.name == 'collection' %}
    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": {{ 'general.breadcrumbs.home' | t | json }},
            "item": {{ shop.url | json }}
          }
        ]
      }
    </script>
  {% endif %}
</head>
```

#### Multi-Language SEO
```liquid
<head>
  {% comment %} Hreflang links {% endcomment %}
  {% for locale in localization.available_locales %}
    <link rel="alternate"
          hreflang="{{ locale.iso_code }}"
          href="{{ request.url | localization_url: locale.iso_code }}">
  {% endfor %}

  {% comment %} Default language {% endcomment %}
  <link rel="alternate"
        hreflang="x-default"
        href="{{ request.url | localization_url: localization.default_locale.iso_code }}">
</head>
```

### Accessibility Implementation

#### Semantic Structure
```liquid
<body>
  {% comment %} Skip navigation {% endcomment %}
  <a class="skip-link" href="#main-content">{{ 'accessibility.skip_to_content' | t }}</a>

  {% comment %} Header landmark {% endcomment %}
  <header role="banner">
    {% sections 'header-group' %}
  </header>

  {% comment %} Main content landmark {% endcomment %}
  <main id="main-content" tabindex="-1" role="main">
    {{ content_for_layout }}
  </main>

  {% comment %} Footer landmark {% endcomment %}
  <footer role="contentinfo">
    {% sections 'footer-group' %}
  </footer>
</body>
```

#### Focus Management
```liquid
<head>
  <style>
    /* Focus indicators */
    .skip-link {
      position: absolute;
      top: -40px;
      left: 6px;
      background: #000;
      color: #fff;
      padding: 8px;
      text-decoration: none;
      transition: top 0.3s;
    }

    .skip-link:focus {
      top: 6px;
    }
  </style>
</head>
```

### Conditional Loading

#### Template-Specific Assets
```liquid
<head>
  {% comment %} Load assets based on template {% endcomment %}
  {% case template.name %}
    {% when 'product' %}
      {{ 'product.css' | asset_url | stylesheet_tag }}
      <link rel="preload" href="{{ 'product-zoom.js' | asset_url }}" as="script">
    {% when 'collection' %}
      {{ 'collection.css' | asset_url | stylesheet_tag }}
    {% when 'cart' %}
      {{ 'cart.css' | asset_url | stylesheet_tag }}
  {% endcase %}
</head>

<body>
  {% comment %} Template-specific JavaScript {% endcomment %}
  {% case template.name %}
    {% when 'product' %}
      {{ 'product-zoom.js' | asset_url | script_tag: defer: true }}
    {% when 'collection' %}
      {{ 'collection-filters.js' | asset_url | script_tag: defer: true }}
  {% endcase %}
</body>
```

#### Device-Specific Loading
```liquid
<head>
  {% comment %} Load mobile-specific assets {% endcomment %}
  <script>
    if (window.innerWidth <= 749) {
      var mobileCSS = document.createElement('link');
      mobileCSS.rel = 'stylesheet';
      mobileCSS.href = '{{ "mobile.css" | asset_url }}';
      document.head.appendChild(mobileCSS);
    }
  </script>
</head>
```

## 🛠️ Common Customizations

### Theme Settings Integration
```liquid
<head>
  {% comment %} Dynamic CSS from theme settings {% endcomment %}
  <style>
    :root {
      --color-primary: {{ settings.color_primary }};
      --color-secondary: {{ settings.color_secondary }};
      --font-primary: {{ settings.font_primary.family }}, {{ settings.font_primary.fallback_families }};
      --border-radius: {{ settings.border_radius }}px;
    }
  </style>
</head>
```

### Third-Party Integrations
```liquid
<head>
  {% comment %} Google Analytics {% endcomment %}
  {% if settings.google_analytics_id != blank %}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ settings.google_analytics_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ settings.google_analytics_id }}');
    </script>
  {% endif %}
</head>
```

## 🚨 Common Pitfalls

### 1. Missing Required Objects
**Problem**: Theme won't save
**Solution**: Always include `{{ content_for_header }}` and `{{ content_for_layout }}`

### 2. Incorrect Object Placement
**Problem**: Scripts don't load properly
**Solution**: `content_for_header` in `<head>`, `content_for_layout` in `<body>`

### 3. Parsing content_for_header
**Problem**: Breaking Shopify functionality
**Solution**: Never modify or parse the content_for_header object

### 4. Missing Viewport Meta Tag
**Problem**: Poor mobile display
**Solution**: Always include `<meta name="viewport" content="width=device-width, initial-scale=1">`

## 📊 Performance Checklist

- [ ] Critical CSS inlined for above-the-fold content
- [ ] Non-critical CSS loaded asynchronously
- [ ] JavaScript deferred or loaded asynchronously
- [ ] Critical resources preloaded with `preload_tag`
- [ ] Fonts optimized with `font-display: swap`
- [ ] Images properly sized and lazy-loaded
- [ ] Third-party scripts loaded conditionally

## ♿ Accessibility Checklist

- [ ] Skip navigation link implemented
- [ ] Semantic HTML landmarks used (header, main, footer)
- [ ] Proper heading hierarchy maintained
- [ ] Focus indicators visible and styled
- [ ] Color contrast meets WCAG standards
- [ ] Touch targets minimum 44px × 44px

---

The `theme.liquid` file is the foundation of your theme's architecture. Following these patterns ensures a robust, performant, and accessible base for all your theme's pages.