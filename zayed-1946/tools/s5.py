import random, math
from common import *

rnd = random.Random(55)
DUR = 7.0
PH = 3200        # panorama height
TILT = PH - 1920 # camera travel

def tier(cx, y, r, h, gid):
    e = r * 0.22
    s = f'<path d="M{f(cx-r)},{f(y)} L{f(cx-r)},{f(y-h)} A{f(r)},{f(e)} 0 0 0 {f(cx+r)},{f(y-h)} L{f(cx+r)},{f(y)} A{f(r)},{f(e)} 0 0 1 {f(cx-r)},{f(y)}Z" fill="url(#{gid})" stroke="#4a2c14" stroke-width="3"/>'
    # crenellations along the front of the top rim
    n = int(r / 9)
    for i in range(n + 1):
        a = math.pi * i / n
        x = cx - r * math.cos(a)
        yy = y - h + e * math.sin(a)
        s += f'<path d="M{f(x-6)},{f(yy)} L{f(x-6)},{f(yy-10)} L{f(x-2)},{f(yy-10)} L{f(x-2)},{f(yy-17)} L{f(x+2)},{f(yy-17)} L{f(x+2)},{f(yy-10)} L{f(x+6)},{f(yy-10)} L{f(x+6)},{f(yy)}Z" fill="#d9a46a" stroke="#4a2c14" stroke-width="1.5"/>'
    s += f'<path d="M{f(cx-r)},{f(y-h+18)} A{f(r)},{f(e)} 0 0 0 {f(cx+r)},{f(y-h+18)}" stroke="#a06a38" stroke-width="3" fill="none"/>'
    return s

def fort(x, y):
    s = ""
    # wall
    s += f'<path d="M{x+60},{y} L{x+470},{y} L{x+470},{y-130} L{x+60},{y-130}Z" fill="#cf9b62" stroke="#4a2c14" stroke-width="3"/>'
    s += f'<path d="M{x+60},{y-110} L{x+470},{y-110}" stroke="#a06a38" stroke-width="3"/>'
    for i in range(28):
        xx = x + 64 + i * 14.5
        s += f'<path d="M{f(xx)},{y-130} l0,-10 l4,0 l0,-7 l4,0 l0,7 l4,0 l0,10Z" fill="#d9a46a" stroke="#4a2c14" stroke-width="1.4"/>'
    s += f'<path d="M{x+230},{y} L{x+230},{y-70} Q{x+265},{y-108} {x+300},{y-70} L{x+300},{y}Z" fill="#6e4224" stroke="#4a2c14" stroke-width="3"/>'
    s += f'<path d="M{x+265},{y-90} L{x+265},{y} M{x+240},{y-40} L{x+290},{y-40}" stroke="#4a2c14" stroke-width="2.5"/>'
    for i in range(3):
        s += f'<rect x="{x+120+i*190 if i < 2 else x+400}" y="{y-90}" width="12" height="26" fill="#4a2c14"/>'
    # square corner tower
    s += f'<path d="M{x+430},{y} L{x+430},{y-210} L{x+520},{y-210} L{x+520},{y}Z" fill="#d6a46a" stroke="#4a2c14" stroke-width="3"/>'
    s += f'<path d="M{x+520},{y} L{x+556},{y-16} L{x+556},{y-226} L{x+520},{y-210}Z" fill="#9c6a3c" stroke="#4a2c14" stroke-width="3"/>'
    for i in range(6):
        s += f'<path d="M{x+433+i*15},{y-210} l0,-10 l4,0 l0,-7 l4,0 l0,7 l4,0 l0,10Z" fill="#d9a46a" stroke="#4a2c14" stroke-width="1.4"/>'
    s += f'<rect x="{x+468}" y="{y-170}" width="12" height="30" fill="#4a2c14"/>'
    # Al Jahili style round tower in tiers
    cx = x + 70
    s += tier(cx, y + 6, 105, 190, "s5-tw")
    s += tier(cx, y - 184, 84, 80, "s5-tw")
    s += tier(cx, y - 264, 64, 60, "s5-tw")
    for yy in (y - 120, y - 230):
        s += f'<rect x="{cx-6}" y="{yy}" width="12" height="28" fill="#4a2c14"/>'
    return s

# ---------- skyline ----------
sky_b = 1068
city = ""
rb = random.Random(5)
x = -40
while x < 1120:
    w = rb.uniform(34, 70)
    h = rb.uniform(90, 260)
    if 380 < x < 700: h *= 1.15
    kind = rb.random()
    col = rb.choice(["#7b7fb3", "#8a86b8", "#6f76a8", "#9690bf"])
    if kind < 0.2:  # curved-top tower
        city += f'<path d="M{f(x)},{sky_b} L{f(x)},{f(sky_b-h)} Q{f(x+w/2)},{f(sky_b-h-w*0.9)} {f(x+w)},{f(sky_b-h)} L{f(x+w)},{sky_b}Z" fill="{col}" stroke="#5b5d8a" stroke-width="1.5"/>'
    elif kind < 0.3:  # spire
        city += f'<path d="M{f(x)},{sky_b} L{f(x+w*0.25)},{f(sky_b-h)} L{f(x+w*0.5)},{f(sky_b-h-120)} L{f(x+w*0.75)},{f(sky_b-h)} L{f(x+w)},{sky_b}Z" fill="{col}" stroke="#5b5d8a" stroke-width="1.5"/>'
    else:
        city += f'<path d="M{f(x)},{sky_b} L{f(x)},{f(sky_b-h)} L{f(x+w*0.8)},{f(sky_b-h)} L{f(x+w)},{f(sky_b-h+18)} L{f(x+w)},{sky_b}Z" fill="{col}" stroke="#5b5d8a" stroke-width="1.5"/>'
    for yy in range(int(sky_b - h + 16), sky_b - 6, 16):
        city += f'<path d="M{f(x+6)},{yy} L{f(x+w-6)},{yy}" stroke="#b9b6d8" stroke-width="1.5" opacity="0.6"/>'
    x += w + rb.uniform(-6, 10)
# landmark: Aldar-like disc and a tall needle
city += f'<rect x="760" y="{sky_b-60}" width="60" height="60" fill="#7178ab"/><circle cx="790" cy="{sky_b-140}" r="88" fill="#8c8cc0" stroke="#5b5d8a" stroke-width="2"/>'
for k in range(-4, 5):
    city += f'<path d="M{790-math.sqrt(max(0,88**2-(k*18)**2)):.1f},{sky_b-140+k*18} L{790+math.sqrt(max(0,88**2-(k*18)**2)):.1f},{sky_b-140+k*18}" stroke="#c4c2e2" stroke-width="1.5" opacity="0.6"/>'
city += f'<path d="M930,{sky_b} L940,{sky_b-330} L950,{sky_b-440} L960,{sky_b-330} L970,{sky_b}Z" fill="#8a86b8" stroke="#5b5d8a" stroke-width="1.5"/>'
city += f'<rect x="-100" y="{sky_b-90}" width="1300" height="90" fill="url(#s5-haze)"/>'

# ---------- oasis palms ----------
oasis = []
for i in range(40):
    yy = rnd.uniform(1420, 2480)
    xx = rnd.uniform(-60, 1140)
    if -40 < xx < 700 and 1380 < yy < 2050: continue  # keep the fort clear
    h = 90 + (yy - 1400) * 0.32
    oasis.append((yy, f'<g transform="translate({f(xx)},{f(yy)})">{palm(h, rnd.uniform(-0.1, 0.1), seed=600+i, dates=h > 260, sw=1.6)}</g>'))
oasis.append((1800, f'<g>{fort(70, 1800)}</g>'))
oasis.sort(key=lambda a: a[0])
oasis_svg = "".join(s for _, s in oasis)

# fields between palms
fields = ""
for i in range(14):
    yy = 1420 + i * 75
    fields += f'<path d="M-50,{yy} C300,{yy-10} 700,{yy+12} 1130,{yy-4} L1130,{yy+40} C700,{yy+52} 300,{yy+30} -50,{yy+40}Z" fill="{rnd.choice(["#3B7A57","#4b8a4a","#5e9a3a","#74A12E"])}" opacity="0.9"/>'

# ---------- foreground falaj ----------
F = "M-60,2620 C200,2600 360,2700 520,2760 C700,2830 860,2860 1140,2840"
fal = f'<path d="M-60,2560 C200,2540 360,2640 520,2700 C700,2770 860,2800 1140,2780 L1140,3220 L-60,3220Z" fill="url(#s5-grass)"/>'
fal += f'<path d="{F}" stroke="#8a6a4a" stroke-width="170" fill="none"/>'
# stone lining
stones_ = ""
rs = random.Random(9)
for t in [i / 40 for i in range(41)]:
    p = cub(((-60, 2620), (200, 2600), (360, 2700), (520, 2760)), t * 2) if t < 0.5 else cub(((520, 2760), (700, 2830), (860, 2860), (1140, 2840)), (t - 0.5) * 2)
    for side in (-1, 1):
        stones_ += stone(p[0] + rs.uniform(-10, 10), p[1] + side * 74 + rs.uniform(-6, 6), rs.uniform(14, 22), rs, grad_id="s5-stone", shadow=False)
fal += f'<path d="{F}" stroke="#2B8CBE" stroke-width="128" fill="none"/>'
fal += f'<path d="{F}" stroke="#48a8d4" stroke-width="80" fill="none"/>'
fal += f'<path id="s5-shine" d="{F}" stroke="#d9fbff" stroke-width="3" fill="none" opacity="0.65" stroke-dasharray="140 60 30 180 60 90" stroke-linecap="round"/>'
fal += f'<path id="s5-shine2" d="{F}" stroke="#a6ecfa" stroke-width="2.5" fill="none" opacity="0.6" stroke-dasharray="90 150 40 110" stroke-linecap="round" transform="translate(0,-30)"/>'
fal += f'<path id="s5-shine3" d="{F}" stroke="#a6ecfa" stroke-width="2.5" fill="none" opacity="0.6" stroke-dasharray="120 90 50 160" stroke-linecap="round" transform="translate(0,34)"/>'
fal += stones_
fg_palms = ""
for xx, yy, h, sd in [(40, 3200, 620, 1), (1060, 3200, 560, 2), (260, 2560, 380, 3), (880, 2620, 400, 4)]:
    fg_palms += f'<g transform="translate({xx},{yy})">{palm(h, -0.06 if xx > 540 else 0.06, seed=700+sd, dates=True, sw=2.2)}</g>'

# walkers toward the city
walkers = ""
for i in range(4):
    walkers += f'<g id="s5-wk{i}" transform="translate({430 + i*34},{1330 + (i%2)*14})"><g>{person_back(s=0.07, variant=i%2, kandura="#f6efe2", ghutra="#fbf6ec", outline="#5a4a3a")}</g></g>'

defs = """
<linearGradient id="s5-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f7fb8"/><stop offset="0.45" stop-color="#9fbcdc"/><stop offset="0.82" stop-color="#f3c9ae"/><stop offset="1" stop-color="#fde2b0"/></linearGradient>
<radialGradient id="s5-sun"><stop offset="0" stop-color="#fff8e0"/><stop offset="0.25" stop-color="#ffe4a0" stop-opacity="0.8"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></radialGradient>
<linearGradient id="s5-haze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7d2b6" stop-opacity="0"/><stop offset="1" stop-color="#f7d2b6" stop-opacity="0.85"/></linearGradient>
<linearGradient id="s5-dune" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3c88c"/><stop offset="1" stop-color="#d49c62"/></linearGradient>
<linearGradient id="s5-dune2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eab878"/><stop offset="1" stop-color="#c88850"/></linearGradient>
<linearGradient id="s5-tw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a06a38"/><stop offset="0.45" stop-color="#d9a46a"/><stop offset="1" stop-color="#f0c890"/></linearGradient>
<linearGradient id="s5-grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e9a3a"/><stop offset="1" stop-color="#2f6a40"/></linearGradient>
<radialGradient id="s5-stone" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#e2c8a0"/><stop offset="0.6" stop-color="#a88a66"/><stop offset="1" stop-color="#6e5640"/></radialGradient>
"""

clouds = ""
for (y, x1, x2, th, op) in [(180, -60, 560, 34, 0.7), (260, 380, 1140, 26, 0.6), (430, -40, 700, 22, 0.5), (560, 500, 1140, 18, 0.55)]:
    clouds += f'<path d="M{x1},{y} C{x1+140},{y-th} {x2-220},{y-th*1.3} {x2},{y-6} C{x2-200},{y+th*0.5} {x1+180},{y+th*0.6} {x1},{y}Z" fill="#fff4ea" opacity="{op}"/>'

FAR_UP = "M-60,1080 C120,1020 260,700 420,690 C560,682 640,760 760,720 C900,676 1000,860 1140,900 L1140,1100 L-60,1100Z"
FAR_DOWN = "M-60,1080 C120,1070 260,1050 420,1052 C560,1054 640,1060 760,1056 C900,1050 1000,1066 1140,1068 L1140,1100 L-60,1100Z"

svg = f"""
<svg viewBox="0 0 1080 {PH}" width="1080" height="{PH}" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0">
  <defs>{defs}</defs>
  <rect width="1080" height="1100" fill="url(#s5-sky)"/>
  <circle cx="830" cy="1000" r="520" fill="url(#s5-sun)"/>
  <g id="s5-clouds">{clouds}</g>
  <path d="M-60,1068 L-60,1010 C60,990 160,950 260,940 C330,934 380,960 450,990 L520,1068Z" fill="#b9a0b4" opacity="0.9"/>
  <g id="s5-city">{city}</g>
  <path id="s5-far" d="{FAR_UP}" fill="url(#s5-dune2)"/>
  <path d="M-60,1100 C200,1060 420,1110 640,1080 C820,1056 960,1090 1140,1070 L1140,1500 L-60,1500Z" fill="url(#s5-dune)"/>
  <path d="M-60,1100 C200,1060 420,1110 640,1080 C820,1056 960,1090 1140,1070" stroke="#fff0cc" stroke-width="4" fill="none" opacity="0.8"/>
  <path d="M560,1500 C540,1420 500,1380 520,1320 C540,1260 600,1200 640,1110" stroke="#e8c08a" stroke-width="14" fill="none" stroke-linecap="round"/>
  {walkers}
  <path d="M-60,1380 C200,1360 500,1400 1140,1370 L1140,3220 L-60,3220Z" fill="#d6a86c"/>
  {fields}
  {oasis_svg}
  {fal}
  {fg_palms}
</svg>
"""

body = f"""
    <div id="s5-wrap" class="clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow style="position:absolute;inset:0;overflow:hidden">
      <div id="s5-cam" style="position:absolute;left:0;top:0;width:1080px;height:{PH}px">
        {svg}
      </div>
      <div id="s5-t1" class="hd" style="top:330px;font-size:168px;color:#fff6e2;text-shadow:0 6px 30px rgba(70,30,10,.65)">زايد الخير</div>
      <div id="s5-t2" class="lb" style="top:560px;left:0;right:0;font-size:58px;color:#fff1d6;text-shadow:0 3px 16px rgba(70,30,10,.7)"><span class="w">مسيرة</span> <span class="w">عطاء</span> <span class="w">لا</span> <span class="w">تنتهي</span></div>
    </div>
"""

script = f"""
    const tl = gsap.timeline({{ paused: true }});
    const D = {DUR};
    // tilt up from the flowing falaj to the horizon
    tl.fromTo("#s5-cam", {{ y: -{TILT}, scale: 1.04, transformOrigin: "540px 50%" }}, {{ y: 0, scale: 1, duration: 4.0, ease: "power2.inOut" }}, 0);
    // water keeps flowing
    tl.fromTo("#s5-shine", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": -700 }}, duration: D, ease: "none" }}, 0);
    tl.fromTo("#s5-shine2", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": -560 }}, duration: D, ease: "none" }}, 0);
    tl.fromTo("#s5-shine3", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": -640 }}, duration: D, ease: "none" }}, 0);
    // the far dunes settle and the modern skyline rises in their place
    tl.fromTo("#s5-far", {{ attr: {{ d: "{FAR_UP}" }} }}, {{ attr: {{ d: "{FAR_DOWN}" }}, duration: 2.6, ease: "power2.inOut" }}, 1.5);
    tl.fromTo("#s5-city", {{ y: 380 }}, {{ y: 0, duration: 2.6, ease: "power3.out" }}, 1.6);
    tl.fromTo("#s5-clouds", {{ x: 0 }}, {{ x: -60, duration: D, ease: "none" }}, 0);
    // walkers head toward the city
    for (let i = 0; i < 4; i++) tl.fromTo("#s5-wk" + i + " > g", {{ x: 0, y: 0 }}, {{ x: 30, y: -70, scale: 0.8, svgOrigin: "0 0", duration: D, ease: "none" }}, 0);
    // closing title
    tl.fromTo("#s5-t1", {{ opacity: 0, filter: "blur(14px)", scale: 1.04 }}, {{ opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.7, ease: "expo.out" }}, 3.55);
    tl.fromTo("#s5-t2 .w", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, stagger: 0.1, ease: "power3.out" }}, 4.2);
"""

open(OUT + "s5.html", "w").write(scene("s5", DUR, defs, body, script))
print("s5 ok", len(open(OUT + "s5.html").read()))
