/* ================================================================
   Ownerdeck — demo section
   1) Renders the demo video (or a "coming soon" card until configured)
   2) Runs an interactive, preset conversation so visitors feel it
   3) Renders "message me" buttons for the channels set in config.js

   Translation
   -----------
   Static markup this file writes carries data-i18n and is painted by
   i18n.js. The conversation is different: it types itself out over
   several seconds, long after i18n.js has finished painting, so every
   line resolves through T() at the moment it is created. Keys are the
   same content hashes used everywhere else — see _i18n_demo.py.

   The mid-conversation language switch is the point of the whole demo,
   so the language it switches *to* is chosen at run time: it must not
   be the language the visitor is already reading the site in.
================================================================ */
(function () {
  "use strict";

  var CFG = window.OD_CONFIG || {};

  function T(key, fallback) {
    try {
      if (window.OD_i18n && typeof window.OD_i18n.t === "function") {
        var v = window.OD_i18n.t(key, fallback);
        if (v) return v;
      }
    } catch (e) {}
    return fallback;
  }

  function lang() {
    try {
      if (window.OD_i18n && typeof window.OD_i18n.lang === "function") return window.OD_i18n.lang();
    } catch (e) {}
    return "en";
  }

  /* A translatable line: key + the English it was hashed from. */
  function S(k, en) { return { k: k, en: en }; }
  function tx(s) { return typeof s === "string" ? s : T(s.k, s.en); }

  /* ------------------------------------------------------------ VIDEO */
  function renderVideo() {
    var host = document.getElementById("od-video");
    if (!host) return;
    var d = CFG.demo || {};
    var type = (d.type || "").toLowerCase();
    var src = d.src || "";

    if (!type || !src) {
      host.innerHTML =
        '<div class="video-soon">' +
        '<div class="video-soon-ic"><svg viewBox="0 0 24 24" fill="currentColor" width="30" height="30"><path d="M8 5.14v13.72L19 12z"/></svg></div>' +
        '<div class="video-soon-t" data-i18n="kae0bea50">Demo video coming soon</div>' +
        '<div class="video-soon-s" data-i18n="k86227053">In the meantime, try the live demo below — it works right now.</div>' +
        "</div>";
      return;
    }

    var html = "";
    if (type === "mp4") {
      html = '<video class="video-el" controls playsinline preload="metadata"' +
             (d.poster ? ' poster="' + d.poster + '"' : "") +
             '><source src="' + src + '" type="video/mp4"></video>';
    } else if (type === "youtube") {
      html = '<iframe class="video-el" src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(src) +
             '" title="Ownerdeck demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
    } else if (type === "loom") {
      html = '<iframe class="video-el" src="https://www.loom.com/embed/' + encodeURIComponent(src) +
             '" title="Ownerdeck demo" frameborder="0" allowfullscreen></iframe>';
    } else if (type === "vimeo") {
      html = '<iframe class="video-el" src="https://player.vimeo.com/video/' + encodeURIComponent(src) +
             '" title="Ownerdeck demo" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>';
    }
    host.innerHTML = '<div class="video-frame">' + html + "</div>";
  }

  /* -------------------------------------------------------------- BOT */

  /* The language-detection demo. Whichever one runs, the customer's message
     and the bot's reply stay in that language on purpose — translating them
     would erase the thing being demonstrated. */
  var LANG_DEMOS = {
    ru: {
      label: S("k8b93d879", "Try asking in Russian"), flag: "🇷🇺",
      send: "Здравствуйте! Вы говорите по-русски?",
      bot: [
        "Конечно! Отвечаю на вашем языке 🇷🇺",
        "Закат-круиз в пятницу в 18:00 — осталось 6 мест, €35 с человека. Забронировать?"
      ],
      yes: "Да, на двоих"
    },
    de: {
      label: S("kbc6b9752", "Try asking in German"), flag: "🇩🇪",
      send: "Hallo! Sprechen Sie Deutsch?",
      bot: [
        "Natürlich! Ich antworte in Ihrer Sprache 🇩🇪",
        "Die Sunset-Cruise am Freitag um 18:00 Uhr hat noch 6 Plätze — 35 € pro Person. Soll ich reservieren?"
      ],
      yes: "Ja, für zwei"
    }
  };

  // Showing a Russian visitor that it can answer in Russian proves nothing.
  function langDemo() {
    var cur = lang();
    if (cur === "ru") return LANG_DEMOS.de;
    if (cur === "de") return LANG_DEMOS.ru;
    return LANG_DEMOS.ru;
  }

  var LANG_OPTION = { langTest: true, to: "langswitch" };

  var SCRIPT = {
    start: {
      bot: [S("kf6d3e02f", "Hey! 👋 I'm Ownerdeck, answering for a demo business — Blue Bay Tours. Ask me what a real customer would ask.")],
      options: [
        { text: S("ka3d9b541", "Any space on the sunset cruise Friday?"), to: "availability" },
        { text: S("kebf737eb", "How much for 2 people?"), to: "price" },
        LANG_OPTION
      ]
    },
    availability: {
      bot: [
        S("k6f87d995", "Friday's 18:00 sunset cruise has 6 seats left — €35 per person."),
        S("k7ede8f2c", "Want me to hold a couple for you?")
      ],
      options: [
        { text: S("kc1d7d8b5", "Yes, 2 people please"), to: "hold" },
        { text: S("k15a7fd3c", "What's included?"), to: "included" }
      ]
    },
    price: {
      bot: [
        S("k6325a6c8", "€35 per person — so €70 for two."),
        S("kf5e66c9f", "That covers hotel pickup, a welcome drink and the full 2-hour cruise.")
      ],
      options: [
        { text: S("k640f86e7", "Great, Friday works"), to: "hold" },
        LANG_OPTION
      ]
    },
    included: {
      bot: [
        S("k10e2fe7f", "Pickup from your hotel, a welcome drink, two hours on the water and a swim stop."),
        S("kdda3faf0", "Shall I put two seats down for Friday?")
      ],
      options: [
        { text: S("k5cb9edc7", "Yes please, book it"), to: "hold" }
      ]
    },
    hold: {
      bot: [
        S("ke718c10f", "Done ✓ Booking #TC-2291 — Friday 18:00, 2 seats, hotel pickup included."),
        S("k3e799bdd", "Confirmation sent, and I've pinged the owner.")
      ],
      end: true
    }
  };

  /* Built fresh each time so it follows the language the visitor is on now. */
  function langSwitchNode() {
    var d = langDemo();
    return {
      bot: d.bot,
      note: S("k6560e73c", "Language auto-detected — no setup needed"),
      options: [
        { text: d.yes, to: "hold" },
        { text: S("k1315c0b8", "Switch back"), to: "included" }
      ]
    };
  }

  var bot = {
    host: null, msgs: null, opts: null, node: "start", busy: false, seq: 0,

    init: function () {
      this.host = document.getElementById("od-bot");
      if (!this.host) return;
      this.host.innerHTML =
        '<div class="bot-head">' +
          '<div class="bot-av">B</div>' +
          '<div><div class="bot-name">Blue Bay Tours</div>' +
          '<div class="bot-status"><span data-i18n="kff796f03">Ownerdeck · answering now</span></div></div>' +
          '<button class="bot-restart" type="button" data-i18n="k129b767a">Start over</button>' +
        '</div>' +
        '<div class="bot-msgs" id="od-bot-msgs"></div>' +
        '<div class="bot-opts" id="od-bot-opts"></div>';
      this.msgs = this.host.querySelector("#od-bot-msgs");
      this.opts = this.host.querySelector("#od-bot-opts");
      var self = this;
      this.host.querySelector(".bot-restart").addEventListener("click", function () { self.reset(); });
      this.run("start");
    },

    reset: function () {
      if (!this.msgs) return;
      this.seq++;                 // strands any typing timer from the old run
      this.msgs.innerHTML = "";
      this.opts.innerHTML = "";
      this.busy = false;
      this.run("start");
    },

    esc: function (s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    },

    add: function (cls, text) {
      var d = document.createElement("div");
      d.className = "bm " + cls;
      d.innerHTML = this.esc(text);
      this.msgs.appendChild(d);
      this.scroll();
      return d;
    },

    note: function (text) {
      var d = document.createElement("div");
      d.className = "bm-note";
      d.innerHTML = "🌐 " + this.esc(text);
      this.msgs.appendChild(d);
      this.scroll();
    },

    // Scroll after layout has flushed — reading scrollHeight in the same
    // tick as the appendChild gives a stale value, which left the newest
    // message off-screen once the transcript was long enough to scroll.
    scroll: function () {
      var m = this.msgs;
      if (!m) return;
      var go = function () { m.scrollTop = m.scrollHeight; };
      go();
      if (window.requestAnimationFrame) requestAnimationFrame(function(){ requestAnimationFrame(go); });
    },

    typing: function () {
      var d = document.createElement("div");
      d.className = "bm bm-bot bm-typing";
      d.innerHTML = "<span></span><span></span><span></span>";
      this.msgs.appendChild(d);
      this.scroll();
      return d;
    },

    run: function (key) {
      var node = key === "langswitch" ? langSwitchNode() : SCRIPT[key];
      if (!node) return;
      this.node = key;
      this.busy = true;
      this.opts.innerHTML = "";
      var self = this;
      var mine = this.seq;        // a reset mid-conversation invalidates this run
      var i = 0;

      function next() {
        if (mine !== self.seq) return;
        if (i >= node.bot.length) {
          if (node.note) self.note(tx(node.note));
          self.busy = false;
          if (node.end) { self.finish(); } else { self.showOptions(node.options); }
          return;
        }
        var line = tx(node.bot[i]);
        var t = self.typing();
        var delay = Math.min(1100, 380 + line.length * 9);
        setTimeout(function () {
          if (mine !== self.seq) { t.remove(); return; }
          t.remove();
          self.add("bm-bot", line);
          i++;
          setTimeout(next, 260);
        }, delay);
      }
      setTimeout(next, 320);
    },

    showOptions: function (options) {
      if (!options) return;
      var self = this;
      options.forEach(function (o) {
        var d = o.langTest ? langDemo() : null;
        var label = d ? d.flag + " " + tx(d.label) : tx(o.text);
        // `send` lets the button label differ from the message actually sent
        var send = d ? d.send : (o.send || label);

        var b = document.createElement("button");
        b.type = "button";
        b.className = "bot-opt";
        b.textContent = label;
        b.addEventListener("click", function () {
          if (self.busy) return;
          self.opts.innerHTML = "";
          self.add("bm-me", send);
          self.run(o.to);
        });
        self.opts.appendChild(b);
      });
    },

    finish: function () {
      var wrap = document.createElement("div");
      wrap.className = "bot-done";
      wrap.innerHTML =
        '<div class="bot-done-t" data-i18n="k4f905fc9">That whole conversation — no human involved.</div>' +
        '<div class="bot-done-s" data-i18n="kae1e5b69">This is a preset demo. The real thing uses your services, prices and availability.</div>';
      this.opts.appendChild(wrap);
      var jump = document.getElementById("od-channels");
      if (jump) jump.classList.add("live");
      if (window.OD_i18n && window.OD_i18n.refresh) window.OD_i18n.refresh();
    }
  };

  /* --------------------------------------------------------- CHANNELS */
  function renderChannels() {
    var host = document.getElementById("od-channels");
    if (!host) return;

    var out = [];
    var msg = T("kc45ef3bf", "Hi! I saw the Ownerdeck demo and I'd like to know more.");

    if (/^\d{8,15}$/.test(CFG.whatsappNumber || "")) {
      out.push({
        cls: "ch-wa",
        href: "https://wa.me/" + CFG.whatsappNumber + "?text=" + encodeURIComponent(msg),
        label: "WhatsApp",
        icon: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.14-.14.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35zM12.05 21.5h-.01a9.5 9.5 0 0 1-4.84-1.33l-.35-.2-3.6.94.96-3.5-.23-.36a9.46 9.46 0 0 1-1.45-5.05c0-5.24 4.27-9.5 9.52-9.5 2.54 0 4.93.99 6.73 2.79a9.44 9.44 0 0 1 2.79 6.72c0 5.24-4.27 9.5-9.52 9.5zm8.1-17.6A11.4 11.4 0 0 0 12.05.5C5.8.5.72 5.57.72 11.8c0 2.08.55 4.11 1.58 5.9L.62 23.5l5.95-1.56a11.35 11.35 0 0 0 5.47 1.39h.01c6.24 0 11.32-5.07 11.33-11.3a11.26 11.26 0 0 0-3.32-8z"/></svg>'
      });
    }
    if (CFG.instagram) {
      out.push({
        cls: "ch-ig",
        href: CFG.instagram,
        label: "Instagram",
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>'
      });
    }
    if ((CFG.telegramHandle || "").replace(/^@/, "")) {
      out.push({
        cls: "ch-tg",
        href: "https://t.me/" + (CFG.telegramHandle || "").replace(/^@/, ""),
        label: "Telegram",
        icon: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.3 18.8 19c-.2 1-.9 1.3-1.7.8l-4.7-3.5-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.8 8.8-8c.4-.3-.1-.5-.6-.2L6.9 13.2 2.3 11.8c-1-.3-1-1 .2-1.5l18-7c.8-.3 1.6.2 1.4 1z"/></svg>'
      });
    }
    if (CFG.email) {
      out.push({
        cls: "ch-em",
        href: "mailto:" + CFG.email + "?subject=" + encodeURIComponent("Ownerdeck enquiry"),
        label: "Email",
        icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 7 9 6 9-6"/></svg>'
      });
    }

    host.innerHTML =
      '<div class="ch-title" data-i18n="k8116b768">Like what you saw? Message me directly.</div>' +
      '<div class="ch-sub" data-i18n="kd6193cc4">Pick whichever you actually use — I reply personally.</div>' +
      '<div class="ch-row">' +
        out.map(function (c) {
          return '<a class="ch ' + c.cls + '" href="' + c.href + '"' +
                 (c.cls === "ch-em" ? "" : ' target="_blank" rel="noopener"') +
                 '>' + c.icon + "<span>" + c.label + "</span></a>";
        }).join("") +
      "</div>";
  }

  function init() {
    renderVideo();
    bot.init();
    renderChannels();
    if (window.OD_i18n && window.OD_i18n.refresh) window.OD_i18n.refresh();

    /* A transcript half-typed in the old language reads as a bug, and the
       prefilled contact message is baked into an href. Redraw both. */
    if (window.OD_i18n && window.OD_i18n.onChange) {
      window.OD_i18n.onChange(function () {
        bot.reset();
        renderChannels();
        window.OD_i18n.refresh();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
