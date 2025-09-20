# JavaScript Assets - Management and Optimization

JavaScript assets provide interactivity and dynamic behavior in Shopify themes. This guide covers modern JS patterns, bundling strategies, and performance optimization techniques for 2024-2025.

## 🎯 JavaScript Asset Types

### Core JavaScript Files
- **`theme.js`** - Main theme functionality
- **`section-*.js`** - Section-specific scripts
- **`component-*.js`** - Reusable component scripts
- **`vendor/`** - Third-party libraries
- **`modules/`** - ES6 modules for organization

### Specialized JavaScript Files
- **`cart.js`** - Shopping cart functionality
- **`product.js`** - Product page interactions
- **`search.js`** - Search and filtering
- **`analytics.js`** - Tracking and metrics

## 🏗️ JavaScript Organization Patterns

### File Structure
```
assets/
├── theme.js                  # Main entry point
├── cart-drawer.js           # Cart functionality
├── product-form.js          # Product interactions
├── search-overlay.js        # Search functionality
├── section-hero.js          # Section-specific JS
├── component-modal.js       # Reusable components
└── vendor/
    ├── swiper.min.js        # Third-party libraries
    └── lazysizes.min.js     # Performance libraries
```

### Module Architecture
```javascript
// theme.js - Main entry point
import { CartDrawer } from './modules/cart-drawer.js';
import { ProductForm } from './modules/product-form.js';
import { SearchOverlay } from './modules/search-overlay.js';
import { LazyLoader } from './modules/lazy-loader.js';

class Theme {
  constructor() {
    this.cartDrawer = new CartDrawer();
    this.productForm = new ProductForm();
    this.searchOverlay = new SearchOverlay();
    this.lazyLoader = new LazyLoader();

    this.init();
  }

  init() {
    this.cartDrawer.init();
    this.productForm.init();
    this.searchOverlay.init();
    this.lazyLoader.init();

    // Global event listeners
    this.bindEvents();
  }

  bindEvents() {
    document.addEventListener('shopify:section:load', this.onSectionLoad.bind(this));
    document.addEventListener('shopify:section:unload', this.onSectionUnload.bind(this));
  }

  onSectionLoad(event) {
    // Re-initialize components when sections are loaded via theme editor
    console.log('Section loaded:', event.detail.sectionId);
  }

  onSectionUnload(event) {
    // Cleanup when sections are removed
    console.log('Section unloaded:', event.detail.sectionId);
  }
}

// Initialize theme when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new Theme();
});
```

## 🚀 Shopify-Specific JavaScript Patterns

### Section and Block JavaScript
```liquid
<!-- Using Shopify's {% javascript %} tag for section-scoped JS -->
{% javascript %}
class HeroSection {
  constructor(container) {
    this.container = container;
    this.slider = container.querySelector('.hero__slider');
    this.init();
  }

  init() {
    if (this.slider) {
      this.initSlider();
    }
  }

  initSlider() {
    // Slider initialization logic
    const swiper = new Swiper(this.slider, {
      autoplay: {{ section.settings.autoplay | json }},
      speed: {{ section.settings.transition_speed | json }},
      loop: {{ section.settings.loop | json }}
    });
  }
}

// Auto-initialize when section loads
document.addEventListener('DOMContentLoaded', () => {
  const heroSections = document.querySelectorAll('.hero-section');
  heroSections.forEach(section => new HeroSection(section));
});

// Re-initialize for theme editor
document.addEventListener('shopify:section:load', (event) => {
  if (event.detail.sectionId.includes('hero')) {
    const section = event.target.querySelector('.hero-section');
    if (section) new HeroSection(section);
  }
});
{% endjavascript %}
```

### Liquid Preprocessing in JavaScript
```javascript
// theme.js.liquid - Dynamic JavaScript with Liquid
(function() {
  'use strict';

  // Theme settings accessible in JavaScript
  const themeSettings = {
    cartType: {{ settings.cart_type | json }},
    enableQuickAdd: {{ settings.enable_quick_add | json }},
    currencyFormat: {{ shop.money_format | json }},
    locale: {{ request.locale.iso_code | json }},
    routes: {
      cart: {{ routes.cart_url | json }},
      cartAdd: {{ routes.cart_add_url | json }},
      cartChange: {{ routes.cart_change_url | json }},
      search: {{ routes.search_url | json }}
    }
  };

  // Cart functionality
  class Cart {
    constructor() {
      this.settings = themeSettings;
      this.init();
    }

    async addItem(variantId, quantity = 1) {
      const response = await fetch(this.settings.routes.cartAdd, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          id: variantId,
          quantity: quantity
        })
      });

      return response.json();
    }

    async getCart() {
      const response = await fetch('/cart.js');
      return response.json();
    }
  }

  // Product functionality
  class Product {
    constructor() {
      this.currentVariant = {{ product.selected_or_first_available_variant | json }};
      this.variants = {{ product.variants | json }};
      this.init();
    }

    init() {
      this.bindVariantSelectors();
    }

    bindVariantSelectors() {
      const variantSelectors = document.querySelectorAll('[data-variant-selector]');
      variantSelectors.forEach(selector => {
        selector.addEventListener('change', this.onVariantChange.bind(this));
      });
    }

    onVariantChange(event) {
      const selectedOptions = this.getSelectedOptions();
      const variant = this.getVariantByOptions(selectedOptions);

      if (variant) {
        this.updatePrice(variant);
        this.updateInventory(variant);
        this.updateUrl(variant);
      }
    }
  }

  // Initialize based on template
  {% case template.name %}
    {% when 'product' %}
      new Product();
    {% when 'cart' %}
      new Cart();
  {% endcase %}

  // Global cart instance
  window.theme = window.theme || {};
  window.theme.cart = new Cart();

})();
```

## 🎯 Performance Optimization

### Bundle Size Optimization
```javascript
// Keep minified bundle under 16KB as recommended by Shopify
// Use dynamic imports for non-critical functionality

// theme.js - Critical functionality only
class ThemeCore {
  constructor() {
    this.initCritical();
  }

  initCritical() {
    // Only essential functionality here
    this.initNavigation();
    this.initAccessibility();
  }

  async loadCartFeatures() {
    // Lazy load cart functionality
    const { Cart } = await import('./modules/cart.js');
    this.cart = new Cart();
  }

  async loadProductFeatures() {
    // Lazy load product functionality
    const { ProductForm } = await import('./modules/product-form.js');
    this.productForm = new ProductForm();
  }
}

// Load additional features on demand
document.addEventListener('DOMContentLoaded', () => {
  const theme = new ThemeCore();

  // Load cart features when cart is first accessed
  document.addEventListener('click', async (e) => {
    if (e.target.closest('[data-cart-trigger]')) {
      await theme.loadCartFeatures();
    }
  });
});
```

### Async Loading Patterns
```javascript
// Avoid parser-blocking scripts
// Use defer for scripts that need DOM
// Use async for independent scripts

// Intersection Observer for performance
class LazyFeatures {
  constructor() {
    this.observer = new IntersectionObserver(this.onIntersect.bind(this));
    this.init();
  }

  init() {
    // Observe elements that trigger feature loading
    const triggers = document.querySelectorAll('[data-lazy-feature]');
    triggers.forEach(trigger => this.observer.observe(trigger));
  }

  async onIntersect(entries) {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const feature = entry.target.dataset.lazyFeature;
        await this.loadFeature(feature);
        this.observer.unobserve(entry.target);
      }
    }
  }

  async loadFeature(featureName) {
    switch (featureName) {
      case 'reviews':
        const { Reviews } = await import('./modules/reviews.js');
        new Reviews();
        break;
      case 'recommendations':
        const { Recommendations } = await import('./modules/recommendations.js');
        new Recommendations();
        break;
    }
  }
}
```

### Namespace Collision Prevention
```javascript
// Wrap code in IIFE to avoid global namespace pollution
(function(window, document, undefined) {
  'use strict';

  // Theme namespace
  const Theme = {
    // Configuration
    config: {
      namespace: 'shopify-theme',
      selectors: {
        cartDrawer: '[data-cart-drawer]',
        productForm: '[data-product-form]',
        searchToggle: '[data-search-toggle]'
      }
    },

    // Utilities
    utils: {
      debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
          const later = () => {
            clearTimeout(timeout);
            func(...args);
          };
          clearTimeout(timeout);
          timeout = setTimeout(later, wait);
        };
      },

      throttle: function(func, limit) {
        let inThrottle;
        return function() {
          const args = arguments;
          const context = this;
          if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
          }
        };
      }
    },

    // Initialize theme
    init: function() {
      this.bindEvents();
      this.initComponents();
    }
  };

  // Expose only what's needed globally
  window.Theme = Theme;

})(window, document);
```

## 🔧 Modern JavaScript Patterns

### ES6+ Features
```javascript
// Use modern JavaScript features for cleaner code
class ShoppingCart {
  constructor() {
    this.items = new Map();
    this.listeners = new Set();
  }

  // Async/await for API calls
  async addItem(variantId, quantity = 1) {
    try {
      const response = await fetch('/cart/add.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: variantId, quantity })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      this.updateCartUI(result);
      return result;
    } catch (error) {
      console.error('Error adding item to cart:', error);
      this.showError(error.message);
    }
  }

  // Destructuring and default parameters
  updateCartUI({ item_count = 0, total_price = 0 } = {}) {
    const cartCount = document.querySelector('[data-cart-count]');
    const cartTotal = document.querySelector('[data-cart-total]');

    cartCount?.textContent = item_count;
    cartTotal?.textContent = this.formatMoney(total_price);
  }

  // Template literals for cleaner string building
  formatMoney(cents) {
    const dollars = (cents / 100).toFixed(2);
    return `$${dollars}`;
  }

  // Spread operator for array manipulation
  getUniqueCategories(products) {
    return [...new Set(products.map(product => product.product_type))];
  }
}
```

### Event Delegation
```javascript
// Efficient event handling with delegation
class EventManager {
  constructor() {
    this.init();
  }

  init() {
    // Single event listener for all product forms
    document.addEventListener('submit', this.handleFormSubmit.bind(this));
    document.addEventListener('click', this.handleClick.bind(this));
    document.addEventListener('input', this.handleInput.bind(this));
  }

  handleFormSubmit(event) {
    const form = event.target;

    if (form.matches('[data-product-form]')) {
      event.preventDefault();
      this.handleProductFormSubmit(form);
    }
  }

  handleClick(event) {
    const target = event.target;

    // Cart drawer toggle
    if (target.matches('[data-cart-toggle]')) {
      event.preventDefault();
      this.toggleCartDrawer();
    }

    // Quick add buttons
    if (target.matches('[data-quick-add]')) {
      event.preventDefault();
      this.handleQuickAdd(target);
    }
  }

  handleInput(event) {
    const input = event.target;

    // Variant selectors
    if (input.matches('[data-variant-selector]')) {
      this.handleVariantChange(input);
    }

    // Search input
    if (input.matches('[data-search-input]')) {
      this.debounce(() => this.handleSearch(input.value), 300)();
    }
  }
}
```

## 📊 Performance Monitoring

### JavaScript Performance Metrics
```javascript
// Monitor performance metrics
class PerformanceMonitor {
  constructor() {
    this.metrics = {
      loadTime: 0,
      renderTime: 0,
      interactionTime: 0
    };
    this.init();
  }

  init() {
    // Measure initial load time
    window.addEventListener('load', () => {
      this.metrics.loadTime = performance.now();
      this.trackMetrics();
    });

    // Measure First Input Delay
    this.observeFirstInput();
  }

  observeFirstInput() {
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        this.metrics.interactionTime = entry.processingStart - entry.startTime;
      }
    }).observe({ type: 'first-input', buffered: true });
  }

  trackMetrics() {
    // Send metrics to analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'timing_complete', {
        name: 'JS_Load_Time',
        value: Math.round(this.metrics.loadTime)
      });
    }
  }
}
```

## 🚨 Common Pitfalls

### 1. Parser-Blocking Scripts
**Problem**: Scripts without defer/async block rendering
```html
<!-- Bad: Blocks parser -->
<script src="{{ 'theme.js' | asset_url }}"></script>

<!-- Good: Deferred loading -->
<script src="{{ 'theme.js' | asset_url }}" defer></script>
```

### 2. Memory Leaks
**Problem**: Event listeners not cleaned up
```javascript
// Bad: Memory leak in theme editor
function initSection() {
  document.addEventListener('scroll', handleScroll);
}

// Good: Cleanup listeners
function initSection() {
  const controller = new AbortController();
  document.addEventListener('scroll', handleScroll, {
    signal: controller.signal
  });

  // Cleanup when section unloads
  document.addEventListener('shopify:section:unload', () => {
    controller.abort();
  });
}
```

### 3. Large Bundle Sizes
**Problem**: Excessive JavaScript payloads
```javascript
// Bad: Loading everything upfront
import * as animations from './animations.js';
import * as socialMedia from './social-media.js';
import * as reviews from './reviews.js';

// Good: Dynamic imports
async function loadAnimations() {
  const { fadeIn, slideUp } = await import('./animations.js');
  return { fadeIn, slideUp };
}
```

## 🛠️ Development Tools

### Theme Check Integration
```yaml
# .theme-check.yml - JavaScript linting
JavaScriptOptimization:
  enabled: true
  severity: suggestion

AssetPreload:
  enabled: true
  severity: warning
```

### Modern Build Tools
```javascript
// webpack.config.js example for Shopify themes
const path = require('path');

module.exports = {
  entry: './src/theme.js',
  output: {
    path: path.resolve(__dirname, 'assets'),
    filename: 'theme.js'
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      maxSize: 16000 // Stay under 16KB limit
    }
  }
};
```

---

JavaScript assets should enhance user experience without compromising performance. Focus on progressive enhancement, efficient loading strategies, and maintaining compatibility with Shopify's theme editor.