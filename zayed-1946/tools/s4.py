import random, math
from common import *

rnd = random.Random(44)
DUR = 7.0
K, Y0 = -0.25, 1260.0          # oblique skew of the ground plane
def scr(x, y): return (x + K * (y - Y0), y)

# main falaj in plane coordinates (cubic segments)
SEG = [((560, 590), (520, 760), (660, 860), (610, 1000)),
       ((610, 1000), (560, 1150), (420, 1220), (460, 1380)),
       ((460, 1380), (500, 1540), (650, 1600), (610, 1760)),
       ((610, 1760), (590, 1850), (550, 1920), (540, 1990))]
MAIN = "M560,590 " + " ".join(f"C{a[1][0]},{a[1][1]} {a[2][0]},{a[2][1]} {a[3][0]},{a[3][1]}" for a in SEG)
def cub(p, t):
    a, b, c, d = p
    m = 1 - t
    return (m**3*a[0] + 3*m*m*t*b[0] + 3*m*t*t*c[0] + t**3*d[0], m**3*a[1] + 3*m*m*t*b[1] + 3*m*t*t*c[1] + t**3*d[1])
samples = []
for sg in SEG:
    for i in range(60):
        samples.append(cub(sg, i / 60))
samples.append(SEG[-1][3])
acc = [0.0]
for i in range(1, len(samples)):
    acc.append(acc[-1] + math.hypot(samples[i][0] - samples[i-1][0], samples[i][1] - samples[i-1][1]))
TOTAL = acc[-1]
T_START, T_FLOW = 0.35, 3.0
def at_y(y):
    best = min(range(len(samples)), key=lambda i: abs(samples[i][1] - y))
    return samples[best][0], T_START + T_FLOW * acc[best] / TOTAL

# ---------- plots ----------
greens = ["#3B7A57", "#4b8a4a", "#74A12E", "#5e9a3a", "#447f50"]
plots_base, plots_green = "", ""
script_green = []
rows = []
y = 612
while y < 1960:
    h = 112 + (y - 600) * 0.06
    rows.append((y, y + h)); y += h + 16
pid = 0
branches = []
for ri, (y0, y1) in enumerate(rows):
    cx0, _ = at_y(y0); cx1, _ = at_y(y1)
    _, tarr = at_y((y0 + y1) / 2)
    for side in (-1, 1):
        if side < 0:
            edges = [-380, rnd.uniform(-140, -40), rnd.uniform(140, 260), None]
        else:
            edges = [None, rnd.uniform(840, 960), rnd.uniform(1080, 1180), 1420]
        for j in range(3):
            a, b = edges[j], edges[j + 1]
            if side < 0 and b is None:
                quad_ = [(a, y0), (cx0 - 62, y0), (cx1 - 62, y1), (a, y1)]
            elif side > 0 and a is None:
                quad_ = [(cx0 + 62, y0), (b, y0), (b, y1), (cx1 + 62, y1)]
            else:
                quad_ = [(a, y0), (b, y0), (b, y1), (a, y1)]
            sand = rnd.choice(["#D9B382", "#d4ab78", "#ddb98a", "#cfa673"])
            plots_base += f'<path d="M{pts(quad_).replace(" ", " L")}Z" fill="{sand}" stroke="#b08452" stroke-width="12" stroke-linejoin="round"/>'
            # crops
            xs = [p[0] for p in quad_]
            rowsl = ""
            yy = y0 + 12
            while yy < y1 - 8:
                t = (yy - y0) / (y1 - y0)
                xl = quad_[0][0] + (quad_[3][0] - quad_[0][0]) * t + 10
                xr = quad_[1][0] + (quad_[2][0] - quad_[1][0]) * t - 10
                rowsl += f"M{f(xl)},{f(yy)} L{f(xr)},{f(yy)} "
                yy += 15
            col = rnd.choice(greens)
            delay = tarr + 0.15 + (0.12 * j if side > 0 else 0.12 * (2 - j))
            plots_green += (f'<g id="s4-g{pid}" opacity="0"><path d="M{pts(quad_).replace(" ", " L")}Z" fill="{col}" stroke="#7a6a3a" stroke-width="12" stroke-linejoin="round"/>'
                            f'<path d="{rowsl}" stroke="#2c5e36" stroke-width="5" stroke-linecap="round" opacity="0.7"/>'
                            f'<path d="{rowsl}" stroke="#9cc55a" stroke-width="2" stroke-linecap="round" opacity="0.55" transform="translate(0,-3)"/></g>')
            script_green.append((pid, round(delay, 2)))
            pid += 1
    if ri % 2 == 1 and ri < len(rows) - 1:
        side = -1 if ri % 4 == 1 else 1
        yb = y1 + 8
        cxb, tb = at_y(yb)
        end = -380 if side < 0 else 1420
        branches.append((f"M{f(cxb)},{f(yb)} L{end},{f(yb)}", tb))

# ---------- falaj strokes ----------
falaj = f'<path d="{MAIN}" stroke="#c9935c" stroke-width="96" fill="none" stroke-linecap="round"/>'
falaj += f'<path d="{MAIN}" stroke="#6e4a2c" stroke-width="56" fill="none" stroke-linecap="round"/>'
falaj += f'<path d="{MAIN}" stroke="#4e321c" stroke-width="10" fill="none" stroke-dasharray="6 18" opacity="0.6"/>'
for i, (d, tb) in enumerate(branches):
    falaj += f'<path d="{d}" stroke="#a87444" stroke-width="30" fill="none"/>'
water = f'<path id="s4-water" d="{MAIN}" opacity="0" pathLength="1" stroke="#2B8CBE" stroke-width="44" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s4-water2" d="{MAIN}" opacity="0" pathLength="1" stroke="#56b9de" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s4-shine" d="{MAIN}" stroke="#d9fbff" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="120 60 30 150" opacity="0"/>'
for i, (d, tb) in enumerate(branches):
    water += f'<path id="s4-br{i}" d="{d}" pathLength="1" stroke="#3a9fcf" stroke-width="16" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'

ground = f'<g transform="matrix(1,0,{K},1,{f(-K*Y0)},0)">' + '<rect x="-500" y="590" width="2100" height="1400" fill="#c99a62"/>' + plots_base + plots_green + falaj + water + '</g>'

# ---------- palms & farmers (upright, placed in screen space) ----------
uprights = []
script_palms = []
k = 0
for yy in range(650, 1960, 92):
    cx, t = at_y(yy)
    for side in (-1, 1):
        if rnd.random() < 0.25: continue
        x = cx + side * rnd.uniform(78, 120)
        sx, sy = scr(x, yy)
        h = 70 + (yy - 600) * 0.1
        uprights.append((sy, f'<g transform="translate({f(sx)},{f(sy)})"><g id="s4-p{k}">{palm(h, rnd.uniform(-0.08, 0.08), seed=400+k, dates=h > 140, sw=1.4)}</g></g>'))
        script_palms.append((k, round(t + 0.1 + rnd.uniform(0, 0.15), 2)))
        k += 1
for i in range(10):  # palms inside the plots
    yy = rnd.uniform(700, 1900)
    cx, t = at_y(yy)
    x = rnd.choice([rnd.uniform(-200, cx - 250), rnd.uniform(cx + 250, 1200)])
    sx, sy = scr(x, yy)
    h = 70 + (yy - 600) * 0.1
    uprights.append((sy, f'<g transform="translate({f(sx)},{f(sy)})"><g id="s4-p{k}">{palm(h, rnd.uniform(-0.08, 0.08), seed=500+k, sw=1.4)}</g></g>'))
    script_palms.append((k, round(t + 0.45, 2)))
    k += 1
farm = []
for i, (yy, side, var) in enumerate([(820, 1, 0), (1120, -1, 1), (1450, 1, 1), (1640, -1, 0), (1850, 1, 0)]):
    cx, t = at_y(yy)
    sx, sy = scr(cx + side * 120, yy)
    s = 0.14 + (yy - 600) * 0.00011
    uprights.append((sy, f'<g transform="translate({f(sx)},{f(sy)})"><g id="s4-f{i}">'
                         f'<ellipse cx="0" cy="0" rx="{f(60*s)}" ry="{f(14*s)}" fill="#3a2414" opacity="0.3"/>'
                         f'{person_back(s=s, variant=var, kandura="#f3ece0", ghutra="#fbf6ec")}</g></g>'))
    farm.append((i, round(t + 0.3, 2)))
uprights.sort(key=lambda a: a[0])
up_svg = "".join(s for _, s in uprights)

# ---------- horizon: old dunes, then the new city rises ----------
def win_grid(x, y, w, h, cols, rows_, col="#6d8fa6"):
    s = ""
    cw, rh = w / cols, h / rows_
    for c in range(cols):
        for r in range(rows_):
            s += f'<rect x="{f(x+c*cw+cw*0.22)}" y="{f(y+r*rh+rh*0.22)}" width="{f(cw*0.56)}" height="{f(rh*0.5)}" fill="{col}" stroke="#3d4a55" stroke-width="1"/>'
    return s
def block(x, y, w, h, d=26, front="#f3e6cc", side="#c9a77a", top="#fff6e0"):
    return (f'<path d="M{x},{y} L{x+w},{y} L{x+w},{y-h} L{x},{y-h}Z" fill="{front}" stroke="#4a3320" stroke-width="2.5"/>'
            f'<path d="M{x+w},{y} L{x+w+d},{y-d*0.5} L{x+w+d},{y-h-d*0.5} L{x+w},{y-h}Z" fill="{side}" stroke="#4a3320" stroke-width="2.5"/>'
            f'<path d="M{x},{y-h} L{x+w},{y-h} L{x+w+d},{y-h-d*0.5} L{x+d},{y-h-d*0.5}Z" fill="{top}" stroke="#4a3320" stroke-width="2"/>')
HZ = 596
school = block(70, HZ, 300, 150) + win_grid(80, HZ - 145, 280, 100, 9, 2) + \
    f'<path d="M190,{HZ} L190,{HZ-40} Q220,{HZ-70} 250,{HZ-40} L250,{HZ}Z" fill="#7a5232" stroke="#4a3320" stroke-width="2"/>' + \
    f'<rect x="388" y="{HZ-300}" width="6" height="300" fill="#6b6b6b"/>' + \
    f'<g transform="translate(394,{HZ-298})"><rect width="22" height="60" fill="#c8202f"/><rect x="22" width="78" height="20" fill="#00843d"/><rect x="22" y="20" width="78" height="20" fill="#ffffff"/><rect x="22" y="40" width="78" height="20" fill="#111"/><rect width="100" height="60" fill="none" stroke="#333" stroke-width="1.5"/></g>'
hospital = block(470, HZ, 190, 330, 30, "#f7f1e4", "#cbbfa6") + win_grid(480, HZ - 300, 170, 240, 5, 6) + \
    f'<rect x="530" y="{HZ-60}" width="70" height="60" fill="#8ec3d6" stroke="#4a3320" stroke-width="2"/>' + \
    f'<g transform="translate(565,{HZ-385})"><rect x="-44" y="-40" width="88" height="80" rx="6" fill="#ffffff" stroke="#4a3320" stroke-width="2.5"/>' + \
    '<path d="M10,-26 A28,28 0 1,0 10,26 A22,22 0 1,1 10,-26Z" fill="#d7262e"/></g>'
houses = ""
for i, (x, w, h) in enumerate([(700, 110, 110), (830, 120, 130), (965, 100, 100)]):
    houses += block(x, HZ, w, h, 22, "#f0dcb8", "#c79f6c", "#fbeccc")
    houses += f'<path d="M{x+w*0.35},{HZ} L{x+w*0.35},{HZ-h*0.45} Q{x+w*0.5},{HZ-h*0.62} {x+w*0.65},{HZ-h*0.45} L{x+w*0.65},{HZ}Z" fill="#7a5232" stroke="#4a3320" stroke-width="2"/>'
    houses += win_grid(x + 6, HZ - h + 8, w - 12, h * 0.3, 3, 1)
    for m in range(int(w // 16)):
        houses += f'<path d="M{x+4+m*16},{HZ-h} l4,-9 l4,9Z" fill="#f0dcb8" stroke="#4a3320" stroke-width="1"/>'
city = f'<g id="s4-b0">{school}</g><g id="s4-b1">{hospital}</g><g id="s4-b2">{houses}</g>'

old = ""
for x, w, h in [(250, 60, 34), (330, 44, 26), (620, 70, 38), (720, 50, 28)]:
    old += block(x, HZ - 12, w, h, 14, "#d6a46a", "#9c6a3c", "#e8bf86")

defs = f"""
<linearGradient id="s4-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fa8cf"/><stop offset="0.55" stop-color="#d8d0b0"/><stop offset="1" stop-color="#f4c47c"/></linearGradient>
<linearGradient id="s4-dune" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0c486"/><stop offset="1" stop-color="#c9905a"/></linearGradient>
<clipPath id="s4-hzclip"><rect x="-200" y="-200" width="1500" height="{HZ+200}"/></clipPath>
<radialGradient id="s4-sun" cx="0.85" cy="0.1" r="0.9"><stop offset="0" stop-color="#ffe4a0" stop-opacity="0.5"/><stop offset="1" stop-color="#ffe4a0" stop-opacity="0"/></radialGradient>
"""

svg = f"""
<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0" overflow="visible">
  <defs>{defs}</defs>
  <rect x="-200" y="-200" width="1480" height="2400" fill="url(#s4-sky)"/>
  <path d="M-200,170 C100,150 300,190 520,160 C700,140 900,170 1280,150" stroke="#fff6e6" stroke-width="18" fill="none" opacity="0.5" stroke-linecap="round"/>
  <path d="M-100,300 C200,285 380,310 640,290" stroke="#fff6e6" stroke-width="10" fill="none" opacity="0.4" stroke-linecap="round"/>
  <path d="M-200,520 C100,470 300,500 520,480 C760,456 960,500 1280,470 L1280,620 L-200,620Z" fill="#e6b378" opacity="0.8"/>
  <g clip-path="url(#s4-hzclip)">{city}</g>
  {old}
  <path d="M-200,{HZ} C200,{HZ-18} 600,{HZ+8} 1280,{HZ-10} L1280,640 L-200,640Z" fill="url(#s4-dune)"/>
  {ground}
  {up_svg}
  <rect x="-200" y="-200" width="1480" height="2400" fill="url(#s4-sun)"/>
</svg>
"""

body = f"""
    <div id="s4-wrap" class="clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow style="position:absolute;inset:0;overflow:hidden">
      <div id="s4-cam" style="position:absolute;inset:0">
        {svg}
      </div>
      <div id="s4-t" class="hd" style="top:190px;font-size:104px;color:#3b1f0e;text-shadow:0 0 22px rgba(255,240,210,.85)"><span class="w">تدفّق</span> <span class="w">الماء..</span><br><span class="w">فازدهرت</span> <span class="w">العين</span></div>
      <div id="s4-l0" class="lb" style="top:630px;left:110px;width:260px;font-size:40px;color:#fff6e4;text-shadow:0 3px 12px rgba(30,15,5,.85)">مدارس</div>
      <div id="s4-l1" class="lb" style="top:630px;left:430px;width:270px;font-size:40px;color:#fff6e4;text-shadow:0 3px 12px rgba(30,15,5,.85)">مستشفيات</div>
      <div id="s4-l2" class="lb" style="top:630px;left:740px;width:300px;font-size:40px;color:#fff6e4;text-shadow:0 3px 12px rgba(30,15,5,.85)">بيوت للجميع</div>
    </div>
"""

gl = ",".join(f"[{p},{t}]" for p, t in script_green)
pl = ",".join(f"[{p},{t}]" for p, t in script_palms)
fl = ",".join(f"[{p},{t}]" for p, t in farm)
brl = ",".join(f"{round(t,2)}" for _, t in branches)
script = f"""
    const tl = gsap.timeline({{ paused: true }});
    const D = {DUR};
    // arrive from the whip (content drops in from above), then a slow drift
    tl.fromTo("#s4-cam", {{ y: -620, scale: 1.0, filter: "blur(14px)", transformOrigin: "540px 1000px" }}, {{ y: 0, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }}, 0);
    tl.to("#s4-cam", {{ scale: 1.06, y: 30, duration: 6.6, ease: "power1.inOut" }}, 0.4);
    // the water runs down the falaj and out into the branches
    tl.set(["#s4-water", "#s4-water2"], {{ opacity: 1 }}, {T_START});
    tl.to(["#s4-water", "#s4-water2"], {{ attr: {{ "stroke-dashoffset": 0 }}, duration: {T_FLOW}, ease: "none", stagger: 0.06 }}, {T_START});
    tl.fromTo("#s4-shine", {{ opacity: 0, attr: {{ "stroke-dashoffset": 0 }} }}, {{ opacity: 0.85, attr: {{ "stroke-dashoffset": -600 }}, duration: 6.5, ease: "none" }}, 0.5);
    [{brl}].forEach((t, i) => tl.to("#s4-br" + i, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.7, ease: "power1.out" }}, t));
    // fields turn green as the water reaches them
    [{gl}].forEach(([i, t]) => tl.fromTo("#s4-g" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7, ease: "power2.out" }}, t));
    // palms spring up
    [{pl}].forEach(([i, t]) => tl.fromTo("#s4-p" + i, {{ scale: 0, svgOrigin: "0 0" }}, {{ scale: 1, duration: 0.7, ease: "back.out(1.6)" }}, t));
    // farmers arrive at the banks and work
    [{fl}].forEach(([i, t]) => {{
      tl.fromTo("#s4-f" + i, {{ opacity: 0, y: 8 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, t);
      tl.fromTo("#s4-f" + i, {{ rotation: 0, svgOrigin: "0 0" }}, {{ rotation: i % 2 ? -9 : 9, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 5 }}, t + 0.4);
    }});
    // title
    tl.fromTo("#s4-t .w", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, stagger: 0.12, ease: "power3.out" }}, 0.55);
    tl.to("#s4-t", {{ opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, 3.55);
    // the new city rises on the horizon
    ["#s4-b0", "#s4-b1", "#s4-b2"].forEach((b, i) => tl.fromTo(b, {{ y: 420 }}, {{ y: 0, duration: 0.9, ease: "expo.out" }}, 4.0 + i * 0.3));
    ["#s4-l0", "#s4-l1", "#s4-l2"].forEach((l, i) => tl.fromTo(l, {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }}, 4.6 + i * 0.3));
"""

open(OUT + "s4.html", "w").write(scene("s4", DUR, defs, body, script))
print("s4 ok", len(open(OUT + "s4.html").read()), "plots", pid, "palms", k)
