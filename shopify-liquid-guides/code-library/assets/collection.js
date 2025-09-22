/**
 * Collection page JavaScript
 * Handles filtering, sorting, and pagination
 */

(function() {
  'use strict';

  // Collection namespace
  window.collection = window.collection || {};

  // Initialize collection functionality
  collection.init = function() {
    collection.initFilters();
    collection.initSorting();
    collection.initInfiniteScroll();
  };

  // Filter functionality
  collection.initFilters = function() {
    const filterButtons = document.querySelectorAll('[data-filter]');
    const productGrid = document.querySelector('.collection-grid');

    filterButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();

        const filterValue = this.getAttribute('data-filter');

        // Update active filter
        filterButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');

        // Filter products
        const products = productGrid.querySelectorAll('.product-card');
        products.forEach(product => {
          if (filterValue === 'all' || product.classList.contains(filterValue)) {
            product.style.display = 'block';
          } else {
            product.style.display = 'none';
          }
        });
      });
    });
  };

  // Sorting functionality
  collection.initSorting = function() {
    const sortSelect = document.querySelector('#sort-by');

    if (sortSelect) {
      sortSelect.addEventListener('change', function() {
        const sortValue = this.value;
        const url = new URL(window.location);
        url.searchParams.set('sort_by', sortValue);
        window.location.href = url.toString();
      });
    }
  };

  // Infinite scroll for large collections
  collection.initInfiniteScroll = function() {
    const loadMoreBtn = document.querySelector('.load-more');

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', function(e) {
        e.preventDefault();

        const nextUrl = this.getAttribute('href');
        if (nextUrl) {
          collection.loadMoreProducts(nextUrl);
        }
      });
    }
  };

  // Load more products via AJAX
  collection.loadMoreProducts = function(url) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newProducts = doc.querySelectorAll('.product-card');
        const productGrid = document.querySelector('.collection-grid');

        newProducts.forEach(product => {
          productGrid.appendChild(product);
        });

        // Update load more button
        const newLoadMore = doc.querySelector('.load-more');
        const currentLoadMore = document.querySelector('.load-more');

        if (newLoadMore) {
          currentLoadMore.setAttribute('href', newLoadMore.getAttribute('href'));
        } else {
          currentLoadMore.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error loading more products:', error);
      });
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', collection.init);
  } else {
    collection.init();
  }

})();