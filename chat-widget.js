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

  var history = [];        // [{role, content}]
  var turns   = 0;
  var busy    = false;
  var tsToken = '';
  var tsReady = false;

  /* ---------- Turnstile (invisible human check) ---------- */
  function loadTurnstile(cb) {
    if (!SITE_KEY) { tsReady = true; return cb && cb(); }
    if (window.turnstile) return renderTurnstile(cb);
    var s = document.createElement('script');
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    s.async = true; s.defer = true;
    s.onload = function () { renderTurnstile(cb); };
    s.onerror = function () { tsReady = true; cb && cb(); };
    document.head.appendChild(s);
  }
  function renderTurnstile(cb) {
    var host = document.getElementById('od-turnstile');
    if (!host || !window.turnstile) { tsReady = true; return cb && cb(); }
    try {
      window.turnstile.render(host, {
        sitekey: SITE_KEY,
        size: 'invisible',
        callback: function (t) { tsToken = t; tsReady = true; cb && cb(); },
        'error-callback': function () { tsReady = true; cb && cb(); }
      });
      window.turnstile.execute(host);
    } catch (e) { tsReady = true; cb && cb(); }
  }
  function refreshToken() {
    if (!SITE_KEY || !window.turnstile) return;
    try { window.turnstile.reset(); window.turnstile.execute(document.getElementById('od-turnstile')); }
    catch (e) {}
  }

  /* ---------- markup ---------- */
  function panelHTML(inline) {
    return '' +
      '<div class="odc-head">' +
        '<span class="odc-dot" aria-hidden="true"></span>' +
        '<div class="odc-title">Ask Ownerdeck</div>' +
        (inline ? '' : '<button class="odc-x" type="button" aria-label="Close chat">&times;</button>') +
      '</div>' +
      '<div class="odc-log" id="odc-log' + (inline ? '-i' : '') + '" role="log" aria-live="polite"></div>' +
      '<form class="odc-form" autocomplete="off">' +
        '<input class="odc-input" type="text" maxlength="' + MAX_CHARS + '" ' +
          'placeholder="Ask about price, setup, languages…" aria-label="Your message">' +
        '<button class="odc-send" type="submit" aria-label="Send">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>' +
        '</button>' +
      '</form>' +
      '<div class="odc-foot">Demo assistant · answers about Ownerdeck only</div>';
  }

  function bubble(log, who, text) {
    var d = document.createElement('div');
    d.className = 'odc-m odc-m--' + who;
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

  /* ---------- send ---------- */
  function wire(root, log) {
    var form  = root.querySelector('.odc-form');
    var input = root.querySelector('.odc-input');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = (input.value || '').trim();
      if (!text || busy) return;
      if (text.length > MAX_CHARS) text = text.slice(0, MAX_CHARS);
      if (turns >= MAX_TURNS) {
        bubble(log, 'bot', "That's as far as the demo goes — email mark@ownerdeck.com and you'll get a straight answer about your own setup.");
        return;
      }

      input.value = '';
      bubble(log, 'me', text);
      busy = true;
      var t = typing(log);

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ message: text, history: history.slice(-12), turnstile: tsToken })
      })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (out) {
        t.remove();
        var reply = (out.j && out.j.reply) || 'Something went wrong. Email mark@ownerdeck.com and he will answer directly.';
        bubble(log, 'bot', reply);
        if (out.ok) {
          history.push({ role: 'user', content: text });
          history.push({ role: 'assistant', content: reply });
          turns++;
        }
        refreshToken();   // one-shot tokens
      })
      .catch(function () {
        t.remove();
        bubble(log, 'bot', 'Could not reach the assistant. Email mark@ownerdeck.com and he will answer directly.');
      })
      .finally(function () { busy = false; });

      try { window.va && window.va('event', { name: 'chat_message' }); } catch (e) {}
    });
  }

  function greet(log) {
    if (log.childElementCount) return;
    bubble(log, 'bot', "Hi — ask me anything about Ownerdeck. What it costs, how setup works, whether it fits your business.");
  }

  /* ---------- floating launcher ---------- */
  function mountFloating() {
    if (CHAT.floating === false) return;
    // Don't stack two chat UIs on one page — the demo mounts it inline.
    if (document.getElementById('od-live-chat')) return;
    var wrap = document.createElement('div');
    wrap.className = 'odc';
    wrap.innerHTML =
      '<button class="odc-launch" type="button" aria-label="Open chat" aria-expanded="false">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.8-.8L3 21l1.9-5a8.4 8.4 0 0 1 3.7-11.3 8.6 8.6 0 0 1 12.4 6.3Z"/></svg>' +
        '<span>Ask a question</span>' +
      '</button>' +
      '<div class="odc-panel" role="dialog" aria-label="Ownerdeck chat" hidden>' + panelHTML(false) + '</div>' +
      '<div id="od-turnstile" style="display:none"></div>';
    document.body.appendChild(wrap);

    var launch = wrap.querySelector('.odc-launch');
    var panel  = wrap.querySelector('.odc-panel');
    var log    = wrap.querySelector('#odc-log');

    function open(v) {
      panel.hidden = !v;
      wrap.classList.toggle('is-open', v);
      launch.setAttribute('aria-expanded', v ? 'true' : 'false');
      if (v) { greet(log); loadTurnstile(); setTimeout(function(){ var i=panel.querySelector('.odc-input'); i && i.focus(); }, 60); }
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
    host.innerHTML = panelHTML(true);
    if (!document.getElementById('od-turnstile')) {
      var t = document.createElement('div'); t.id = 'od-turnstile'; t.style.display = 'none';
      document.body.appendChild(t);
    }
    var log = host.querySelector('#odc-log-i');
    greet(log);
    loadTurnstile();
    wire(host, log);
  }

  function init() { mountFloating(); mountInline(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
