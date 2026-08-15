# Logo brief — Ownerdeck

Paste everything below the line into a design tool that can output SVG.
Supersedes `CLAUDE-DESIGN-PROMPT.md`, which describes the retired terracotta
brand.

---

## The brief

Design an identity for **Ownerdeck**.

### What the business is

Ownerdeck builds and runs the online side of small owner-operated businesses —
car and boat rental, villas, clinics, salons, small hotels. One website, one
database, one AI assistant answering WhatsApp and Instagram, bookings, and the
Google listing. The owner tells it the facts once and everything reads from
that.

It is sold as a **deck of cards**. Five cards — Answer, Site, Book, Reach,
Return — and you pick a hand. "Five cards. One system." That metaphor is the
whole identity and the mark has to carry it.

### The one idea the mark must carry

**Cards that overlap.** Separate pieces, offset, clearly a set rather than one
object. Not a fan of five — five reads as noise below about 32px. Two or three
shapes, arranged so the eye completes the rest.

Secondary reading, if it comes for free and never at the cost of the first: the
silhouette suggesting an **O**.

### Hard constraints

- **One colour.** The mark is a single fill, inheriting `currentColor`. No
  gradients, no second colour, no shadow, no outline-plus-fill. It is drawn in
  near-black on white and the identical path in near-white on near-black.
  Overlap must be expressed by geometry — a gap, an offset, a notch — never by
  opacity or tint, because at one colour those disappear.
- **Legible at 16px.** This is the binding constraint. Test it before anything
  else.
- **Geometric and precise.** Straight edges, consistent corner radius, shapes
  on a regular grid. Not hand-drawn, not organic, not textured.
- **No literal playing-card iconography.** No suits, no pips, no face cards,
  no numbers, no poker chips, no dealt-hand illustration, no casino anything.
  The metaphor is a *set of things you choose from*, not gambling.
- No speech bubbles, no chat icons, no robot heads, no circuitry, no neural
  nets, no glowing orbs, no isometric 3D, no swooshes, no gradients meant to
  imply "AI".
- No text inside the mark itself.

### Current placeholder — the thing to beat

```svg
<svg viewBox="0 0 24 24" fill="none">
  <rect x="3"   y="5.5" width="12" height="15" rx="2.2" fill="currentColor" opacity=".22"/>
  <rect x="7.5" y="3.5" width="12" height="15" rx="2.2" fill="currentColor"/>
</svg>
```

Two offset rounded rectangles. It is correct and it is boring, and it breaks
the one-colour rule by leaning on `opacity`. Beat it, or tell me it cannot be
beaten and tighten it instead.

### Palette

The whole brand is one neutral ramp. These are the only values.

| Token | Light | Dark |
|---|---|---|
| Ink (the mark) | `#09090B` | `#FAFAFA` |
| Ground | `#FFFFFF` | `#0A0A0B` |
| Muted | `#71717A` | `#A1A1AA` |
| Rule | `#E4E4E7` | `#26262A` |

There is no accent colour. Do not introduce one.

### Type

**Geist** (SIL OFL), weight 600, letter-spacing `-0.02em`, sentence case:
"Ownerdeck". Never all-caps, never a script or serif face, never letter-spaced
open. Geist Mono weight 500 exists for small uppercase labels but is not part
of the logotype.

### Deliverables

1. **`logo-mark.svg`** — 24×24 viewBox, single path or minimal group,
   `fill="currentColor"`, no `<style>`, no ids, no embedded fonts. Optimised.
2. **`favicon.svg`** — the same mark, redrawn if necessary for 16px. It may be
   simpler than the full mark; it may not be a different idea.
3. **`favicon.png`** — 512×512, and **`apple-touch-icon.png`** at 180×180, ink
   on ground with roughly 12% padding.
4. **`logo-lockup-light.svg`** and **`logo-lockup-dark.svg`** — mark plus
   "Ownerdeck" set in Geist 600. Optical spacing between mark and word, mark
   height matching cap height not the full em box. Text converted to outlines.
5. **`og-image.png`** — 1200×630. Ground colour, lockup optically centred,
   generous margin, and the line "Run the online side of your business." in
   Geist 500 at about 40px in the muted tone. Nothing else. No screenshot, no
   device mockup, no photograph.

### Where it has to work

- 21px tall in a sticky site header, beside the word "Ownerdeck"
- 16px browser tab favicon
- A WhatsApp Business profile picture, cropped to a circle
- Flat black on a white invoice, and flat white on a black slide
- Embroidered or vinyl-cut at ~30mm, so no detail thinner than about 1/12 of
  the mark's height

### Acceptance tests

Run these and report the results. A design that fails any of them is not done.

1. Render at 16×16 and look at it. Are the separate cards still separate?
2. Fill it in one flat colour with no opacity anywhere. Does it still read?
3. Invert it — white on `#0A0A0B`. Does it hold, or does the negative space
   take over?
4. Blur it heavily. Is the silhouette still distinctive, or is it a rounded
   square like a thousand others?
5. Put it beside the Vercel triangle, the Linear mark and the Notion N. Does it
   look like it belongs in that company without looking derivative of any of
   them?

### Deliver

Three distinct directions first, as 24×24 SVG source with a one-line rationale
each — not variations of one idea, three different readings of "overlapping
cards". I will pick one, then you produce the full deliverable list above.
