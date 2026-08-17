/* Drives the real Turnstile token cache out of chat-widget.js. The token is
   single-use and time-limited, and it is now minted ahead of the send rather
   than during it — three properties that fail silently if they regress
   (a spent token reads as "could not verify you are human", a stale one the
   same, and a lost pre-mint just makes the chat slow again). */
const fs = require('path');
const src = require('fs').readFileSync(require('path').join(__dirname, 'chat-widget.js'), 'utf8');

function slice(from, to) {
  const a = src.indexOf(from);
  const b = src.indexOf(to, a);
  if (a < 0 || b < 0) { console.error(`  FAIL: cannot find ${from}`); process.exit(1); }
  return src.slice(a, b);
}

// The real code, lifted verbatim.
const body = slice('  function settle(token)', '  function loadTurnstile()') +
             slice('  function tokenFresh()', '  /* ---------- markup ----------');

// Everything the block reaches for that lives elsewhere in the widget.
const PREAMBLE = `
  var SITE_KEY = 'test-key';
  var unavailable = false;
  var widgetId = 1;
  var waiting = [];
  var tokenCache = '', tokenAt = 0, inflight = null;
  var TOKEN_TTL = 240000;
  var pass = '';
  var minted = 0;
  var window = { turnstile: {
    reset: function () {},
    execute: function () {
      // Cloudflare answers asynchronously, as it does in a browser.
      setTimeout(function () { settle('tok' + (++minted)); }, delay);
    }
  }};
  function loadTurnstile() {}
`;
const EXPORTS = `
  return { getToken: getToken, prime: prime, tokenFresh: tokenFresh,
           stats: function () { return { minted: minted, cache: tokenCache, inflight: !!inflight }; },
           expire: function () { tokenAt = Date.now() - TOKEN_TTL - 1; },
           setPass: function (v) { pass = v; },
           setUnavailable: function (v) { unavailable = v; } };
`;
const build = (delay) => new Function('delay', PREAMBLE + body + EXPORTS)(delay);

const wait = (ms) => new Promise(r => setTimeout(r, ms));
let pass = true;
function check(name, cond, extra) {
  if (!cond) { pass = false; console.log(`  FAIL  ${name}${extra ? '  ' + extra : ''}`); }
  else console.log(`  PASS  ${name}`);
}

(async () => {
  // 1. priming means the send path does not wait
  let m = build(30);
  m.prime();
  await wait(60);
  check('prime() fills the cache before any send', m.tokenFresh(), JSON.stringify(m.stats()));

  const t0 = Date.now();
  const tok = await m.getToken();
  check('cached token returns immediately', Date.now() - t0 < 10 && tok === 'tok1', `${Date.now() - t0}ms ${tok}`);

  // 2. single use — the cache must be empty straight after
  check('token is spent once taken', m.stats().cache === '', JSON.stringify(m.stats()));
  await wait(60);
  check('next token is minted in the background', m.tokenFresh() && m.stats().minted === 2,
        JSON.stringify(m.stats()));

  const second = await m.getToken();
  check('second send gets a different token', second === 'tok2', second);

  // 3. a stale token is not offered
  m = build(30);
  m.prime(); await wait(60);
  m.expire();
  check('expired token is not considered fresh', !m.tokenFresh());
  const fresh = await m.getToken();
  check('expired token triggers a new mint', fresh === 'tok2', fresh);

  // 4. overlapping calls must not race two executes
  m = build(40);
  m.prime(); m.prime(); m.prime();
  const both = await Promise.all([m.getToken(), m.getToken()]);
  check('concurrent callers share one mint', m.stats().minted === 1, JSON.stringify(m.stats()));
  check('no caller is left without a token', both[0] === 'tok1' && both[1] === 'tok1', JSON.stringify(both));

  // 5. Turnstile unavailable resolves empty rather than hanging
  m = build(30);
  m.setUnavailable(true);
  const t1 = Date.now();
  const none = await m.getToken();
  check('unavailable resolves empty at once', none === '' && Date.now() - t1 < 10, `${none} ${Date.now() - t1}ms`);

  /* 6. Holding a pass must stop Turnstile being touched at all. This is what
     keeps the checkbox from reappearing before every message — if either of
     these regresses, the visitor is challenged again and again. */
  m = build(30);
  m.setPass('exp.tag.sig');
  m.prime(); await wait(60);
  check('a held pass suppresses priming', m.stats().minted === 0, JSON.stringify(m.stats()));
  const withPass = await m.getToken();
  check('a held pass sends no token', withPass === '' && m.stats().minted === 0, JSON.stringify(m.stats()));

  // 7. a Turnstile that never answers gives up, and well short of the old 20s
  m = build(999999);
  const t2 = Date.now();
  await m.getToken();
  const waited = Date.now() - t2;
  check('a dead Turnstile gives up near 5s', waited >= 4900 && waited < 6000, `${waited}ms`);

  console.log(pass ? '\n  all token tests passed' : '\n  FAILURES');
  process.exit(pass ? 0 : 1);
})();
