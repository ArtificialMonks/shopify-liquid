# checkout.liquid - Shopify Plus Checkout Layout

The `checkout.liquid` file is available exclusively to **Shopify Plus** merchants and provides complete control over the checkout process layout and styling. This powerful feature enables custom checkout experiences while maintaining Shopify's secure payment processing.

## 🎯 Purpose and Availability

### What is checkout.liquid?
- **Shopify Plus exclusive** feature for checkout customization
- **Complete control** over checkout page HTML and CSS
- **Secure framework** maintaining PCI compliance
- **Custom branding** and user experience optimization

### When to Use
- **Brand consistency** across entire customer journey
- **Custom checkout flows** for specific business needs
- **Enhanced user experience** beyond standard checkout
- **A/B testing** checkout variations for conversion optimization

## 📋 Required Elements

### Essential Checkout Objects
Every `checkout.liquid` file **must** include these objects:

#### 1. content_for_header
```liquid
<head>
  {{ content_for_header }}
</head>
```
- **Purpose**: Essential Shopify scripts and metadata
- **Critical**: Required for checkout functionality

#### 2. content_for_layout
```liquid
<body>
  {{ content_for_layout }}
</body>
```
- **Purpose**: Dynamic checkout step content
- **Critical**: Contains the actual checkout forms and process

#### 3. checkout_stylesheets
```liquid
<head>
  {{ checkout_stylesheets }}
</head>
```
- **Purpose**: Shopify's checkout-specific CSS
- **Critical**: Provides base checkout styling

#### 4. checkout_scripts
```liquid
<head>
  {{ checkout_scripts }}
</head>
```
- **Purpose**: Checkout functionality and validation
- **Critical**: Enables form processing and payment handling

## 🏗️ Basic Structure

### Minimal Required Structure
```liquid
<!DOCTYPE html>
<html lang="{{ locale }}" dir="{{ direction }}" class="{{ checkout_html_classes }}">
<head>
  <meta charset="utf-8">
  <title>{{ page_title }}</title>
  {{ content_for_header }}
  {{ checkout_stylesheets }}
  {{ checkout_scripts }}
</head>
<body>
  {{ content_for_layout }}
  {{ tracking_code }}
</body>
</html>
```

### Production-Ready Structure
```liquid
<!DOCTYPE html>
<html lang="{{ locale }}" dir="{{ direction }}" class="{{ checkout_html_classes }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, height=device-height, minimum-scale=1.0, user-scalable=0">
  <meta name="referrer" content="origin">

  <title>{{ page_title }}</title>

  {{ content_for_header }}
  {{ checkout_stylesheets }}
  {{ checkout_scripts }}

  {% comment %} Custom checkout styles {% endcomment %}
  <style>
    {{ 'checkout-custom.css' | asset_url | asset }}
  </style>
</head>
<body>
  {{ skip_to_content_link }}

  <div class="banner" data-header>
    <div class="wrap">
      {{ content_for_logo }}
    </div>
  </div>

  {{ order_summary_toggle }}

  <div class="content" data-content>
    <div class="wrap">
      <div class="main">
        <header class="main__header" role="banner">
          {{ content_for_logo }}
          {{ breadcrumb }}
          {{ alternative_payment_methods }}
        </header>

        <main class="main__content" role="main">
          {{ content_for_layout }}
        </main>

        <footer class="main__footer" role="contentinfo">
          {{ content_for_footer }}
        </footer>
      </div>

      <aside class="sidebar" role="complementary">
        {{ content_for_order_summary }}
      </aside>
    </div>
  </div>

  {{ tracking_code }}
</body>
</html>
```

## 🎨 Checkout-Specific Objects

### Layout Objects
Objects available specifically in checkout.liquid:

#### Logo and Branding
```liquid
{{ content_for_logo }}        <!-- Shop logo/branding area -->
```

#### Navigation and Progress
```liquid
{{ breadcrumb }}              <!-- Checkout step breadcrumb -->
{{ skip_to_content_link }}    <!-- Accessibility skip link -->
```

#### Order Summary
```liquid
{{ content_for_order_summary }}  <!-- Cart items and totals -->
{{ order_summary_toggle }}       <!-- Mobile order summary toggle -->
```

#### Payment Methods
```liquid
{{ alternative_payment_methods }} <!-- PayPal, Apple Pay, etc. -->
```

#### Footer Content
```liquid
{{ content_for_footer }}      <!-- Footer policies and links -->
```

#### Analytics and Tracking
```liquid
{{ tracking_code }}           <!-- Conversion tracking scripts -->
```

#### CSS Classes
```liquid
{{ checkout_html_classes }}   <!-- Dynamic HTML classes for styling -->
```

### Checkout Context Variables
Access checkout-specific information:

```liquid
{{ checkout.id }}                    <!-- Unique checkout ID -->
{{ checkout.created_at }}            <!-- Checkout creation time -->
{{ checkout.currency }}              <!-- Checkout currency -->
{{ checkout.customer }}              <!-- Customer information -->
{{ checkout.shipping_address }}      <!-- Shipping address -->
{{ checkout.billing_address }}       <!-- Billing address -->
{{ checkout.shipping_rate }}         <!-- Selected shipping method -->
{{ checkout.tax_lines }}             <!-- Tax information -->
{{ checkout.discount_applications }} <!-- Applied discounts -->
```

## 🎨 Styling and Customization

### Custom CSS Integration
```liquid
<head>
  {{ checkout_stylesheets }}

  {% comment %} Custom overrides {% endcomment %}
  <style>
    /* Brand colors */
    :root {
      --colorPrimary: {{ settings.checkout_accent_color | default: '#1990c6' }};
      --colorSecondary: {{ settings.checkout_button_color | default: '#333' }};
    }

    /* Custom header styling */
    .banner {
      background-color: var(--colorPrimary);
      border-bottom: 1px solid #ddd;
    }

    /* Button customization */
    .btn {
      background-color: var(--colorSecondary);
      border-radius: {{ settings.button_border_radius | default: 4 }}px;
    }

    /* Step indicator styling */
    .breadcrumb__item--current {
      color: var(--colorPrimary);
    }
  </style>
</head>
```

### Responsive Design
```liquid
<style>
  /* Mobile-first checkout styles */
  @media (max-width: 999px) {
    .main__content {
      padding: 1rem;
    }

    .order-summary-toggle {
      display: block;
    }

    .sidebar {
      display: none;
    }
  }

  @media (min-width: 1000px) {
    .content {
      display: flex;
    }

    .main {
      flex: 1;
      padding-right: 2rem;
    }

    .sidebar {
      width: 350px;
    }
  }
</style>
```

## 🚀 Advanced Customizations

### Multi-Step Progress Indicator
```liquid
<style>
  .checkout-progress {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .progress-step {
    flex: 1;
    text-align: center;
    padding: 1rem;
    position: relative;
  }

  .progress-step.completed {
    color: var(--colorPrimary);
  }

  .progress-step.current {
    font-weight: bold;
    color: var(--colorPrimary);
  }
</style>

<div class="checkout-progress">
  <div class="progress-step completed">
    <span>{{ 'checkout.progress.information' | t }}</span>
  </div>
  <div class="progress-step current">
    <span>{{ 'checkout.progress.shipping' | t }}</span>
  </div>
  <div class="progress-step">
    <span>{{ 'checkout.progress.payment' | t }}</span>
  </div>
</div>
```

### Trust Signals and Security
```liquid
<div class="checkout-security">
  <div class="security-badges">
    {% if settings.security_badge_1 %}
      <img src="{{ settings.security_badge_1 | image_url: width: 100 }}"
           alt="{{ 'checkout.security.ssl' | t }}"
           loading="lazy">
    {% endif %}

    <div class="security-text">
      <p>{{ 'checkout.security.message' | t }}</p>
    </div>
  </div>
</div>
```

### Custom Footer with Policies
```liquid
<style>
  .checkout-footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #ddd;
    font-size: 0.875rem;
    color: #666;
  }

  .footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1rem;
  }

  .footer-links a {
    color: inherit;
    text-decoration: none;
  }

  .footer-links a:hover {
    text-decoration: underline;
  }
</style>

<footer class="checkout-footer">
  <div class="footer-links">
    <a href="{{ pages.privacy-policy.url }}">{{ 'footer.privacy_policy' | t }}</a>
    <a href="{{ pages.terms-of-service.url }}">{{ 'footer.terms_of_service' | t }}</a>
    <a href="{{ pages.refund-policy.url }}">{{ 'footer.refund_policy' | t }}</a>
  </div>

  <div class="footer-copyright">
    <p>&copy; {{ 'now' | date: "%Y" }} {{ shop.name }}. {{ 'footer.all_rights_reserved' | t }}</p>
  </div>
</footer>
```

## 🔒 Security Considerations

### PCI Compliance
- **Never modify** payment form fields
- **Don't add** custom JavaScript to payment areas
- **Use HTTPS** for all custom assets
- **Validate** all custom inputs server-side

### Safe Customization Areas
✅ **Safe to customize:**
- Header and branding
- Footer content and links
- CSS styling and layout
- Progress indicators
- Trust signals and badges

❌ **Do not modify:**
- Payment form fields
- Credit card input areas
- Security tokens
- Core checkout functionality

## 📊 Performance Optimization

### Critical Path Optimization
```liquid
<head>
  <!-- Inline critical checkout CSS -->
  <style>
    /* Critical above-the-fold styles */
    .banner { background: #f8f8f8; padding: 1rem; }
    .main__content { max-width: 600px; margin: 0 auto; }
  </style>

  {{ checkout_stylesheets }}
  {{ checkout_scripts }}

  <!-- Preload custom assets -->
  {{ 'checkout-custom.css' | asset_url | preload_tag: as: 'style' }}
</head>
```

### Image Optimization
```liquid
<!-- Optimized logo loading -->
{% if settings.checkout_logo %}
  <img src="{{ settings.checkout_logo | image_url: width: 200 }}"
       srcset="{{ settings.checkout_logo | image_url: width: 200 }} 1x,
               {{ settings.checkout_logo | image_url: width: 400 }} 2x"
       alt="{{ shop.name }}"
       loading="eager"
       width="200"
       height="auto">
{% endif %}
```

## 🛠️ Testing and Validation

### Checkout Testing Checklist
- [ ] All checkout steps complete successfully
- [ ] Mobile responsiveness across devices
- [ ] Payment methods function correctly
- [ ] Form validation works properly
- [ ] Error messages display clearly
- [ ] Success page renders correctly
- [ ] Analytics tracking fires correctly

### Browser Compatibility
Test across major browsers:
- Chrome (latest 2 versions)
- Safari (latest 2 versions)
- Firefox (latest 2 versions)
- Edge (latest version)

### Device Testing
- Mobile phones (iOS/Android)
- Tablets (iPad/Android)
- Desktop computers
- Various screen sizes and orientations

## 🚨 Common Pitfalls

### 1. Missing Required Objects
**Problem**: Checkout breaks or doesn't process payments
**Solution**: Always include all required objects in correct locations

### 2. Modifying Payment Forms
**Problem**: PCI compliance violations and payment failures
**Solution**: Only style payment areas, never modify form structure

### 3. JavaScript Errors
**Problem**: Checkout process fails or becomes unresponsive
**Solution**: Test all custom JavaScript thoroughly, avoid conflicts

### 4. Mobile Optimization
**Problem**: Poor mobile checkout experience
**Solution**: Test extensively on mobile devices, optimize touch targets

## 📈 Conversion Optimization

### Trust Signals
- Display security badges prominently
- Show customer reviews or testimonials
- Include money-back guarantees
- Display accepted payment methods

### User Experience
- Minimize form fields
- Provide clear progress indicators
- Show total costs upfront
- Enable guest checkout options

### Performance
- Optimize for fast loading
- Minimize HTTP requests
- Compress images and assets
- Use efficient CSS and JavaScript

---

The `checkout.liquid` file is a powerful tool for Shopify Plus merchants to create custom checkout experiences that drive conversions while maintaining security and compliance standards.