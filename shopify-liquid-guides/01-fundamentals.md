# Liquid Fundamentals

Liquid is Shopify's templating language, extended in themes to expose store objects, logic tags, and filters for transforming output. Understanding these fundamentals is essential for building effective Shopify sections.

## Core Syntax

### Output
```liquid
{{ variable }}              <!-- Basic output -->
{{ product.title }}         <!-- Dot notation for object properties -->
{{ product.price | money }} <!-- With filter applied -->
```

### Tags (Logic & Flow Control)
```liquid
{% if condition %}          <!-- Conditional logic -->
{% for item in collection %}  <!-- Loops -->
{% assign var = value %}    <!-- Variable assignment -->
{% capture var %}content{% endcapture %} <!-- Multi-line capture -->
{% render 'snippet-name', param: value %} <!-- Include snippets -->
```

### Filters (Transform Output)
```liquid
{{ text | upcase }}         <!-- Text transformation -->
{{ price | money }}         <!-- Currency formatting -->
{{ text | escape }}         <!-- HTML escaping (ALWAYS use for user input) -->
{{ image | image_url: width: 800 }} <!-- Image resizing -->
```

Filters are chainable from left to right:
```liquid
{{ product.title | escape | upcase | truncate: 50 }}
```

## Key Objects in Themes

### Global Objects (Available Everywhere)
- `shop` - Store information (name, domain, etc.)
- `settings` - Theme settings from settings_schema.json
- `content_for_header` - Shopify's required head content
- `request` - Page request information

### Template-Specific Objects
- `product` - Available on product pages
- `collection` - Available on collection pages
- `cart` - Cart object and line items
- `customer` - Logged-in customer data
- `article`, `blog` - Blog content

### Section & Block Objects
- `section` - Current section data and settings
- `block` - Current block data and settings (inside block loops)
- `section.settings` - Section configuration from schema
- `block.settings` - Block configuration from schema

## Variables & Assignment

### Simple Assignment
```liquid
{% assign price = product.price | money %}
{% assign image_alt = product.featured_image.alt | escape %}
```

### Capture (Multi-line Content)
```liquid
{% capture product_info %}
  <h3>{{ product.title | escape }}</h3>
  <p>{{ product.price | money }}</p>
{% endcapture %}

{{ product_info }}
```

## Control Flow

### Conditionals
```liquid
{% if product.available %}
  <button>Add to Cart</button>
{% elsif product.tags contains 'coming-soon' %}
  <p>Coming Soon</p>
{% else %}
  <p>Sold Out</p>
{% endif %}
```

### Comparison Operators
- `==` equals
- `!=` not equals
- `>`, `<`, `>=`, `<=` numerical comparison
- `contains` check if string/array contains value

### Boolean Operators
```liquid
{% if product.available and product.price > 0 %}
{% if collection.id == 123456 or collection.handle == 'sale' %}
```

### Case Statements
```liquid
{% case product.type %}
  {% when 'Clothing' %}
    <!-- Clothing specific content -->
  {% when 'Electronics' %}
    <!-- Electronics specific content -->
  {% else %}
    <!-- Default content -->
{% endcase %}
```

### Loops
```liquid
{% for product in collection.products limit: 8 %}
  <div class="product-card">
    <h3>{{ product.title | escape }}</h3>
    <p>{{ product.price | money }}</p>
  </div>
{% endfor %}
```

#### Loop Variables
```liquid
{% for item in array %}
  {{ forloop.index }}     <!-- Current iteration (1-based) -->
  {{ forloop.index0 }}    <!-- Current iteration (0-based) -->
  {{ forloop.first }}     <!-- true if first iteration -->
  {{ forloop.last }}      <!-- true if last iteration -->
  {{ forloop.length }}    <!-- Total number of iterations -->
{% endfor %}
```

#### Loop Modifiers
```liquid
{% for product in collection.products limit: 6 offset: 3 reversed %}
  <!-- Process 6 products starting from the 4th, in reverse order -->
{% endfor %}
```

## Pagination
For large collections (>50 items), always use pagination:

```liquid
{% paginate collection.products by 24 %}
  {% for product in collection.products %}
    <!-- Product markup -->
  {% endfor %}

  <!-- Pagination controls -->
  {{ paginate | default_pagination }}
{% endpaginate %}
```

## Includes & Components

### Render Snippets (Preferred)
```liquid
{% render 'product-card', product: product, show_vendor: true %}
```
- Isolates scope (variables don't leak)
- Pass data explicitly via parameters
- More maintainable and predictable

### Include Snippets (Legacy)
```liquid
{% include 'product-card' %}
```
- Shares scope with parent template
- Variables accessible without passing
- Avoid in new development

## Image Handling

### Responsive Images (Essential Pattern)
```liquid
{% if product.featured_image %}
  <img
    src="{{ product.featured_image | image_url: width: 800 }}"
    srcset="
      {{ product.featured_image | image_url: width: 400 }} 400w,
      {{ product.featured_image | image_url: width: 800 }} 800w,
      {{ product.featured_image | image_url: width: 1200 }} 1200w
    "
    sizes="(min-width: 990px) 800px, 100vw"
    alt="{{ product.featured_image.alt | escape }}"
    loading="lazy"
    width="800"
    height="{{ product.featured_image.height | default: 600 }}"
  >
{% endif %}
```

### Image URL Parameters
```liquid
{{ image | image_url: width: 800 }}           <!-- Resize to 800px wide -->
{{ image | image_url: width: 800, height: 600 }} <!-- Crop to 800x600 -->
{{ image | image_url: width: 800, crop: 'center' }} <!-- Crop position -->
```

## Essential Filters

### Text Filters
```liquid
{{ text | escape }}         <!-- HTML escape (REQUIRED for user input) -->
{{ text | strip_html }}     <!-- Remove HTML tags -->
{{ text | truncate: 100 }}  <!-- Limit to 100 characters -->
{{ text | upcase }}         <!-- Uppercase -->
{{ text | downcase }}       <!-- Lowercase -->
{{ text | capitalize }}     <!-- Capitalize first letter -->
```

### Number & Money Filters
```liquid
{{ price | money }}                    <!-- Format as currency -->
{{ price | money_without_currency }}   <!-- Just the number -->
{{ number | round: 2 }}               <!-- Round to 2 decimal places -->
```

### Array Filters
```liquid
{{ collection.products | size }}      <!-- Get array length -->
{{ array | join: ', ' }}             <!-- Join with separator -->
{{ array | first }}                  <!-- Get first item -->
{{ array | last }}                   <!-- Get last item -->
```

### Date Filters
```liquid
{{ article.published_at | date: '%B %d, %Y' }}  <!-- Format date -->
{{ 'now' | date: '%Y-%m-%d' }}                  <!-- Current date -->
```

## Performance & Best Practices

### Always Guard Optional Content
```liquid
{% if section.settings.title != blank %}
  <h2>{{ section.settings.title | escape }}</h2>
{% endif %}

{% if product.featured_image %}
  <!-- Image markup -->
{% endif %}
```

### Escape User Input
```liquid
<!-- ALWAYS escape user-generated content -->
<h2>{{ section.settings.heading | escape }}</h2>
<p>{{ customer.first_name | escape }}</p>

<!-- Rich text fields don't need escaping -->
<div class="content">{{ section.settings.rich_text }}</div>
```

### Avoid Heavy Global Queries
```liquid
<!-- BAD: Heavy query in loop -->
{% for product in all_products %}
  {% for variant in product.variants %}
    <!-- This gets expensive quickly -->
  {% endfor %}
{% endfor %}

<!-- GOOD: Target specific collections -->
{% for product in collections.featured.products limit: 8 %}
  <!-- Much more efficient -->
{% endfor %}
```

### Use Specific Resources
```liquid
<!-- BAD: Generic, slow -->
{% assign featured_product = all_products['product-handle'] %}

<!-- GOOD: Specific, fast -->
{% assign featured_product = collections.featured.products.first %}
```

## Common Patterns

### Safe Property Access
```liquid
<!-- Check before accessing nested properties -->
{% if product.featured_image.alt %}
  {{ product.featured_image.alt | escape }}
{% else %}
  {{ product.title | escape }}
{% endif %}
```

### Setting Defaults
```liquid
{{ section.settings.heading | default: 'Default Heading' | escape }}
{{ image.alt | default: 'Product image' | escape }}
```

### Building Dynamic Classes
```liquid
{% assign css_class = 'product-card' %}
{% if product.available %}
  {% assign css_class = css_class | append: ' product-card--available' %}
{% endif %}
{% if product.compare_at_price > product.price %}
  {% assign css_class = css_class | append: ' product-card--on-sale' %}
{% endif %}

<div class="{{ css_class }}">
  <!-- Product content -->
</div>
```

## Next Steps

Now that you understand Liquid fundamentals, you're ready to learn how to build sections and blocks:

- **[Quick Start Guide](./02-quick-start.md)** - Build your first section
- **[Sections & Schema](./03-sections-and-schema.md)** - Learn section configuration
- **[Code Library](./code-library/)** - See these concepts in action

## References

- [Shopify Liquid Reference](https://shopify.dev/docs/api/liquid)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [Shopify Objects Documentation](https://shopify.dev/docs/api/liquid/objects)