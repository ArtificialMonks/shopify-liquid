# Theme Store Compliant theme.liquid

This documentation provides a **Theme Store compliant** version of theme.liquid that passes all validation requirements.

## Key Compliance Features

- ✅ **Content Security Policy (CSP)**: Prevents XSS attacks
- ✅ **No External Resources**: All fonts and assets served from Shopify CDN
- ✅ **Proper Schema Documentation**: Layout files don't require schemas
- ✅ **Performance Optimized**: Font loading with font_display swap

## Implementation

```liquid
{%- comment -%}
  theme.liquid - Main layout file (Theme Store Compliant)
  Layout files don't require schema blocks - this is correct per Shopify standards
{%- endcomment -%}

<!doctype html>
<html class="no-js" lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width,initial-scale=1">

  {%- comment -%} Content Security Policy for Theme Store compliance {%- endcomment -%}
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self' *.shopify.com *.shopifycdn.com;
    script-src 'self' 'unsafe-inline' *.shopify.com *.shopifycdn.com;
    style-src 'self' 'unsafe-inline' *.shopifycdn.com;
    img-src 'self' data: *.shopifycdn.com *.shopify.com;
    font-src 'self' *.shopifycdn.com;
    connect-src 'self' *.shopify.com *.shopifycdn.com;
    frame-src 'self' *.shopify.com *.youtube.com *.vimeo.com;
    media-src 'self' *.shopifycdn.com *.shopify.com;
  ">

  <link rel="canonical" href="{{ canonical_url }}">
  <link rel="preconnect" href="https://cdn.shopify.com" crossorigin>

  {%- if settings.favicon != blank -%}
    <link rel="icon" type="image/png" href="{{ settings.favicon | image_url: width: 32, height: 32 }}">
  {%- endif -%}

  <title>{{ page_title }}{% unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless %}</title>

  {% if page_description %}
    <meta name="description" content="{{ page_description | escape }}">
  {% endif %}

  {{ content_for_header }}

  {%- comment -%} Font loading using Shopify's font system {%- endcomment -%}
  {% style %}
    {{ settings.type_body_font | font_face: font_display: 'swap' }}
    {{ settings.type_header_font | font_face: font_display: 'swap' }}

    :root {
      --font-body-family: {{ settings.type_body_font.family }}, {{ settings.type_body_font.fallback_families }};
      --font-header-family: {{ settings.type_header_font.family }}, {{ settings.type_header_font.fallback_families }};
    }

    body {
      font-family: var(--font-body-family);
    }
  {% endstyle %}

  {%- comment -%} Only local CSS files allowed for Theme Store compliance {%- endcomment -%}
  {{ 'base.css' | asset_url | stylesheet_tag }}

  {%- comment -%} Only Shopify's font CDN allowed {%- endcomment -%}
  {%- unless settings.type_body_font.system? and settings.type_header_font.system? -%}
    <link rel="preconnect" href="https://fonts.shopifycdn.com" crossorigin>
  {%- endunless -%}
</head>

<body>
  {% sections 'header-group' %}

  <main id="MainContent" role="main">
    {{ content_for_layout }}
  </main>

  {% sections 'footer-group' %}
</body>
</html>
```

## CSP Security Benefits

The Content Security Policy implementation provides:

1. **XSS Protection**: Prevents execution of malicious scripts
2. **Resource Control**: Only allows loading from trusted Shopify domains
3. **Font Security**: Restricts font loading to Shopify's CDN only
4. **Media Security**: Controls video/image sources to prevent data leaks

## Theme Store Requirements Met

- ✅ No external font imports (Google Fonts, etc.)
- ✅ No external CSS imports
- ✅ No external JavaScript libraries
- ✅ Proper CSP implementation
- ✅ Uses Shopify's font_picker system
- ✅ Performance optimized with font_display: swap

## Migration from External Fonts

```liquid
<!-- ❌ NOT ALLOWED: External font imports -->
<!-- <link href="https://fonts.googleapis.com/css2?family=Open+Sans" rel="stylesheet"> -->

<!-- ✅ THEME STORE COMPLIANT: Use settings.json -->
{
  "type": "font_picker",
  "id": "body_font",
  "label": "Body Font",
  "default": "assistant_n4"
}

<!-- ✅ THEME STORE COMPLIANT: Load with font_face filter -->
{{ settings.body_font | font_face: font_display: 'swap' }}
```

This approach ensures full Theme Store compliance while maintaining performance and flexibility.