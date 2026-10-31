import random
from common import *

rnd = random.Random(11)
DUR = 6.0

# ---------- valley details ----------
def house(x, y, w, h, d=None):
    d = d or w * 0.35
    s = f'<g>'
    s += f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y-h} L{x},{y-h}Z" fill="#d6a46a" stroke="#4a2e18" stroke-width="1.6"/>'
    s += f'<path d="M{x+w},{y} L{x+w+d},{y-d*0.4} L{x+w+d},{y-h-d*0.4} L{x+w},{y-h}Z" fill="#9c6a3c" stroke="#4a2e18" stroke-width="1.6"/>'
    s += f'<path d="M{x},{y-h} L{x+w},{y-h} L{x+w+d},{y-h-d*0.4} L{x+d},{y-h-d*0.4}Z" fill="#e8bf86" stroke="#4a2e18" stroke-width="1.4"/>'
    # parapet notches
    for i in range(int(w // 9)):
        px = x + 3 + i * 9
        s += f'<rect x="{px}" y="{y-h-4}" width="5" height="4" fill="#d6a46a" stroke="#4a2e18" stroke-width="0.8"/>'
    s += f'<rect x="{x+w*0.4}" y="{y-h*0.55}" width="{w*0.18:.1f}" height="{h*0.55:.1f}" fill="#4a2e18"/>'
    if w > 30:
        s += f'<rect x="{x+w*0.12}" y="{y-h*0.75}" width="{w*0.12:.1f}" height="{h*0.18:.1f}" fill="#4a2e18"/>'
    return s + '</g>'

def fort(x, y):
    s = '<g>'
    # main wall block
    s += f'<path d="M{x},{y} L{x+190},{y} L{x+190},{y-62} L{x},{y-62}Z" fill="#d9a86d" stroke="#3f2614" stroke-width="2"/>'
    s += f'<path d="M{x+190},{y} L{x+240},{y-18} L{x+240},{y-80} L{x+190},{y-62}Z" fill="#9f6b3b" stroke="#3f2614" stroke-width="2"/>'
    for i in range(19):
        s += f'<path d="M{x+2+i*10},{y-62} l3,-8 l3,8Z" fill="#d9a86d" stroke="#3f2614" stroke-width="1"/>'
    # gate
    s += f'<path d="M{x+80},{y} L{x+80},{y-30} Q{x+95},{y-44} {x+110},{y-30} L{x+110},{y}Z" fill="#5a3418" stroke="#3f2614" stroke-width="1.5"/>'
    # round tower (Muwaiji)
    tx = x - 18
    s += f'<path d="M{tx},{y+2} L{tx},{y-118} Q{tx+32},{y-128} {tx+64},{y-118} L{tx+64},{y+2} Q{tx+32},{y+10} {tx},{y+2}Z" fill="url(#s1-tower)" stroke="#3f2614" stroke-width="2"/>'
    for i in range(7):
        s += f'<rect x="{tx+1+i*9}" y="{y-130}" width="6" height="11" fill="#e2b47a" stroke="#3f2614" stroke-width="1"/>'
    s += f'<path d="M{tx},{y-90} Q{tx+32},{y-98} {tx+64},{y-90}" stroke="#3f2614" stroke-width="1.5" fill="none"/>'
    s += f'<rect x="{tx+27}" y="{y-75}" width="7" height="16" fill="#3f2614"/>'
    # square tower right
    s += f'<path d="M{x+160},{y-60} L{x+160},{y-120} L{x+200},{y-120} L{x+200},{y-60}Z" fill="#dcae74" stroke="#3f2614" stroke-width="2"/>'
    s += f'<path d="M{x+200},{y-60} L{x+222},{y-70} L{x+222},{y-130} L{x+200},{y-120}Z" fill="#9f6b3b" stroke="#3f2614" stroke-width="2"/>'
    for i in range(4):
        s += f'<path d="M{x+162+i*10},{y-120} l3,-8 l3,8Z" fill="#dcae74" stroke="#3f2614" stroke-width="1"/>'
    s += f'<rect x="{x+176}" y="{y-104}" width="6" height="14" fill="#3f2614"/>'
    return s + '</g>'

valley = ""
# falaj (narrow, nearly dry)
falaj = "M690,935 C 650,980 760,1010 720,1060 C 680,1110 560,1130 600,1200 C 640,1270 820,1290 860,1360 C 890,1420 870,1470 900,1520"
valley += f'<path d="{falaj}" fill="none" stroke="#7d5432" stroke-width="16" stroke-linecap="round"/>'
valley += f'<path d="{falaj}" fill="none" stroke="#5e3c22" stroke-width="7" stroke-linecap="round"/>'
valley += f'<path id="s1-glint" d="{falaj}" fill="none" stroke="#6fb7cf" stroke-width="2.4" stroke-dasharray="10 60" stroke-linecap="round" opacity="0.7"/>'

palms_back, palms_front = [], []
for i in range(46):
    y = rnd.uniform(930, 1330)
    x = rnd.uniform(-20, 1100)
    h = 18 + (y - 920) * 0.13 + rnd.uniform(-4, 4)
    item = (y, f'<g transform="translate({f(x)},{f(y)})">{palm(h, rnd.uniform(-0.12, 0.12), dry=True, seed=i, sw=1.0)}</g>')
    palms_back.append(item)
houses = [(470, 1040, 34, 22), (520, 1052, 46, 26), (585, 1046, 30, 20), (930, 1058, 40, 24), (985, 1070, 52, 28),
          (420, 1090, 50, 30), (360, 1072, 32, 22), (880, 1120, 58, 34), (960, 1150, 44, 28), (300, 1130, 54, 32)]
items = palms_back + [(y, house(x, y, w, h)) for x, y, w, h in houses] + [(1018, fort(640, 1018))]
items.sort(key=lambda a: a[0])
valley += "".join(s for _, s in items)

# ---------- the man (back view), feet at origin ----------
MAN = """
<g id="s1-man" transform="translate(330 1792)">
  <path d="M-30,6 C -200,40 -420,80 -600,110 C -620,122 -560,132 -520,128 C -330,105 -120,62 70,14Z" fill="#5b3418" opacity="0.38"/>
  <!-- kandura hem -->
  <path d="M-118,-130 L-132,-14 Q0,4 132,-14 L118,-130Z" fill="url(#s1-kandura)" stroke="#2f1d10" stroke-width="3"/>
  <path d="M-40,-120 Q-46,-60 -52,-14 M38,-118 Q46,-60 50,-14" stroke="#b8a58a" stroke-width="4" fill="none"/>
  <!-- sandals -->
  <path d="M-78,-16 Q-50,-30 -22,-16 L-20,0 Q-50,8 -80,0Z" fill="#4a2c18" stroke="#24150b" stroke-width="2"/>
  <path d="M24,-16 Q52,-30 80,-16 L82,0 Q52,8 22,0Z" fill="#4a2c18" stroke="#24150b" stroke-width="2"/>
  <path d="M-70,-18 Q-50,-24 -30,-18 M32,-18 Q52,-24 72,-18" stroke="#9a6b44" stroke-width="5" fill="none"/>
  <!-- bisht flap (flutters) -->
  <path id="s1-flap" d="M-200,-480 C-260,-400 -300,-250 -330,-150 Q-290,-128 -240,-112 C-225,-250 -215,-380 -200,-480Z" fill="url(#s1-bisht2)" stroke="#2a170b" stroke-width="3"/>
  <!-- bisht body -->
  <path d="M-150,-690 C-190,-600 -215,-400 -240,-110 Q-120,-84 0,-96 Q120,-84 235,-116 C215,-400 200,-590 160,-690 Q0,-736 -150,-690Z" fill="url(#s1-bisht)" stroke="#2a170b" stroke-width="3.5"/>
  <path d="M-60,-650 C-70,-450 -82,-260 -92,-104 M18,-664 C14,-450 12,-260 8,-98 M92,-652 C100,-450 112,-260 122,-104 M-120,-560 C-140,-400 -160,-260 -180,-112" stroke="#3a2010" stroke-width="5" fill="none" opacity="0.55"/>
  <path d="M-30,-640 C-36,-450 -44,-260 -50,-100 M140,-560 C150,-400 165,-260 178,-112" stroke="#c48a55" stroke-width="3" fill="none" opacity="0.45"/>
  <!-- gold zari edge -->
  <path d="M-240,-110 Q-120,-84 0,-96 Q120,-84 235,-116" stroke="#d9a441" stroke-width="5" fill="none"/>
  <path d="M-240,-110 C-232,-200 -226,-260 -220,-330" stroke="#e8b84f" stroke-width="5" fill="none"/>
  <path d="M-330,-150 Q-290,-128 -240,-112" stroke="#e8b84f" stroke-width="4" fill="none"/>
  <!-- rim light (sun ahead, right) -->
  <path d="M160,-690 C200,-590 215,-400 235,-116" stroke="#f6c46a" stroke-width="5" fill="none" opacity="0.9"/>
  <!-- right arm: sleeve drape, cuff, hand pointing -->
  <path id="s1-sleeve" d="M140,-705 C230,-745 320,-768 392,-782 L400,-740 C340,-700 290,-620 255,-515 C225,-540 195,-580 165,-600Z" fill="url(#s1-bisht)" stroke="#2a170b" stroke-width="3"/>
  <path d="M150,-712 C235,-752 320,-772 392,-784" stroke="#f6c46a" stroke-width="4" fill="none"/>
  <path d="M392,-782 L414,-787 L420,-746 L400,-740Z" fill="#f2ebdf" stroke="#2a170b" stroke-width="2.5"/>
  <path d="M414,-784 C430,-791 446,-791 454,-787 L484,-791 Q492,-786 484,-781 L454,-777 C455,-766 447,-752 433,-748 C423,-746 417,-748 417,-748Z" fill="#b07a50" stroke="#3a2010" stroke-width="2.4"/>
  <path d="M440,-776 Q446,-770 444,-760" stroke="#7a4a2a" stroke-width="2" fill="none"/>
  <!-- ghutra tail (flutters) -->
  <path id="s1-tail" d="M-150,-692 C-192,-672 -232,-622 -262,-560 C-238,-568 -204,-602 -158,-642Z" fill="url(#s1-ghutra)" stroke="#2f2418" stroke-width="2.5"/>
  <!-- ghutra from behind -->
  <path d="M-62,-830 C-62,-912 62,-912 62,-830 C75,-780 120,-730 165,-700 C120,-660 60,-604 0,-560 C-60,-604 -120,-660 -160,-695 C-115,-730 -75,-780 -62,-830Z" fill="url(#s1-ghutra)" stroke="#2f2418" stroke-width="3"/>
  <path d="M-30,-800 C-40,-720 -30,-640 -10,-580 M28,-806 C40,-730 60,-670 90,-640 M-50,-790 C-80,-740 -110,-710 -140,-694" stroke="#bfb3a0" stroke-width="3" fill="none"/>
  <path d="M62,-830 C75,-780 120,-730 165,-700" stroke="#f8d48a" stroke-width="4" fill="none"/>
  <!-- agal (double cord) seen from behind -->
  <path d="M-64,-852 Q0,-828 64,-852" stroke="#141010" stroke-width="12" fill="none" stroke-linecap="round"/>
  <path d="M-65,-834 Q0,-810 65,-834" stroke="#141010" stroke-width="11" fill="none" stroke-linecap="round"/>
  <path d="M-50,-848 Q0,-830 50,-848" stroke="#4a4040" stroke-width="2.5" fill="none"/>
</g>
"""

defs = """
<linearGradient id="s1-sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#27406e"/><stop offset="0.28" stop-color="#58709b"/><stop offset="0.52" stop-color="#c98a72"/>
  <stop offset="0.74" stop-color="#eda55c"/><stop offset="1" stop-color="#f7cf86"/>
</linearGradient>
<radialGradient id="s1-sunglow"><stop offset="0" stop-color="#fff2c4" stop-opacity="1"/><stop offset="0.18" stop-color="#ffd27a" stop-opacity="0.85"/><stop offset="0.5" stop-color="#E6A145" stop-opacity="0.35"/><stop offset="1" stop-color="#E6A145" stop-opacity="0"/></radialGradient>
<radialGradient id="s1-sun"><stop offset="0" stop-color="#fffaf0"/><stop offset="0.7" stop-color="#ffe7a8"/><stop offset="1" stop-color="#ffc764"/></radialGradient>
<linearGradient id="s1-mtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7083"/><stop offset="1" stop-color="#c4927a"/></linearGradient>
<linearGradient id="s1-far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6b07a"/><stop offset="1" stop-color="#c88c55"/></linearGradient>
<linearGradient id="s1-valley" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4a06a"/><stop offset="1" stop-color="#b47a46"/></linearGradient>
<linearGradient id="s1-dune1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0c27e"/><stop offset="0.5" stop-color="#D9B382"/><stop offset="1" stop-color="#a8713f"/></linearGradient>
<linearGradient id="s1-dune2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6c985"/><stop offset="0.45" stop-color="#dba264"/><stop offset="1" stop-color="#8C5A3C"/></linearGradient>
<linearGradient id="s1-bisht" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3e2312"/><stop offset="0.6" stop-color="#5e3820"/><stop offset="1" stop-color="#8C5A3C"/></linearGradient>
<linearGradient id="s1-bisht2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2e190c"/><stop offset="1" stop-color="#4a2a16"/></linearGradient>
<linearGradient id="s1-ghutra" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#bdb1a0"/><stop offset="0.55" stop-color="#e9e1d3"/><stop offset="1" stop-color="#fff6e4"/></linearGradient>
<linearGradient id="s1-kandura" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9ac97"/><stop offset="1" stop-color="#f1e8d8"/></linearGradient>
<linearGradient id="s1-tower" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a97440"/><stop offset="0.5" stop-color="#d9a86d"/><stop offset="1" stop-color="#f0c88e"/></linearGradient>
<linearGradient id="s1-cloud" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d98f86" stop-opacity="0"/><stop offset="0.3" stop-color="#f2a98a"/><stop offset="1" stop-color="#ffd59a"/></linearGradient>
"""

clouds = ""
for (y, x1, x2, th, op) in [(330, -40, 620, 26, 0.75), (372, 140, 900, 18, 0.6), (520, 420, 1120, 30, 0.8), (566, -60, 520, 16, 0.55), (640, 560, 1120, 14, 0.7), (700, 100, 640, 12, 0.5)]:
    clouds += f'<path d="M{x1},{y} C{x1+120},{y-th} {x2-200},{y-th*1.2} {x2},{y-4} C{x2-180},{y+th*0.5} {x1+160},{y+th*0.6} {x1},{y}Z" fill="url(#s1-cloud)" opacity="{op}"/>'

svg = f"""
<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0">
  <defs>{defs}</defs>
  <rect width="1080" height="1920" fill="url(#s1-sky)"/>
  <g id="s1-clouds">{clouds}</g>
  <circle id="s1-glow" cx="850" cy="872" r="520" fill="url(#s1-sunglow)"/>
  <circle id="s1-sun" cx="850" cy="872" r="64" fill="url(#s1-sun)"/>
  <!-- Jebel Hafeet on the horizon -->
  <path d="M-40,912 L-40,868 C40,850 120,810 200,790 C260,776 300,800 360,820 C430,842 520,850 600,872 L640,912Z" fill="url(#s1-mtn)" stroke="#7d5a62" stroke-width="1.5" opacity="0.92"/>
  <path d="M200,790 C230,812 250,840 290,880 M360,820 C380,850 400,870 430,900" stroke="#b88a86" stroke-width="2" fill="none" opacity="0.6"/>
  <path d="M-40,930 C120,890 300,925 480,900 C640,880 820,915 1120,890 L1120,960 L-40,960Z" fill="url(#s1-far)"/>
  <path d="M-40,940 C200,925 500,950 760,930 C900,920 1000,935 1120,925 L1120,1600 L-40,1600Z" fill="url(#s1-valley)"/>
  <g id="s1-valley">{valley}</g>
  <!-- warm haze over the valley -->
  <rect x="0" y="900" width="1080" height="200" fill="#f3b46a" opacity="0.18"/>
  <!-- mid dune right -->
  <path d="M380,1620 C560,1520 760,1420 1120,1380 L1120,1920 L380,1920Z" fill="url(#s1-dune2)" stroke="#7a4a26" stroke-width="2"/>
  <path d="M600,1560 C760,1480 900,1440 1120,1420" stroke="#ffe0a8" stroke-width="4" fill="none" opacity="0.7"/>
  <!-- foreground dune with the man -->
  <path d="M-60,1620 C120,1640 250,1740 360,1792 C520,1862 760,1890 1140,1900 L1140,1940 L-60,1940Z" fill="url(#s1-dune1)" stroke="#7a4a26" stroke-width="2.5"/>
  <path d="M-60,1620 C120,1640 250,1740 360,1792" stroke="#ffe6b0" stroke-width="5" fill="none" opacity="0.75"/>
  <path d="M40,1700 C160,1720 230,1780 300,1830 M120,1800 C240,1820 380,1860 520,1880 M600,1880 C760,1892 900,1900 1080,1905" stroke="#b98048" stroke-width="2.5" fill="none" opacity="0.6"/>
  {MAN}
</svg>
"""

body = f"""
    <div id="s1-wrap" class="clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow style="position:absolute;inset:0;overflow:hidden">
      <div id="s1-cam" style="position:absolute;inset:0">
        {svg}
        <canvas id="s1-sand" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>
      </div>
      <div id="s1-place" class="lb" style="top:236px;left:0;right:0;font-size:54px;color:#ffe9c4;text-shadow:0 3px 14px rgba(40,20,10,.55)">واحة العين</div>
      <div id="s1-year" class="hd" style="top:300px;font-size:200px;color:#fff3da;text-shadow:0 6px 24px rgba(50,25,10,.55)">١٩٤٦</div>
    </div>
"""

script = RNG_JS + f"""
    const tl = gsap.timeline({{ paused: true }});
    const D = {DUR};
    // camera: slow push, then zoom through into the valley
    tl.fromTo("#s1-cam", {{ scale: 1, transformOrigin: "600px 1000px", filter: "blur(0px)" }}, {{ scale: 1.09, duration: 5.4, ease: "power1.inOut" }}, 0);
    tl.to("#s1-cam", {{ scale: 1.7, filter: "blur(10px)", duration: 0.6, ease: "power3.in" }}, 5.4);
    // wind in the bisht and ghutra
    tl.fromTo("#s1-flap", {{ attr: {{ d: "M-200,-480 C-260,-400 -300,-250 -330,-150 Q-290,-128 -240,-112 C-225,-250 -215,-380 -200,-480Z" }} }},
      {{ attr: {{ d: "M-200,-480 C-275,-392 -330,-262 -372,-176 Q-305,-140 -240,-112 C-228,-250 -216,-380 -200,-480Z" }}, duration: 0.55, ease: "sine.inOut", yoyo: true, repeat: 10 }}, 0);
    tl.fromTo("#s1-tail", {{ attr: {{ d: "M-150,-692 C-192,-672 -232,-622 -262,-560 C-238,-568 -204,-602 -158,-642Z" }} }},
      {{ attr: {{ d: "M-150,-692 C-204,-684 -252,-642 -294,-592 C-262,-590 -214,-614 -158,-642Z" }}, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 12 }}, 0.1);
    tl.fromTo("#s1-sleeve", {{ attr: {{ d: "M140,-705 C230,-745 320,-768 392,-782 L400,-740 C340,-700 290,-620 255,-515 C225,-540 195,-580 165,-600Z" }} }},
      {{ attr: {{ d: "M140,-705 C230,-745 320,-768 392,-782 L400,-740 C336,-694 278,-622 232,-528 C210,-552 188,-584 165,-600Z" }}, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 9 }}, 0.2);
    // sun swells, clouds drift, falaj glints
    tl.fromTo("#s1-glow", {{ scale: 0.9, opacity: 0.75, transformOrigin: "850px 872px" }}, {{ scale: 1.15, opacity: 1, duration: D, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s1-sun", {{ scale: 1, transformOrigin: "850px 872px" }}, {{ scale: 1.08, duration: D, ease: "sine.inOut" }}, 0);
    tl.fromTo("#s1-clouds", {{ x: 0 }}, {{ x: -50, duration: D, ease: "none" }}, 0);
    tl.fromTo("#s1-glint", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": -140 }}, duration: D, ease: "none" }}, 0);
    // titles
    tl.fromTo("#s1-year", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.9, ease: "expo.out" }}, 0);
    tl.to(["#s1-place", "#s1-year"], {{ opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, 5.15);

    // blowing sand off the dune crest (deterministic)
    const cv = document.getElementById("s1-sand");
    const ctx = cv.getContext("2d");
    const R = rng(7);
    const P = [];
    for (let i = 0; i < 260; i++) {{
      const x0 = R() * 760;
      const crest = 1620 + (x0 / 360) * 172 * (x0 < 360 ? 1 : 0) + (x0 >= 360 ? 172 + (x0 - 360) * 0.25 : 0);
      P.push({{ t0: R() * D - 1.2, x0, y0: crest - 4, vx: -(140 + R() * 220), vy: -(20 + R() * 50), life: 1.0 + R() * 1.4, r: 0.8 + R() * 2.2, a: 0.35 + R() * 0.5 }});
    }}
    function draw(t) {{
      ctx.clearRect(0, 0, 1080, 1920);
      for (const p of P) {{
        const u = t - p.t0;
        if (u < 0 || u > p.life) continue;
        const k = u / p.life;
        const x = p.x0 + p.vx * u, y = p.y0 + p.vy * u + 30 * u * u;
        ctx.globalAlpha = p.a * Math.sin(Math.PI * k);
        ctx.fillStyle = k < 0.5 ? "#ffe2a8" : "#e8b673";
        ctx.beginPath(); ctx.ellipse(x, y, p.r * 2.2, p.r, -0.15, 0, 6.283); ctx.fill();
      }}
      ctx.globalAlpha = 1;
    }}
    const clock = {{ t: 0 }};
    tl.fromTo(clock, {{ t: 0 }}, {{ t: D, duration: D, ease: "none", onUpdate: () => draw(clock.t) }}, 0);
    draw(0);
"""

open(OUT + "s1.html", "w").write(scene("s1", DUR, defs, body, script))
print("s1 ok", len(open(OUT + "s1.html").read()))
