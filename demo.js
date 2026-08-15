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
      inner = '<video class="video-el" controls playsinline preload="metadata"' +
              (d.poster ? ' poster="' + d.poster + '"' : "") +
              '><source src="' + src + '" type="video/mp4">' +
              'Your browser cannot play this video.</video>';
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
