document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#order-form');
  const status = document.querySelector('#form-status');
  if (!form) return;
  const previous = localStorage.getItem('midwestOrderDraft');
  if (previous && status) status.textContent = 'Previous request draft found on this device.';
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    localStorage.setItem('midwestOrderDraft', JSON.stringify({...data, savedAt: new Date().toISOString()}));
    if (status) status.textContent = 'Request draft saved. Backend delivery is the next integration step.';
  });
});
