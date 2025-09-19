# Minimal JS Enhancements for Blocks (Scoped-CSS Friendly)

Goal: add small progressive enhancements (toggles, carousels) that work with the instance‑scoped CSS block pattern (suffix from `block.id`), support the Shopify editor lifecycle, and remain dependency‑free.

On this page
- Lifecycle hooks (Shopify editor)
- Selector strategy with instance suffix
- Toggle (accordion) example
- Carousel example (no dependency)
- A11y & reduced motion
- Cleanup, performance, and testing

## Lifecycle hooks (Shopify editor)
Theme editor emits events you can use to init/teardown logic when a section or block is added/removed/selected:

- `shopify:section:load` / `shopify:section:unload`
- `shopify:block:select` / `shopify:block:deselect`

Basic bootstrap (put in assets/section-enhancements.js and include it in theme.liquid):

```js
(function () {
  const registry = new Map(); // section.id -> teardown function

  function initSection(sectionEl) {
    // Find any interactive widgets within the section
    sectionEl.querySelectorAll('[data-enhance="accordion"]').forEach(initAccordion);
    sectionEl.querySelectorAll('[data-enhance="carousel"]').forEach(initCarousel);
  }

  function teardownSection(sectionEl) {
    // Optional: if your initializers return cleanup fns, call them here
  }

  document.addEventListener('shopify:section:load', (e) => initSection(e.target));
  document.addEventListener('shopify:section:unload', (e) => teardownSection(e.target));
  // Optionally react to block selection for focus/scroll
  document.addEventListener('shopify:block:select', (e) => {
    const el = e.target;
    if (el && el.scrollIntoView) try { el.scrollIntoView({ block: 'center', behavior: 'smooth' }); } catch {}
  });

  // Export hooks if needed globally
  window.__SectionEnhancers = { initSection, teardownSection };
})();
```

## Selector strategy with instance suffix
Your CSS/markup uses a unique class suffix (e.g., `.accordion-{{ unique }}`) derived from `block.id`. JS has two safe ways to target an instance:

- Query by the unique class you already render: `sectionEl.querySelector('.accordion-<suffix>')`
- Add a data attribute on the root: `<div data-block-id="{{ block.id }}" ...>` and query `[data-block-id]`

Prefer scoping queries to the current section element you receive from `shopify:section:load` to avoid touching other instances.

## Toggle (accordion) — minimal, accessible
Markup (per block, inside the section):

```liquid
{%- assign u = block.id | replace: '_', '' | downcase -%}
<button class="accordion__trigger-{{ u }}" aria-expanded="false" aria-controls="acc-panel-{{ u }}">{{ block.settings.title | escape }}</button>
<div id="acc-panel-{{ u }}" class="accordion__panel-{{ u }}" hidden>{{ block.settings.rte }}</div>
```

JS initializer:

```js
function initAccordion(root) {
  root.setAttribute('data-enhance', 'accordion');
  const trigger = root.querySelector('[aria-controls]');
  const panelId = trigger && trigger.getAttribute('aria-controls');
  const panel = panelId && root.querySelector('#' + CSS.escape(panelId));
  if (!trigger || !panel) return;
  const onClick = () => {
    const expanded = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', String(!expanded));
    panel.hidden = expanded;
  };
  trigger.addEventListener('click', onClick);
  return () => trigger.removeEventListener('click', onClick);
}
```

Notes
- `hidden` toggling provides instant show/hide without layout thrash.
- Keep styles in your scoped CSS (`.accordion__panel-{{ u }}[hidden]{display:none}`) if needed for older browsers.

## Carousel — minimal, dependency‑free
Markup (matches our testimonial block structure):

```liquid
{%- assign u = block.id | replace: '_', '' | downcase -%}
<div class="carousel-{{ u }}" data-enhance="carousel">
  <button class="carousel__prev-{{ u }}" aria-label="Previous"></button>
  <div class="carousel__viewport-{{ u }}" role="region" aria-roledescription="carousel" tabindex="0">
    <ul class="carousel__slides-{{ u }}" role="list"> ... slides ... </ul>
  </div>
  <button class="carousel__next-{{ u }}" aria-label="Next"></button>
  <div class="sr-only carousel__status-{{ u }}" aria-live="polite"></div>
</div>
```

JS initializer (horizontal translate + roving tabindex):

```js
function initCarousel(root) {
  const prev = root.querySelector('[class*="carousel__prev-"]');
  const next = root.querySelector('[class*="carousel__next-"]');
  const viewport = root.querySelector('[class*="carousel__viewport-"]');
  const slides = Array.from(root.querySelectorAll('[class*="carousel__slides-"] > *'));
  if (!viewport || slides.length === 0) return;
  let index = 0;
  const status = root.querySelector('[class*="carousel__status-"]');

  function update() {
    slides.forEach((li, i) => {
      li.setAttribute('aria-hidden', String(i !== index));
      li.tabIndex = i === index ? 0 : -1;
    });
    // Snap to slide (assumes equal width cards via CSS)
    root.querySelector('[class*="carousel__slides-"]').style.transform = `translateX(${-index * 100}%)`;
    if (status) status.textContent = `Slide ${index + 1} of ${slides.length}`;
  }
  function go(delta) { index = (index + delta + slides.length) % slides.length; update(); }

  const onPrev = () => go(-1);
  const onNext = () => go(1);
  prev && prev.addEventListener('click', onPrev);
  next && next.addEventListener('click', onNext);
  viewport.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') go(-1);
    if (e.key === 'ArrowRight') go(1);
  });

  // Respect reduced motion
  const m = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (m && m.matches) root.querySelector('[class*="carousel__slides-"]').style.transition = 'none';

  update();
  return () => {
    prev && prev.removeEventListener('click', onPrev);
    next && next.removeEventListener('click', onNext);
  };
}
```

CSS expectations (in your scoped CSS):
- `.carousel__slides-{{ u }}` is a flex row of equal‑width slides.
- Add `transition: transform .3s ease` (JS will disable it for reduced motion).

## Accessibility & reduced motion
- Use `aria-live="polite"` status updates.
- Keep controls as `<button>` with clear `aria-label`s.
- Keyboard: ArrowLeft/ArrowRight on viewport; ensure focus ring is visible.
- Respect `prefers-reduced-motion` for transitions.

## Cleanup, performance, and testing
- Return cleanup functions from initializers; call them in `shopify:section:unload`.
- Scope queries to the section element to avoid touching other instances.
- Avoid layout thrash: use transforms for carousels; `hidden` for toggles.
- Test in the editor: moving/deleting sections should not leak listeners.

