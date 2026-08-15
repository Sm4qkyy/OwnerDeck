/* ============================================================
   Ownerdeck — motion, theme and menu

   No dependencies, no build step. The effects here were rebuilt by
   hand rather than pulled from a React component library, because the
   site has no framework and adding one to get a hover effect is a bad
   trade.

   Three rules this file keeps:

   1. Motion is decoration. The page is complete and readable with this
      file deleted, with JavaScript blocked, and for anyone who has asked
      their system for less movement.
   2. Nothing that tracks the pointer may read layout during the move.
      getBoundingClientRect() in a pointermove handler forces a reflow on
      every event; rects are measured on enter and on resize instead.
   3. Nothing that tracks the pointer may transition the property it is
      setting. A 300ms ease fighting a 120Hz pointer is what "choppy"
      actually is.

   Colours are read from brand.css at runtime. Nothing here declares one.
   ============================================================ */
(function () {
  "use strict";

  var mqReduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  var reduce   = mqReduce ? mqReduce.matches : false;
  var fine     = window.matchMedia ? matchMedia('(pointer: fine)').matches : false;

  /* ---------------------------------------------------------------- THEME */
  /* The pre-paint half of this runs inline in <head>; without it the page
     would flash light before switching. This half is only the button. */
  function theme() {
    var btn = document.getElementById('theme-toggle');
    if (!btn) return;
    var root = document.documentElement;

    function current() {
      var set = root.getAttribute('data-theme');
      if (set) return set;
      return (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches)
        ? 'dark' : 'light';
    }
    function label() {
      var next = current() === 'dark' ? 'light' : 'dark';
      btn.setAttribute('aria-label', 'Switch to ' + next + ' mode');
      btn.setAttribute('title', 'Switch to ' + next + ' mode');
    }
    label();

    btn.addEventListener('click', function () {
      var next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('od_theme', next); } catch (e) {}
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) {
        meta.setAttribute('content',
          getComputedStyle(root).getPropertyValue('--bone').trim());
      }
      label();
    });
  }

  /* ----------------------------------------------------------- MOBILE MENU */
  /* <details> already opens, closes and takes focus on its own. This only
     closes it on navigation and on Escape, which <details> does not do. */
  function menu() {
    var m = document.querySelector('.mmenu');
    if (!m) return;
    m.addEventListener('click', function (e) {
      if (e.target.closest('a')) m.removeAttribute('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && m.hasAttribute('open')) {
        m.removeAttribute('open');
        var s = m.querySelector('summary');
        if (s) s.focus();
      }
    });
  }

  /* ------------------------------------------------------------ DOT FIELD */
  /* A halftone grid in clay on bone that leans away from the pointer.
     Printed rather than sci-fi, which is the whole brief in one effect.
     Canvas, because a thousand DOM nodes would not survive a scroll. */
  function dotField(host) {
    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    canvas.className = 'dotfield__canvas';
    host.appendChild(canvas);

    var ctx = canvas.getContext('2d', { alpha: true });
    var dots = [], w = 0, h = 0, rect = null;
    var GAP = 26, RADIUS = 130, PULL = 11;
    var raf = 0, running = false, visible = true;
    var px = -9999, py = -9999, pointerIn = false;
    var clay = getComputedStyle(document.documentElement)
                 .getPropertyValue('--clay').trim() || '#C4643C';

    function measure() {
      rect = host.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);  // retina x3 is wasted here
      w = rect.width; h = rect.height;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      dots.length = 0;
      for (var i = 0; i * GAP <= w + GAP; i++) {
        for (var j = 0; j * GAP <= h + GAP; j++) {
          dots.push({ x: i * GAP, y: j * GAP, ox: 0, oy: 0, a: 0 });
        }
      }
    }

    /* Returns true while anything is still moving, so the loop can idle out
       instead of burning frames on a field that has already settled. */
    function frame() {
      ctx.clearRect(0, 0, w, h);
      var moving = false;

      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var dx = d.x - px, dy = d.y - py;
        var dist = Math.sqrt(dx * dx + dy * dy);
        var near = (pointerIn && dist < RADIUS) ? 1 - dist / RADIUS : 0;
        near *= near;                                   // ease the falloff

        var tx = near ? (dx / (dist || 1)) * near * PULL : 0;
        var ty = near ? (dy / (dist || 1)) * near * PULL : 0;
        d.ox += (tx - d.ox) * 0.14;
        d.oy += (ty - d.oy) * 0.14;
        d.a  += (near - d.a) * 0.14;

        if (Math.abs(tx - d.ox) > 0.05 || Math.abs(ty - d.oy) > 0.05 ||
            Math.abs(near - d.a) > 0.004) moving = true;

        ctx.globalAlpha = 0.15 + d.a * 0.5;
        ctx.fillStyle = clay;
        ctx.beginPath();
        ctx.arc(d.x + d.ox, d.y + d.oy, 1 + d.a * 1.5, 0, 6.2832);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      return moving;
    }

    function loop() {
      var moving = frame();
      if (moving && visible) { raf = requestAnimationFrame(loop); }
      else { running = false; }         // settled: stop cleanly, restart on demand
    }
    function kick() {
      if (!running && visible) { running = true; raf = requestAnimationFrame(loop); }
    }
    function halt() { running = false; cancelAnimationFrame(raf); }

    measure();
    frame();                            // one static frame, for everyone

    if (reduce || !fine) return;        // touch and reduced-motion end here

    // Rect is cached; pointermove never reads layout.
    host.addEventListener('pointerenter', function () { rect = host.getBoundingClientRect(); });
    host.addEventListener('pointermove', function (e) {
      if (!rect) rect = host.getBoundingClientRect();
      px = e.clientX - rect.left;
      py = e.clientY - rect.top;
      pointerIn = true;
      kick();
    }, { passive: true });
    host.addEventListener('pointerleave', function () {
      pointerIn = false;                // the loop eases home and idles by itself
      kick();
    });

    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (!visible) halt(); else if (pointerIn) kick();
      }, { threshold: 0 }).observe(host);
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) halt();
    });

    var t;
    addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(function () { measure(); frame(); }, 150);
    }, { passive: true });

    addEventListener('scroll', function () { rect = null; }, { passive: true });
  }

  /* --------------------------------------------------------------- REVEALS */
  function reveals() {
    var nodes = document.querySelectorAll('[data-reveal]');
    if (!nodes.length) return;
    if (reduce || !window.IntersectionObserver) {
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.add('is-in');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        el.style.transitionDelay = (Number(el.dataset.reveal) || 0) + 'ms';
        el.classList.add('is-in');
        // Clear the delay once it has played, or any later transition on the
        // same element inherits it.
        setTimeout(function () { el.style.transitionDelay = ''; }, 1200);
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    for (var j = 0; j < nodes.length; j++) io.observe(nodes[j]);
  }

  /* ------------------------------------------------------------------ DECK */
  function deck() {
    var fan = document.querySelector('.deck--fan');
    if (!fan) return;
    var cards = Array.prototype.slice.call(fan.querySelectorAll('.card'));

    if (reduce) { fan.classList.add('is-dealt', 'is-live'); return; }

    // Deal, then hand `transform` back to the shorter hover timing and clear
    // the per-card delays so a hover never waits out its card's stagger.
    cards.forEach(function (c, i) { c.style.transitionDelay = (i * 85) + 'ms'; });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        fan.classList.add('is-dealt');
        setTimeout(function () {
          cards.forEach(function (c) { c.style.transitionDelay = ''; });
          fan.classList.add('is-live');
        }, 85 * cards.length + 620);
      });
    });

    if (!fine) return;

    cards.forEach(function (card) {
      var box = null, queued = false, mx = 0, my = 0;

      function apply() {
        queued = false;
        card.style.setProperty('--tilt-x', (-my * 9).toFixed(2) + 'deg');
        card.style.setProperty('--tilt-y', (mx * 11).toFixed(2) + 'deg');
      }
      card.addEventListener('pointerenter', function () {
        box = card.getBoundingClientRect();          // measured once, on enter
        fan.classList.add('is-tracking');
      });
      card.addEventListener('pointermove', function (e) {
        if (!box) box = card.getBoundingClientRect();
        mx = (e.clientX - box.left) / box.width - 0.5;
        my = (e.clientY - box.top) / box.height - 0.5;
        if (!queued) { queued = true; requestAnimationFrame(apply); }
      }, { passive: true });
      card.addEventListener('pointerleave', function () {
        box = null;
        fan.classList.remove('is-tracking');          // transition back smoothly
        card.style.setProperty('--tilt-x', '0deg');
        card.style.setProperty('--tilt-y', '0deg');
      });
    });
  }

  /* ------------------------------------------------------------- SPOTLIGHT */
  function spotlight() {
    if (reduce || !fine) return;
    Array.prototype.forEach.call(document.querySelectorAll('[data-spotlight]'), function (el) {
      var box = null, queued = false, x = 0, y = 0;
      function apply() {
        queued = false;
        el.style.setProperty('--mx', x + 'px');
        el.style.setProperty('--my', y + 'px');
      }
      el.addEventListener('pointerenter', function () {
        box = el.getBoundingClientRect();
        el.style.setProperty('--spot', '1');
      });
      el.addEventListener('pointermove', function (e) {
        if (!box) box = el.getBoundingClientRect();
        x = Math.round(e.clientX - box.left);
        y = Math.round(e.clientY - box.top);
        if (!queued) { queued = true; requestAnimationFrame(apply); }
      }, { passive: true });
      el.addEventListener('pointerleave', function () {
        box = null;
        el.style.setProperty('--spot', '0');
      });
    });
  }

  /* --------------------------------------------------------------- MAGNETS */
  /* Capped deliberately low. A button that runs away from the cursor is a
     worse button than one that sits still. */
  function magnets() {
    if (reduce || !fine) return;
    Array.prototype.forEach.call(document.querySelectorAll('[data-magnet]'), function (el) {
      var box = null, queued = false, x = 0, y = 0;
      function apply() {
        queued = false;
        el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      }
      el.addEventListener('pointerenter', function () {
        box = el.getBoundingClientRect();
        el.classList.add('is-tracking');       // drops the transition while tracking
      });
      el.addEventListener('pointermove', function (e) {
        if (!box) box = el.getBoundingClientRect();
        x = (e.clientX - box.left - box.width / 2) * 0.2;
        y = (e.clientY - box.top - box.height / 2) * 0.3;
        if (!queued) { queued = true; requestAnimationFrame(apply); }
      }, { passive: true });
      el.addEventListener('pointerleave', function () {
        box = null;
        el.classList.remove('is-tracking');    // …and restores it for the way home
        el.style.transform = '';
      });
    });
  }

  /* -------------------------------------------------------------- HEADLINE */
  /* Words, never characters: splitting a word into per-letter spans makes some
     screen readers spell it out. textContent is unchanged, so assistive tech
     reads the sentence normally. */
  function splitHeadline() {
    var el = document.querySelector('[data-split]');
    if (!el || reduce) return;
    var words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    words.forEach(function (word, i) {
      var outer = document.createElement('span');
      outer.className = 'word';
      var inner = document.createElement('span');
      inner.className = 'word__in';
      inner.textContent = word;
      inner.style.transitionDelay = (i * 52) + 'ms';
      outer.appendChild(inner);
      el.appendChild(outer);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.classList.add('is-in'); });
    });
  }

  /* ------------------------------------------------------- HEADER + PROGRESS */
  /* One scroll listener for both, rAF-throttled. Two listeners each doing their
     own layout read is how a smooth page becomes a janky one. */
  function scrollUI() {
    var head = document.querySelector('.masthead');
    var bar = null;

    if (!reduce) {
      bar = document.createElement('div');
      bar.className = 'progress';
      bar.setAttribute('aria-hidden', 'true');
      document.body.appendChild(bar);
    }

    var queued = false;
    function apply() {
      queued = false;
      var y = window.scrollY || document.documentElement.scrollTop;
      if (head) head.classList.toggle('is-stuck', y > 4);
      if (bar) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.setProperty('--p', max > 0 ? Math.min(1, y / max).toFixed(4) : 0);
      }
    }
    addEventListener('scroll', function () {
      if (!queued) { queued = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  }

  function init() {
    theme();
    menu();
    scrollUI();
    var host = document.querySelector('[data-dotfield]');
    if (host) dotField(host);
    reveals();
    deck();
    spotlight();
    magnets();
    splitHeadline();

    // Someone can turn reduced-motion on while the page is open.
    if (mqReduce && mqReduce.addEventListener) {
      mqReduce.addEventListener('change', function (e) {
        if (e.matches) location.reload();
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
