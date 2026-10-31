import random, math
from common import *

rnd = random.Random(33)
DUR = 7.0
A_TIMES = [0.8, 2.0, 3.2, 4.4]
B_TIMES = [1.4, 2.6, 3.8]

def norm(v):
    L = math.hypot(*v); return (v[0] / L, v[1] / L)
def add(a, b, k=1): return (a[0] + b[0] * k, a[1] + b[1] * k)
def ang(v): return math.degrees(math.atan2(v[1], v[0]))

def sleeve(S, W, ws, we, gid):
    u = norm((W[0] - S[0], W[1] - S[1])); n = (-u[1], u[0])
    L = math.hypot(W[0] - S[0], W[1] - S[1])
    a1, a2 = add(S, n, ws / 2), add(W, n, we / 2)
    b1, b2 = add(S, n, -ws / 2), add(W, n, -we / 2)
    c1 = add(add(S, u, L * 0.5), n, ws * 0.42 + 10)
    c2 = add(add(S, u, L * 0.5), n, -ws * 0.42 - 10)
    d = f"M{f(a1[0])},{f(a1[1])} Q{f(c1[0])},{f(c1[1])} {f(a2[0])},{f(a2[1])} L{f(b2[0])},{f(b2[1])} Q{f(c2[0])},{f(c2[1])} {f(b1[0])},{f(b1[1])}Z"
    s = f'<path d="{d}" fill="url(#{gid})" stroke="#3a2a1a" stroke-width="3"/>'
    folds = ""
    for k, off in enumerate((-0.25, 0.05, 0.3)):
        p0 = add(add(S, u, L * 0.15), n, ws * off)
        p1 = add(add(S, u, L * (0.55 + 0.1 * k)), n, ws * off * 0.6 + 12)
        p2 = add(add(S, u, L * 0.9), n, we * off)
        folds += f"M{f(p0[0])},{f(p0[1])} Q{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} "
    s += f'<path d="{folds}" stroke="#b9ab94" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    # cuff
    s += f'<ellipse cx="{f(W[0])}" cy="{f(W[1])}" rx="{f(we/2+4)}" ry="{f(we/4)}" transform="rotate({f(ang(n))} {f(W[0])} {f(W[1])})" fill="#efe7d8" stroke="#3a2a1a" stroke-width="3"/>'
    return s, u

def forearm(W, Hp, w=40):
    u = norm((Hp[0] - W[0], Hp[1] - W[1])); n = (-u[1], u[0])
    p = [add(W, n, w / 2), add(Hp, n, w * 0.42), add(Hp, n, -w * 0.42), add(W, n, -w / 2)]
    return f'<path d="M{pts(p).replace(" ", " L")}Z" fill="#a8744e" stroke="#4a2a14" stroke-width="2.5"/>'

def hand_back(P, d):
    a = ang(d)
    return (f'<g transform="translate({f(P[0])},{f(P[1])}) rotate({f(a)})">'
            f'<ellipse cx="0" cy="-20" rx="36" ry="24" fill="#a8744e" stroke="#4a2a14" stroke-width="2.5"/>'
            f'<path d="M-24,-30 Q0,-40 24,-30" stroke="#c99068" stroke-width="3" fill="none"/></g>')

def hand_front(P, d):
    a = ang(d)
    s = f'<g transform="translate({f(P[0])},{f(P[1])}) rotate({f(a)})">'
    for i in range(4):
        x = (i - 1.5) * 15.5
        s += f'<rect x="{f(x-7.5)}" y="-10" width="15" height="{34 - abs(i-1.5)*3:.0f}" rx="7.5" fill="#b07c55" stroke="#4a2a14" stroke-width="2.2"/>'
        s += f'<path d="M{f(x-4)},{12 - abs(i-1.5)*2:.0f} q4,3 8,0" stroke="#6e4529" stroke-width="1.6" fill="none"/>'
    s += '<rect x="-46" y="-6" width="26" height="14" rx="7" transform="rotate(-25 -33 1)" fill="#b07c55" stroke="#4a2a14" stroke-width="2.2"/>'
    return s + "</g>"

def handle(p0, p1, w=22):
    return (f'<path d="M{f(p0[0])},{f(p0[1])} L{f(p1[0])},{f(p1[1])}" stroke="#2a170b" stroke-width="{w+5}" stroke-linecap="round"/>'
            f'<path d="M{f(p0[0])},{f(p0[1])} L{f(p1[0])},{f(p1[1])}" stroke="#80512a" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{f(p0[0]+5)},{f(p0[1])} L{f(p1[0]+5)},{f(p1[1])}" stroke="#b07a44" stroke-width="5" stroke-linecap="round" opacity="0.8"/>'
            f'<path d="M{f(p0[0]-4)},{f(p0[1]+2)} L{f(p1[0]-4)},{f(p1[1]+2)}" stroke="#4e2e16" stroke-width="2" stroke-dasharray="40 26" opacity="0.6"/>')

def pick_head(H, d, n):
    up, lo = [], []
    for k in range(-15, 12):
        s = k * 10.0
        c = add(H, n, s)
        c = add(c, d, 38 * (abs(s) / 150) ** 2)
        if s < 0:
            t = 30 * (1 - (abs(s) / 150) ** 1.4) + 2
        else:
            t = 30 + (s / 110) * 14
        up.append(add(c, d, -t / 2)); lo.append(add(c, d, t / 2))
    outline = up + lo[::-1]
    s = f'<path d="M{pts(outline).replace(" ", " L")}Z" fill="url(#s3-metal)" stroke="#1f2124" stroke-width="3" stroke-linejoin="round"/>'
    hl = [add(p, d, 5) for p in up[2:-2]]
    s += f'<path d="{smooth_path(hl, closed=False)}" stroke="#d6dde3" stroke-width="3" fill="none" opacity="0.8"/>'
    # socket
    s += f'<rect x="{f(H[0]-22)}" y="{f(H[1]-26)}" width="44" height="52" rx="8" transform="rotate({f(ang(d))} {f(H[0])} {f(H[1])})" fill="#55595e" stroke="#1f2124" stroke-width="3"/>'
    tip = outline[0]
    return s, tip

def hoe_head(E, d, n):
    p = [add(E, n, -46), add(E, n, 46), add(add(E, n, 78), d, 100), add(add(E, n, -78), d, 100)]
    s = f'<path d="M{pts(p).replace(" ", " L")}Z" fill="url(#s3-metal)" stroke="#1f2124" stroke-width="3" stroke-linejoin="round"/>'
    e1, e2 = add(add(E, n, 74), d, 92), add(add(E, n, -74), d, 92)
    s += f'<path d="M{f(e1[0])},{f(e1[1])} L{f(e2[0])},{f(e2[1])}" stroke="#e2e8ec" stroke-width="4"/>'
    s += f'<rect x="{f(E[0]-20)}" y="{f(E[1]-30)}" width="40" height="48" rx="7" transform="rotate({f(ang(d))} {f(E[0])} {f(E[1])})" fill="#55595e" stroke="#1f2124" stroke-width="3"/>'
    return s, add(E, d, 100)

# ---------- Arm A: pickaxe ----------
hA0, H = (830, 580), (455, 1240)
dA = norm((H[0] - hA0[0], H[1] - hA0[1])); nA = (-dA[1], dA[0])
if nA[0] < 0: nA = (-nA[0], -nA[1])
HA1 = add(hA0, dA, 260); HA2 = add(hA0, dA, 470)
headA, TIP_A = pick_head(H, dA, nA)
armA = ""
for S, Hp, wsz in (((1140, -50), HA1, 150), ((920, -70), HA2, 135)):
    u = norm((Hp[0] - S[0], Hp[1] - S[1]))
    W = add(Hp, u, -110)
    sl, _ = sleeve(S, W, wsz, 78, "s3-sleeve")
    armA += sl + forearm(add(W, u, -10), Hp, 46)
armA_parts = hand_back(HA1, dA) + hand_back(HA2, dA) + handle(hA0, H) + headA + hand_front(HA1, dA) + hand_front(HA2, dA)
# sleeves drawn first, then forearms over the cuff opening
armA_svg = f'<g id="s3-armA">{armA}{armA_parts}</g>'

# ---------- Arm B: hoe (مسحاة) ----------
hB0, E = (60, 1060), (400, 1560)
dB = norm((E[0] - hB0[0], E[1] - hB0[1])); nB = (-dB[1], dB[0])
HB1 = add(hB0, dB, 180); HB2 = add(hB0, dB, 340)
headB, EDGE_B = hoe_head(E, dB, nB)
armB = ""
for S, Hp, wsz in (((-160, 860), HB1, 180), ((-170, 1180), HB2, 170)):
    u = norm((Hp[0] - S[0], Hp[1] - S[1]))
    W = add(Hp, u, -110)
    sl, _ = sleeve(S, W, wsz, 76, "s3-sleeve2")
    armB += sl + forearm(add(W, u, -10), Hp, 44)
armB_svg = f'<g id="s3-armB">{armB}{hand_back(HB1, dB)}{hand_back(HB2, dB)}{handle(hB0, E)}{headB}{hand_front(HB1, dB)}{hand_front(HB2, dB)}</g>'

# ---------- ground ----------
ground = '<rect width="1080" height="1920" fill="url(#s3-ground)"/>'
# trench walls
ground += '<path d="M0,0 L120,0 C150,500 110,1200 160,1920 L0,1920Z" fill="url(#s3-wallL)" stroke="#3a2010" stroke-width="3"/>'
ground += '<path d="M1080,0 L960,0 C930,600 990,1300 950,1920 L1080,1920Z" fill="url(#s3-wallR)" stroke="#3a2010" stroke-width="3"/>'
strata = ""
for k in range(12):
    y = 60 + k * 160 + rnd.uniform(-30, 30)
    strata += f"M0,{f(y)} C40,{f(y+10)} 90,{f(y-6)} {f(125+rnd.uniform(0,20))},{f(y+8)} "
    strata += f"M1080,{f(y+40)} C1040,{f(y+50)} 1000,{f(y+30)} {f(960+rnd.uniform(-10,10))},{f(y+44)} "
ground += f'<path d="{strata}" stroke="#4a2614" stroke-width="3" fill="none" opacity="0.6"/>'
ground += '<path d="M120,0 C150,500 110,1200 160,1920 M960,0 C930,600 990,1300 950,1920" stroke="#e0a56a" stroke-width="4" fill="none" opacity="0.7"/>'
# static cracks
cr = ""
for i in range(34):
    x, y = rnd.uniform(160, 940), rnd.uniform(0, 1920)
    p = [(x, y)]
    for j in range(rnd.randint(3, 7)):
        x += rnd.uniform(-40, 40); y += rnd.uniform(-40, 40); p.append((x, y))
    cr += "M" + " L".join(f"{f(a)},{f(b)}" for a, b in p) + " "
ground += f'<path d="{cr}" stroke="#3e200e" stroke-width="2.5" fill="none" opacity="0.65" stroke-linejoin="round"/>'
# stones
for i in range(70):
    x, y = rnd.uniform(140, 960), rnd.uniform(-20, 1950)
    if math.hypot(x - TIP_A[0], y - TIP_A[1]) < 140: continue
    r = rnd.uniform(8, 40) if rnd.random() < 0.85 else rnd.uniform(45, 70)
    ground += stone(x, y, r, rnd, grad_id="s3-stone")
# pebbles
peb = ""
for i in range(260):
    x, y = rnd.uniform(130, 970), rnd.uniform(0, 1920)
    peb += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(1.2,3.6))}" fill="{rnd.choice(["#c08a5a","#5e3620","#a8744a"])}"/>'
ground += peb

# wet soil + stream + splash (water born at the pickaxe tip)
tx, ty = TIP_A
stream = f"M{f(tx)},{f(ty)} C{f(tx+40)},{f(ty+140)} {f(tx-60)},{f(ty+260)} {f(tx+30)},{f(ty+400)} C{f(tx+120)},{f(ty+520)} {f(tx+300)},{f(ty+560)} {f(tx+320)},{f(ty+800)}"
water = f'<path id="s3-wet" d="{stream}" opacity="0" pathLength="1" stroke="#4a2814" stroke-width="150" stroke-linecap="round" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s3-edge" d="{stream}" opacity="0" pathLength="1" stroke="#16587a" stroke-width="82" stroke-linecap="round" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s3-stream" d="{stream}" opacity="0" pathLength="1" stroke="#2B8CBE" stroke-width="70" stroke-linecap="round" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s3-stream2" d="{stream}" opacity="0" pathLength="1" stroke="#4fb3d9" stroke-width="40" stroke-linecap="round" fill="none" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
water += f'<path id="s3-shine" d="{stream}" stroke="#bff3fb" stroke-width="5" stroke-linecap="round" fill="none" stroke-dasharray="120 50 30 160 60 90" opacity="0" transform="translate(-10,0)"/>'
water += f'<path id="s3-shine2" d="{stream}" stroke="#e8fcff" stroke-width="3" stroke-linecap="round" fill="none" stroke-dasharray="30 80 50 40" opacity="0" transform="translate(12,4)"/>'
water += f'<ellipse id="s3-pool" cx="{f(tx)}" cy="{f(ty)}" rx="70" ry="48" fill="#2B8CBE" stroke="#16587a" stroke-width="3"/>'
spl = ""
for k in range(11):
    a = math.radians(k * 360 / 11 + rnd.uniform(-10, 10))
    L = rnd.uniform(70, 130)
    w = rnd.uniform(10, 18)
    tip = (math.cos(a) * L, math.sin(a) * L * 0.8 - 30)
    nx, ny = -math.sin(a), math.cos(a)
    spl += f'<path d="M{f(nx*w)},{f(ny*w)} Q{f(tip[0]*0.6+nx*w*0.6)},{f(tip[1]*0.6+ny*w*0.6)} {f(tip[0])},{f(tip[1])} Q{f(tip[0]*0.6-nx*w*0.6)},{f(tip[1]*0.6-ny*w*0.6)} {f(-nx*w)},{f(-ny*w)}Z" fill="{rnd.choice(["#4fb3d9","#7fd3ec","#2B8CBE"])}" stroke="#16587a" stroke-width="2"/>'
    spl += f'<circle cx="{f(tip[0]*1.15)}" cy="{f(tip[1]*1.15)}" r="{f(w*0.45)}" fill="#bff3fb"/>'
water += f'<g transform="translate({f(tx)},{f(ty)})"><g id="s3-splash">{spl}</g></g>'

# cracks spreading from the pickaxe tip, one set per strike
dyn = ""
for g in range(3):
    paths = ""
    for b in range(3):
        a = rnd.uniform(0, 6.28)
        x, y = tx, ty
        p = [(x, y)]
        for j in range(6):
            a += rnd.uniform(-0.6, 0.6)
            step = rnd.uniform(18, 34) * (1 + g * 0.5)
            x += math.cos(a) * step; y += math.sin(a) * step; p.append((x, y))
        paths += f'<path class="s3-ck{g}" d="M{pts(p).replace(" ", " L")}" pathLength="1" stroke="#2a1408" stroke-width="{5-g}" fill="none" stroke-linecap="butt" stroke-dasharray="1 1" stroke-dashoffset="1"/>'
    dyn += paths
# gouges under the hoe
ex, ey = EDGE_B
gouge = ""
for g in range(3):
    gouge += f'<path id="s3-gg{g}" d="M{f(ex-70+g*8)},{f(ey+10+g*16)} Q{f(ex)},{f(ey+34+g*16)} {f(ex+70-g*6)},{f(ey+4+g*16)}" stroke="#3a1c0c" stroke-width="{9-g*2}" fill="none" stroke-linecap="round" opacity="0"/>'

defs = """
<linearGradient id="s3-ground" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#b47a4c"/><stop offset="0.5" stop-color="#8C5A3C"/><stop offset="1" stop-color="#6a3e24"/></linearGradient>
<linearGradient id="s3-wallL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5e341b"/><stop offset="1" stop-color="#8c552f"/></linearGradient>
<linearGradient id="s3-wallR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#9c6438"/><stop offset="1" stop-color="#c2864f"/></linearGradient>
<radialGradient id="s3-stone" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#d4a476"/><stop offset="0.6" stop-color="#9c6a44"/><stop offset="1" stop-color="#6a4128"/></radialGradient>
<linearGradient id="s3-metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a9b0b6"/><stop offset="0.5" stop-color="#6b7178"/><stop offset="1" stop-color="#3c4045"/></linearGradient>
<linearGradient id="s3-sleeve" x1="1" y1="0" x2="0" y2="0.3"><stop offset="0" stop-color="#fffaf0"/><stop offset="0.6" stop-color="#ece3d3"/><stop offset="1" stop-color="#bfb19a"/></linearGradient>
<linearGradient id="s3-sleeve2" x1="0" y1="0" x2="1" y2="0.6"><stop offset="0" stop-color="#c9bba4"/><stop offset="0.5" stop-color="#efe7d8"/><stop offset="1" stop-color="#fffaf0"/></linearGradient>
<radialGradient id="s3-sun" cx="0.1" cy="0" r="1.2"><stop offset="0" stop-color="#ffd68a" stop-opacity="0.55"/><stop offset="0.6" stop-color="#E6A145" stop-opacity="0.12"/><stop offset="1" stop-color="#E6A145" stop-opacity="0"/></radialGradient>
"""

svg = f"""
<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0">
  <defs>{defs}</defs>
  {ground}
  {dyn}
  {gouge}
  {water}
  {armB_svg}
  {armA_svg}
  <rect width="1080" height="1920" fill="url(#s3-sun)"/>
</svg>
"""

body = f"""
    <div id="s3-wrap" class="clip" data-start="0" data-duration="{DUR}" data-layout-allow-overflow style="position:absolute;inset:0;overflow:hidden">
      <div id="s3-cam" style="position:absolute;inset:0">
        {svg}
        <canvas id="s3-fx" width="1080" height="1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px"></canvas>
      </div>
      <div id="s3-gold" style="position:absolute;inset:0;background:radial-gradient(70% 55% at 50% 50%, #fff3cf 0%, #ffd27a 55%, #f2a948 100%)"></div>
      <div id="s3-t" class="hd" style="top:210px;left:30px;right:470px;font-size:90px;color:#fff3dc;text-shadow:0 5px 22px rgba(30,12,4,.75)"><span class="w">بيديه..</span> <br><span class="w">مع</span> <span class="w">الأهالي</span></div>
    </div>
"""

script = RNG_JS + f"""
    const tl = gsap.timeline({{ paused: true }});
    const D = {DUR};
    const A = {A_TIMES}, B = {B_TIMES};
    const TA = [{f(TIP_A[0])}, {f(TIP_A[1])}], TB = [{f(EDGE_B[0])}, {f(EDGE_B[1])}];
    // gold from the previous shot burns off
    tl.fromTo("#s3-gold", {{ opacity: 0.96 }}, {{ opacity: 0, duration: 0.55, ease: "power2.out" }}, 0);
    tl.fromTo("#s3-cam", {{ scale: 1.06, x: 0, y: 0, transformOrigin: "330px 1250px" }}, {{ scale: 1.0, duration: 1.2, ease: "power2.out" }}, 0);
    // pickaxe: wind-up, strike, recoil
    tl.fromTo("#s3-armA", {{ rotation: -16, scale: 1.05, svgOrigin: "1000 -150" }}, {{ rotation: -16, scale: 1.05, duration: 0.01 }}, 0);
    A.forEach((t, i) => {{
      tl.to("#s3-armA", {{ rotation: 0, scale: 1, duration: 0.15, ease: "power3.in" }}, t - 0.15);
      tl.to("#s3-armA", {{ rotation: -2.5, duration: 0.14, ease: "power2.out" }}, t);
      if (i < A.length - 1) tl.to("#s3-armA", {{ rotation: -16, scale: 1.05, duration: 0.55, ease: "power2.inOut" }}, t + 0.3);
    }});
    tl.to("#s3-armA", {{ rotation: -24, scale: 1.08, duration: 0.9, ease: "power2.inOut" }}, 4.9);
    // hoe: offset rhythm
    tl.fromTo("#s3-armB", {{ rotation: 13, scale: 1.04, svgOrigin: "-250 700" }}, {{ rotation: 13, scale: 1.04, duration: 0.01 }}, 0);
    B.forEach((t, i) => {{
      tl.to("#s3-armB", {{ rotation: 0, scale: 1, duration: 0.15, ease: "power3.in" }}, t - 0.15);
      tl.to("#s3-armB", {{ rotation: 2, duration: 0.14, ease: "power2.out" }}, t);
      if (i < B.length - 1) tl.to("#s3-armB", {{ rotation: 13, scale: 1.04, duration: 0.55, ease: "power2.inOut" }}, t + 0.3);
      tl.to("#s3-gg" + i, {{ opacity: 0.85, duration: 0.05 }}, t);
    }});
    tl.to("#s3-armB", {{ rotation: 20, scale: 1.06, duration: 1.0, ease: "power2.inOut" }}, 4.6);
    // cracks open with each pickaxe strike
    [0, 1, 2].forEach(g => tl.to(".s3-ck" + g, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.14, ease: "power2.out" }}, A[g]));
    // camera shake on every hit (bigger on the last)
    [...A, ...B].forEach(t => {{
      const k = t === 4.4 ? 2.2 : 1;
      tl.to("#s3-cam", {{ x: 9 * k, y: -7 * k, duration: 0.035, ease: "none" }}, t);
      tl.to("#s3-cam", {{ x: -7 * k, y: 6 * k, duration: 0.05, ease: "none" }}, t + 0.035);
      tl.to("#s3-cam", {{ x: 3 * k, y: -2 * k, duration: 0.05, ease: "none" }}, t + 0.085);
      tl.to("#s3-cam", {{ x: 0, y: 0, duration: 0.07, ease: "power1.out" }}, t + 0.135);
    }});
    // water bursts out and runs
    tl.fromTo("#s3-pool", {{ scale: 0, svgOrigin: TA[0] + " " + TA[1] }}, {{ scale: 1.6, duration: 0.6, ease: "expo.out" }}, 4.42);
    tl.fromTo("#s3-splash", {{ scale: 0, opacity: 1, svgOrigin: "0 0" }}, {{ scale: 1.25, duration: 0.35, ease: "expo.out" }}, 4.42);
    tl.to("#s3-splash", {{ scale: 0.75, opacity: 0.85, duration: 1.2, ease: "power2.inOut" }}, 4.8);
    tl.fromTo("#s3-wet", {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.2 }}, 4.6);
    tl.to("#s3-wet", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 2.0, ease: "power1.inOut" }}, 4.62);

    tl.fromTo("#s3-edge", {{ opacity: 0, attr: {{ "stroke-dashoffset": 1, "stroke-width": 26 }} }}, {{ opacity: 1, attr: {{ "stroke-dashoffset": 0, "stroke-width": 104 }}, duration: 2.0, ease: "power1.inOut" }}, 4.55);
    tl.fromTo("#s3-shine2", {{ opacity: 0, attr: {{ "stroke-dashoffset": 0 }} }}, {{ opacity: 0.8, attr: {{ "stroke-dashoffset": -340 }}, duration: 2.5, ease: "none" }}, 4.7);
    tl.fromTo("#s3-stream", {{ opacity: 0, attr: {{ "stroke-dashoffset": 1, "stroke-width": 18 }} }}, {{ opacity: 1, attr: {{ "stroke-dashoffset": 0, "stroke-width": 92 }}, duration: 2.0, ease: "power1.inOut" }}, 4.55);
    tl.fromTo("#s3-stream2", {{ opacity: 0, attr: {{ "stroke-dashoffset": 1, "stroke-width": 8 }} }}, {{ opacity: 1, attr: {{ "stroke-dashoffset": 0, "stroke-width": 50 }}, duration: 2.0, ease: "power1.inOut" }}, 4.62);
    tl.fromTo("#s3-shine", {{ opacity: 0, attr: {{ "stroke-dashoffset": 0 }} }}, {{ opacity: 0.9, attr: {{ "stroke-dashoffset": -260 }}, duration: 2.5, ease: "none" }}, 4.5);
    tl.to("#s3-cam", {{ scale: 1.12, duration: 2.2, ease: "power1.inOut" }}, 4.45);
    // vertical whip into the next shot
    tl.to("#s3-cam", {{ y: 760, filter: "blur(14px)", duration: 0.35, ease: "power3.in" }}, 6.65);
    // title
    tl.fromTo("#s3-t .w", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, stagger: 0.1, ease: "power3.out" }}, 0.5);
    tl.to("#s3-t", {{ opacity: 0, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, 4.1);

    // dust, chips and water drops
    const cv = document.getElementById("s3-fx"), ctx = cv.getContext("2d");
    const R = rng(33), P = [];
    function burst(t0, x, y, n, kind) {{
      for (let i = 0; i < n; i++) {{
        const a = R() * Math.PI * 2, sp = (kind === "w" ? 250 : 120) + R() * (kind === "w" ? 650 : 420);
        P.push({{ t0: t0 + R() * (kind === "w" ? 2.4 : 0.05), x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp * 0.7 - (kind === "w" ? 260 : 120),
                 life: (kind === "w" ? 0.45 : 0.5) + R() * 0.6, r: kind === "c" ? 2 + R() * 4 : (kind === "w" ? 2 + R() * 5 : 3 + R() * 9), kind }});
      }}
    }}
    A.forEach(t => {{ burst(t, TA[0], TA[1], 34, "d"); burst(t, TA[0], TA[1], 16, "c"); }});
    B.forEach(t => {{ burst(t, TB[0], TB[1], 30, "d"); burst(t, TB[0], TB[1], 12, "c"); }});
    burst(4.42, TA[0], TA[1], 220, "w");
    function draw(t) {{
      ctx.clearRect(0, 0, 1080, 1920);
      for (const p of P) {{
        const u = t - p.t0;
        if (u < 0 || u > p.life) continue;
        const k = u / p.life;
        const drag = p.kind === "d" ? 0.55 : 1;
        const x = p.x + p.vx * u * drag, y = p.y + p.vy * u * drag + (p.kind === "d" ? 60 : 900) * u * u;
        if (p.kind === "d") {{ ctx.globalAlpha = 0.5 * (1 - k); ctx.fillStyle = "#d9a874"; ctx.beginPath(); ctx.arc(x, y, p.r * (1 + 2.2 * k), 0, 6.283); ctx.fill(); }}
        else if (p.kind === "c") {{ ctx.globalAlpha = 1 - k * k; ctx.fillStyle = "#4e2a14"; ctx.fillRect(x - p.r / 2, y - p.r / 2, p.r, p.r); }}
        else {{ ctx.globalAlpha = 0.95 * (1 - k); ctx.fillStyle = (p.r > 4.5) ? "#4fb3d9" : "#c9f6ff"; ctx.beginPath(); ctx.ellipse(x, y, p.r, p.r * 1.4, 0, 0, 6.283); ctx.fill(); }}
      }}
      ctx.globalAlpha = 1;
    }}
    const clock = {{ t: 0 }};
    tl.fromTo(clock, {{ t: 0 }}, {{ t: D, duration: D, ease: "none", onUpdate: () => draw(clock.t) }}, 0);
    draw(0);
"""

open(OUT + "s3.html", "w").write(scene("s3", DUR, defs, body, script))
print("s3 ok", len(open(OUT + "s3.html").read()), "tipA", TIP_A, "edgeB", EDGE_B)
