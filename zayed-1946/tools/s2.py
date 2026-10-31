import random, math
from common import *

rnd = random.Random(22)
DUR = 6.0
VP = (540, 772)

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

defs = """
<linearGradient id="s2-sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#5a2f22"/><stop offset="0.35" stop-color="#a5552c"/><stop offset="0.7" stop-color="#e79a45"/><stop offset="1" stop-color="#ffe2a0"/>
</linearGradient>
<radialGradient id="s2-sunglow"><stop offset="0" stop-color="#fffbe6"/><stop offset="0.15" stop-color="#ffe7a6" stop-opacity="0.95"/><stop offset="0.45" stop-color="#E6A145" stop-opacity="0.45"/><stop offset="1" stop-color="#E6A145" stop-opacity="0"/></radialGradient>
<linearGradient id="s2-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a066"/><stop offset="0.4" stop-color="#a86a3e"/><stop offset="1" stop-color="#5a321b"/></linearGradient>
<linearGradient id="s2-wallL" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#b8763f"/><stop offset="1" stop-color="#6a3c1f"/></linearGradient>
<linearGradient id="s2-wallR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d1904f"/><stop offset="1" stop-color="#7d4724"/></linearGradient>
<linearGradient id="s2-bank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3a964"/><stop offset="1" stop-color="#9a5f32"/></linearGradient>
<linearGradient id="s2-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5e3a1e"/><stop offset="0.5" stop-color="#8a5a32"/><stop offset="1" stop-color="#4a2c16"/></linearGradient>
<linearGradient id="s2-leak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6d0"/><stop offset="1" stop-color="#ffc964"/></linearGradient>
<linearGradient id="s2-ray" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff3c4" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>
<linearGradient id="s2-rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset="0.35" stop-color="#e6a145" stop-opacity="0.6"/><stop offset="0.7" stop-color="#e6a145" stop-opacity="0"/></linearGradient>
"""

# horizon: mud houses and palms as warm silhouettes, both sides
hz = ""
for side in (-1, 1):
    for i in range(7):
        x = 540 + side * (110 + i * 95 + rnd.uniform(-20, 20))
        w = rnd.uniform(60, 110); h = rnd.uniform(30, 70)
        y = 772
        hz += f'<path d="M{f(x-w/2)},{y} L{f(x-w/2)},{f(y-h)} L{f(x+w/2)},{f(y-h)} L{f(x+w/2)},{y}Z" fill="#8a4e2a" stroke="#5b2f17" stroke-width="2"/>'
        hz += f'<path d="M{f(x-w/2)},{f(y-h)} L{f(x+w/2)},{f(y-h)}" stroke="#ffd58a" stroke-width="3" opacity="0.8"/>'
        for k in range(int(w // 12)):
            hz += f'<rect x="{f(x-w/2+3+k*12)}" y="{f(y-h-6)}" width="6" height="6" fill="#8a4e2a"/>'
        hz += f'<rect x="{f(x-6)}" y="{f(y-h*0.6)}" width="10" height="{f(h*0.4)}" fill="#4a2512"/>'
    for i in range(6):
        x = 540 + side * (60 + i * 120 + rnd.uniform(-30, 30))
        hz += f'<g transform="translate({f(x)},776)" opacity="0.9">{palm(rnd.uniform(110, 170), rnd.uniform(-0.1, 0.1), dry=True, seed=200+i*side, sw=1.2)}</g>'

# god rays from the vanishing point
rays = ""
for k in range(9):
    a = math.radians(-90 + (k - 4) * 17 + rnd.uniform(-4, 4))
    w = math.radians(rnd.uniform(3, 6))
    L = 1500
    p1 = (VP[0] + math.cos(a - w) * L, VP[1] + math.sin(a - w) * L)
    p2 = (VP[0] + math.cos(a + w) * L, VP[1] + math.sin(a + w) * L)
    rays += f'<path d="M{VP[0]},{VP[1]} L{f(p1[0])},{f(p1[1])} L{f(p2[0])},{f(p2[1])}Z" fill="url(#s2-ray)"/>'
for k in range(6):  # rays down the channel too
    a = math.radians(90 + (k - 2.5) * 18)
    w = math.radians(3)
    L = 1400
    p1 = (VP[0] + math.cos(a - w) * L, VP[1] + math.sin(a - w) * L)
    p2 = (VP[0] + math.cos(a + w) * L, VP[1] + math.sin(a + w) * L)
    rays += f'<path d="M{VP[0]},{VP[1]} L{f(p1[0])},{f(p1[1])} L{f(p2[0])},{f(p2[1])}Z" fill="#ffe7a8" opacity="0.35"/>'

# channel geometry
FL0, FL1 = (505, 790), (-100, 1920)
FR0, FR1 = (575, 790), (1180, 1920)
WL0, WL1 = (470, 776), (-100, 1250)
WR0, WR1 = (610, 776), (1180, 1250)
chan = ""
chan += f'<path d="M-140,772 L{WL0[0]},{WL0[1]} L{WL1[0]},{WL1[1]} L-140,1260Z" fill="url(#s2-bank)"/>'
chan += f'<path d="M1220,772 L{WR0[0]},{WR0[1]} L{WR1[0]},{WR1[1]} L1220,1260Z" fill="url(#s2-bank)"/>'
chan += f'<path d="M{WL0[0]},{WL0[1]} L{WL1[0]},{WL1[1]} L{FL1[0]},{FL1[1]} L{FL0[0]},{FL0[1]}Z" fill="url(#s2-wallL)" stroke="#3a2010" stroke-width="2"/>'
chan += f'<path d="M{WR0[0]},{WR0[1]} L{WR1[0]},{WR1[1]} L{FR1[0]},{FR1[1]} L{FR0[0]},{FR0[1]}Z" fill="url(#s2-wallR)" stroke="#3a2010" stroke-width="2"/>'
chan += f'<path d="M{FL0[0]},{FL0[1]} L{FL1[0]},{FL1[1]} L{FR1[0]},{FR1[1]} L{FR0[0]},{FR0[1]}Z" fill="url(#s2-floor)"/>'
# wall strata (lines converging on the VP)
strata = ""
for k in range(1, 9):
    t = k / 9
    a = lerp(WL1, FL1, t); strata += f"M{f(a[0])},{f(a[1])} L{f(lerp(WL0, FL0, t)[0])},{f(lerp(WL0, FL0, t)[1])} "
    b = lerp(WR1, FR1, t); strata += f"M{f(b[0])},{f(b[1])} L{f(lerp(WR0, FR0, t)[0])},{f(lerp(WR0, FR0, t)[1])} "
chan += f'<path d="{strata}" stroke="#4a2814" stroke-width="2.5" opacity="0.45" fill="none"/>'
# rim of the banks catching light
chan += f'<path d="M{WL1[0]},{WL1[1]} L{WL0[0]},{WL0[1]} M{WR1[0]},{WR1[1]} L{WR0[0]},{WR0[1]}" stroke="#ffd58a" stroke-width="5" opacity="0.85"/>'
# cracked floor (perspective)
cracks = ""
for i in range(70):
    t = rnd.uniform(0.05, 1) ** 1.5
    y = 790 + (1920 - 790) * t
    xl = FL0[0] + (FL1[0] - FL0[0]) * t; xr = FR0[0] + (FR1[0] - FR0[0]) * t
    x = rnd.uniform(xl, xr)
    sc = 0.2 + t
    pts_ = [(x, y)]
    for j in range(rnd.randint(3, 6)):
        x += rnd.uniform(-50, 50) * sc; y += rnd.uniform(-8, 8) * sc
        pts_.append((x, y))
    cracks += "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts_) + " "
chan += f'<path d="{cracks}" stroke="#4a2612" stroke-width="2.4" fill="none" opacity="0.7" stroke-linejoin="round"/>'
# old tree on the left bank, roots over the wall
tree = '<g transform="translate(150,1050)">'
tree += '<path d="M-30,0 C-40,-120 -20,-260 -60,-420 L-20,-420 C10,-280 10,-140 30,0Z" fill="#5a3418" stroke="#2a170b" stroke-width="3"/>'
for k in range(6):
    tree += f'<path d="M{-10+k*8},0 C{-20+k*14},{40+k*10} {10+k*16},{90+k*14} {-5+k*20},{160+k*18}" stroke="#4a2a14" stroke-width="{7-k*0.6:.1f}" fill="none" stroke-linecap="round"/>'
tree += f'<g transform="translate(-40,-420)">{palm(1, 0, dry=True, seed=9)}</g>'
tree += '</g>'

# the sluice gate: light behind, planks, beams, posts
X0, X1, YT, YB = 360, 720, 880, 1060
gate = f'<rect id="s2-leak" x="{X0}" y="{YT-10}" width="{X1-X0}" height="{YB-YT+10}" fill="url(#s2-leak)"/>'
planks = ""
n = 7
pw = (X1 - X0) / n
for i in range(n):
    x = X0 + i * pw + 2
    top = YT + rnd.uniform(-14, 10)
    w = pw - 5
    jag = f"M{f(x)},{YB} L{f(x)},{f(top+6)} L{f(x+w*0.3)},{f(top)} L{f(x+w*0.6)},{f(top+8)} L{f(x+w)},{f(top+2)} L{f(x+w)},{YB}Z"
    grain = f"M{f(x+w*0.3)},{f(top+12)} C{f(x+w*0.4)},{f(top+60)} {f(x+w*0.2)},{f(top+110)} {f(x+w*0.35)},{YB-4} M{f(x+w*0.7)},{f(top+14)} C{f(x+w*0.6)},{f(top+70)} {f(x+w*0.8)},{f(top+120)} {f(x+w*0.68)},{YB-4}"
    planks += (f'<g id="s2-pl{i}"><path d="{jag}" fill="url(#s2-wood)" stroke="#2a170b" stroke-width="2.5"/>'
               f'<path d="{grain}" stroke="#3a2210" stroke-width="1.6" fill="none" opacity="0.7"/>'
               f'<circle cx="{f(x+w/2)}" cy="922" r="3" fill="#2a1a10"/><circle cx="{f(x+w/2)}" cy="1012" r="3" fill="#2a1a10"/></g>')
beams = ""
for j, y in enumerate((914, 1004)):
    mid = (X0 + X1) / 2 + (20 if j else -15)
    beams += f'<g id="s2-bmL{j}"><path d="M{X0-14},{y} L{f(mid)},{y+2} L{f(mid-6)},{y+18} L{X0-14},{y+16}Z" fill="#6e4526" stroke="#2a170b" stroke-width="2.5"/></g>'
    beams += f'<g id="s2-bmR{j}"><path d="M{f(mid)},{y+2} L{X1+14},{y} L{X1+14},{y+16} L{f(mid-6)},{y+18}Z" fill="#7a4d2a" stroke="#2a170b" stroke-width="2.5"/></g>'
posts = (f'<path d="M{X0-30},{YB+6} L{X0-28},{YT-40} L{X0-8},{YT-46} L{X0-6},{YB+4}Z" fill="#4e2f18" stroke="#2a170b" stroke-width="2.5"/>'
         f'<path d="M{X1+6},{YB+4} L{X1+8},{YT-46} L{X1+28},{YT-40} L{X1+30},{YB+6}Z" fill="#4e2f18" stroke="#2a170b" stroke-width="2.5"/>')
gate += f'<g id="s2-gate">{planks}{beams}</g>{posts}'

# crowd (backlit silhouettes, no faces)
crowd = ""
people = [(470, 2000, 1.45, 1), (330, 1960, 1.55, 0), (860, 1975, 1.6, 0), (130, 2010, 2.0, 0), (1040, 2040, 2.1, 1)]
for x, base, s, v in people:
    crowd += f'<g transform="translate({x},{base})">{person_back("#2a170c", "url(#s2-rim)", s, v)}</g>'
# leader with bisht and raising arm
LX, LB, LS = 640, 2085, 2.3
leader = f'<g transform="translate({LX},{LB})">{person_back("#1f1108", "url(#s2-rim)", LS, 0, bisht=True)}</g>'
PX, PY = LX + 55 * LS, LB - 300 * LS
arm = (f'<g id="s2-arm">'
       f'<path d="M-60,0 C-96,-120 -104,-262 -66,-386 C-52,-300 -30,-150 44,-18Z" fill="#1f1108"/>'
       f'<path d="M-48,12 C-50,-150 -40,-350 -30,-520 L30,-520 C40,-350 60,-150 70,12Z" fill="#1f1108"/>'
       f'<path d="M-30,-515 L-34,-590 Q-34,-602 -24,-602 L-20,-560 L-16,-625 Q-14,-637 -4,-635 L-2,-570 L4,-632 Q8,-642 16,-638 L18,-568 L24,-618 Q30,-626 36,-616 L36,-550 L48,-575 Q58,-580 56,-566 L40,-515Z" fill="#1f1108"/>'
       f'<path d="M30,-520 C40,-350 60,-150 70,12 M36,-616 L36,-550 L48,-575 Q58,-580 56,-566 L40,-515 M-34,-590 Q-34,-602 -24,-602 M-16,-625 Q-14,-637 -4,-635 M4,-632 Q8,-642 16,-638 M24,-618 Q30,-626 36,-616" stroke="#ffcf7a" stroke-width="4" fill="none" stroke-linecap="round"/>'
       f'</g>')
leader += f'<g transform="translate({f(PX)},{f(PY)})">{arm}</g>'

svg = f"""
<svg viewBox="-80 0 1240 1920" width="1240" height="1920" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:-80px;top:0">
  <defs>{defs}</defs>
  <rect x="-80" width="1240" height="1920" fill="url(#s2-sky)"/>
  <circle id="s2-glow" cx="{VP[0]}" cy="{VP[1]}" r="640" fill="url(#s2-sunglow)"/>
  <g id="s2-rays" opacity="0">{rays}</g>
  <g>{hz}</g>
  {chan}
  {gate}
  <g id="s2-burst" opacity="0"><circle cx="540" cy="960" r="260" fill="url(#s2-sunglow)"/></g>
  {crowd}
  {leader}
</svg>
"""

body = f"""
    <div id="s2-wrap" class="clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow style="position:absolute;inset:0;overflow:hidden">
      <div id="s2-cam" style="position:absolute;inset:0">
        {svg}
        <canvas id="s2-fx" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>
      </div>
      <div id="s2-flood" style="position:absolute;inset:0;background:radial-gradient(70% 55% at 50% 50%, #fff3cf 0%, #ffd27a 55%, #f2a948 100%);opacity:0"></div>
      <div id="s2-l1" class="hd" style="top:206px;font-size:64px;color:#ffe8c0;text-shadow:0 3px 14px rgba(50,20,8,.6)"><span class="w">الماء هبة من الله</span></div>
      <div id="s2-l2" class="hd" style="top:318px;font-size:138px;color:#fff4dc;text-shadow:0 6px 26px rgba(60,25,8,.6)"><span class="w">وحقٌ</span> <span class="w">للجميع</span></div>
    </div>
"""

script = RNG_JS + f"""
    const tl = gsap.timeline({{ paused: true }});
    const D = {DUR};
    // camera: slow pan right-to-left across the crowd, slight push
    tl.fromTo("#s2-cam", {{ x: 55, scale: 1.04, transformOrigin: "540px 900px" }}, {{ x: -55, scale: 1.0, duration: D, ease: "power1.inOut" }}, 0);
    // leader raises his hand
    tl.fromTo("#s2-arm", {{ rotation: 168, svgOrigin: "0 0" }}, {{ rotation: 8, svgOrigin: "0 0", duration: 0.75, ease: "back.out(1.3)" }}, 0.55);
    // the gate strains, then bursts
    const planks = [0,1,2,3,4,5,6].map(i => "#s2-pl" + i);
    [2.35, 2.5, 2.62, 2.74, 2.86].forEach((t, k) => {{
      tl.to("#s2-gate", {{ x: (k % 2 ? -1 : 1) * (2 + k), duration: 0.06, ease: "none" }}, t);
    }});
    tl.to("#s2-gate", {{ x: 0, duration: 0.06 }}, 2.95);
    tl.fromTo("#s2-leak", {{ opacity: 0.55 }}, {{ opacity: 1, duration: 0.6, ease: "power2.in" }}, 2.4);
    const fly = [[-230,-60,-70],[-160,40,-45],[-70,90,-20],[10,140,8],[90,80,28],[170,30,52],[250,-40,75]];
    planks.forEach((p, i) => {{
      const [dx, dy, r] = fly[i];
      tl.fromTo(p, {{ x: 0, y: 0, rotation: 0, scale: 1, opacity: 1, transformOrigin: "50% 100%" }},
        {{ x: dx * 1.6, y: 420 + dy, rotation: r * 1.4, scale: 2.4, opacity: 0, duration: 0.95, ease: "power2.in" }}, 3.0 + i * 0.015 * Math.abs(3 - i));
    }});
    ["#s2-bmL0","#s2-bmL1"].forEach((b, j) => tl.fromTo(b, {{ x: 0, y: 0, rotation: 0, opacity: 1, transformOrigin: "0% 50%" }}, {{ x: -260, y: 380, rotation: -55, scale: 2, opacity: 0, duration: 0.85, ease: "power2.in" }}, 2.98 + j * 0.03));
    ["#s2-bmR0","#s2-bmR1"].forEach((b, j) => tl.fromTo(b, {{ x: 0, y: 0, rotation: 0, opacity: 1, transformOrigin: "100% 50%" }}, {{ x: 260, y: 380, rotation: 60, scale: 2, opacity: 0, duration: 0.85, ease: "power2.in" }}, 3.0 + j * 0.03));
    // light floods through the opening
    tl.fromTo("#s2-burst", {{ opacity: 0, scale: 0.4, transformOrigin: "540px 960px" }}, {{ opacity: 1, scale: 2.6, duration: 1.6, ease: "power2.out" }}, 3.0);
    tl.fromTo("#s2-rays", {{ opacity: 0, rotation: -3, svgOrigin: "540 772" }}, {{ opacity: 0.85, rotation: 3, duration: 2.8, ease: "power1.out" }}, 3.05);
    tl.fromTo("#s2-glow", {{ scale: 0.85, svgOrigin: "540 772" }}, {{ scale: 1.5, duration: 3, ease: "power2.out" }}, 3.0);
    tl.fromTo("#s2-flood", {{ opacity: 0 }}, {{ opacity: 0.96, duration: 1.1, ease: "power2.in" }}, 4.9);
    // words
    tl.fromTo("#s2-l1 .w", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.16, stagger: 0.08, ease: "power3.out" }}, 3.2);
    tl.fromTo("#s2-l2 .w", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.24, stagger: 0.14, ease: "power3.out" }}, 3.55);

    // splinters and dust from the gate
    const cv = document.getElementById("s2-fx"), ctx = cv.getContext("2d");
    const R = rng(21), P = [];
    for (let i = 0; i < 140; i++) {{
      const a = -Math.PI * (0.05 + 0.9 * R());
      const sp = 300 + R() * 900;
      P.push({{ t0: 3.0 + R() * 0.12, x0: 400 + R() * 280, y0: 900 + R() * 150, vx: Math.cos(a) * sp * 0.8, vy: -Math.sin(a) * sp * 0.25 + 200 + R() * 500,
               life: 0.6 + R() * 0.9, w: R() < 0.5 ? 12 + R() * 22 : 1.2 + R() * 2.2, rot: R() * 6, vr: (R() - 0.5) * 14, wood: null }});
    }}
    function draw(t) {{
      ctx.clearRect(0, 0, 1080, 1920);
      for (const p of P) {{
        const u = t - p.t0;
        if (u < 0 || u > p.life) continue;
        const k = u / p.life, s = 1 + u * 1.8;
        const x = p.x0 + p.vx * u, y = p.y0 + p.vy * u + 380 * u * u;
        ctx.save(); ctx.translate(x, y); ctx.rotate(p.rot + p.vr * u);
        ctx.globalAlpha = (1 - k) * 0.95;
        if (p.w > 8) {{ ctx.fillStyle = "#5a361c"; ctx.fillRect(-p.w * s / 2, -2.5 * s, p.w * s, 5 * s); }}
        else {{ ctx.fillStyle = "#ffe2a0"; ctx.beginPath(); ctx.arc(0, 0, p.w * (1 + u * 0.6), 0, 6.283); ctx.fill(); }}
        ctx.restore();
      }}
    }}
    const clock = {{ t: 0 }};
    tl.fromTo(clock, {{ t: 0 }}, {{ t: D, duration: D, ease: "none", onUpdate: () => draw(clock.t) }}, 0);
    draw(0);
"""

open(OUT + "s2.html", "w").write(scene("s2", DUR, defs, body, script))
print("s2 ok", len(open(OUT + "s2.html").read()))
