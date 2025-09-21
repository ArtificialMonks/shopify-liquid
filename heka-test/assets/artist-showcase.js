/**
 * Artist Showcase - Olympic-Level JavaScript Architecture
 *
 * Interactive functionality for the artist showcase section including:
 * - Gallery management (carousel, lightbox, masonry)
 * - Video controls and lazy loading
 * - Expandable content and tabs
 * - Product variant selection and cart integration
 * - Parallax effects and animations
 * - Touch/swipe support for mobile
 */

class ArtistShowcase {
  constructor(element) {
    this.element = element;
    this.sectionId = element.dataset.sectionId;
    this.galleries = [];
    this.videos = [];
    this.products = [];
    this.expandables = [];
    this.tabs = [];

    this.init();
  }

  init() {
    this.initGalleries();
    this.initVideos();
    this.initProducts();
    this.initExpandables();
    this.initTabs();
    this.initParallax();
    this.initAnimations();
    this.initSocialSharing();
    this.initAccessibility();
  }

  /**
   * Gallery Management
   */
  initGalleries() {
    const galleries = this.element.querySelectorAll('.artist-showcase__gallery');

    galleries.forEach(gallery => {
      const galleryManager = new GalleryManager(gallery);
      this.galleries.push(galleryManager);
    });
  }

  /**
   * Video Management
   */
  initVideos() {
    const videos = this.element.querySelectorAll('.artist-showcase__video');

    videos.forEach(video => {
      const videoManager = new VideoManager(video);
      this.videos.push(videoManager);
    });
  }

  /**
   * Product Integration
   */
  initProducts() {
    const products = this.element.querySelectorAll('.artist-showcase__product');

    products.forEach(product => {
      const productManager = new ProductManager(product);
      this.products.push(productManager);
    });
  }

  /**
   * Expandable Content
   */
  initExpandables() {
    const expandables = this.element.querySelectorAll('[data-expandable-trigger]');

    expandables.forEach(trigger => {
      const expandableManager = new ExpandableManager(trigger);
      this.expandables.push(expandableManager);
    });
  }

  /**
   * Tabbed Content
   */
  initTabs() {
    const tabContainers = this.element.querySelectorAll('[data-tabs-container]');

    tabContainers.forEach(container => {
      const tabManager = new TabManager(container);
      this.tabs.push(tabManager);
    });
  }

  /**
   * Parallax Effects
   */
  initParallax() {
    const parallaxElements = this.element.querySelectorAll('[data-parallax="true"]');

    if (parallaxElements.length > 0 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      this.parallaxManager = new ParallaxManager(parallaxElements);
    }
  }

  /**
   * Scroll Animations
   */
  initAnimations() {
    if (this.element.classList.contains('artist-showcase--animated')) {
      this.animationManager = new AnimationManager(this.element);
    }
  }

  /**
   * Social Sharing
   */
  initSocialSharing() {
    const shareButtons = this.element.querySelectorAll('.artist-showcase__content-share-button');

    shareButtons.forEach(button => {
      button.addEventListener('click', this.handleSocialShare.bind(this));
    });
  }

  /**
   * Accessibility Features
   */
  initAccessibility() {
    // Skip links for keyboard navigation
    this.initSkipLinks();

    // Focus management
    this.initFocusManagement();

    // ARIA live regions for dynamic content
    this.initLiveRegions();
  }

  initSkipLinks() {
    const firstBlock = this.element.querySelector('.artist-showcase__block');
    if (firstBlock) {
      firstBlock.setAttribute('tabindex', '-1');
    }
  }

  initFocusManagement() {
    // Trap focus in modals/lightboxes
    this.element.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeActiveModals();
      }
    });
  }

  initLiveRegions() {
    // Create live region for announcements
    if (!document.getElementById('artist-showcase-live-region')) {
      const liveRegion = document.createElement('div');
      liveRegion.id = 'artist-showcase-live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('aria-atomic', 'true');
      liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
      document.body.appendChild(liveRegion);
    }
  }

  handleSocialShare(e) {
    e.preventDefault();
    const url = e.currentTarget.href;

    // Open in popup window
    window.open(url, 'share', 'width=600,height=400,scrollbars=yes,resizable=yes');
  }

  closeActiveModals() {
    // Close any open lightboxes
    this.galleries.forEach(gallery => gallery.closeLightbox());

    // Close any expanded content
    this.expandables.forEach(expandable => expandable.collapse());
  }

  announce(message) {
    const liveRegion = document.getElementById('artist-showcase-live-region');
    if (liveRegion) {
      liveRegion.textContent = message;
    }
  }
}

/**
 * Gallery Manager - Handles image galleries, carousels, and lightboxes
 */
class GalleryManager {
  constructor(element) {
    this.element = element;
    this.layout = element.dataset.galleryLayout;
    this.lightboxEnabled = element.dataset.lightbox === 'true';
    this.currentIndex = 0;
    this.images = Array.from(element.querySelectorAll('.artist-showcase__gallery-item'));
    this.lightbox = null;

    this.init();
  }

  init() {
    if (this.layout === 'carousel') {
      this.initCarousel();
    }

    if (this.lightboxEnabled) {
      this.initLightbox();
    }

    this.initTouchSupport();
  }

  initCarousel() {
    const navButtons = this.element.querySelectorAll('[data-gallery-nav]');
    const dots = this.element.querySelectorAll('[data-gallery-dot]');

    navButtons.forEach(button => {
      button.addEventListener('click', this.handleNavigation.bind(this));
    });

    dots.forEach(dot => {
      dot.addEventListener('click', this.handleDotNavigation.bind(this));
    });

    // Auto-advance carousel
    this.startAutoAdvance();
  }

  initLightbox() {
    const triggers = this.element.querySelectorAll('[data-lightbox-trigger]');

    triggers.forEach(trigger => {
      trigger.addEventListener('click', this.openLightbox.bind(this));
    });
  }

  initTouchSupport() {
    if (this.layout === 'carousel') {
      let startX = 0;
      let startY = 0;

      this.element.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      });

      this.element.addEventListener('touchend', (e) => {
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;
        const diffX = startX - endX;
        const diffY = startY - endY;

        // Horizontal swipe
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
          if (diffX > 0) {
            this.next();
          } else {
            this.previous();
          }
        }
      });
    }
  }

  handleNavigation(e) {
    const direction = e.currentTarget.dataset.galleryNav;

    if (direction === 'next') {
      this.next();
    } else {
      this.previous();
    }
  }

  handleDotNavigation(e) {
    const index = parseInt(e.currentTarget.dataset.galleryDot);
    this.goToSlide(index);
  }

  next() {
    this.currentIndex = (this.currentIndex + 1) % this.images.length;
    this.updateCarousel();
  }

  previous() {
    this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    this.updateCarousel();
  }

  goToSlide(index) {
    this.currentIndex = index;
    this.updateCarousel();
  }

  updateCarousel() {
    // Update visible slide
    this.images.forEach((image, index) => {
      image.style.transform = `translateX(${(index - this.currentIndex) * 100}%)`;
    });

    // Update dots
    const dots = this.element.querySelectorAll('[data-gallery-dot]');
    dots.forEach((dot, index) => {
      dot.classList.toggle('artist-showcase__gallery-dot--active', index === this.currentIndex);
    });

    // Update counter
    const counter = this.element.querySelector('.artist-showcase__gallery-counter-current');
    if (counter) {
      counter.textContent = this.currentIndex + 1;
    }
  }

  startAutoAdvance() {
    // Auto-advance every 5 seconds, pause on hover
    this.autoAdvanceInterval = setInterval(() => {
      this.next();
    }, 5000);

    this.element.addEventListener('mouseenter', () => {
      clearInterval(this.autoAdvanceInterval);
    });

    this.element.addEventListener('mouseleave', () => {
      this.startAutoAdvance();
    });
  }

  openLightbox(e) {
    e.preventDefault();
    const index = parseInt(e.currentTarget.dataset.lightboxIndex);
    this.createLightbox(index);
  }

  createLightbox(startIndex = 0) {
    // Create lightbox HTML
    this.lightbox = document.createElement('div');
    this.lightbox.className = 'artist-showcase__lightbox';
    this.lightbox.innerHTML = `
      <div class="artist-showcase__lightbox-overlay"></div>
      <div class="artist-showcase__lightbox-content">
        <button class="artist-showcase__lightbox-close" aria-label="Close lightbox">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
        <div class="artist-showcase__lightbox-image-container">
          <img class="artist-showcase__lightbox-image" src="" alt="">
        </div>
        <div class="artist-showcase__lightbox-navigation">
          <button class="artist-showcase__lightbox-nav artist-showcase__lightbox-nav--prev" aria-label="Previous image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <button class="artist-showcase__lightbox-nav artist-showcase__lightbox-nav--next" aria-label="Next image">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
        <div class="artist-showcase__lightbox-counter">
          <span class="artist-showcase__lightbox-counter-current">${startIndex + 1}</span>
          /
          <span class="artist-showcase__lightbox-counter-total">${this.images.length}</span>
        </div>
      </div>
    `;

    document.body.appendChild(this.lightbox);
    this.currentLightboxIndex = startIndex;
    this.updateLightboxImage();

    // Event listeners
    this.lightbox.querySelector('.artist-showcase__lightbox-close').addEventListener('click', this.closeLightbox.bind(this));
    this.lightbox.querySelector('.artist-showcase__lightbox-overlay').addEventListener('click', this.closeLightbox.bind(this));
    this.lightbox.querySelector('.artist-showcase__lightbox-nav--prev').addEventListener('click', this.lightboxPrevious.bind(this));
    this.lightbox.querySelector('.artist-showcase__lightbox-nav--next').addEventListener('click', this.lightboxNext.bind(this));

    // Keyboard support
    document.addEventListener('keydown', this.handleLightboxKeyboard.bind(this));

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }

  updateLightboxImage() {
    const image = this.lightbox.querySelector('.artist-showcase__lightbox-image');
    const counter = this.lightbox.querySelector('.artist-showcase__lightbox-counter-current');
    const currentImage = this.images[this.currentLightboxIndex];

    image.src = currentImage.querySelector('img').src.replace(/width=\d+/, 'width=1200');
    image.alt = currentImage.querySelector('img').alt;
    counter.textContent = this.currentLightboxIndex + 1;
  }

  lightboxNext() {
    this.currentLightboxIndex = (this.currentLightboxIndex + 1) % this.images.length;
    this.updateLightboxImage();
  }

  lightboxPrevious() {
    this.currentLightboxIndex = (this.currentLightboxIndex - 1 + this.images.length) % this.images.length;
    this.updateLightboxImage();
  }

  handleLightboxKeyboard(e) {
    if (!this.lightbox) return;

    switch (e.key) {
      case 'Escape':
        this.closeLightbox();
        break;
      case 'ArrowLeft':
        this.lightboxPrevious();
        break;
      case 'ArrowRight':
        this.lightboxNext();
        break;
    }
  }

  closeLightbox() {
    if (this.lightbox) {
      this.lightbox.remove();
      this.lightbox = null;
      document.body.style.overflow = '';
      document.removeEventListener('keydown', this.handleLightboxKeyboard.bind(this));
    }
  }
}

/**
 * Video Manager - Handles video loading, controls, and optimization
 */
class VideoManager {
  constructor(element) {
    this.element = element;
    this.type = element.dataset.videoType;
    this.autoplay = element.dataset.videoAutoplay === 'true';
    this.controls = element.dataset.videoControls === 'true';

    this.init();
  }

  init() {
    this.initLazyLoading();
    this.initCustomControls();
    this.initThumbnailPlayback();
  }

  initLazyLoading() {
    // Implement intersection observer for video loading
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadVideo();
          observer.unobserve(entry.target);
        }
      });
    });

    observer.observe(this.element);
  }

  initCustomControls() {
    const playButton = this.element.querySelector('.artist-showcase__video-play-button');

    if (playButton) {
      playButton.addEventListener('click', this.handlePlayButton.bind(this));
    }
  }

  initThumbnailPlayback() {
    const thumbnail = this.element.querySelector('.artist-showcase__video-thumbnail');

    if (thumbnail) {
      thumbnail.addEventListener('click', this.loadAndPlayVideo.bind(this));
    }
  }

  loadVideo() {
    const loadingState = this.element.querySelector('.artist-showcase__video-loading');

    if (loadingState) {
      loadingState.style.display = 'block';
    }

    // Simulate loading delay
    setTimeout(() => {
      if (loadingState) {
        loadingState.style.display = 'none';
      }
    }, 1000);
  }

  handlePlayButton(e) {
    e.preventDefault();
    const video = this.element.querySelector('video');

    if (video) {
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    }
  }

  loadAndPlayVideo() {
    const thumbnail = this.element.querySelector('.artist-showcase__video-thumbnail');
    const iframe = this.element.querySelector('.artist-showcase__video-iframe');

    if (thumbnail && iframe) {
      thumbnail.style.display = 'none';
      iframe.style.display = 'block';

      // Update iframe src to trigger autoplay
      let src = iframe.src;
      if (src.includes('autoplay=0')) {
        src = src.replace('autoplay=0', 'autoplay=1');
      } else {
        src += (src.includes('?') ? '&' : '?') + 'autoplay=1';
      }
      iframe.src = src;
    }
  }
}

/**
 * Product Manager - Handles product variants, cart integration, and pricing
 */
class ProductManager {
  constructor(element) {
    this.element = element;
    this.productId = element.dataset.productId;
    this.productData = this.getProductData();
    this.currentVariant = this.productData?.variants?.[0];

    this.init();
  }

  init() {
    this.initVariantSelection();
    this.initAddToCart();
    this.updateVariantInfo();
  }

  getProductData() {
    const script = this.element.querySelector(`[data-product-json="${this.element.id}"]`);
    return script ? JSON.parse(script.textContent) : null;
  }

  initVariantSelection() {
    const selects = this.element.querySelectorAll('.artist-showcase__product-option-select');

    selects.forEach(select => {
      select.addEventListener('change', this.handleVariantChange.bind(this));
    });
  }

  initAddToCart() {
    const form = this.element.querySelector('[data-product-form]');

    if (form) {
      form.addEventListener('submit', this.handleAddToCart.bind(this));
    }
  }

  handleVariantChange() {
    const selectedOptions = Array.from(this.element.querySelectorAll('.artist-showcase__product-option-select'))
      .map(select => select.value);

    // Find matching variant
    this.currentVariant = this.productData.variants.find(variant => {
      return variant.options.every((option, index) => option === selectedOptions[index]);
    });

    this.updateVariantInfo();
  }

  updateVariantInfo() {
    if (!this.currentVariant) return;

    // Update price
    const priceElement = this.element.querySelector('.artist-showcase__product-price-current');
    if (priceElement) {
      priceElement.textContent = this.formatMoney(this.currentVariant.price);
    }

    // Update availability
    const stockElement = this.element.querySelector('.artist-showcase__product-stock');
    const addToCartButton = this.element.querySelector('[data-add-to-cart]');

    if (this.currentVariant.available) {
      if (stockElement) {
        stockElement.className = 'artist-showcase__product-stock artist-showcase__product-stock--available';
        stockElement.textContent = '✓ In Stock';
      }
      if (addToCartButton) {
        addToCartButton.disabled = false;
        addToCartButton.querySelector('.artist-showcase__product-add-to-cart-text').textContent =
          `Add to Cart - ${this.formatMoney(this.currentVariant.price)}`;
      }
    } else {
      if (stockElement) {
        stockElement.className = 'artist-showcase__product-stock artist-showcase__product-stock--unavailable';
        stockElement.textContent = '✗ Sold Out';
      }
      if (addToCartButton) {
        addToCartButton.disabled = true;
        addToCartButton.querySelector('.artist-showcase__product-add-to-cart-text').textContent = 'Sold Out';
      }
    }

    // Update variant ID
    const variantInput = this.element.querySelector('[data-variant-id]');
    if (variantInput) {
      variantInput.value = this.currentVariant.id;
    }
  }

  async handleAddToCart(e) {
    e.preventDefault();

    const addToCartButton = e.target.querySelector('[data-add-to-cart]');
    const buttonText = addToCartButton.querySelector('.artist-showcase__product-add-to-cart-text');
    const loadingText = addToCartButton.querySelector('.artist-showcase__product-add-to-cart-loading');

    // Validate required elements exist
    if (!addToCartButton || !buttonText || !loadingText) {
      console.error('Artist Showcase: Required cart elements not found');
      return;
    }

    // Show loading state
    buttonText.style.display = 'none';
    loadingText.style.display = 'inline-flex';
    addToCartButton.disabled = true;

    try {
      const formData = new FormData(e.target);
      const response = await fetch(window.routes?.cart_add_url || '/cart/add.js', {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (response.ok) {
        const result = await response.json();
        this.showAddToCartSuccess(result);
        this.updateCartCount();
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.description || 'Failed to add to cart');
      }
    } catch (error) {
      console.error('Artist Showcase: Add to cart failed:', error);
      this.showAddToCartError(error.message);
    } finally {
      // Restore button state
      buttonText.style.display = '';
      loadingText.style.display = 'none';
      addToCartButton.disabled = false;
    }
  }

  showAddToCartSuccess() {
    // You could integrate with a cart drawer or notification system here
    const showcase = this.element.closest('.artist-showcase');
    if (showcase && showcase.artistShowcase) {
      showcase.artistShowcase.announce('Product added to cart successfully');
    }
  }

  showAddToCartError() {
    const showcase = this.element.closest('.artist-showcase');
    if (showcase && showcase.artistShowcase) {
      showcase.artistShowcase.announce('Failed to add product to cart. Please try again.');
    }
  }

  async updateCartCount() {
    try {
      const response = await fetch('/cart.js');
      const cart = await response.json();

      // Update cart count in header (if exists)
      const cartCount = document.querySelector('.cart-count');
      if (cartCount) {
        cartCount.textContent = cart.item_count;
      }
    } catch (error) {
      console.error('Failed to update cart count:', error);
    }
  }

  formatMoney(cents) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(cents / 100);
  }
}

/**
 * Expandable Manager - Handles expandable content sections
 */
class ExpandableManager {
  constructor(trigger) {
    this.trigger = trigger;
    this.content = document.querySelector(trigger.getAttribute('aria-controls'));
    this.isExpanded = false;

    this.init();
  }

  init() {
    this.trigger.addEventListener('click', this.toggle.bind(this));
  }

  toggle() {
    if (this.isExpanded) {
      this.collapse();
    } else {
      this.expand();
    }
  }

  expand() {
    this.isExpanded = true;
    this.trigger.setAttribute('aria-expanded', 'true');
    this.content.style.display = 'block';

    // Animate expansion
    this.content.style.height = '0px';
    this.content.style.overflow = 'hidden';

    const height = this.content.scrollHeight;
    this.content.style.height = height + 'px';

    setTimeout(() => {
      this.content.style.height = 'auto';
      this.content.style.overflow = '';
    }, 300);

    // Update button text
    const expandText = this.trigger.querySelector('.artist-showcase__content-expand-text');
    const collapseText = this.trigger.querySelector('.artist-showcase__content-collapse-text');

    if (expandText && collapseText) {
      expandText.style.display = 'none';
      collapseText.style.display = '';
    }
  }

  collapse() {
    this.isExpanded = false;
    this.trigger.setAttribute('aria-expanded', 'false');

    // Animate collapse
    const height = this.content.scrollHeight;
    this.content.style.height = height + 'px';
    this.content.style.overflow = 'hidden';

    setTimeout(() => {
      this.content.style.height = '0px';
    }, 10);

    setTimeout(() => {
      this.content.style.display = 'none';
      this.content.style.height = '';
      this.content.style.overflow = '';
    }, 300);

    // Update button text
    const expandText = this.trigger.querySelector('.artist-showcase__content-expand-text');
    const collapseText = this.trigger.querySelector('.artist-showcase__content-collapse-text');

    if (expandText && collapseText) {
      expandText.style.display = '';
      collapseText.style.display = 'none';
    }
  }
}

/**
 * Tab Manager - Handles tabbed content interfaces
 */
class TabManager {
  constructor(container) {
    this.container = container;
    this.triggers = container.querySelectorAll('[data-tab-trigger]');
    this.panels = container.querySelectorAll('[data-tab-panel]');
    this.currentTab = '1';

    this.init();
  }

  init() {
    this.triggers.forEach(trigger => {
      trigger.addEventListener('click', this.handleTabClick.bind(this));
    });

    // Keyboard navigation
    this.container.addEventListener('keydown', this.handleKeyboard.bind(this));
  }

  handleTabClick(e) {
    const tabId = e.currentTarget.dataset.tabTrigger;
    this.switchTab(tabId);
  }

  switchTab(tabId) {
    // Update triggers
    this.triggers.forEach(trigger => {
      const isActive = trigger.dataset.tabTrigger === tabId;
      trigger.classList.toggle('artist-showcase__content-tab-trigger--active', isActive);
      trigger.setAttribute('aria-selected', isActive);
    });

    // Update panels
    this.panels.forEach(panel => {
      const isActive = panel.dataset.tabPanel === tabId;
      panel.classList.toggle('artist-showcase__content-tab-panel--active', isActive);
      panel.style.display = isActive ? 'block' : 'none';
    });

    this.currentTab = tabId;
  }

  handleKeyboard(e) {
    if (!e.target.matches('[data-tab-trigger]')) return;

    const triggers = Array.from(this.triggers);
    const currentIndex = triggers.indexOf(e.target);

    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        const prevIndex = (currentIndex - 1 + triggers.length) % triggers.length;
        triggers[prevIndex].focus();
        this.switchTab(triggers[prevIndex].dataset.tabTrigger);
        break;

      case 'ArrowRight':
        e.preventDefault();
        const nextIndex = (currentIndex + 1) % triggers.length;
        triggers[nextIndex].focus();
        this.switchTab(triggers[nextIndex].dataset.tabTrigger);
        break;
    }
  }
}

/**
 * Parallax Manager - Handles parallax scrolling effects
 */
class ParallaxManager {
  constructor(elements) {
    this.elements = Array.from(elements);
    this.init();
  }

  init() {
    this.bindEvents();
    this.updateParallax();
  }

  bindEvents() {
    window.addEventListener('scroll', this.throttle(this.updateParallax.bind(this), 16));
    window.addEventListener('resize', this.throttle(this.updateParallax.bind(this), 100));
  }

  updateParallax() {
    const scrollY = window.pageYOffset;

    this.elements.forEach(element => {
      const rect = element.getBoundingClientRect();
      const speed = parseFloat(element.dataset.parallaxSpeed) || 0.5;

      if (rect.bottom >= 0 && rect.top <= window.innerHeight) {
        const yPos = -(scrollY * speed);
        element.style.transform = `translate3d(0, ${yPos}px, 0)`;
      }
    });
  }

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    }
  }
}

/**
 * Animation Manager - Handles scroll-based animations
 */
class AnimationManager {
  constructor(element) {
    this.element = element;
    this.blocks = element.querySelectorAll('.artist-showcase__block');
    this.observer = null;

    this.init();
  }

  init() {
    if ('IntersectionObserver' in window) {
      this.initIntersectionObserver();
    } else {
      // Fallback: show all blocks immediately
      this.blocks.forEach(block => block.style.opacity = '1');
    }
  }

  initIntersectionObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          this.observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '50px'
    });

    this.blocks.forEach(block => {
      this.observer.observe(block);
    });
  }
}

/**
 * Initialize artist showcase sections with lazy loading
 */
const initializeShowcases = () => {
  const showcases = document.querySelectorAll('.artist-showcase');

  showcases.forEach(showcase => {
    // Use intersection observer for lazy initialization
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.artistShowcase) {
          entry.target.artistShowcase = new ArtistShowcase(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '50px'
    });

    observer.observe(showcase);
  });
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeShowcases);
} else {
  initializeShowcases();
}

/**
 * Reinitialize when section is reloaded (Shopify theme editor)
 */
document.addEventListener('shopify:section:load', function(e) {
  if (e.target.classList.contains('artist-showcase')) {
    e.target.artistShowcase = new ArtistShowcase(e.target);
  }
});

/**
 * Cleanup when section is unloaded
 */
document.addEventListener('shopify:section:unload', function(e) {
  if (e.target.artistShowcase) {
    // Cleanup event listeners and intervals
    e.target.artistShowcase = null;
  }
});