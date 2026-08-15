# Ownerdeck — complete build brief

Paste everything between the rules into another AI. It is written to be
self-contained: it assumes no access to the existing repo and repeats every
value it depends on.

---

## THE BRIEF

You are building the marketing website for **Ownerdeck**, a small studio that
builds and runs the online side of small owner-operated businesses.

### What the business actually does

Ownerdeck builds five things. A client takes the ones they need and adds the
rest later:

| Service | What it is |
|---|---|
| **Site** | A fast website, designed and built for them — not a template. It reads live from their database, so the prices on it are the prices they actually charge. |
| **Data** | One database holding services, prices, availability, customers and bookings, instead of a spreadsheet plus a notebook plus the owner's memory. |
| **Answer** | An AI chat assistant on WhatsApp, Instagram DMs and their own site. Replies in the customer's language at any hour, quoting from their real prices and real availability. |
| **Book** | Real availability, confirmations, deposits, calendar. The booking lands on the owner's phone the moment it happens. |
| **Reach** | Google Business Profile set up properly, and a review request sent after every booking. |

**The differentiator is the wiring, not any one part.** Anyone can build a
website. The pitch is that one set of facts drives the site, the assistant and
the booking confirmation, so changing a price once changes it everywhere. Make
that idea land visually, not just in a sentence.

**The name is a deck of cards.** The owner starts with a hand and adds cards as
they grow. This drives the design. Abstract only — **no suits, no pips, no
casino imagery ever.**

### Who buys it

Owner-operators of small businesses, mostly around the Mediterranean: car,
scooter and buggy rental; boat charters and tours; watersports and diving;
villas and short-term rentals; estate agencies; private clinics; salons,
barbers and spas; guesthouses and small hotels.

The reader is the owner, on a phone, not a marketing department. They are not
technical. They are sceptical of agencies.

### Pricing — put these exact figures on the page

| Plan | Build | Monthly | Includes |
|---|---|---|---|
| **Answer** | €600 | €150 | The AI chat assistant only |
| **Deck** | €1,800 | €249 | Site + Data + Answer + Book — **mark this as the common choice** |
| **Full Deck** | €2,400 | €299 | All five |

Plus one line beneath: *Starting from nothing? Everything built from zero in a
week, no build fee, €249 a month on a twelve month term.*

No VAT (not VAT registered). The monthly covers hosting, the database, the
assistant running, backups and changes. The client's site, data and phone
number stay theirs if they leave.

> **Why setup + monthly, in case you are tempted to simplify it.** A monthly-only
> price never repays the build. A website-and-database build is roughly 36 hours;
> at €249/month it takes about eleven months just to break even at cost, and a
> client who leaves at month six means the work was done for nothing. The setup
> fee covers the hours; the margin lives in the monthly.

### The only real proof point

> A car rental operator in Limassol, built and run by Ownerdeck, live at €150 a
> month. Last month the after-hours cover booked **14 enquiries** that came in
> between 9pm and 8am — ones the owner would otherwise have picked up the next
> morning.

Use it prominently, stated quietly and factually. **Do not invent any other
statistic, testimonial, client logo, or "trusted by N businesses" claim.** The
only numbers on the site are the prices above and that 14.

---

## HARD TECHNICAL CONSTRAINTS

These are not preferences. The site is live on Vercel behind Cloudflare.

1. **Static HTML, CSS and vanilla JS. No framework, no build step, no npm.**
   Hand-written `.html` files served directly.
2. **No external runtime dependencies.** No CDN scripts, no jQuery, no
   Tailwind CDN, no React, no component library.
3. **A Content-Security-Policy is already deployed and cannot be changed:**
   ```
   default-src 'self'; script-src 'self' 'unsafe-inline';
   style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
   font-src 'self' https://fonts.gstatic.com data:;
   img-src 'self' data:; connect-src 'self'
   ```
   Consequences you must design around:
   - **Every image must be downloaded and served from the site itself.** No
     hotlinking to Unsplash, Cloudinary or anything else — it will be blocked.
   - **Fonts must be self-hosted** or come from Google Fonts. Fontshare and
     other CDNs are blocked.
4. `cleanUrls` is on — link to `/terms`, not `/terms.html`.
5. Target Lighthouse performance 95+, accessibility 100.

---

## VISUAL DIRECTION

### Palette — use these exact values

Dark is the primary look. Both themes must exist, with a toggle, defaulting to
the visitor's system preference and remembering an explicit choice.

**Dark (primary):**
```
--bg           #0A0D14   near-black with a blue cast, never pure #000
--bg-raised    #121822   raised surfaces, alternating sections
--ink          #E9EEF7   body text
--ink-soft     #95A1B5   secondary text
--rule         #1E2733   hairlines
--accent       #5B9CFF   blue: rules, focus rings, swatches
--accent-deep  #8AB9FF   blue for TEXT and filled buttons
--spark        #FF8A3D   orange, the hint
--spark-deep   #FFA463   orange when it carries text
```

**Light:**
```
--bg           #F7F9FC
--bg-raised    #ECF1F7
--ink          #0C111A
--ink-soft     #525C6B
--rule         #DCE3EC
--accent       #2563EB
--accent-deep  #1D4ED8
--spark        #D9541A
--spark-deep   #B7440F
```

Every pair above has been measured and passes WCAG AA:

```
DARK   ink 16.69:1 · ink-soft 7.44:1 · accent-deep as text 9.68:1
       bg on accent-deep 9.68:1 · spark-deep as text 9.94:1
LIGHT  ink 17.93:1 · ink-soft 6.42:1 · accent-deep as text 6.35:1
       bg on accent-deep 6.35:1 · spark-deep as text 5.18:1
```

**The two-tier accent split is load-bearing.** `--accent` is bright enough for
rules, focus rings and decorative swatches but not always for small text;
`--accent-deep` is the one that carries text and button labels. Do not collapse
them into one token — re-measure if you change either.

**Orange is a hint, not a second brand colour.** Use it for exactly one thing
per screen: the highlighted plan, or a single figure, or the active state.
Never orange and blue competing for attention in the same block.

Card identity tints (small decorative squares only, never backgrounds):

```
        light      dark
site    #2563EB    #5B9CFF
data    #0E7490    #22C7E0
answer  #D9541A    #FF8A3D
book    #0F766E    #2DD4BF
reach   #475569    #94A3B8
```

Declare every colour once in `:root` (and once more in the dark override). **No
hex literal anywhere else in the CSS or the HTML.**

### Type

- Headlines: a serif or a high-character sans with real personality. **Not
  Inter, not Roboto, not system-ui, not Arial.** Self-host it.
- Body: a clean geometric or neo-grotesque sans, self-hosted.
- Headlines large and tight — around 1.02 line height, tracking about
  `-0.03em`, scaling to roughly 5rem on desktop.
- Body 1.6 line height, maximum 68 characters per line.
- Contrast between heading levels should be strong. A timid type scale is the
  single clearest sign of a template.

### Layout

- Long vertical page. Sections separated by whitespace and hairline rules, not
  boxes and shadows.
- **Asymmetry.** Not every section centred. Use 7:5 and 5:7 splits.
- More space between sections than inside them.
- Mobile first. Most readers are on a phone.
- Small corner radius throughout, 4–6px. Never a pill.

---

## IMAGES

The site needs real imagery and has none. Two rules:

1. **Everything must be downloaded and served locally** (see the CSP above).
2. **No business-people stock photography.** Smiling teams around a laptop is
   the strongest "generated site" signal there is, and the whole point is to
   avoid looking generated.

Use **real subject photography** of the trades themselves — a boat on water, a
salon chair, a set of car keys, a villa pool, a clinic room — plus texture and
material shots. Specific beats generic.

**Where to get them, licensed cleanly:** the Openverse API needs no key and can
filter to public domain, which carries no attribution requirement:

```
https://api.openverse.org/v1/images/?q=sailboat+sea&license=cc0,pdm&page_size=5
```

Read `results[].url` for the file, download it, store it in `img/`, and record
`title`, `creator` and `license` in a `img/CREDITS.md` even for public-domain
work. Verify before shipping that every image is genuinely cc0/pdm — do not
ship a CC-BY image without the required credit.

Resize to no more than 1600px on the long edge, and serve `.webp` with a
`.jpg` fallback if you can. Every `<img>` needs a real `alt` describing the
subject, and `loading="lazy"` on anything below the fold.

---

## PAGE STRUCTURE

In order. Each section needs a visual, not only text — the most common failure
of this page is that it reads as a wall of paragraphs.

1. **Hero.** One sentence: *We build the online side of your business.* Then a
   plain-English subhead naming all five services. One primary action —
   WhatsApp — and one quiet secondary. The fanned hand of five cards as the
   signature image.
2. **What we build.** The five services, each with an icon, a real description,
   and who it is for.
3. **The work, shown.** The most important section. Three mockups side by side —
   a browser window showing a real site layout, the database table behind it,
   and the assistant answering from both — proving "one set of facts, three
   places it shows up." Build these in HTML and CSS, not as screenshots.
4. **Why owners call.** Four separate failures: a stale website nobody has
   opened in years; prices right in one place and wrong in three; enquiries
   arriving at 11pm; a Google listing never claimed.
5. **How we work.** Three steps: we talk about the business; we build and test
   it; we run it. Database first, site on top, assistant wired to both.
6. **Where we stop.** Honest limits: not a marketing agency, does not handle
   their money, does not build apps, the assistant never invents a price and
   hands anything it does not know to the owner.
7. **Proof.** The Limassol operator and the 14 bookings. Quiet, factual, not a
   testimonial block.
8. **Pricing.** Three columns, Deck marked as the common choice, the
   new-business line underneath.
9. **Questions.** Ten, written for someone buying a build: *I already have a
   website, do I need a new one · who owns the site and the data · do I need a
   new phone number · what if the assistant says something wrong · can I take
   over a conversation · what languages · how long does it take · what does the
   monthly cover · what happens when my prices change · who is behind this.*
   Build on `<details>`/`<summary>` so it works with no JavaScript.
10. **Who it is for.** The eight trades, each with the questions that trade
    actually gets — a clinic sees slots and preparation, a charter sees group
    size and the weather call. A bare list says *not you* to seven of the eight.
11. **Close.** One action.

Header: sticky, wordmark left, nav, theme toggle, one CTA. On mobile collapse
to wordmark plus two icons, with a hamburger opening a full-screen menu.

Footer: four columns — what we build, reading, contact, legal — not one line.

---

## MOTION

Modern but restrained. Everything below is decoration; the page must be
complete and readable with the JavaScript deleted.

- Scroll reveals, staggered, subtle rise and fade.
- The hero cards deal in on load, then tilt slightly toward the pointer.
- A spotlight following the cursor across the pricing cards.
- The primary button's arrow slides on hover.
- A reading-progress hairline.
- Optional: a canvas dot field behind the hero that leans away from the pointer.

**Four rules that decide whether this feels expensive or cheap:**

1. **Never transition the property you are also setting from a pointer event.**
   A 300ms ease fighting a 120Hz pointer *is* what "choppy" means. Drop the
   transition while tracking, restore it for the return.
2. **Never call `getBoundingClientRect()` inside a `pointermove` handler.** It
   forces a layout on every event. Measure once on `pointerenter`, cache it.
3. **Batch pointer updates with `requestAnimationFrame`.** One pending frame,
   not one write per event.
4. **Never use `@keyframes` with `fill-mode: both` on a property you also want
   to transition on hover.** The finished animation keeps ownership of that
   property and the hover silently does nothing. Use transitions.

Share one rAF-throttled scroll listener between the header state and the
progress bar rather than registering two.

`prefers-reduced-motion: reduce` must remove all of it, not shorten it.

---

## ACCESSIBILITY — non-negotiable

- Every contrast pair passes WCAG AA. Verify by calculation, not by eye.
- Exactly one `<h1>` per page; heading levels never skip.
- Visible focus states on everything interactive, in the accent colour.
- Every image has a real `alt`.
- Keyboard navigable throughout; a skip link to main content.
- **Never hide content behind a class only JavaScript can add.** If a reveal
  sets `opacity: 0`, scope it to a `.js` class set by an inline script in
  `<head>`, so a blocked or failed script leaves a complete page rather than a
  blank one.
- Decorative elements get `aria-hidden="true"`. Do not add `tabindex` to
  non-interactive cards — it creates empty tab stops.

---

## COPY RULES

Plain and specific. One person explaining something to another.

- **Say what you build.** "Website", "database", "AI chat assistant" are the
  words buyers search for. Use them.
- **Banned as fluff:** supercharge, seamless, effortless, unlock, revolutionise,
  game-changer, cutting-edge, best-in-class, leverage, synergy, one-stop shop,
  turnkey, and every "trusted by N businesses" formulation.
- No exclamation marks anywhere.
- Short sentences. Cut adjectives that carry no weight.
- Say the price. Never "contact us for pricing".
- Every claim must be true. Invent no statistic, client or testimonial.
- English only, but write the markup so a Greek translation can be added later
  without restructuring.

---

## THE "DOES NOT LOOK GENERATED" LIST

Every item here is a tell. None appear:

- Purple or blue-to-pink gradients, gradient text, gradient buttons
- Glassmorphism, frosted panels, blurred colour blobs
- Neon or glowing accents; `box-shadow` used as a glow
- Large drop shadows used for depth
- Inter, Roboto, or the default Tailwind palette
- Three identical feature cards in a row with an icon on top
- Emoji used as icons, anywhere
- Pill buttons with heavy border radius
- Animated counters, typewriter effects, marquees, parallax
- Stock photography of people in offices
- Fake logos, fake testimonials, invented statistics

---

## BEFORE YOU CALL IT DONE

Write a script that checks these against the built files rather than trusting
yourself:

- [ ] No hex literal outside the `:root` palette blocks, in CSS or HTML
- [ ] Every contrast pair recalculated and passing AA
- [ ] No banned word in any visible copy; no exclamation marks
- [ ] No emoji in any file
- [ ] Exactly one `<h1>` per page, no skipped heading levels
- [ ] Every `<img>` has a non-empty `alt`
- [ ] Every internal link and asset path resolves
- [ ] The page renders completely with JavaScript disabled
- [ ] The FAQ opens and closes with JavaScript disabled
- [ ] `prefers-reduced-motion` removes every transform and transition
- [ ] No image loads from an external origin
- [ ] Every image is cc0/pdm, or credited as its licence requires

Then look at it at 375px and at 1440px, in both themes.
