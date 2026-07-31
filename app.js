document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#order-form');
  const status = document.querySelector('#form-status');
  if (!form) return;

  const draft = localStorage.getItem('midwestSuppliersOrderRequest');
  if (draft && status) status.textContent = 'Saved request draft found on this device.';

  form.addEventListener('submit', () => {
    const data = Object.fromEntries(new FormData(form).entries());
    data.savedAt = new Date().toISOString();
    localStorage.setItem('midwestSuppliersOrderRequest', JSON.stringify(data));
    if (status) status.textContent = 'Sending your request to Midwest Suppliers...';
  });
});
