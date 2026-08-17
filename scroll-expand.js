/* ============================================================
   Ownerdeck — scroll-expand hero

   A port of the React Bits <ScrollExpand /> to plain JS, because this site
   has no build step and the CSP would not load a framework anyway. Nothing
   in the original is React-specific: it is scroll maths driving clip-path
   and transform, so the port is faithful rather than an approximation.

   Driven by window scroll. A tall track holds the space, the stage sticks
   to the top of it, and progress is read from how far the track has moved
   past the viewport. The frame opens from a centred inset to full bleed
   while the media eases back from its resting zoom.

   Everything is guarded by the .js class: with scripting off the frame is
   already full bleed and the overlay copy is already visible, so the
   section reads as an ordinary image with a caption.
============================================================ */
(function () {
  "use strict";

  var root = document.querySelector('[data-scroll-expand]');
  if (!root) return;

  var track   = root.querySelector('.se__track');
  var stage   = root.querySelector('.se__stage');
  var frame   = root.querySelector('.se__frame');
  var media   = root.querySelector('.se__media');
  var scrim   = root.querySelector('.se__scrim');
  var title   = root.querySelector('.se__title');
  var hint    = root.querySelector('.se__hint');
  var overlay = root.querySelector('.se__overlay');
  if (!track || !stage || !frame || !media) return;

  /* Defaults match the component's. Any of them can be overridden per
     instance with a data- attribute, so the markup stays declarative. */
  function num(name, fallback) {
    var v = parseFloat(root.getAttribute('data-' + name));
    return isNaN(v) ? fallback : v;
  }
  var startWidth     = num('start-width', 42);
  var startHeight    = num('start-height', 58);
  var startRadius    = num('start-radius', 24);
  var endRadius      = num('end-radius', 0);
  var mediaZoom      = num('media-zoom', 1.35);
  var scrollDistance = num('scroll-distance', 1.2);
  var holdDistance   = num('hold-distance', 0.35);
  var smoothing      = num('smoothing', 0.1);
  var overlayScrim   = num('overlay-scrim', 0.45);
  /* The component fades the scrim in from nothing, which leaves the title on
     bare photograph at rest. The day plate is near-white and cannot carry
     type that way, so the scrim starts here and deepens rather than
     appearing. Matches the resting value in od.css. */
  var restScrim      = num('rest-scrim', 0.28);

  var reduce = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Not on a phone. Pinning a stage for nearly two screens is a lot of
     scrolling to ask for on a device where the whole page is already
     thirteen screens; the section becomes an ordinary picture instead,
     which the CSS below 48rem already lays out. */
  if (window.matchMedia && window.matchMedia('(max-width: 48rem)').matches) return;

  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }

  /* Cubic ease. The original uses this both for the master curve and for
     staggering the title, hint and overlay against it. */
  function smoothstep(e0, e1, x) {
    var t = clamp((x - e0) / ((e1 - e0) || 1e-6), 0, 1);
    return t * t * (3 - 2 * t);
  }

  var raf = 0, current = 0, target = 0, stageH = 0, running = false;

  function apply(p) {
    var e = smoothstep(0, 1, p);

    var w  = startWidth + (100 - startWidth) * e;
    var h  = startHeight + (100 - startHeight) * e;
    var ix = Math.max(0, (100 - w) / 2);
    var iy = Math.max(0, (100 - h) / 2);
    var r  = startRadius + (endRadius - startRadius) * e;
    frame.style.clipPath = 'inset(' + iy + '% ' + ix + '% ' + iy + '% ' + ix + '% round ' + r + 'px)';

    media.style.transform = 'scale(' + (mediaZoom + (1 - mediaZoom) * e) + ')';

    if (scrim) scrim.style.opacity = String(restScrim + (overlayScrim - restScrim) * e);

    if (title) {
      var out = smoothstep(0.4, 0.88, p);
      title.style.opacity = String(1 - out);
      title.style.transform = 'translate3d(0,' + (-28 * out) + 'px,0) scale(' + (1 + 0.06 * out) + ')';
    }
    if (hint) {
      var gone = smoothstep(0, 0.12, p);
      hint.style.opacity = String(1 - gone);
      hint.style.transform = 'translate3d(0,' + (8 * gone) + 'px,0)';
    }
    if (overlay) {
      var inn = smoothstep(0.68, 1, p);
      overlay.style.opacity = String(inn);
      overlay.style.transform = 'translate3d(0,' + (18 * (1 - inn)) + 'px,0)';
    }
  }

  function measure() {
    stageH = window.innerHeight || document.documentElement.clientHeight;
    /* A zero viewport is real: hidden tabs and some load states report it.
       Bailing here used to leave the track at zero height and the whole
       section invisible, so the CSS keeps a vh-based fallback and this just
       waits for a viewport worth measuring. */
    if (stageH <= 0) return;
    stage.style.height = stageH + 'px';
    track.style.height = (stageH * (1 + Math.max(0, scrollDistance) + Math.max(0, holdDistance))) + 'px';
    var w = root.clientWidth || stageH;
    stage.style.setProperty('--se-title-size', clamp(w * 0.075, 20, 84) + 'px');
  }

  function readProgress() {
    // Unmeasured: span would be zero and the division would clamp to a full
    // expansion for no reason. Sit at rest until there is a viewport.
    if (stageH <= 0) return 0;
    var span = stageH * Math.max(0.01, scrollDistance);
    return clamp(-track.getBoundingClientRect().top / span, 0, 1);
  }

  function tick() {
    /* Frame-rate independent exponential follow: `smoothing` is a time in
       seconds, not a per-frame fraction, so the ease feels the same at
       120Hz as at 60. */
    var k = smoothing <= 0 ? 1 : 1 - Math.exp(-1 / (60 * smoothing));
    current += (target - current) * k;
    if (Math.abs(target - current) < 0.0004) {
      current = target;
      running = false;
    }
    apply(current);
    raf = running ? requestAnimationFrame(tick) : 0;
  }

  function onScroll() {
    target = readProgress();
    if (smoothing <= 0 || reduce) {      // no easing to chase; paint it now
      current = target;
      apply(current);
      return;
    }
    if (running) return;
    running = true;
    if (!raf) raf = requestAnimationFrame(tick);
  }

  function onResize() {
    measure();
    target = current = readProgress();
    apply(current);
  }

  measure();
  target = current = readProgress();
  apply(current);

  // If the first measure found no viewport, try again once the page is fully
  // up rather than leaving the section on its CSS fallback for the session.
  if (stageH <= 0) window.addEventListener('load', onResize, { once: true });

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);
  if ('ResizeObserver' in window) new ResizeObserver(onResize).observe(root);

})();
