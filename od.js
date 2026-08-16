/* ==========================================================================
   Ownerdeck — od.js

   Everything in this file is decoration or convenience. Delete it and the
   site is still complete, navigable and readable: the reveal rules in od.css
   are scoped to the .js class that the inline bootstrap in <head> adds, the
   menus are <details> elements that work unscripted, and links are ordinary
   links.

   prefers-reduced-motion removes the motion without removing the behaviour.
   ========================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;

  /* ---- Theme -----------------------------------------------------------
     The stored value is read in the inline <head> script, not here, so the
     page paints in the right theme the first time. This only handles the
     click. */
  (function theme() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;

    function current() {
      return root.getAttribute('data-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }

    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('od_theme', next); } catch (e) {}
      btn.setAttribute('aria-label',
        next === 'dark' ? 'Switch to the light theme' : 'Switch to the dark theme');
    });
  })();

  /* ---- Menus -----------------------------------------------------------
     Both the mobile menu and the language menu are open/closed by the
     browser. All that is added here is closing them on Escape, on a click
     elsewhere, and after following a link. */
  (function menus() {
    var mmenu = document.querySelector('.mmenu');
    if (!mmenu) return;

    mmenu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { mmenu.removeAttribute('open'); });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mmenu.hasAttribute('open')) {
        mmenu.removeAttribute('open');
        var s = mmenu.querySelector('summary');
        if (s) s.focus();
      }
    });

    document.addEventListener('click', function (e) {
      if (mmenu.hasAttribute('open') && !mmenu.contains(e.target)) {
        mmenu.removeAttribute('open');
      }
    });
  })();

  /* ---- Header state ----------------------------------------------------
     One scroll listener for the whole page, and it only ever toggles a
     class inside a rAF callback. */
  (function header() {
    var bar = document.querySelector('.masthead');
    // The hero's ambient cards ride the same loop. One scroll listener for the
    // page, one rAF, one place where anything reads scrollY — adding a second
    // listener for the parallax is how you end up with two handlers fighting
    // over the same frame.
    var floaters = [];
    if (!reduce && window.matchMedia('(min-width: 62rem)').matches) {
      floaters = Array.prototype.map.call(
        document.querySelectorAll('.floater'),
        function (el) { return { el: el, depth: parseFloat(el.getAttribute('data-depth')) || 0 }; });
    }
    if (!bar && !floaters.length) return;
    var ticking = false;

    function update() {
      ticking = false;
      var y = window.scrollY || window.pageYOffset;
      if (bar) bar.classList.toggle('is-stuck', y > 6);
      for (var i = 0; i < floaters.length; i++) {
        // Capped so a long scroll cannot drag a card halfway down the page.
        var shift = Math.max(-160, Math.min(160, y * floaters[i].depth));
        floaters[i].el.style.setProperty('--shift', shift.toFixed(1) + 'px');
      }
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  })();

  /* ---- Reveals ---------------------------------------------------------
     Siblings that come into view together are staggered, so a row of cards
     arrives as a row rather than four separate events. */
  (function reveals() {
    var items = document.querySelectorAll('[data-reveal]');
    if (!items.length) return;

    if (reduce || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var explicit = el.getAttribute('data-reveal');
        var delay;

        if (explicit) {
          delay = parseInt(explicit, 10) || 0;
        } else {
          var sibs = el.parentElement
            ? el.parentElement.querySelectorAll(':scope > [data-reveal]')
            : [el];
          delay = Math.min(Math.max(0, Array.prototype.indexOf.call(sibs, el)), 6) * 70;
        }

        el.style.transitionDelay = delay + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  })();

  /* ---- Page transitions ------------------------------------------------
     The site is multi-page, so without this every link is a white flash.
     main already fades in via a keyframe in od.css; this adds the matching
     fade out.

     Guarded hard, because getting this wrong breaks navigation itself:
     plain left-clicks only, same origin only, and never for downloads, new
     tabs, hash links or anything with a modifier held. The pageshow reset
     matters for the back button — a bfcache restore replays the DOM exactly
     as it was left, faded out, unless the class is cleared. */
  (function transitions() {
    if (reduce || !window.history || !window.matchMedia('(pointer: fine)').matches) return;

    var leaving = false;

    window.addEventListener('pageshow', function () {
      leaving = false;
      root.classList.remove('is-leaving');
    });

    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var a = e.target.closest ? e.target.closest('a') : null;
      if (!a || !a.href) return;
      if (a.target && a.target !== '_self') return;
      if (a.hasAttribute('download')) return;
      if (a.getAttribute('href').charAt(0) === '#') return;

      var url;
      try { url = new URL(a.href); } catch (err) { return; }
      if (url.origin !== window.location.origin) return;
      if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
      // Same page, different hash — let the browser scroll.
      if (url.pathname === window.location.pathname && url.hash) return;

      e.preventDefault();
      if (leaving) return;
      leaving = true;
      root.classList.add('is-leaving');

      // Navigate on the transition's own event, with a timer as the backstop
      // in case the element is not composited and the event never fires.
      var done = false;
      function go() {
        if (done) return;
        done = true;
        window.location.href = a.href;
      }
      var main = document.querySelector('main');
      if (main) main.addEventListener('transitionend', go, { once: true });
      setTimeout(go, 260);
    });
  })();

  /* ---- Current page in the nav ----------------------------------------
     Written here rather than by hand in eight files, so a renamed page
     cannot leave a stale highlight behind. */
  (function currentPage() {
    var here = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    if (here.length > 1 && here.charAt(here.length - 1) === '/') here = here.slice(0, -1);
    if (here === '') here = '/';

    document.querySelectorAll('.masthead__nav a, .mmenu__panel a').forEach(function (a) {
      var path = a.getAttribute('href') || '';
      if (path.charAt(0) !== '/') return;
      path = path.split('#')[0].replace(/\.html$/, '');
      if (path.length > 1 && path.charAt(path.length - 1) === '/') path = path.slice(0, -1);
      if (path === '') path = '/';
      if (path === here) a.setAttribute('aria-current', 'page');
    });
  })();
})();
