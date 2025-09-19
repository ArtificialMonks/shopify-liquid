# ELLA Theme – Implementation Notes (from scraped docs)

This file distills implementation-relevant details. Where class names are required, inspect your installed ELLA theme CSS and map our BEM classes to ELLA utilities/tokens. We avoid guessing internal class names.

Key takeaways
- Versioning: Ella 6.x is current; releases are frequent (see Changelog in docs). When updating, theme code is a new copy; customizations must be reapplied (general Shopify rule echoed by Ella docs).
- Presets: Docs provide JSON presets (index.json, settings_data.json, header-group.json, footer-group.json). This indicates ELLA relies on section groups for header/footer and rich JSON templates.
- Section widths: Many sections offer width presets (body default, 1170px, 1770px, full width) and padding controls—plan for container logic when aligning our blocks.
- Product variants: Color swatches support several sources (default named colors, PNG assets by naming convention, metafields, metaobjects). For stores using ELLA, prefer metafields/metaobjects for robust color chips.
- Quick cart & popular products: ELLA exposes settings for sidebar cart UI (colors, borders) and an optional popular products carousel. If we integrate with their cart UI, respect their toggles and data flow.

How to align our blocks
1) Keep our scoped CSS suffix intact
- Our `-{{ unique }}` suffix guarantees isolation; keep it even when mapping classes.

2) Map structural wrappers to ELLA containers
- Our examples use generic `.container` or simple wrappers. In ELLA, use their width controls or wrapper utilities that correspond to “Default / 1170 / 1770 / Full”.

3) Buttons & links
- Replace `.btn .btn--primary` with ELLA’s preferred button tokens. Keep aria-labels and semantic `<button>`/`<a>`.

4) Grids & spacing
- ELLA offers section padding and grid options via settings. If embedding blocks in sections, prefer section-level spacing controls and keep block defaults conservative.

5) Media & images
- Use `image_url` with responsive widths and `loading="lazy"`. Ensure aspect-ratio placeholders to avoid CLS, compatible with ELLA’s layout controls.

6) Carousels
- ELLA ships a variety of sliders; if you must keep a custom, keep it minimal and opt-out (reduced motion). Otherwise, prefer ELLA’s built-in slider sections/blocks.

Where to confirm specifics
- Inspect your theme’s assets (CSS/JS) for:
  - Container utilities
  - Button classes
  - Grid helpers
  - Any data-attributes used by ELLA JS
- Cross-reference with the official GitBook pages above.

