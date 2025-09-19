# Liquid Fundamentals (Theme Variant)

Liquid is Shopifys templating language, extended in themes to expose store objects (product, collection, cart, shop, etc.), tags (logic/flow), and filters (transform output).

Core syntax
- Output: `{{ variable }}` (supports dot access, e.g., `product.title`)
- Tags (logic/flow): `{% if %}`, `{% for %}`, `{% assign %}`, `{% capture %}`, `{% render %}`, `{% paginate %}`, etc.
- Filters: `| upcase`, `| money`, `| escape`, `| image_url: width: 800`, chainable left to right

Objects (theme highlights)
- `product`, `collection`, `cart`, `article`, `blog`, `shop`, `customer`, `settings`, `section`, `block`, `content_for_header`
- Object scope: some are global; others only available in specific templates/contexts (see object docs)

Variables
- `assign`: `{% assign price = product.price | money %}`
- `capture`: multi line capture to a string variable

Control flow
- `if` / `elsif` / `else` with comparison (`==`, `!=`, `>`, `<`, `contains`) and boolean operators (`and`, `or`)
- `case` / `when`
- `for` with optional `limit`, `offset`, `reversed`; use `forloop.index`, `forloop.last`
- `paginate` for large collections (Shopify storefront limit: 50 items per page without pagination)

Includes & components
- `{% render 'snippet-name', param: value %}` isolates scope (preferred)
- `{% section 'name' %}` (static; avoid except in legacy layouts). Prefer JSON templates and section groups.

Images
- Use `image_url` to request CDN resized variants; pair with `image_tag` or manual `<img>` for srcset/sizes

Example: safe heading and responsive image

```liquid
<h2>{{ section.settings.heading | escape }}</h2>
{% if section.settings.image %}
  <img
    src="{{ section.settings.image | image_url: width: 800 }}"
    srcset="{{ section.settings.image | image_url: width: 400 }} 400w, {{ section.settings.image | image_url: width: 800 }} 800w, {{ section.settings.image | image_url: width: 1200 }} 1200w"
    sizes="(min-width: 990px) 800px, 100vw"
    alt="{{ section.settings.image.alt | escape }}"
    loading="lazy"
    width="800" height="{{ section.settings.image.height | default: 600 }}"
  >
{% endif %}
```

Performance notes
- Avoid heavy global collections in loops (like `all_products`) on templates; prefer specific resources
- Use `paginate` for lists > 50
- Keep logic server side; avoid client side rendering unless strictly necessary (SSR first)

References
- Liquid ref: https://shopify.dev/docs/api/liquid
- Liquid OSS: https://shopify.github.io/liquid/

