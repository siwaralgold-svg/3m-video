# The cartoon art style

The look of the Edison video, written so another video can use it with a different story and setting.

## Drawing

- Flat 2D, like a cut-paper cartoon. Every shape is a flat fill with a dark outline: #0c1a30, 8 px on bodies and big shapes, 6–7 px on details and props, round joins.
- No gradients, glow, shadows, particles or textures. Depth comes from overlap only.
- People are busts (head and shoulders), large in frame: a head about 250 px wide at 1080 px.
  - Head: a tall oval, two small ears, eyes as white ovals with round black pupils.
  - Brows: thick 11 px strokes that carry the emotion.
  - Nose: one curved line. Mouth: one stroke, or a filled shape for shock and grins.
  - Hair, beards, moustaches and glasses tell people apart: a few simple filled shapes each, never strands.
- Skin #efc8a6–#f3cdaa. Suits muted: #3d4a63, #4a4038, #55606b, #2f2a3d, #1f2433. Shirt #F4F6F9. One small colour on the tie or bow tie (#8c2f2f).
- Props are the same: flat, outlined, a little chunky and simplified (a bulb, a box camera with a crank, a film reel, a cheque, a moon with a face).

## Colour

- T3M navy #13294B for walls and grounds; panels #172f55, lines #1C385A.
- Warm wood #8a5a33, #6b4226, #a8703f for furniture and floors.
- Text light #F4F6F9; secondary text #9fb4d0.
- Gold #CEA532 is rationed: only the strongest moment of each scene (a verdict, a key word) and the end card.
- Yellow #ffd94a only for light (a lit bulb, sparks).

## Type

- Titles and big words: Lalezar, 128–160 px; punch words up to 230 px.
- Labels and small cards: Noto Kufi Arabic 800, 38–52 px.
- Arabic-Indic digits (١٨٧٩), all copy right to left.

## Cards and plates

- Info card: #F4F6F9 with a 7 px #0c1a30 border, 12 px corners, tilted 3–6°.
- Wood sign: #a8703f with white Lalezar text.
- Punch plate: gold fill, 9 px ink border, a gold outline 9 px outside it, tilted 5–7°.
- Captions: a #0c1a30 box with a 5 px white border, Noto Kufi 800 at 50 px, at y 1212–1316.

## Motion

- Characters act: every change of mood is a take (0.1 s squash, new face, overshoot, elastic settle). They blink, glance at what matters, and breathe while idle.
- Cards pop in on back.out(2) with a small rotation. Punch plates slam in 0.17 s and shake the stage.
- Each scene enters a different way: rise from below, whip from one side, zoom out of an object.
- Titles land and hold still.

## Layout (vertical 1080×1920)

- Text between y 168 and 1330; nothing to read below 1330.
- The main character fills at least 40% of the frame.
