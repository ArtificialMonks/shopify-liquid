# Schema Examples (Copy/Paste)

1) Simple settings

```json
{
  "name": "Text banner",
  "settings": [
    {"type":"text","id":"heading","label":"Heading","default":"Welcome"},
    {"type":"richtext","id":"subtext","label":"Subtext"},
    {"type":"url","id":"link","label":"Link"},
    {"type":"checkbox","id":"center","label":"Center content","default": true}
  ],
  "presets": [{"name":"Text banner"}]
}
```

2) With blocks and max_blocks

```json
{
  "name": "FAQ",
  "max_blocks": 12,
  "settings": [
    {"type":"select","id":"style","label":"Style","options":[
      {"value":"bordered","label":"Bordered"},
      {"value":"plain","label":"Plain"}
    ],"default":"bordered"}
  ],
  "blocks": [
    {
      "type": "item",
      "name": "Item",
      "settings": [
        {"type":"text","id":"q","label":"Question"},
        {"type":"richtext","id":"a","label":"Answer"}
      ]
    }
  ],
  "presets": [{"name":"FAQ","blocks":[{"type":"item"},{"type":"item"}]}]
}
```

3) enabled_on / disabled_on

```json
{
  "name": "Promo banner",
  "settings": [
    {"type":"text","id":"title","label":"Title","default":"Free shipping over $50"}
  ],
  "presets": [{"name":"Promo banner"}],
  "enabled_on": {"templates": ["*"]},
  "disabled_on": {"templates": ["cart"], "groups": ["footer"]}
}
```

4) Locales (section3 editor labels)

```json
{
  "name": "Slideshow",
  "settings": [{"type":"text","id":"title","label":"Title"}],
  "locales": {
    "en": {"title": "Slideshow"},
    "fr": {"title": "Diaporama"}
  },
  "presets": [{"name":"Slideshow"}]
}
```

5) Presets with default blocks

```json
{
  "name":"Logo list",
  "max_blocks": 12,
  "blocks": [{"type":"logo","name":"Logo","settings":[{"type":"image_picker","id":"image","label":"Image"}]}],
  "presets": [{"name":"Logo list","blocks":[{"type":"logo"},{"type":"logo"},{"type":"logo"}]}]
}
```

Notes
- Only valid JSON inside `{% schema %}`. Liquid is not rendered.
- One schema per section.
- Prefer short, clear labels; provide sane `default` values.
- Use `enabled_on`/`disabled_on` to guide where merchants can add the section.

References
- Section schema (attributes incl. enabled_on/disabled_on): https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema

