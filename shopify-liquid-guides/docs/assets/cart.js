/**
 * Cart page JavaScript
 * Handles cart updates, quantity changes, and checkout functionality
 */

(function() {
  'use strict';

  // Cart namespace
  window.cart = window.cart || {};

  // Initialize cart functionality
  cart.init = function() {
    cart.initQuantityUpdates();
    cart.initItemRemoval();
    cart.initDiscountCode();
    cart.initShippingCalculator();
    cart.initCartNotes();
  };

  // Quantity update functionality
  cart.initQuantityUpdates = function() {
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');

    quantityInputs.forEach(input => {
      const decreaseBtn = input.parentElement.querySelector('.quantity-decrease');
      const increaseBtn = input.parentElement.querySelector('.quantity-increase');

      // Decrease quantity
      if (decreaseBtn) {
        decreaseBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value) || 0;
          if (currentValue > 0) {
            cart.updateQuantity(input, currentValue - 1);
          }
        });
      }

      // Increase quantity
      if (increaseBtn) {
        increaseBtn.addEventListener('click', function() {
          const currentValue = parseInt(input.value) || 0;
          cart.updateQuantity(input, currentValue + 1);
        });
      }

      // Direct input change
      input.addEventListener('change', function() {
        const newValue = parseInt(this.value) || 0;
        cart.updateQuantity(this, newValue);
      });
    });
  };

  // Update item quantity
  cart.updateQuantity = function(input, quantity) {
    const itemKey = input.getAttribute('data-key');
    if (!itemKey) return;

    const lineItem = input.closest('.cart-item');
    if (lineItem) {
      lineItem.classList.add('updating');
    }

    const formData = new FormData();
    formData.append('updates[' + itemKey + ']', quantity);

    fetch('/cart/update.js', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(cart => {
      if (quantity === 0) {
        cart.removeLineItem(lineItem);
      } else {
        cart.updateLineItem(lineItem, cart);
      }
      cart.updateCartTotals(cart);
    })
    .catch(error => {
      console.error('Error updating cart:', error);
      if (window.theme && window.theme.showNotification) {
        window.theme.showNotification('Error updating cart', 'error');
      }
    })
    .finally(() => {
      if (lineItem) {
        lineItem.classList.remove('updating');
      }
    });
  };

  // Remove line item from DOM
  cart.removeLineItem = function(lineItem) {
    if (lineItem) {
      lineItem.style.opacity = '0';
      setTimeout(() => {
        lineItem.remove();
        cart.checkEmptyCart();
      }, 300);
    }
  };

  // Update line item display
  cart.updateLineItem = function(lineItem, cartData) {
    const itemKey = lineItem.getAttribute('data-key');
    const item = cartData.items.find(item => item.key === itemKey);

    if (item && lineItem) {
      // Update price
      const priceElement = lineItem.querySelector('.line-item-price');
      if (priceElement) {
        priceElement.textContent = cart.formatMoney(item.line_price);
      }

      // Update quantity input
      const quantityInput = lineItem.querySelector('.cart-quantity-input');
      if (quantityInput && quantityInput.value != item.quantity) {
        quantityInput.value = item.quantity;
      }
    }
  };

  // Update cart totals
  cart.updateCartTotals = function(cartData) {
    // Update subtotal
    const subtotalElements = document.querySelectorAll('.cart-subtotal');
    subtotalElements.forEach(element => {
      element.textContent = cart.formatMoney(cartData.total_price);
    });

    // Update item count
    const itemCountElements = document.querySelectorAll('.cart-item-count');
    itemCountElements.forEach(element => {
      element.textContent = cartData.item_count;
    });
  };

  // Item removal functionality
  cart.initItemRemoval = function() {
    const removeButtons = document.querySelectorAll('.cart-remove-item');

    removeButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();

        const itemKey = this.getAttribute('data-key');
        const lineItem = this.closest('.cart-item');

        if (confirm('Remove this item from your cart?')) {
          cart.updateQuantity(lineItem.querySelector('.cart-quantity-input'), 0);
        }
      });
    });
  };

  // Check if cart is empty and show appropriate message
  cart.checkEmptyCart = function() {
    const cartItems = document.querySelectorAll('.cart-item');
    const emptyCartMessage = document.querySelector('.cart-empty');
    const cartContents = document.querySelector('.cart-contents');

    if (cartItems.length === 0) {
      if (emptyCartMessage) emptyCartMessage.style.display = 'block';
      if (cartContents) cartContents.style.display = 'none';
    }
  };

  // Discount code functionality
  cart.initDiscountCode = function() {
    const discountForm = document.querySelector('.discount-form');

    if (discountForm) {
      discountForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const discountCode = this.querySelector('input[name="discount"]').value;
        const submitBtn = this.querySelector('[type="submit"]');

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Applying...';
        }

        // Redirect to checkout with discount code
        window.location.href = `/checkout?discount=${encodeURIComponent(discountCode)}`;
      });
    }
  };

  // Shipping calculator functionality
  cart.initShippingCalculator = function() {
    const shippingForm = document.querySelector('.shipping-calculator');

    if (shippingForm) {
      shippingForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const country = this.querySelector('select[name="country"]').value;
        const province = this.querySelector('select[name="province"]').value;
        const zip = this.querySelector('input[name="zip"]').value;

        cart.calculateShipping(country, province, zip);
      });
    }
  };

  // Calculate shipping rates
  cart.calculateShipping = function(country, province, zip) {
    const shippingResults = document.querySelector('.shipping-results');

    if (shippingResults) {
      shippingResults.innerHTML = '<div class="loading">Calculating shipping...</div>';
    }

    fetch('/cart/shipping_rates.json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        shipping_address: {
          country: country,
          province: province,
          zip: zip
        }
      })
    })
    .then(response => response.json())
    .then(data => {
      cart.displayShippingRates(data.shipping_rates);
    })
    .catch(error => {
      console.error('Error calculating shipping:', error);
      if (shippingResults) {
        shippingResults.innerHTML = '<div class="error">Unable to calculate shipping</div>';
      }
    });
  };

  // Display shipping rates
  cart.displayShippingRates = function(rates) {
    const shippingResults = document.querySelector('.shipping-results');

    if (!shippingResults || !rates) return;

    if (rates.length === 0) {
      shippingResults.innerHTML = '<div class="no-rates">No shipping rates available</div>';
      return;
    }

    let html = '<div class="shipping-rates"><h4>Available shipping rates:</h4><ul>';
    rates.forEach(rate => {
      html += `<li>${rate.name}: ${cart.formatMoney(rate.price)}</li>`;
    });
    html += '</ul></div>';

    shippingResults.innerHTML = html;
  };

  // Cart notes functionality
  cart.initCartNotes = function() {
    const notesTextarea = document.querySelector('textarea[name="note"]');

    if (notesTextarea) {
      let timeout;

      notesTextarea.addEventListener('input', function() {
        clearTimeout(timeout);

        timeout = setTimeout(() => {
          cart.updateCartNote(this.value);
        }, 1000); // Debounce for 1 second
      });
    }
  };

  // Update cart note
  cart.updateCartNote = function(note) {
    const formData = new FormData();
    formData.append('note', note);

    fetch('/cart/update.js', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .catch(error => {
      console.error('Error updating cart note:', error);
    });
  };

  // Format money helper
  cart.formatMoney = function(cents) {
    const dollars = (cents / 100).toFixed(2);
    return `$${dollars}`;
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', cart.init);
  } else {
    cart.init();
  }

})();