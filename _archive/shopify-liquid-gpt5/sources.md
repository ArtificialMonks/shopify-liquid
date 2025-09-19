# Sources & Extracts (Verbatim where useful)

Official docs
1) Liquid reference (Shopify): https://shopify.dev/docs/api/liquid
> "Liquid is used to dynamically output objects and their properties. You can further modify that output by creating logic with tags, or directly altering it with a filter."

2) Liquid (OSS): https://shopify.github.io/liquid/
> "Liquid is an open-source template language created by Shopify. It is the backbone of Shopify themes and is used to load dynamic content on storefronts."

3) Section schema: https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
> Attributes include: name, tag, class, limit, settings, blocks, max_blocks, presets, default, locales, enabled_on, disabled_on.

4) Sections & blocks best practices: https://shopify.dev/docs/storefronts/themes/best-practices/templates-sections-blocks
> "When building theme templates, ensure default content is available in a main template section, and that sections can be added, removed, and reordered."

5) Section groups (header/footer): https://shopify.dev/docs/storefronts/themes/architecture/section-groups
> "A section group is a JSON data file that stores a list of sections and app blocks to be rendered, and their associated settings."

Code samples repository
- Shopify/liquid-docs-code-samples: https://github.com/Shopify/liquid-docs-code-samples (sections/, blocks/, templates/ examples)

Community reference
- Shopify Liquid Cheatsheet (community gist): https://gist.github.com/liqtags/d9fd9fabe8bfc67cb4fca98d045d8190

Context7 (Shopify Theme Liquid Docs)
- Theme Liquid Docs (auto-generated guidance on CSS/UX/JS for themes): https://github.com/shopify/theme-liquid-docs
> CSS Specificity: "Never use IDs as selectors; avoid element selectors; avoid !important; use single-class selectors where possible."
> CSS Scoping: "Use stylesheet tags in sections/blocks/snippets; reset CSS variables inline for settings."

Blog reference used for onboarding context
- Instant: Custom Liquid Shopify (how to add a custom section): https://instant.so/blog/custom-liquid-shopify (step-by-step walkthrough)

Notes
- This doc lists primary links and select quotes used to triangulate the guidance in this folder. For canonical behavior, prefer shopify.dev pages.

