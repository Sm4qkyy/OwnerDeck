// =================================================================
//  OwnerDeck — Preview Wizard
// =================================================================
//  This script runs the 3-step interactive preview flow.
//
//  IMPORTANT: form submission goes to FormSubmit (https://formsubmit.co)
//  using ownerdeck@outlook.com. The first time anyone submits the form,
//  FormSubmit will email ownerdeck@outlook.com asking you to confirm
//  ownership of that address. Click the confirm link in that email
//  (one-time setup) and all future submissions will arrive in your inbox.
//
//  When you have a Stripe Payment Link, replace STRIPE_PAYMENT_LINK_HERE
//  in preview.html (Step 3, "Skip the wait — subscribe now" button).
// =================================================================

const FORM_ENDPOINT = 'https://formsubmit.co/ajax/ownerdeck@outlook.com';

const $ = sel => document.querySelector(sel);
const $$ = sel => document.querySelectorAll(sel);

// ---- Step nav ----------------------------------------------------
function showStep(n) {
  $$('.preview-step').forEach(s => s.classList.remove('active'));
  $('#step-' + n).classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ---- Helpers -----------------------------------------------------
function fillDynamic(field, value) {
  $$('.dynamic-' + field).forEach(el => { el.textContent = value; });
}

function applyBranding(data) {
  const company = (data.company || 'Your Company').trim();
  const color   = data.color || '#C97B3F';
  const property = (data.property || 'Villa Aphrodite').trim();
  const owner    = (data.owner    || 'Maria Constantinou').trim();

  document.documentElement.style.setProperty('--user-color', color);
  fillDynamic('company',  company);
  fillDynamic('property', property);
  fillDynamic('owner',    owner);

  // Populate hidden fields for the unlock form
  $('#hidden-company').value  = company;
  $('#hidden-color').value    = color;
  $('#hidden-property').value = property;
  $('#hidden-owner').value    = owner;
}

// ---- Step 1: live color hex display ------------------------------
const colorInput = $('#color');
const colorHex   = $('#color-hex');
if (colorInput && colorHex) {
  colorInput.addEventListener('input', () => {
    colorHex.textContent = colorInput.value.toUpperCase();
  });
}

// ---- Step 1: branding form ---------------------------------------
$('#branding-form').addEventListener('submit', e => {
  e.preventDefault();
  const fd = new FormData(e.target);
  applyBranding({
    company:  fd.get('company'),
    color:    fd.get('color'),
    property: fd.get('property'),
    owner:    fd.get('owner'),
  });
  showStep(2);
});

// ---- Step 2: unlock form (Formsubmit AJAX) -----------------------
$('#unlock-form').addEventListener('submit', async e => {
  e.preventDefault();
  const form = e.target;
  const submitBtn = $('#unlock-submit');
  const originalText = submitBtn.innerHTML;

  submitBtn.classList.add('loading');
  submitBtn.innerHTML = 'Sending…';

  const data = Object.fromEntries(new FormData(form));
  data._subject  = `OwnerDeck preview request — ${data.company || 'new lead'}`;
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
    showStep(3);
  } catch (err) {
    console.error(err);
    submitBtn.classList.remove('loading');
    submitBtn.innerHTML = originalText;
    alert(
      "Something went wrong sending your preview request. " +
      "Please email ownerdeck@outlook.com and we'll handle it manually."
    );
  }
});

// ---- Restart -----------------------------------------------------
const restartBtn = $('#restart');
if (restartBtn) {
  restartBtn.addEventListener('click', () => {
    showStep(1);
  });
}

// ---- Hide the Stripe button if the placeholder hasn't been filled
// -----------------------------------------------------------------
const stripeBtn = $('#stripe-subscribe');
if (stripeBtn && stripeBtn.href.includes('STRIPE_PAYMENT_LINK_HERE')) {
  stripeBtn.style.display = 'none';
}
