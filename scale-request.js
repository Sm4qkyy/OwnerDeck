// =================================================================
//  OwnerDeck — Scale Request Page
// =================================================================
//  Handles the async form submission to FormSubmit and swaps the
//  form card for the confirmation state on success.
// =================================================================

const FORM_ENDPOINT = 'https://formsubmit.co/ajax/ownerdeck@outlook.com';

const form      = document.getElementById('scale-form');
const submitBtn = document.getElementById('sr-submit-btn');
const formWrap  = document.getElementById('sr-form-wrap');
const confirm   = document.getElementById('sr-confirm');

if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();

    const originalHTML = submitBtn.innerHTML;
    submitBtn.classList.add('loading');
    submitBtn.innerHTML = 'Sending…';

    const data = Object.fromEntries(new FormData(form));
    data._subject  = `OwnerDeck Scale request — ${data.company || 'new lead'} (${data.property_count || '?'} properties)`;
    data._template = 'table';
    data._captcha  = 'false';

    try {
      const res = await fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!res.ok) throw new Error('Submission failed');

      // Hide form, show confirmation
      formWrap.hidden = true;
      confirm.hidden  = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });

    } catch (err) {
      console.error(err);
      submitBtn.classList.remove('loading');
      submitBtn.innerHTML = originalHTML;
      alert(
        "Something went wrong sending your request. " +
        "Please email ownerdeck@outlook.com directly and we'll get back to you within 24 hours."
      );
    }
  });
}
