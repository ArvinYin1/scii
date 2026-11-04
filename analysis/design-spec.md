# Shoal — background animation: measured design spec

Source: `3WzIRLEUmwL6GDHl.mp4` — 992x990, 30fps, 452 frames, 15.07s.
Origin: the "shoal" landing page (scrolltide.co showcase). Tagline on page:
"a page where fish made of letters swim around, and tapping the water feeds them."

## Concept
A calm, warm "graph paper" page. Fish silhouettes are composed of a grid of
typographic characters — one glyph per graph-paper cell. Some cells are filled
with a muted colour block, others are bare glyphs, which makes every fish edge
dissolve into loose characters. Fish drift slowly; a soft white glow in the
centre pushes them back so the headline/UI reads clearly. Tapping the water
scatters a ripple and the fish turn toward it and feed.

## Measured numbers (native 992px)
- Background fill: **#FAFAF8** (warm off-white; sampled 250,250,248)
- Graph-paper grid: **19.5px** spacing, both axes. Lines are very low contrast
  (~#E8E6E1 on #FAFAF8, roughly 3-5% darker). Gridlines 1px.
- Glyph cell = **exactly one grid square (19.5px)**. Glyph is centred in the cell.
  Fish therefore align to the paper grid — nothing is off-grid.
- Fish palette (muted, desaturated, "archive print"):
  - brick / terracotta red — family around `#B5523F`, `#A54A38`, `#C0685A`
  - faded salmon / dusty rose — `#D9A79A`, `#C98B7D`
  - olive / ochre — `#B0A060`, `#A89A5E`
  - slate blue-grey — `#8E9AA6`, `#7E8A96`
  - warm grey / taupe — `#9C9187`, `#B5ABA0`
  Each fish is ONE hue family (a school = one colour); colour varies *per cell*
  in lightness so the body has internal texture, not a flat fill.
- Glyph set (observed): `S 8 % X # o t s 0 e a ; : . , ' @ 3` — a mix of
  uppercase, digits, punctuation and lowercase. Punctuation appears mostly on
  the dissolving edges; the dense core uses heavy marks (`# % 8 S X`).
- Glyph colour: near-white on filled cells (the glyph is knocked out), dark
  warm grey (~`#6B5B4E`) on bare cells.
- Headline: "what's surfacing today?" — geometric/neo-grotesque, light weight
  (~300), large (~40px at 992 → ~4.1% of width), normal tracking, dark
  near-black `#1A1A1A`, single line, centred.
- Search field: pill/rounded-rect, ~608px wide, ~100px tall, white ~#FFFFFF at
  ~70% with a soft blurred drop shadow and a 1px light border. Placeholder
  "Ask Shoal anything…" in warm grey. Left: a "+" in a circle. Then a segmented
  control `shallow | deep` (active = white pill on a light grey track). Right: a
  circular submit button with a `↗` arrow (disabled = light grey / enabled = dark).
- Footer line under the field, small monospace, letter-spaced, warm grey:
  `cast ⌾ netline ⌗ tap the water to feed them`
- Corner chrome: top-left wordmark "shoal" with a small 2-square glyph mark;
  top-right `history 03` in monospace + a moon (theme toggle) in a circle.
- Depth of field: a large radial white glow (~#FAFAF8) centred on the headline/
  field. Fish crossing it are faded and blurred; fish at the frame edge are
  crisp and fully saturated. This is what makes the flat page feel like water.

## Layers (back → front)
1. warm off-white page
2. graph paper (19.5px grid, very low contrast)
3. far fish school — small, low opacity, heavy blur (~6-10px), slow
4. mid fish school — medium, slight blur (~2-3px)
5. near fish school — large, crisp (0-1px), fastest, occasional crop at edges
6. centre radial glow (white, big soft falloff) — fakes depth + protects UI
7. UI: headline, search field, footer links, corner chrome
8. interaction layer: tap ripple rings + feed particles
