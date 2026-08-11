/* ================================================================
   Ownerdeck — conversion events on top of Vercel Web Analytics.

   Pageviews answer "how many". These answer "did they care": did they
   play the video, reach the demo, actually message the assistant, click
   through to WhatsApp. For a page whose whole job is to turn a curious
   owner into a conversation, the second question is the one worth money.

   Every selector here is checked against the current markup. The previous
   version targeted .contact-form, .btn-primary, .nav-cta and .lang-select
   — none of which survived the redesign, so it had been firing nothing
   into a script that was not loaded on any page anyone visits.

   Events appear in Vercel → Analytics → Events.
================================================================ */
(function () {
  "use strict";

  function track(name, props) {
    try {
      window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
      window.va("event", props ? Object.assign({ name: name }, props) : { name: name });
    } catch (e) {}
  }

  function sectionOf(el) {
    var s = el.closest && el.closest("section");
    if (!s) return "nav";
    return s.id || "body";
  }

  function init() {

    /* --- primary CTAs: which one earns the click, and from where --- */
    document.querySelectorAll(".od-btn--primary, .od-mmenu__cta").forEach(function (el) {
      el.addEventListener("click", function () {
        track("cta_click", { location: sectionOf(el) });
      });
    });

    /* --- demo video: started, and did they stay --- */
    var vid = document.querySelector("video.video-el");
    if (vid) {
      var marks = { 25: false, 50: false, 75: false, 90: false };
      vid.addEventListener("play", function () { track("video_play"); }, { once: true });
      vid.addEventListener("timeupdate", function () {
        if (!vid.duration) return;
        var pct = (vid.currentTime / vid.duration) * 100;
        Object.keys(marks).forEach(function (m) {
          if (!marks[m] && pct >= Number(m)) {
            marks[m] = true;
            track("video_progress", { percent: m });
          }
        });
      });
    }

    /* --- chat: opening it is intent, sending is engagement --- */
    document.addEventListener("click", function (e) {
      var t = e.target;
      if (t.closest && t.closest(".odc-launch")) track("chat_opened");
      var lang = t.closest && t.closest("[data-lang]");
      if (lang) track("lang_switch", { lang: lang.getAttribute("data-lang") });
    });

    /* --- leaving for a channel: the closest thing to a lead --- */
    document.querySelectorAll('a[href^="https://wa.me"], a[href^="mailto:"], a[href*="instagram.com"], a[href*="tiktok.com"]')
      .forEach(function (a) {
        a.addEventListener("click", function () {
          var h = a.getAttribute("href") || "";
          var ch = h.indexOf("wa.me") > -1 ? "whatsapp"
                 : h.indexOf("mailto:") === 0 ? "email"
                 : h.indexOf("instagram") > -1 ? "instagram" : "tiktok";
          track("contact_click", { channel: ch });
        });
      });

    /* --- how far down the page they actually got --- */
    var hit = {};
    var onScroll = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      if (max <= 0) return;
      var pct = Math.round((h.scrollTop / max) * 100);
      [25, 50, 75, 100].forEach(function (m) {
        if (!hit[m] && pct >= m) { hit[m] = true; track("scroll_depth", { percent: String(m) }); }
      });
      if (hit[100]) window.removeEventListener("scroll", onScroll);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
