/* ============================================================
   Ownerdeck — refundable deposit

   Creates a Stripe Checkout Session and hands back its URL. The browser then
   navigates to Stripe's own hosted page.

   Why redirect-mode Checkout rather than Stripe.js or Elements:
   · No card data ever touches this origin, so nothing here is in PCI scope.
   · No third-party script on the site, so the Content-Security-Policy needs
     no new script-src entry. The only network call from the page is a POST to
     this endpoint, which connect-src 'self' already allows, and the hop to
     Stripe is a top-level navigation that CSP does not govern.
   · Nothing to keep in step when Stripe changes their client library.

   The secret key lives only in the Vercel environment. It is never sent to
   the browser and must never be committed.
============================================================ */

const AMOUNT_CENTS = 7500;          // EUR 75
const CURRENCY = 'eur';

/* Accept the names Stripe's own docs use, plus the shorter one people tend to
   type into a dashboard. Checked in order so an explicit STRIPE_SECRET_KEY
   always wins. */
function secretKey() {
  return process.env.STRIPE_SECRET_KEY ||
         process.env.STRIPE_SECRET ||
         process.env.STRIPE_API_KEY || '';
}

function form(obj, prefix, out) {
  out = out || [];
  for (const k of Object.keys(obj)) {
    const v = obj[k];
    if (v === undefined || v === null || v === '') continue;
    const key = prefix ? `${prefix}[${k}]` : k;
    if (typeof v === 'object') form(v, key, out);
    else out.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(v))}`);
  }
  return out;
}

function clean(s, max) {
  return String(s == null ? '' : s).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max);
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method' });
  }

  // Same-origin only. This endpoint spends money on Stripe's side by creating
  // sessions, so it should not be callable from anywhere else.
  const allowed = process.env.ALLOWED_ORIGIN || 'https://www.ownerdeck.com';
  const origin = req.headers.origin || '';
  if (origin && origin !== allowed && !/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin)) {
    return res.status(403).json({ error: 'origin' });
  }

  const key = secretKey();
  if (!key) {
    // Not an error the visitor caused. The flow treats this as "deposit not
    // available" and falls back to the WhatsApp handoff.
    return res.status(503).json({ error: 'unconfigured' });
  }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  const trade = clean(body.trade, 80);
  const plan = clean(body.plan, 60);
  const note = clean(body.note, 400);

  const base = (origin && /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin))
    ? origin : allowed;

  const payload = form({
    mode: 'payment',
    'payment_method_types[0]': 'card',
    success_url: `${base}/start?deposit=paid&s={CHECKOUT_SESSION_ID}`,
    cancel_url: `${base}/start?deposit=cancelled`,
    'line_items[0][quantity]': 1,
    'line_items[0][price_data][currency]': CURRENCY,
    'line_items[0][price_data][unit_amount]': AMOUNT_CENTS,
    'line_items[0][price_data][product_data][name]': 'Ownerdeck holding deposit',
    'line_items[0][price_data][product_data][description]':
      'Refundable in full until work starts. Credited against your build fee.',
    // Metadata is what makes the Stripe dashboard readable: the payment arrives
    // already saying which business it came from and what they picked.
    'metadata[trade]': trade,
    'metadata[plan]': plan,
    'metadata[note]': note,
    'metadata[source]': 'start-flow',
  }).join('&');

  try {
    const r = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${key}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        // Stripe replays a repeated key instead of charging twice, which
        // matters if a double tap fires two requests.
        'Idempotency-Key': `od-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`,
      },
      body: payload,
    });

    const data = await r.json();
    if (!r.ok || !data.url) {
      console.error('stripe session failed', r.status, data && data.error && data.error.message);
      return res.status(502).json({ error: 'upstream' });
    }
    return res.status(200).json({ url: data.url });
  } catch (e) {
    console.error('stripe request threw', e && e.message);
    return res.status(502).json({ error: 'upstream' });
  }
};
