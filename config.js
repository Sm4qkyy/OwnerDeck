/* ================================================================
   OWNERDECK — SITE CONFIG
   This is the only file you need to edit to switch things on.
   Anything left empty stays hidden on the site (nothing breaks).
================================================================ */
window.OD_CONFIG = {

  /* ---------------------------------------------------------------
     1) DEMO VIDEO  — record it, then fill this in.

     Pick ONE type:
       type: "mp4"      src: "demo.mp4"          (drop the file in this folder)
       type: "youtube"  src: "dQw4w9WgXcQ"      (just the video ID from the URL)
       type: "loom"     src: "a1b2c3d4e5f6"     (the ID after /share/)
       type: "vimeo"    src: "123456789"        (the numeric ID)

     Leave type empty and a tidy "coming soon" card shows instead.
     TIP: for anything over ~20 MB use YouTube (unlisted) or Loom —
     much faster for visitors than a big file on the site.
  --------------------------------------------------------------- */
  demo: {
    type: "",
    src: "",
    poster: ""   // optional image shown before play, e.g. "demo-poster.png"
  },

  /* ---------------------------------------------------------------
     2) CONTACT CHANNELS — buttons appear only when filled in.
  --------------------------------------------------------------- */
  whatsappNumber: "",        // digits only, country code, no + or spaces: "35799123456"
  telegramHandle: "",        // without the @, e.g. "ownerdeckcy"
  instagram: "https://www.instagram.com/ownerdeckcy/",
  tiktok: "https://www.tiktok.com/@ownerdeckcy",
  email: "mark@ownerdeck.com",

  /* ---------------------------------------------------------------
     3) Floating "Try it live" button (bottom-right, all pages).
        Uses whatsappNumber above. Set to false to hide it entirely.
  --------------------------------------------------------------- */
  floatingButton: true
};
