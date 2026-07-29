/* ============================================================
   Ownerdeck — site translation

   Keys are a hash of the English source text (see data-i18n in the
   markup). That means editing English copy changes its key, the lookup
   misses, and the element falls back to the English already in the DOM.
   A stale translation can never outlive the sentence it was made from.

   Language packs live in lang/<code>.json and are fetched on demand, so
   a visitor downloads one language, not six. Anything absent from a pack
   — prices, reference numbers, brand names, the Russian transcript —
   stays exactly as authored.

   el/ru/de/he/ar are machine-assisted. Have a native speaker read them
   before you lean on them commercially.
============================================================ */
(function () {
  "use strict";

  var LANGS = [
    { code: 'en', native: 'English',  dir: 'ltr' },
    { code: 'el', native: 'Ελληνικά', dir: 'ltr' },
    { code: 'ru', native: 'Русский',  dir: 'ltr' },
    { code: 'de', native: 'Deutsch',  dir: 'ltr' },
    { code: 'he', native: 'עברית',    dir: 'rtl' },
    { code: 'ar', native: 'العربية',  dir: 'rtl' }
  ];

  var STORE = 'od_lang';
  var packs = {};        // code -> dictionary
  var english = null;    // key -> original DOM text
  var current = 'en';

  function byCode(c) {
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i].code === c) return LANGS[i];
    return LANGS[0];
  }

  /* Snapshot the English in the markup once, before anything is replaced. */
  function captureEnglish() {
    if (english) return;
    english = {};
    var nodes = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < nodes.length; i++) {
      var k = nodes[i].getAttribute('data-i18n');
      if (!(k in english)) english[k] = nodes[i].textContent;
    }
  }

  function paint(dict) {
    var nodes = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < nodes.length; i++) {
      var k = nodes[i].getAttribute('data-i18n');
      var v = (dict && dict[k]) || english[k];
      if (v != null && nodes[i].textContent !== v) nodes[i].textContent = v;
    }
  }

  function apply(code) {
    var L = byCode(code);
    current = L.code;
    document.documentElement.setAttribute('lang', L.code);
    document.documentElement.setAttribute('dir', L.dir);
    paint(L.code === 'en' ? null : packs[L.code]);
    syncButton();
  }

  function load(code, done) {
    if (code === 'en' || packs[code]) return done();
    fetch('lang/' + code + '.json', { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { packs[code] = j; done(); })
      .catch(function () { done(); });   // stay on English rather than break
  }

  function set(code, remember) {
    load(code, function () {
      apply(code);
      if (remember) { try { localStorage.setItem(STORE, code); } catch (e) {} }
    });
  }

  /* ---------- switcher ---------- */
  var wrap, menu, btnLabel;

  function syncButton() {
    if (btnLabel) btnLabel.textContent = current.toUpperCase();
    if (!menu) return;
    var items = menu.querySelectorAll('[data-lang]');
    for (var i = 0; i < items.length; i++) {
      items[i].setAttribute('aria-checked',
        items[i].getAttribute('data-lang') === current ? 'true' : 'false');
    }
  }

  function openMenu(v) {
    menu.hidden = !v;
    wrap.querySelector('.od-lang-btn').setAttribute('aria-expanded', v ? 'true' : 'false');
  }

  function buildSwitcher() {
    var anchor = document.getElementById('theme-toggle');
    if (!anchor) return;

    wrap = document.createElement('div');
    wrap.className = 'od-lang';

    var html = '<button type="button" class="od-lang-btn" aria-haspopup="true" aria-expanded="false" aria-label="Change language">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true">' +
      '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/></svg>' +
      '<span class="od-lang-code">EN</span></button>' +
      '<div class="od-lang-menu" role="menu" hidden>';
    for (var i = 0; i < LANGS.length; i++) {
      html += '<button type="button" role="menuitemradio" aria-checked="false" data-lang="' +
        LANGS[i].code + '" lang="' + LANGS[i].code + '">' + LANGS[i].native + '</button>';
    }
    html += '</div>';
    wrap.innerHTML = html;

    anchor.parentNode.insertBefore(wrap, anchor);
    menu = wrap.querySelector('.od-lang-menu');
    btnLabel = wrap.querySelector('.od-lang-code');

    wrap.querySelector('.od-lang-btn').addEventListener('click', function (e) {
      e.stopPropagation();
      openMenu(menu.hidden);
    });
    menu.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('[data-lang]') : null;
      if (!b) return;
      set(b.getAttribute('data-lang'), true);
      openMenu(false);
    });
    document.addEventListener('click', function () { if (menu && !menu.hidden) openMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu && !menu.hidden) openMenu(false);
    });
  }

  /* ---------- first paint ---------- */
  function initial() {
    var saved = null;
    try { saved = localStorage.getItem(STORE); } catch (e) {}
    if (saved) return saved;
    var nav = (navigator.languages || [navigator.language || 'en']);
    for (var i = 0; i < nav.length; i++) {
      var two = String(nav[i]).slice(0, 2).toLowerCase();
      for (var j = 0; j < LANGS.length; j++) if (LANGS[j].code === two) return two;
    }
    return 'en';
  }

  function init() {
    captureEnglish();
    buildSwitcher();
    var start = initial();
    if (start !== 'en') set(start, false); else syncButton();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.OD_setLang = function (c) { set(c, true); };
})();
