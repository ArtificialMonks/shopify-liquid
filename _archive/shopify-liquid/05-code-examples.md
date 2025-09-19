# Code Examples & Patterns

This section contains **real-world, production-ready** examples of custom Shopify sections. Each example includes the complete Liquid code, schema configuration, and explanations of key concepts.

> 💡 **Pro Tip**: Copy these examples as starting points and customize them for your specific needs!

---

## 1. Logo List Section

A flexible section for displaying client logos, sponsors, or brand partnerships.

### Features
- Upload multiple logo images
- Optional links for each logo
- Configurable logo sizes
- Responsive grid layout
- Placeholder support when no image is uploaded

### Complete Code

```liquid
<!-- Logo List Section -->
<style>
  .logo-bar {
    text-align: center;
    padding: 60px 0;
  }
  
  .logo-bar__title {
    font-size: 2rem;
    margin-bottom: 40px;
    color: #333;
  }
  
  .logo-bar__grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .logo-bar__item {
    display: inline-block;
    max-width: {{ section.settings.logo_width }};
    opacity: 0.7;
    transition: opacity 0.3s ease;
  }
  
  .logo-bar__item:hover {
    opacity: 1;
  }
  
  .logo-bar__item img {
    width: 100%;
    height: auto;
    max-height: 80px;
    object-fit: contain;
  }
  
  .placeholder-svg {
    width: 100%;
    height: 60px;
    opacity: 0.3;
  }
  
  @media (max-width: 768px) {
    .logo-bar__grid {
      gap: 20px;
    }
    .logo-bar__item {
      max-width: calc({{ section.settings.logo_width }} * 0.8);
    }
  }
</style>

<div class="logo-bar">
  {% if section.settings.title != blank %}
    <h2 class="logo-bar__title">{{ section.settings.title | escape }}</h2>
  {% endif %}

  {%- if section.blocks.size > 0 -%}
    <div class="logo-bar__grid">
      {%- for block in section.blocks -%}
        <div class="logo-bar__item" {{ block.shopify_attributes }}>
          {%- if block.settings.link != blank -%}
            <a href="{{ block.settings.link }}" target="_blank" rel="noopener">
          {%- endif -%}

          {%- if block.settings.image != blank -%}
            {{ block.settings.image | image_url: width: 320, height: 160 | image_tag: block.settings.image.alt, loading: 'lazy' }}
          {%- else -%}
            {{ 'logo' | placeholder_svg_tag: 'placeholder-svg' }}
          {%- endif -%}

          {%- if block.settings.link != blank -%}
            </a>
          {%- endif -%}
        </div>
      {%- endfor -%}
    </div>
  {%- endif -%}
</div>

{% schema %}
{
  "name": "Logo List",
  "class": "index-section",
  "max_blocks": 10,
  "settings": [
    {
      "type": "text",
      "id": "title",
      "label": "Heading",
      "default": "Our Partners"
    },
    {
      "type": "select",
      "id": "logo_width",
      "label": "Logo width",
      "default": "160px",
      "options": [
        {"label": "Extra Small", "value": "100px"},
        {"label": "Small", "value": "125px"},
        {"label": "Medium", "value": "160px"},
        {"label": "Large", "value": "175px"},
        {"label": "Extra Large", "value": "200px"}
      ]
    }
  ],
  "blocks": [
    {
      "type": "logo_image",
      "name": "Logo",
      "settings": [
        {
          "type": "image_picker",
          "id": "image",
          "label": "Image"
        },
        {
          "type": "url",
          "id": "link",
          "label": "Link",
          "info": "Optional"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Logo List",
      "category": "Image",
      "blocks": [
        {"type": "logo_image"},
        {"type": "logo_image"},
        {"type": "logo_image"},
        {"type": "logo_image"}
      ]
    }
  ]
}
{% endschema %}
```

### Key Learning Points

1. **Dynamic CSS**: `max-width: {{ section.settings.logo_width }}` uses Liquid in CSS
2. **Placeholder SVG**: `{{ 'logo' | placeholder_svg_tag }}` shows placeholder when no image
3. **Image Optimization**: `image_url: width: 320, height: 160` for better performance
4. **Block Attributes**: `{{ block.shopify_attributes }}` enables theme editor functionality
5. **Responsive Design**: Mobile-specific styles with media queries

---

## 2. Testimonial Carousel Section

A dynamic testimonial section with customer quotes, ratings, and photos.

### Features
- Multiple testimonial blocks
- Star ratings
- Customer photos
- Company names and titles
- Responsive carousel layout

### Complete Code

```liquid
<!-- Testimonial Section -->
<style>
  .testimonials-section {
    padding: 80px 0;
    background: #f8f9fa;
  }
  
  .testimonials-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    text-align: center;
  }
  
  .testimonials-title {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #333;
  }
  
  .testimonials-subtitle {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 50px;
  }
  
  .testimonials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 40px;
    margin-bottom: 40px;
  }
  
  .testimonial-card {
    background: white;
    padding: 40px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  }
  
  .testimonial-quote {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #333;
    margin-bottom: 20px;
    font-style: italic;
  }
  
  .testimonial-rating {
    margin-bottom: 20px;
  }
  
  .star {
    color: #ffc107;
    font-size: 1.2rem;
  }
  
  .testimonial-author {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
  }
  
  .author-photo {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .author-info {
    text-align: left;
  }
  
  .author-name {
    font-weight: bold;
    color: #333;
    margin: 0;
  }
  
  .author-title {
    color: #666;
    font-size: 0.9rem;
    margin: 2px 0 0 0;
  }
  
  .author-company {
    color: #007cba;
    font-size: 0.9rem;
    margin: 2px 0 0 0;
  }
  
  @media (max-width: 768px) {
    .testimonials-grid {
      grid-template-columns: 1fr;
    }
    
    .testimonial-card {
      padding: 30px 20px;
    }
  }
</style>

<div class="testimonials-section" id="section-{{ section.id }}">
  <div class="testimonials-container">
    {% if section.settings.title != blank %}
      <h2 class="testimonials-title">{{ section.settings.title | escape }}</h2>
    {% endif %}
    
    {% if section.settings.subtitle != blank %}
      <p class="testimonials-subtitle">{{ section.settings.subtitle | escape }}</p>
    {% endif %}
    
    {% if section.blocks.size > 0 %}
      <div class="testimonials-grid">
        {% for block in section.blocks %}
          {% case block.type %}
            {% when 'testimonial' %}
              <div class="testimonial-card" {{ block.shopify_attributes }}>
                {% if block.settings.quote != blank %}
                  <blockquote class="testimonial-quote">
                    "{{ block.settings.quote | escape }}"
                  </blockquote>
                {% endif %}
                
                {% if block.settings.rating > 0 %}
                  <div class="testimonial-rating">
                    {% for i in (1..5) %}
                      {% if i <= block.settings.rating %}
                        <span class="star">★</span>
                      {% else %}
                        <span class="star" style="color: #ddd;">★</span>
                      {% endif %}
                    {% endfor %}
                  </div>
                {% endif %}
                
                <div class="testimonial-author">
                  {% if block.settings.photo %}
                    <img src="{{ block.settings.photo | image_url: width: 120 }}" 
                         alt="{{ block.settings.author_name }}" 
                         class="author-photo"
                         loading="lazy">
                  {% endif %}
                  
                  <div class="author-info">
                    {% if block.settings.author_name != blank %}
                      <p class="author-name">{{ block.settings.author_name | escape }}</p>
                    {% endif %}
                    {% if block.settings.author_title != blank %}
                      <p class="author-title">{{ block.settings.author_title | escape }}</p>
                    {% endif %}
                    {% if block.settings.company != blank %}
                      <p class="author-company">{{ block.settings.company | escape }}</p>
                    {% endif %}
                  </div>
                </div>
              </div>
          {% endcase %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>

{% schema %}
{
  "name": "Customer Testimonials",
  "tag": "section",
  "class": "testimonials",
  "max_blocks": 12,
  "settings": [
    {
      "type": "text",
      "id": "title",
      "label": "Section Title",
      "default": "What Our Customers Say"
    },
    {
      "type": "text",
      "id": "subtitle", 
      "label": "Subtitle",
      "default": "Don't just take our word for it"
    }
  ],
  "blocks": [
    {
      "type": "testimonial",
      "name": "Testimonial",
      "settings": [
        {
          "type": "textarea",
          "id": "quote",
          "label": "Customer Quote",
          "default": "This product exceeded my expectations!"
        },
        {
          "type": "range",
          "id": "rating",
          "label": "Star Rating",
          "min": 1,
          "max": 5,
          "step": 1,
          "default": 5
        },
        {
          "type": "text",
          "id": "author_name",
          "label": "Customer Name",
          "default": "John Smith"
        },
        {
          "type": "text",
          "id": "author_title", 
          "label": "Job Title",
          "default": "Marketing Director"
        },
        {
          "type": "text",
          "id": "company",
          "label": "Company",
          "default": "ABC Company"
        },
        {
          "type": "image_picker",
          "id": "photo",
          "label": "Customer Photo"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Customer Testimonials",
      "category": "Text",
      "blocks": [
        {
          "type": "testimonial",
          "settings": {
            "quote": "Absolutely love this product! The quality is outstanding and customer service was excellent.",
            "rating": 5,
            "author_name": "Sarah Johnson",
            "author_title": "Business Owner",
            "company": "Johnson & Co"
          }
        },
        {
          "type": "testimonial", 
          "settings": {
            "quote": "Fast shipping and exactly what I ordered. Will definitely be purchasing again!",
            "rating": 5,
            "author_name": "Mike Chen",
            "author_title": "Operations Manager", 
            "company": "Tech Solutions Inc"
          }
        }
      ]
    }
  ]
}
{% endschema %}
```

### Key Learning Points

1. **For Loops in Liquid**: `{% for i in (1..5) %}` creates star ratings
2. **Conditional Logic**: Complex if/else structures for optional content
3. **CSS Grid**: Modern responsive layout with `grid-template-columns`
4. **Block Types**: Using `{% case block.type %}` to handle different block types
5. **Default Content**: Presets with realistic sample data

---

## 3. Product Recommendations Section

Dynamic product recommendations powered by Shopify's machine learning.

### Features
- AI-powered product suggestions
- Configurable number of products
- AJAX loading for better performance
- Customizable styling
- Integration with cart functionality

### Complete Code

```liquid
<!-- Product Recommendations Section -->
<style>
  .product-recommendations {
    padding: 60px 0;
  }
  
  .recommendations-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .recommendations-title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 40px;
    color: #333;
  }
  
  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
  }
  
  .product-card {
    border: 1px solid #eee;
    border-radius: 8px;
    overflow: hidden;
    transition: box-shadow 0.3s ease;
  }
  
  .product-card:hover {
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  }
  
  .product-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  
  .product-card:hover .product-image {
    transform: scale(1.05);
  }
  
  .product-info {
    padding: 20px;
  }
  
  .product-title {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
    text-decoration: none;
  }
  
  .product-title:hover {
    color: #007cba;
  }
  
  .product-price {
    font-size: 1.2rem;
    font-weight: bold;
    color: #007cba;
  }
  
  .loading-spinner {
    text-align: center;
    padding: 40px;
    color: #666;
  }
</style>

{%- if section.settings.show_product_recommendations -%}
  <div class="product-recommendations" 
       data-product-id="{{ product.id }}" 
       data-limit="{{ section.settings.products_to_show }}"
       data-section-id="{{ section.id }}">
    
    <div class="recommendations-container">
      {% if section.settings.title != blank %}
        <h2 class="recommendations-title">{{ section.settings.title | escape }}</h2>
      {% endif %}
      
      {%- if recommendations.performed and recommendations.products_count > 0 -%}
        <div class="products-grid">
          {%- for product in recommendations.products limit: section.settings.products_to_show -%}
            <div class="product-card">
              <a href="{{ product.url }}">
                {% if product.featured_image %}
                  <img src="{{ product.featured_image | image_url: width: 400 }}" 
                       alt="{{ product.title | escape }}" 
                       class="product-image"
                       loading="lazy">
                {% endif %}
              </a>
              
              <div class="product-info">
                <a href="{{ product.url }}" class="product-title">
                  {{ product.title | escape }}
                </a>
                <div class="product-price">
                  {{ product.price | money }}
                </div>
              </div>
            </div>
          {%- endfor -%}
        </div>
      {%- else -%}
        <div class="loading-spinner">
          <p>Loading recommendations...</p>
        </div>
      {%- endif -%}
    </div>
  </div>
{%- endif -%}

{% schema %}
{
  "name": "Product Recommendations",
  "settings": [
    {
      "type": "checkbox",
      "id": "show_product_recommendations",
      "label": "Show product recommendations",
      "default": true
    },
    {
      "type": "text",
      "id": "title",
      "label": "Section title",
      "default": "You may also like"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "label": "Products to show",
      "min": 3,
      "max": 12,
      "step": 1,
      "default": 6
    }
  ],
  "presets": [
    {
      "name": "Product Recommendations"
    }
  ]
}
{% endschema %}

{% javascript %}
// Enhanced product recommendations with AJAX loading
var loadProductRecommendations = function() {
  var productRecommendationsSection = document.querySelector('.product-recommendations');
  if (!productRecommendationsSection) return;
  
  var productId = productRecommendationsSection.dataset.productId;
  var limit = productRecommendationsSection.dataset.limit;
  var sectionId = productRecommendationsSection.dataset.sectionId;
  
  if (!productId) return;
  
  var requestUrl = '/recommendations/products?section_id=product-recommendations&limit=' + limit + '&product_id=' + productId;
  
  fetch(requestUrl)
    .then(response => response.text())
    .then(html => {
      var tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      var newContent = tempDiv.querySelector('.product-recommendations');
      
      if (newContent) {
        productRecommendationsSection.innerHTML = newContent.innerHTML;
      }
    })
    .catch(error => {
      console.error('Error loading product recommendations:', error);
    });
};

// Load recommendations when page loads
document.addEventListener('DOMContentLoaded', loadProductRecommendations);

// Reload recommendations when section is updated in theme editor
document.addEventListener('shopify:section:load', function(event) {
  if (event.detail.sectionId.includes('product-recommendations')) {
    loadProductRecommendations();
  }
});
{% endjavascript %}
```

### Key Learning Points

1. **AJAX Integration**: Using JavaScript to load recommendations dynamically
2. **Data Attributes**: Passing data from Liquid to JavaScript
3. **Shopify APIs**: Using `/recommendations/products` endpoint
4. **Theme Editor Events**: Handling `shopify:section:load` events
5. **Error Handling**: Graceful fallbacks when recommendations fail

---

## 4. FAQ Accordion Section

An accessible FAQ section with expandable/collapsible answers.

### Features
- Expandable FAQ items
- Keyboard accessibility
- Multiple FAQ blocks
- Optional search functionality
- Responsive design

### Complete Code

```liquid
<!-- FAQ Accordion Section -->
<style>
  .faq-section {
    padding: 80px 0;
    background: white;
  }
  
  .faq-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .faq-title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 50px;
    color: #333;
  }
  
  .faq-item {
    border-bottom: 1px solid #eee;
    margin-bottom: 0;
  }
  
  .faq-question {
    width: 100%;
    background: none;
    border: none;
    padding: 30px 60px 30px 0;
    text-align: left;
    font-size: 1.2rem;
    font-weight: 600;
    color: #333;
    cursor: pointer;
    position: relative;
    transition: color 0.3s ease;
  }
  
  .faq-question:hover {
    color: #007cba;
  }
  
  .faq-question:focus {
    outline: 2px solid #007cba;
    outline-offset: 2px;
  }
  
  .faq-question::after {
    content: '+';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2rem;
    font-weight: 300;
    transition: transform 0.3s ease;
  }
  
  .faq-question.active::after {
    transform: translateY(-50%) rotate(45deg);
  }
  
  .faq-answer {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, padding 0.3s ease;
    padding: 0 0 0 0;
  }
  
  .faq-answer.active {
    max-height: 500px;
    padding: 0 0 30px 0;
  }
  
  .faq-answer-content {
    color: #666;
    line-height: 1.6;
    font-size: 1rem;
  }
  
  .faq-answer-content p {
    margin-bottom: 15px;
  }
  
  .faq-answer-content p:last-child {
    margin-bottom: 0;
  }
  
  @media (max-width: 768px) {
    .faq-question {
      padding-right: 50px;
      font-size: 1.1rem;
    }
    
    .faq-question::after {
      right: 15px;
      font-size: 1.5rem;
    }
  }
</style>

<div class="faq-section" id="section-{{ section.id }}">
  <div class="faq-container">
    {% if section.settings.title != blank %}
      <h2 class="faq-title">{{ section.settings.title | escape }}</h2>
    {% endif %}
    
    {% if section.blocks.size > 0 %}
      <div class="faq-list">
        {% for block in section.blocks %}
          {% case block.type %}
            {% when 'faq_item' %}
              <div class="faq-item" {{ block.shopify_attributes }}>
                <button class="faq-question" 
                        type="button"
                        aria-expanded="false"
                        data-faq-toggle>
                  {{ block.settings.question | escape }}
                </button>
                <div class="faq-answer" data-faq-answer>
                  <div class="faq-answer-content">
                    {{ block.settings.answer }}
                  </div>
                </div>
              </div>
          {% endcase %}
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>

{% schema %}
{
  "name": "FAQ Accordion",
  "tag": "section",
  "class": "faq-section",
  "max_blocks": 20,
  "settings": [
    {
      "type": "text",
      "id": "title",
      "label": "Section Title",
      "default": "Frequently Asked Questions"
    }
  ],
  "blocks": [
    {
      "type": "faq_item",
      "name": "FAQ Item",
      "settings": [
        {
          "type": "text",
          "id": "question",
          "label": "Question",
          "default": "What is your return policy?"
        },
        {
          "type": "richtext",
          "id": "answer",
          "label": "Answer", 
          "default": "<p>We offer a 30-day return policy on all items. Items must be in original condition with tags attached.</p>"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "FAQ Accordion",
      "category": "Text",
      "blocks": [
        {
          "type": "faq_item",
          "settings": {
            "question": "How long does shipping take?",
            "answer": "<p>Standard shipping takes 3-5 business days. Express shipping is available for 1-2 day delivery.</p>"
          }
        },
        {
          "type": "faq_item",
          "settings": {
            "question": "What is your return policy?", 
            "answer": "<p>We offer a 30-day return policy on all items. Items must be in original condition with tags attached.</p>"
          }
        },
        {
          "type": "faq_item",
          "settings": {
            "question": "Do you ship internationally?",
            "answer": "<p>Yes, we ship to most countries worldwide. International shipping rates apply.</p>"
          }
        }
      ]
    }
  ]
}
{% endschema %}

{% javascript %}
// FAQ Accordion Functionality
document.addEventListener('DOMContentLoaded', function() {
  const faqToggles = document.querySelectorAll('[data-faq-toggle]');
  
  faqToggles.forEach(function(toggle) {
    toggle.addEventListener('click', function() {
      const answer = this.nextElementSibling;
      const isOpen = this.classList.contains('active');
      
      // Close all other FAQ items
      faqToggles.forEach(function(otherToggle) {
        const otherAnswer = otherToggle.nextElementSibling;
        otherToggle.classList.remove('active');
        otherAnswer.classList.remove('active');
        otherToggle.setAttribute('aria-expanded', 'false');
      });
      
      // Toggle current FAQ item
      if (!isOpen) {
        this.classList.add('active');
        answer.classList.add('active');
        this.setAttribute('aria-expanded', 'true');
      }
    });
    
    // Keyboard accessibility
    toggle.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });
});

// Handle theme editor reloads
document.addEventListener('shopify:section:load', function(event) {
  if (event.detail.sectionId.includes('faq')) {
    // Re-initialize FAQ functionality after section reload
    const newToggles = event.target.querySelectorAll('[data-faq-toggle]');
    // Add event listeners to new elements...
  }
});
{% endjavascript %}
```

### Key Learning Points

1. **Accessibility**: Proper ARIA attributes and keyboard navigation
2. **JavaScript Events**: DOM event handling and section reloads
3. **CSS Animations**: Smooth expand/collapse with max-height transitions
4. **Rich Text**: Using `richtext` setting type for formatted answers
5. **Progressive Enhancement**: Works without JavaScript

---

## Common Patterns & Best Practices

### Pattern 1: Conditional Content Display

```liquid
<!-- Always check if content exists before displaying -->
{% if section.settings.title != blank %}
  <h2>{{ section.settings.title | escape }}</h2>
{% endif %}

<!-- For images, check the setting exists -->
{% if section.settings.background_image %}
  <img src="{{ section.settings.background_image | image_url: width: 1200 }}" 
       alt="{{ section.settings.background_image.alt | escape }}">
{% endif %}
```

### Pattern 2: Loop with Fallbacks

```liquid
<!-- Always check if blocks exist before looping -->
{% if section.blocks.size > 0 %}
  {% for block in section.blocks %}
    <!-- Content here -->
  {% endfor %}
{% else %}
  <p>No content available.</p>
{% endif %}
```

### Pattern 3: Responsive Images

```liquid
<!-- Use responsive image sizes -->
<img src="{{ image | image_url: width: 800 }}"
     srcset="{{ image | image_url: width: 400 }} 400w,
             {{ image | image_url: width: 800 }} 800w,
             {{ image | image_url: width: 1200 }} 1200w"
     sizes="(max-width: 768px) 400px, 800px"
     alt="{{ image.alt | escape }}"
     loading="lazy">
```

### Pattern 4: Safe Text Output

```liquid
<!-- Always escape user input -->
<h2>{{ section.settings.heading | escape }}</h2>

<!-- Rich text doesn't need escaping -->
<div class="content">{{ section.settings.rich_text }}</div>

<!-- URLs should be filtered -->
<a href="{{ section.settings.link_url | url }}">Link Text</a>
```

### Pattern 5: CSS Custom Properties

```liquid
<!-- Use CSS custom properties for dynamic styling -->
<style>
  .my-section {
    --text-color: {{ section.settings.text_color }};
    --bg-color: {{ section.settings.background_color }};
    --spacing: {{ section.settings.spacing }}px;
    
    color: var(--text-color);
    background-color: var(--bg-color);
    padding: var(--spacing) 0;
  }
</style>
```

---

## Performance Tips

1. **Optimize Images**: Always specify width/height parameters
2. **Lazy Loading**: Use `loading="lazy"` for below-the-fold images  
3. **Minimal JavaScript**: Keep JS under 16KB for theme store approval
4. **CSS in Head**: Move critical CSS to theme.liquid for better loading
5. **Preload Key Assets**: Use `preload_tag` filter for critical resources

---

## Next Steps

Ready to dive deeper? Check out:
- [Best Practices & Performance](./06-best-practices.md) for optimization techniques
- [Theme Editor Integration](./07-theme-editor.md) for better merchant experience  
- [Troubleshooting Guide](./09-troubleshooting.md) for debugging help
