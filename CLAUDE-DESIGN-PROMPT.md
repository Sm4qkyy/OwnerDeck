# Ownerdeck — brief for a design tool

Paste the block below into Claude Design (or any image/design tool). It is
written to be self-contained: it repeats the palette and type rather than
referring to this repo, so it works with no other context.

Four assets are worth having, in this order of value:

1. **Logo mark** — there isn't one. The site currently sets the word "Ownerdeck"
   in Fraunces, which is fine but generic.
2. **Favicon** — `favicon.png` is still the old teal brand and appears in every
   browser tab.
3. **OG image** — `og-image.png` is still the old teal brand and is what shows
   on every WhatsApp and LinkedIn share.
4. **Spot illustrations** — optional. The site's line drawings are hand-written
   SVG and hold up; only replace them if the tool produces something better.

---

## The prompt

> I need brand assets for **Ownerdeck**, a small studio that builds and runs the
> online side of small owner-operated businesses — the website, the database
> behind it, an AI chat assistant on WhatsApp, the bookings, and the Google
> listing. The customers are car rental firms, boat charters, villas, clinics,
> salons and guesthouses, mostly around the Mediterranean. The buyer is the
> owner, not a marketing department.
>
> **The name is the idea.** Ownerdeck is a *deck of cards*: the owner starts
> with a hand of services and adds cards as they grow. The design already uses
> a loosely fanned hand of five cards as its one memorable image. Any mark
> should come from that idea — but abstractly. **No suits, no pips, no aces,
> no casino or poker imagery whatsoever.** Think of a hand of plain rectangles
> held slightly fanned, or the overlapping edges of stacked cards.
>
> **Palette — use these exact values and nothing else.**
> ```
> bone      #F7F4EF   page background, never pure white
> bone-2    #EFE9E1   raised surfaces
> ink       #1F1D1A   text, warm near-black, never #000
> ink-soft  #6B6560   secondary text
> rule      #E0D8CD   hairlines
> clay      #C4643C   the single brand accent
> clay-deep #A84F2C   accent when it needs to carry text
> ```
> There is also a dark mode: ground `#17140F`, text `#F2ECE1`, accent lightened
> to `#E08A5F`. Any mark must work on both `#F7F4EF` and `#17140F`.
>
> These are Mediterranean colours — terracotta, bone, olive — chosen so the
> brand feels native to a business owner in Cyprus rather than to Silicon
> Valley. Keep that.
>
> **Type.** Headlines are **Fraunces** (variable, soft axis low, wonk on) —
> warm, slightly hand-cut, not decorative. Body is **Switzer**. If you need a
> wordmark, set "Ownerdeck" in Fraunces SemiBold with tight negative tracking,
> one word, lowercase d.
>
> **Style rules, all hard:**
> - Flat colour only. No gradients, no glows, no drop shadows, no bevels.
> - No glassmorphism, no 3D, no isometric.
> - No stock photography and no photorealism.
> - Nothing that looks like generic AI output: no purple-blue gradients, no
>   neon, no floating translucent orbs.
> - Small corner radius if any — 4 to 6px at normal scale. Never a pill.
> - It should look *printed* rather than *digital*. Letterpress, not neon.
>
> **Deliver, as separate assets:**
>
> 1. **Logo mark**, square, on transparent. Abstract fanned-cards idea. Must
>    stay legible at 32×32 and at 512×512. Give me it in clay `#C4643C` on
>    transparent, and a second version in `#F2ECE1` for dark backgrounds.
>
> 2. **Horizontal lockup** — mark plus the word "Ownerdeck" in Fraunces.
>    Light and dark versions.
>
> 3. **Favicon**, 512×512 PNG. Just the mark, generous padding, on a solid
>    `#F7F4EF` ground so it reads as a tile in a browser tab.
>
> 4. **Open Graph image**, exactly 1200×630 PNG. Ground `#F7F4EF`. The lockup
>    upper-left, and the line **"We build the online side of your business."**
>    set in Fraunces, large, in `#1F1D1A`, occupying the left two-thirds. On
>    the right, the fanned hand of five cards as flat outlined rectangles in
>    portrait ratio, each with a small square of colour in its corner — using
>    `#C4643C`, `#6E7A5A`, `#3F6B6B`, `#C89B4A`, `#7A5C6B` in that order. Cards
>    rotated only 2–4 degrees each, overlapping slightly, set down by hand
>    rather than aligned to a grid. Generous whitespace. No other text.
>
> Give me SVG wherever the asset is vector, PNG at 2x for anything raster.

---

## After the assets arrive

Drop them into the repo root and they take effect immediately:

| File | Replaces | Referenced by |
|---|---|---|
| `favicon.png` | old teal mark | every page, `<link rel="icon">` |
| `og-image.png` | old teal banner | every page's `og:image` and `twitter:image` |

The Content-Security-Policy allows `img-src 'self' data:` only, so every image
must be served from the site itself. Do not link to a CDN — it will be blocked.

If you get an SVG logo mark, tell me and I will inline it into the header in
place of the Fraunces wordmark, so it scales and recolours with the theme
instead of being a fixed-colour bitmap.
