import math, random

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "compositions") + "/"

def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)

def pts(points):
    return " ".join(f"{f(x)},{f(y)}" for x, y in points)

def smooth_path(points, closed=True):
    """Catmull-Rom-ish smooth path through points using quadratic midpoints."""
    n = len(points)
    if closed:
        mids = [((points[i][0] + points[(i + 1) % n][0]) / 2, (points[i][1] + points[(i + 1) % n][1]) / 2) for i in range(n)]
        d = f"M{f(mids[-1][0])},{f(mids[-1][1])}"
        for i in range(n):
            d += f" Q{f(points[i][0])},{f(points[i][1])} {f(mids[i][0])},{f(mids[i][1])}"
        return d + "Z"
    d = f"M{f(points[0][0])},{f(points[0][1])}"
    for i in range(1, n - 1):
        mx, my = (points[i][0] + points[i + 1][0]) / 2, (points[i][1] + points[i + 1][1]) / 2
        d += f" Q{f(points[i][0])},{f(points[i][1])} {f(mx)},{f(my)}"
    d += f" L{f(points[-1][0])},{f(points[-1][1])}"
    return d

def quad(p0, p1, p2, t):
    a = (1 - t) ** 2; b = 2 * (1 - t) * t; c = t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])

def frond(angle, length, droop, width, fill, stroke, sw=1.4, opacity=1.0):
    """Date palm frond: a rib with zig-zag leaflets on both sides. Origin = crown."""
    a = math.radians(angle)
    d = (math.cos(a), math.sin(a))
    p0 = (0.0, 0.0)
    p1 = (d[0] * length * 0.5, d[1] * length * 0.5 - length * 0.12)
    p2 = (d[0] * length, d[1] * length + droop * length)
    N = 14
    up, lo = [], []
    for i in range(1, N):
        t = i / N
        p = quad(p0, p1, p2, t)
        q = quad(p0, p1, p2, min(1, t + 0.02))
        tx, ty = q[0] - p[0], q[1] - p[1]
        L = math.hypot(tx, ty) or 1
        tx, ty = tx / L, ty / L
        nx, ny = -ty, tx
        w = width * (math.sin(math.pi * t) ** 0.6) * (1.05 - 0.45 * t)
        # leaflet tip (angled toward the frond tip) and notch
        up.append((p[0] + nx * w + tx * w * 0.55, p[1] + ny * w + ty * w * 0.55))
        up.append((p[0] + nx * w * 0.18 + tx * 3, p[1] + ny * w * 0.18 + ty * 3))
        lo.append((p[0] - nx * w + tx * w * 0.55, p[1] - ny * w + ty * w * 0.55))
        lo.append((p[0] - nx * w * 0.18 + tx * 3, p[1] - ny * w * 0.18 + ty * 3))
    outline = [p0] + up + [p2] + lo[::-1]
    rib = f"M0,0 Q{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])}"
    op = f' opacity="{opacity}"' if opacity < 1 else ""
    return (f'<path d="M{pts(outline).replace(" ", " L")}Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{op}/>'
            f'<path d="{rib}" fill="none" stroke="{stroke}" stroke-width="{sw*1.3:.1f}" stroke-linecap="round"{op}/>')

def palm(h, lean=0.0, dry=False, lit=1.0, seed=1, dates=False, outline="#2f2414", sw=1.6, fronds_scale=1.0):
    """Date palm with base at origin, height h (to crown)."""
    rnd = random.Random(seed)
    top = (lean * h, -h)
    ctrl = (lean * h * 0.2 + h * 0.04 * rnd.uniform(-1, 1), -h * 0.55)
    wb, wt = h * 0.055, h * 0.032
    left, right = [], []
    N = 12
    for i in range(N + 1):
        t = i / N
        p = quad((0, 0), ctrl, top, t)
        w = wb + (wt - wb) * t
        left.append((p[0] - w, p[1])); right.append((p[0] + w, p[1]))
    trunk_c = "#7a5532" if not dry else "#8a6a45"
    trunk_s = "#5a3b20" if not dry else "#6b5034"
    s = f'<path d="M{pts(left + right[::-1]).replace(" ", " L")}Z" fill="{trunk_c}" stroke="{outline}" stroke-width="{sw}"/>'
    # lit side
    s += f'<path d="{smooth_path(right, closed=False)}" fill="none" stroke="#c99a5e" stroke-width="{max(1.5, wb*0.35):.1f}" opacity="{0.55*lit:.2f}"/>'
    # bark rings
    rings = ""
    for i in range(1, 15):
        t = i / 15
        p = quad((0, 0), ctrl, top, t)
        w = wb + (wt - wb) * t
        rings += f"M{f(p[0]-w*0.9)},{f(p[1]+w*0.3)} L{f(p[0]+w*0.9)},{f(p[1]-w*0.25)} "
    s += f'<path d="{rings}" stroke="{trunk_s}" stroke-width="{max(1, h*0.008):.1f}" fill="none"/>'
    if dry:
        back, mid, front = "#7d7a3a", "#9c9547", "#b5a95a"
        dead = "#8a6a3a"
    else:
        back, mid, front = "#2f5e3a", "#3B7A57", "#74A12E"
        dead = None
    L = h * 0.62 * fronds_scale
    W = h * 0.085 * fronds_scale
    g = f'<g transform="translate({f(top[0])},{f(top[1])})">'
    if dry:
        for ang in (100, 75, 115):
            g += frond(ang, L * 0.7, 0.15, W * 0.6, dead, outline, sw * 0.8)
    back_angles = [-175, -150, -118, -62, -30, -5]
    for k, ang in enumerate(back_angles):
        dr = 0.55 if dry else 0.35
        g += frond(ang + rnd.uniform(-6, 6), L * rnd.uniform(0.9, 1.05), dr * (1 if abs(ang + 90) > 40 else 0.3), W, back, outline, sw * 0.8)
    if dates:
        for k in range(-1, 2, 2):
            for j in range(5):
                cx = k * h * 0.06 + rnd.uniform(-6, 6) * h / 300
                cy = h * 0.06 + j * h * 0.012
                g += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(h*0.018)}" fill="#c4702b" stroke="{outline}" stroke-width="0.8"/>'
    front_angles = [-165, -138, -100, -80, -42, -15, 160, 20]
    for k, ang in enumerate(front_angles):
        dr = 0.5 if dry else 0.3
        if ang in (160, 20):
            dr = 0.55
        col = mid if k % 2 else front
        if dry and k % 3 == 0:
            col = dead
        g += frond(ang + rnd.uniform(-5, 5), L * rnd.uniform(0.85, 1.0), dr * (1 if abs(ang + 90) > 30 else 0.2), W * 0.95, col, outline, sw * 0.8)
    g += "</g>"
    return s + g

def stone(cx, cy, r, rnd, light="#b98a5e", dark="#6d4529", outline="#3a2414", grad_id="stoneg", shadow=True):
    k = rnd.randint(7, 10)
    ang0 = rnd.uniform(0, 6.28)
    p = []
    for i in range(k):
        a = ang0 + i * 2 * math.pi / k
        rr = r * rnd.uniform(0.78, 1.1)
        p.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.72))
    d = smooth_path(p)
    s = ""
    if shadow:
        sp = [(x + r * 0.18, y + r * 0.22) for x, y in p]
        s += f'<path d="{smooth_path(sp)}" fill="#2a170b" opacity="0.35"/>'
    s += f'<path d="{d}" fill="url(#{grad_id})" stroke="{outline}" stroke-width="{max(1.2, r*0.06):.1f}"/>'
    # highlight
    hp = [(cx - r * 0.35 + math.cos(a) * r * 0.28, cy - r * 0.3 + math.sin(a) * r * 0.16) for a in [i * 2 * math.pi / 6 for i in range(6)]]
    s += f'<path d="{smooth_path(hp)}" fill="#e2b98a" opacity="0.45"/>'
    return s

def person_back(fill="#2b1a10", rim=None, s=1.0, variant=0, kandura=None, ghutra=None, agal="#141010", outline="#2f2414", bisht=None):
    """Back view figure, feet at origin, height ~400*s. No face: only the back of the ghutra."""
    def P(x, y):
        return f"{f(x*s)},{f(y*s)}"
    body = (f"M{P(-55,-300)} C{P(-70,-200)} {P(-74,-100)} {P(-64,0)} L{P(64,0)} "
            f"C{P(74,-100)} {P(70,-200)} {P(55,-300)} Q{P(0,-318)} {P(-55,-300)}Z")
    head = (f"M{P(-31,-352)} C{P(-31,-392)} {P(31,-392)} {P(31,-352)} C{P(36,-330)} {P(52,-312)} {P(64,-296)} "
            f"C{P(34,-280)} {P(12,-268)} {P(0,-258)} C{P(-12,-268)} {P(-34,-280)} {P(-64,-296)} C{P(-52,-312)} {P(-36,-330)} {P(-31,-352)}Z")
    if variant == 1:  # ghutra wrapped (worker style)
        head = (f"M{P(-30,-350)} C{P(-30,-392)} {P(30,-392)} {P(30,-350)} C{P(32,-332)} {P(30,-318)} {P(22,-308)} "
                f"L{P(-22,-308)} C{P(-30,-318)} {P(-32,-332)} {P(-30,-350)}Z")
    out = ""
    if kandura is None:  # silhouette
        out += f'<path d="{body}" fill="{fill}"/>'
        if bisht:
            cape = (f"M{P(-58,-302)} C{P(-90,-200)} {P(-100,-100)} {P(-96,-20)} Q{P(0,-6)} {P(96,-20)} "
                    f"C{P(100,-100)} {P(90,-200)} {P(58,-302)} Q{P(0,-322)} {P(-58,-302)}Z")
            out += f'<path d="{cape}" fill="{fill}"/>'
        out += f'<path d="{head}" fill="{fill}"/>'
        agal_s = f"M{P(-35,-366)} Q{P(0,-352)} {P(35,-366)} L{P(35,-350)} Q{P(0,-336)} {P(-35,-350)}Z"
        out += f'<path d="{agal_s}" fill="{fill}"/>'
        if rim:
            out += f'<path d="M{P(-35,-366)} Q{P(0,-352)} {P(35,-366)}" fill="none" stroke="#ffd27a" stroke-width="{max(1.5,2.5*s):.1f}" opacity="0.9"/>' 
            out += f'<path d="{head}" fill="none" stroke="{rim}" stroke-width="{max(1.5,3*s):.1f}"/>'
            out += f'<path d="{body if not bisht else cape}" fill="none" stroke="{rim}" stroke-width="{max(1.5,3*s):.1f}"/>'
    else:
        out += f'<path d="{body}" fill="{kandura}" stroke="{outline}" stroke-width="{max(1,2*s):.1f}"/>'
        out += f'<path d="M{P(20,-290)} C{P(30,-200)} {P(34,-100)} {P(30,-5)}" stroke="#cdbfa8" stroke-width="{max(1,6*s):.1f}" fill="none"/>'
        out += f'<path d="{head}" fill="{ghutra}" stroke="{outline}" stroke-width="{max(1,2*s):.1f}"/>'
        out += f'<path d="M{P(-30,-362)} Q{P(0,-352)} {P(30,-362)}" stroke="{agal}" stroke-width="{max(1.5,6*s):.1f}" fill="none"/>'
        out += f'<path d="M{P(-31,-350)} Q{P(0,-340)} {P(31,-350)}" stroke="{agal}" stroke-width="{max(1.5,5*s):.1f}" fill="none"/>'
    return out

FONTS = """
    @font-face { font-family: "Amiri"; src: url("assets/fonts/Amiri-Bold.ttf"); font-weight: 700; }
    @font-face { font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }
"""

def scene(sid, dur, svg_defs, body_html, script, extra_css=""):
    return f"""<template>
  <style>{FONTS}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .hd {{ font-family: "Amiri", serif; font-weight: 700; direction: rtl; text-align: center; position: absolute; left: 80px; right: 80px; line-height: 1.2; }}
    .lb {{ font-family: "Noto Kufi Arabic", sans-serif; font-weight: 600; direction: rtl; text-align: center; position: absolute; line-height: 1.35; }}
    .w {{ display: inline-block; }}
{extra_css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{body_html}
  </div>
  <script>
{script}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

RNG_JS = """
    function rng(seed) { return function () { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
"""

def cub(p, t):
    a, b, c, d = p
    m = 1 - t
    return (m**3*a[0] + 3*m*m*t*b[0] + 3*m*t*t*c[0] + t**3*d[0], m**3*a[1] + 3*m*m*t*b[1] + 3*m*t*t*c[1] + t**3*d[1])
