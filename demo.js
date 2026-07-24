/* ================================================================
   Ownerdeck — demo section
   1) Renders the demo video (or a "coming soon" card until configured)
   2) Runs an interactive, preset conversation so visitors feel it
   3) Renders "message me" buttons for the channels set in config.js

   The bot script is illustrative and stays in English across locales —
   it deliberately switches to Russian mid-conversation to show off
   automatic language detection.
================================================================ */
(function () {
  "use strict";

  var CFG = window.OD_CONFIG || {};

  function T(key, fallback) {
    try {
      if (window.OD_I18N && typeof window.OD_I18N.t === "function") {
        var v = window.OD_I18N.t(key);
        if (v) return v;
      }
    } catch (e) {}
    return fallback;
  }

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
        '<div class="video-soon-t" data-i18n="demo.soonTitle">Demo video coming soon</div>' +
        '<div class="video-soon-s" data-i18n="demo.soonSub">In the meantime, try the live demo below — it works right now.</div>' +
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
  var SCRIPT = {
    start: {
      bot: ["Hey! 👋 I'm Ownerdeck, answering for a demo business — Blue Bay Tours. Ask me what a real customer would ask."],
      options: [
        { text: "Any space on the sunset cruise Friday?", to: "availability" },
        { text: "How much for 2 people?", to: "price" },
        // Label is English so it's clearly a deliberate language test,
        // but the message actually sent is Russian.
        { text: "🇷🇺 Try asking in Russian", send: "Здравствуйте! Вы говорите по-русски?", to: "russian" }
      ]
    },
    availability: {
      bot: ["Friday's 18:00 sunset cruise has 6 seats left — €35 per person.", "Want me to hold a couple for you?"],
      options: [
        { text: "Yes, 2 people please", to: "hold" },
        { text: "What's included?", to: "included" }
      ]
    },
    price: {
      bot: ["€35 per person — so €70 for two.", "That covers hotel pickup, a welcome drink and the full 2-hour cruise."],
      options: [
        { text: "Great, Friday works", to: "hold" },
        { text: "🇷🇺 Try asking in Russian", send: "Вы говорите по-русски?", to: "russian" }
      ]
    },
    russian: {
      bot: ["Конечно! Отвечаю на вашем языке 🇷🇺", "Закат-круиз в пятницу в 18:00 — осталось 6 мест, €35 с человека. Забронировать?"],
      note: "Language auto-detected — no setup needed",
      options: [
        { text: "Да, на двоих", to: "hold" },
        { text: "Back to English please", to: "included" }
      ]
    },
    included: {
      bot: ["Pickup from any Protaras hotel, a welcome drink, two hours on the water and a swim stop.", "Shall I put two seats down for Friday?"],
      options: [
        { text: "Yes please, book it", to: "hold" }
      ]
    },
    hold: {
      bot: [
        "Done ✓ Booking #TC-2291 — Friday 18:00, 2 seats, hotel pickup included.",
        "Confirmation sent, and I've pinged the owner."
      ],
      end: true
    }
  };

  var bot = {
    host: null, msgs: null, opts: null, node: "start", busy: false,

    init: function () {
      this.host = document.getElementById("od-bot");
      if (!this.host) return;
      this.host.innerHTML =
        '<div class="bot-head">' +
          '<div class="bot-av">B</div>' +
          '<div><div class="bot-name">Blue Bay Tours</div>' +
          '<div class="bot-status"><span data-i18n="demo.botStatus">Ownerdeck · answering now</span></div></div>' +
          '<button class="bot-restart" type="button" data-i18n="demo.restart">Start over</button>' +
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

    scroll: function () { this.msgs.scrollTop = this.msgs.scrollHeight; },

    typing: function () {
      var d = document.createElement("div");
      d.className = "bm bm-bot bm-typing";
      d.innerHTML = "<span></span><span></span><span></span>";
      this.msgs.appendChild(d);
      this.scroll();
      return d;
    },

    run: function (key) {
      var node = SCRIPT[key];
      if (!node) return;
      this.node = key;
      this.busy = true;
      this.opts.innerHTML = "";
      var self = this;
      var i = 0;

      function next() {
        if (i >= node.bot.length) {
          if (node.note) self.note(node.note);
          self.busy = false;
          if (node.end) { self.finish(); } else { self.showOptions(node.options); }
          return;
        }
        var t = self.typing();
        var delay = Math.min(1100, 380 + node.bot[i].length * 9);
        setTimeout(function () {
          t.remove();
          self.add("bm-bot", node.bot[i]);
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
        var b = document.createElement("button");
        b.type = "button";
        b.className = "bot-opt";
        b.textContent = o.text;
        b.addEventListener("click", function () {
          if (self.busy) return;
          self.opts.innerHTML = "";
          // `send` lets the button label differ from the message sent
          self.add("bm-me", o.send || o.text);
          self.run(o.to);
        });
        self.opts.appendChild(b);
      });
    },

    finish: function () {
      var wrap = document.createElement("div");
      wrap.className = "bot-done";
      wrap.innerHTML =
        '<div class="bot-done-t" data-i18n="demo.doneTitle">That whole conversation — no human involved.</div>' +
        '<div class="bot-done-s" data-i18n="demo.doneSub">This is a preset demo. The real thing uses your services, prices and availability.</div>';
      this.opts.appendChild(wrap);
      var jump = document.getElementById("od-channels");
      if (jump) jump.classList.add("live");
      if (window.OD_I18N && window.OD_I18N.refresh) window.OD_I18N.refresh();
    }
  };

  /* --------------------------------------------------------- CHANNELS */
  function renderChannels() {
    var host = document.getElementById("od-channels");
    if (!host) return;

    var out = [];
    var msg = "Hi! I saw the Ownerdeck demo and I'd like to know more.";

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
      '<div class="ch-title" data-i18n="demo.channelsTitle">Like what you saw? Message me directly.</div>' +
      '<div class="ch-sub" data-i18n="demo.channelsSub">Pick whichever you actually use — I reply personally.</div>' +
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
    if (window.OD_I18N && window.OD_I18N.refresh) window.OD_I18N.refresh();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
