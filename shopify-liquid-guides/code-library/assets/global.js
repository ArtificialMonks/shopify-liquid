/**
 * global.js - Essential global JavaScript for Shopify themes
 * Provides basic functionality expected by theme.liquid layout
 */

// Basic theme utilities
class Theme {
  constructor() {
    this.initializeBasicFunctionality();
    this.setupCartDrawer();
    this.setupMobileNavigation();
  }

  initializeBasicFunctionality() {
    // Handle no-js class removal (already done in theme.liquid)
    document.documentElement.classList.remove('no-js');

    // Basic accessibility improvements
    this.setupSkipLinks();
    this.setupFocusManagement();
  }

  setupSkipLinks() {
    const skipLinks = document.querySelectorAll('.skip-to-content-link');
    skipLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
          target.focus();
        }
      });
    });
  }

  setupFocusManagement() {
    // Basic focus management for better accessibility
    const mainContent = document.getElementById('MainContent');
    if (mainContent) {
      mainContent.setAttribute('tabindex', '-1');
    }
  }

  setupCartDrawer() {
    // Placeholder for cart drawer functionality
    // Individual sections will handle their own cart interactions
    console.log('Cart functionality initialized');
  }

  setupMobileNavigation() {
    // Placeholder for mobile navigation
    // Header sections will handle their own navigation logic
    console.log('Mobile navigation initialized');
  }
}

// Initialize theme when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new Theme();
});

// Shopify design mode helpers
if (Shopify.designMode) {
  document.addEventListener('shopify:section:load', () => {
    // Reinitialize any JavaScript when sections are reloaded in the theme editor
    console.log('Section reloaded in theme editor');
  });
}