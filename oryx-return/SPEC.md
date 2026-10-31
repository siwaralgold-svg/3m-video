# المها أبو حراب: العودة إلى البرية · spec

- 1080×1920, 30 fps, 40.0 s. Voice 0.1–39.2 s (ElevenLabs "Khalifa", normalised to −17.5 LUFS, peak −1.7 dBFS). Last line holds 0.8 s past the voice; the kit caps the film at 40 s.
- Source: `Oryx_Storyboard_HyperFrames_Kit` (storyboard, shot list, fact sheet, style guide). The kit's art plates were split into a landscape plate plus one transparent PNG per silhouette (`assets/art/*_plate.jpg`, `*_pN.png`) so each animal, person and the hand move on their own.
- Clock: the voice. Anchors from `assets/transcript.json` (whisper) tightened against silence detection.
- Palette: paper #FAF6ED (the plates' own ivory), ink #513D2C, muted ink #8B6F52, sand #C5AC86, sage #A6AD90, amber card #EFE0BF / border #D9B978, old-status card #EADDD3, accent gold #A87A2C (one word per scene at most).
- Type: Noto Kufi Arabic (800 headlines, 600 labels). Latin digits and Latin labels in Inter 900/700 inside LTR spans, as the kit asks (2016, 2023, 600+).
- Text lives inside x 100–980, y 168–1330. Below 1330 only the art.
- Motion: words blur in (8 px → 0, 0.25 s, power2.out) on their spoken word; silhouettes rise 30–40 px or walk in, expo/power3 out; plates drift 4–6 % over a scene (the world moves, landed titles stay still).
- Transitions (one cause each): blur swap on the ivory stage (s1→s2, s6→s7), lift-out (s2→s3), horizontal whip (s3→s4, s4→s5), dip cut (s5→s6), hard cut on «لكن رجع» (s7→s8).
- Banned: bouncy/elastic eases, shakes, floating loops on titles, every element fading up the same way, emoji, neon, claims beyond the fact sheet (600+ is "by 2023", Endangered is not "safe").
- Sound: voice 1.0; ~15 CC0 effects from `sfx-library` at 0.25–0.4, each on a visible action, peak one frame after the picture. No music bed (no music source in this session).

| # | Abs time | Anchor words (abs s) | Picture |
|---|---|---|---|
| s1 | 0–3.1 | هذا الحيوان 0.1 · اختفى 1.6 | Hero oryx on ground, hand points in, two distant oryx fade on «اختفى». |
| s2 | 3.1–5.05 | أبوظبي 3.2 · يرجع 4.5 | Abu Dhabi node, dashed line drawn to Chad node (a relation, not a map). |
| s3 | 5.05–12.45 | المها 5.5 · كان 7.39 · رعاية 8.8 · اختفى 10.5 | Name title, then the care pen rises: herd, grazer, caretaker. |
| s4 | 12.45–18.4 | هيئة 12.69 · قادت 14.24 · بالتعاون 15.79 · تشاد 16.5 · شركاء 17.1 | Three figures and an oryx; arc with three nodes draws as partners are named. |
| s5 | 18.4–21.35 | 2016 18.9 · بدأ 19.96 | Year lands; two oryx walk out of the gate into open land. |
| s6 | 21.35–27.0 | 2023 22.5 · تجاوز 23.67 · ستمية 25.96 | Empty savanna fills with the herd as the counter climbs to 600+. |
| s7 | 27.0–33.25 | منقرض 28.3 · مهدد 30.2 · حماية 31.7 | Status cards: Extinct in the Wild → Endangered (amber); "still needs protection". |
| s8 | 33.25–40.0 | رجع 33.4 · الأمل 36.3 · يحميه 38.9 | Adult and calf at home; titles hand over to the closing line «الأمل ما يختفي… إذا لقى أحد يحميه». |
