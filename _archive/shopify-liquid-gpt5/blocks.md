# Building Custom Blocks with Scoped CSS (Production Pattern)

This guide documents a proven pattern for creating isolated, reusable blocks inside Shopify sections using instance‑scoped CSS derived from `block.id`. It aligns with the rest of this documentation set and is easy to adapt to the ELLA theme.

On this page
- Block architecture pattern
- Complete code template (copy/paste)
- Best practices (layout, empty states, a11y, performance, schema)
- Real‑world examples (2–3 blocks)

## Block architecture pattern

Goal: Build blocks that can be safely repeated in a section without style collisions, configurable via theme editor.

Key elements
1) Instance‑scoped CSS
- Compute a unique suffix from `block.id`.
- Append the suffix to every selector in the CSS and to the corresponding class names in the markup.

2) Dynamic CSS via `{% style %}`
- Author CSS in a `{% style %}` block and parameterize values from `block.settings`.
- Include responsive overrides with media queries in the same block.

3) Editor integration
- Add `{{ block.shopify_attributes }}` on the block’s root element for theme editor selection/drag.

4) Naming conventions (BEM + suffix)
- Use BEM for clarity: `block__element--modifier`.
- Add the unique suffix to the base and elements to avoid collisions: `feature__title-{{ unique }}`.

5) Schema placement
- Define blocks in the section’s `{% schema %}` → `blocks: []` with settings matching what your CSS/markup expects.

## Complete code template (copy/paste)

Paste inside your section where `block` is in scope (within `{% for block in section.blocks %}`).

```liquid
{% assign unique = block.id | replace: '_', '' | downcase %}

{% style %}
  .media-text-{{ unique }}{display:flex;gap:{{ block.settings.gap }}px;padding:{{ block.settings.pad }}px}
  .media-text__media-{{ unique }}{flex:1;border-radius:{{ block.settings.radius }}px;overflow:hidden}
  .media-text__text-{{ unique }}{flex:1;color:{{ block.settings.text_color }};font-size:{{ block.settings.text_size }}px;line-height:1.6}
  {% if block.settings.layout == 'text_left' %}
    .media-text-{{ unique }}{flex-direction:row}
  {% else %}
    .media-text-{{ unique }}{flex-direction:row-reverse}
  {% endif %}
  @media (max-width:749px){
    .media-text-{{ unique }}{flex-direction:column;gap:{{ block.settings.gap_mobile }}px;padding:{{ block.settings.pad_mobile }}px}
    .media-text__text-{{ unique }}{font-size:{{ block.settings.text_size_mobile }}px}
  }
{% endstyle %}

<div class="media-text-{{ unique }}" {{ block.shopify_attributes }}>
  <div class="media-text__media-{{ unique }}">
    {% if block.settings.image %}
      <img src="{{ block.settings.image | image_url: width: 1200 }}" alt="{{ block.settings.image.alt | escape }}" loading="lazy">
    {% else %}
      <div class="media-text__placeholder-{{ unique }}" aria-hidden="true" style="aspect-ratio:16/9;background:#f4f4f4"></div>
    {% endif %}
  </div>
  <div class="media-text__text-{{ unique }}">
    {% if block.settings.rte != blank %}
      {{ block.settings.rte }}
    {% else %}
      <h3>{{ block.settings.fallback_heading | default: 'Heading' | escape }}</h3>
      <p>Add text in the block settings.</p>
    {% endif %}
  </div>
</div>
```

Block schema entry (add into the section’s `{% schema %}` under `blocks: []`):

```json
{
  "type": "media_text",
  "name": "Media & Text",
  "settings": [
    {"type":"image_picker","id":"image","label":"Image"},
    {"type":"richtext","id":"rte","label":"Text"},
    {"type":"text","id":"fallback_heading","label":"Fallback heading"},
    {"type":"select","id":"layout","label":"Layout","options":[
      {"value":"text_left","label":"Text left, media right"},
      {"value":"text_right","label":"Media left, text right"}
    ],"default":"text_left"},
    {"type":"range","id":"gap","label":"Gap","min":0,"max":100,"step":4,"unit":"px","default":24},
    {"type":"range","id":"pad","label":"Padding","min":0,"max":100,"step":4,"unit":"px","default":24},
    {"type":"range","id":"radius","label":"Media radius","min":0,"max":30,"step":2,"unit":"px","default":8},
    {"type":"color","id":"text_color","label":"Text color","default":"#333333"},
    {"type":"range","id":"text_size","label":"Text size","min":12,"max":28,"step":1,"unit":"px","default":16},
    {"type":"range","id":"gap_mobile","label":"Mobile gap","min":0,"max":60,"step":4,"unit":"px","default":16},
    {"type":"range","id":"pad_mobile","label":"Mobile padding","min":0,"max":60,"step":4,"unit":"px","default":16},
    {"type":"range","id":"text_size_mobile","label":"Mobile text size","min":12,"max":24,"step":1,"unit":"px","default":14}
  ]
}
```

## Best practices

Layout toggling
- Prefer CSS flex‑direction controlled by a `layout` select; avoid branching markup.

Content guarding & placeholders
- Guard optional media and text with `if … != blank`.
- Use aspect‑ratio placeholders to prevent layout shifts.

Accessibility
- Provide descriptive `alt` text for media; if decorative, consider empty alt.
- Ensure headings follow a logical order; don’t skip levels.
- Respect keyboard navigation and visible focus styles for interactive content.

Performance
- Inline `{% style %}` is fast to implement; extract stable CSS to assets when blocks become large/shared.
- Always use responsive images with `image_url` + `loading="lazy"`.

Schema organization
- Group with `header` items; choose precise input types; specify `unit` for numeric ranges.
- Keep defaults sensible so merchants see a good initial state.

ELLA compatibility
- Keep BEM classes and map to ELLA’s tokens if needed (e.g., replace `container`, `btn` variants). The instance suffix `-{{ unique }}` remains the same to ensure isolation.

## Real‑world examples

The following examples are complete block implementations to paste inside a section’s block loop.

### 1) Media + Text (image)

```liquid
{% assign u = block.id | replace: '_', '' | downcase %}
{% style %}
  .img-text-{{ u }}{display:flex;gap:{{ block.settings.gap }}px}
  .img-text__img-{{ u }} img{width:100%;display:block;border-radius:{{ block.settings.radius }}px}
  .img-text__text-{{ u }}{font-size:{{ block.settings.text_size }}px}
  @media(max-width:749px){.img-text-{{ u }}{flex-direction:column}}
{% endstyle %}
<div class="img-text-{{ u }}" {{ block.shopify_attributes }}>
  <div class="img-text__img-{{ u }}">{% if block.settings.image %}<img src="{{ block.settings.image | image_url: width: 1200 }}" alt="{{ block.settings.image.alt | escape }}">{% endif %}</div>
  <div class="img-text__text-{{ u }}">{{ block.settings.rte }}</div>
</div>
```

Block schema (add under section schema → `blocks`):

```json
{"type":"img_text","name":"Image + Text","settings":[
  {"type":"image_picker","id":"image","label":"Image"},
  {"type":"richtext","id":"rte","label":"Text"},
  {"type":"range","id":"gap","label":"Gap","min":0,"max":60,"step":4,"unit":"px","default":20},
  {"type":"range","id":"radius","label":"Radius","min":0,"max":30,"step":2,"unit":"px","default":8},
  {"type":"range","id":"text_size","label":"Text size","min":12,"max":28,"step":1,"unit":"px","default":16}
]}
```

### 2) Feature item (icon + title + text + link)

```liquid
{% assign u = block.id | replace: '_', '' | downcase %}
{% style %}
  .feature-{{ u }}{text-align:center;padding:{{ block.settings.pad }}px}
  .feature__icon-{{ u }} img{width:{{ block.settings.icon_size }}px;height:{{ block.settings.icon_size }}px}
  .feature__title-{{ u }}{margin:8px 0}
{% endstyle %}
<div class="feature-{{ u }}" {{ block.shopify_attributes }}>
  <div class="feature__icon-{{ u }}">{% if block.settings.icon %}<img src="{{ block.settings.icon | image_url: width: 200 }}" alt="">{% endif %}</div>
  <h3 class="feature__title-{{ u }}">{{ block.settings.title | escape }}</h3>
  <p class="feature__text-{{ u }}">{{ block.settings.text }}</p>
  {% if block.settings.url and block.settings.cta %}<a class="btn" href="{{ block.settings.url }}">{{ block.settings.cta | escape }}</a>{% endif %}
</div>
```

Block schema:

```json
{"type":"feature","name":"Feature","settings":[
  {"type":"image_picker","id":"icon","label":"Icon"},
  {"type":"text","id":"title","label":"Title","default":"Feature"},
  {"type":"richtext","id":"text","label":"Text"},
  {"type":"text","id":"cta","label":"CTA label"},
  {"type":"url","id":"url","label":"Link"},
  {"type":"range","id":"icon_size","label":"Icon size","min":24,"max":128,"step":4,"unit":"px","default":48},
  {"type":"range","id":"pad","label":"Padding","min":0,"max":60,"step":4,"unit":"px","default":16}
]}
```

### 3) Video + Text (URL video)

```liquid
{% assign u = block.id | replace: '_', '' | downcase %}
{% style %}
  .video-text-{{ u }}{display:flex;gap:{{ block.settings.gap }}px}
  .video-text__media-{{ u }} video{width:100%;display:block;border-radius:{{ block.settings.radius }}px}
  @media(max-width:749px){.video-text-{{ u }}{flex-direction:column}}
{% endstyle %}
<div class="video-text-{{ u }}" {{ block.shopify_attributes }}>
  <div class="video-text__media-{{ u }}">
    {% if block.settings.video_url %}
      <video {% if block.settings.muted %}muted{% endif %} {% if block.settings.autoplay %}autoplay{% endif %} {% if block.settings.loop %}loop{% endif %} {% if block.settings.controls %}controls{% endif %} preload="metadata" playsinline>
        <source src="{{ block.settings.video_url }}" type="video/mp4">
      </video>
    {% else %}
      <div style="aspect-ratio:16/9;background:#f4f4f4"></div>
    {% endif %}
  </div>
  <div class="video-text__text-{{ u }}">{{ block.settings.rte }}</div>
</div>
```

Block schema:

```json
{"type":"video_text","name":"Video + Text","settings":[
  {"type":"url","id":"video_url","label":"MP4 URL"},
  {"type":"richtext","id":"rte","label":"Text"},
  {"type":"range","id":"gap","label":"Gap","min":0,"max":60,"step":4,"unit":"px","default":20},
  {"type":"range","id":"radius","label":"Video radius","min":0,"max":30,"step":2,"unit":"px","default":8},
  {"type":"checkbox","id":"autoplay","label":"Autoplay"},
  {"type":"checkbox","id":"loop","label":"Loop"},
  {"type":"checkbox","id":"muted","label":"Muted","default":true},
  {"type":"checkbox","id":"controls","label":"Show controls","default":true}
]}
```

References
- Liquid reference: https://shopify.dev/docs/api/liquid
- Sections & blocks best practices: https://shopify.dev/docs/storefronts/themes/best-practices/templates-sections-blocks
- Section schema: https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema

