/* ================================================================
   Floating "Try it live" WhatsApp button (bottom-right, all pages).

   Configured in config.js -> whatsappNumber / floatingButton.
   Empty number = button stays hidden, so nothing broken ships.

   IMPORTANT: use a dedicated Ownerdeck demo line, NEVER a live client's
   number (a real client's chat would fill up with demo traffic).
================================================================ */
(function () {
  "use strict";

  // Number and on/off switch both live in config.js
  var CFG = window.OD_CONFIG || {};
  var DEMO_NUMBER = CFG.whatsappNumber || "";

  if (CFG.floatingButton === false) return;
  if (!/^\d{8,15}$/.test(DEMO_NUMBER)) return; // hidden until a valid number is set

  var lang = (function () {
    try { return (localStorage.getItem("od_lang") || document.documentElement.lang || "en").slice(0, 2); }
    catch (e) { return "en"; }
  })();
  var LABEL = { en: "Try it live", el: "Δοκιμάστε το ζωντανά", ru: "Попробовать вживую" };
  var MSG = { en: "Hi, I'm checking out OwnerDeck", el: "Γεια σας, ενδιαφέρομαι για το OwnerDeck", ru: "Здравствуйте, интересуюсь OwnerDeck" };
  var label = LABEL[lang] || LABEL.en;
  var href = "https://wa.me/" + DEMO_NUMBER + "?text=" + encodeURIComponent(MSG[lang] || MSG.en);

  var css =
    ".wa-fab{position:fixed;right:20px;bottom:20px;z-index:200;display:inline-flex;align-items:center;gap:10px;" +
    "background:#25D366;color:#fff;font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-weight:600;font-size:15px;" +
    "padding:13px 20px;border-radius:999px;box-shadow:0 14px 34px -10px rgba(37,211,102,.6);cursor:pointer;text-decoration:none;" +
    "transition:transform .2s,box-shadow .2s;}" +
    ".wa-fab:hover{transform:translateY(-2px);box-shadow:0 20px 44px -12px rgba(37,211,102,.75);}" +
    ".wa-fab svg{width:22px;height:22px;flex-shrink:0;}" +
    "@media(max-width:520px){.wa-fab{padding:14px;right:16px;bottom:16px;}.wa-fab span{display:none;}}";

  function mount() {
    var style = document.createElement("style"); style.textContent = css; document.head.appendChild(style);
    var a = document.createElement("a");
    a.href = href; a.target = "_blank"; a.rel = "noopener"; a.className = "wa-fab"; a.setAttribute("aria-label", label);
    a.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.14-.14.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35zM12.05 21.5h-.01a9.5 9.5 0 0 1-4.84-1.33l-.35-.2-3.6.94.96-3.5-.23-.36a9.46 9.46 0 0 1-1.45-5.05c0-5.24 4.27-9.5 9.52-9.5 2.54 0 4.93.99 6.73 2.79a9.44 9.44 0 0 1 2.79 6.72c0 5.24-4.27 9.5-9.52 9.5zm8.1-17.6A11.4 11.4 0 0 0 12.05.5C5.8.5.72 5.57.72 11.8c0 2.08.55 4.11 1.58 5.9L.62 23.5l5.95-1.56a11.35 11.35 0 0 0 5.47 1.39h.01c6.24 0 11.32-5.07 11.33-11.3a11.26 11.26 0 0 0-3.32-8z"/></svg><span>' + label + "</span>";
    document.body.appendChild(a);
  }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", mount); } else { mount(); }
})();
