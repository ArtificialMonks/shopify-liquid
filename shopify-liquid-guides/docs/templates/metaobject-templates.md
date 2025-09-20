# Metaobject Templates - Custom Content Types (2024 Feature)

Metaobject templates represent the cutting-edge of Shopify theme development, enabling custom content types and data structures beyond traditional products, collections, and pages. Introduced in late 2024, this feature opens up new possibilities for content management and dynamic page creation.

## 🎯 What are Metaobject Templates?

### Core Concept
Metaobject templates allow you to:
- **Create custom content types** (Authors, Events, Locations, etc.)
- **Define custom data structures** with specific fields and relationships
- **Build dynamic pages** from structured data
- **Enable content management** beyond traditional Shopify resources

### Real-World Examples
✅ **Author pages** with biography, photo, and related articles
✅ **Event listings** with dates, locations, and ticket information
✅ **Location pages** with addresses, hours, and contact details
✅ **Recipe pages** with ingredients, instructions, and nutritional info
✅ **Team member profiles** with roles, skills, and contact information

## 🏗️ Metaobject Template Structure

### File Location and Naming
```
templates/
└── metaobject/
    ├── author.json         # For "author" metaobject type
    ├── event.json          # For "event" metaobject type
    ├── location.liquid     # Alternative liquid approach
    └── recipe.json         # For "recipe" metaobject type
```

### Basic JSON Structure
```json
{
  "sections": {
    "main": {
      "type": "main-metaobject",
      "settings": {
        "show_title": true,
        "show_description": true
      }
    },
    "related_content": {
      "type": "related-metaobjects",
      "settings": {
        "heading": "Related Items",
        "items_to_show": 3
      }
    }
  },
  "order": ["main", "related_content"]
}
```

### Custom Liquid Template
```liquid
{% comment %}
  Template: templates/metaobject/author.liquid
  Displays author metaobject with custom fields
{% endcomment %}

<div class="author-page">
  <header class="author-header">
    {% if metaobject.photo %}
      <div class="author-photo">
        {{ metaobject.photo.value | image_url: width: 300 | image_tag }}
      </div>
    {% endif %}

    <div class="author-info">
      <h1 class="author-name">{{ metaobject.display_name | escape }}</h1>

      {% if metaobject.title %}
        <div class="author-title">{{ metaobject.title.value | escape }}</div>
      {% endif %}

      {% if metaobject.bio %}
        <div class="author-bio">{{ metaobject.bio.value }}</div>
      {% endif %}

      {% if metaobject.social_links %}
        <div class="author-social">
          {% for link in metaobject.social_links.value %}
            <a href="{{ link.url }}" target="_blank" rel="noopener">
              {{ link.title | escape }}
            </a>
          {% endfor %}
        </div>
      {% endif %}
    </div>
  </header>

  {% if metaobject.expertise %}
    <section class="author-expertise">
      <h2>{{ 'metaobject.author.expertise' | t }}</h2>
      <div class="expertise-tags">
        {% for skill in metaobject.expertise.value %}
          <span class="expertise-tag">{{ skill | escape }}</span>
        {% endfor %}
      </div>
    </section>
  {% endif %}

  {% comment %} Related articles by this author {% endcomment %}
  {% assign author_articles = blog.articles | where: 'author', metaobject.display_name %}
  {% if author_articles.size > 0 %}
    <section class="author-articles">
      <h2>{{ 'metaobject.author.articles' | t }}</h2>
      <div class="articles-grid">
        {% for article in author_articles limit: 6 %}
          <article class="article-card">
            {% if article.image %}
              <div class="article-image">
                <a href="{{ article.url }}">
                  {{ article.image | image_url: width: 400 | image_tag }}
                </a>
              </div>
            {% endif %}

            <div class="article-content">
              <h3 class="article-title">
                <a href="{{ article.url }}">{{ article.title | escape }}</a>
              </h3>

              <div class="article-excerpt">
                {{ article.excerpt | truncatewords: 20 }}
              </div>

              <div class="article-meta">
                <time datetime="{{ article.published_at | date: '%Y-%m-%d' }}">
                  {{ article.published_at | date: format: 'month_day_year' }}
                </time>
              </div>
            </div>
          </article>
        {% endfor %}
      </div>
    </section>
  {% endif %}
</div>
```

## 🎨 Metaobject Field Types and Usage

### Text and Rich Text Fields
```liquid
{% comment %} Single line text {% endcomment %}
<h1>{{ metaobject.title.value | escape }}</h1>

{% comment %} Multi-line text {% endcomment %}
<div class="description">
  {{ metaobject.description.value | newline_to_br }}
</div>

{% comment %} Rich text with HTML {% endcomment %}
<div class="content">
  {{ metaobject.content.value }}
</div>
```

### Number and Date Fields
```liquid
{% comment %} Number field {% endcomment %}
<div class="price">
  ${{ metaobject.price.value | money_without_currency }}
</div>

{% comment %} Date field {% endcomment %}
<time datetime="{{ metaobject.event_date.value | date: '%Y-%m-%d' }}">
  {{ metaobject.event_date.value | date: format: 'month_day_year' }}
</time>

{% comment %} Date range {% endcomment %}
{% if metaobject.start_date and metaobject.end_date %}
  <div class="date-range">
    {{ metaobject.start_date.value | date: format: 'abbreviated_date' }} -
    {{ metaobject.end_date.value | date: format: 'abbreviated_date' }}
  </div>
{% endif %}
```

### Boolean and Selection Fields
```liquid
{% comment %} Boolean field {% endcomment %}
{% if metaobject.featured.value %}
  <span class="featured-badge">{{ 'general.featured' | t }}</span>
{% endif %}

{% comment %} Single select {% endcomment %}
<div class="category">
  {{ metaobject.category.value | escape }}
</div>

{% comment %} Multi-select {% endcomment %}
{% if metaobject.tags.value.size > 0 %}
  <div class="tags">
    {% for tag in metaobject.tags.value %}
      <span class="tag">{{ tag | escape }}</span>
    {% endfor %}
  </div>
{% endif %}
```

### File and Media Fields
```liquid
{% comment %} Image field {% endcomment %}
{% if metaobject.hero_image %}
  <div class="hero-image">
    {{ metaobject.hero_image.value | image_url: width: 1200 | image_tag }}
  </div>
{% endif %}

{% comment %} Multiple images {% endcomment %}
{% if metaobject.gallery.value.size > 0 %}
  <div class="image-gallery">
    {% for image in metaobject.gallery.value %}
      <div class="gallery-item">
        {{ image | image_url: width: 600 | image_tag }}
      </div>
    {% endfor %}
  </div>
{% endif %}

{% comment %} File download {% endcomment %}
{% if metaobject.pdf_file %}
  <a href="{{ metaobject.pdf_file.value.url }}"
     download="{{ metaobject.pdf_file.value.filename }}"
     class="download-link">
    {{ 'general.download' | t }}: {{ metaobject.pdf_file.value.filename }}
  </a>
{% endif %}
```

### Reference Fields
```liquid
{% comment %} Product reference {% endcomment %}
{% if metaobject.featured_product %}
  {% assign product = metaobject.featured_product.value %}
  <div class="featured-product">
    <h3>{{ product.title | escape }}</h3>
    <div class="price">{{ product.price | money }}</div>
    <a href="{{ product.url }}" class="product-link">
      {{ 'products.general.view_product' | t }}
    </a>
  </div>
{% endif %}

{% comment %} Collection reference {% endcomment %}
{% if metaobject.related_collection %}
  {% assign collection = metaobject.related_collection.value %}
  <div class="related-collection">
    <h3>{{ collection.title | escape }}</h3>
    <p>{{ collection.products_count }} {{ 'collections.general.items' | t }}</p>
    <a href="{{ collection.url }}">{{ 'collections.general.view_collection' | t }}</a>
  </div>
{% endif %}

{% comment %} Metaobject reference (relationships) {% endcomment %}
{% if metaobject.related_authors %}
  <div class="related-authors">
    <h3>{{ 'metaobject.related_authors' | t }}</h3>
    {% for author in metaobject.related_authors.value %}
      <div class="author-reference">
        <a href="{{ author.url }}">{{ author.display_name | escape }}</a>
      </div>
    {% endfor %}
  </div>
{% endif %}
```

## 🚀 Advanced Metaobject Patterns

### Event Template with Registration
```liquid
{% comment %} Event metaobject template {% endcomment %}
<div class="event-page">
  <header class="event-header">
    {% if metaobject.cover_image %}
      <div class="event-cover">
        {{ metaobject.cover_image.value | image_url: width: 1200 | image_tag }}
      </div>
    {% endif %}

    <div class="event-details">
      <h1 class="event-title">{{ metaobject.display_name | escape }}</h1>

      <div class="event-meta">
        <div class="event-date">
          <strong>{{ 'metaobject.event.date' | t }}:</strong>
          {{ metaobject.event_date.value | date: format: 'month_day_year' }}
        </div>

        {% if metaobject.start_time %}
          <div class="event-time">
            <strong>{{ 'metaobject.event.time' | t }}:</strong>
            {{ metaobject.start_time.value }} - {{ metaobject.end_time.value }}
          </div>
        {% endif %}

        {% if metaobject.location %}
          <div class="event-location">
            <strong>{{ 'metaobject.event.location' | t }}:</strong>
            {{ metaobject.location.value | escape }}
          </div>
        {% endif %}

        {% if metaobject.capacity %}
          <div class="event-capacity">
            <strong>{{ 'metaobject.event.capacity' | t }}:</strong>
            {{ metaobject.capacity.value }} {{ 'metaobject.event.attendees' | t }}
          </div>
        {% endif %}
      </div>

      {% if metaobject.registration_product %}
        {% assign ticket_product = metaobject.registration_product.value %}
        <div class="event-registration">
          {% form 'product', ticket_product %}
            <div class="ticket-price">
              {{ ticket_product.price | money }}
            </div>

            <button type="submit" class="btn btn-primary">
              {{ 'metaobject.event.register' | t }}
            </button>
          {% endform %}
        </div>
      {% endif %}
    </div>
  </header>

  {% if metaobject.description %}
    <section class="event-description">
      <h2>{{ 'metaobject.event.about' | t }}</h2>
      {{ metaobject.description.value }}
    </section>
  {% endif %}

  {% if metaobject.agenda %}
    <section class="event-agenda">
      <h2>{{ 'metaobject.event.agenda' | t }}</h2>
      {{ metaobject.agenda.value }}
    </section>
  {% endif %}

  {% if metaobject.speakers %}
    <section class="event-speakers">
      <h2>{{ 'metaobject.event.speakers' | t }}</h2>
      <div class="speakers-grid">
        {% for speaker in metaobject.speakers.value %}
          <div class="speaker-card">
            {% if speaker.photo %}
              <div class="speaker-photo">
                {{ speaker.photo.value | image_url: width: 200 | image_tag }}
              </div>
            {% endif %}
            <div class="speaker-info">
              <h3>{{ speaker.display_name | escape }}</h3>
              {% if speaker.title %}
                <div class="speaker-title">{{ speaker.title.value | escape }}</div>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </div>
    </section>
  {% endif %}
</div>
```

### Recipe Template with Structured Data
```liquid
{% comment %} Recipe metaobject with schema markup {% endcomment %}
<div class="recipe-page" itemscope itemtype="https://schema.org/Recipe">
  <header class="recipe-header">
    {% if metaobject.hero_image %}
      <div class="recipe-image">
        {{ metaobject.hero_image.value | image_url: width: 800 | image_tag: itemprop: 'image' }}
      </div>
    {% endif %}

    <div class="recipe-info">
      <h1 class="recipe-title" itemprop="name">{{ metaobject.display_name | escape }}</h1>

      {% if metaobject.description %}
        <div class="recipe-description" itemprop="description">
          {{ metaobject.description.value }}
        </div>
      {% endif %}

      <div class="recipe-meta">
        {% if metaobject.prep_time %}
          <div class="recipe-time">
            <strong>{{ 'metaobject.recipe.prep_time' | t }}:</strong>
            <time itemprop="prepTime" datetime="PT{{ metaobject.prep_time.value }}M">
              {{ metaobject.prep_time.value }} {{ 'metaobject.recipe.minutes' | t }}
            </time>
          </div>
        {% endif %}

        {% if metaobject.cook_time %}
          <div class="recipe-time">
            <strong>{{ 'metaobject.recipe.cook_time' | t }}:</strong>
            <time itemprop="cookTime" datetime="PT{{ metaobject.cook_time.value }}M">
              {{ metaobject.cook_time.value }} {{ 'metaobject.recipe.minutes' | t }}
            </time>
          </div>
        {% endif %}

        {% if metaobject.servings %}
          <div class="recipe-servings">
            <strong>{{ 'metaobject.recipe.servings' | t }}:</strong>
            <span itemprop="recipeYield">{{ metaobject.servings.value }}</span>
          </div>
        {% endif %}

        {% if metaobject.difficulty %}
          <div class="recipe-difficulty">
            <strong>{{ 'metaobject.recipe.difficulty' | t }}:</strong>
            {{ metaobject.difficulty.value | escape }}
          </div>
        {% endif %}
      </div>
    </div>
  </header>

  <div class="recipe-content">
    {% if metaobject.ingredients %}
      <section class="recipe-ingredients">
        <h2>{{ 'metaobject.recipe.ingredients' | t }}</h2>
        <ul>
          {% for ingredient in metaobject.ingredients.value %}
            <li itemprop="recipeIngredient">{{ ingredient | escape }}</li>
          {% endfor %}
        </ul>
      </section>
    {% endif %}

    {% if metaobject.instructions %}
      <section class="recipe-instructions">
        <h2>{{ 'metaobject.recipe.instructions' | t }}</h2>
        <div itemprop="recipeInstructions">
          {{ metaobject.instructions.value }}
        </div>
      </section>
    {% endif %}

    {% if metaobject.nutrition_info %}
      <section class="recipe-nutrition" itemprop="nutrition" itemscope itemtype="https://schema.org/NutritionInformation">
        <h2>{{ 'metaobject.recipe.nutrition' | t }}</h2>
        {{ metaobject.nutrition_info.value }}
      </section>
    {% endif %}
  </div>
</div>
```

## 🔧 Metaobject Section Integration

### Main Metaobject Section
```liquid
{% comment %} Section: sections/main-metaobject.liquid {% endcomment %}
<div class="metaobject-main" {{ section.shopify_attributes }}>
  {% if section.settings.show_title %}
    <h1 class="metaobject-title">{{ metaobject.display_name | escape }}</h1>
  {% endif %}

  {% if section.settings.show_description and metaobject.description %}
    <div class="metaobject-description">
      {{ metaobject.description.value }}
    </div>
  {% endif %}

  {% for field in metaobject.fields %}
    {% unless field.key == 'description' %}
      <div class="metaobject-field" data-field="{{ field.key }}">
        {% case field.type %}
          {% when 'single_line_text_field' %}
            <div class="field-text">{{ field.value | escape }}</div>
          {% when 'multi_line_text_field' %}
            <div class="field-multitext">{{ field.value | newline_to_br }}</div>
          {% when 'rich_text_field' %}
            <div class="field-richtext">{{ field.value }}</div>
          {% when 'file_reference' %}
            {% if field.value.media_type == 'image' %}
              <div class="field-image">
                {{ field.value | image_url: width: 600 | image_tag }}
              </div>
            {% endif %}
        {% endcase %}
      </div>
    {% endunless %}
  {% endfor %}
</div>

{% schema %}
{
  "name": "Main Metaobject",
  "settings": [
    {
      "type": "checkbox",
      "id": "show_title",
      "label": "Show title",
      "default": true
    },
    {
      "type": "checkbox",
      "id": "show_description",
      "label": "Show description",
      "default": true
    }
  ]
}
{% endschema %}
```

## 🌐 SEO and Schema Markup

### Dynamic SEO Meta Tags
```liquid
{% comment %} In layout/theme.liquid {% endcomment %}
{% if template.name == 'metaobject' %}
  {% if metaobject.seo_title %}
    <title>{{ metaobject.seo_title.value | escape }}</title>
  {% else %}
    <title>{{ metaobject.display_name | escape }} - {{ shop.name }}</title>
  {% endif %}

  {% if metaobject.seo_description %}
    <meta name="description" content="{{ metaobject.seo_description.value | escape }}">
  {% elsif metaobject.description %}
    <meta name="description" content="{{ metaobject.description.value | strip_html | truncatewords: 25 | escape }}">
  {% endif %}

  {% if metaobject.featured_image %}
    <meta property="og:image" content="{{ metaobject.featured_image.value | image_url: width: 1200 }}">
    <meta name="twitter:image" content="{{ metaobject.featured_image.value | image_url: width: 1200 }}">
  {% endif %}
{% endif %}
```

### Structured Data for Different Types
```liquid
{% comment %} Person schema for author metaobjects {% endcomment %}
{% if metaobject.type == 'author' %}
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": {{ metaobject.display_name | json }},
      {% if metaobject.bio %}"description": {{ metaobject.bio.value | strip_html | json }},{% endif %}
      {% if metaobject.photo %}"image": {{ metaobject.photo.value | image_url: width: 400 | json }},{% endif %}
      {% if metaobject.website %}"url": {{ metaobject.website.value | json }},{% endif %}
      "jobTitle": {{ metaobject.title.value | json }}
    }
  </script>
{% endif %}

{% comment %} Event schema for event metaobjects {% endcomment %}
{% if metaobject.type == 'event' %}
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Event",
      "name": {{ metaobject.display_name | json }},
      {% if metaobject.description %}"description": {{ metaobject.description.value | strip_html | json }},{% endif %}
      {% if metaobject.event_date %}"startDate": {{ metaobject.event_date.value | date: '%Y-%m-%d' | json }},{% endif %}
      {% if metaobject.location %}"location": {
        "@type": "Place",
        "name": {{ metaobject.location.value | json }}
      },{% endif %}
      {% if metaobject.registration_product %}"offers": {
        "@type": "Offer",
        "price": {{ metaobject.registration_product.value.price | money_without_currency | json }},
        "priceCurrency": {{ shop.currency | json }}
      }{% endif %}
    }
  </script>
{% endif %}
```

## 🛠️ Development Best Practices

### 1. Field Validation
```liquid
{% comment %} Always check field existence {% endcomment %}
{% if metaobject.custom_field and metaobject.custom_field.value != blank %}
  <div class="custom-content">{{ metaobject.custom_field.value }}</div>
{% endif %}
```

### 2. Performance Considerations
```liquid
{% comment %} Limit expensive operations {% endcomment %}
{% assign related_items = metaobject.related_metaobjects.value | limit: 5 %}
{% for item in related_items %}
  <!-- Process limited set -->
{% endfor %}
```

### 3. Responsive Design
```liquid
{% comment %} Responsive image handling {% endcomment %}
{% if metaobject.hero_image %}
  <picture>
    <source media="(min-width: 750px)"
            srcset="{{ metaobject.hero_image.value | image_url: width: 1200 }}">
    <img src="{{ metaobject.hero_image.value | image_url: width: 600 }}"
         alt="{{ metaobject.hero_image.value.alt | default: metaobject.display_name | escape }}">
  </picture>
{% endif %}
```

## 🚨 Common Challenges

### 1. Complex Data Relationships
**Challenge**: Managing related metaobjects and references
**Solution**: Use reference fields and careful data modeling

### 2. Performance with Large Datasets
**Challenge**: Slow loading with many related items
**Solution**: Implement pagination and lazy loading

### 3. Content Management Workflow
**Challenge**: Non-technical users managing complex structures
**Solution**: Provide clear field labels and helpful instructions

### 4. SEO for Dynamic Content
**Challenge**: Proper meta tags and structured data
**Solution**: Implement dynamic SEO patterns based on metaobject fields

---

Metaobject templates unlock powerful content management capabilities, enabling custom content types and dynamic page generation that goes far beyond traditional Shopify resources.