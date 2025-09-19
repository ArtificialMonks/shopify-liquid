# Best Practices: Sections, Schema, Performance, A11y

General principles (Theme Liquid docs)
- SSR first: render storefront with Liquid; use JS sparingly for interactions
- Keep sections self-contained; blocks for repeatable subcontent
- Prefer JSON templates and section groups (header/footer) over static sections in layouts

Performance
- Limit list sizes; use `paginate` for >50 items
- Avoid heavy globals (e.g., massive loops on `all_products`) on templates
- Images: always request sized variants (`image_url` with `width`), provide `srcset` + `sizes`, `loading="lazy"`
- CSS/JS scoping: use section-scoped style/script tags; avoid global leakage and ID selectors
- Keep Liquid logic simple; precompute with `assign` / `capture` where helpful

Accessibility (WCAG 2.1 AA)
- Headings in logical order; one `h1` per page, sections typically start from `h2`
- Alt text: `{{ image.alt | default: section.settings.heading | escape }}` for informative images
- Color contrast: follow tokens/color schemes; avoid hardcoded colors
- Keyboard support: focusable controls, visible focus ring, no keyboard traps
- ARIA: only when necessary; native semantics first; landmark roles for complex sections (e.g., `role="region"` with accessible name)

Responsive design
- Mobile-first CSS (min-width queries)
- Fluid containers; avoid fixed heights; use intrinsic image sizes
- Use `sizes` tailored to layout; don’t overserve images

Schema & Editor UX
- Clear labels, helpful `info`, and useful defaults
- Blocks: keep to practical limits (≤50) and provide sensible `max_blocks`
- Use `enabled_on`/`disabled_on` to constrain placement (e.g., disable in cart)
- Group related settings and avoid deep conditional setting trees (≤2 levels)

Common pitfalls to avoid
- Invalid JSON in `{% schema %}` (breaks editor)
- Multiple `{% schema %}` tags or nesting schema inside other tags
- Unescaped user content; always `| escape` for headings/text
- Global CSS collisions; avoid IDs and !important
- Missing guards for optional settings (nil checks)

Verification
- Run Theme Check (VS Code extension / CLI)
- Test in theme editor: add/remove section, reordering blocks, check defaults
- Throttle network to validate lazy-loading and image size choices

Key references
- Liquid reference: https://shopify.dev/docs/api/liquid
- Section schema: https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema
- Sections & blocks best practices: https://shopify.dev/docs/storefronts/themes/best-practices/templates-sections-blocks

