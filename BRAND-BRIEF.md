# Ownerdeck — Brand & Design Brief

Everything an AI image tool (Midjourney / DALL·E / Ideogram / Firefly) or a
human designer needs to produce the full asset set. Copy the prompts verbatim.

---

## 1. The brand in one paragraph

**Ownerdeck** is an AI assistant that answers a small business's **WhatsApp,
Instagram DMs and website chat** — replying in ~2 seconds, in any language,
quoting real availability and prices, and capturing the booking. Customers are
small service businesses in Cyprus: boat tours, car rental, salons, clinics,
restaurants. The feeling should be **capable, modern, calm and trustworthy** —
an intelligent operator quietly handling things in the background. Not a
cartoon robot, not a cutesy chat bubble mascot, not corporate-stiff.

**Tone words:** intelligent · instant · effortless · dependable · modern
**Avoid:** cartoon robots, speech-bubble clichés, generic "AI brain" imagery,
stock gradients-on-white, anything that looks like a WhatsApp clone.

---

## 2. Locked brand values

| Token | Hex | Use |
|---|---|---|
| Indigo (primary) | `#6366F1` | Buttons, logo mark, key accents |
| Violet (secondary) | `#8B5CF6` | Gradient partner to indigo |
| Light indigo | `#A5B4FC` | Small accent text on dark |
| Near-black plum | `#0B0B18` | Primary background |
| Panel | `#14142A` | Cards, raised surfaces |
| Off-white | `#F8FAFC` | Headings on dark |
| Body text | `#A5A5C4` | Paragraphs on dark |

**Signature gradient:** `linear-gradient(135deg, #6366F1 → #8B5CF6)` (135°)
**Typeface:** Plus Jakarta Sans — Bold/ExtraBold for headings, Regular for body.
Monospace accents: JetBrains Mono.
**Shape language:** generous rounded corners (12–24px), pill-shaped buttons
(999px), soft radial glows, no hard drop shadows.

---

## 3. Assets needed

### A. Primary logo — wordmark + mark
```
Minimal modern logo for "Ownerdeck", a multi-channel AI messaging assistant
for small businesses. Abstract geometric mark: a lightning bolt fused with a
rounded message bubble, suggesting instant replies. Mark sits inside a
squircle (superellipse) with 22% corner radius, filled with a 135° gradient
from indigo #6366F1 to violet #8B5CF6, bolt knocked out in pure white.
Wordmark "Ownerdeck" set to the right in a geometric sans-serif, ExtraBold,
tight letter-spacing, pure white #F8FAFC. Flat vector, no bevels, no
gradients on the type, no drop shadow. Transparent background.
Style: Linear, Vercel, Stripe — precise, confident, contemporary.
--no 3d, bevel, gloss, cartoon, mascot, photorealism, clutter
```

### B. Icon / app mark only (square)
```
App icon for "Ownerdeck". Squircle tile with 22% corner radius filled with a
135° gradient from #6366F1 to #8B5CF6. Centred inside: a single bold
lightning bolt in pure white, geometric and slightly italic-leaning, with
clean straight edges. Generous padding — the bolt occupies ~55% of the tile.
Flat vector, crisp edges, no shadow, no texture, no text.
Export square, centred, safe margins for rounding.
--no text, letters, shadow, 3d, gradient mesh, noise
```
**Sizes needed:** 1024×1024 master → 512, 256, 180 (Apple touch), 32, 16 (favicon).

### C. Monochrome / one-colour variants
```
Same Ownerdeck lightning-bolt-in-bubble mark, rendered as a single flat solid
shape with no gradient. Produce three versions: pure white on transparent;
pure black on transparent; and #6366F1 indigo on transparent. Simplified so
it stays legible at 16px. Flat vector, no detail smaller than 1/12 of the mark.
```
*(Needed for: invoices, dark/light backgrounds, stamps, embroidery, favicons.)*

### D. Social profile picture (Instagram / TikTok / WhatsApp Business)
```
Social avatar for "Ownerdeck". Circular crop. Background: 135° gradient from
#6366F1 indigo to #8B5CF6 violet with a subtle darker vignette at the edges.
Centred: bold white lightning bolt mark, occupying ~50% of the circle so it
stays clear at 40px. High contrast, no text, no fine detail.
```

### E. Social share / OG image (1200×630)
```
Wide banner 1200x630 for a modern AI SaaS called Ownerdeck. Background very
dark near-black plum #0B0B18 with two soft radial glows: indigo #6366F1 in
the top right, violet #8B5CF6 in the bottom left, both very diffuse and
subtle. Left-aligned composition with generous negative space. Small squircle
logo mark top-left. Large bold headline text area in off-white. Clean, calm,
premium. Flat vector, no photos, no people, no 3d renders.
--ar 40:21 --no clutter, stock photo, people, robots
```

### F. Website hero visual (optional upgrade)
```
Abstract illustration for a multi-channel AI messaging assistant. Three
stylised message streams — one green-tinted (WhatsApp), one magenta-tinted
(Instagram), one blue-tinted (website chat) — flowing from the left and
converging into a single glowing indigo-violet node on the right, which emits
one clean outgoing reply. Dark near-black plum background #0B0B18, thin
luminous lines, soft glow, generous negative space. Flat vector / subtle
gradient. Elegant and minimal, not busy.
--no robots, faces, text, clutter, photorealism
```

### G. Channel icon set
```
Set of three matching line icons on transparent background: a WhatsApp-style
phone-chat glyph, an Instagram-style rounded-square camera glyph, and a
browser window with a chat bubble. Uniform 1.8px stroke weight, rounded caps
and joins, 24x24 grid, geometric and consistent. Colour #A5B4FC light indigo.
Flat, minimal, no fill, no shadow.
```

### H. Business card
```
Business card design 85x55mm for "Ownerdeck". FRONT: near-black plum #0B0B18
background, centred squircle logo mark with indigo-violet gradient, wordmark
"Ownerdeck" beneath in white ExtraBold geometric sans, and a single line of
light indigo #A5B4FC micro-type reading "Every customer message, answered."
BACK: same dark background, left-aligned contact block in white and light
indigo, with a subtle indigo radial glow in the top-right corner. Minimal,
lots of negative space, premium matte feel.
```

---

## 4. Non-negotiables for whoever builds these

1. **Keep the gradient direction consistent** — always 135°, indigo→violet.
2. **The mark must survive 16px.** If a detail disappears at favicon size,
   remove it from the master.
3. **Always supply SVG** for the logo and icons, plus PNG exports with
   transparency. Never deliver logo-on-a-white-rectangle only.
4. **Never recolour the channel logos.** WhatsApp stays green, Instagram keeps
   its gradient, Telegram stays blue — they must remain instantly
   recognisable, even though the brand is indigo.
5. **Clear space** around the logo = the height of the "O" on all sides.
6. **Wordmark capitalisation is "Ownerdeck"** — capital O, lowercase d. Not
   "OwnerDeck", not "ownerdeck".

---

## 5. Where each asset lands on the site

| Asset | File | Notes |
|---|---|---|
| Nav logo | `Logo.png` | Wordmark + mark, transparent, ~128px tall export |
| Favicon | `favicon.png` | Icon only, 256×256 |
| Social share | `og-image.png` | 1200×630, already auto-generated — replace if you want a designed one |
| Profile pics | — | Upload to Instagram / TikTok / WhatsApp Business |

> **Current gap:** `Logo.png` is still the old teal mark and reads
> "ownerdeck" in lowercase. Replacing it with asset **A** above (indigo/violet,
> capital O) is the last piece of the rebrand.
