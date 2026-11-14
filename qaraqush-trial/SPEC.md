# محاكمة قراقوش — spec

GOAL:    the viewer leaves asking whether the joke, not the man, deserves the trial, and comments a verdict.
OUTPUT:  HyperFrames, 1080×1920, 30 fps, TikTok.
TIME:    94.4 s. Clock: the voiceover (assets/voiceover.mp3, 90.3 s); word times in assets/transcript.json.
         Every scene keeps its anchors in one `const T = {…}` line, local to the scene.
LOOK:    the Edison cartoon style (../edison-stole/STYLE.md) in a new setting: a hall of three pointed arches,
         navy #13294B with panels #172f55, a stone floor #6b4226 / #7a4c2a / #a8703f from y 1150 down.
         Flat busts in robes and turbans, outline #0c1a30. Gold #CEA532 only on the five plates.
         Display: Lalezar. Labels: Noto Kufi Arabic 800. Arabic-Indic digits, all copy RTL.
         Text between y 168 and 1330; y 1212–1316 is the caption band.
OBJECTS: Qaraqush (white turban, red cap, no beard), Saladin (dark beard, grey turban), Ibn Mammati (dark cap,
         grey pointed beard), Ibn Khallikan (white beard, blue turban), a builder. The citadel, a wall, a map of the
         coast with ships and tents, shackles, a bag of silver, the booklet, a falcon, a city gate, a key.
SHOTS:
| # | Abs time | Picture | Plate |
|---|---|---|---|
| s1 | 0–11.75 | a man with "؟" for a face; "ظالم", "غبي"; the name lands and the joke's cross-eyed face shows, then turns serious | حُكم قراقوش |
| s2 | 11.75–17.75 | Qaraqush behind the table; "محكمة التاريخ"; three files drop | |
| s3 | 17.75–32.55 | ١١٧٦, القاهرة; Saladin; the citadel rises, the wall spreads; "؟" → Qaraqush gets the scroll | واقفة لين اليوم |
| s4 | 32.55–48.95 | map: Acre ringed by ships and tents; Qaraqush on the wall; the wall falls, shackles; Saladin's silver; free | سنتين |
| s5 | 48.95–66.8 | Ibn Mammati writes the booklet; inside it: the falcon flies, the gates slam, it flies over; "هههه" | ٨٠٠ سنة |
| s6 | 66.8–78.85 | "كان شديد" and the tired builder; Ibn Khallikan: "بعيد تصير"; Saladin, the key, the joke crossed out | |
| s7 | 78.85–91.6 | citadel tagged "نكتة"; the writer's name becomes "؟؟؟"; each steps forward in turn | الحكم... لك أنت |
| s8 | 91.6–94.4 | T3M logo on navy | |
FACTS:   to check before publishing: the 1176 start of the citadel and wall under Qaraqush; Acre 1189–1191 and the
         ransom; the falcon story's place in the booklet attributed to Ibn Mammati; Ibn Khallikan's remark (by meaning,
         from Wafayat al-A'yan); forced labour on the works; "800 years" is rounded. Qaraqush's face is imagined:
         no portrait of him exists. The booklet page is labelled "من كتيّب «الفاشوش»" so the joke is not read as fact.
BANNED:  glow and particles, gold outside the plates, the same entrance twice in a row, anything readable below y 1330.
CAPTIONS: compositions/captions.html, 62 groups, script spelling with transcript times. The last line is the plate.
SOUND:   voice normalised to about −18 LUFS, at 1.0. 24 effects from ../sfx-library, each on a visible action:
         plates = heavy punch (three takes rotated), whip cuts = swipes, files = wood, gate = door, booklet = book
         sounds, shackles = latch, ransom = coins. No music: no music source in this session.
