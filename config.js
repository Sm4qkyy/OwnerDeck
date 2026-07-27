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
  /* Used ONLY by the WhatsApp button on the final step of demo.html.
     The number is never printed anywhere on the site — no "Talk to Mark"
     CTAs, nothing in the footer, nothing in the schema. Blank this out and
     that button disappears, leaving Instagram + email as the contact route. */
  whatsappNumber: "35796922259",

  /* The "Try the live demo" buttons (8 of them) point here.
     This should be a SEPARATE line running the demo assistant, not Mark's
     personal number. Until it's set, those buttons fall back to
     whatsappNumber above with a pre-filled message, so nothing is broken. */
  demoNumber: "",
  telegramHandle: "",        // without the @, e.g. "ownerdeckcy"
  instagram: "https://www.instagram.com/ownerdeckcy/",
  tiktok: "https://www.tiktok.com/@ownerdeckcy",
  email: "mark@ownerdeck.com",

  /* ---------------------------------------------------------------
     3) Floating "Try it live" button (bottom-right, all pages).

     OFF deliberately: the number should only appear at the final step
     of the demo flow (demo.html step 3), so visitors watch and try it
     before they get the contact details. Flip to true to bring it back.
  --------------------------------------------------------------- */
  floatingButton: false
};
