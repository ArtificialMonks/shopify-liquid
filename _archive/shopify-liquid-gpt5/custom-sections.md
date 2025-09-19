# Building Custom Sections (2024–2025)

A section is a Liquid file in `sections/` that renders markup and exposes settings (and optional blocks) to the theme editor via a single `{% schema %}` JSON block.

Create a section
1) Add `sections/your-section.liquid`
2) Output HTML/Liquid
3) Append one `{% schema %}` (valid JSON only)

Minimal working example

```liquid
<section class="text-banner">
  <h2>{{ section.settings.heading | escape }}</h2>
  {% if section.settings.subtext != blank %}
    <p>{{ section.settings.subtext }}</p>
  {% endif %}
</section>
{% schema %}{
  "name": "Text banner",
  "settings": [
    {"type":"text","id":"heading","label":"Heading","default":"Welcome"},
    {"type":"richtext","id":"subtext","label":"Subtext"}
  ],
  "presets": [{"name":"Text banner"}]
}{% endschema %}
```

Blocks
- Use `blocks` when content is repeatable (testimonials, slides, logos)
- Each block has a `type`, `name`, and its own `settings`

Snippet (with blocks)

```liquid
<section class="logos" aria-label="Brand logos">
  <ul class="logos__list">
    {% for block in section.blocks %}
      <li class="logos__item" {{ block.shopify_attributes }}>
        {% if block.settings.image %}
          <img src="{{ block.settings.image | image_url: width: 240 }}" alt="{{ block.settings.alt | escape }}" loading="lazy">
        {% endif %}
      </li>
    {% endfor %}
  </ul>
</section>
{% schema %}{
  "name": "Logo list",
  "max_blocks": 12,
  "settings": [],
  "blocks": [
    {
      "type": "logo",
      "name": "Logo",
      "settings": [
        {"type":"image_picker","id":"image","label":"Image"},
        {"type":"text","id":"alt","label":"Alt text"}
      ]
    }
  ],
  "presets": [{"name":"Logo list","blocks":[{"type":"logo"},{"type":"logo"}]}]
}{% endschema %}
```

Availability (enabled_on / disabled_on)
- Control where a section can be added or is hidden by default

```liquid
{% schema %}{
  "name": "Promo banner",
  "settings": [ {"type":"text","id":"title","label":"Title"} ],
  "presets": [{"name":"Promo banner"}],
  "enabled_on": {"templates": ["*"]},
  "disabled_on": {"groups": ["footer"], "templates": ["cart"]}
}{% endschema %}
```

Add to a template (JSON)
- In `templates/page.about.json` (example), add your section to the `sections` object and to `order`

```json
{
  "sections": {
    "main": {"type": "main-page"},
    "promo": {"type": "promo-banner"}
  },
  "order": ["main","promo"]
}
```

Section groups (header/footer)
- Use `header-group.json` / `footer-group.json` in `sections/` to manage header/footer composition
- Reference groups in `layout/theme.liquid`

Key rules
- One `{% schema %}` per section; valid JSON only; don’t nest in tags
- Keep blocks 50 and per section limit 25 within groups/templates to avoid editor/UX issues
- Always escape user text in output; guard optional settings


More examples (see code-snippets/)
- hero-richtext-cta.liquid — Rich-text hero with CTA
- product-grid-paginate.liquid — Product grid with pagination
- testimonial-carousel.liquid — Accessible testimonial carousel


References
- Section schema: https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
- Sections & blocks best practices: https://shopify.dev/docs/storefronts/themes/best-practices/templates-sections-blocks

