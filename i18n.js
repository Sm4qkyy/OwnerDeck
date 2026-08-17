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

   el/ru are machine-assisted. Have a native speaker read them before you
   lean on them commercially.
============================================================ */
(function () {
  "use strict";

  /* Only languages that are actually translated end to end belong here.
     A code in this list that has no pack silently serves English, which is a
     promise the visitor breaks by clicking it. de, pt, he and ar were removed
     for that reason; their packs are still on disk, so adding a market back is
     re-adding a line here once the pack is complete. */
  var LANGS = [
    { code: 'en', native: 'English',  dir: 'ltr' },
    { code: 'el', native: 'Ελληνικά', dir: 'ltr' },
    { code: 'ru', native: 'Русский',  dir: 'ltr' }
  ];

  var STORE = 'od_lang';
  var packs = {};        // code -> dictionary
  var english = null;    // key -> original DOM text
  var current = 'en';
  var listeners = [];    // notified after every language change

  function byCode(c) {
    for (var i = 0; i < LANGS.length; i++) if (LANGS[i].code === c) return LANGS[i];
    return LANGS[0];
  }

  /* Snapshot the English in the markup, before anything is replaced. Safe to
     call more than once: a key is captured the first time its node is seen and
     never overwritten, so nodes that appear later — the chat widget builds its
     panel after this file runs — get their English recorded too, while a key
     already captured is left untouched even if its node now shows a
     translation. Without this, dynamically added nodes had no English to
     revert to and stayed stuck in the last language on the switch back. */
  function captureEnglish() {
    if (!english) english = {};
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
    for (var i = 0; i < listeners.length; i++) {
      try { listeners[i](L.code); } catch (e) {}
    }
  }

  function load(code, done) {
    if (code === 'en' || packs[code]) return done();
    /* Absolute. The site is multi-page now, so a relative path would resolve
       against whichever sub-page is open. */
    fetch('/lang/' + code + '.json', { cache: 'no-store' })
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

    /* Where this lives depends on the width. On a phone the header pill has
       to hold the wordmark and three 44px controls, and it cannot; the
       language control is the one anybody touches least, so it goes into
       the menu with the navigation. Above 48rem it sits in the header as
       before. Moved rather than duplicated — two switchers would be two
       things to keep in sync. */
    var narrow = window.matchMedia('(max-width: 48rem)');

    function place() {
      var panel = document.querySelector('.mmenu__panel');
      if (narrow.matches && panel) {
        if (wrap.parentNode !== panel) panel.appendChild(wrap);
        wrap.classList.add('od-lang--in-menu');
      } else {
        if (wrap.parentNode !== anchor.parentNode) anchor.parentNode.insertBefore(wrap, anchor);
        wrap.classList.remove('od-lang--in-menu');
      }
    }
    place();
    if (narrow.addEventListener) narrow.addEventListener('change', place);
    else if (narrow.addListener) narrow.addListener(place);
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

  /* Public API, for UI that JavaScript builds after this file has run — the
     chat widget in particular. Static nodes it creates can carry data-i18n and
     will be picked up by refresh(); text created later (a greeting, an error)
     has to ask for a translation directly via t(). */
  window.OD_i18n = {
    lang: function () { return current; },
    t: function (key, fallbackText) {
      var d = packs[current];
      return (d && d[key]) || fallbackText;
    },
    refresh: function () {
      captureEnglish();
      paint(current === 'en' ? null : packs[current]);
    },
    /* Record the English source for a key whose text is built in JavaScript
       rather than written in the markup — a chat greeting, an error reply.
       captureEnglish() only sees the DOM, so text that is created already
       translated (opening the chat while on Greek) would otherwise be missing
       its English and could not revert. Register it at build time, from the
       English fallback the caller already holds, and the switch back to
       English has something to paint. First writer wins, so a later Greek
       render never overwrites it. */
    note: function (key, en) {
      if (key == null || en == null) return;
      if (!english) english = {};
      if (!(key in english)) english[key] = en;
    },
    onChange: function (fn) { listeners.push(fn); }
  };

  window.OD_setLang = function (c) { set(c, true); };
})();
