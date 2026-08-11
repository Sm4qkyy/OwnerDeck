/* ============================================================
   Ownerdeck — private pageview counter.

   Vercel Web Analytics already records traffic, but its data is only
   readable inside the Vercel dashboard. This keeps a parallel set of
   counters in the Redis we already run for chat rate limiting, so
   /stats.html can show numbers without a Vercel API token.

   Deliberately counts almost nothing: a path, a day, a referrer host, a
   country. No identifiers, no cookies, no per-visitor record. That keeps
   it outside the scope of anything requiring a consent banner and keeps
   the privacy policy true as written.
============================================================ */

const DAYS_KEPT = 90 * 24 * 3600;   // counters expire on their own

// Paths are attacker-controlled, so they are matched against what exists
// rather than used as keys directly. Otherwise a bot can mint unlimited
// Redis keys by requesting /?a=1, /?a=2, ... and quietly fill the database.
const KNOWN = new Set([
  '/', '/demo.html', '/privacy.html', '/terms.html',
  '/whatsapp-bot-car-rental.html',
  '/whatsapp-booking-bot-boat-charter-tours.html',
  '/stop-losing-bookings-slow-whatsapp-replies.html',
  '/whatsapp-auto-reply-vs-ai-assistant.html',
  '/do-i-need-a-new-number-whatsapp-bot.html'
]);

function redis() {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const tok = process.env.UPSTASH_REDIS_REST_TOKEN;
  if (!url || !tok) return null;
  return async function (cmd) {
    const r = await fetch(`${url}/pipeline`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${tok}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(cmd)
    });
    if (!r.ok) throw new Error('redis ' + r.status);
    return r.json();
  };
}

function today() { return new Date().toISOString().slice(0, 10); }

function refHost(ref) {
  if (!ref) return 'direct';
  try {
    const h = new URL(ref).hostname.replace(/^www\./, '');
    if (h.endsWith('ownerdeck.com')) return 'direct';   // internal navigation
    return h.slice(0, 40);
  } catch (e) { return 'direct'; }
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).end();
  }

  const allowed = process.env.ALLOWED_ORIGIN || 'https://www.ownerdeck.com';
  const origin = req.headers.origin || '';
  if (origin && !allowed.split(',').some(o => origin === o.trim())) return res.status(403).end();

  const run = redis();
  if (!run) return res.status(204).end();   // nothing configured: silently no-op

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};

  let path = typeof body.path === 'string' ? body.path.split('?')[0] : '/';
  if (!KNOWN.has(path)) path = 'other';
  const ref = refHost(typeof body.ref === 'string' ? body.ref : '');
  const country = (req.headers['cf-ipcountry'] || req.headers['x-vercel-ip-country'] || 'ZZ')
    .toString().slice(0, 2).toUpperCase();
  const d = today();

  try {
    await run([
      ['INCR', 'od:s:total'],
      ['INCR', `od:s:day:${d}`],       ['EXPIRE', `od:s:day:${d}`, DAYS_KEPT],
      ['HINCRBY', 'od:s:paths', path, 1],
      ['HINCRBY', 'od:s:refs', ref, 1],
      ['HINCRBY', 'od:s:countries', country, 1],
      ['HINCRBY', `od:s:pathday:${d}`, path, 1], ['EXPIRE', `od:s:pathday:${d}`, DAYS_KEPT]
    ]);
  } catch (e) {
    // A counter is never worth failing a pageview over.
    console.error('track_failed', e && e.message);
  }
  return res.status(204).end();
};
