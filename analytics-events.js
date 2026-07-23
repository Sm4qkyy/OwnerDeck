/* ================================================================
   Lightweight conversion tracking on top of Vercel Analytics.
   Fires custom events so you can see what actually converts, not just
   pageviews. Events show up in Vercel → Analytics → Events.
================================================================ */
(function () {
  "use strict";

  function track(name, props) {
    try {
      window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
      window.va("event", props ? Object.assign({ name: name }, props) : { name: name });
    } catch (e) {}
  }

  function init() {
    // Lead form submitted
    var form = document.querySelector(".contact-form");
    if (form) {
      form.addEventListener("submit", function () { track("lead_submit"); });
    }
    // CTA clicks — which button, from which section
    document.querySelectorAll(".btn-primary, .nav-cta, .nav-mobile-cta").forEach(function (el) {
      el.addEventListener("click", function () {
        var sec = el.closest("section");
        track("cta_click", { location: sec ? (sec.className.split(" ")[0] || "section") : "nav" });
      });
    });
    // Language switched
    document.querySelectorAll(".lang-select").forEach(function (sel) {
      sel.addEventListener("change", function () { track("lang_change", { lang: this.value }); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
