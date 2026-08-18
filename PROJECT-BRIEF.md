# Project Brief — Ownerdeck

> Written after the build rather than before it, which is the wrong order. It
> is here to make the decisions inspectable and to record where the site
> currently disagrees with its own rules. Conflicts are listed at the end
> rather than quietly resolved.

## What is this?
Ownerdeck builds and runs the online side of a small owner-operated business:
the website, the database behind it, an AI assistant that answers customers on
WhatsApp and Instagram, and bookings that land on the owner's phone. One person
builds it and the same person answers the messages.

## Goal
Start the funnel at `/start`. Three questions, then a €75 refundable deposit
that holds a build slot. Everything else on the site exists to get one button
pressed.

## Audience
- **Who they are:** Owner-operators in Cyprus. Rental first — cars, scooters,
  boats — then anyone with availability, a price and a booking. They run the
  business and answer the messages themselves.
- **What they care about:** Not losing the enquiry that arrived at 2am. Knowing
  the price before they have to ask for it. Being able to stop without a fight.
- **What they hate:** Being sold to by someone who has never run a fleet.
  Agencies with account managers and ticket queues. "Request a quote" with no
  numbers anywhere on the page. Software that needs them to change how they
  already work. Anything that reads like it was written by a committee.

## The subject's own world
Five things from the actual domain, taken from the live client's setup:

1. A WhatsApp thread timestamped 02:14, asking whether there is a jeep free
   tomorrow and what three days costs.
2. `ownerdeck-bot-data` — a Google Sheet with columns for timestamp, reference,
   car, pickup_date, dropoff_time, pickup_location, days, quoted_total, extras.
3. Booking references in the shape `VOY-1CMR3`, `VOY-1GUGA`.
4. Larnaca Airport as a pickup location, and quoted totals like €367 and €653.
5. The owner's phone face-down on a bedside table, doing the work.

**Two decisions that trace back to this list:**

- **The proof card is built as an instrument readout, not a banner.** A LIVE
  badge straddles its top border, then banded rows, hairline rules and tabular
  figures. That comes from item 2: the subject's world is a status line and a
  spreadsheet row, so evidence of work should look like a readout rather than
  an advertisement.
- **The monospace face carries every label, eyebrow and figure.** That comes
  from items 3 and 4 — reference codes and euro totals in a column. Mono is
  what this data already looks like where it actually lives.

## Aesthetic direction
**An instrument panel rather than a brochure.** Near-white ground, near-black
type, hairline rules with a cool blue-grey cast, uppercase mono labels, tabular
numerals, and one accent used strictly for wayfinding. The closest real-world
reference is a well-set financial statement or an aircraft checklist:
everything is a value with a label, nothing is decorated, and any colour
present is doing a job.

→ **Why this serves the audience:** they are sceptical of software and of the
people selling it. A page that reads like a readout implies the numbers on it
are measurements rather than claims. The restraint is the argument.

## Signature element
The live operator card in the hero. A pill reading `● LIVE · LIMASSOL` sits
across the card's top border rather than inside its padding — that detail is
what makes it read as a device with a light on it rather than a box. Three
measured figures, then a footer of standing facts: `Now live · 1`,
`Channel · WhatsApp`, `Status · Running`.

## Tone of voice
Concrete, plain, unhurried.

## References — two-brand remix
**Typography and spacing discipline from Stripe's documentation.** Steal: a
type scale held without exception, and figures set in mono so columns align.

**Instrumentation language from the Base44 build of this same site.** Steal:
the badge across the card edge, the header / metrics / footer banding, and the
blue-grey rule colour. Rejected from it: gold as text on white, which measured
2.46:1 and fails AA; and the sparkline, which needs thirty real daily figures
that do not exist.

Where the two disagree, the stricter spacing scale wins, and no colour ships
without a measured contrast ratio recorded beside it.

## Typography
- **Display:** Geist 600 — *see Conflicts, item 1.*
- **Body:** Geist 400/500 — *see Conflicts, item 1.*
- **Mono:** Geist Mono 400/500 — labels, eyebrows, figures, booking references.
- **Size scale:** hero display clamps 2.15–3.35rem; body never below 1rem; card
  labels 0.6875rem uppercase at 0.13em tracking. Tracking tightens as size
  grows: −0.035em on the h1, +0.16em on mono labels.

## Colour
- **Background:** `#FFFFFF` light, `#0B0B12` dark — *see Conflicts, item 2.*
- **Foreground:** `#09090B` (19.9:1) light, `#FAFAFA` (18.1:1) dark.
- **Primary accent:** `#1D4ED8` light, `#8FB3FF` dark. Spent on exactly four
  things — section eyebrows, the recommended plan flag, the payback number, and
  inline prose links. Not available as decoration.
- **Secondary:** `--gold #C5A059`, used only inside the dark LIVE pill, where it
  runs 7.8:1. It measures 2.46:1 on paper, so it never appears there.
  `--live #16803C` marks confirmed states.
- **Forbidden:** gold or accent as text on the light ground; anything but
  `--invert` on the dark CTA band, where the accent falls to 2.97:1.
- **Neutrals:** cool throughout. Rules carry a blue cast (`--blueprint
  #E1E7EF`), never warm. Every palette entry has its measured contrast ratio in
  a comment beside it.

## Motion
- **The one high-impact moment:** the hero backdrop — a raymarched lattice
  drifting behind the headline. Desktop only; it costs battery and frame budget
  on the devices with least of both.
- Scroll reveals on 29 elements, staggered between siblings so a row arrives as
  a row.
- A sticky action bar that appears once the hero's own buttons leave the
  viewport, and retreats when they return.
- Everything honours `prefers-reduced-motion`: the shader never starts, and the
  scroll expansion collapses to a static frame.
- All reveals are scoped to `.js`, so nothing is hidden when scripting is off.

## Sections (home, in order)
1. **Hero** — the promise, two buttons, the proof card. Answers what, why and
   what-next in one screen.
2. **The reality** — "The online side runs whether you are watching or not."
   Names the problem the promise solves.
3. **Tell it once** — the mechanism: how one set of prices feeds everything.
4. **Five cards. One system.** — the product decomposed. The only place the
   offer is enumerated.
5. **The questions you have answered a thousand times** — objection handling,
   including "why not just use ChatGPT?".
6. **You own all of it** — the exit terms, volunteered before anyone asks.
7. **One person builds it** — the differentiator, and the only place a human is
   named.
8. **CTA band** — one action.

## Tech stack
Static HTML, CSS and vanilla JS on Vercel behind Cloudflare. No build step, no
framework, no npm. Pages are generated by `_build_site.py`; `_verify.py` fails
the build on palette, contrast, link, heading and stale-claim violations.

---

## Conflicts — where the site disagrees with this brief

Recorded rather than quietly resolved. Each needs a decision.

1. **Geist is on the forbidden list, and the site uses it for everything.**
   Display, body and mono are all Geist. The brief also asks for two typefaces
   from *different classes*, and Geist plus Geist Mono is one superfamily.
   Changing it is real work: every measured line length and every clamp would
   need rechecking.
2. **Pure `#FFFFFF` is forbidden; the light ground is `#FFFFFF`.** Moving to an
   off-white would invalidate every contrast ratio currently recorded in
   `od.css`, all of which were measured against white.
3. **"No 3-up big-number stat banner."** The hero proof card is exactly that.
   It is also the signature element and the site's only proof.
4. **"No decorative glassmorphism by default."** The header is a glass capsule
   with `backdrop-filter`. Arguably not decorative — it lets the page show
   through a sticky bar — but it is glass.
5. **"No icon-above-heading card layout."** The five deck cards are an icon in
   a container, then a name, then a line.
6. **"No motion for its own sake (scroll-fade everything)."** Twenty-nine
   elements carry `data-reveal`. That is close to everything.
7. **"Every section must argue; if two can swap, neither is working."**
   Sections 3 and 4 could swap without anything reading wrong.

**My read:** 1 and 2 are expensive and probably not worth reopening. 3 is a
rule worth breaking deliberately — it is the strongest thing on the page. 5, 6
and 7 are the ones actually worth fixing.
