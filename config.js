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
    type: "mp4",
    /* Version query, not decoration. A <video> keeps its own media cache and
       routinely ignores Cache-Control: no-store, so re-cutting the file is not
       enough to make a browser fetch it — the URL has to change. Bump this
       whenever demo.mp4 is replaced. */
    src: "demo.mp4?v=2",
    poster: "demo-poster.jpg?v=2"
  },

  /* ---------------------------------------------------------------
     2) CONTACT CHANNELS — buttons appear only when filled in.
  --------------------------------------------------------------- */
  /* Used ONLY by the WhatsApp button on the final step of demo.html.
     The number is never printed anywhere on the site — no "Talk to Mark"
     CTAs, nothing in the footer, nothing in the schema. Blank this out and
     that button disappears, leaving Instagram + email as the contact route. */
  whatsappNumber: "447520689685",

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
     LIVE AI CHAT
     The API key lives ONLY in Vercel env vars — never here, this file is
     public. See SECURITY-CHAT.md for the full setup and the spend cap.

       enabled          false to hide the chat everywhere
       floating         false to keep it only inside the demo (step 4)
       turnstileSiteKey Cloudflare Turnstile SITE key (public — safe here).
                        The SECRET key goes in Vercel env vars.
  --------------------------------------------------------------- */
  liveChat: {
    enabled: true,
    floating: true,
    endpoint: "/api/chat",
    turnstileSiteKey: "0x4AAAAAAD_9xwr6or8BKILz"
  },

  /* ---------------------------------------------------------------
     3) Floating "Try it live" button (bottom-right, all pages).

     OFF deliberately: the number should only appear at the final step
     of the demo flow (demo.html step 3), so visitors watch and try it
     before they get the contact details. Flip to true to bring it back.
  --------------------------------------------------------------- */
  floatingButton: false
};
