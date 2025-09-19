# Shopify Liquid Custom Sections – Practical Guide (2024–2025)

This guide is a concise, copy‑paste‑ready reference for building custom Shopify Liquid sections that work in production themes. It is organized for fast use and verified against current Liquid and themes docs.

Contents


- fundamentals.md – Liquid language essentials
- custom-sections.md – How to build sections and blocks
- blocks.md – Building custom blocks (scoped CSS pattern)
- schema-examples.md – Ready schema patterns (settings, blocks, presets, disabled_on)
- best-practices.md – Performance, accessibility, responsive patterns, pitfalls
- code-snippets/ – Reusable, paste‑ready snippets referenced throughout

Highlighted code snippets

- blocks-js-enhancements.md — Minimal JS patterns for toggles/carousels (editor-aware)
- ella-shopify/ — Scraped docs & notes to align with ELLA theme


- code-snippets/hero-richtext-cta.liquid — Rich-text hero with CTA
- code-snippets/product-grid-paginate.liquid — Product grid with pagination
- code-snippets/testimonial-carousel.liquid — Accessible testimonial carousel


Primary sources (selected)


- Shopify Liquid reference: https://shopify.dev/docs/api/liquid
- Liquid (OSS): https://shopify.github.io/liquid/
- Section schema + best practices (themes): https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
- Building with sections & blocks: https://shopify.dev/docs/storefronts/themes/best-practices/templates-sections-blocks
- Shopify/liquid (source): https://github.com/Shopify/liquid
- Shopify liquid docs code samples: https://github.com/Shopify/liquid-docs-code-samples
- Cheatsheet (community): https://gist.github.com/liqtags/d9fd9fabe8bfc67cb4fca98d045d8190

Quick start
1) Create a section in sections/<your-section>.liquid
2) Output HTML + Liquid; add a single {% schema %} JSON block
3) Define settings, optional blocks, presets
4) Control availability with enabled_on / disabled_on
5) Add the section to a template (JSON) or to a section group (header/footer)

Copy‑paste minimal section (full file under code-snippets/section-minimal.liquid)

```liquid
{% comment %} sections/hero-banner.liquid {% endcomment %}
<section class="hero">
  <h2>{{ section.settings.heading | escape }}</h2>
</section>
{% schema %}{
  "name": "Hero banner",
  "settings": [
    {"type":"text","id":"heading","label":"Heading","default":"Welcome"}
  ],
  "presets": [{"name":"Hero banner"}]
}{% endschema %}
```

Notes
- Schema must be valid JSON. Liquid inside {% schema %} is ignored and not rendered.
- One {% schema %} per section. Don’t nest it in other tags.
- Use blocks for repeatable content; keep max_blocks sensible (≤ 50).
- Prefer JSON templates + section groups over static sections in layouts.

