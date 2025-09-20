# Shopify Locales Documentation

Locale files enable theme internationalization and translation, allowing themes to support multiple languages and regions. This documentation covers locale file structure, translation patterns, and best practices for creating multilingual Shopify themes.

## 📁 What's in This Section

### Core Documentation
| File | Purpose | What You'll Learn |
|------|---------|-------------------|
| **[translation-system.md](./translation-system.md)** | Translation implementation | How Shopify's translation system works |
| **[locale-file-structure.md](./locale-file-structure.md)** | JSON locale organization | Structuring translation files |
| **[pluralization-rules.md](./pluralization-rules.md)** | Plural form handling | Complex plural rules across languages |
| **[regional-formatting.md](./regional-formatting.md)** | Date, number, currency formats | Regional formatting patterns |

### Practical Resources
| Directory | Purpose | Contents |
|-----------|---------|----------|
| **[examples/](./examples/)** | Working locale files | Complete translation examples, regional formats |

## 🎯 Quick Start

### For Beginners
1. Start with **[translation-system.md](./translation-system.md)** to understand Shopify's translation approach
2. Review **[locale-file-structure.md](./locale-file-structure.md)** for file organization
3. Study **[examples/](./examples/)** for practical implementations

### For Experienced Developers
- Jump to **[pluralization-rules.md](./pluralization-rules.md)** for complex language rules
- Browse **[regional-formatting.md](./regional-formatting.md)** for formatting patterns
- Reference **[examples/](./examples/)** for production-ready translations

## 📋 Locales System Overview

### Purpose and Function
Locale files enable:
- **Multi-language support** - Translate theme text into different languages
- **Regional customization** - Adapt formatting for different regions
- **Merchant localization** - Allow store-specific translations
- **Dynamic language switching** - Runtime language selection

### File Structure
```
locales/
├── en.default.json          # Default English translations
├── en.json                  # English translations
├── es.json                  # Spanish translations
├── fr.json                  # French translations
├── de.json                  # German translations
└── ja.json                  # Japanese translations
```

### Translation Scope
- **Theme text** - Static text in templates
- **Section settings** - Setting labels and descriptions
- **Error messages** - User-facing error text
- **Form labels** - Input and button text
- **Accessibility text** - Screen reader content

## 🏗️ Basic Locale File Structure

### Standard Translation Format
```json
{
  "general": {
    "meta": {
      "title": "Welcome to {{ shop.name }}",
      "description": "Discover amazing products at great prices"
    },
    "navigation": {
      "home": "Home",
      "shop": "Shop",
      "about": "About",
      "contact": "Contact"
    },
    "buttons": {
      "add_to_cart": "Add to cart",
      "buy_now": "Buy now",
      "view_details": "View details",
      "continue_shopping": "Continue shopping"
    }
  },
  "products": {
    "general": {
      "price": "Price",
      "sale_price": "Sale price",
      "regular_price": "Regular price",
      "vendor": "Vendor",
      "availability": "Availability"
    },
    "form": {
      "quantity": "Quantity",
      "variant": "Variant",
      "add_to_cart": "Add to cart",
      "sold_out": "Sold out",
      "unavailable": "Unavailable"
    }
  }
}
```

### Hierarchical Organization
```json
{
  "cart": {
    "general": {
      "title": "Shopping Cart",
      "empty": "Your cart is empty",
      "continue_shopping": "Continue shopping"
    },
    "item": {
      "quantity": "Quantity",
      "price": "Price",
      "total": "Total",
      "remove": "Remove"
    },
    "checkout": {
      "button": "Checkout",
      "subtotal": "Subtotal",
      "shipping": "Shipping",
      "tax": "Tax",
      "total": "Total"
    }
  }
}
```

## 🚀 Translation Implementation

### Basic Translation Usage
```liquid
<!-- Simple text translation -->
<h1>{{ 'general.navigation.home' | t }}</h1>

<!-- Translation with variables -->
<p>{{ 'general.meta.title' | t: shop_name: shop.name }}</p>

<!-- Translation with default fallback -->
<span>{{ 'products.general.vendor' | t | default: 'Brand' }}</span>
```

### Dynamic Translation Keys
```liquid
<!-- Dynamic key construction -->
{% assign status_key = 'products.form.' | append: product.available %}
<span class="status">{{ status_key | t }}</span>

<!-- Template-specific translations -->
{% assign page_title_key = 'templates.' | append: template.name | append: '.title' %}
<title>{{ page_title_key | t | default: shop.name }}</title>
```

### Pluralization Handling
```liquid
<!-- Count-based pluralization -->
{% assign item_count = cart.item_count %}
<span>{{ 'cart.general.item_count' | t: count: item_count }}</span>

<!-- Zero, one, other handling -->
{% if collection.products_count == 0 %}
  {{ 'collections.general.no_products' | t }}
{% elsif collection.products_count == 1 %}
  {{ 'collections.general.one_product' | t }}
{% else %}
  {{ 'collections.general.other_products' | t: count: collection.products_count }}
{% endif %}
```

## 🎨 Advanced Translation Patterns

### Section-Specific Translations
```json
{
  "sections": {
    "header": {
      "search_placeholder": "Search products...",
      "account_link": "Account",
      "cart_link": "Cart ({{ count }})"
    },
    "footer": {
      "newsletter_title": "Stay updated",
      "newsletter_subtitle": "Subscribe for exclusive offers",
      "social_media_title": "Follow us"
    },
    "product_card": {
      "quick_add": "Quick add",
      "choose_options": "Choose options",
      "sale_badge": "Sale",
      "new_badge": "New"
    }
  }
}
```

### Form Translations
```json
{
  "customer": {
    "login": {
      "title": "Sign in",
      "email_label": "Email address",
      "password_label": "Password",
      "submit_button": "Sign in",
      "forgot_password": "Forgot password?",
      "create_account": "Create account"
    },
    "register": {
      "title": "Create account",
      "first_name_label": "First name",
      "last_name_label": "Last name",
      "email_label": "Email address",
      "password_label": "Password",
      "submit_button": "Create account"
    }
  }
}
```

### Error Message Translations
```json
{
  "errors": {
    "general": {
      "required_field": "This field is required",
      "invalid_email": "Please enter a valid email address",
      "password_too_short": "Password must be at least 6 characters",
      "generic_error": "Something went wrong. Please try again."
    },
    "cart": {
      "item_not_available": "This item is no longer available",
      "quantity_exceeded": "Not enough items in stock",
      "add_to_cart_failed": "Could not add item to cart"
    },
    "checkout": {
      "shipping_required": "Please select a shipping method",
      "payment_failed": "Payment could not be processed",
      "address_invalid": "Please check your address details"
    }
  }
}
```

## 🌍 Regional Formatting

### Date and Time Formatting
```json
{
  "date_formats": {
    "short": "%b %d",
    "long": "%B %d, %Y",
    "month_day_year": "%m/%d/%Y"
  },
  "time_formats": {
    "12_hour": "%I:%M %p",
    "24_hour": "%H:%M"
  }
}
```

### Number and Currency Formatting
```json
{
  "number_formats": {
    "decimal_separator": ".",
    "thousands_separator": ",",
    "currency_format": "${{ amount }}",
    "currency_code": "USD"
  }
}
```

### Address Formatting
```json
{
  "addresses": {
    "labels": {
      "company": "Company",
      "first_name": "First name",
      "last_name": "Last name",
      "address1": "Address",
      "address2": "Apartment, suite, etc.",
      "city": "City",
      "province": "State",
      "zip": "ZIP code",
      "country": "Country",
      "phone": "Phone"
    },
    "format": {
      "street_first": true,
      "postal_code_position": "after_city"
    }
  }
}
```

## 📱 Responsive and Accessibility Translations

### Screen Reader Content
```json
{
  "accessibility": {
    "skip_to_content": "Skip to content",
    "close_dialog": "Close dialog",
    "open_menu": "Open navigation menu",
    "close_menu": "Close navigation menu",
    "product_image": "Product image",
    "loading": "Loading...",
    "error": "Error occurred"
  }
}
```

### Mobile-Specific Text
```json
{
  "mobile": {
    "navigation": {
      "menu": "Menu",
      "search": "Search",
      "account": "Account",
      "cart": "Cart"
    },
    "buttons": {
      "tap_to_call": "Tap to call",
      "view_more": "View more",
      "show_less": "Show less"
    }
  }
}
```

## 🔧 Translation Management

### Translation Key Naming
```json
{
  // ✅ Good: Hierarchical, descriptive
  "products": {
    "form": {
      "add_to_cart_button": "Add to cart",
      "quantity_label": "Quantity",
      "variant_selector_label": "Select variant"
    }
  },

  // ❌ Bad: Flat, unclear
  "btn_text": "Add to cart",
  "qty": "Quantity",
  "var": "Select variant"
}
```

### Translation Variables
```liquid
<!-- Using variables in translations -->
{% assign product_title = product.title | escape %}
<h1>{{ 'products.general.title_with_vendor' | t: title: product_title, vendor: product.vendor }}</h1>

<!-- Complex variable substitution -->
{% assign discount_percent = product.compare_at_price | minus: product.price | times: 100 | divided_by: product.compare_at_price %}
<span>{{ 'products.general.save_percent' | t: percent: discount_percent }}</span>
```

### Fallback Strategies
```liquid
<!-- Fallback to default locale -->
{{ 'custom.translation.key' | t | default: 'Default text' }}

<!-- Fallback to English if current locale missing -->
{{ 'products.general.title' | t | default: 'products.general.title' | t: locale: 'en' }}

<!-- Template-specific fallback -->
{% assign template_key = 'templates.' | append: template.name | append: '.heading' %}
{{ template_key | t | default: 'general.headings.default' | t }}
```

## 📊 Multi-Language Implementation

### Language Selector
```liquid
<!-- Language selector dropdown -->
<div class="language-selector">
  <label for="language-select">{{ 'general.language.select' | t }}</label>
  <select id="language-select" onchange="changeLanguage(this.value)">
    {% for locale in shop.published_locales %}
      <option value="{{ locale.iso_code }}" {% if locale.iso_code == request.locale.iso_code %}selected{% endif %}>
        {{ locale.endonym_name }}
      </option>
    {% endfor %}
  </select>
</div>

<script>
function changeLanguage(localeCode) {
  const url = new URL(window.location);
  url.searchParams.set('locale', localeCode);
  window.location.href = url.toString();
}
</script>
```

### URL Structure for Locales
```liquid
<!-- Locale-aware URLs -->
<nav>
  {% for link in linklists.main-menu.links %}
    <a href="{{ link.url | localized_url }}"
       {% if link.active %}aria-current="page"{% endif %}>
      {{ link.title }}
    </a>
  {% endfor %}
</nav>

<!-- Canonical and alternate URLs -->
<link rel="canonical" href="{{ canonical_url | localized_url }}">
{% for locale in shop.published_locales %}
  {% unless locale.iso_code == request.locale.iso_code %}
    <link rel="alternate" hreflang="{{ locale.iso_code }}" href="{{ canonical_url | localized_url: locale }}">
  {% endunless %}
{% endfor %}
```

## 🚨 Common Localization Pitfalls

### 1. Hard-coded Text
**Problem**: Text not using translation filters
```liquid
<!-- ❌ Bad: Hard-coded text -->
<button>Add to cart</button>

<!-- ✅ Good: Translated text -->
<button>{{ 'products.form.add_to_cart' | t }}</button>
```

### 2. Missing Translation Keys
**Problem**: Undefined translation keys
```liquid
<!-- ❌ Bad: Will show key instead of text -->
{{ 'undefined.translation.key' | t }}

<!-- ✅ Good: With fallback -->
{{ 'undefined.translation.key' | t | default: 'Default text' }}
```

### 3. Improper Pluralization
**Problem**: Not handling plural forms correctly
```json
{
  // ❌ Bad: No plural handling
  "item_count": "{{ count }} items"
}
```

```json
{
  // ✅ Good: Proper pluralization
  "item_count": {
    "zero": "No items",
    "one": "{{ count }} item",
    "other": "{{ count }} items"
  }
}
```

### 4. Variable Escaping Issues
**Problem**: Not properly escaping variables in translations
```json
{
  // ❌ Bad: Variables not properly handled
  "welcome_message": "Welcome {{ customer.name }}!"
}
```

```liquid
<!-- ✅ Good: Proper escaping -->
{{ 'general.welcome_message' | t: name: customer.name | escape }}
```

## 🛠️ Development Workflow

### Translation Development Process
1. **Audit existing text** - Identify all hard-coded strings
2. **Create translation keys** - Design logical key hierarchy
3. **Build default locale** - Create comprehensive en.default.json
4. **Implement translation calls** - Update templates with | t filters
5. **Test language switching** - Verify all translations work
6. **Add additional locales** - Create files for target languages

### Translation Testing
```liquid
<!-- Test translation with debug mode -->
{% if settings.translation_debug_mode %}
  <div class="translation-debug">
    Key: {{ 'products.form.add_to_cart' }}
    Value: {{ 'products.form.add_to_cart' | t }}
  </div>
{% endif %}
```

### Translation Validation
```bash
# Validate JSON syntax
npx jsonlint locales/en.default.json

# Check for missing translations
shopify theme check

# Test translation coverage
shopify theme dev --locale=es
```

---

Locale files are essential for creating globally accessible Shopify themes. Proper internationalization enables themes to serve diverse markets while maintaining consistent functionality and user experience across languages and regions.