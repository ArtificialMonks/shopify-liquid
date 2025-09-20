# Shopify Schema Validation Guidelines

**Comprehensive Guide to Error-Free Shopify Section Schema Development**

*Last Updated: January 2025 - Based on Official Shopify Developer Documentation*

## 🚨 **Critical Context**

This document is the **single source of truth** for schema validation rules in this repository. All agents, developers, and tools MUST follow these guidelines to prevent "Invalid schema" errors when saving Shopify liquid files.

---

## 📋 **Quick Validation Checklist**

Before saving ANY `.liquid` file with schema, verify:

- [ ] ✅ **Valid JSON syntax** (no trailing commas, proper quotes)
- [ ] ✅ **Range step validation**: `(max - min) / step ≤ 101`
- [ ] ✅ **Valid setting types** only (see [Valid Types List](#valid-setting-types))
- [ ] ✅ **No `enabled_on` or `disabled_on`** in regular sections
- [ ] ✅ **Unique IDs** within each section/block
- [ ] ✅ **Required attributes** present for each setting type
- [ ] ✅ **Single `{% schema %}` tag** only
- [ ] ✅ **No schema tag nesting** inside other Liquid tags

---

## 🎯 **Most Common Schema Violations**

### 1. **Range Step Violations (101 Steps Rule)**

**❌ WRONG:**
```json
{
  "type": "range",
  "id": "video_x_offset",
  "min": -200,
  "max": 200,
  "step": 1    // (200 - (-200)) / 1 = 400 steps > 101 ❌
}
```

**✅ CORRECT:**
```json
{
  "type": "range",
  "id": "video_x_offset",
  "min": -200,
  "max": 200,
  "step": 4    // (200 - (-200)) / 4 = 100 steps ≤ 101 ✅
}
```

**Formula:** `(max - min) / step ≤ 101`

### 2. **Invalid Setting Types**

**❌ WRONG:**
```json
{
  "type": "file",              // ❌ Not a valid type
  "id": "video_file",
  "accept": "video/mp4"
}
```

**✅ CORRECT:**
```json
{
  "type": "video",             // ✅ Valid video input type
  "id": "video_file",
  "label": "Upload Video"
}
```

### 3. **App Block Properties in Sections**

**❌ WRONG:**
```json
{
  "name": "My Section",
  "settings": [...],
  "enabled_on": {              // ❌ Only for app blocks
    "templates": ["*"],
    "groups": ["footer"]
  }
}
```

**✅ CORRECT:**
```json
{
  "name": "My Section",
  "settings": [...],
  "presets": [...]
  // ✅ Regular sections don't need enabled_on
}
```

### 4. **Step Values Below Minimum**

**❌ WRONG:**
```json
{
  "type": "range",
  "id": "letter_spacing",
  "min": -0.1,
  "max": 0.5,
  "step": 0.01             // ❌ Below 0.1 minimum
}
```

**✅ CORRECT:**
```json
{
  "type": "range",
  "id": "letter_spacing",
  "min": -0.1,
  "max": 0.5,
  "step": 0.1              // ✅ Meets 0.1 minimum
}
```

---

## 📚 **Valid Setting Types**

### **Basic Input Settings**
- `text` - Single-line text field
- `textarea` - Multi-line text field
- `number` - Numerical input
- `range` - Slider with input field
- `checkbox` - Boolean toggle
- `radio` - Radio button selection
- `select` - Dropdown or segmented control

### **Specialized Input Settings**
- `image_picker` - Image selection from admin
- `video` - Video file upload
- `video_url` - YouTube/Vimeo URL input
- `color` - Color picker
- `color_background` - CSS background properties
- `color_scheme` - Theme color scheme picker
- `font_picker` - Font selection from Shopify library
- `richtext` - Rich text editor
- `inline_richtext` - Inline rich text (no paragraphs)
- `html` - HTML markup input
- `liquid` - Liquid code input (limited)
- `url` - URL picker with resources
- `collection` - Single collection picker
- `collection_list` - Multiple collections picker
- `product` - Single product picker
- `product_list` - Multiple products picker
- `article` - Article picker
- `blog` - Blog picker
- `page` - Page picker
- `link_list` - Menu picker
- `metaobject` - Single metaobject picker
- `metaobject_list` - Multiple metaobjects picker
- `text_alignment` - Text alignment controls

### **Sidebar Settings (Non-Input)**
- `header` - Section header/divider
- `paragraph` - Informational text

---

## 🔧 **Range Setting Validation Rules**

### **Critical Formula**
```
(max - min) / step ≤ 101
```

### **Step Minimum Values**
- **Integer ranges**: `step ≥ 1`
- **Decimal ranges**: `step ≥ 0.1`

### **Common Range Fixes**

| Range | Problem | Solution |
|-------|---------|----------|
| `-200 to 200, step 1` | 400 steps | Change step to `4` |
| `-100 to 100, step 1` | 200 steps | Change step to `2` |
| `-180 to 180, step 1` | 360 steps | Change step to `4` |
| `0 to 100, step 0.5` | 200 steps | Change step to `1` |
| `10 to 200, step 1` | 190 steps | Change step to `2` |

### **Range Setting Requirements**

**Required Attributes:**
- `type`: Must be "range"
- `id`: Unique identifier
- `label`: Display label
- `min`: Minimum value (number)
- `max`: Maximum value (number)
- `default`: Default value (number, required)

**Optional Attributes:**
- `step`: Increment size (defaults to 1)
- `unit`: Display unit (e.g., "px", "%", "em")
- `info`: Help text

**❌ COMMON MISTAKES:**
```json
{
  "type": "range",
  "min": "0",        // ❌ String instead of number
  "max": "100",      // ❌ String instead of number
  "step": "1",       // ❌ String instead of number
  "default": "50"    // ❌ String instead of number
}
```

**✅ CORRECT:**
```json
{
  "type": "range",
  "min": 0,          // ✅ Number
  "max": 100,        // ✅ Number
  "step": 1,         // ✅ Number
  "default": 50      // ✅ Number
}
```

---

## 🎥 **Video Input Validation**

### **Correct Video Types**

**✅ For uploaded video files:**
```json
{
  "type": "video",
  "id": "my_video",
  "label": "Upload Video"
}
```

**✅ For external video URLs:**
```json
{
  "type": "video_url",
  "id": "youtube_video",
  "label": "YouTube URL",
  "accept": ["youtube", "vimeo"]
}
```

**✅ For manual URL entry:**
```json
{
  "type": "text",
  "id": "video_url",
  "label": "Video URL"
}
```

### **❌ INVALID Video Types**
```json
{
  "type": "file",              // ❌ Not supported
  "accept": "video/mp4"        // ❌ Invalid combination
}
```

---

## 📝 **Schema Structure: Sections vs Blocks**

### **🎯 CRITICAL: Two Types of Schemas**

#### **1. Section Schemas (Standalone Sections)**
- **Location**: Section files in `/sections` folder
- **Schema Tag**: `{% schema %}...{% endschema %}`
- **Purpose**: Complete page sections with their own configurations

#### **2. Theme Block Schemas (Standalone Blocks)**
- **Location**: Block files in `/blocks` folder
- **Schema Tag**: `{% schema %}...{% endschema %}`
- **Purpose**: Reusable components that can be used across multiple sections

---

## 📝 **Section Schema Structure**

### **Valid Section Schema Attributes**

```json
{
  "name": "Section Name",           // ✅ Required
  "tag": "section",                 // ✅ Optional: article, aside, div, footer, header, section
  "class": "my-section",            // ✅ Optional: CSS class
  "limit": 1,                       // ✅ Optional: 1 or 2 max instances
  "settings": [...],                // ✅ Optional: Input settings array
  "blocks": [...],                  // ✅ Optional: Block definitions or references
  "max_blocks": 50,                 // ✅ Optional: Max 50 blocks
  "presets": [...],                 // ✅ Optional: Preset configurations
  "default": {...},                 // ✅ Optional: Default for static sections
  "locales": {...},                 // ✅ Optional: Translations
  "enabled_on": {...},              // ❌ NEVER use in sections (app blocks only)
  "disabled_on": {...}              // ❌ NEVER use in sections (app blocks only)
}
```

### **❌ INVALID Section Attributes**
```json
{
  "name": "My Section",
  "enabled_on": {...},              // ❌ Only for app blocks
  "disabled_on": {...},             // ❌ Only for app blocks
  "templates": [...]                // ❌ Deprecated, use enabled_on in app blocks
}
```

---

## 🧩 **Theme Block Schema Structure**

### **Valid Theme Block Schema Attributes**

```json
{
  "name": "Block Name",             // ✅ Required: Display name
  "tag": "div",                     // ✅ Optional: HTML wrapper tag
  "class": "my-block",              // ✅ Optional: CSS class
  "settings": [...],                // ✅ Optional: Block settings
  "blocks": [...],                  // ✅ Optional: Child blocks (nesting)
  "presets": [...]                  // ✅ Optional: Preset configurations
}
```

### **Section Block Definitions (Within Section Schema)**

```json
{
  "blocks": [
    {
      "type": "my_block",           // ✅ Required: Block type identifier
      "name": "My Block",           // ✅ Required: Display name
      "limit": 5,                   // ✅ Optional: Max instances per section
      "settings": [...]             // ✅ Optional: Block settings
    }
  ]
}
```

### **Block Validation Rules**
- ✅ Block `type` must be unique within section
- ✅ Block `name` must be unique within section
- ✅ Setting `id` must be unique within block
- ✅ Maximum 50 blocks per section total
- ✅ Static blocks don't count toward limit

### **Key Differences: Theme Blocks vs Section Blocks**

| Feature | Theme Blocks | Section Blocks |
|---------|-------------|----------------|
| **File Location** | `/blocks` folder | Defined in section schema |
| **Schema Tag** | Own `{% schema %}` | In section's `blocks` array |
| **Reusability** | Cross-section | Single section only |
| **Nesting** | ✅ Can contain blocks | ❌ Single level only |
| **Schema Attributes** | `name`, `settings`, `blocks`, `presets` | `type`, `name`, `limit`, `settings` |

---

## 🎨 **Preset Configuration**

### **Valid Preset Structure**

```json
{
  "presets": [
    {
      "name": "Preset Name",         // ✅ Required
      "category": "Layout",          // ✅ Optional: Groups presets
      "settings": {                  // ✅ Optional: Default values
        "heading": "Default Title",
        "show_borders": true
      },
      "blocks": [                    // ✅ Optional: Default blocks
        {
          "type": "text_block",
          "settings": {
            "content": "Default text"
          }
        }
      ]
    }
  ]
}
```

### **Preset Rules**
- ✅ Don't use presets with statically rendered sections
- ✅ Use `default` attribute for static sections instead
- ✅ Settings in presets override schema defaults
- ✅ `name` is required for each preset

---

## 🌐 **Translation Support**

### **Valid Locales Structure**

```json
{
  "locales": {
    "en": {
      "title": "Slideshow",
      "description": "Image slideshow section"
    },
    "fr": {
      "title": "Diaporama",
      "description": "Section diaporama d'images"
    }
  }
}
```

### **Translation Access**
```liquid
{{ 'sections.slideshow.title' | t }}
```

---

## ⚠️ **JSON Validation Rules**

### **Critical JSON Requirements**
- ✅ **No trailing commas** in objects or arrays
- ✅ **Double quotes only** for strings and keys
- ✅ **Valid escape sequences** in strings
- ✅ **Proper nesting** of objects and arrays
- ✅ **No comments** allowed in JSON

### **❌ COMMON JSON ERRORS**

**Trailing Commas:**
```json
{
  "type": "text",
  "label": "Title",    // ❌ Trailing comma
}
```

**Single Quotes:**
```json
{
  'type': 'text',     // ❌ Single quotes
  "label": "Title"
}
```

**Missing Quotes:**
```json
{
  type: "text",       // ❌ Unquoted key
  "label": "Title"
}
```

### **✅ CORRECT JSON**
```json
{
  "type": "text",
  "label": "Title"
}
```

---

## 🏗️ **Schema Tag Placement Rules**

### **✅ VALID Placement**
```liquid
<!-- Anywhere in section file -->
{% schema %}
{
  "name": "My Section"
}
{% endschema %}

<!-- At the end (recommended) -->
<section>
  <!-- Section content -->
</section>

{% schema %}
{
  "name": "My Section"
}
{% endschema %}
```

### **❌ INVALID Placement**
```liquid
<!-- Inside another Liquid tag -->
{% if true %}
  {% schema %}           // ❌ Nested inside if tag
  {
    "name": "My Section"
  }
  {% endschema %}
{% endif %}

<!-- Multiple schema tags -->
{% schema %}              // ❌ First schema tag
{"name": "Section 1"}
{% endschema %}

{% schema %}              // ❌ Second schema tag (invalid)
{"name": "Section 2"}
{% endschema %}
```

---

## 🔍 **Setting ID Validation**

### **ID Uniqueness Rules**
- ✅ **Section setting IDs** must be unique within the section
- ✅ **Block setting IDs** must be unique within each block type
- ✅ **Block types** must be unique within the section
- ✅ **Block names** must be unique within the section

### **Valid ID Patterns**
```json
{
  "settings": [
    {"id": "heading", "type": "text"},        // ✅ Valid
    {"id": "show_borders", "type": "checkbox"}, // ✅ Valid
    {"id": "text_color", "type": "color"}     // ✅ Valid
  ]
}
```

### **❌ ID Collision Examples**
```json
{
  "settings": [
    {"id": "title", "type": "text"},
    {"id": "title", "type": "richtext"}      // ❌ Duplicate ID
  ]
}
```

---

## 📊 **Limits and Constraints**

### **Section Limits**
- ✅ **Maximum sections per template**: 25
- ✅ **Maximum blocks per section**: 50 (static blocks don't count)
- ✅ **Section limit attribute**: 1 or 2 only
- ✅ **Collection list limit**: 50 maximum
- ✅ **Product list limit**: 50 maximum

### **Setting Limits**
- ✅ **Range steps maximum**: 101 steps total
- ✅ **Step value minimum**: 0.1
- ✅ **Liquid content maximum**: 50kb
- ✅ **Color scheme maximum**: 21 schemes

---

## 🚫 **What NOT to Do**

### **❌ NEVER Use These**
```json
{
  "enabled_on": {...},              // ❌ Only for app blocks
  "disabled_on": {...},             // ❌ Only for app blocks
  "templates": [...],               // ❌ Deprecated
  "type": "file"                    // ❌ Invalid type
}
```

### **❌ AVOID These Patterns**
- Multiple `{% schema %}` tags
- Schema tags inside Liquid conditionals
- String values for numeric range attributes
- Trailing commas in JSON
- Single quotes in JSON
- Comments in schema JSON

---

## 🛠️ **Development Workflow**

### **Pre-Save Checklist**
1. **Validate JSON syntax** with a JSON validator
2. **Calculate range steps** using formula: `(max - min) / step ≤ 101`
3. **Check setting types** against valid types list
4. **Verify unique IDs** within sections and blocks
5. **Test in Shopify admin** theme editor

### **Tools for Validation**
- **JSON Validators**: JSONLint, VS Code JSON validation
- **Theme Check**: Shopify's official linting tool
- **Shopify CLI**: Theme development tools
- **Browser Dev Tools**: Network tab for error messages

### **Error Debugging Steps**
1. **Check error message** for specific line/issue
2. **Validate JSON syntax** first
3. **Check range calculations** if ranges present
4. **Verify setting types** against documentation
5. **Remove `enabled_on`** if present in sections
6. **Check for duplicate IDs**

---

## 📋 **Agent Validation Rules**

All agents in this repository must validate schemas before suggesting or creating code:

### **Mandatory Checks**
1. ✅ **Range Validation**: Calculate `(max - min) / step ≤ 101` for all ranges
2. ✅ **Type Validation**: Only use valid setting types from approved list
3. ✅ **JSON Validation**: Ensure valid JSON syntax
4. ✅ **ID Uniqueness**: Check for duplicate IDs
5. ✅ **Required Attributes**: Verify all required attributes present
6. ✅ **App Block Detection**: Remove `enabled_on`/`disabled_on` from sections

### **Agent Response Pattern**
When creating schema, agents must:
1. Calculate all range steps and adjust if needed
2. Use only validated setting types
3. Include validation comments in code
4. Provide explanation of any adjustments made

---

## 📖 **Reference Examples**

### **Complete Valid Section Schema**
```json
{% schema %}
{
  "name": "Text with Image",
  "tag": "section",
  "class": "text-image",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Our Story"
    },
    {
      "type": "richtext",
      "id": "content",
      "label": "Content"
    },
    {
      "type": "image_picker",
      "id": "image",
      "label": "Image"
    },
    {
      "type": "range",
      "id": "image_width",
      "label": "Image Width (%)",
      "min": 20,
      "max": 80,
      "step": 5,
      "default": 50,
      "unit": "%"
    }
  ],
  "blocks": [
    {
      "type": "feature",
      "name": "Feature",
      "settings": [
        {
          "type": "text",
          "id": "title",
          "label": "Feature Title"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Text with Image",
      "settings": {
        "heading": "Our Story"
      }
    }
  ]
}
{% endschema %}
```

---

## 🔗 **Official Documentation Links**

- [Section Schema](https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema)
- [Input Settings](https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings)
- [Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check)
- [Theme Architecture](https://shopify.dev/docs/storefronts/themes/architecture)

---

## 🎯 **Quick Formula Reference**

### **Range Step Calculation**
```
Steps = (max - min) / step
Valid when: Steps ≤ 101
```

### **Common Conversions**
| Original | Problem | Fixed |
|----------|---------|-------|
| `step: 1, range: -200 to 200` | 400 steps | `step: 4` = 100 steps |
| `step: 1, range: -100 to 100` | 200 steps | `step: 2` = 100 steps |
| `step: 1, range: 0 to 150` | 150 steps | `step: 2` = 75 steps |
| `step: 0.5, range: 0 to 100` | 200 steps | `step: 1` = 100 steps |

---

## 🤖 **Agent Validation Instructions**

**For AI assistants and code review agents working with Shopify Liquid schemas:**

### Pre-Save Validation Checklist
Before any schema implementation, verify:
- [ ] JSON syntax is valid (no trailing commas, proper quotes)
- [ ] All setting types are from the valid list above
- [ ] Range settings follow `(max - min) / step ≤ 101` rule
- [ ] Step values are ≥ 0.1 for all ranges
- [ ] **Section schemas**: No `enabled_on` attributes (app blocks only)
- [ ] **Theme block schemas**: Include required `name` attribute
- [ ] Video uploads use `"type": "video"` not `"type": "file"`
- [ ] All required fields (`type`, `id`, `label`) are present
- [ ] Setting IDs are unique within the schema
- [ ] Block type names are unique and descriptive

### Schema Type Detection
**Before validation, identify schema type:**

#### **Section Schema (in `/sections` folder)**
- Must have `name` attribute
- Can have `limit`, `max_blocks`, `default`, `locales`
- NEVER use `enabled_on` or `disabled_on`
- Can define block types in `blocks` array

#### **Theme Block Schema (in `/blocks` folder)**
- Must have `name` attribute
- Can have `tag`, `class`, `settings`, `blocks`, `presets`
- Can contain child blocks (nesting)
- Used across multiple sections

### Common Error Prevention
**Always check for these patterns that cause "FileSaveError: Invalid schema":**
1. Range step calculations exceeding 101 steps
2. Invalid setting types (especially `file` for videos)
3. Section-level `enabled_on` attributes (sections vs app blocks confusion)
4. Missing required schema fields
5. Invalid JSON syntax
6. Wrong schema structure for file type (section vs theme block)

### Implementation Standards
When creating or modifying Shopify schemas:
- **Identify file type first**: Section or Theme Block
- Use this document as the single source of truth
- Validate each setting against the type reference
- Calculate range steps before implementation
- Test schema JSON validity before suggesting code
- Ensure proper schema structure for file type
- Reference official Shopify documentation for any edge cases

---

**📅 Document Version**: 1.0 - January 2025
**📚 Source**: Official Shopify Developer Documentation
**🔄 Next Review**: Updates following Shopify releases

This document serves as the definitive guide for schema validation in this repository. All code must comply with these standards to ensure error-free Shopify liquid file saves.