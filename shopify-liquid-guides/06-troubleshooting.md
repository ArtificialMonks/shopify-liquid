# Troubleshooting

Common issues, solutions, and debugging techniques for Shopify Liquid development. Quick fixes for the problems you'll encounter most often.

## Schema Issues

### Section Not Appearing in Theme Editor

**Problem**: Section file exists but doesn't show up in "Add section" menu.

**Common Causes & Solutions**:

```liquid
<!-- ❌ BAD: Invalid JSON syntax -->
{% schema %}
{
  "name": "My Section",
  "settings": [
    {"type": "text", "id": "title", "label": "Title",}  // Trailing comma!
  ]
}
{% endschema %}

<!-- ✅ GOOD: Valid JSON -->
{% schema %}
{
  "name": "My Section",
  "settings": [
    {"type": "text", "id": "title", "label": "Title"}
  ]
}
{% endschema %}
```

**Debug Steps**:
1. Validate JSON at [jsonlint.com](https://jsonlint.com)
2. Check file is in correct `sections/` folder
3. Ensure filename has `.liquid` extension
4. Refresh theme editor (Ctrl+F5 / Cmd+Shift+R)
5. Check for Liquid syntax errors in template

### Settings Not Working

**Problem**: Section settings don't affect output or cause errors.

**Common Issues**:

```liquid
<!-- ❌ BAD: Mismatched setting ID -->
{% schema %}
{"settings": [{"type": "text", "id": "heading", "label": "Heading"}]}
{% endschema %}

<!-- Using wrong variable name -->
<h2>{{ section.settings.title }}</h2>  <!-- Should be 'heading' -->

<!-- ✅ GOOD: Matching IDs -->
{% schema %}
{"settings": [{"type": "text", "id": "heading", "label": "Heading"}]}
{% endschema %}

<h2>{{ section.settings.heading | escape }}</h2>
```

**Debug Checklist**:
- ✅ Setting `id` matches Liquid variable exactly
- ✅ No typos in setting names
- ✅ Correct data type (text, color, range, etc.)
- ✅ Valid default values
- ✅ Proper escaping with `| escape` filter

### Block Issues

**Problem**: Blocks don't display or theme editor breaks.

```liquid
<!-- ❌ BAD: Missing shopify_attributes -->
{% for block in section.blocks %}
  <div class="block">
    {{ block.settings.content }}
  </div>
{% endfor %}

<!-- ✅ GOOD: Include shopify_attributes -->
{% for block in section.blocks %}
  <div class="block" {{ block.shopify_attributes }}>
    {{ block.settings.content }}
  </div>
{% endfor %}
```

**Required for Blocks**:
- ✅ `{{ block.shopify_attributes }}` on root element
- ✅ Block `type` matches case statement
- ✅ `max_blocks` set to reasonable limit
- ✅ Valid block schema structure

## Liquid Template Errors

### Object Does Not Exist

**Problem**: `Liquid error: undefined method` or empty output.

```liquid
<!-- ❌ BAD: Assuming object exists -->
{{ product.featured_image.alt }}

<!-- ✅ GOOD: Check existence first -->
{% if product.featured_image %}
  {{ product.featured_image.alt | escape }}
{% endif %}
```

**Safe Access Patterns**:
```liquid
<!-- Guard with if statements -->
{% if section.settings.title != blank %}
  <h2>{{ section.settings.title | escape }}</h2>
{% endif %}

<!-- Use default filter -->
{{ section.settings.title | default: 'Default Title' | escape }}

<!-- Chain with assign for complex checks -->
{% assign image_alt = product.featured_image.alt | default: product.title %}
<img alt="{{ image_alt | escape }}">
```

### Filter Errors

**Problem**: `Liquid error: wrong number of arguments` or unexpected output.

```liquid
<!-- ❌ BAD: Incorrect filter usage -->
{{ product.price | money: 'USD' }}  <!-- money filter takes no arguments -->
{{ product.title | truncate }}     <!-- truncate requires length argument -->

<!-- ✅ GOOD: Correct filter syntax -->
{{ product.price | money }}
{{ product.title | truncate: 50 }}
{{ image | image_url: width: 400 }}
```

**Common Filter Issues**:
- `money` filter: Takes no arguments, formats based on shop currency
- `truncate` filter: Requires length parameter
- `image_url` filter: Use `width:` or `height:` parameters
- `date` filter: Requires format string

### Loop Performance Issues

**Problem**: Page loads slowly or times out.

```liquid
<!-- ❌ BAD: Expensive nested loops -->
{% for product in collections.all.products %}
  {% for variant in product.variants %}
    {% for collection in collections %}
      {% if collection.products contains product %}
        <!-- Very expensive operation -->
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endfor %}

<!-- ✅ GOOD: Targeted, limited queries -->
{% for product in collections.featured.products limit: 8 %}
  {% if product.available %}
    <!-- Process only available featured products -->
  {% endif %}
{% endfor %}
```

**Performance Optimization**:
- Use specific collections instead of `collections.all`
- Add `limit:` to prevent excessive processing
- Avoid nested loops when possible
- Use `assign` to cache complex calculations

## CSS Issues

### Styles Not Applying

**Problem**: CSS appears correct but doesn't affect elements.

**Common Causes**:

```liquid
<!-- ❌ BAD: CSS outside style tags -->
.my-section { background: red; }

<section class="my-section">Content</section>

<!-- ✅ GOOD: CSS inside style tags -->
<style>
  .my-section { background: red; }
</style>

<section class="my-section">Content</section>
```

**Debug Steps**:
1. Check CSS is inside `<style>` tags
2. Verify class names match exactly (case-sensitive)
3. Inspect element in browser dev tools
4. Check for CSS specificity conflicts
5. Validate CSS syntax

### CSS Conflicts

**Problem**: Styles affect other sections unintentionally.

```liquid
<!-- ❌ BAD: Generic class names -->
<style>
  .button { background: blue; }  <!-- Affects all buttons -->
  .card { padding: 20px; }       <!-- Affects all cards -->
</style>

<!-- ✅ GOOD: Scoped class names -->
<style>
  .hero-section-{{ section.id }} .button { background: blue; }
  .hero-section-{{ section.id }} .card { padding: 20px; }
</style>

<section class="hero-section-{{ section.id }}">
```

**CSS Scoping Best Practices**:
- Always scope CSS to section/block ID
- Use unique class prefixes
- Avoid `!important` declarations
- Test with multiple sections on same page

### Responsive Issues

**Problem**: Layout breaks on mobile/tablet devices.

```liquid
<!-- ❌ BAD: Fixed widths without responsive design -->
<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(4, 300px);  /* Fixed width */
  }
</style>

<!-- ✅ GOOD: Responsive grid -->
<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }

  @media (max-width: 749px) {
    .grid {
      grid-template-columns: 1fr;
      gap: 16px;
    }
  }
</style>
```

## Image Issues

### Images Not Loading

**Problem**: Broken image links or missing images.

```liquid
<!-- ❌ BAD: Not checking if image exists -->
<img src="{{ section.settings.image | image_url: width: 400 }}">

<!-- ✅ GOOD: Check existence and provide fallback -->
{% if section.settings.image %}
  <img src="{{ section.settings.image | image_url: width: 400 }}"
       alt="{{ section.settings.image.alt | escape }}"
       loading="lazy">
{% else %}
  {{ 'image' | placeholder_svg_tag: 'placeholder-image' }}
{% endif %}
```

### Image Sizing Issues

**Problem**: Images appear blurry or take too long to load.

```liquid
<!-- ❌ BAD: No size optimization -->
<img src="{{ product.featured_image }}">  <!-- Original size, could be huge -->

<!-- ✅ GOOD: Optimized responsive images -->
<img src="{{ product.featured_image | image_url: width: 800 }}"
     srcset="
       {{ product.featured_image | image_url: width: 400 }} 400w,
       {{ product.featured_image | image_url: width: 800 }} 800w,
       {{ product.featured_image | image_url: width: 1200 }} 1200w
     "
     sizes="(min-width: 750px) 400px, 100vw"
     alt="{{ product.title | escape }}"
     loading="lazy">
```

### Layout Shift Issues

**Problem**: Page content jumps when images load.

```liquid
<!-- ❌ BAD: No dimensions specified -->
<img src="{{ image | image_url: width: 400 }}" alt="Product">

<!-- ✅ GOOD: Prevent layout shift -->
<div style="aspect-ratio: {{ image.width }}/{{ image.height }};">
  <img src="{{ image | image_url: width: 400 }}"
       alt="{{ product.title | escape }}"
       style="width: 100%; height: 100%; object-fit: cover;"
       loading="lazy">
</div>
```

## Theme Editor Issues

### Section Settings Not Updating

**Problem**: Changes in theme editor don't reflect on page.

**Debug Steps**:
1. Check browser cache (hard refresh: Ctrl+Shift+R)
2. Verify setting is being used in template
3. Check for conditional logic hiding content
4. Ensure proper escaping doesn't interfere
5. Test in incognito/private browsing mode

```liquid
<!-- ❌ BAD: Setting exists but not used -->
{% schema %}
{"settings": [{"type": "color", "id": "bg_color", "label": "Background"}]}
{% endschema %}

<!-- Missing implementation -->
<section class="hero">Content</section>

<!-- ✅ GOOD: Setting properly implemented -->
{% schema %}
{"settings": [{"type": "color", "id": "bg_color", "label": "Background"}]}
{% endschema %}

<style>
  .hero-{{ section.id }} {
    background: {{ section.settings.bg_color | default: '#ffffff' }};
  }
</style>

<section class="hero-{{ section.id }}">Content</section>
```

### Block Reordering Not Working

**Problem**: Drag and drop in theme editor breaks or doesn't work.

**Common Issues**:
- Missing `{{ block.shopify_attributes }}`
- Block attributes on wrong element
- JavaScript interfering with editor

```liquid
<!-- ❌ BAD: Missing block attributes -->
<div class="testimonial">
  <p>{{ block.settings.quote | escape }}</p>
</div>

<!-- ✅ GOOD: Block attributes on root element -->
<div class="testimonial" {{ block.shopify_attributes }}>
  <p>{{ block.settings.quote | escape }}</p>
</div>
```

## Performance Issues

### Slow Page Loading

**Problem**: Pages take too long to load.

**Diagnosis Steps**:
1. Run Lighthouse audit in Chrome DevTools
2. Check Network tab for slow requests
3. Look for large images or excessive Liquid loops
4. Test with throttled connection

**Common Fixes**:
```liquid
<!-- ❌ BAD: Loading all products unnecessarily -->
{% for product in collections.all.products %}
  <!-- Processes potentially thousands of products -->
{% endfor %}

<!-- ✅ GOOD: Limit and target specific collections -->
{% for product in collections.featured.products limit: 8 %}
  <!-- Only processes 8 products -->
{% endfor %}

<!-- ✅ Use pagination for large collections -->
{% paginate collection.products by 24 %}
  {% for product in collection.products %}
    <!-- Process paginated products -->
  {% endfor %}
  {{ paginate | default_pagination }}
{% endpaginate %}
```

### Memory Issues

**Problem**: Theme editor becomes unresponsive or crashes.

**Common Causes**:
- Too many blocks (>50)
- Complex CSS with many dynamic properties
- Large images without optimization
- Infinite loops in Liquid logic

```liquid
<!-- ❌ BAD: Unlimited blocks -->
{% schema %}
{
  "blocks": [...]
  // No max_blocks limit
}
{% endschema %}

<!-- ✅ GOOD: Reasonable block limits -->
{% schema %}
{
  "blocks": [...],
  "max_blocks": 12
}
{% endschema %}
```

## JavaScript Issues

### Script Errors

**Problem**: JavaScript console shows errors.

```liquid
<!-- ❌ BAD: Not checking if elements exist -->
{% javascript %}
document.querySelector('.my-button').addEventListener('click', function() {
  // Error if .my-button doesn't exist
});
{% endjavascript %}

<!-- ✅ GOOD: Check elements exist -->
{% javascript %}
document.addEventListener('DOMContentLoaded', function() {
  const button = document.querySelector('.my-button');
  if (button) {
    button.addEventListener('click', function() {
      // Safe to add event listener
    });
  }
});
{% endjavascript %}
```

### Theme Editor Conflicts

**Problem**: JavaScript breaks when editing in theme editor.

```liquid
<!-- ✅ Handle section reloads in theme editor -->
{% javascript %}
function initMySection() {
  const elements = document.querySelectorAll('.my-component');
  elements.forEach(element => {
    // Initialize component
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initMySection);

// Re-initialize when section reloads in theme editor
document.addEventListener('shopify:section:load', function(event) {
  if (event.detail.sectionId === '{{ section.id }}') {
    initMySection();
  }
});
{% endjavascript %}
```

## Debugging Tools

### Browser DevTools
- **Elements tab**: Inspect HTML structure and CSS
- **Console tab**: Check for JavaScript errors
- **Network tab**: Monitor loading performance
- **Lighthouse tab**: Performance and accessibility audits

### Liquid Debugging
```liquid
<!-- Output variable contents for debugging -->
{{ section.settings | json }}
{{ block | json }}
{{ product | json }}

<!-- Check variable types and values -->
{% assign debug_var = section.settings.title %}
{{ debug_var }} ({{ debug_var.size }} characters)

<!-- Conditional debugging -->
{% if section.settings.debug_mode %}
  <pre>{{ section | json }}</pre>
{% endif %}
```

### Theme Inspector (Shopify CLI)
```bash
# Install Shopify CLI
npm install -g @shopify/cli @shopify/theme

# Connect to your store
shopify theme dev

# Real-time debugging and hot reload
```

## Prevention Strategies

### Development Checklist
- ✅ Validate JSON schema before testing
- ✅ Test with empty/missing content
- ✅ Check multiple screen sizes
- ✅ Test in theme editor environment
- ✅ Validate HTML and CSS
- ✅ Run Lighthouse audits regularly

### Code Review Points
- ✅ All user input properly escaped
- ✅ Optional content properly guarded
- ✅ CSS properly scoped
- ✅ Images optimized and responsive
- ✅ JavaScript handles edge cases
- ✅ Accessibility requirements met

### Testing Scenarios
```liquid
<!-- Test these scenarios for every section -->
<!--
1. Empty content:
   - No settings configured
   - No blocks added
   - Missing images

2. Maximum content:
   - All settings filled
   - Maximum blocks
   - Very long text

3. Edge cases:
   - Special characters
   - Very short/long content
   - Missing resources

4. Responsive:
   - Mobile (320px)
   - Tablet (768px)
   - Desktop (1024px+)

5. Performance:
   - Slow network
   - Many sections on page
   - Large images
-->
```

## Getting Help

### Official Resources
- [Shopify Liquid Documentation](https://shopify.dev/docs/api/liquid)
- [Theme Development Tools](https://shopify.dev/docs/storefronts/themes/tools)
- [Community Forums](https://community.shopify.com/c/shopify-design/bd-p/shopify-design)

### Debugging Communities
- [Shopify Partners Slack](https://shopifypartners.slack.com)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/shopify)
- [GitHub Discussions](https://github.com/Shopify/liquid/discussions)

### Professional Support
- Shopify Partner Directory
- Theme development agencies
- Freelance Liquid developers

Remember: Most issues stem from simple syntax errors, missing content guards, or incorrect variable names. Start with the basics before diving into complex debugging.