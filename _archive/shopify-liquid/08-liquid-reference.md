# Liquid Object Reference - Complete Cheatsheet

This comprehensive reference covers all Liquid objects, properties, and methods available in Shopify themes. Think of this as your **quick lookup guide** when writing section templates.

> 💡 **Bookmark this page!** You'll reference these objects constantly when building custom sections.

---

## Section-Specific Objects

### `section` Object
Available in all section templates.

```liquid
{{ section.id }}                    <!-- Unique section ID -->
{{ section.type }}                  <!-- Section filename without .liquid -->
{{ section.index }}                 <!-- Section position on page (1-based) -->
{{ section.settings.your_setting }} <!-- Access schema settings -->
{{ section.blocks }}                <!-- Array of blocks -->
{{ section.blocks.size }}           <!-- Number of blocks -->
```

### `block` Object
Available when looping through `section.blocks`.

```liquid
{{ block.id }}                    <!-- Unique block ID -->
{{ block.type }}                  <!-- Block type from schema -->
{{ block.settings.your_setting }} <!-- Access block settings -->
{{ block.shopify_attributes }}    <!-- Required for theme editor -->
```

---

## Product Objects

### `product` Object
The main product object with all product data.

#### Basic Properties
```liquid
{{ product.id }}                     <!-- Product ID -->
{{ product.title }}                  <!-- Product name -->
{{ product.handle }}                 <!-- URL handle -->
{{ product.description }}            <!-- Product description -->
{{ product.content }}               <!-- Alias for description -->
{{ product.vendor }}                 <!-- Product vendor/brand -->
{{ product.type }}                   <!-- Product type -->
{{ product.url }}                    <!-- Relative product URL -->
{{ product.tags }}                   <!-- Array of tags -->
```

#### Pricing
```liquid
{{ product.price }}                  <!-- Minimum variant price -->
{{ product.price_min }}              <!-- Minimum price -->
{{ product.price_max }}              <!-- Maximum price -->
{{ product.price_varies }}           <!-- true/false if prices vary -->
{{ product.compare_at_price_min }}   <!-- Compare at price (min) -->
{{ product.compare_at_price_max }}   <!-- Compare at price (max) -->
{{ product.compare_at_price_varies }} <!-- true/false if compare prices vary -->
```

#### Availability
```liquid
{{ product.available }}              <!-- true/false if available -->
{{ product.first_available_variant }} <!-- First available variant object -->
{{ product.selected_variant }}       <!-- Currently selected variant -->
{{ product.selected_or_first_available_variant }} <!-- Smart variant selection -->
```

#### Images
```liquid
{{ product.featured_image }}         <!-- Main product image -->
{{ product.images }}                 <!-- Array of all images -->
{{ product.images.size }}           <!-- Number of images -->

<!-- Loop through images -->
{% for image in product.images %}
  {{ image | image_url: width: 800 }}
{% endfor %}
```

#### Variants & Options
```liquid
{{ product.variants }}              <!-- Array of all variants -->
{{ product.variants.size }}         <!-- Number of variants -->
{{ product.options }}               <!-- Array of option names -->
{{ product.options.size }}          <!-- Number of options (max 3) -->
{{ product.options_with_values }}   <!-- Options with available values -->
```

#### Collections
```liquid
{{ product.collections }}           <!-- Array of collections this product belongs to -->

<!-- Loop through collections -->
{% for collection in product.collections %}
  {{ collection.title }}
{% endfor %}
```

#### Advanced Properties
```liquid
{{ product.template_suffix }}       <!-- Custom template suffix -->
{{ product.published_at }}          <!-- Publication date -->
{{ product.created_at }}           <!-- Creation date -->
{{ product.updated_at }}           <!-- Last update date -->
```

### `variant` Object
Individual product variant data.

#### Basic Properties
```liquid
{{ variant.id }}                    <!-- Variant ID -->
{{ variant.title }}                 <!-- Concatenated option values -->
{{ variant.price }}                 <!-- Variant price -->
{{ variant.compare_at_price }}      <!-- Compare at price -->
{{ variant.sku }}                   <!-- Stock keeping unit -->
{{ variant.barcode }}              <!-- Barcode -->
{{ variant.url }}                   <!-- Variant-specific URL -->
```

#### Options
```liquid
{{ variant.option1 }}               <!-- First option value -->
{{ variant.option2 }}               <!-- Second option value -->
{{ variant.option3 }}               <!-- Third option value -->
```

#### Inventory
```liquid
{{ variant.available }}             <!-- true/false availability -->
{{ variant.inventory_quantity }}    <!-- Available quantity -->
{{ variant.inventory_management }}  <!-- Inventory tracking service -->
{{ variant.inventory_policy }}      <!-- "deny" or "continue" -->
{{ variant.incoming }}              <!-- true/false incoming inventory -->
{{ variant.next_incoming_date }}    <!-- Next restock date -->
```

#### Shipping & Tax
```liquid
{{ variant.weight }}                <!-- Weight in grams -->
{{ variant.weight_unit }}           <!-- Weight unit -->
{{ variant.weight_in_unit }}        <!-- Weight in specified unit -->
{{ variant.requires_shipping }}     <!-- true/false -->
{{ variant.taxable }}               <!-- true/false -->
```

#### Selection State
```liquid
{{ variant.selected }}              <!-- true/false if currently selected -->
```

#### Image
```liquid
{{ variant.image }}                 <!-- Associated variant image -->
```

---

## Collection Objects

### `collection` Object
Collection data and products.

#### Basic Properties
```liquid
{{ collection.id }}                 <!-- Collection ID -->
{{ collection.title }}              <!-- Collection name -->
{{ collection.handle }}             <!-- URL handle -->
{{ collection.description }}        <!-- Collection description -->
{{ collection.url }}                <!-- Collection URL -->
{{ collection.template_suffix }}    <!-- Custom template suffix -->
```

#### Products
```liquid
{{ collection.products }}           <!-- Array of products (max 50) -->
{{ collection.products_count }}     <!-- Products in current view -->
{{ collection.all_products_count }} <!-- Total products in collection -->
```

#### Sorting & Types
```liquid
{{ collection.default_sort_by }}    <!-- Default sort order -->
{{ collection.all_types }}          <!-- Array of all product types -->
{{ collection.all_vendors }}        <!-- Array of all vendors -->
{{ collection.current_type }}       <!-- Current type filter -->
{{ collection.current_vendor }}     <!-- Current vendor filter -->
```

#### Image
```liquid
{{ collection.image }}              <!-- Collection image -->
{{ collection.image.src }}          <!-- Image URL -->
```

#### Pagination
```liquid
{{ collection.next_product }}       <!-- Next product URL -->
{{ collection.previous_product }}   <!-- Previous product URL -->
```

#### Tags
```liquid
{{ collection.tags }}               <!-- Tags in current view -->
```

#### Publishing
```liquid
{{ collection.published_at }}       <!-- Publication date -->
```

---

## Cart Objects

### `cart` Object
Shopping cart data.

#### Basic Properties
```liquid
{{ cart.item_count }}               <!-- Total number of items -->
{{ cart.total_price }}              <!-- Total cart price -->
{{ cart.total_weight }}             <!-- Total cart weight -->
{{ cart.original_total_price }}     <!-- Price before discounts -->
```

#### Cart Items
```liquid
{{ cart.items }}                    <!-- Array of line items -->

<!-- Loop through cart items -->
{% for item in cart.items %}
  {{ item.title }}
  {{ item.quantity }}
  {{ item.price }}
{% endfor %}
```

#### Custom Attributes
```liquid
{{ cart.note }}                     <!-- Cart note -->
{{ cart.attributes }}               <!-- Custom cart attributes -->

<!-- Access specific attribute -->
{{ cart.attributes['gift-wrap'] }}
```

### `line_item` Object
Individual cart item data.

#### Basic Properties
```liquid
{{ line_item.id }}                  <!-- Line item ID -->
{{ line_item.key }}                 <!-- Unique identifier -->
{{ line_item.title }}               <!-- Product + variant title -->
{{ line_item.quantity }}            <!-- Quantity -->
{{ line_item.price }}               <!-- Unit price -->
{{ line_item.line_price }}          <!-- Total line price -->
{{ line_item.original_price }}      <!-- Price before discounts -->
{{ line_item.original_line_price }} <!-- Line price before discounts -->
{{ line_item.total_discount }}      <!-- Total discount amount -->
```

#### Product Data
```liquid
{{ line_item.product }}             <!-- Product object -->
{{ line_item.product_id }}          <!-- Product ID -->
{{ line_item.variant }}             <!-- Variant object -->
{{ line_item.variant_id }}          <!-- Variant ID -->
{{ line_item.vendor }}              <!-- Product vendor -->
{{ line_item.sku }}                 <!-- Variant SKU -->
```

#### Properties
```liquid
{{ line_item.properties }}          <!-- Custom line item properties -->

<!-- Loop through properties -->
{% for property in line_item.properties %}
  {{ property.first }}: {{ property.last }}
{% endfor %}
```

#### Shipping & Tax
```liquid
{{ line_item.requires_shipping }}   <!-- true/false -->
{{ line_item.taxable }}             <!-- true/false -->
{{ line_item.grams }}               <!-- Weight in grams -->
```

#### Images
```liquid
{{ line_item.image }}               <!-- Variant or product image -->
```

#### Gift Cards
```liquid
{{ line_item.gift_card }}           <!-- true/false if gift card -->
```

#### Fulfillment
```liquid
{{ line_item.fulfillment }}         <!-- Fulfillment object -->
{{ line_item.fulfillment_service }} <!-- Fulfillment service -->
{{ line_item.successfully_fulfilled_quantity }} <!-- Fulfilled quantity -->
```

#### Discounts
```liquid
{{ line_item.discounts }}           <!-- Array of discounts -->
{{ line_item.message }}             <!-- Discount message -->
```

---

## Customer Objects

### `customer` Object
Logged-in customer data.

#### Basic Properties
```liquid
{{ customer.id }}                   <!-- Customer ID -->
{{ customer.email }}                <!-- Email address -->
{{ customer.first_name }}           <!-- First name -->
{{ customer.last_name }}            <!-- Last name -->
{{ customer.name }}                 <!-- Full name -->
{{ customer.accepts_marketing }}    <!-- Marketing consent -->
{{ customer.has_account }}          <!-- true/false -->
```

#### Addresses
```liquid
{{ customer.addresses }}            <!-- Array of addresses -->
{{ customer.addresses_count }}      <!-- Number of addresses -->
{{ customer.default_address }}      <!-- Default address object -->
```

#### Orders
```liquid
{{ customer.orders }}               <!-- Array of orders -->
{{ customer.orders_count }}         <!-- Number of orders -->
{{ customer.last_order }}           <!-- Most recent order -->
{{ customer.total_spent }}          <!-- Total amount spent -->
```

#### Tags
```liquid
{{ customer.tags }}                 <!-- Customer tags -->
```

### `address` Object
Customer address data.

```liquid
{{ address.id }}                    <!-- Address ID -->
{{ address.first_name }}            <!-- First name -->
{{ address.last_name }}             <!-- Last name -->
{{ address.name }}                  <!-- Full name -->
{{ address.company }}               <!-- Company name -->
{{ address.address1 }}              <!-- Address line 1 -->
{{ address.address2 }}              <!-- Address line 2 -->
{{ address.street }}                <!-- Combined address lines -->
{{ address.city }}                  <!-- City -->
{{ address.province }}              <!-- Province/state name -->
{{ address.province_code }}         <!-- Province/state code -->
{{ address.zip }}                   <!-- Postal/zip code -->
{{ address.country }}               <!-- Country name -->
{{ address.country_code }}          <!-- Country code -->
{{ address.phone }}                 <!-- Phone number -->
```

---

## Blog Objects

### `blog` Object
Blog data and articles.

#### Basic Properties
```liquid
{{ blog.id }}                       <!-- Blog ID -->
{{ blog.title }}                    <!-- Blog title -->
{{ blog.handle }}                   <!-- URL handle -->
{{ blog.url }}                      <!-- Blog URL -->
```

#### Articles
```liquid
{{ blog.articles }}                 <!-- Array of articles -->
{{ blog.articles_count }}           <!-- Article count -->
```

#### Comments
```liquid
{{ blog.comments_enabled? }}        <!-- true/false -->
{{ blog.moderated? }}               <!-- true/false -->
```

#### Tags
```liquid
{{ blog.tags }}                     <!-- Tags in current view -->
{{ blog.all_tags }}                 <!-- All blog tags -->
```

#### Navigation
```liquid
{{ blog.next_article }}             <!-- Next article URL -->
{{ blog.previous_article }}         <!-- Previous article URL -->
```

### `article` Object
Individual blog article data.

#### Basic Properties
```liquid
{{ article.id }}                    <!-- Article ID -->
{{ article.title }}                 <!-- Article title -->
{{ article.content }}               <!-- Article content -->
{{ article.excerpt }}               <!-- Article excerpt -->
{{ article.excerpt_or_content }}    <!-- Excerpt or content -->
{{ article.url }}                   <!-- Article URL -->
{{ article.author }}                <!-- Author name -->
```

#### Dates
```liquid
{{ article.created_at }}            <!-- Creation date -->
{{ article.published_at }}          <!-- Publication date -->
```

#### Comments
```liquid
{{ article.comments }}              <!-- Array of comments -->
{{ article.comments_count }}        <!-- Comment count -->
{{ article.comments_enabled? }}     <!-- true/false -->
{{ article.moderated? }}            <!-- true/false -->
{{ article.comment_post_url }}      <!-- Comment submission URL -->
```

#### Tags
```liquid
{{ article.tags }}                  <!-- Article tags -->
```

#### Images
```liquid
{{ article.image }}                 <!-- Article image -->
{{ article.image.src }}             <!-- Image URL -->
```

#### Author Details
```liquid
{{ article.user.account_owner }}    <!-- true/false -->
{{ article.user.bio }}              <!-- Author bio -->
{{ article.user.email }}            <!-- Author email -->
{{ article.user.first_name }}       <!-- Author first name -->
{{ article.user.last_name }}        <!-- Author last name -->
{{ article.user.homepage }}         <!-- Author website -->
```

### `comment` Object
Blog comment data.

```liquid
{{ comment.id }}                    <!-- Comment ID -->
{{ comment.author }}                <!-- Commenter name -->
{{ comment.email }}                 <!-- Commenter email -->
{{ comment.content }}               <!-- Comment content -->
{{ comment.status }}                <!-- "published", "unapproved", etc. -->
{{ comment.url }}                   <!-- Comment anchor URL -->
{{ comment.created_at }}            <!-- Creation date -->
```

---

## Shop Objects

### `shop` Object
Store information.

#### Basic Properties
```liquid
{{ shop.name }}                     <!-- Store name -->
{{ shop.description }}              <!-- Store description -->
{{ shop.domain }}                   <!-- Primary domain -->
{{ shop.permanent_domain }}         <!-- .myshopify.com domain -->
{{ shop.url }}                      <!-- Full store URL -->
{{ shop.secure_url }}               <!-- HTTPS store URL -->
{{ shop.email }}                    <!-- Store email -->
```

#### Address
```liquid
{{ shop.address }}                  <!-- Address object -->
{{ shop.address.summary }}          <!-- Formatted address -->
{{ shop.address.street }}           <!-- Street address -->
{{ shop.address.city }}             <!-- City -->
{{ shop.address.province }}         <!-- Province/state -->
{{ shop.address.province_code }}    <!-- Province/state code -->
{{ shop.address.country }}          <!-- Country -->
{{ shop.address.country_upper }}    <!-- Country (uppercase) -->
{{ shop.address.zip }}              <!-- Postal code -->
```

#### Currency & Money
```liquid
{{ shop.currency }}                 <!-- Currency code (USD, CAD, etc.) -->
{{ shop.money_format }}             <!-- Money format string -->
{{ shop.money_with_currency_format }} <!-- Money with currency format -->
```

#### Counts
```liquid
{{ shop.products_count }}           <!-- Total products -->
{{ shop.collections_count }}        <!-- Total collections -->
```

#### Product Data
```liquid
{{ shop.types }}                    <!-- Array of product types -->
{{ shop.vendors }}                  <!-- Array of vendors -->
```

#### Payment
```liquid
{{ shop.enabled_payment_types }}    <!-- Array of payment methods -->
```

#### Metafields
```liquid
{{ shop.metafields }}               <!-- Shop metafields -->
```

#### Locale
```liquid
{{ shop.locale }}                   <!-- Current locale (en, fr, etc.) -->
```

#### Password Page
```liquid
{{ shop.password_message }}         <!-- Password page message -->
```

---

## Page Objects

### `page` Object
Static page data.

```liquid
{{ page.id }}                       <!-- Page ID -->
{{ page.title }}                    <!-- Page title -->
{{ page.content }}                  <!-- Page content -->
{{ page.handle }}                   <!-- URL handle -->
{{ page.url }}                      <!-- Page URL -->
{{ page.author }}                   <!-- Page author -->
{{ page.template_suffix }}          <!-- Custom template suffix -->
{{ page.published_at }}             <!-- Publication date -->
```

---

## Navigation Objects

### `linklist` Object
Menu/navigation data.

```liquid
{{ linklist.id }}                   <!-- Menu ID -->
{{ linklist.title }}                <!-- Menu title -->
{{ linklist.handle }}               <!-- Menu handle -->
{{ linklist.links }}                <!-- Array of link objects -->
```

### `link` Object
Individual menu link data.

```liquid
{{ link.title }}                    <!-- Link text -->
{{ link.url }}                      <!-- Link URL -->
{{ link.type }}                     <!-- Link type -->
{{ link.object }}                   <!-- Linked object -->
{{ link.active }}                   <!-- true/false if current page -->
```

#### Link Types
- `collection_link` - Links to collection
- `product_link` - Links to product
- `page_link` - Links to page
- `blog_link` - Links to blog
- `relative_link` - Links to home, search, etc.
- `http_link` - External links

---

## Search Objects

### `search` Object
Search results data.

```liquid
{{ search.performed }}              <!-- true/false if search performed -->
{{ search.results }}                <!-- Array of search results -->
{{ search.results_count }}          <!-- Number of results -->
{{ search.terms }}                  <!-- Search query -->
```

---

## Template & Theme Objects

### `template` Object
Current template information.

```liquid
{{ template.name }}                 <!-- Template name -->
{{ template.suffix }}               <!-- Template suffix -->
```

### `theme` Object
Current theme information.

```liquid
{{ theme.id }}                      <!-- Theme ID -->
{{ theme.name }}                    <!-- Theme name -->
```

---

## Request Objects

### `request` Object
Current request information.

```liquid
{{ request.host }}                  <!-- Current hostname -->
{{ request.origin }}                <!-- Origin URL -->
{{ request.path }}                  <!-- URL path -->
{{ request.page_type }}             <!-- Page type -->
{{ request.design_mode }}           <!-- true/false in theme editor -->
{{ request.visual_preview_mode }}   <!-- true/false in visual preview -->
```

---

## Loop Objects

### `forloop` Object
Available in `{% for %}` loops.

```liquid
{% for item in collection.products %}
  {{ forloop.first }}               <!-- true/false if first iteration -->
  {{ forloop.last }}                <!-- true/false if last iteration -->
  {{ forloop.index }}               <!-- Current index (1-based) -->
  {{ forloop.index0 }}              <!-- Current index (0-based) -->
  {{ forloop.rindex }}              <!-- Reverse index (1-based) -->
  {{ forloop.rindex0 }}             <!-- Reverse index (0-based) -->
  {{ forloop.length }}              <!-- Total loop iterations -->
{% endfor %}
```

### `tablerow` Object
Available in `{% tablerow %}` loops.

```liquid
{% tablerow product in collection.products %}
  {{ tablerow.first }}              <!-- true/false if first in row -->
  {{ tablerow.last }}               <!-- true/false if last in row -->
  {{ tablerow.index }}              <!-- Current index (1-based) -->
  {{ tablerow.index0 }}             <!-- Current index (0-based) -->
  {{ tablerow.rindex }}             <!-- Reverse index (1-based) -->
  {{ tablerow.rindex0 }}            <!-- Reverse index (0-based) -->
  {{ tablerow.length }}             <!-- Total iterations -->
  {{ tablerow.col }}                <!-- Current column (1-based) -->
  {{ tablerow.col0 }}               <!-- Current column (0-based) -->
  {{ tablerow.col_first }}          <!-- true/false if first column -->
  {{ tablerow.col_last }}           <!-- true/false if last column -->
{% endtablerow %}
```

---

## Order Objects (Email Templates)

### `order` Object
Order data for email templates.

#### Basic Properties
```liquid
{{ order.id }}                      <!-- Order ID -->
{{ order.name }}                    <!-- Order name (#1001) -->
{{ order.order_number }}            <!-- Order number (1001) -->
{{ order.email }}                   <!-- Customer email -->
{{ order.phone }}                   <!-- Customer phone -->
```

#### Dates
```liquid
{{ order.created_at }}              <!-- Order creation date -->
{{ order.cancelled_at }}            <!-- Cancellation date -->
```

#### Status
```liquid
{{ order.cancelled }}               <!-- true/false if cancelled -->
{{ order.cancel_reason }}           <!-- Cancellation reason -->
{{ order.cancel_reason_label }}     <!-- Translated cancel reason -->
{{ order.financial_status }}        <!-- Payment status -->
{{ order.financial_status_label }}  <!-- Translated payment status -->
{{ order.fulfillment_status }}      <!-- Shipping status -->
{{ order.fulfillment_status_label }} <!-- Translated shipping status -->
```

#### Customer
```liquid
{{ order.customer }}                <!-- Customer object -->
{{ order.customer_url }}            <!-- Customer account URL -->
```

#### Addresses
```liquid
{{ order.billing_address }}         <!-- Billing address -->
{{ order.shipping_address }}        <!-- Shipping address -->
```

#### Items
```liquid
{{ order.line_items }}              <!-- Array of line items -->
```

#### Pricing
```liquid
{{ order.subtotal_price }}          <!-- Subtotal -->
{{ order.tax_price }}               <!-- Tax amount -->
{{ order.shipping_price }}          <!-- Shipping cost -->
{{ order.total_price }}             <!-- Total amount -->
```

#### Discounts
```liquid
{{ order.discounts }}               <!-- Array of discounts -->
```

#### Shipping
```liquid
{{ order.shipping_methods }}        <!-- Array of shipping methods -->
```

#### Tax
```liquid
{{ order.tax_lines }}               <!-- Array of tax lines -->
```

#### Transactions
```liquid
{{ order.transactions }}            <!-- Array of transactions -->
```

#### Notes
```liquid
{{ order.note }}                    <!-- Order note -->
```

#### Tags
```liquid
{{ order.tags }}                    <!-- Order tags -->
```

#### Location
```liquid
{{ order.location }}                <!-- Physical location (POS) -->
```

#### URLs
```liquid
{{ order.order_status_url }}        <!-- Order status page URL -->
```

---

## Utility Objects

### `paginate` Object
Pagination data.

```liquid
{% paginate collection.products by 12 %}
  {{ paginate.current_page }}       <!-- Current page number -->
  {{ paginate.current_offset }}     <!-- Current offset -->
  {{ paginate.items }}              <!-- Total items -->
  {{ paginate.parts }}              <!-- Page parts array -->
  {{ paginate.pages }}              <!-- Total pages -->
  {{ paginate.next }}               <!-- Next page info -->
  {{ paginate.previous }}           <!-- Previous page info -->
{% endpaginate %}
```

### `country_option_tags`
Generates country select options.

```liquid
<select name="country">
  {{ country_option_tags }}
</select>
```

---

## Quick Reference by Use Case

### Product Display
```liquid
{{ product.title }}
{{ product.price | money }}
{{ product.featured_image | image_url: width: 600 }}
{{ product.url }}
```

### Collection Loop
```liquid
{% for product in collection.products %}
  {{ product.title }}
  {{ product.price | money }}
{% endfor %}
```

### Cart Items
```liquid
{% for item in cart.items %}
  {{ item.title }}
  {{ item.quantity }}
  {{ item.line_price | money }}
{% endfor %}
```

### Customer Info
```liquid
{% if customer %}
  Welcome, {{ customer.first_name }}!
  Orders: {{ customer.orders_count }}
{% endif %}
```

### Section Settings
```liquid
{{ section.settings.heading }}
{{ section.settings.description }}
{% if section.settings.show_button %}
  <a href="{{ section.settings.button_url }}">
    {{ section.settings.button_text }}
  </a>
{% endif %}
```

---

This reference covers the most commonly used objects in Shopify Liquid. For the complete list of all objects and properties, refer to the [official Shopify Liquid documentation](https://shopify.dev/docs/api/liquid/objects).
