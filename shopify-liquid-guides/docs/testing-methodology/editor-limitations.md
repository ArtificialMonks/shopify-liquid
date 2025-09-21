# Theme Editor Limitations & Testing Methodology

**Complete guide to understanding what works in theme editor vs preview mode**

## Editor vs Preview Mode Overview

The Shopify theme editor has specific limitations that affect how animations, effects, and interactions are displayed. Understanding these limitations is crucial for proper testing and merchant education.

## What Doesn't Work in Theme Editor

### ❌ **Scroll-Triggered Animations**

**Limitation**: Scroll animations are completely disabled in the theme editor.

```css
/* These animations won't trigger in editor */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-animate {
  animation: fadeInUp 0.6s ease-out;
}
```

**Why**: Theme editor needs responsive scrolling for configuration panels.

**Testing Required**: Always test scroll animations in preview mode.

### ❌ **Intersection Observer Effects**

**Limitation**: JavaScript-based viewport detection doesn't work properly.

```javascript
// Won't work in theme editor
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate');
    }
  });
});
```

**Alternative**: Use CSS-only animations or test in preview mode.

### ⚠️ **Limited Hover Effects**

**Limitation**: Complex hover states may not behave correctly.

```css
/* May not work properly in editor */
.video-container:hover .video-overlay {
  opacity: 0;
  transform: scale(1.05);
  transition: all 0.3s ease;
}
```

**Why**: Editor interface can interfere with hover states.

**Testing Required**: Verify hover effects in preview mode.

### ❌ **Autoplay Media**

**Limitation**: Autoplay videos and audio don't function in editor.

```liquid
<!-- Won't autoplay in editor -->
<video autoplay muted loop>
  <source src="{{ 'hero-video.mp4' | asset_url }}" type="video/mp4">
</video>
```

**Why**: Browser autoplay policies and editor security restrictions.

**Testing Required**: Test autoplay functionality in preview mode.

### ⚠️ **CSS Animations with Delays**

**Limitation**: Staggered animations may not display correctly.

```css
/* Timing may be off in editor */
.stagger-animation:nth-child(1) { animation-delay: 0.1s; }
.stagger-animation:nth-child(2) { animation-delay: 0.2s; }
.stagger-animation:nth-child(3) { animation-delay: 0.3s; }
```

**Why**: Editor rendering optimizations can affect timing.

## What Works in Theme Editor

### ✅ **Basic CSS Transitions**

```css
/* Works perfectly in editor */
.button {
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #007acc;
}
```

### ✅ **Transform Effects**

```css
/* Works in editor */
.card:hover {
  transform: translateY(-5px);
  transition: transform 0.2s ease;
}
```

### ✅ **Color and Opacity Changes**

```css
/* Works in editor */
.overlay {
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.overlay:hover {
  opacity: 1;
}
```

### ✅ **Layout Changes**

```css
/* Works in editor */
.grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  transition: grid-template-columns 0.3s ease;
}

.grid.expanded {
  grid-template-columns: 1fr 3fr;
}
```

## Testing Methodology

### Phase 1: Editor Testing

**Purpose**: Verify settings functionality and basic interactions.

**Test Checklist**:
- ✅ All settings appear and function
- ✅ Basic hover effects work
- ✅ Color changes apply correctly
- ✅ Layout adjustments respond
- ✅ Typography changes work
- ✅ No JavaScript console errors

**Process**:
```bash
1. Open theme editor
2. Navigate to section/block
3. Test each setting systematically
4. Verify responsive behavior at different screen sizes
5. Check for console errors (F12 → Console)
```

### Phase 2: Preview Mode Testing

**Purpose**: Verify animations, effects, and complete functionality.

**Test Checklist**:
- ✅ Scroll animations trigger correctly
- ✅ Autoplay media functions
- ✅ Hover effects work as intended
- ✅ Interactive elements respond
- ✅ Performance is acceptable
- ✅ Mobile behavior is correct

**Process**:
```bash
1. Click "Preview" in theme editor
2. Navigate to pages with your components
3. Test scroll animations by scrolling up/down
4. Test hover effects on desktop
5. Test touch interactions on mobile
6. Check performance with DevTools
```

### Phase 3: Live Testing

**Purpose**: Final validation in production environment.

**Test Checklist**:
- ✅ All functionality works as expected
- ✅ Performance meets standards
- ✅ No breaking changes from editor to live
- ✅ Analytics and tracking work
- ✅ SEO elements function correctly

## Component-Specific Testing

### Video + Text Block Testing

**Editor Tests**:
```bash
1. Layout Style Changes
   - Switch between side_by_side, stacked, overlay
   - Verify layout responds immediately

2. Video Position Controls
   - Test left, center, right positioning
   - Check mobile layout overrides

3. Text Positioning
   - Verify all position options work
   - Test overlay positioning

4. Typography Settings
   - Font changes apply correctly
   - Size adjustments work
   - Color changes are immediate
```

**Preview Mode Tests**:
```bash
1. Scroll Animations
   - Scroll to trigger animations
   - Test different animation styles
   - Verify reduced motion preference

2. Hover Effects
   - Video hover effects (scale, glow, etc.)
   - Text hover effects (highlight, underline)
   - Combined hover interactions

3. Video Functionality
   - Autoplay behavior
   - Background video coverage
   - Video controls functionality

4. Performance
   - Smooth animations at 60fps
   - No layout shift during load
   - Reasonable loading times
```

## Testing Tools and Scripts

### Automated Testing Script

```javascript
// Theme testing utility
class ThemeTestingUtility {
  constructor() {
    this.isEditor = window.location.href.includes('editor');
    this.isPreview = window.location.href.includes('preview_theme_id');
  }

  testAnimations() {
    if (this.isEditor) {
      console.warn('⚠️ Scroll animations disabled in editor - test in preview mode');
      return false;
    }

    // Test scroll animations
    const animatedElements = document.querySelectorAll('[data-scroll-animate]');
    console.log(`✅ Found ${animatedElements.length} scroll-animated elements`);

    return animatedElements.length > 0;
  }

  testHoverEffects() {
    const hoverElements = document.querySelectorAll('[data-hover-effect]');

    hoverElements.forEach(el => {
      // Simulate hover for testing
      el.dispatchEvent(new MouseEvent('mouseenter'));
      setTimeout(() => {
        el.dispatchEvent(new MouseEvent('mouseleave'));
      }, 1000);
    });

    console.log(`✅ Tested ${hoverElements.length} hover effects`);
  }

  testVideoElements() {
    const videos = document.querySelectorAll('video');

    videos.forEach(video => {
      if (video.autoplay && this.isEditor) {
        console.warn('⚠️ Autoplay video detected - may not work in editor');
      }
    });

    console.log(`✅ Found ${videos.length} video elements`);
  }

  runFullTest() {
    console.log('🧪 Running theme testing suite...');
    console.log(`📍 Environment: ${this.isEditor ? 'Editor' : this.isPreview ? 'Preview' : 'Live'}`);

    this.testAnimations();
    this.testHoverEffects();
    this.testVideoElements();

    console.log('✅ Testing complete');
  }
}

// Usage: Open browser console and run
// new ThemeTestingUtility().runFullTest();
```

### Manual Testing Checklist

**Print-friendly checklist for comprehensive testing**:

```markdown
## Theme Component Testing Checklist

### Editor Testing ✓
- [ ] All settings visible and functional
- [ ] Layout changes apply immediately
- [ ] Typography settings work
- [ ] Color changes are instant
- [ ] No console errors
- [ ] Mobile responsive behavior
- [ ] Settings persist after save

### Preview Mode Testing ✓
- [ ] Scroll animations trigger
- [ ] Hover effects function correctly
- [ ] Autoplay media works
- [ ] Interactive elements respond
- [ ] Performance is smooth (60fps)
- [ ] Mobile touch interactions work
- [ ] Loading states are acceptable

### Cross-Browser Testing ✓
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers

### Performance Testing ✓
- [ ] Lighthouse score >90
- [ ] Core Web Vitals pass
- [ ] No layout shift
- [ ] Fast loading times
- [ ] Smooth animations

### Accessibility Testing ✓
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Focus states visible
- [ ] Reduced motion respected
- [ ] Color contrast passes
```

## Best Practices

### 🎯 **Testing Strategy**

1. **Test in Editor First**
   - Verify basic functionality
   - Check settings integration
   - Ensure no console errors

2. **Validate in Preview**
   - Test all animations and effects
   - Verify complete user experience
   - Check performance metrics

3. **Final Live Testing**
   - Confirm production behavior
   - Test with real content
   - Monitor ongoing performance

### 🔧 **Development Guidelines**

1. **Design for Editor Limitations**
   - Don't rely on scroll animations for basic functionality
   - Provide fallbacks for complex effects
   - Use CSS-only animations when possible

2. **Documentation for Merchants**
   - Clearly explain what needs preview testing
   - Provide preview links for animation testing
   - Include screenshots of expected behavior

3. **Progressive Enhancement**
   - Basic functionality works in editor
   - Enhanced features work in preview/live
   - Graceful degradation for unsupported features

---

*This testing methodology ensures that all theme features work correctly across all environments while accounting for the specific limitations of the Shopify theme editor.*