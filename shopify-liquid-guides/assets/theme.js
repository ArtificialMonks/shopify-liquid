/**
 * Main theme JavaScript file
 * Handles core theme functionality
 */

(function() {
  'use strict';

  // Theme namespace
  window.theme = window.theme || {};

  // Basic theme functionality
  theme.init = function() {
    console.log('Theme initialized');

    // Add to cart functionality
    theme.initAddToCart();

    // Mobile menu toggle
    theme.initMobileMenu();

    // Product image gallery
    theme.initProductGallery();
  };

  // Add to cart functionality
  theme.initAddToCart = function() {
    const addToCartForms = document.querySelectorAll('form[action*="/cart/add"]');

    addToCartForms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch('/cart/add.js', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          // Show success message
          theme.showNotification('Product added to cart!');
        })
        .catch(error => {
          theme.showNotification('Error adding product to cart', 'error');
        });
      });
    });
  };

  // Mobile menu toggle
  theme.initMobileMenu = function() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('is-open');
      });
    }
  };

  // Product image gallery
  theme.initProductGallery = function() {
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.querySelector('.product-main-image');

    thumbnails.forEach(function(thumbnail) {
      thumbnail.addEventListener('click', function(e) {
        e.preventDefault();

        const newSrc = thumbnail.getAttribute('href');
        if (mainImage && newSrc) {
          mainImage.src = newSrc;
        }
      });
    });
  };

  // Show notification
  theme.showNotification = function(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(function() {
      notification.remove();
    }, 3000);
  };

  // Initialize theme when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', theme.init);
  } else {
    theme.init();
  }

})();