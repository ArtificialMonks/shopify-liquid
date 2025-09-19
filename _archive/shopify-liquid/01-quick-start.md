# Quick Start Guide: Creating Your First Custom Liquid Section

Let's build a custom Shopify section from scratch in 6 simple steps. Think of this like creating a **smart content block** that merchants can configure through the theme editor.

## What We're Building

We'll create an **"Image with Text"** section that allows merchants to:
- Upload an image
- Add a headline and description
- Configure layout and styling
- Enable/disable the section

Here's what the final section will look like in the theme editor:

![Custom Section Preview](https://via.placeholder.com/600x300/2563eb/ffffff?text=Image+with+Text+Section)

---

## Step 1: Access Your Theme Code

In your Shopify admin:

1. Go to **Online Store** → **Themes**
2. Find your active theme and click **Actions** → **Edit code**
3. Locate the **`sections/`** folder in the file tree

💡 **Think of it like this**: The `sections` folder is your **toolbox** where you store all your custom building blocks.

---

## Step 2: Create Your Section File

1. In the `sections` folder, click **Add a new section**
2. Name it `image-with-text.liquid`
3. Click **Create section**

🎯 **Naming Convention**: Use lowercase with hyphens. The filename becomes the section's ID.

---

## Step 3: Add the Basic Structure

Paste this foundation code into your new file:

```liquid
<!-- Image with Text Section HTML -->
<div class="image-with-text-section" id="section-{{ section.id }}">
  {% if section.settings.show_section %}
    <div class="container">
      <div class="content-wrapper">
        
        <!-- Image Block -->
        {% if section.settings.image %}
          <div class="image-block">
            <img 
              src="{{ section.settings.image | image_url: width: 600 }}" 
              alt="{{ section.settings.image.alt | escape }}"
              loading="lazy"
            >
          </div>
        {% endif %}
        
        <!-- Text Block -->
        <div class="text-block">
          {% if section.settings.heading %}
            <h2>{{ section.settings.heading | escape }}</h2>
          {% endif %}
          
          {% if section.settings.description %}
            <div class="description">
              {{ section.settings.description }}
            </div>
          {% endif %}
          
          {% if section.settings.button_text and section.settings.button_url %}
            <a href="{{ section.settings.button_url }}" class="btn">
              {{ section.settings.button_text | escape }}
            </a>
          {% endif %}
        </div>
        
      </div>
    </div>
  {% endif %}
</div>

<!-- Basic Styling -->
<style>
  .image-with-text-section {
    padding: 40px 0;
  }
  .content-wrapper {
    display: flex;
    align-items: center;
    gap: 40px;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  .image-block, .text-block {
    flex: 1;
  }
  .image-block img {
    width: 100%;
    height: auto;
    border-radius: 8px;
  }
  .text-block h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }
  .description {
    margin-bottom: 1.5rem;
    line-height: 1.6;
  }
  .btn {
    display: inline-block;
    padding: 12px 24px;
    background: #007cba;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background 0.3s;
  }
  .btn:hover {
    background: #005a8b;
  }
  
  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .content-wrapper {
      flex-direction: column;
      text-align: center;
    }
  }
</style>
```

💡 **What's happening here**: We're creating a flexible container that shows an image next to text, with responsive design built-in.

---

## Step 4: Add the Configuration Schema

Now add the **schema** - this is the **blueprint** that creates the settings in the theme editor. Add this at the very end of your file:

```liquid
{% schema %}
{
  "name": "Image with Text",
  "tag": "section",
  "class": "image-text-section",
  "settings": [
    {
      "type": "checkbox",
      "id": "show_section",
      "label": "Show this section",
      "default": true
    },
    {
      "type": "header",
      "content": "Image Settings"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Choose Image"
    },
    {
      "type": "header",
      "content": "Text Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Headline",
      "default": "Tell Your Story"
    },
    {
      "type": "richtext",
      "id": "description", 
      "label": "Description",
      "default": "<p>Use this section to describe your company or share your brand story.</p>"
    },
    {
      "type": "header",
      "content": "Button Settings"
    },
    {
      "type": "text",
      "id": "button_text",
      "label": "Button Text",
      "default": "Learn More"
    },
    {
      "type": "url",
      "id": "button_url",
      "label": "Button Link"
    }
  ],
  "presets": [
    {
      "name": "Image with Text",
      "category": "Custom"
    }
  ]
}
{% endschema %}
```

🎯 **Schema Breakdown**:
- **`name`**: What merchants see in the editor
- **`settings`**: All the options merchants can configure
- **`presets`**: Default setup when first added

---

## Step 5: Test Your Section

1. **Save** your section file
2. Go to your store's **theme editor** (Customize theme)
3. Click **Add section**
4. Look for **"Image with Text"** in the Custom category
5. Click to add it to your page

You should see:
- ✅ Image upload field
- ✅ Text input fields  
- ✅ Button configuration
- ✅ Show/hide toggle

---

## Step 6: Configure and Preview

Now test your section:

1. **Upload an image** using the image picker
2. **Change the headline** to something like "Welcome to Our Store"
3. **Add description text** about your business
4. **Set button text** and link
5. **Preview** your changes

🎉 **Congratulations!** You've just built your first custom Shopify section!

---

## What You Just Built

Here's what makes this section **powerful**:

```liquid
<!-- Smart Image Handling -->
{{ section.settings.image | image_url: width: 600 }}
<!-- Automatically resizes and optimizes images -->

<!-- Safe Text Output -->
{{ section.settings.heading | escape }}
<!-- Prevents XSS attacks by escaping HTML -->

<!-- Conditional Display -->
{% if section.settings.show_section %}
<!-- Only shows content when enabled -->

<!-- Rich Text Support -->
{{ section.settings.description }}
<!-- Allows merchants to add formatted text -->
```

---

## Next Steps

Now that you have a working section, you can:

1. **Add more settings** - colors, fonts, layout options
2. **Create blocks** - for repeatable content like testimonials
3. **Improve styling** - match your theme's design system
4. **Add JavaScript** - for interactive features
5. **Optimize performance** - lazy loading, image optimization

🚀 **Ready for more?** Check out [Section Schema Deep Dive](./02-section-schema.md) to understand all the configuration options available.

---

## Troubleshooting

**Section not appearing in editor?**
- Check that your schema is valid JSON
- Make sure you have a `presets` array
- Verify the file is saved in the `sections/` folder

**Settings not working?**
- Ensure setting `id` values match your Liquid code
- Check for typos in `section.settings.your_id`
- Verify the section is enabled (`show_section: true`)

**Styling issues?**
- Check CSS syntax in your `<style>` block
- Test on mobile devices for responsive design
- Validate HTML structure

Need help? Jump to our [Troubleshooting Guide](./09-troubleshooting.md) for more solutions!
