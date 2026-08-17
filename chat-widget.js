/* ============================================================
   Ownerdeck — live chat widget

   Renders a floating launcher (bottom-right) and, if the page has a
   #od-live-chat mount, an inline panel there too (demo.html step 4).

   Cost/abuse controls live on the server (api/chat.js). The client-side
   caps here are UX, not security — never trust them.
============================================================ */
(function () {
  "use strict";

  var CFG = window.OD_CONFIG || {};
  var CHAT = CFG.liveChat || {};
  if (CHAT.enabled === false) return;

  var ENDPOINT   = CHAT.endpoint || '/api/chat';
  var SITE_KEY   = CHAT.turnstileSiteKey || '';
  var MAX_CHARS  = 500;
  var MAX_TURNS  = 12;

  /* Translation. i18n.js may not be on the page (demo.html has no switcher),
     so every call falls back to the English passed in. Static markup below
     carries data-i18n and is repainted by refresh(); text created later — the
     greeting, error replies — has to ask for a translation as it is built. */
  function T(key, en) {
    /* Register the English source as we go, so a line built while the visitor
       is on another language can still revert when they switch back to English
       (i18n.js only snapshots English it finds in the DOM). */
    if (key && window.OD_i18n && window.OD_i18n.note) window.OD_i18n.note(key, en);
    return (window.OD_i18n && window.OD_i18n.t(key, en)) || en;
  }
  function repaint() {
    if (window.OD_i18n) window.OD_i18n.refresh();
  }

  var history  = [];       // [{role, content}]
  var turns    = 0;
  var busy     = false;
  var widgetId = null;
  var waiting  = [];       // resolvers queued for the next token
  var unavailable = false; // Turnstile could not be rendered; stop waiting on it
  var tokenCache = '';     // a minted, unused token waiting for the next send
  var tokenAt    = 0;      // when it was minted
  var inflight   = null;   // the mint in progress, if any

  /* Cloudflare expires a token at 300s. Retiring ours early means a visitor
     who opens the panel and then takes a while to type still sends a token
     the server will accept, rather than one that just went stale. */
  var TOKEN_TTL = 240000;

  /* The server's stand-in for a passed check. While one is held, Turnstile is
     not asked for anything — which is the whole point: the visitor sees the
     challenge once, not before every message. */
  var pass = '';

  /* ---------- Turnstile (invisible human check) ----------
     A token is redeemed exactly once at siteverify and expires after a few
     minutes, so a fresh one is needed per message. Reusing the token issued
     at page load would get the second message rejected as
     timeout-or-duplicate.

     The token used to be minted when the visitor pressed send, which put a
     round-trip to Cloudflare — and on a cold cache the Turnstile script
     download too — in front of every single message, before the request to
     our own endpoint had even started. That was most of the wait people
     complained about.

     So it is minted ahead of time instead: once when the panel opens, and
     again immediately after each send. By the time anyone has typed a
     sentence the next token is already sitting in tokenCache, and the send
     path takes it without waiting for anything. */

  function settle(token) {
    var queued = waiting;
    waiting = [];
    queued.forEach(function (resolve) { resolve(token || ''); });
  }

  function loadTurnstile() {
    if (!SITE_KEY || widgetId !== null) return;
    if (window.turnstile) return renderTurnstile();
    if (document.getElementById('od-ts-script')) return;   // already in flight
    var s = document.createElement('script');
    s.id = 'od-ts-script';
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    s.async = true; s.defer = true;
    s.onload  = renderTurnstile;
    s.onerror = function () { settle(''); };
    document.head.appendChild(s);
  }

  function renderTurnstile() {
    var host = document.getElementById('od-turnstile');
    if (!host || !window.turnstile || widgetId !== null || unavailable) return;
    try {
      widgetId = window.turnstile.render(host, {
        sitekey: SITE_KEY,
        /* `size: 'invisible'` is not a valid value and made render() throw on
           every load — Turnstile accepts compact, flexible or normal. The way
           to ask for a check that only surfaces when Cloudflare wants one is
           appearance: 'interaction-only'. */
        appearance: 'interaction-only',
        action: 'chat-message',
        callback: function (t) { settle(t); },
        'error-callback': function () { settle(''); },
        'timeout-callback': function () { settle(''); }
      });
      if (waiting.length) window.turnstile.execute(widgetId);
    } catch (e) {
      /* Render failed, so nothing will ever call settle() again. Without this
         flag the first message resolved (the catch settles it) and every
         message after it sat in `waiting` with no one to resolve it, waiting
         out the full 20s timeout before the request was even sent. */
      unavailable = true;
      settle('');
    }
  }

  function tokenFresh() {
    return !!tokenCache && (Date.now() - tokenAt) < TOKEN_TTL;
  }

  /* One mint at a time. Two overlapping execute() calls on the same widget
     race, and whichever token loses is spent for nothing. */
  function mint() {
    if (inflight) return inflight;
    inflight = new Promise(function (resolve) {
      if (!SITE_KEY || unavailable) { inflight = null; return resolve(''); }
      var done = false;
      /* 20s was the old ceiling, and it was only survivable because nothing
         else was waiting on it. Now that minting happens in the background,
         a slow attempt should give up and let the next one try rather than
         hold a message hostage. */
      var timer = setTimeout(function () { finish(''); }, 5000);
      function finish(t) {
        if (done) return;
        done = true; clearTimeout(timer); inflight = null; resolve(t || '');
      }
      waiting.push(finish);
      loadTurnstile();
      if (widgetId !== null && window.turnstile) {
        try { window.turnstile.reset(widgetId); window.turnstile.execute(widgetId); }
        catch (e) { finish(''); }
      }
    });
    return inflight;
  }

  // Start one in the background. Safe to call whenever; it no-ops if a usable
  // token is already in hand or one is on its way.
  function prime() {
    if (pass) return;                 // already cleared; nothing to mint
    if (!SITE_KEY || unavailable || inflight || tokenFresh()) return;
    mint().then(function (t) {
      if (t) { tokenCache = t; tokenAt = Date.now(); }
    });
  }

  // Resolves with a fresh token, or '' if Turnstile can't produce one.
  // An empty token is not treated as permission — the server rejects it.
  function getToken() {
    if (pass) return Promise.resolve('');   // the pass speaks for us
    if (!SITE_KEY || unavailable) return Promise.resolve('');
    if (tokenFresh()) {
      var t = tokenCache;
      tokenCache = '';               // single use
      setTimeout(prime, 0);          // line up the next one straight away
      return Promise.resolve(t);
    }
    return mint().then(function (t) { setTimeout(prime, 0); return t; });
  }

  /* ---------- markup ---------- */
  function panelHTML(inline) {
    return '' +
      '<div class="odc-head">' +
        '<span class="odc-dot" aria-hidden="true"></span>' +
        '<div class="odc-title" data-i18n="k81b934cf">Ask Ownerdeck</div>' +
        (inline ? '' : '<button class="odc-x" type="button" aria-label="' + T('k726da9c1', 'Close chat') + '">&times;</button>') +
      '</div>' +
      '<div class="odc-log" id="odc-log' + (inline ? '-i' : '') + '" role="log" aria-live="polite"></div>' +
      /* The Turnstile host lives in the panel, in normal flow. It renders
         nothing at all until Cloudflare wants a challenge; when it does, the
         visitor can actually see and complete it. */
      '<div id="od-turnstile" class="odc-ts cf-turnstile" data-action="chat-message"></div>' +
      '<form class="odc-form" autocomplete="off">' +
        '<input class="odc-input" type="text" maxlength="' + MAX_CHARS + '" ' +
          'placeholder="' + T('k309d1a72', 'Ask about price, setup, languages…') + '" ' +
          'aria-label="' + T('kcfe1b4b7', 'Your message') + '">' +
        '<button class="odc-send" type="submit" aria-label="' + T('k94966d90', 'Send') + '">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>' +
        '</button>' +
      '</form>' +
      '<div class="odc-foot" data-i18n="k07fe50da">AI assistant · answers about Ownerdeck only</div>';
  }

  function bubble(log, who, text, key) {
    var d = document.createElement('div');
    d.className = 'odc-m odc-m--' + who;
    // Tagging our own canned lines lets them re-translate on a language
    // switch. Anything the model or the visitor wrote stays untagged: it is
    // already in the right language and must never be swapped out.
    if (key) d.setAttribute('data-i18n', key);
    d.textContent = text;
    log.appendChild(d);
    requestAnimationFrame(function () { log.scrollTop = log.scrollHeight; });
    return d;
  }
  function typing(log) {
    var d = document.createElement('div');
    d.className = 'odc-m odc-m--bot odc-typing';
    d.innerHTML = '<span></span><span></span><span></span>';
    log.appendChild(d);
    requestAnimationFrame(function () { log.scrollTop = log.scrollHeight; });
    return d;
  }

  /* ---------- streaming reply ----------
     The endpoint answers errors as JSON and successes as SSE, so the caller
     picks by content type. Tokens are appended to one bubble as they land,
     which is the whole point: the first words show up in about half a second
     instead of the visitor watching a typing dot until the model has finished
     composing the entire answer. */
  function readStream(r, dots, log) {
    var reader = r.body.getReader();
    var dec = new TextDecoder();
    var buf = '', full = '', node = null;

    function paint(chunk) {
      // Work out whether to follow the text down BEFORE it grows, otherwise
      // every measurement says "not at the bottom" and someone who scrolled
      // up to re-read gets yanked back on each token.
      var follow = log.scrollHeight - log.scrollTop - log.clientHeight < 60;
      if (!node) { dots.remove(); node = bubble(log, 'bot', ''); }
      full += chunk;
      node.textContent = full;
      if (follow) log.scrollTop = log.scrollHeight;
    }

    function pump() {
      return reader.read().then(function (res) {
        if (res.done) return done();
        buf += dec.decode(res.value, { stream: true });
        var frames = buf.split('\n\n');
        buf = frames.pop();          // trailing partial frame waits for more
        for (var i = 0; i < frames.length; i++) {
          var parts = frames[i].split('\n'), line = null;
          for (var k = 0; k < parts.length; k++) {
            if (parts[k].indexOf('data:') === 0) { line = parts[k]; break; }
          }
          if (!line) continue;
          var evt;
          try { evt = JSON.parse(line.slice(5)); } catch (e) { continue; }
          if (typeof evt.t === 'string') paint(evt.t);
          if (typeof evt.pass === 'string' && evt.pass) pass = evt.pass;
        }
        return pump();
      });
    }

    function done() {
      if (!node) {
        // Stream closed without a single token.
        dots.remove();
        full = T('k7e647227', 'Something went wrong. Email mark@ownerdeck.com and he will answer directly.');
        bubble(log, 'bot', full);
        return { ok: false, reply: full };
      }
      return { ok: true, reply: full };
    }

    return pump();
  }

  /* ---------- send ---------- */
  function wire(root, log) {
    var form  = root.querySelector('.odc-form');
    var input = root.querySelector('.odc-input');

    // First keystroke is the cue to get a token ready: early enough that the
    // send path never waits, late enough that opening the panel is quiet.
    input.addEventListener('input', function once() {
      input.removeEventListener('input', once);
      prime();
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = (input.value || '').trim();
      if (!text || busy) return;
      if (text.length > MAX_CHARS) text = text.slice(0, MAX_CHARS);
      if (turns >= MAX_TURNS) {
        bubble(log, 'bot', T('k7aa1c0db', "That's as far as the demo goes — email mark@ownerdeck.com and you'll get a straight answer about your own setup."), 'k7aa1c0db');
        return;
      }

      input.value = '';
      bubble(log, 'me', text);
      busy = true;
      var t = typing(log);

      getToken()
      .then(function (token) {
        return fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ message: text, history: history.slice(-8), turnstile: token, pass: pass })
        });
      })
      .then(function (r) {
        var ct = r.headers.get('content-type') || '';
        // Errors still come back as JSON with a real status code; so does any
        // browser too old for streaming bodies, because the server only
        // streams when it has something to stream.
        if (ct.indexOf('text/event-stream') === -1 || !r.body || !r.body.getReader) {
          return r.json().then(function (j) {
            t.remove();
            var reply = (j && j.reply) || T('k7e647227', 'Something went wrong. Email mark@ownerdeck.com and he will answer directly.');
            bubble(log, 'bot', reply);
            return { ok: r.ok, reply: reply };
          });
        }
        return readStream(r, t, log);
      })
      .then(function (out) {
        if (out && out.ok && out.reply) {
          history.push({ role: 'user', content: text });
          history.push({ role: 'assistant', content: out.reply });
          turns++;
        }
      })
      .catch(function () {
        t.remove();
        bubble(log, 'bot', T('k85721b54', 'Could not reach the assistant. Email mark@ownerdeck.com and he will answer directly.'), 'k85721b54');
      })
      .finally(function () { busy = false; prime(); });

      try { window.va && window.va('event', { name: 'chat_message' }); } catch (e) {}
    });
  }

  function greet(log) {
    if (log.childElementCount) return;
    bubble(log, 'bot', T('k3fc90439', "Hi — I'm an AI assistant, not a person. Ask me anything about Ownerdeck: what it costs, how setup works, whether it fits your business."), 'k3fc90439');
  }

  /* ---------- floating launcher ---------- */
  function mountFloating() {
    if (CHAT.floating === false) return;
    // Don't stack two chat UIs on one page — the demo mounts it inline.
    if (document.getElementById('od-live-chat')) return;
    var wrap = document.createElement('div');
    wrap.className = 'odc';
    wrap.innerHTML =
      '<button class="odc-launch" type="button" aria-label="' + T('kb0f90548','Open chat') + '" aria-expanded="false">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.8-.8L3 21l1.9-5a8.4 8.4 0 0 1 3.7-11.3 8.6 8.6 0 0 1 12.4 6.3Z"/></svg>' +
        '<span data-i18n="k69d9a05e">Ask a question</span>' +
      '</button>' +
      '<div class="odc-panel" role="dialog" aria-label="Ownerdeck chat" hidden>' + panelHTML(false) + '</div>';
    document.body.appendChild(wrap);

    var launch = wrap.querySelector('.odc-launch');
    var panel  = wrap.querySelector('.odc-panel');
    var log    = wrap.querySelector('#odc-log');

    /* Open and close are animated (chat-widget.css). The panel keeps its
       [hidden] attribute for accessibility and the no-JS case, but on close we
       hold the hide back until the exit animation has run so it is visible
       while it shrinks away. A single timer, cleared on re-open, prevents a
       fast close-then-open from hiding a panel that is open again. */
    var reduceMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // Must match the odcPanelOut duration in chat-widget.css. If this is the
    // shorter of the two the panel is hidden mid-flight and the close reads as
    // a snap; if it is longer, the panel sits there finished but still present.
    var EXIT_MS = reduceMotion ? 0 : 200;
    var closeTimer = null;

    function open(v) {
      launch.setAttribute('aria-expanded', v ? 'true' : 'false');
      if (v) {
        if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
        panel.classList.remove('odc-panel--out');
        panel.hidden = false;
        wrap.classList.remove('is-closing');
        wrap.classList.add('is-open');
        // Restart the entrance animation from the top on every open.
        panel.classList.remove('odc-panel--in');
        void panel.offsetWidth;
        panel.classList.add('odc-panel--in');
        greet(log); loadTurnstile();
        /* Deliberately not primed here. If Cloudflare wants an interactive
           challenge, minting on open drops a checkbox into the panel before
           the visitor has typed anything. Priming starts when they do. */
        setTimeout(function(){ var i=panel.querySelector('.odc-input'); i && i.focus(); }, 60);
      } else {
        if (panel.hidden) return;
        wrap.classList.remove('is-open');
        wrap.classList.add('is-closing');
        panel.classList.remove('odc-panel--in');
        panel.classList.add('odc-panel--out');
        closeTimer = setTimeout(function () {
          panel.hidden = true;
          panel.classList.remove('odc-panel--out');
          wrap.classList.remove('is-closing');
          closeTimer = null;
        }, EXIT_MS);
      }
    }
    launch.addEventListener('click', function () { open(panel.hidden); });
    panel.querySelector('.odc-x').addEventListener('click', function () { open(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) open(false); });

    wire(panel, log);
  }

  /* ---------- inline mount (demo step 4) ---------- */
  function mountInline() {
    var host = document.getElementById('od-live-chat');
    if (!host) return;
    host.className = 'odc-inline';
    host.innerHTML = panelHTML(true);   // panelHTML carries the Turnstile host
    var log = host.querySelector('#odc-log-i');
    greet(log);
    loadTurnstile();
    prime();
    wire(host, log);
  }

  /* Attributes were interpolated when the panel was built, before the
     language pack had loaded, so they need re-applying on every change. */
  function retranslate() {
    repaint();
    var ins = document.querySelectorAll('.odc-input');
    for (var n = 0; n < ins.length; n++) {
      ins[n].placeholder = T('k309d1a72', 'Ask about price, setup, languages…');
      ins[n].setAttribute('aria-label', T('kcfe1b4b7', 'Your message'));
    }
    var x = document.querySelector('.odc-x');
    if (x) x.setAttribute('aria-label', T('k726da9c1', 'Close chat'));
    var sd = document.querySelector('.odc-send');
    if (sd) sd.setAttribute('aria-label', T('k94966d90', 'Send'));
    var lz = document.querySelector('.odc-launch');
    if (lz) lz.setAttribute('aria-label', T('kb0f90548', 'Open chat'));
  }

  function init() {
    mountFloating();
    mountInline();
    retranslate();
    if (window.OD_i18n && window.OD_i18n.onChange) window.OD_i18n.onChange(retranslate);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
