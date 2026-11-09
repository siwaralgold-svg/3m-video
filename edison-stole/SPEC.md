# الشعب ضد توماس إديسون — spec

GOAL:    the viewer leaves doubting "Edison invented it" and comments a verdict.
OUTPUT:  HyperFrames, 1080×1920, 30 fps, TikTok.
TIME:    66.1 s on estimated timing. Clock: the Arabic voiceover (Egyptian), not recorded yet.
         Every scene keeps its anchors in one `const T = {…}` line; retime there when the voice arrives.
LOOK:    a courtroom. Wall navy #13294B with panels #172f55; wood #8a5a33 / #6b4226 / #a8703f from y 1150 down.
         Flat 2D busts, outline #0c1a30 at 7–8 px. Text light #F4F6F9, secondary #9fb4d0.
         Gold #CEA532 only on verdict plates and the end card.
         Display: Lalezar (titles 128–160 px, verdicts 150–230 px). Labels: Noto Kufi Arabic 800, 38–52 px.
         Arabic-Indic digits, all copy RTL. Text between y 168 and 1330; y 1180–1320 is kept free for captions.
OBJECTS: Edison (grey swept hair, red bow tie), Swan (white beard, glasses), Dickson (brown hair, moustache),
         Méliès (bald, curled moustache, goatee), Tesla (black centre-parted hair). Light bulb, box camera with crank,
         the moon with a rocket in its eye, film reels, a torn cheque, a dynamo, a gavel.
MOTION:  verdict plates slam in 0.17 s power3.in with a 6-step stage shake. Cards pop on back.out(2).
         Mood changes are takes: 0.1 s squash, new face, overshoot, elastic settle (assets/kit.js `EK.mood`).
         Each count scene enters differently: rise, whip right, film screen, whip left, punch-in.
SHOTS:
| # | Abs time | Picture | Verdict |
|---|---|---|---|
| s1 | 0–8.6 | Edison's portrait, "محتاج يتراجع", plaque, gavel hits, title, "٤ تهم" | |
| s2 | 8.6–20 | Swan lights his lamp, ١٨٧٩, Edison's lights late, the Ediswan sign drops | ما كانش الأول |
| s3 | 20–29.6 | Dickson cranks the camera, the patent: "مسجّلة باسم ؟" → توماس إديسون | خد الفضل |
| s4 | 29.6–40.1 | the film: rocket hits the moon; reel copies fly to Edison; "٠ مليم" | سرقة |
| s5 | 40.1–52.6 | the ٥٠٬٠٠٠ cheque, dynamo runs, cheque torn, "دي نكتة أمريكاني!" | ما اتدفعش (حسب رواية تسلا) |
| s6 | 52.6–63.1 | Edison alone, four verdicts return, "الحكم؟ ليك إنت", comment call | |
| s7 | 63.1–66.1 | T3M logo on navy | |
FACTS:   Swan demonstrated a working lamp in Newcastle in early 1879; Ediswan was incorporated in October 1883.
         Dickson did most of the work on the Kinetograph, 1889–1892; the patents were Edison's.
         Edison's company duplicated "A Trip to the Moon" (1902) and showed it in the US; Méliès earned nothing there.
         The $50,000 promise and the "American humor" reply come from Tesla's own account and are disputed,
         so the plate says "حسب رواية تسلا". "Stolen" is used only for the film.
BANNED:  glow and particles, gold outside verdicts and the end card, the same entrance twice in a row,
         text over a witness's face, anything readable below y 1330.
SOUND:   voice at 1.0 (pending). Gavel = wood impact; each verdict = heavy punch, three takes rotated;
         a switch click on Swan's lamp; a swipe on the two whip cuts. No music source in this session.
