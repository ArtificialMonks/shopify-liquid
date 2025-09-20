# Font Assets - Typography and Performance

Font assets define your theme's typography and significantly impact both visual design and loading performance. This guide covers modern font loading strategies, optimization techniques, and accessibility considerations.

## 🎯 Font Asset Types

### System Fonts
- **System UI** - Platform-native fonts (fastest loading)
- **Web Safe Fonts** - Universally available fonts
- **Font Stacks** - Fallback chains for reliability

### Web Fonts
- **Brand fonts** - Custom typography for brand identity
- **Icon fonts** - Font-based icon systems
- **Variable fonts** - Single files with multiple weights/styles

### Font Formats
- **WOFF2** - Modern, compressed format (recommended)
- **WOFF** - Fallback for older browsers
- **TTF/OTF** - Legacy formats (avoid for web)

## 🏗️ Font Organization Patterns

### File Structure
```
assets/
├── fonts/
│   ├── brand-font-regular.woff2
│   ├── brand-font-bold.woff2
│   ├── brand-font-italic.woff2
│   └── brand-font-variable.woff2
├── font-face.css
└── typography.css
```

### CSS Font Organization
```css
/* font-face.css - Font definitions */
@font-face {
  font-family: 'Brand Font';
  src: url('{{ "brand-font-regular.woff2" | asset_url }}') format('woff2'),
       url('{{ "brand-font-regular.woff" | asset_url }}') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Brand Font';
  src: url('{{ "brand-font-bold.woff2" | asset_url }}') format('woff2'),
       url('{{ "brand-font-bold.woff" | asset_url }}') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* Variable font implementation */
@font-face {
  font-family: 'Brand Variable';
  src: url('{{ "brand-font-variable.woff2" | asset_url }}') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal oblique 20deg;
  font-display: swap;
}
```

## 🚀 Font Loading Strategies

### System Font Implementation
```css
/* theme.css.liquid - System font stack */
:root {
  /* System font stacks for optimal performance */
  --font-system: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                  'Helvetica Neue', Arial, sans-serif;
  --font-system-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono',
                       Consolas, 'Courier New', monospace;

  /* Theme settings integration */
  --font-heading: {{ settings.font_heading.family | default: 'var(--font-system)' }},
                  {{ settings.font_heading.fallback_families }};
  --font-body: {{ settings.font_body.family | default: 'var(--font-system)' }},
               {{ settings.font_body.fallback_families }};
}

body {
  font-family: var(--font-body);
  font-weight: {{ settings.font_body.weight | default: 400 }};
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: {{ settings.font_heading.weight | default: 700 }};
}
```

### Web Font Loading with Performance
```liquid
<!-- theme.liquid - Optimized font loading -->
<head>
  <!-- Preload critical fonts -->
  {% if settings.font_heading.family contains 'woff2' %}
    <link rel="preload"
          href="{{ settings.font_heading.family | split: 'url(' | last | split: ')' | first | remove: '"' | remove: "'" }}"
          as="font"
          type="font/woff2"
          crossorigin>
  {% endif %}

  <!-- Font face CSS -->
  <style>
    {{ 'font-face.css' | asset_url | asset_content }}
  </style>

  <!-- Critical typography CSS inline -->
  <style>
    :root {
      --font-heading: {{ settings.font_heading.family }}, {{ settings.font_heading.fallback_families }};
      --font-body: {{ settings.font_body.family }}, {{ settings.font_body.fallback_families }};
    }

    body {
      font-family: var(--font-body);
      font-size: {{ settings.font_size_base | default: 16 }}px;
      line-height: {{ settings.line_height_base | default: 1.5 }};
    }

    h1, h2, h3, h4, h5, h6 {
      font-family: var(--font-heading);
      line-height: {{ settings.line_height_headings | default: 1.2 }};
    }
  </style>
</head>
```

### Font Display Strategies
```css
/* Different font-display strategies for different use cases */

/* Critical text - swap immediately */
@font-face {
  font-family: 'Heading Font';
  src: url('heading-font.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately, swap when loaded */
}

/* Decorative text - optional loading */
@font-face {
  font-family: 'Decorative Font';
  src: url('decorative-font.woff2') format('woff2');
  font-display: optional; /* Only use if already cached */
}

/* Icon fonts - block briefly then fallback */
@font-face {
  font-family: 'Icon Font';
  src: url('icon-font.woff2') format('woff2');
  font-display: block; /* Block briefly, then show fallback */
}
```

## 🎨 Typography Scale and Variables

### Responsive Typography Scale
```css
/* theme.css.liquid - Fluid typography */
:root {
  /* Base font sizes from theme settings */
  --font-size-base: {{ settings.font_size_base | default: 16 }}px;

  /* Modular scale for typography */
  --font-scale: {{ settings.font_scale | default: 1.25 }};

  /* Calculated font sizes */
  --font-size-xs: calc(var(--font-size-base) / var(--font-scale) / var(--font-scale));
  --font-size-sm: calc(var(--font-size-base) / var(--font-scale));
  --font-size-md: var(--font-size-base);
  --font-size-lg: calc(var(--font-size-base) * var(--font-scale));
  --font-size-xl: calc(var(--font-size-base) * var(--font-scale) * var(--font-scale));
  --font-size-2xl: calc(var(--font-size-base) * var(--font-scale) * var(--font-scale) * var(--font-scale));

  /* Responsive font sizes using clamp() */
  --font-size-h1: clamp(2rem, 4vw, 3.5rem);
  --font-size-h2: clamp(1.75rem, 3.5vw, 2.5rem);
  --font-size-h3: clamp(1.5rem, 3vw, 2rem);
  --font-size-h4: clamp(1.25rem, 2.5vw, 1.5rem);

  /* Line heights */
  --line-height-tight: 1.1;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}

/* Typography classes */
.text-xs { font-size: var(--font-size-xs); }
.text-sm { font-size: var(--font-size-sm); }
.text-base { font-size: var(--font-size-md); }
.text-lg { font-size: var(--font-size-lg); }
.text-xl { font-size: var(--font-size-xl); }
.text-2xl { font-size: var(--font-size-2xl); }

/* Heading styles */
h1 {
  font-size: var(--font-size-h1);
  line-height: var(--line-height-tight);
}

h2 {
  font-size: var(--font-size-h2);
  line-height: var(--line-height-tight);
}

h3 {
  font-size: var(--font-size-h3);
  line-height: var(--line-height-normal);
}
```

### Variable Font Implementation
```css
/* Variable font with responsive weight and width */
@font-face {
  font-family: 'InterVariable';
  src: url('{{ "inter-variable.woff2" | asset_url }}') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

:root {
  /* Variable font axes */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Responsive font weight */
  --font-weight-responsive: clamp(400, 50vw, 600);
}

.heading-variable {
  font-family: 'InterVariable', var(--font-system);
  font-weight: var(--font-weight-responsive);
  font-variation-settings: 'wght' var(--font-weight-responsive);
}

/* Responsive font weight based on screen size */
@media (max-width: 767px) {
  .heading-variable {
    --font-weight-responsive: 400;
  }
}

@media (min-width: 768px) {
  .heading-variable {
    --font-weight-responsive: 600;
  }
}
```

## 🔧 Advanced Font Techniques

### Font Loading Detection
```javascript
// JavaScript for font loading optimization
class FontLoader {
  constructor() {
    this.fonts = [
      { family: 'Brand Font', weight: '400' },
      { family: 'Brand Font', weight: '700' }
    ];
    this.init();
  }

  async init() {
    // Check if Font Loading API is supported
    if ('fonts' in document) {
      await this.loadFonts();
    } else {
      // Fallback for older browsers
      this.loadFontsFallback();
    }
  }

  async loadFonts() {
    try {
      // Load fonts using Font Loading API
      const fontPromises = this.fonts.map(font =>
        document.fonts.load(`${font.weight} 16px "${font.family}"`)
      );

      await Promise.all(fontPromises);
      document.documentElement.classList.add('fonts-loaded');
    } catch (error) {
      console.warn('Font loading failed:', error);
    }
  }

  loadFontsFallback() {
    // Create test elements to detect font loading
    const testElements = this.fonts.map(font => {
      const element = document.createElement('div');
      element.style.fontFamily = `"${font.family}", monospace`;
      element.style.fontWeight = font.weight;
      element.style.position = 'absolute';
      element.style.left = '-9999px';
      element.textContent = 'Font loading test';
      document.body.appendChild(element);
      return element;
    });

    // Check if fonts have loaded
    setTimeout(() => {
      document.documentElement.classList.add('fonts-loaded');
      testElements.forEach(el => document.body.removeChild(el));
    }, 3000); // Timeout after 3 seconds
  }
}

// Initialize font loader
new FontLoader();
```

### Critical Font Inlining
```liquid
<!-- Inline critical font data to avoid FOIT -->
{% if settings.inline_critical_fonts %}
  <style>
    @font-face {
      font-family: 'Critical Font';
      src: url(data:font/woff2;base64,{{ 'critical-font.woff2' | asset_url | base64_encode }}) format('woff2');
      font-display: block;
    }

    .critical-text {
      font-family: 'Critical Font', {{ settings.font_body.fallback_families }};
    }
  </style>
{% endif %}
```

### Font Subsetting
```css
/* Load only required character sets */
@font-face {
  font-family: 'Optimized Font';
  src: url('{{ "font-latin.woff2" | asset_url }}') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
  font-display: swap;
}

@font-face {
  font-family: 'Optimized Font';
  src: url('{{ "font-extended.woff2" | asset_url }}') format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
  font-display: swap;
}
```

## 📊 Font Performance Optimization

### Performance Metrics
```javascript
// Monitor font loading performance
class FontPerformanceMonitor {
  constructor() {
    this.metrics = {
      fontLoadTime: 0,
      layoutShift: 0,
      renderBlocking: false
    };
    this.init();
  }

  init() {
    // Monitor font loading time
    if ('fonts' in document) {
      const startTime = performance.now();

      document.fonts.ready.then(() => {
        this.metrics.fontLoadTime = performance.now() - startTime;
        this.trackMetrics();
      });
    }

    // Monitor layout shift caused by font swapping
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          this.metrics.layoutShift += entry.value;
        }
      }
    }).observe({ type: 'layout-shift', buffered: true });
  }

  trackMetrics() {
    // Send metrics to analytics
    console.log('Font Performance:', {
      loadTime: this.metrics.fontLoadTime,
      layoutShift: this.metrics.layoutShift
    });
  }
}
```

### Font Loading Optimization
```css
/* Optimize font loading for performance */

/* Preload critical fonts */
/* <link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin> */

/* Use font-display strategies appropriately */
@font-face {
  font-family: 'Logo Font';
  src: url('logo-font.woff2') format('woff2');
  font-display: block; /* Logo text should wait for font */
}

@font-face {
  font-family: 'Body Font';
  src: url('body-font.woff2') format('woff2');
  font-display: swap; /* Body text should swap immediately */
}

@font-face {
  font-family: 'Decorative Font';
  src: url('decorative-font.woff2') format('woff2');
  font-display: optional; /* Only use if already loaded */
}

/* Reduce layout shift with size-adjust */
@font-face {
  font-family: 'Web Font';
  src: url('web-font.woff2') format('woff2');
  size-adjust: 90%; /* Adjust to match fallback font metrics */
  font-display: swap;
}
```

## 🎯 Accessibility Considerations

### Font Size and Readability
```css
/* Accessible font sizing */
:root {
  /* Minimum font sizes for accessibility */
  --font-size-min: 16px; /* Never go below 16px for body text */
  --line-height-min: 1.5; /* Minimum line height for readability */

  /* High contrast mode support */
  --color-text-high-contrast: #000000;
  --color-background-high-contrast: #ffffff;
}

/* Ensure minimum font sizes */
body {
  font-size: max(16px, var(--font-size-base));
  line-height: max(1.5, var(--line-height-base));
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
  }
}

@media (prefers-contrast: high) {
  :root {
    --color-text: var(--color-text-high-contrast);
    --color-background: var(--color-background-high-contrast);
  }
}

/* Font size scaling for user preferences */
html {
  font-size: 100%; /* Respect user's browser font size setting */
}
```

### Screen Reader Compatibility
```css
/* Ensure text remains readable when fonts fail to load */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Icon fonts accessibility */
.icon-font {
  font-family: 'Icon Font', 'Arial'; /* Fallback to readable font */
  speak: none; /* Prevent screen readers from attempting to pronounce */
}

.icon-font::before {
  /* Add aria-hidden to decorative icons */
  display: inline-block;
}
```

## 🚨 Common Pitfalls

### 1. Flash of Invisible Text (FOIT)
**Problem**: Text hidden while fonts load
```css
/* Bad: Default font-display behavior */
@font-face {
  font-family: 'Custom Font';
  src: url('font.woff2') format('woff2');
  /* Missing font-display causes FOIT */
}

/* Good: Immediate fallback */
@font-face {
  font-family: 'Custom Font';
  src: url('font.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately */
}
```

### 2. Excessive Font Loading
**Problem**: Too many font variants slow loading
```css
/* Bad: Loading unnecessary font weights */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700;800;900');

/* Good: Load only needed weights */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700');
```

### 3. Missing Fallback Fonts
**Problem**: Poor experience when custom fonts fail
```css
/* Bad: No fallback fonts */
h1 {
  font-family: 'Custom Font';
}

/* Good: Comprehensive fallback stack */
h1 {
  font-family: 'Custom Font', 'Helvetica Neue', Arial, sans-serif;
}
```

### 4. Inaccessible Font Sizes
**Problem**: Font sizes too small for accessibility
```css
/* Bad: Tiny font sizes */
.caption {
  font-size: 12px; /* Too small */
}

/* Good: Accessible minimum sizes */
.caption {
  font-size: max(14px, 0.875rem); /* Minimum 14px */
}
```

## 🛠️ Development Tools

### Font Analysis Tools
```javascript
// Analyze loaded fonts
function analyzeFonts() {
  if ('fonts' in document) {
    document.fonts.forEach(font => {
      console.log(`Font: ${font.family} ${font.weight} ${font.style}`);
      console.log(`Status: ${font.status}`);
    });
  }
}

// Test font loading performance
function testFontPerformance() {
  const fonts = ['Brand Font', 'Body Font'];

  fonts.forEach(async (fontFamily) => {
    const startTime = performance.now();

    try {
      await document.fonts.load(`16px "${fontFamily}"`);
      const loadTime = performance.now() - startTime;
      console.log(`${fontFamily} loaded in ${loadTime.toFixed(2)}ms`);
    } catch (error) {
      console.error(`Failed to load ${fontFamily}:`, error);
    }
  });
}
```

### Font Optimization Workflow
```yaml
# Font optimization checklist
font_optimization:
  format: WOFF2 (primary), WOFF (fallback)
  compression: Maximum compression ratio
  subsetting: Include only required character sets
  variable_fonts: Use when multiple weights needed
  preload: Only critical fonts
  fallback_fonts: Always include system font fallbacks
  font_display: swap (for most cases)
  size_limit: Keep total font payload under 100KB
```

---

Font assets are crucial for brand identity and user experience. Balance visual design with performance by using appropriate loading strategies, system font fallbacks, and accessibility best practices.