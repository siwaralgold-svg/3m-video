import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + "/"
SCENES = [("s1", 0, 6), ("s2", 6, 6), ("s3", 12, 7), ("s4", 19, 7), ("s5", 26, 7)]
TOTAL = 33

# (id, file, global time of the picture it belongs to, peak_at, duration, volume, kind)
# kind "peak": start = t - peak + 1/30 ; "end": start = t - duration (risers)
SFX = [
    ("sfx-wind", "risers/air_swell.mp3", 0.0, None, 1.541, 0.30, "at"),
    ("sfx-cut1", "transitions/whoosh_deep_08.mp3", 6.0, 0.457, 1.091, 0.35, "peak"),
    ("sfx-cloth", "foley/rpg_cloth1.mp3", 7.25, 0.113, 0.616, 0.40, "peak"),
    ("sfx-creak", "foley/rpg_creak2.mp3", 8.75, 0.564, 0.763, 0.40, "peak"),
    ("sfx-break1", "impacts/impact_plank_medium_000.mp3", 9.0, 0.009, 0.443, 0.45, "peak"),
    ("sfx-break2", "impacts/impact_wood_heavy_001.mp3", 9.05, 0.004, 0.31, 0.40, "peak"),
    ("sfx-break3", "impacts/impact_wood_light_002.mp3", 9.45, 0.001, 0.263, 0.30, "peak"),
    ("sfx-cut2", "transitions/whoosh_soft_01.mp3", 12.0, 0.372, 0.928, 0.32, "peak"),
    ("sfx-pick1", "impacts/impact_mining_000.mp3", 12.8, 0.013, 0.729, 0.40, "peak"),
    ("sfx-hoe1", "impacts/impact_soft_heavy_000.mp3", 13.4, 0.006, 0.526, 0.40, "peak"),
    ("sfx-pick2", "impacts/impact_mining_001.mp3", 14.0, 0.005, 0.675, 0.40, "peak"),
    ("sfx-hoe2", "impacts/impact_soft_heavy_001.mp3", 14.6, 0.006, 0.569, 0.40, "peak"),
    ("sfx-pick3", "impacts/impact_mining_002.mp3", 15.2, 0.008, 0.678, 0.40, "peak"),
    ("sfx-hoe3", "impacts/impact_soft_heavy_000.mp3", 15.8, 0.006, 0.526, 0.36, "peak"),
    ("sfx-suck", "risers/reverse_swell_01.mp3", 16.4, 0.782, 0.825, 0.35, "peak"),
    ("sfx-pick4", "impacts/impact_mining_001.mp3", 16.4, 0.005, 0.675, 0.45, "peak"),
    ("sfx-gush", "transitions/whoosh_air_03.mp3", 16.9, 0.523, 0.929, 0.40, "peak"),
    ("sfx-cut3", "transitions/whoosh_fast_02.mp3", 19.0, 0.322, 0.82, 0.30, "peak"),
    ("sfx-flow", "transitions/whoosh_air_07.mp3", 19.9, 0.405, 0.656, 0.35, "peak"),
    ("sfx-pop1", "ui-clicks/pop_soft.mp3", 23.6, 0.005, 0.08, 0.35, "peak"),
    ("sfx-pop2", "ui-clicks/interface_pluck_001.mp3", 23.9, 0.002, 0.1, 0.30, "peak"),
    ("sfx-pop3", "ui-clicks/interface_pluck_002.mp3", 24.2, 0.001, 0.146, 0.30, "peak"),
    ("sfx-cut4", "transitions/whoosh_deep_04.mp3", 26.0, 0.248, 0.497, 0.30, "peak"),
    ("sfx-riser", "risers/riser_01.mp3", 29.6, None, 2.2, 0.30, "end"),
    ("sfx-boom", "impacts/boom.mp3", 29.6, 0.047, 1.918, 0.40, "peak"),
]

def audio_tags():
    out = []
    for i, (aid, file, t, peak, dur, vol, kind) in enumerate(SFX):
        if kind == "peak":
            start = t - peak + 1 / 30
        elif kind == "end":
            start = t - dur
        else:
            start = t
        start = max(0, round(start, 3))
        src = "assets/sfx/" + os.path.basename(file)
        out.append(f'      <audio id="{aid}" class="clip" src="{src}" data-start="{start}" data-duration="{dur}" data-track-index="{11 + i % 3}" data-volume="{vol}"></audio>')
    return "\n".join(out)

hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>'
    for sid, st, d in SCENES)

html = f"""<!doctype html>
<html lang="ar" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Amiri"; src: url("assets/fonts/Amiri-Bold.ttf"); font-weight: 700; }}
      @font-face {{ font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #2a1a10; }}
      #ground {{ position: absolute; inset: 0; background: #2a1a10; }}
      #vignette {{
        position: absolute; inset: 0; pointer-events: none; z-index: 90;
        background: radial-gradient(125% 90% at 50% 45%, transparent 58%, rgba(70,35,10,0.42) 100%);
      }}
      @keyframes hf-grain-noise {{
        0%, 100% {{ transform: translate(0, 0); }} 10% {{ transform: translate(-5%, -5%); }}
        20% {{ transform: translate(-10%, 5%); }} 30% {{ transform: translate(5%, -10%); }}
        40% {{ transform: translate(-5%, 15%); }} 50% {{ transform: translate(-10%, 5%); }}
        60% {{ transform: translate(15%, 0); }} 70% {{ transform: translate(0, 10%); }}
        80% {{ transform: translate(-15%, 0); }} 90% {{ transform: translate(10%, 5%); }}
      }}
      #grain-overlay {{ position: absolute; inset: 0; pointer-events: none; z-index: 100; overflow: hidden; }}
      #grain-overlay .grain-texture {{
        position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
        opacity: 0.14; mix-blend-mode: overlay;
        animation: hf-grain-noise 0.5s steps(1) infinite;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="ground" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-layout-ignore style="z-index:1"></div>
{hosts}
      <div id="vignette" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-layout-ignore></div>
      <div id="grain-overlay" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-layout-ignore><div class="grain-texture"></div></div>

      <!-- Voiceover: export from ElevenLabs as assets/voiceover.mp3 and add <audio id="voiceover" class="clip" src="assets/voiceover.mp3" data-start="0" data-track-index="10" data-volume="1"> here. -->
{audio_tags()}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(ROOT + "index.html", "w").write(html)

# copy sfx
import shutil
os.makedirs(ROOT + "assets/sfx", exist_ok=True)
for _, file, *_ in SFX:
    shutil.copy(ROOT + "../sfx-library/" + file, ROOT + "assets/sfx/" + os.path.basename(file))
print("index ok")
