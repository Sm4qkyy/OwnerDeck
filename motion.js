/* ============================================================
   Ownerdeck — motion

   Five effects, no dependencies, no build step. Written by hand
   rather than pulled from a React component library, because the
   site has no framework and adding one to get a hover effect is a
   bad trade.

   Every effect here is decoration. The page is complete and
   readable with this file deleted, with JavaScript off, and for
   anyone who has asked their system for less movement — the
   reduced-motion check below returns before anything starts.

   Colours are read from brand.css at runtime. Nothing in this file
   declares one.
   ============================================================ */
(function () {
  "use strict";

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine   = window.matchMedia && matchMedia('(pointer: fine)').matches;

  function token(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /* ------------------------------------------------------------------
     1. Dot field — the hero set-piece.

     A halftone grid in clay on bone that leans away from the pointer.
     Printed rather than sci-fi: it reads as ink on paper that someone
     has just pressed a thumb into, which is the whole brief in one
     effect. Canvas, because a thousand DOM nodes would not survive
     a scroll.
  ------------------------------------------------------------------ */
  function dotField(host) {
    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    canvas.className = 'dotfield__canvas';
    host.appendChild(canvas);

    var ctx = canvas.getContext('2d', { alpha: true });
    var dots = [], w = 0, h = 0, dpr = 1;
    var GAP = 26, RADIUS = 120, running = false, raf = 0;
    var px = -9999, py = -9999;          // pointer, parked off-canvas
    var clay = token('--clay') || '#C4643C';

    function build() {
      var rect = host.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);   // cap: retina x3 is wasted here
      w = rect.width; h = rect.height;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      dots = [];
      var cols = Math.ceil(w / GAP), rows = Math.ceil(h / GAP);
      for (var i = 0; i <= cols; i++) {
        for (var j = 0; j <= rows; j++) {
          dots.push({ x: i * GAP, y: j * GAP, ox: 0, oy: 0 });
        }
      }
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var dx = d.x - px, dy = d.y - py;
        var dist = Math.sqrt(dx * dx + dy * dy);
        var near = dist < RADIUS ? 1 - dist / RADIUS : 0;

        // Ease toward the target rather than snapping, so the field
        // settles after the pointer leaves instead of stopping dead.
        var tx = near ? (dx / (dist || 1)) * near * 11 : 0;
        var ty = near ? (dy / (dist || 1)) * near * 11 : 0;
        d.ox += (tx - d.ox) * 0.12;
        d.oy += (ty - d.oy) * 0.12;

        var r = 1 + near * 1.6;
        ctx.globalAlpha = 0.16 + near * 0.5;
        ctx.fillStyle = clay;
        ctx.beginPath();
        ctx.arc(d.x + d.ox, d.y + d.oy, r, 0, 6.2832);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    }

    function loop() { draw(); raf = requestAnimationFrame(loop); }
    function start() { if (!running) { running = true; loop(); } }
    function stop()  { running = false; cancelAnimationFrame(raf); }

    build();
    draw();                                    // one static frame for everyone

    if (reduce || !fine) return;               // touch and reduced-motion stop here

    host.addEventListener('pointermove', function (e) {
      var r = host.getBoundingClientRect();
      px = e.clientX - r.left; py = e.clientY - r.top;
      start();
    });
    host.addEventListener('pointerleave', function () {
      px = py = -9999;
      setTimeout(stop, 900);                   // let it settle, then stop burning frames
    });

    // Never animate a canvas that has scrolled out of view.
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) stop();
      }, { threshold: 0 }).observe(host);
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop();
    });

    var t;
    addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(function () { build(); draw(); }, 150);
    }, { passive: true });
  }

  /* ------------------------------------------------------------------
     2. Reveal on scroll.
     One observer for the whole page; each element unobserves itself
     once it has appeared, so nothing accumulates.
  ------------------------------------------------------------------ */
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
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    for (var j = 0; j < nodes.length; j++) io.observe(nodes[j]);
  }

  /* ------------------------------------------------------------------
     3. The deck — depth and tilt.
     The fan already exists in CSS. This adds a pointer-tracked tilt on
     top of each card's resting rotation, and deals the hand in on load.
  ------------------------------------------------------------------ */
  function deck() {
    var fan = document.querySelector('.deck--fan');
    if (!fan) return;

    if (!reduce) fan.classList.add('is-dealt');
    if (reduce || !fine) return;

    var cards = fan.querySelectorAll('.card');
    Array.prototype.forEach.call(cards, function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var cx = (e.clientX - r.left) / r.width - 0.5;
        var cy = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty('--tilt-x', (-cy * 9).toFixed(2) + 'deg');
        card.style.setProperty('--tilt-y', (cx * 11).toFixed(2) + 'deg');
      });
      card.addEventListener('pointerleave', function () {
        card.style.setProperty('--tilt-x', '0deg');
        card.style.setProperty('--tilt-y', '0deg');
      });
    });
  }

  /* ------------------------------------------------------------------
     4. Spotlight — pricing cards.
     A single-hue clay wash tracking the pointer. Written as coordinates
     on the element; the wash itself lives in brand.css so no colour is
     declared here.
  ------------------------------------------------------------------ */
  function spotlight() {
    if (reduce || !fine) return;
    var nodes = document.querySelectorAll('[data-spotlight]');
    Array.prototype.forEach.call(nodes, function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
        el.style.setProperty('--spot', '1');
      });
      el.addEventListener('pointerleave', function () {
        el.style.setProperty('--spot', '0');
      });
    });
  }

  /* ------------------------------------------------------------------
     5. Magnetic primary action.
     Small pull toward the pointer. Capped at a few pixels: a button
     that runs away from the cursor is a worse button.
  ------------------------------------------------------------------ */
  function magnets() {
    if (reduce || !fine) return;
    var nodes = document.querySelectorAll('[data-magnet]');
    Array.prototype.forEach.call(nodes, function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.22;
        var y = (e.clientY - r.top - r.height / 2) * 0.34;
        el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ------------------------------------------------------------------
     6. Headline, word by word.
     Words, never characters: splitting a word into per-letter spans
     makes some screen readers spell it out. The element's text content
     is unchanged, so assistive tech reads the sentence normally.
  ------------------------------------------------------------------ */
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
      inner.style.transitionDelay = (i * 55) + 'ms';
      outer.appendChild(inner);
      el.appendChild(outer);
      if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
    });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.classList.add('is-in'); });
    });
  }

  function init() {
    var host = document.querySelector('[data-dotfield]');
    if (host) dotField(host);
    reveals();
    deck();
    spotlight();
    magnets();
    splitHeadline();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
