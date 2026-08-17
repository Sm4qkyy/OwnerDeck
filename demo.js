/* ================================================================
   Ownerdeck — demo page
   1) Renders the demo video (or a placeholder until one is configured)
   2) Runs a preset conversation so visitors feel how it answers
   3) Renders the contact channels set in config.js

   English only. The site-wide translation layer was retired in the
   rebrand; i18n.js and lang/*.json are still in the repo for whenever a
   Greek version is wanted, but nothing on this page depends on them.

   The customer's Russian message and the reply to it stay in Russian on
   purpose — that exchange exists to show language being detected, and
   translating it would erase the thing being demonstrated.
================================================================ */
(function () {
  "use strict";

  var CFG = window.OD_CONFIG || {};

  /* ------------------------------------------------------------ VIDEO */
  function renderVideo() {
    var host = document.getElementById("od-video");
    if (!host) return;
    var d = CFG.demo || {};
    var type = (d.type || "").toLowerCase();
    var src = d.src || "";

    if (!type || !src) {
      host.innerHTML =
        '<div class="video-soon"><div>' +
        '<p class="bot__name">Demo video coming soon</p>' +
        '<p class="bot__done">In the meantime, try the live assistant in step three.</p>' +
        '</div></div>';
      return;
    }

    var inner = "";
    if (type === "mp4") {
      /* Our own chrome. The browser's default bar is fine, but it is the one
         piece of the page that looks like someone else built it — different
         type, different radius, different blue. An embedded iframe below
         still gets the provider's player; only the file we serve ourselves
         can be dressed. */
      inner = playerHTML(src, d.poster);
    } else if (type === "youtube") {
      inner = '<iframe class="video-el" src="https://www.youtube-nocookie.com/embed/' +
              encodeURIComponent(src) + '" title="Ownerdeck demo" allowfullscreen></iframe>';
    } else if (type === "loom") {
      inner = '<iframe class="video-el" src="https://www.loom.com/embed/' +
              encodeURIComponent(src) + '" title="Ownerdeck demo" allowfullscreen></iframe>';
    } else if (type === "vimeo") {
      inner = '<iframe class="video-el" src="https://player.vimeo.com/video/' +
              encodeURIComponent(src) + '" title="Ownerdeck demo" allowfullscreen></iframe>';
    }
    host.innerHTML = '<div class="video-frame">' + inner + "</div>";
    if (type === "mp4") wirePlayer(host);
  }

  /* ---------------------------------------------------- CUSTOM PLAYER */

  function icon(paths) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + paths + '</svg>';
  }
  var I_PLAY  = icon('<path d="M8 5.5v13l11-6.5z"/>');
  var I_PAUSE = icon('<path d="M7 5h3.2v14H7zm6.8 0H17v14h-3.2z"/>');
  var I_MUTE  = icon('<path d="M4 9.5h3.5L12 5.5v13L7.5 14.5H4z"/>' +
                     '<path d="m16.5 9.5 4 5m0-5-4 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>');
  var I_VOL   = icon('<path d="M4 9.5h3.5L12 5.5v13L7.5 14.5H4z"/>' +
                     '<path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>');
  var I_FULL  = icon('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>');
  var I_EXIT  = icon('<path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>');

  function playerHTML(src, poster) {
    return '' +
      '<div class="vp" data-state="idle">' +
        '<video class="vp__v" playsinline preload="metadata"' +
          (poster ? ' poster="' + poster + '"' : '') + '>' +
          '<source src="' + src + '" type="video/mp4">' +
          'Your browser cannot play this video.' +
        '</video>' +
        '<button class="vp__big" type="button" aria-label="Play the demo">' + I_PLAY + '</button>' +
        '<div class="vp__bar">' +
          '<button class="vp__btn vp__play" type="button" aria-label="Play">' + I_PLAY + '</button>' +
          '<input class="vp__seek" type="range" min="0" max="0" step="0.1" value="0" ' +
            'aria-label="Seek" style="--fill:0%">' +
          '<span class="vp__time"><span class="vp__now">0:00</span>' +
            '<span class="vp__sep"> / </span><span class="vp__dur">0:00</span></span>' +
          '<button class="vp__btn vp__mute" type="button" aria-label="Mute">' + I_VOL + '</button>' +
          '<button class="vp__btn vp__full" type="button" aria-label="Full screen">' + I_FULL + '</button>' +
        '</div>' +
      '</div>';
  }

  function clock(t) {
    if (!isFinite(t) || t < 0) t = 0;
    var m = Math.floor(t / 60), sec = Math.floor(t % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function wirePlayer(host) {
    var vp   = host.querySelector('.vp');
    var v    = host.querySelector('.vp__v');
    var big  = host.querySelector('.vp__big');
    var play = host.querySelector('.vp__play');
    var seek = host.querySelector('.vp__seek');
    var now  = host.querySelector('.vp__now');
    var dur  = host.querySelector('.vp__dur');
    var mute = host.querySelector('.vp__mute');
    var full = host.querySelector('.vp__full');
    if (!vp || !v) return;

    var idle = null;
    var scrubbing = false;

    function setPlayIcon() {
      var lbl = v.paused ? 'Play' : 'Pause';
      play.innerHTML = v.paused ? I_PLAY : I_PAUSE;
      play.setAttribute('aria-label', lbl);
      big.setAttribute('aria-label', v.paused ? 'Play the demo' : 'Pause the demo');
      vp.setAttribute('data-state', v.paused ? (v.currentTime ? 'paused' : 'idle') : 'playing');
    }
    function toggle() { if (v.paused) { v.play(); } else { v.pause(); } }

    /* The bar hides itself while the video is playing and nobody is
       interacting. Any pointer movement, focus or keypress brings it back. */
    function wake() {
      vp.classList.add('is-awake');
      clearTimeout(idle);
      if (!v.paused) idle = setTimeout(function () {
        if (!vp.contains(document.activeElement)) vp.classList.remove('is-awake');
      }, 2200);
    }

    function paintSeek() {
      var d = v.duration;
      if (!isFinite(d) || d <= 0) return;
      if (!scrubbing) { seek.value = v.currentTime; }
      seek.style.setProperty('--fill', (v.currentTime / d * 100).toFixed(2) + '%');
      now.textContent = clock(v.currentTime);
      seek.setAttribute('aria-valuetext', clock(v.currentTime) + ' of ' + clock(d));
    }

    v.addEventListener('loadedmetadata', function () {
      seek.max = v.duration || 0;
      dur.textContent = clock(v.duration);
      paintSeek();
    });
    v.addEventListener('timeupdate', paintSeek);
    v.addEventListener('play',  function () { setPlayIcon(); wake(); });
    v.addEventListener('pause', function () { setPlayIcon(); wake(); });
    v.addEventListener('ended', function () {
      vp.setAttribute('data-state', 'idle');
      vp.classList.add('is-awake');
      setPlayIcon();
    });
    v.addEventListener('volumechange', function () {
      mute.innerHTML = v.muted || !v.volume ? I_MUTE : I_VOL;
      mute.setAttribute('aria-label', v.muted || !v.volume ? 'Unmute' : 'Mute');
    });

    big.addEventListener('click', toggle);
    play.addEventListener('click', toggle);
    v.addEventListener('click', toggle);
    mute.addEventListener('click', function () { v.muted = !v.muted; });

    seek.addEventListener('pointerdown', function () { scrubbing = true; });
    // Release can land outside the control, so listen on the document.
    document.addEventListener('pointerup', function () { scrubbing = false; });
    seek.addEventListener('input', function () {
      v.currentTime = Number(seek.value);
      seek.style.setProperty('--fill',
        (v.duration ? Number(seek.value) / v.duration * 100 : 0).toFixed(2) + '%');
      now.textContent = clock(Number(seek.value));
    });

    function fsEl() {
      return document.fullscreenElement || document.webkitFullscreenElement || null;
    }
    full.addEventListener('click', function () {
      if (fsEl()) {
        (document.exitFullscreen || document.webkitExitFullscreen).call(document);
      } else if (vp.requestFullscreen) {
        vp.requestFullscreen();
      } else if (vp.webkitRequestFullscreen) {
        vp.webkitRequestFullscreen();
      } else if (v.webkitEnterFullscreen) {
        v.webkitEnterFullscreen();      // iPhone only allows the video itself
      }
    });
    document.addEventListener('fullscreenchange', function () {
      var on = !!fsEl();
      full.innerHTML = on ? I_EXIT : I_FULL;
      full.setAttribute('aria-label', on ? 'Exit full screen' : 'Full screen');
      vp.classList.toggle('is-full', on);
    });

    /* Keyboard, on the container so it works wherever focus sits inside it.
       Space and the arrows are only intercepted when the focused thing is not
       already a control that uses them — otherwise the seek slider would stop
       responding to its own arrow keys. */
    vp.setAttribute('tabindex', '0');
    vp.addEventListener('keydown', function (e) {
      var onSlider = e.target === seek;
      var k = e.key;
      if ((k === ' ' || k === 'k') && !/^(BUTTON|INPUT)$/.test(e.target.tagName)) {
        e.preventDefault(); toggle();
      } else if (k === 'ArrowRight' && !onSlider) {
        e.preventDefault(); v.currentTime = Math.min(v.duration || 0, v.currentTime + 5);
      } else if (k === 'ArrowLeft' && !onSlider) {
        e.preventDefault(); v.currentTime = Math.max(0, v.currentTime - 5);
      } else if (k === 'ArrowUp' && !onSlider) {
        e.preventDefault(); v.volume = Math.min(1, v.volume + 0.1);
      } else if (k === 'ArrowDown' && !onSlider) {
        e.preventDefault(); v.volume = Math.max(0, v.volume - 0.1);
      } else if (k === 'm') { v.muted = !v.muted; }
      else if (k === 'f')   { full.click(); }
      wake();
    });

    ['pointermove', 'pointerdown', 'focusin'].forEach(function (ev) {
      vp.addEventListener(ev, wake);
    });
    vp.addEventListener('pointerleave', function () {
      if (!v.paused && !vp.contains(document.activeElement)) vp.classList.remove('is-awake');
    });

    setPlayIcon();
    wake();
  }

  /* -------------------------------------------------------------- BOT */
  var SCRIPT = {
    start: {
      bot: ["Hello. I answer for a demo business, Blue Bay Tours. Ask me what a real customer would ask."],
      options: [
        { text: "Any space on the sunset cruise Friday?", to: "availability" },
        { text: "How much for 2 people?", to: "price" },
        { text: "Try asking in Russian", send: "Здравствуйте. Вы говорите по-русски?", to: "russian" }
      ]
    },
    availability: {
      bot: ["Friday's 18:00 sunset cruise has six seats left, at €35 per person.",
            "Want me to hold a couple for you?"],
      options: [
        { text: "Yes, two people please", to: "hold" },
        { text: "What is included?", to: "included" }
      ]
    },
    price: {
      bot: ["€35 per person, so €70 for two.",
            "That covers hotel pickup, a welcome drink and the full two-hour cruise."],
      options: [
        { text: "Great, Friday works", to: "hold" },
        { text: "Try asking in Russian", send: "Вы говорите по-русски?", to: "russian" }
      ]
    },
    russian: {
      bot: ["Конечно. Отвечаю на вашем языке.",
            "Закат-круиз в пятницу в 18:00 — осталось шесть мест, €35 с человека. Забронировать?"],
      note: "Language detected on its own. Nothing to set up.",
      options: [
        { text: "Да, на двоих", to: "hold" },
        { text: "Back to English please", to: "included" }
      ]
    },
    included: {
      bot: ["Pickup from your hotel, a welcome drink, two hours on the water and a swim stop.",
            "Shall I put two seats down for Friday?"],
      options: [{ text: "Yes please, book it", to: "hold" }]
    },
    hold: {
      bot: ["Done. Booking TC-2291, Friday 18:00, two seats, hotel pickup included.",
            "Confirmation sent, and the owner has been told."],
      end: true
    }
  };

  var bot = {
    host: null, msgs: null, opts: null, busy: false, seq: 0,

    init: function () {
      this.host = document.getElementById("od-bot");
      if (!this.host) return;
      this.host.innerHTML =
        '<div class="bot__head">' +
          '<div><p class="bot__name">Blue Bay Tours</p>' +
          '<p class="bot__state">Ownerdeck, answering now</p></div>' +
          '<button class="bot__restart" type="button">Start over</button>' +
        '</div>' +
        '<div class="bot__msgs" id="od-bot-msgs" role="log" aria-live="polite" aria-label="Demo conversation"></div>' +
        '<div class="bot__opts" id="od-bot-opts"></div>';
      this.msgs = this.host.querySelector("#od-bot-msgs");
      this.opts = this.host.querySelector("#od-bot-opts");
      var self = this;
      this.host.querySelector(".bot__restart").addEventListener("click", function () { self.reset(); });
      this.run("start");
    },

    reset: function () {
      if (!this.msgs) return;
      this.seq++;                  // strands any timer left over from the old run
      this.msgs.innerHTML = "";
      this.opts.innerHTML = "";
      this.busy = false;
      this.run("start");
    },

    add: function (cls, text) {
      var d = document.createElement("div");
      d.className = "msg " + cls;
      d.textContent = text;
      this.msgs.appendChild(d);
      this.scroll();
      return d;
    },

    note: function (text) {
      var d = document.createElement("p");
      d.className = "msg msg--note";
      d.textContent = text;
      this.msgs.appendChild(d);
      this.scroll();
    },

    // Read scrollHeight after layout has flushed; in the same tick as the
    // appendChild it is stale, which left the newest message off-screen.
    scroll: function () {
      var m = this.msgs;
      if (!m) return;
      var go = function () { m.scrollTop = m.scrollHeight; };
      go();
      if (window.requestAnimationFrame) requestAnimationFrame(function () { requestAnimationFrame(go); });
    },

    typing: function () {
      var d = document.createElement("div");
      d.className = "msg msg--bot typing";
      d.innerHTML = "<i></i><i></i><i></i>";
      this.msgs.appendChild(d);
      this.scroll();
      return d;
    },

    run: function (key) {
      var node = SCRIPT[key];
      if (!node) return;
      this.busy = true;
      this.opts.innerHTML = "";
      var self = this, mine = this.seq, i = 0;

      function next() {
        if (mine !== self.seq) return;
        if (i >= node.bot.length) {
          if (node.note) self.note(node.note);
          self.busy = false;
          if (node.end) { self.finish(); } else { self.showOptions(node.options); }
          return;
        }
        var line = node.bot[i];
        var t = self.typing();
        setTimeout(function () {
          if (mine !== self.seq) { t.remove(); return; }
          t.remove();
          self.add("msg--bot", line);
          i++;
          setTimeout(next, 260);
        }, Math.min(1100, 380 + line.length * 9));
      }
      setTimeout(next, 320);
    },

    showOptions: function (options) {
      if (!options) return;
      var self = this;
      options.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "bot__opt";
        b.textContent = o.text;
        b.addEventListener("click", function () {
          if (self.busy) return;
          self.opts.innerHTML = "";
          self.add("msg--me", o.send || o.text);   // label can differ from what is sent
          self.run(o.to);
        });
        self.opts.appendChild(b);
      });
    },

    finish: function () {
      var p = document.createElement("p");
      p.className = "bot__done";
      p.textContent = "That whole conversation, with no human involved. This is a preset " +
                      "demo — the real one uses your services, prices and availability.";
      this.opts.appendChild(p);
    }
  };

  /* --------------------------------------------------------- CHANNELS */
  function renderChannels() {
    var host = document.getElementById("od-channels");
    if (!host) return;

    var msg = "Hi Mark. I saw the Ownerdeck demo and I'd like to know more.";
    var out = [];

    if (/^\d{8,15}$/.test(CFG.whatsappNumber || "")) {
      out.push({ href: "https://wa.me/" + CFG.whatsappNumber + "?text=" + encodeURIComponent(msg),
                 label: "WhatsApp" });
    }
    if (CFG.instagram)  out.push({ href: CFG.instagram, label: "Instagram" });
    if (CFG.email)      out.push({ href: "mailto:" + CFG.email + "?subject=" +
                                        encodeURIComponent("Ownerdeck enquiry"), label: "Email" });

    var row = document.createElement("div");
    row.className = "channels";
    out.forEach(function (c) {
      var a = document.createElement("a");
      a.className = "channel";
      a.href = c.href;
      a.textContent = c.label;
      if (c.href.indexOf("mailto:") !== 0) { a.rel = "noopener"; a.target = "_blank"; }
      row.appendChild(a);
    });
    host.innerHTML = "";
    host.appendChild(row);
  }

  function init() {
    renderVideo();
    bot.init();
    renderChannels();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
