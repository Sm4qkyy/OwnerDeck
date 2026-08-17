/* ============================================================
   Ownerdeck — hero backdrop

   The React Bits AcidSquares shader, running on raw WebGL2. The original
   pulls in ogl, but ogl was only ever a thin wrapper around one program,
   one fullscreen triangle and a handful of uniforms — and the render
   targets it also provided were needed solely for the blur pass, which
   went with the pointer interaction. Without those there is nothing left
   for a library to do, so there is no dependency and no build step.

   Removed from the original: the pointer dent and every uniform feeding
   it, and the two-pass Gaussian blur.

   Kept: the raymarched lattice itself, the tone mapping and the grain.

   Colours come from CSS custom properties, so the backdrop follows the
   theme rather than carrying a palette of its own. On paper the ramp runs
   pale-to-accent, because the shader multiplies colour by brightness and
   writes brightness to alpha — the bright parts are the visible ones, and
   on a white page the visible parts have to be the dark ones.
============================================================ */
(function () {
  "use strict";

  var host = document.querySelector('[data-acid-bg]');
  if (!host) return;

  /* An always-animating fullscreen raymarch is exactly what someone asking
     for less motion does not want, and the page is legible without it. */
  if (window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  /* Not on a phone. A per-pixel raymarch behind the first thing anyone sees
     costs battery and frame budget on exactly the devices with least of
     both, and the hero reads perfectly well without it. */
  if (window.matchMedia && window.matchMedia('(max-width: 48rem)').matches) return;

  var canvas = document.createElement('canvas');
  canvas.className = 'acid-bg__canvas';
  canvas.setAttribute('aria-hidden', 'true');

  var gl = canvas.getContext('webgl2', {
    alpha: true, premultipliedAlpha: true, antialias: false, depth: false
  });
  if (!gl) return;              // no WebGL2: the CSS wash behind it stands

  host.appendChild(canvas);

  var VERT =
    '#version 300 es\n' +
    'in vec2 position;\n' +
    'void main() { gl_Position = vec4(position, 0.0, 1.0); }\n';

  var FRAG =
    '#version 300 es\n' +
    'precision highp float;\n' +
    'uniform vec2 iResolution;\n' +
    'uniform float iTime;\n' +
    'uniform float uSpeed, uWaveDepth, uZoom, uDensity, uSpread, uStepSize;\n' +
    'uniform float uGlow, uExposure, uColorShift, uContrast, uBrightness;\n' +
    'uniform float uOpacity, uSteps, uGrainIntensity;\n' +
    'uniform vec3 uColor1, uColor2, uColor3;\n' +
    'out vec4 fragColor;\n' +
    'void main() {\n' +
    '  vec2 frag = gl_FragCoord.xy;\n' +
    '  float zoom = max(uZoom, 0.05);\n' +
    '  vec2 ndc = (2.0 * frag - iResolution.xy) / iResolution.y;\n' +
    '  vec2 dir = ndc * (0.5 / zoom);\n' +
    '  float travel = sin(iTime * uSpeed) * uWaveDepth;\n' +
    '  float density = max(uDensity, 1.0);\n' +
    '  float spread = clamp(uSpread, 0.05, 0.6);\n' +
    '  float stepSize = max(uStepSize, 0.0005);\n' +
    '  float glowGain = max(uGlow, 0.0);\n' +
    /* tOffset.y was the pointer depression. Held at zero now. */
    '  vec3 tOffset = vec3(0.0, 0.0, travel);\n' +
    '  vec3 p = vec3(0.0);\n' +
    '  float s = 0.0;\n' +
    '  float glow = 0.0;\n' +
    '  for (int i = 0; i < 64; i++) {\n' +
    '    if (float(i) >= uSteps) break;\n' +
    '    p += vec3(dir * s, s);\n' +
    '    vec3 q = p + tOffset;\n' +
    '    s += density - length(q.xz) + length(ceil(q).xy);\n' +
    '    s = stepSize + abs(s) * spread;\n' +
    '    glow += glowGain / s;\n' +
    '  }\n' +
    '  float e = glow / max(uExposure, 1.0);\n' +
    '  float shimmer = 0.5 + 0.5 * dot(cos(iTime * uColorShift + p), vec3(0.3333));\n' +
    '  float v = tanh(e * uBrightness * mix(0.7, 1.05, shimmer));\n' +
    '  v = clamp((v - 0.5) * uContrast + 0.5, 0.0, 1.0);\n' +
    '  vec3 col = mix(uColor1, uColor2, smoothstep(0.0, 0.55, v));\n' +
    '  col = mix(col, uColor3, smoothstep(0.55, 1.0, v));\n' +
    '  col *= v;\n' +
    '  float a = clamp(v, 0.0, 1.0) * uOpacity;\n' +
    '  vec3 outRgb = col * a;\n' +
    '  if (uGrainIntensity > 0.0) {\n' +
    '    float gv = (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233)) + iTime) * 43758.5453) - 0.5) * uGrainIntensity;\n' +
    '    outRgb = clamp(outRgb + gv, 0.0, 1.0);\n' +
    '    a = clamp(a + gv, 0.0, 1.0);\n' +
    '  }\n' +
    '  fragColor = vec4(outRgb, a);\n' +
    '}\n';

  function compile(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  var vs = compile(gl.VERTEX_SHADER, VERT);
  var fs = compile(gl.FRAGMENT_SHADER, FRAG);
  if (!vs || !fs) { host.removeChild(canvas); return; }

  var prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.bindAttribLocation(prog, 0, 'position');
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { host.removeChild(canvas); return; }
  gl.useProgram(prog);

  // One oversized triangle covering the viewport — cheaper than two.
  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

  var U = {};
  ['iResolution', 'iTime', 'uSpeed', 'uWaveDepth', 'uZoom', 'uDensity', 'uSpread',
   'uStepSize', 'uGlow', 'uExposure', 'uColorShift', 'uContrast', 'uBrightness',
   'uOpacity', 'uSteps', 'uGrainIntensity', 'uColor1', 'uColor2', 'uColor3'
  ].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });

  function css(name, fallback) {
    var v = getComputedStyle(host).getPropertyValue(name).trim();
    return v || fallback;
  }
  function rgb(hex) {
    var m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!m) return [1, 1, 1];
    return [parseInt(m[1], 16) / 255, parseInt(m[2], 16) / 255, parseInt(m[3], 16) / 255];
  }
  function nf(name, fallback) {
    var v = parseFloat(css(name, ''));
    return isNaN(v) ? fallback : v;
  }

  /* A 32-step raymarch per pixel at full retina density is a lot of work to
     put behind a headline. Half the steps and a capped ratio on a phone. */
  var small = window.matchMedia('(max-width: 48rem)').matches;
  var DPR = Math.min(window.devicePixelRatio || 1, small ? 1.25 : 1.75);

  function paintUniforms() {
    var c1 = rgb(css('--acid-1', '#C9D4E6'));
    var c2 = rgb(css('--acid-2', '#8FB3FF'));
    var c3 = rgb(css('--acid-3', '#1D4ED8'));
    gl.uniform3f(U.uColor1, c1[0], c1[1], c1[2]);
    gl.uniform3f(U.uColor2, c2[0], c2[1], c2[2]);
    gl.uniform3f(U.uColor3, c3[0], c3[1], c3[2]);
    gl.uniform1f(U.uOpacity, nf('--acid-opacity', 0.34));
    gl.uniform1f(U.uSpeed, 0.7);
    gl.uniform1f(U.uWaveDepth, 1.0);
    gl.uniform1f(U.uZoom, 1.3);
    gl.uniform1f(U.uDensity, 10.0);
    gl.uniform1f(U.uSpread, 0.3);
    gl.uniform1f(U.uStepSize, 0.002);
    gl.uniform1f(U.uGlow, 1.0);
    gl.uniform1f(U.uExposure, 2700.0);
    gl.uniform1f(U.uColorShift, 0.0);
    gl.uniform1f(U.uContrast, 1.0);
    gl.uniform1f(U.uBrightness, 1.0);
    gl.uniform1f(U.uSteps, small ? 16.0 : 26.0);
    gl.uniform1f(U.uGrainIntensity, 0.04);
  }

  var sized = false;

  function size() {
    var r = host.getBoundingClientRect();
    /* A host measuring zero — a hidden tab, a display:none ancestor, some
       load states — would give a 1px canvas that renders nothing and never
       corrects itself, because nothing fires a resize afterwards. Wait for
       a real box instead, and let the load event try again. */
    if (r.width < 2 || r.height < 2) { sized = false; return; }
    var w = Math.max(1, Math.floor(r.width * DPR));
    var h = Math.max(1, Math.floor(r.height * DPR));
    sized = true;
    if (canvas.width === w && canvas.height === h) return;
    canvas.width = w;
    canvas.height = h;
    gl.viewport(0, 0, w, h);
    gl.uniform2f(U.iResolution, w, h);
  }

  gl.clearColor(0, 0, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);   // premultiplied
  paintUniforms();
  size();

  var raf = 0, t0 = performance.now(), onScreen = true, pageOn = !document.hidden;

  function frame(t) {
    gl.uniform1f(U.iTime, (t - t0) * 0.001);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    raf = requestAnimationFrame(frame);
  }
  function start() {
    if (!sized) size();                       // nothing to draw into yet
    if (sized && onScreen && pageOn && !raf) raf = requestAnimationFrame(frame);
  }
  function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

  // Nothing is gained by shading pixels nobody is looking at.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      onScreen = es[0].isIntersecting;
      onScreen ? start() : stop();
    }, { threshold: 0 }).observe(host);
  }
  document.addEventListener('visibilitychange', function () {
    pageOn = !document.hidden;
    pageOn ? start() : stop();
  });

  if (!sized) window.addEventListener('load', function () { size(); start(); }, { once: true });
  window.addEventListener('resize', function () { size(); start(); });
  if ('ResizeObserver' in window) new ResizeObserver(function () { size(); start(); }).observe(host);

  // The theme toggle rewrites the custom properties this reads.
  if (window.OD_theme && window.OD_theme.onChange) {
    window.OD_theme.onChange(paintUniforms);
  } else {
    new MutationObserver(paintUniforms).observe(document.documentElement,
      { attributes: true, attributeFilter: ['data-theme'] });
  }

  start();
})();
