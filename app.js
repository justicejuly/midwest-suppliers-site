document.addEventListener('DOMContentLoaded', () => {
  const selected = new Set();
  const products = document.querySelectorAll('.product');
  const cartSummary = document.querySelector('#cart-summary');
  const notes = document.querySelector('#notes');
  const form = document.querySelector('#order-form');
  const status = document.querySelector('#form-status');

  const updateCart = () => {
    const items = [...selected];
    if (!items.length) {
      cartSummary.textContent = 'Select items from the store to start.';
      return;
    }
    cartSummary.textContent = `Interested in: ${items.join(', ')}`;
    if (notes && !notes.value.trim()) {
      notes.value = `I am interested in: ${items.join(', ')}.`;
    }
  };

  products.forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.dataset.item;
      if (selected.has(item)) {
        selected.delete(item);
        button.classList.remove('selected');
      } else {
        selected.add(item);
        button.classList.add('selected');
      }
      updateCart();
    });
  });

  if (form) {
    const draft = localStorage.getItem('midwestSuppliersOrderRequest');
    if (draft && status) status.textContent = 'Saved request draft found on this device.';
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      data.items = [...selected];
      data.savedAt = new Date().toISOString();
      localStorage.setItem('midwestSuppliersOrderRequest', JSON.stringify(data));
      status.textContent = 'Order request saved. Share it with your Midwest Suppliers representative to confirm availability and delivery.';
    });
  }
});
