# Hero emblem — 3D render brief

The hero currently shows a **CSS-faked** metal emblem. It is good, but it is
flat: a gradient poured through the logo's alpha mask. A real render will beat
it, because CSS has no way to produce the four things that actually make the
Revolut shield read as an object:

| What sells a 3D emblem | CSS can do it? |
|---|---|
| Extruded thickness — you see the side wall of the form | No |
| Rounded bevel on the edge, catching a hard light | No |
| Environment reflection (a room bending across the surface) | No |
| Contact shadow / ambient occlusion where forms meet | Only a flat blur |

What CSS *can* do — a banded gradient that mimics a reflection horizon — is
what is shipping now. If you want the real thing, generate it and drop the
file in. Nothing else has to change.

---

## The prompt

> Attach `ownerdeck-mark-mask.png` as a reference image and say "match this
> shape exactly — it is a logo, the geometry must not be redrawn or
> reinterpreted."

```
A 3D render of the attached logo mark as a solid polished chrome object,
photographed in a studio.

FORM
Extrude the flat shape to roughly 12% of its height in thickness, so the
side wall is visible. Round the front edge with a small, even bevel — about
6% of the thickness — all the way around, including the inner cutouts. The
silhouette must match the attached reference exactly: same proportions, same
curve tangents, same negative space. Do not restyle, simplify, add serifs,
or redraw it.

MATERIAL
Polished chromium. Near-mirror finish, roughness 0.08, no colour tint, no
brushed grain, no scratches, no fingerprints. The surface reflects the
environment, so its brightness varies sharply across the form rather than
shading smoothly.

LIGHT
Studio HDRI: one large soft key from the upper left at about 45 degrees, one
narrow strip light from the lower right for a rim, and a bright horizon line
in the reflected environment so the metal shows a clear break between a light
upper reflection and a darker lower one. Crisp specular hits along the top
bevel. No coloured gels — the reflections stay neutral grey to white.

CAMERA
Straight-on orthographic front view, dead centre, zero perspective
distortion, no tilt, no rotation. The mark reads flat-on, like a badge.

OUTPUT
Transparent background — no ground plane, no baked drop shadow, no glow, no
backdrop, no reflection puddle beneath it. Alpha channel only around the
object. Aspect ratio 506:284, at least 2024 x 1136 px. PNG.
```

### Why "transparent, no baked shadow" is not optional

The site has a light mode and a dark mode. A render with a dark shadow baked
into it shows as a grey smear on white paper; a render with a background baked
in shows as a rectangle. The shadow is applied in CSS, per theme, and already
works. Ask for the object alone.

If the generator refuses transparency, get it on a **pure magenta `#FF00FF`**
background and key it out — never on black or white, both of which sit inside
the chrome's own value range and will eat the edges.

---

## Swapping it in

1. Save as `ownerdeck-emblem.png` in the repo root.
2. In `od.css`, replace the body of `.emblem` (section 15a) with:

```css
.emblem {
  width: min(100%, 24rem);
  aspect-ratio: 506 / 284;
  background: url("/ownerdeck-emblem.png") no-repeat center / contain;
  filter: drop-shadow(0 24px 44px rgb(var(--shadow) / .45));
}
```

   Delete the `-webkit-mask`/`mask` lines, the `linear-gradient`, and the
   `drop-shadow(0 1px 0 var(--metal-1))` lip — a real render has its own
   bevel and does not need the fake one.

3. The `--metal-*` tokens can then go, unless something else has started using
   them. `_verify.py` will not complain either way.
4. Leave the `@supports not (mask:...)` block alone — it now only guards
   `.od-mark`, which still needs it.
5. Rebuild and check:

```bash
python _build_site.py && python _verify.py
```

The `@media (max-width: 62rem)` size override and the dark-mode shadow rule
keep working untouched.
