# Liquid Templates - Custom Logic and Static Markup

Liquid templates provide complete control over page markup and logic, offering maximum flexibility for complex custom implementations. While JSON templates are preferred for merchant flexibility, Liquid templates excel in scenarios requiring custom logic, static layouts, or specific performance optimizations.

## 🎯 When to Use Liquid Templates

### Ideal Use Cases
✅ **Static layouts** that don't need merchant customization
✅ **Complex custom logic** that can't be handled in sections
✅ **Performance-critical pages** requiring optimized markup
✅ **Legacy template migration** from older theme architectures
✅ **Highly specific designs** that don't fit section patterns

### Consider JSON Instead When
❌ Merchants need to customize content
❌ You want drag-and-drop functionality
❌ Future updates and maintenance are priorities
❌ Multiple layout variations are needed

## 🏗️ Liquid Template Structure

### Basic Template Structure
```liquid
{% comment %} Template: templates/product.liquid {% endcomment %}

{% layout 'product-layout' %}

<div class="product-page">
  <div class="product-media">
    {% for media in product.media %}
      <div class="product-media-item">
        {% case media.media_type %}
          {% when 'image' %}
            {{ media | image_url: width: 800 | image_tag }}
          {% when 'video' %}
            {{ media | video_tag: controls: true }}
          {% when 'model' %}
            {{ media | model_viewer_tag }}
        {% endcase %}
      </div>
    {% endfor %}
  </div>

  <div class="product-details">
    <h1 class="product-title">{{ product.title | escape }}</h1>

    {% if product.vendor != blank %}
      <div class="product-vendor">{{ product.vendor | escape }}</div>
    {% endif %}

    <div class="product-price">
      {% if product.compare_at_price > product.price %}
        <span class="price-compare">{{ product.compare_at_price | money }}</span>
        <span class="price-current price-on-sale">{{ product.price | money }}</span>
      {% else %}
        <span class="price-current">{{ product.price | money }}</span>
      {% endif %}
    </div>

    {% form 'product', product %}
      <!-- Product form content -->
    {% endform %}

    {% if product.description != blank %}
      <div class="product-description">
        {{ product.description }}
      </div>
    {% endif %}
  </div>
</div>
```

### Advanced Liquid Template
```liquid
{% comment %}
  Template: templates/collection.liquid
  Custom collection template with advanced filtering
{% endcomment %}

{% assign current_tags = collection.current_tags %}
{% assign current_vendor = collection.current_vendor %}
{% assign sort_by = collection.sort_by | default: collection.default_sort_by %}

<div class="collection-page">
  <header class="collection-header">
    <h1 class="collection-title">{{ collection.title | escape }}</h1>

    {% if collection.description != blank %}
      <div class="collection-description">
        {{ collection.description }}
      </div>
    {% endif %}

    <div class="collection-count">
      {{ 'collections.general.items_with_count' | t: count: collection.products_count }}
    </div>
  </header>

  <div class="collection-toolbar">
    {% comment %} Filter by tags {% endcomment %}
    {% if collection.all_tags.size > 0 %}
      <div class="collection-filters">
        <h3>{{ 'collections.filters.title' | t }}</h3>
        {% for tag in collection.all_tags %}
          {% if current_tags contains tag %}
            <a href="{{ collection.url }}" class="filter-tag active">
              {{ tag | escape }}
            </a>
          {% else %}
            <a href="{{ collection.url }}/{{ tag | handle }}" class="filter-tag">
              {{ tag | escape }}
            </a>
          {% endif %}
        {% endfor %}
      </div>
    {% endif %}

    {% comment %} Sort options {% endcomment %}
    <div class="collection-sort">
      <label for="sort-by">{{ 'collections.sorting.title' | t }}</label>
      <select id="sort-by" onchange="window.location.href = this.value">
        {% for option in collection.sort_options %}
          <option value="{{ collection.url }}?sort_by={{ option.value }}"
                  {% if option.value == sort_by %}selected{% endif %}>
            {{ option.name | escape }}
          </option>
        {% endfor %}
      </select>
    </div>
  </div>

  {% paginate collection.products by 24 %}
    <div class="product-grid">
      {% for product in collection.products %}
        <div class="product-card">
          <a href="{{ product.url }}" class="product-card-link">
            {% if product.featured_image %}
              {{ product.featured_image | image_url: width: 400 | image_tag: loading: 'lazy' }}
            {% endif %}

            <h3 class="product-card-title">{{ product.title | escape }}</h3>

            <div class="product-card-price">
              {% if product.compare_at_price > product.price %}
                <span class="price-compare">{{ product.compare_at_price | money }}</span>
                <span class="price-current">{{ product.price | money }}</span>
              {% else %}
                <span class="price-current">{{ product.price | money }}</span>
              {% endif %}
            </div>
          </a>
        </div>
      {% endfor %}
    </div>

    {% if paginate.pages > 1 %}
      <nav class="pagination" aria-label="{{ 'general.pagination.label' | t }}">
        {% if paginate.previous %}
          <a href="{{ paginate.previous.url }}" class="pagination-prev">
            {{ 'general.pagination.previous' | t }}
          </a>
        {% endif %}

        {% for part in paginate.parts %}
          {% if part.is_link %}
            <a href="{{ part.url }}" class="pagination-item">{{ part.title }}</a>
          {% else %}
            {% if part.title == paginate.current_page %}
              <span class="pagination-item current">{{ part.title }}</span>
            {% else %}
              <span class="pagination-item">{{ part.title }}</span>
            {% endif %}
          {% endif %}
        {% endfor %}

        {% if paginate.next %}
          <a href="{{ paginate.next.url }}" class="pagination-next">
            {{ 'general.pagination.next' | t }}
          </a>
        {% endif %}
      </nav>
    {% endif %}
  {% endpaginate %}
</div>
```

## 🎨 Template-Specific Patterns

### Product Template Patterns

#### Variant Handling
```liquid
{% comment %} Advanced variant selector {% endcomment %}
<div class="product-variants">
  {% for option in product.options_with_values %}
    <div class="variant-option">
      <label for="option-{{ option.position }}">{{ option.name | escape }}</label>
      <select id="option-{{ option.position }}"
              name="options[{{ option.name | escape }}]"
              data-index="option{{ option.position }}">
        {% for value in option.values %}
          <option value="{{ value | escape }}"
                  {% if option.selected_value == value %}selected{% endif %}>
            {{ value | escape }}
          </option>
        {% endfor %}
      </select>
    </div>
  {% endfor %}
</div>

{% comment %} Variant availability {% endcomment %}
<script>
  const productVariants = {{ product.variants | json }};
  const productOptions = {{ product.options | json }};

  function updateVariantAvailability() {
    // Custom variant logic
  }
</script>
```

#### Media Gallery
```liquid
{% comment %} Product media with thumbnails {% endcomment %}
<div class="product-media-gallery">
  <div class="main-media">
    {% assign featured_media = product.selected_or_first_available_variant.featured_media | default: product.featured_media %}
    {% if featured_media %}
      <div class="media-item" data-media-id="{{ featured_media.id }}">
        {% case featured_media.media_type %}
          {% when 'image' %}
            {{ featured_media | image_url: width: 800 | image_tag }}
          {% when 'video' %}
            {{ featured_media | video_tag: controls: true }}
          {% when 'external_video' %}
            {{ featured_media | external_video_tag }}
          {% when 'model' %}
            {{ featured_media | model_viewer_tag }}
        {% endcase %}
      </div>
    {% endif %}
  </div>

  {% if product.media.size > 1 %}
    <div class="media-thumbnails">
      {% for media in product.media %}
        <button type="button"
                class="thumbnail-button{% if media.id == featured_media.id %} active{% endif %}"
                data-media-id="{{ media.id }}">
          {% case media.media_type %}
            {% when 'image' %}
              {{ media | image_url: width: 100 | image_tag }}
            {% when 'video' %}
              {{ media.preview_image | image_url: width: 100 | image_tag }}
              <span class="media-badge">Video</span>
            {% when 'model' %}
              {{ media.preview_image | image_url: width: 100 | image_tag }}
              <span class="media-badge">3D</span>
          {% endcase %}
        </button>
      {% endfor %}
    </div>
  {% endif %}
</div>
```

### Collection Template Patterns

#### Advanced Filtering
```liquid
{% comment %} Multi-faceted filtering {% endcomment %}
<div class="collection-filters">
  {% comment %} Price range filter {% endcomment %}
  <div class="filter-group">
    <h4>{{ 'collections.filters.price' | t }}</h4>
    {% assign price_ranges = 'Under $25,25,50|$25 - $50,50,100|$50 - $100,100,200|Over $200,200,' | split: '|' %}
    {% for range in price_ranges %}
      {% assign range_parts = range | split: ',' %}
      {% assign range_label = range_parts[0] %}
      {% assign range_min = range_parts[1] %}
      {% assign range_max = range_parts[2] %}

      <a href="{{ collection.url }}?price_min={{ range_min }}&price_max={{ range_max }}"
         class="filter-option">
        {{ range_label }}
      </a>
    {% endfor %}
  </div>

  {% comment %} Availability filter {% endcomment %}
  <div class="filter-group">
    <h4>{{ 'collections.filters.availability' | t }}</h4>
    <a href="{{ collection.url }}?available=true" class="filter-option">
      {{ 'collections.filters.in_stock' | t }}
    </a>
  </div>

  {% comment %} Vendor filter {% endcomment %}
  {% if collection.all_vendors.size > 1 %}
    <div class="filter-group">
      <h4>{{ 'collections.filters.vendor' | t }}</h4>
      {% for vendor in collection.all_vendors %}
        <a href="{{ collection.url }}/{{ vendor | handle }}" class="filter-option">
          {{ vendor | escape }}
        </a>
      {% endfor %}
    </div>
  {% endif %}
</div>
```

### Page Template Patterns

#### Contact Form
```liquid
{% comment %} Custom contact form template {% endcomment %}
<div class="contact-page">
  <div class="contact-info">
    <h1>{{ page.title | escape }}</h1>
    {{ page.content }}

    <div class="contact-details">
      {% if settings.contact_email %}
        <div class="contact-item">
          <strong>{{ 'contact.email' | t }}:</strong>
          <a href="mailto:{{ settings.contact_email }}">{{ settings.contact_email }}</a>
        </div>
      {% endif %}

      {% if settings.contact_phone %}
        <div class="contact-item">
          <strong>{{ 'contact.phone' | t }}:</strong>
          <a href="tel:{{ settings.contact_phone }}">{{ settings.contact_phone }}</a>
        </div>
      {% endif %}
    </div>
  </div>

  <div class="contact-form">
    {% form 'contact' %}
      {% if form.posted_successfully? %}
        <div class="form-success">
          {{ 'contact.form.post_success' | t }}
        </div>
      {% endif %}

      {% if form.errors %}
        <div class="form-errors">
          <h4>{{ 'contact.form.error_heading' | t }}</h4>
          <ul>
            {% for field in form.errors %}
              <li>
                {% if field == 'form' %}
                  {{ form.errors.messages[field] }}
                {% else %}
                  {{ form.errors.translated_fields[field] | capitalize }}
                  {{ form.errors.messages[field] }}
                {% endif %}
              </li>
            {% endfor %}
          </ul>
        </div>
      {% endif %}

      <div class="form-group">
        <label for="contact-name">{{ 'contact.form.name' | t }} *</label>
        <input type="text"
               id="contact-name"
               name="contact[name]"
               value="{{ form.name }}"
               required>
      </div>

      <div class="form-group">
        <label for="contact-email">{{ 'contact.form.email' | t }} *</label>
        <input type="email"
               id="contact-email"
               name="contact[email]"
               value="{{ form.email }}"
               required>
      </div>

      <div class="form-group">
        <label for="contact-message">{{ 'contact.form.message' | t }} *</label>
        <textarea id="contact-message"
                  name="contact[body]"
                  rows="6"
                  required>{{ form.body }}</textarea>
      </div>

      <button type="submit" class="btn btn-primary">
        {{ 'contact.form.send' | t }}
      </button>
    {% endform %}
  </div>
</div>
```

## 🚀 Advanced Liquid Techniques

### Custom Pagination
```liquid
{% comment %} Advanced pagination with custom logic {% endcomment %}
{% paginate collection.products by 12 %}
  {% assign total_pages = paginate.pages %}
  {% assign current_page = paginate.current_page %}
  {% assign show_pages = 5 %}
  {% assign half_show = show_pages | divided_by: 2 %}

  <nav class="pagination" aria-label="Pagination">
    {% if paginate.previous %}
      <a href="{{ paginate.previous.url }}" class="pagination-prev">
        <span aria-hidden="true">&larr;</span>
        <span class="sr-only">{{ 'general.pagination.previous' | t }}</span>
      </a>
    {% endif %}

    {% comment %} First page {% endcomment %}
    {% if current_page > half_show + 1 %}
      <a href="{{ paginate.parts.first.url }}" class="pagination-item">1</a>
      {% if current_page > half_show + 2 %}
        <span class="pagination-ellipsis">…</span>
      {% endif %}
    {% endif %}

    {% comment %} Visible pages {% endcomment %}
    {% for i in (1..total_pages) %}
      {% assign start_page = current_page | minus: half_show %}
      {% assign end_page = current_page | plus: half_show %}

      {% if start_page < 1 %}
        {% assign start_page = 1 %}
        {% assign end_page = show_pages | at_most: total_pages %}
      {% endif %}

      {% if end_page > total_pages %}
        {% assign end_page = total_pages %}
        {% assign start_page = total_pages | minus: show_pages | plus: 1 | at_least: 1 %}
      {% endif %}

      {% if i >= start_page and i <= end_page %}
        {% if i == current_page %}
          <span class="pagination-item current" aria-current="page">{{ i }}</span>
        {% else %}
          {% for part in paginate.parts %}
            {% if part.title == i and part.is_link %}
              <a href="{{ part.url }}" class="pagination-item">{{ i }}</a>
              {% break %}
            {% endif %}
          {% endfor %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% comment %} Last page {% endcomment %}
    {% if current_page < total_pages | minus: half_show %}
      {% if current_page < total_pages | minus: half_show | minus: 1 %}
        <span class="pagination-ellipsis">…</span>
      {% endif %}
      <a href="{{ paginate.parts.last.url }}" class="pagination-item">{{ total_pages }}</a>
    {% endif %}

    {% if paginate.next %}
      <a href="{{ paginate.next.url }}" class="pagination-next">
        <span class="sr-only">{{ 'general.pagination.next' | t }}</span>
        <span aria-hidden="true">&rarr;</span>
      </a>
    {% endif %}
  </nav>
{% endpaginate %}
```

### Dynamic Content Loading
```liquid
{% comment %} AJAX content loading {% endcomment %}
<div class="dynamic-content" data-url="{{ collection.url }}">
  <div class="loading-indicator" style="display: none;">
    {{ 'general.loading' | t }}
  </div>

  <div class="content-container">
    <!-- Initial content loaded server-side -->
  </div>
</div>

<script>
  class DynamicContentLoader {
    constructor(container) {
      this.container = container;
      this.loadingIndicator = container.querySelector('.loading-indicator');
      this.contentContainer = container.querySelector('.content-container');
      this.baseUrl = container.dataset.url;
    }

    async loadContent(params) {
      this.showLoading();

      try {
        const url = new URL(this.baseUrl);
        Object.entries(params).forEach(([key, value]) => {
          url.searchParams.set(key, value);
        });

        const response = await fetch(url);
        const html = await response.text();

        // Parse and update content
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.querySelector('.content-container');

        if (newContent) {
          this.contentContainer.innerHTML = newContent.innerHTML;
        }
      } catch (error) {
        console.error('Failed to load content:', error);
      } finally {
        this.hideLoading();
      }
    }

    showLoading() {
      this.loadingIndicator.style.display = 'block';
      this.contentContainer.style.opacity = '0.5';
    }

    hideLoading() {
      this.loadingIndicator.style.display = 'none';
      this.contentContainer.style.opacity = '1';
    }
  }

  // Initialize dynamic loading
  document.querySelectorAll('.dynamic-content').forEach(container => {
    new DynamicContentLoader(container);
  });
</script>
```

## 🔧 Template Organization

### Modular Include Pattern
```liquid
{% comment %} Main template: templates/product.liquid {% endcomment %}
<div class="product-page">
  {% include 'product-breadcrumbs' %}
  {% include 'product-media' %}
  {% include 'product-details' %}
  {% include 'product-recommendations' %}
</div>

{% comment %} Include: snippets/product-media.liquid {% endcomment %}
<div class="product-media">
  {% for media in product.media %}
    {% include 'product-media-item', media: media %}
  {% endfor %}
</div>

{% comment %} Include: snippets/product-details.liquid {% endcomment %}
<div class="product-details">
  <h1>{{ product.title | escape }}</h1>
  {% include 'product-price', product: product %}
  {% include 'product-form', product: product %}
  {% include 'product-description', product: product %}
</div>
```

### Layout Switching
```liquid
{% comment %} Conditional layout assignment {% endcomment %}
{% if product.type == 'bundle' %}
  {% layout 'bundle-product' %}
{% elsif collection.handle == 'featured' %}
  {% layout 'featured-product' %}
{% else %}
  {% layout 'theme' %}
{% endif %}
```

## 🛠️ Performance Optimization

### Efficient Loops
```liquid
{% comment %} Limit expensive operations {% endcomment %}
{% assign featured_products = collections.featured.products | limit: 8 %}
{% for product in featured_products %}
  <!-- Product card -->
{% endfor %}

{% comment %} Cache expensive calculations {% endcomment %}
{% assign discount_percent = product.compare_at_price | minus: product.price | times: 100 | divided_by: product.compare_at_price | round %}
```

### Conditional Asset Loading
```liquid
{% comment %} Load template-specific assets {% endcomment %}
{% case template.name %}
  {% when 'product' %}
    {{ 'product-zoom.js' | asset_url | script_tag: defer: true }}
    {{ 'product-reviews.css' | asset_url | stylesheet_tag }}
  {% when 'collection' %}
    {{ 'collection-filters.js' | asset_url | script_tag: defer: true }}
{% endcase %}
```

## 🚨 Common Pitfalls

### 1. Over-Complex Logic
**Problem**: Template becomes unmaintainable
**Solution**: Move complex logic to snippets or consider JSON templates

### 2. Performance Issues
**Problem**: Expensive operations in loops
**Solution**: Use `limit`, `offset`, and efficient filtering

### 3. Missing Error Handling
**Problem**: Template breaks with missing data
**Solution**: Always check for object existence and provide fallbacks

### 4. Poor Accessibility
**Problem**: Custom markup lacks semantic structure
**Solution**: Use proper HTML5 elements and ARIA attributes

---

Liquid templates provide ultimate flexibility for custom Shopify theme development, but require careful consideration of maintainability, performance, and user experience compared to section-based JSON templates.