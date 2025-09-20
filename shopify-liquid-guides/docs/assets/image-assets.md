# Image Assets - Optimization and Responsive Design

Image assets significantly impact theme performance and user experience. This guide covers modern image optimization techniques, responsive patterns, and best practices for Shopify themes.

## 🎯 Image Asset Types

### Content Images
- **Product images** - High-quality product photography
- **Collection images** - Category and collection banners
- **Hero images** - Homepage and landing page banners
- **Blog images** - Article featured images and content

### UI Images
- **Logo images** - Brand logos and variations
- **Icon images** - SVG icons and UI elements
- **Background images** - Decorative and pattern images
- **Placeholder images** - Default images for missing content

### Specialized Images
- **Favicon** - Browser tab and bookmark icons
- **Social media images** - Open Graph and Twitter cards
- **App icons** - PWA and mobile app icons

## 🏗️ Image Organization Patterns

### File Structure
```
assets/
├── logo.svg                 # Primary logo
├── logo-light.svg          # Light theme variant
├── favicon.ico             # Browser favicon
├── placeholder-product.svg  # Product placeholder
├── placeholder-collection.svg # Collection placeholder
├── hero-banner.jpg         # Homepage hero
├── about-team.jpg          # Static content images
└── icons/
    ├── cart.svg            # Shopping cart icon
    ├── search.svg          # Search icon
    └── arrow.svg           # Navigation arrows
```

### Shopify Image Processing
```liquid
<!-- Shopify automatically optimizes uploaded images -->
<!-- Original: hero-banner.jpg (2MB) -->
<!-- Processed: Multiple sizes with WebP support -->

{{ 'hero-banner.jpg' | image_url: width: 1200 }}
<!-- Outputs: hero-banner_1200x.jpg -->

{{ 'hero-banner.jpg' | image_url: width: 1200, format: 'webp' }}
<!-- Outputs: hero-banner_1200x.webp -->
```

## 🚀 Responsive Image Implementation

### Basic Responsive Images
```liquid
<!-- Single image with responsive sizing -->
<img src=\"{{ product.featured_image | image_url: width: 400 }}\"
     srcset=\"{{ product.featured_image | image_url: width: 400 }} 400w,
             {{ product.featured_image | image_url: width: 800 }} 800w,
             {{ product.featured_image | image_url: width: 1200 }} 1200w\"
     sizes=\"(max-width: 749px) 100vw, 50vw\"
     loading=\"lazy\"
     alt=\"{{ product.featured_image.alt | escape }}\"
     width=\"400\"
     height=\"{{ 400 | divided_by: product.featured_image.aspect_ratio | round }}\"
>
```

### Advanced Responsive Patterns
```liquid
<!-- Art direction with picture element -->
<picture>
  <!-- Mobile: Cropped to focus on product -->
  <source media=\"(max-width: 749px)\"
          srcset=\"{{ product.featured_image | image_url: width: 400, height: 400, crop: 'center' | image_url: format: 'webp' }} 400w,
                  {{ product.featured_image | image_url: width: 800, height: 800, crop: 'center' | image_url: format: 'webp' }} 800w\"
          type=\"image/webp\">

  <!-- Desktop: Full aspect ratio -->
  <source media=\"(min-width: 750px)\"
          srcset=\"{{ product.featured_image | image_url: width: 600 | image_url: format: 'webp' }} 600w,
                  {{ product.featured_image | image_url: width: 1200 | image_url: format: 'webp' }} 1200w\"
          type=\"image/webp\">

  <!-- Fallback for browsers without WebP support -->
  <img src=\"{{ product.featured_image | image_url: width: 600 }}\"
       srcset=\"{{ product.featured_image | image_url: width: 400 }} 400w,
               {{ product.featured_image | image_url: width: 800 }} 800w,
               {{ product.featured_image | image_url: width: 1200 }} 1200w\"
       sizes=\"(max-width: 749px) 100vw, 50vw\"
       loading=\"lazy\"
       alt=\"{{ product.featured_image.alt | escape }}\"
       width=\"600\"
       height=\"{{ 600 | divided_by: product.featured_image.aspect_ratio | round }}\">
</picture>
```

### Product Image Gallery
```liquid
<!-- Product image gallery with zoom -->
<div class=\"product__media-gallery\" data-media-gallery>
  {% for media in product.media limit: 6 %}
    {% case media.media_type %}
      {% when 'image' %}
        <div class=\"product__media-item\" data-media-id=\"{{ media.id }}\">
          <img src=\"{{ media | image_url: width: 800 }}\"
               srcset=\"{{ media | image_url: width: 400 }} 400w,
                       {{ media | image_url: width: 800 }} 800w,
                       {{ media | image_url: width: 1200 }} 1200w\"
               sizes=\"(max-width: 749px) 100vw, 60vw\"
               loading=\"{% if forloop.first %}eager{% else %}lazy{% endif %}\"
               alt=\"{{ media.alt | escape | default: product.title }}\"
               width=\"800\"
               height=\"{{ 800 | divided_by: media.aspect_ratio | round }}\"
               data-zoom-src=\"{{ media | image_url: width: 1600 }}\">
        </div>

      {% when 'video' %}
        <div class=\"product__media-item product__media-item--video\">
          <video controls preload=\"metadata\"
                 poster=\"{{ media.preview_image | image_url: width: 800 }}\">
            {% for source in media.sources %}
              <source src=\"{{ source.url }}\" type=\"{{ source.mime_type }}\">
            {% endfor %}
          </video>
        </div>
    {% endcase %}
  {% endfor %}
</div>

<!-- Thumbnail navigation -->
<div class=\"product__media-thumbnails\">
  {% for media in product.media limit: 6 %}
    <button class=\"product__media-thumbnail\"
            data-media-id=\"{{ media.id }}\"
            aria-label=\"View {{ media.media_type }}: {{ media.alt | escape | default: product.title }}\">
      <img src=\"{{ media | image_url: width: 100 }}\"
           alt=\"{{ media.alt | escape | default: product.title }}\"
           width=\"100\"
           height=\"{{ 100 | divided_by: media.aspect_ratio | round }}\">
    </button>
  {% endfor %}
</div>
```

## 🎨 Image Optimization Techniques

### WebP Implementation with Fallbacks
```liquid
<!-- WebP with JPEG fallback -->
<picture>
  <source srcset=\"{{ image | image_url: width: 800, format: 'webp' }} 800w,
                  {{ image | image_url: width: 1200, format: 'webp' }} 1200w\"
          type=\"image/webp\">
  <img src=\"{{ image | image_url: width: 800 }}\"
       srcset=\"{{ image | image_url: width: 800 }} 800w,
               {{ image | image_url: width: 1200 }} 1200w\"
       sizes=\"(max-width: 749px) 100vw, 50vw\"
       loading=\"lazy\"
       alt=\"{{ image.alt | escape }}\">
</picture>
```

### Lazy Loading Strategies
```liquid
<!-- Intersection Observer lazy loading -->
<img src=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E\"
     data-src=\"{{ image | image_url: width: 800 }}\"
     data-srcset=\"{{ image | image_url: width: 400 }} 400w,
                  {{ image | image_url: width: 800 }} 800w,
                  {{ image | image_url: width: 1200 }} 1200w\"
     data-sizes=\"(max-width: 749px) 100vw, 50vw\"
     class=\"lazy-image\"
     alt=\"{{ image.alt | escape }}\"
     width=\"800\"
     height=\"{{ 800 | divided_by: image.aspect_ratio | round }}\">

<script>
// JavaScript for lazy loading
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.srcset = img.dataset.srcset;
      img.sizes = img.dataset.sizes;
      img.classList.remove('lazy-image');
      imageObserver.unobserve(img);
    }
  });
});

document.querySelectorAll('.lazy-image').forEach(img => {
  imageObserver.observe(img);
});
</script>
```

### Critical Image Optimization
```liquid
<!-- Above-the-fold images: eager loading -->
{% if forloop.first or section.settings.critical_image %}
  <img src=\"{{ image | image_url: width: 800 }}\"
       srcset=\"{{ image | image_url: width: 400 }} 400w,
               {{ image | image_url: width: 800 }} 800w,
               {{ image | image_url: width: 1200 }} 1200w\"
       sizes=\"(max-width: 749px) 100vw, 50vw\"
       loading=\"eager\"
       fetchpriority=\"high\"
       alt=\"{{ image.alt | escape }}\">
{% else %}
  <!-- Below-the-fold images: lazy loading -->
  <img src=\"{{ image | image_url: width: 800 }}\"
       srcset=\"{{ image | image_url: width: 400 }} 400w,
               {{ image | image_url: width: 800 }} 800w,
               {{ image | image_url: width: 1200 }} 1200w\"
       sizes=\"(max-width: 749px) 100vw, 50vw\"
       loading=\"lazy\"
       alt=\"{{ image.alt | escape }}\">
{% endif %}
```

## 🔧 Advanced Image Patterns

### Dynamic Image Sizing
```liquid
<!-- Container-based responsive images -->
{% assign container_width = section.settings.container_width | default: 1200 %}
{% assign columns = section.settings.columns_desktop | default: 3 %}
{% assign image_width = container_width | divided_by: columns | round %}

<img src=\"{{ image | image_url: width: image_width }}\"
     srcset=\"{% for width in (200..1200) step: 200 %}
               {{ image | image_url: width: width }} {{ width }}w{% unless forloop.last %},{% endunless %}
             {% endfor %}\"
     sizes=\"(max-width: 749px) 100vw, {{ 100 | divided_by: columns }}vw\"
     loading=\"lazy\"
     alt=\"{{ image.alt | escape }}\">
```

### Aspect Ratio Preservation
```liquid
<!-- CSS aspect ratio with object-fit -->
<div class=\"image-container\" style=\"aspect-ratio: {{ image.aspect_ratio | default: 1.0 }}\">
  <img src=\"{{ image | image_url: width: 800 }}\"
       srcset=\"{{ image | image_url: width: 400 }} 400w,
               {{ image | image_url: width: 800 }} 800w\"
       sizes=\"(max-width: 749px) 100vw, 50vw\"
       loading=\"lazy\"
       alt=\"{{ image.alt | escape }}\"
       style=\"object-fit: {{ section.settings.image_fit | default: 'cover' }}\">
</div>

<style>
.image-container {
  overflow: hidden;
  border-radius: {{ section.settings.border_radius | default: 0 }}px;
}

.image-container img {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

.image-container:hover img {
  transform: scale({{ section.settings.hover_scale | default: 1.05 }});
}
</style>
```

### Placeholder Images
```liquid
<!-- SVG placeholder for missing images -->
{% assign placeholder_svg = '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 300 300\"><rect width=\"100%\" height=\"100%\" fill=\"#f8f8f8\"/><text x=\"50%\" y=\"50%\" text-anchor=\"middle\" dy=\".3em\" fill=\"#ccc\" font-family=\"sans-serif\" font-size=\"14\">No Image</text></svg>' %}

{% if product.featured_image %}
  <img src=\"{{ product.featured_image | image_url: width: 800 }}\"
       alt=\"{{ product.featured_image.alt | escape }}\">
{% else %}
  <img src=\"data:image/svg+xml,{{ placeholder_svg | url_encode }}\"
       alt=\"{{ product.title | escape }} - No image available\"
       width=\"800\"
       height=\"800\">
{% endif %}
```

## 📊 Performance Monitoring

### Image Performance Metrics
```javascript
// Monitor image loading performance
class ImagePerformanceMonitor {
  constructor() {
    this.metrics = {
      lcp: 0,
      imageLoadTimes: []
    };
    this.init();
  }

  init() {
    // Monitor Largest Contentful Paint
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (entry.element && entry.element.tagName === 'IMG') {
          this.metrics.lcp = entry.startTime;
        }
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true });

    // Monitor individual image load times
    document.querySelectorAll('img').forEach(img => {
      if (img.complete) {
        this.trackImageLoad(img, 0);
      } else {
        const startTime = performance.now();
        img.addEventListener('load', () => {
          const loadTime = performance.now() - startTime;
          this.trackImageLoad(img, loadTime);
        });
      }
    });
  }

  trackImageLoad(img, loadTime) {
    this.metrics.imageLoadTimes.push({
      src: img.src,
      loadTime: loadTime,
      size: img.naturalWidth * img.naturalHeight
    });
  }
}
```

### Image Optimization Checklist
```liquid
<!-- Image optimization validation -->
{% comment %}
  Checklist for optimal image implementation:
  ✓ Responsive srcset with multiple sizes
  ✓ Appropriate sizes attribute
  ✓ Lazy loading for below-the-fold images
  ✓ WebP format with fallbacks
  ✓ Proper alt text for accessibility
  ✓ Width and height attributes to prevent layout shift
  ✓ Aspect ratio preservation
{% endcomment %}

<img src=\"{{ image | image_url: width: 800 }}\"
     srcset=\"{{ image | image_url: width: 400 }} 400w,
             {{ image | image_url: width: 800 }} 800w,
             {{ image | image_url: width: 1200 }} 1200w\"
     sizes=\"(max-width: 749px) 100vw, 50vw\"
     loading=\"lazy\"
     alt=\"{{ image.alt | escape | default: 'Product image' }}\"
     width=\"800\"
     height=\"{{ 800 | divided_by: image.aspect_ratio | round }}\"
     style=\"aspect-ratio: {{ image.aspect_ratio | default: 1.0 }}\">
```

## 🚨 Common Pitfalls

### 1. Missing Alt Text
**Problem**: Inaccessible images for screen readers
```liquid
<!-- Bad: Missing alt text -->
<img src=\"{{ image | image_url: width: 800 }}\">

<!-- Good: Descriptive alt text -->
<img src=\"{{ image | image_url: width: 800 }}\"
     alt=\"{{ image.alt | escape | default: product.title | escape }}\">
```

### 2. Layout Shift Issues
**Problem**: Images without dimensions cause layout shift
```liquid
<!-- Bad: No width/height specified -->
<img src=\"{{ image | image_url: width: 800 }}\"
     alt=\"{{ image.alt | escape }}\">

<!-- Good: Dimensions specified -->
<img src=\"{{ image | image_url: width: 800 }}\"
     alt=\"{{ image.alt | escape }}\"
     width=\"800\"
     height=\"{{ 800 | divided_by: image.aspect_ratio | round }}\"
     style=\"aspect-ratio: {{ image.aspect_ratio }}\">
```

### 3. Oversized Images
**Problem**: Serving huge images for small displays
```liquid
<!-- Bad: Same large image for all devices -->
<img src=\"{{ image | image_url: width: 2000 }}\" alt=\"{{ image.alt | escape }}\">

<!-- Good: Responsive image sizes -->
<img src=\"{{ image | image_url: width: 800 }}\"
     srcset=\"{{ image | image_url: width: 400 }} 400w,
             {{ image | image_url: width: 800 }} 800w,
             {{ image | image_url: width: 1200 }} 1200w\"
     sizes=\"(max-width: 749px) 100vw, 50vw\"
     alt=\"{{ image.alt | escape }}\">
```

### 4. Blocking Critical Render Path
**Problem**: Above-the-fold images with lazy loading
```liquid
<!-- Bad: Hero image with lazy loading -->
<img src=\"{{ section.settings.hero_image | image_url: width: 1200 }}\"
     loading=\"lazy\"
     alt=\"{{ section.settings.hero_image.alt | escape }}\">

<!-- Good: Hero image with eager loading -->
<img src=\"{{ section.settings.hero_image | image_url: width: 1200 }}\"
     loading=\"eager\"
     fetchpriority=\"high\"
     alt=\"{{ section.settings.hero_image.alt | escape }}\">
```

## 🛠️ Development Tools

### Image Format Detection
```javascript
// Detect WebP support
function supportsWebP() {
  return new Promise(resolve => {
    const webP = new Image();
    webP.onload = webP.onerror = () => resolve(webP.height === 2);
    webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
  });
}

// Progressive enhancement for WebP
supportsWebP().then(supported => {
  if (supported) {
    document.documentElement.classList.add('webp');
  }
});
```

### Image Compression Guidelines
```yaml
# Image optimization guidelines
JPEG:
  quality: 85-90
  progressive: true
  use_for: photos, complex images

PNG:
  compression: 9
  use_for: graphics, logos, transparency

WebP:
  quality: 80-85
  use_for: all images (with fallbacks)

SVG:
  minify: true
  use_for: icons, simple graphics
```

---

Image optimization is crucial for Core Web Vitals and user experience. Focus on responsive delivery, modern formats, and appropriate loading strategies to create fast, accessible themes.