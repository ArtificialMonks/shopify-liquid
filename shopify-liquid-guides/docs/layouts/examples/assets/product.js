/**
 * Product page JavaScript
 * Handles product variants, image gallery, and cart functionality
 */

(function() {
  'use strict';

  // Product namespace
  window.product = window.product || {};

  // Initialize product functionality
  product.init = function() {
    product.initVariantSelection();
    product.initImageGallery();
    product.initQuantitySelectors();
    product.initAddToCart();
  };

  // Variant selection functionality
  product.initVariantSelection = function() {
    const variantSelectors = document.querySelectorAll('.variant-selector select');

    variantSelectors.forEach(selector => {
      selector.addEventListener('change', function() {
        product.updateVariant();
      });
    });
  };

  // Update variant based on selected options
  product.updateVariant = function() {
    const form = document.querySelector('form[action*="/cart/add"]');
    if (!form) return;

    const selectors = form.querySelectorAll('.variant-selector select');
    const selectedOptions = Array.from(selectors).map(select => select.value);

    // Find matching variant (simplified - in real implementation you'd use product JSON)
    const variantIdInput = form.querySelector('input[name="id"]');
    if (variantIdInput && selectedOptions.length > 0) {
      // Update price, availability, etc. based on variant
      product.updatePrice();
      product.updateAvailability();
    }
  };

  // Update price display
  product.updatePrice = function() {
    const priceElement = document.querySelector('.product-price');
    if (priceElement) {
      // Price update logic would go here
      console.log('Price updated for variant');
    }
  };

  // Update availability display
  product.updateAvailability = function() {
    const availabilityElement = document.querySelector('.product-availability');
    if (availabilityElement) {
      // Availability update logic would go here
      console.log('Availability updated for variant');
    }
  };

  // Image gallery functionality
  product.initImageGallery = function() {
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.querySelector('.product-main-image img');
    const imageContainer = document.querySelector('.product-images');

    thumbnails.forEach(thumbnail => {
      thumbnail.addEventListener('click', function(e) {
        e.preventDefault();

        const newImageSrc = this.getAttribute('href') || this.querySelector('img').src;
        if (mainImage && newImageSrc) {
          mainImage.src = newImageSrc;

          // Update active thumbnail
          thumbnails.forEach(thumb => thumb.classList.remove('active'));
          this.classList.add('active');
        }
      });
    });

    // Initialize zoom functionality if container exists
    if (imageContainer) {
      product.initImageZoom();
    }
  };

  // Image zoom functionality
  product.initImageZoom = function() {
    const mainImage = document.querySelector('.product-main-image img');

    if (mainImage) {
      mainImage.addEventListener('mousemove', function(e) {
        // Zoom logic would go here
        const rect = this.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;

        this.style.transformOrigin = `${x}% ${y}%`;
      });

      mainImage.addEventListener('mouseleave', function() {
        this.style.transformOrigin = 'center';
      });
    }
  };

  // Quantity selector functionality
  product.initQuantitySelectors = function() {
    const quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(input => {
      const decreaseBtn = input.previousElementSibling;
      const increaseBtn = input.nextElementSibling;

      if (decreaseBtn && decreaseBtn.classList.contains('quantity-decrease')) {
        decreaseBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value) || 1;
          if (currentValue > 1) {
            input.value = currentValue - 1;
          }
        });
      }

      if (increaseBtn && increaseBtn.classList.contains('quantity-increase')) {
        increaseBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value) || 1;
          input.value = currentValue + 1;
        });
      }
    });
  };

  // Enhanced add to cart functionality
  product.initAddToCart = function() {
    const addToCartForms = document.querySelectorAll('form[action*="/cart/add"]');

    addToCartForms.forEach(form => {
      form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const submitBtn = form.querySelector('[type="submit"]');

        // Disable button and show loading
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Adding...';
        }

        fetch('/cart/add.js', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          // Show success message
          if (window.theme && window.theme.showNotification) {
            window.theme.showNotification('Product added to cart!');
          }

          // Update cart count if available
          product.updateCartCount();
        })
        .catch(error => {
          if (window.theme && window.theme.showNotification) {
            window.theme.showNotification('Error adding product to cart', 'error');
          }
        })
        .finally(() => {
          // Re-enable button
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add to Cart';
          }
        });
      });
    });
  };

  // Update cart count display
  product.updateCartCount = function() {
    fetch('/cart.js')
      .then(response => response.json())
      .then(cart => {
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(element => {
          element.textContent = cart.item_count;
        });
      })
      .catch(error => {
        console.error('Error updating cart count:', error);
      });
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', product.init);
  } else {
    product.init();
  }

})();