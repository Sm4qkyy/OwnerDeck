/* ============================================================
   Ownerdeck — password-gated stats reader.

   The important property: stats.html contains no numbers. It is an empty
   shell. Everything comes from here, and this refuses to answer without a
   valid session, so finding the URL gets you a login box and nothing else.
   A password checked in browser JavaScript would be decoration — anyone can
   read the page source — so the check happens only on the server.

   Env vars (Vercel → Settings → Environments → Production):
     STATS_PASSWORD   the password. Never in the repo, never in a response.
     STATS_SECRET     any long random string, used to sign session tokens.
                      If unset, a value derived from STATS_PASSWORD is used,
                      which means changing the password invalidates sessions.

   With STATS_PASSWORD unset the endpoint returns 503 and the page stays
   locked, so this ships inert rather than open.
============================================================ */

const crypto = require('crypto');

const SESSION_HOURS   = 12;
const MAX_LOGIN_TRIES = 8;      // per IP…
const LOGIN_WINDOW    = 900;    // …per 15 minutes

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

function ipOf(req) {
  const h = req.headers || {};
  return (h['cf-connecting-ip'] || (h['x-forwarded-for'] || '').split(',')[0].trim() ||
          h['x-real-ip'] || 'unknown');
}

function secret() {
  return process.env.STATS_SECRET ||
         crypto.createHash('sha256').update('od|' + (process.env.STATS_PASSWORD || '')).digest('hex');
}

/* Constant-time compare. A plain === leaks the position of the first wrong
   character through timing, which is enough to guess a password one letter
   at a time given sufficient attempts. */
function sameSecret(a, b) {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  if (x.length !== y.length) {
    // Still burn a comparison so length is not signalled by returning early.
    crypto.timingSafeEqual(x, x);
    return false;
  }
  return crypto.timingSafeEqual(x, y);
}

function issue() {
  const exp = Date.now() + SESSION_HOURS * 3600 * 1000;
  const sig = crypto.createHmac('sha256', secret()).update(String(exp)).digest('hex');
  return `${exp}.${sig}`;
}

function valid(token) {
  if (typeof token !== 'string' || token.indexOf('.') < 0) return false;
  const [exp, sig] = token.split('.');
  if (!/^\d+$/.test(exp) || Number(exp) < Date.now()) return false;
  const want = crypto.createHmac('sha256', secret()).update(exp).digest('hex');
  return sameSecret(sig, want);
}

function lastNDays(n) {
  const out = [];
  for (let i = n - 1; i >= 0; i--) {
    out.push(new Date(Date.now() - i * 86400000).toISOString().slice(0, 10));
  }
  return out;
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');

  if (!process.env.STATS_PASSWORD) {
    return res.status(503).json({ error: 'not_configured' });
  }

  const allowed = process.env.ALLOWED_ORIGIN || 'https://www.ownerdeck.com';
  const origin = req.headers.origin || '';
  if (origin && !allowed.split(',').some(o => origin === o.trim())) {
    return res.status(403).json({ error: 'bad_origin' });
  }

  const run = redis();
  const ip = ipOf(req);

  /* ---------- login ---------- */
  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
    body = body || {};

    // Throttle guessing. Without this a 12-character password is still
    // reachable by a script that never gets tired.
    if (run) {
      try {
        const key = `od:st:try:${ip}`;
        const out = await run([['INCR', key], ['EXPIRE', key, LOGIN_WINDOW]]);
        const tries = Number((out[0] || {}).result || 0);
        if (tries > MAX_LOGIN_TRIES) {
          return res.status(429).json({ error: 'too_many', message: 'Too many attempts. Try again in 15 minutes.' });
        }
      } catch (e) { /* throttle unavailable; the password check still stands */ }
    }

    if (!sameSecret(body.password || '', process.env.STATS_PASSWORD)) {
      return res.status(401).json({ error: 'bad_password' });
    }
    return res.status(200).json({ token: issue(), hours: SESSION_HOURS });
  }

  /* ---------- read ---------- */
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const auth = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!valid(auth)) return res.status(401).json({ error: 'unauthorized' });

  if (!run) return res.status(200).json({ ready: false, reason: 'no_redis' });

  const days = lastNDays(30);
  try {
    const cmd = [
      ['GET', 'od:s:total'],
      ['HGETALL', 'od:s:paths'],
      ['HGETALL', 'od:s:refs'],
      ['HGETALL', 'od:s:countries']
    ].concat(days.map(d => ['GET', `od:s:day:${d}`]));

    const out = await run(cmd);
    const val = i => (out[i] || {}).result;

    const toObj = r => {
      // Upstash returns HGETALL as a flat array or an object depending on path
      if (!r) return {};
      if (Array.isArray(r)) {
        const o = {};
        for (let i = 0; i < r.length; i += 2) o[r[i]] = Number(r[i + 1]) || 0;
        return o;
      }
      const o = {};
      Object.keys(r).forEach(k => { o[k] = Number(r[k]) || 0; });
      return o;
    };

    const daily = days.map((d, i) => ({ date: d, views: Number(val(4 + i)) || 0 }));
    const total = Number(val(0)) || 0;
    const sum = n => daily.slice(-n).reduce((a, b) => a + b.views, 0);

    return res.status(200).json({
      ready: true,
      total,
      today: daily[daily.length - 1].views,
      last7: sum(7),
      last30: sum(30),
      daily,
      paths: toObj(val(1)),
      refs: toObj(val(2)),
      countries: toObj(val(3))
    });
  } catch (e) {
    console.error('stats_read_failed', e && e.message);
    return res.status(500).json({ error: 'read_failed' });
  }
};
