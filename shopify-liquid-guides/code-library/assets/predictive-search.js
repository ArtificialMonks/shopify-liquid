/**
 * predictive-search.js - Shopify predictive search functionality
 * Provides search-as-you-type functionality for the theme
 */

class PredictiveSearch {
  constructor() {
    this.searchInput = document.querySelector('input[name="q"]');
    this.searchResults = document.querySelector('[data-predictive-search]');
    this.searchForm = document.querySelector('form[action*="/search"]');

    if (!this.searchInput) return;

    this.setupSearch();
  }

  setupSearch() {
    this.searchInput.addEventListener('input', this.debounce(this.onSearchInput.bind(this), 300));
    this.searchInput.addEventListener('keydown', this.onKeyDown.bind(this));

    // Close search results when clicking outside
    document.addEventListener('click', (e) => {
      if (!this.searchForm?.contains(e.target)) {
        this.hideResults();
      }
    });
  }

  async onSearchInput(event) {
    const query = event.target.value.trim();

    if (query.length < 2) {
      this.hideResults();
      return;
    }

    try {
      const response = await fetch(`${window.routes.predictive_search_url}?q=${encodeURIComponent(query)}&resources[type]=product,page,article&resources[limit]=6&section_id=predictive-search`);

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      const resultsHtml = await response.text();
      this.displayResults(resultsHtml);
    } catch (error) {
      console.error('Predictive search error:', error);
      this.hideResults();
    }
  }

  displayResults(html) {
    if (!this.searchResults) {
      this.createResultsContainer();
    }

    this.searchResults.innerHTML = html;
    this.searchResults.style.display = 'block';
    this.searchResults.setAttribute('aria-hidden', 'false');
  }

  hideResults() {
    if (this.searchResults) {
      this.searchResults.style.display = 'none';
      this.searchResults.setAttribute('aria-hidden', 'true');
    }
  }

  createResultsContainer() {
    const container = document.createElement('div');
    container.setAttribute('data-predictive-search', '');
    container.style.position = 'absolute';
    container.style.top = '100%';
    container.style.left = '0';
    container.style.right = '0';
    container.style.background = 'rgb(var(--color-base-background-1))';
    container.style.border = '1px solid rgba(var(--color-base-text), 0.2)';
    container.style.borderTop = 'none';
    container.style.zIndex = '999';
    container.style.display = 'none';
    container.setAttribute('aria-hidden', 'true');

    if (this.searchForm) {
      this.searchForm.style.position = 'relative';
      this.searchForm.appendChild(container);
      this.searchResults = container;
    }
  }

  onKeyDown(event) {
    // Handle keyboard navigation
    switch (event.code) {
      case 'Escape':
        this.hideResults();
        break;
      case 'ArrowDown':
        event.preventDefault();
        this.navigateResults('down');
        break;
      case 'ArrowUp':
        event.preventDefault();
        this.navigateResults('up');
        break;
      case 'Enter':
        if (this.selectedResult) {
          event.preventDefault();
          this.selectedResult.click();
        }
        break;
    }
  }

  navigateResults(direction) {
    if (!this.searchResults) return;

    const results = this.searchResults.querySelectorAll('a, button');
    if (results.length === 0) return;

    let currentIndex = Array.from(results).findIndex(result => result === this.selectedResult);

    if (direction === 'down') {
      currentIndex = currentIndex < results.length - 1 ? currentIndex + 1 : 0;
    } else {
      currentIndex = currentIndex > 0 ? currentIndex - 1 : results.length - 1;
    }

    if (this.selectedResult) {
      this.selectedResult.classList.remove('selected');
    }

    this.selectedResult = results[currentIndex];
    this.selectedResult.classList.add('selected');
    this.selectedResult.focus();
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

// Initialize predictive search when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new PredictiveSearch();
});

// Reinitialize when sections are reloaded in theme editor
if (Shopify.designMode) {
  document.addEventListener('shopify:section:load', () => {
    new PredictiveSearch();
  });
}