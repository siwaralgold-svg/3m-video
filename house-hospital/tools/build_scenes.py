#!/usr/bin/env python3
"""Writes compositions/*.html and index.html for «البيت اللي صار مستشفى».

Each scene is timed against the recorded voice (assets/audio/voice.mp3).
Inside a scene, `at(a)` turns a voice time (seconds into voice.mp3) into scene time.
The voice starts at film time VO = 3.0 s, after the title.
Run:  python3 tools/build_scenes.py   (from the project folder)
"""
import json, os

VO = 3.0
# The scenes were first timed to an earlier take of the voice. The current take
# (assets/audio/voice.mp3, 140.04 s) has the same text and order with small timing
# shifts; tools/voice_warp.json maps earlier-take times to current-take times
# (word-level alignment of both transcripts). Every voice time written below is in
# the earlier take and passes through warp(), so actions stay on their words.
WARP = json.load(open(os.path.join(os.path.dirname(__file__), "voice_warp.json")))


def warp(a):
    if a <= WARP[0][0]:
        return a
    for (a0, b0), (a1, b1) in zip(WARP, WARP[1:]):
        if a <= a1:
            return b0 + (b1 - b0) * (a - a0) / (a1 - a0)
    return WARP[-1][1] + (a - WARP[-1][0])


def g(t):
    # film time (earlier take) -> film time (current take)
    return t if t <= VO else warp(t - VO) + VO


END_VOICE = 117.316 + VO
WARP_JS = json.dumps([[round(a, 3), round(b, 3)] for a, b in WARP])
OUT = os.path.join(os.path.dirname(__file__), "..")

SCENES = []


def scene(sid, start, dur, bg, els, js, overlay=""):
    if sid == "sc17":
        start = END_VOICE + 0.5
    else:
        start = g(start)
    SCENES.append(dict(id=sid, start=round(start, 3), dur=round(dur, 3), bg=bg, els=els, js=js, overlay=overlay))


def rig(name, z, cls="actor"):
    return f'<div id="{name}" class="{cls}" style="z-index:{z}"></div>'


def img(name, src, z, style=""):
    return f'<img id="{name}" class="prop" src="assets/{src}" style="z-index:{z};{style}">'


def sickle(name, z):
    # the palm-grower's sickle (das): wooden handle, curved steel blade. Grip at (80, 165).
    return (f'<svg id="{name}" width="160" height="200" viewBox="0 0 160 200" style="position:absolute;left:0;top:0;z-index:{z};overflow:visible;transform-origin:0 0">'
            '<path d="M73 124 C58 58, 104 6, 152 44 C120 30, 92 62, 89 124 Z" fill="#aab0b4" stroke="#5f666b" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M80 116 C73 72, 104 30, 138 39" fill="none" stroke="#dfe3e6" stroke-width="2.5" opacity=".75"/>'
            '<rect x="70" y="120" width="21" height="80" rx="8" fill="#8a5b34" stroke="#5c3a1f" stroke-width="3"/>'
            '<rect x="69" y="118" width="23" height="12" rx="3" fill="#6f4a2a"/></svg>')


def steth(name, z):
    # stethoscope drawn in the prop sheet's colours: cream ear tips, steel ear tubes and chest piece, black tubing
    return (f'<svg id="{name}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible;z-index:{z}">'
            f'<path id="{name}-m2" d="" fill="none" stroke="#8d949a" stroke-width="3.2" stroke-linecap="round"/>'
            f'<path id="{name}-m1" d="" fill="none" stroke="#b9c0c5" stroke-width="3.2" stroke-linecap="round"/>'
            f'<path id="{name}-t" d="" fill="none" stroke="#2b2929" stroke-width="5.5" stroke-linecap="round"/>'
            f'<circle id="{name}-e1" r="4.6" fill="#efe6d2" stroke="#b8ad95" stroke-width="1.2"/>'
            f'<circle id="{name}-e2" r="4.6" fill="#efe6d2" stroke="#b8ad95" stroke-width="1.2"/>'
            f'<circle id="{name}-b" r="10.5" fill="#c9cfd3" stroke="#6d7479" stroke-width="3"/>'
            f'<circle id="{name}-bi" r="4.5" fill="#e9edef"/></svg>')


def div(name, z, style="", inner=""):
    return f'<div id="{name}" style="position:absolute;z-index:{z};{style}">{inner}</div>'


# ------------------------------------------------------------------ sc01 title + courtyard
scene("sc01", 0, 12.74, "03_salem_home_courtyard",
      [rig("sc01-salem", 20)],
      r"""
const salem = Rig.make(q('sc01-salem'), 'salem_q34', {seed: 4});
const cam = Rig.camera(q('sc01-cam'));
const head = T([[0,0],[at(6.1),0],[at(7.0),9],[at(8.7),9],[at(9.2),-3],[at(9.8),0]]);
const lean = T([[0,0],[at(8.9),0],[at(9.4),-2.5],[at(10.5),0]]);
const arm = T([[0,0],[at(8.9),0],[at(9.3),-8],[at(10.4),0]]);
const cz = T([[0,1],[12.74,1.22,'lin']]), cx = T([[0,960],[12.74,1060,'lin']]), cy = T([[0,560],[12.74,640,'lin']]);
const tOp = T([[0,0],[0.5,0],[1.3,1],[2.6,1],[3.2,0]]);
const tY = T([[0,14],[1.3,0,'out']]);
const glow = T([[0,0.55],[4,0.15]]);
// the disclaimer sits at the foot of the frame while Salem starts talking
const dOp = T([[0,0],[3.2,0],[3.55,1],[8.0,1],[8.4,0]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: cx(t), cy: cy(t), z: cz(t)});
  salem.render({t, x: 1120, y: 905, h: 560, dir: 1, head: head(t), lean: lean(t), arm: [arm(t), 0]});
  q('sc01-title').style.opacity = tOp(t);
  q('sc01-title').style.transform = `translateY(${tY(t)}px)`;
  q('sc01-dawn').style.opacity = glow(t);
  q('sc01-disc').style.opacity = dOp(t);
});
""",
      overlay='<div id="sc01-dawn" class="grade" style="background:linear-gradient(180deg,rgba(255,196,120,.55),rgba(120,70,40,.25))"></div>'
              '<div id="sc01-title" class="title">البيت اللي صار مستشفى</div>'
              '<div id="sc01-disc" class="disc">قصة درامية مستوحاة من تأسيس مستشفى الواحة في العين عام ١٩٦٠.<br>سالم وعائلته شخصيات متخيّلة.</div>')

# ------------------------------------------------------------------ sc02 lane, Al Ain
scene("sc02", 12.74, 3.51, "02_neighborhood_lane",
      [rig("sc02-salem", 30), rig("sc02-woman", 12), rig("sc02-girl", 12), rig("sc02-old", 10), rig("sc02-basket", 9)],
      r"""
const salem = Rig.make(q('sc02-salem'), 'salem_side', {seed: 3});
const woman = Rig.figure(q('sc02-woman'), 'assets/chars/res_woman_stand.png', 528, 1304, {seed: 2});
const girl = Rig.figure(q('sc02-girl'), 'assets/chars/res_girl_stand.png', 512, 1204, {seed: 8});
const old = Rig.figure(q('sc02-old'), 'assets/chars/res_oldman_walk.png', 816, 1316, {seed: 5, amp: 0.3});
const bas = Rig.figure(q('sc02-basket'), 'assets/chars/res_basket_stand.png', 752, 1332, {seed: 6});
const cam = Rig.camera(q('sc02-cam'));
const sx = T([[0,1560],[DUR,860,'lin']]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 1000 - t*25, cy: 560, z: 1.08});
  salem.render({t, x: sx(t), x0: 1560, y: 1010, h: 640, dir: -1});
  woman.render({t, x: 470, y: 820, h: 330, dir: 1, rot: Rig.talk(t, 0.2, 3.4, 1.2, 1)});
  girl.render({t, x: 590, y: 828, h: 330, dir: -1});
  old.render({t, x: 1330, y: 735, h: 215, dir: -1});
  bas.render({t, x: 1580, y: 770, h: 260, dir: -1});
});
""")

# ------------------------------------------------------------------ sc03 palms, the morning ritual
PALM_FATHER = r"""
// The father trims the old frond stubs on the palm trunk with a sickle (das): reach up, hook, pull down.
const CYC = 1.15;                                   // one stroke
const FX = 1516, FY = 932, FH = 600;                // where he stands, facing the trunk
const HAND_HI = {x: FX + 130, y: FY - 462}, HAND_LO = {x: FX + 100, y: FY - 356};
const SICKLE = {grip: [80, 165], rot: 96, scale: 1.35};
function palmWork(fa, tStop) {
  const ph = 0.5 * CYC - (tStop % CYC);             // he ends hooked in, at the top of a stroke
  const stroke = (t) => { const c = ((t + ph) % CYC) / CYC;
    return c < 0.45 ? Rig.smooth(c / 0.45) : c < 0.56 ? 1 : c < 0.72 ? 1 - Math.pow((c - 0.56) / 0.16, 2) : 0; };
  const state = (t) => { const s = stroke(Math.min(t, tStop));
    const st = {t, x: FX, y: FY, h: FH, dir: 1, d: 0, settle: 1, idle: 0, lean: 1.5 + 3.5 * (1 - s), head: -11 + 7 * (1 - s)};
    st.arm = Rig.reach(fa, st, 0, Rig.lerp(HAND_LO.x, HAND_HI.x, s), Rig.lerp(HAND_LO.y, HAND_HI.y, s), 1);
    return st; };
  // times the blade bites: the pull's end
  const hits = []; for (let k = 1; tStop - (0.78 + k - 1) * CYC > 0.05; k++) hits.push(tStop - (0.78 + k - 1) * CYC);
  return {state, hits};
}
// dry fibre falling from the cut: 4 shreds per bite
function fibres(layer, hits, cut) {
  const els = []; hits.forEach(() => { for (let i = 0; i < 4; i++) { const e = document.createElement('div');
    Object.assign(e.style, {position: 'absolute', left: '0px', top: '0px', width: (10 + 5 * i) + 'px', height: '4px', borderRadius: '2px',
      background: i % 2 ? '#7a5a38' : '#a07c4f', opacity: 0}); layer.appendChild(e); els.push(e); } });
  return (t) => hits.forEach((h, n) => { for (let i = 0; i < 4; i++) { const e = els[n * 4 + i], a = t - h;
    if (a < 0 || a > 1.0) { e.style.opacity = 0; continue; }
    const r1 = ((n * 7 + i * 13) % 10) / 10, r2 = ((n * 3 + i * 5) % 7) / 7;
    const x = cut.x - 6 - (20 + 70 * r1) * a, y = Math.min(FY - 8, cut.y + 6 - 50 * r2 * a + 520 * a * a);
    e.style.opacity = a < 0.8 ? 1 : (1 - a) * 5;
    e.style.transform = `translate(${x}px, ${y}px) rotate(${(r1 - 0.5) * 700 * a + 40 * i}deg)`; } });
}
"""
scene("sc03", 16.25, 7.85, "05_palm_garden",
      [div("sc03-dust", 18, "left:0;top:0"), rig("sc03-father", 20), rig("sc03-fatherF", 20), sickle("sc03-sickle", 21),
       div("sc03-fib", 22, "left:0;top:0"), rig("sc03-salem", 25)],
      PALM_FATHER + r"""
const fa = Rig.make(q('sc03-father'), 'father_side', {seed: 2});
const faF = Rig.make(q('sc03-fatherF'), 'father_front', {seed: 2});
const sa = Rig.make(q('sc03-salem'), 'salem_side', {seed: 7});
const cam = Rig.camera(q('sc03-cam'));
// «ألقاه يشتغل ويقول لي»: he hooks the sickle into the trunk, lets go and turns to Salem
const tStop = at(17.95), tA = at(18.12), tB = at(18.3);
const PW = palmWork(fa, tStop);
fa.render(PW.state(tStop)); const CUTPT = (() => { const h = Rig.attach(q('sc03-sickle'), fa, 0, SICKLE); return {x: h.x + 34, y: h.y - 96}; })();
const fib = fibres(q('sc03-fib'), PW.hits, CUTPT);
const drop = T([[0,0],[tStop,0],[tStop + 0.28,1]]);
const head = T([[0,0],[tB,2],[at(18.8),-4],[at(19.2),2],[at(19.5),-4],[at(19.9),3],[at(20.3),-3],[at(20.9),0]]);
const lean = T([[0,0],[tB,-1],[at(18.9),-3],[at(20.9),-1]]);
// «الشمس سبقتك»: he points up at the sun
const pt = T([[0,0],[at(19.2),0],[at(19.7),1,'out'],[at(20.55),1],[at(21.0),0]]);
const sx = T([[0,-160],[at(15.4),-160],[at(18.15),880,'out']]);
const sset = T([[0,0],[at(18.05),0],[at(18.5),1]]);
const sHead = T([[0,0],[at(18.3),0],[at(18.8),-9],[at(21),-7]]);
const pant = (t) => t > at(18.4) ? 2.2 * Math.sin((t - at(18.4)) * 8.5) * Math.exp(-(t - at(18.4)) * 0.9) : 0;
const falls = Rig.footfalls(sa, {x: sx, x0: -160, h: 600, run: 1, dir: 1, t0: at(15.4), t1: at(18.1), y: 962});
const dust = Rig.dust(q('sc03-dust'), falls, {drift: 26});
const cut = at(18.6);
Rig.drive(tl, DUR, (t) => {
  if (t < cut) cam.render({cx: 1000 + t * 9, cy: 560, z: 1.03});
  else cam.render({cx: 1190 + (t - cut) * 5, cy: 545, z: 1.42 + (t - cut) * 0.008});
  // the sickle rides his hand while he works, then stays hooked in the trunk
  fa.render(PW.state(Math.min(t, tStop)));
  Rig.attach(q('sc03-sickle'), fa, 0, SICKLE);
  const front = t >= tA && t < tB, left = t >= tB;
  let st = PW.state(t);
  if (t > tStop) st.arm = Rig.mixArm(st.arm, [0, -9], Rig.smooth(drop(t)));
  if (left) { st = {t, x: FX, y: FY, h: FH, dir: -1, d: 0, settle: 1, head: head(t), lean: lean(t), idle: 0.6};
    st.arm = Rig.mixArm([0, -9], [-152, -12], Rig.smooth(pt(t))); }
  st.op = front ? 0 : 1;
  fa.render(st);
  faF.render({t, x: FX, y: FY, h: FH, dir: -1, op: front ? 1 : 0});
  fib(t); dust.render(t);
  sa.render({t, x: sx(t), x0: -160, y: 965, h: 600, dir: 1, run: 1, settle: sset(t), head: sHead(t), dy: pant(t)});
});
""")

# ------------------------------------------------------------------ sc04 interior: the morning he did not get up
scene("sc04", 24.1, 12.9, "04_salem_home_interior",
      [rig("sc04-father", 14), div("sc04-blanket", 16, "left:0;top:0;width:620px;height:120px;transform-origin:0 0",
                                   '<svg width="620" height="120" viewBox="0 0 620 120"><path d="M8 40 Q40 8 120 14 L560 18 Q612 22 612 70 L610 110 L10 110 Q2 80 8 40 Z" fill="#7a4f33" stroke="#5c3a24" stroke-width="3"/>'
                                   '<path d="M440 18 L452 110 M470 19 L482 110" stroke="#e7d6b8" stroke-width="7" opacity=".85"/><path d="M60 40 Q300 30 600 46" stroke="#5c3a24" stroke-width="2" fill="none" opacity=".5"/></svg>'),
       rig("sc04-salemw", 20), rig("sc04-salem", 20), div("sc04-motes", 30, "left:0;top:0")],
      r"""
const fa = Rig.make(q('sc04-father'), 'father_side', {seed: 9});
const sw = Rig.make(q('sc04-salemw'), 'salem_side', {seed: 4});
const ss = Rig.make(q('sc04-salem'), 'salem_q34', {seed: 6, lap: {y: 430}});
const cam = Rig.camera(q('sc04-cam'));
const sun = T([[0,0.05],[at(22.9),0.05],[at(24.1),0.85]]);
// dust motes drifting in the shaft of light from the window
const moteEls = []; for (let i = 0; i < 14; i++) { const e = document.createElement('div'); const sz = 3 + (i % 4);
  Object.assign(e.style, {position: 'absolute', left: '0px', top: '0px', width: sz + 'px', height: sz + 'px', borderRadius: '50%', background: '#fff3cf', opacity: 0});
  q('sc04-motes').appendChild(e); moteEls.push(e); }
const motes = (t, lit) => moteEls.forEach((e, i) => { const r1 = ((i * 37) % 100) / 100, r2 = ((i * 61) % 100) / 100;
  const u = (r1 + t * (0.012 + 0.01 * r2)) % 1, w = (r2 - 0.5) * 150 + 14 * Math.sin(t * 0.6 + i);
  e.style.transform = `translate(${170 + 300 * u + w * 0.85}px, ${230 + 470 * u - w * 0.5 + 8 * Math.sin(t * 0.9 + i * 2)}px)`;
  e.style.opacity = lit * (0.25 + 0.3 * (0.5 + 0.5 * Math.sin(t * 1.4 + i * 1.7))) * Math.sin(Math.PI * u); });
const dark = T([[0,0.42],[at(22.9),0.42],[at(24.1),0.08]]);
const cutB = at(25.75), cutC = at(27.6);
const swx = T([[0,1720],[at(25.9),1720],[at(27.4),1260,'lin']]);
const swset = T([[0,0],[at(27.4),0],[at(27.8),1]]);
// Salem seated: lean in on «يبه», proud bounce on «اليوم أنا سبقتك»
const sLean = T([[0,2],[at(28.1),2],[at(28.45),10],[at(28.9),4],[at(30.0),2]]);
const sArm = T([[0,0],[at(28.0),0],[at(28.45),1],[at(29.0),1],[at(29.4),0]]);
const sHead = T([[0,4],[at(28.6),4],[at(29.0),-6],[at(29.5),-3],[at(30.1),2],[at(31.5),6]]);
const sDy = T([[0,0],[at(29.05),0],[at(29.25),-7],[at(29.45),0],[at(29.65),-5],[at(29.85),0]]);
// father: head turns to Salem («ابتسم لي»), tries to rise («ما قدر يقوم»)
const fHead = T([[0,0],[at(30.7),0],[at(31.2),14],[at(31.45),10],[at(31.65),15],[at(33.5),12]]);
const fLean = T([[0,0],[at(31.95),0],[at(32.45),13,'out'],[at(32.65),12],[at(33.2),1,'in']]);
const fArm = T([[0,0],[at(31.9),0],[at(32.4),-18],[at(33.2),0]]);
Rig.drive(tl, DUR, (t) => {
  if (t < cutB) cam.render({cx: 900 - t * 8, cy: 560, z: 1.05});
  else if (t < cutC) cam.render({cx: 1150, cy: 600, z: 1.15});
  else cam.render({cx: 760 + (t - cutC) * 4, cy: 650, z: 1.75 + (t - cutC) * 0.012});
  q('sc04-sun').style.opacity = sun(t);
  q('sc04-dark').style.opacity = dark(t);
  const fst = {t, x: 1030, y: 712, h: 600, dir: 1, rot: -90, d: 0, settle: 1, head: fHead(t), lean: fLean(t),
               arm: [fArm(t), -10], idle: 0.3, shadow: 0, swing: 0};
  fa.render(fst);
  // blanket covers him from the chest down
  const p = Rig.pt(fa, fst, fa.ox, fa.R.waist * 0.62);
  const br = 0.045 * Math.sin(t * 2 * Math.PI / 3.6);          // slow, tired breathing under the blanket
  q('sc04-blanket').style.transform = `translate(${p.x - 24}px, ${p.y - 46 - 102 * br}px) scale(0.66, ${0.85 * (1 + br)})`;
  motes(t, sun(t));
  const walking = t < cutC;
  sw.render({t, x: swx(t), x0: 1720, y: 880, h: 600, dir: -1, settle: swset(t), op: walking ? 1 : 0});
  const sst = {t, x: 700, y: 850, h: 540, dir: -1, lean: sLean(t), head: sHead(t), dy: sDy(t), op: walking ? 0 : 1, shadow: 0.6};
  // hand to father's shoulder
  // a gentle reach: his hand comes to rest on his father's chest, just in front of him
  const sh = Rig.pt(ss, sst, ss.R.arms[0].shoulder[0], ss.R.arms[0].shoulder[1] + ss.sitGap);
  const reachA = Rig.reach(ss, sst, 0, sh.x - 40, sh.y + 100, 1);
  sst.arm = Rig.mixArm([4, -6], reachA, Rig.smooth(sArm(t)));
  ss.render(sst);
});
""",
      overlay='<div id="sc04-dark" class="grade" style="background:rgba(40,30,45,1)"></div>'
              '<div id="sc04-sun" class="grade" style="background:linear-gradient(115deg,rgba(255,214,140,.0) 10%,rgba(255,214,140,.35) 22%,rgba(255,214,140,0) 34%,rgba(255,214,140,.25) 40%,rgba(255,214,140,0) 52%);mix-blend-mode:screen"></div>')

# ------------------------------------------------------------------ sc05 courtyard: mother tells uncle; uncle helps father out
scene("sc05", 37.0, 10.0, "03_salem_home_courtyard",
      [rig("sc05-mother", 20), rig("sc05-uncleq", 21), rig("sc05-salem", 18),
       rig("sc05-father", 22), div("sc05-farm", 25, "left:0;top:0"), rig("sc05-uncle", 24), rig("sc05-salemw", 26)],
      r"""
const mo = Rig.make(q('sc05-mother'), 'mother_q34', {seed: 3});
const uq = Rig.make(q('sc05-uncleq'), 'uncle_q34', {seed: 5});
const sq = Rig.make(q('sc05-salem'), 'salem_q34', {seed: 8});
const fa = Rig.make(q('sc05-father'), 'father_side', {seed: 2, armLayer: q('sc05-farm')});
const un = Rig.make(q('sc05-uncle'), 'uncle_side', {seed: 6});
const sw = Rig.make(q('sc05-salemw'), 'salem_side', {seed: 4});
const cam = Rig.camera(q('sc05-cam'));
const cut1 = at(39.55), cut2 = at(41.3);
const moHead = T([[0,0],[at(36.2),0],[at(36.5),4],[at(37.9),2],[at(38.3),-6],[at(39.4),-2]]);
const moLean = T([[0,0],[at(36.2),0],[at(36.6),3],[at(38.4),5],[at(39.4),1]]);
const unHead = T([[0,-2],[at(39.3),-2],[at(39.55),7],[at(39.8),1],[at(40.0),6],[at(40.4),0]]);
const sHead = T([[0,0],[at(39.7),0],[at(40.2),-10],[at(40.9),-8],[at(41.3),0]]);
const sDy = T([[0,0],[at(40.6),0],[at(40.8),-6],[at(41.1),0]]);
const sArm = T([[0,0],[at(40.5),0],[at(40.8),-14],[at(41.1),0]]);
const ex = T([[0,1460],[cut2,1460],[10,1000,'lin']]);
const swx = T([[0,1330],[at(43.9),1330],[10,1130,'lin']]);
Rig.drive(tl, DUR, (t) => {
  if (t < cut1) cam.render({cx: 820 + t * 6, cy: 580, z: 1.12});
  else if (t < cut2) cam.render({cx: 1290, cy: 560, z: 1.9});
  else cam.render({cx: 1080 - (t - cut2) * 20, cy: 580, z: 1.25});
  const before = t < cut2;
  mo.render({t, x: 440, y: 885, h: 560, dir: 1, head: moHead(t) + Rig.talk(t, at(36.34), at(39.34), 2.5, 1), lean: moLean(t)});
  uq.render({t, x: 690, y: 890, h: 560, dir: -1, head: unHead(t), op: before ? 1 : 0});
  sq.render({t, x: before ? 1290 : 1180, y: 805, h: 470, dir: -1, head: sHead(t), dy: sDy(t), arm: [sArm(t), 0],
             op: t < at(43.9) ? 1 : 0});
  // supported walk: father leans on uncle, his arm across uncle's shoulders
  const ust = {t, x: ex(t), x0: 1460, y: 840, h: 560, dir: -1, op: before ? 0 : 1, swing: 0.6};
  const fst = {t, x: ex(t) + 105, x0: 1565, y: 812, h: 548, dir: -1, head: 9, lean: 5, op: before ? 0 : 1, swing: 0.2};
  un.render(ust);
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] - 4, un.R.arms[0].shoulder[1] - 26);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, 1); fst.lock = 1;
  fa.render(fst);
  sw.render({t, x: swx(t), x0: 1330, y: 806, h: 470, dir: -1, op: t >= at(43.9) ? 1 : 0});
});
""")

# ------------------------------------------------------------------ sc07 hospital exterior: «هذا؟ هذا بيت!»
scene("sc07", 48.4, 7.2, "01_hospital_exterior",
      [rig("sc07-father", 20), div("sc07-farm", 23, "left:0;top:0"), rig("sc07-uncle", 22), rig("sc07-salemw", 24), rig("sc07-salem", 24),
       rig("sc07-woman", 8), rig("sc07-girl", 8)],
      r"""
const fa = Rig.make(q('sc07-father'), 'father_side', {seed: 1, armLayer: q('sc07-farm')});
const un = Rig.make(q('sc07-uncle'), 'uncle_side', {seed: 3});
const sw = Rig.make(q('sc07-salemw'), 'salem_side', {seed: 5});
const sq = Rig.make(q('sc07-salem'), 'salem_q34', {seed: 7});
const wo = Rig.figure(q('sc07-woman'), 'assets/chars/res_woman_stand.png', 528, 1304, {seed: 2});
const gi = Rig.figure(q('sc07-girl'), 'assets/chars/res_girl_stand.png', 512, 1204, {seed: 6});
const cam = Rig.camera(q('sc07-cam'));
const stop = at(47.1);
const ux = T([[0,1560],[stop,1270,'out'],[at(52.05),1270],[DUR,1130,'in']]);
const uset = T([[0,0],[stop - 0.1,0],[stop + 0.45,1],[at(52.0),1],[at(52.3),0]]);
const sx = T([[0,1330],[stop,1060,'out']]);
const sset = T([[0,0],[stop - 0.1,0],[stop + 0.4,1]]);
const turnBack = at(47.65), pointT = at(48.45), turnUncle = at(49.15), goT = at(52.1);
const sDir = (t) => (t >= turnBack && t < pointT) || (t >= turnUncle && t < goT) ? 1 : -1;
const sPoint = T([[0,0],[pointT,0],[pointT + 0.3,1,'out'],[at(49.1),1],[at(49.4),0]]);
const sHead = T([[0,0],[turnBack,-8],[pointT,-4],[turnUncle,-8],[at(50.0),-3],[at(50.5),-6]]);
const sDy = T([[0,0],[at(49.7),0],[at(49.9),-6],[at(50.15),0]]);
const beck = T([[0,0],[at(50.85),0],[at(51.1),1],[at(52.2),1],[at(52.45),0]]);
const uHead = T([[0,0],[at(50.8),0],[at(51.0),6],[at(51.4),-2],[at(51.8),5],[at(52.3),0]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 1000 - t * 8, cy: 560, z: 1.08 + t * 0.012});
  const ust = {t, x: ux(t), x0: 1560, y: 975, h: 600, dir: -1, settle: uset(t), swing: 0.6, head: uHead(t)};
  const b = beck(t);
  // «تعال»: forearm flicks towards himself twice
  const flick = Math.sin(Math.max(0, t - at(51.0)) * 2 * Math.PI * 1.6);
  if (b > 0) ust.arm = Rig.mixArm([0, 0], [-62 - 6 * flick, -58 - 22 * flick], b);
  un.render(ust);
  const fst = {t, x: ux(t) + 105, x0: 1665, y: 945, h: 588, dir: -1, head: 9, lean: 5, settle: uset(t), swing: 0.2};
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] - 4, un.R.arms[0].shoulder[1] - 26);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, 1); fst.lock = 1;
  fa.render(fst);
  const walking = t < stop + 0.45 || t >= goT;
  const swst = {t, x: t < goT ? sx(t) : 1060 - (t - goT) * 140, y: 990, h: 600, dir: -1, op: walking ? 1 : 0};
  swst.x0 = t < goT ? 1330 : 1060; swst.settle = t < goT ? sset(t) : 0;
  sw.render(swst);
  const p = sPoint(t);
  sq.render({t, x: 1060, y: 990, h: 600, dir: sDir(t), head: sHead(t), dy: sDy(t), op: walking ? 0 : 1,
             arm: [Rig.lerp(0, -118, p), Rig.lerp(0, -12, p)]});
  wo.render({t, x: 690, y: 712, h: 151, dir: 1});
  gi.render({t, x: 735, y: 714, h: 154, dir: -1});
});
""")

# ------------------------------------------------------------------ sc08 waiting courtyard
scene("sc08", 55.6, 10.3, "06_hospital_waiting_courtyard",
      [img("sc08-box", "props/prop_box.png", 6, "width:1324px;height:1240px"),
       img("sc08-basin", "props/prop_basin.png", 6, "width:1528px;height:752px"),
       img("sc08-bottle", "props/prop_bottle.png", 6, "width:520px;height:964px"),
       img("sc08-bandage", "props/prop_bandage.png", 6, "width:1112px;height:716px"),
       rig("sc08-old", 10), rig("sc08-boy", 10), rig("sc08-mom", 11), rig("sc08-woman", 9),
       rig("sc08-father", 20), div("sc08-farm", 23, "left:0;top:0"), rig("sc08-uncle", 22), rig("sc08-salem", 24),
       rig("sc08-marian", 18)],
      r"""
const fa = Rig.make(q('sc08-father'), 'father_side', {seed: 1, armLayer: q('sc08-farm')});
const un = Rig.make(q('sc08-uncle'), 'uncle_side', {seed: 3});
const sw = Rig.make(q('sc08-salem'), 'salem_side', {seed: 5});
const ma = Rig.make(q('sc08-marian'), 'marian_side', {seed: 8});
const old = Rig.figure(q('sc08-old'), 'assets/chars/res_oldman_sit.png', 820, 1044, {seed: 4, amp: 0.3});
const boy = Rig.figure(q('sc08-boy'), 'assets/chars/res_boy_stand.png', 504, 1300, {seed: 7});
const mom = Rig.figure(q('sc08-mom'), 'assets/chars/res_mombaby_sit.png', 836, 968, {seed: 2, amp: 1.4, period: 2.6});
const wo = Rig.figure(q('sc08-woman'), 'assets/chars/res_woman_stand.png', 528, 1304, {seed: 9});
const cam = Rig.camera(q('sc08-cam'));
const place = (id, x, y, w) => { const e = q(id); e.style.transformOrigin = '0 0'; e.style.transform = `translate(${x}px,${y}px) scale(${w / e.width})`; };
place('sc08-box', 70, 612, 120); place('sc08-basin', 196, 664, 112); place('sc08-bottle', 300, 628, 34); place('sc08-bandage', 236, 625, 52);
const stop = at(54.6);
const ux = T([[0,-140],[stop,470,'out']]);
const uset = T([[0,0],[stop - 0.1,0],[stop + 0.45,1]]);
const sx = T([[0,-40],[stop + 0.2,640,'out']]);
const sset = T([[0,0],[stop + 0.1,0],[stop + 0.55,1]]);
const sHead = T([[0,0],[at(56.6),0],[at(57.0),-6],[at(57.6),4],[at(59.5),2],[at(60.3),-4]]);
const mx = T([[0,1820],[at(60.15),1820],[at(61.5),1330,'out']]);
const mset = T([[0,0],[at(61.35),0],[at(61.8),1]]);
const mArm = T([[0,0],[at(61.5),0],[at(61.9),1],[at(62.7),1],[at(63.0),0.4]]);
const mHead = T([[0,0],[at(61.5),0],[at(61.9),-8],[at(62.6),0]]);
const c1 = at(53.6), c2 = at(55.2), c3 = at(56.7), c4 = at(59.9);
const pan = T([[c1,980],[c2,1180]]);
Rig.drive(tl, DUR, (t) => {
  if (t < c1) cam.render({cx: 900, cy: 600, z: 1.1});
  else if (t < c2) cam.render({cx: pan(t), cy: 600, z: 1.3});
  else if (t < c3) cam.render({cx: 1330 + (t - c2) * 6, cy: 640, z: 2.1 + (t - c2) * 0.03});
  else if (t < c4) cam.render({cx: 260 + (t - c3) * 12, cy: 700, z: 2.2});
  else cam.render({cx: 1060, cy: 580, z: 1.12});
  old.render({t, x: 1030, y: 770, h: 330, dir: 1});
  boy.render({t, x: 1155, y: 762, h: 330, dir: -1, rot: 0.5});
  mom.render({t, x: 1350, y: 772, h: 330, dir: -1});
  wo.render({t, x: 1585, y: 735, h: 310, dir: -1});
  const ust = {t, x: ux(t), x0: -140, y: 1000, h: 620, dir: 1, settle: uset(t), swing: 0.6};
  un.render(ust);
  const fst = {t, x: ux(t) - 105, x0: -245, y: 970, h: 608, dir: 1, head: 9, lean: 5, settle: uset(t), swing: 0.2};
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] - 4, un.R.arms[0].shoulder[1] - 26);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, 1); fst.lock = 1;
  fa.render(fst);
  sw.render({t, x: sx(t), x0: -40, y: 1012, h: 620, dir: 1, settle: sset(t), head: sHead(t)});
  const m = mArm(t);
  ma.render({t, x: mx(t), x0: 1820, y: 820, h: 560, dir: -1, settle: mset(t), head: mHead(t), arm: [Rig.lerp(0, 52, m), Rig.lerp(0, -30, m)]});
});
""")

# ------------------------------------------------------------------ sc09 clinic: bag, stethoscope, whisper, hand
scene("sc09", 65.9, 26.7, "07_clinic_interior",
      [img("sc09-bagc", "props/prop_bag_closed.png", 12, "width:1512px;height:1152px"),
       img("sc09-bago", "props/prop_bag_open.png", 12, "width:1392px;height:1312px"),
       rig("sc09-marian", 14), rig("sc09-father", 16), steth("sc09-stb", 17), rig("sc09-pat", 18), steth("sc09-stf", 19),
       # the bag's front wall again, above his hand: the hand and the stethoscope go in behind it
       img("sc09-lip", "props/prop_bag_open.png", 20, "width:1392px;height:1312px;clip-path:polygon(0% 49.5%,10% 49.5%,23.7% 63.9%,93% 52.6%,100% 53.4%,100% 100%,0% 100%)"),
       rig("sc09-uncle", 22), rig("sc09-salem", 24), rig("sc09-salemS", 24), div("sc09-farm", 26, "left:0;top:0")],
      r"""
const fa = Rig.make(q('sc09-father'), 'father_side', {seed: 3, armLayer: q('sc09-farm')});
const pat = Rig.make(q('sc09-pat'), 'pat_side', {seed: 5});
const ma = Rig.figure(q('sc09-marian'), 'assets/chars/marian_front.png', 648, 1644, {seed: 2, amp: 0.4});
const un = Rig.make(q('sc09-uncle'), 'uncle_q34', {seed: 6});
const sa = Rig.make(q('sc09-salem'), 'salem_q34', {seed: 9});
const saS = Rig.make(q('sc09-salemS'), 'salem_side', {seed: 9});
const cam = Rig.camera(q('sc09-cam'));
const place = (id, x, y, w, op, sy) => { const e = q(id); e.style.transformOrigin = '0 100%'; e.style.transform = `translate(${x}px,${y}px) scale(${w / e.width}, ${(w / e.width) * (sy || 1)})`; e.style.opacity = op; };
// shot cuts (scene time)
const S2 = at(65.95), S3 = at(68.5), S4a = at(72.95), S4b = at(74.3), S5 = at(78.7), S6 = at(85.05);

// ---- the stethoscope, drawn each frame
const SV = (id, k, v) => q(id).setAttribute(k, v);
function stethHeld(id, g, phi) {            // held at the fork: ear tubes spring up, tubing and chest piece hang
  const L = 108, bx = g.x + L * Math.sin(phi), by = g.y + L * Math.cos(phi);
  SV(id + '-m1', 'd', `M ${g.x} ${g.y} Q ${g.x - 4} ${g.y - 26} ${g.x - 15} ${g.y - 46}`);
  SV(id + '-m2', 'd', `M ${g.x} ${g.y} Q ${g.x + 4} ${g.y - 26} ${g.x + 15} ${g.y - 46}`);
  SV(id + '-e1', 'cx', g.x - 16); SV(id + '-e1', 'cy', g.y - 49); SV(id + '-e2', 'cx', g.x + 16); SV(id + '-e2', 'cy', g.y - 49);
  SV(id + '-t', 'd', `M ${g.x} ${g.y} Q ${g.x + L * 0.5 * Math.sin(phi * 0.3)} ${g.y + L * 0.55} ${bx} ${by}`);
  SV(id + '-b', 'cx', bx); SV(id + '-b', 'cy', by); SV(id + '-bi', 'cx', bx); SV(id + '-bi', 'cy', by);
}
function stethWorn(id, ear, fork, bell, dir) {   // in his ears, fork on his chest, tubing to the chest piece
  SV(id + '-m1', 'd', `M ${ear.x} ${ear.y} Q ${ear.x + 30 * dir} ${ear.y + 30} ${fork.x} ${fork.y}`);
  SV(id + '-m2', 'd', `M ${ear.x + 5 * dir} ${ear.y + 3} Q ${ear.x + 34 * dir} ${ear.y + 34} ${fork.x} ${fork.y}`);
  SV(id + '-e1', 'cx', ear.x); SV(id + '-e1', 'cy', ear.y); SV(id + '-e2', 'cx', ear.x); SV(id + '-e2', 'cy', ear.y);
  const sag = Math.max(26, 96 - Math.hypot(bell.x - fork.x, bell.y - fork.y) * 0.32);
  SV(id + '-t', 'd', `M ${fork.x} ${fork.y} C ${fork.x + 4 * dir} ${fork.y + sag}, ${bell.x - 34 * dir} ${bell.y + sag * 0.8}, ${bell.x} ${bell.y}`);
  SV(id + '-b', 'cx', bell.x); SV(id + '-b', 'cy', bell.y); SV(id + '-bi', 'cx', bell.x); SV(id + '-bi', 'cy', bell.y);
}

// ---- shot 1: «فتح شنطته، وطلّع شي فيه أنبوب»
const BAG = {x: 418, y: 414, w: 154};                       // open bag on the desk; its mouth is near (500, 500)
const tOpen = at(63.38), tOut = at(64.05), tUp = at(64.78);
const k1 = T([[0,0],[at(62.95),0],[at(63.25),1]]);
const hx = T([[0,512],[at(63.45),512],[at(63.85),498],[tOut,498],[tUp,548,'io'],[at(65.3),548],[at(65.95),588]]);
const hy = T([[0,438],[at(63.45),438],[at(63.85),506],[tOut,506],[tUp,338,'io'],[at(65.3),338],[at(65.95),318]]);
const pop = T([[0,1],[tOpen,1],[tOpen + 0.07,1.1],[tOpen + 0.24,1]]);
const swing = (t) => t < tUp ? -0.10 * Math.sin((t - tOut) * 7) : 0.2 * Math.exp(-(t - tUp) * 2.4) * Math.sin((t - tUp) * 7.5 + 0.6);
const p1Head = T([[0,7],[tOut,9],[tUp,3],[at(65.6),0]]);
// ---- shots 2-6: «وحط طرفه على صدر أبوي»
const PX = 1388, PY = 905, FAX = 1572, FAY = 900;
const toChest = T([[0,0],[S2,0],[at(66.95),1,'out'],[at(84.2),1],[at(85.0),0]]);
const shift = T([[0,0],[at(69.6),0],[at(70.1),1],[at(76.6),1],[at(77.1),2],[at(81.2),2],[at(81.7),1]]);   // he moves the chest piece
const press = (t) => 1.2 * Math.sin(t * 2.1);
const patHead = T([[0,5],[at(69.6),5],[at(70.0),8],[at(76.6),8],[at(77.0),5],[at(81.6),5],[at(81.85),10],[at(82.1),5],[at(82.35),9],[at(82.7),5]]);
const fHead0 = T([[0,5],[at(67.2),5],[at(67.8),9],[at(84),7]]);
// ---- shot 3: whisper
const sLean = T([[0,0],[at(68.6),0],[at(69.3),9],[at(70.7),11],[at(71.4),7],[at(72.4),3]]);
const sDy = T([[0,0],[at(69.0),0],[at(69.3),-10],[at(71.5),-10],[at(71.9),0]]);
const sHead = T([[0,0],[at(70.6),0],[at(70.85),-12],[at(71.4),-6],[at(72.9),-2]]);
const uHead = T([[0,0],[at(71.3),0],[at(71.6),10],[at(72.5),8],[at(73.0),2]]);
const uArm = T([[0,0],[at(71.5),0],[at(71.9),-28],[at(72.6),-30],[at(73.2),0]]);
// ---- shot 6: watching
const s5lean = (t) => Rig.wob(t, 4, 2.3, 2.2);
const s5head = T([[0,-6],[at(81.3),-6],[at(81.7),-11],[at(83.0),-9],[at(83.6),-13],[at(85),-9]]);
// ---- shot 7: «مسك يدي وقال: ما عليك يا سالم»
const hand = T([[0,0],[at(86.3),0],[at(87.3),1,'io']]);
const salHand = T([[0,0],[at(86.45),0],[at(87.2),1]]);
const fNod = T([[0,4],[at(86.3),4],[at(87.0),12],[at(87.9),12],[at(88.25),17],[at(88.55),11],[at(88.85),16],[at(89.6),12]]);
const fLean = T([[0,1],[at(86.3),1],[at(87.2),5],[at(89.6),4]]);
const sUp = T([[0,0],[at(86.6),0],[at(87.3),-10],[at(89.6),-12]]);
const MEET = {x: 1508, y: 634};

Rig.drive(tl, DUR, (t) => {
  const shot = t < S2 ? 1 : t < S3 ? 2 : t < S4a ? 3 : t < S4b ? 4 : t < S5 ? 5 : t < S6 ? 6 : 7;
  // father, in profile, facing the doctor
  const fst = {t, x: FAX, y: FAY, h: 610, dir: -1, d: 0, settle: 1, head: shot === 7 ? fNod(t) : fHead0(t), lean: shot === 7 ? fLean(t) : 1,
               idle: 0.4, breath: shot === 7 ? 1 : 2.6};
  const chest = Rig.pt(fa, fst, 196, 330);                  // the front of his chest
  const spot = {x: chest.x + 3, y: chest.y + Rig.lerp(0, 34, Rig.clamp(shift(t), 0, 1)) - Rig.lerp(0, 50, Rig.clamp(shift(t) - 1, 0, 1))};
  if (shot === 1) cam.render({cx: 610, cy: 500, z: 1.8 + t * 0.02});
  else if (shot === 2) cam.render({cx: 1300, cy: 520, z: 1.55 + (t - S2) * 0.01});
  else if (shot === 3) cam.render({cx: 960, cy: 560, z: 1.02});
  else if (shot === 4) cam.render({cx: 600, cy: 600, z: 2.0});
  else if (shot === 5) cam.render({cx: chest.x - 70, cy: chest.y + 16, z: 2.5 + (t - S4b) * 0.03});
  else if (shot === 6) cam.render({cx: 1330, cy: 540, z: 1.45});
  else cam.render({cx: 1415, cy: 575, z: 1.85 + (t - S6) * 0.012});

  // ---- the bag
  const opened = t >= tOpen;
  place('sc09-bagc', BAG.x - 6, BAG.y + 18 + 126 - 1152, 165, opened ? 0 : 1);
  place('sc09-bago', BAG.x, BAG.y + 145 - 1312, BAG.w, opened ? 1 : 0, pop(t));
  place('sc09-lip', BAG.x, BAG.y + 145 - 1312, BAG.w, opened ? 1 : 0, pop(t));

  // ---- the doctor
  let pst, bell = null;
  const ear = (st) => Rig.pt(pat, st, 212, 150), fork = (st) => Rig.pt(pat, st, 276, 470);
  if (shot === 1) {
    pst = {t, x: 668, y: 900, h: 640, dir: -1, head: p1Head(t), lean: 2 * k1(t), idle: 0.2};
    pst.arm = Rig.mixArm([0, -9], Rig.reach(pat, pst, 0, hx(t), hy(t), 1), Rig.smooth(k1(t)));
  } else if (shot === 7) {
    pst = {t, x: 1215, y: 905, h: 640, dir: 1, head: 4, idle: 0.5};
  } else {
    pst = {t, x: PX, y: PY, h: 640, dir: 1, head: patHead(t), lean: 1.5 * toChest(t), idle: 0.15};
    const f0 = fork(pst);
    const own = {x: f0.x + 26, y: f0.y + 76};                // the chest piece starts in his hand, by his own chest
    const u = Rig.smooth(toChest(t));
    const tx = Rig.lerp(own.x, spot.x - 30, u) + press(t) * u, ty = Rig.lerp(own.y, spot.y + 3, u);
    pst.arm = Rig.reach(pat, pst, 0, tx, ty, 1);
  }
  pat.render(pst);
  const hw = pat.handWorld(0);
  const ar = hw.ang * Math.PI / 180, ux = -Math.sin(ar) * hw.dir, uy = Math.cos(ar);   // along his forearm
  // ---- the stethoscope
  const held = shot === 1 && t >= tOut;
  q('sc09-stb').style.opacity = held ? 1 : 0;
  q('sc09-stb').style.clipPath = 'inset(0px 0px 548px 0px)';       // nothing shows below the bag's foot
  if (held) stethHeld('sc09-stb', {x: hw.x + ux * 4, y: hw.y + uy * 4}, swing(t));
  const worn = shot >= 2 && shot !== 4;
  q('sc09-stf').style.opacity = worn ? 1 : 0;
  if (worn) {
    const f1 = fork(pst);
    bell = shot === 7 ? {x: f1.x + 8, y: f1.y + 118} : {x: hw.x + ux * 23, y: hw.y + uy * 23};
    stethWorn('sc09-stf', ear(pst), f1, bell, 1);
  }
  // ---- father's arm, and the hand
  if (shot === 7) {
    fst.arm = Rig.mixArm([0, -9], Rig.reach(fa, fst, 0, MEET.x + 9, MEET.y - 10, 1), Rig.smooth(hand(t)));
    fst.idle = 0.15;
  }
  fa.render(fst);
  ma.render({t, x: 1800, y: 852, h: 640, dir: -1});
  // ---- uncle + Salem
  const ust = (shot === 7 || shot === 1) ? {t, x: 980, y: 930, h: 640, dir: 1, op: 0} : {t, x: 470, y: 960, h: 640, dir: 1, head: uHead(t), arm: [uArm(t), -10]};
  un.render(ust);
  let sst;
  if (shot <= 3) sst = {t, x: 640, y: 975, h: 640, dir: -1, lean: sLean(t), dy: sDy(t), head: sHead(t), op: shot === 1 ? 0 : 1};
  else if (shot === 4) sst = {t, x: 640, y: 975, h: 640, dir: 1, head: T([[S4a,-2],[S4a+0.5,-9]])(t)};
  else if (shot === 5) sst = {t, x: 1100, y: 975, h: 640, dir: 1, op: 0};
  else if (shot === 6) sst = {t, x: 1100, y: 985, h: 640, dir: 1, lean: s5lean(t), head: s5head(t), arm: [Rig.wob(t, 2, 1.7, 6), -10]};
  else sst = {t, x: 1100, y: 975, h: 640, dir: 1, op: 0};
  sa.render(sst);
  // in profile for the hand-hold: he lifts his hand and his father's closes over it
  const s7 = {t, x: 1428, y: 908, h: 640, dir: 1, d: 0, settle: 1, head: sUp(t), idle: 0.2, op: shot === 7 ? 1 : 0};
  s7.arm = Rig.mixArm([0, -9], Rig.reach(saS, s7, 0, MEET.x - 9, MEET.y + 10, 1), Rig.smooth(salHand(t)));
  saS.render(s7);
});
""")

# ------------------------------------------------------------------ sc10 lane: walking home hand in hand
HAND_WALK = r"""
// Salem leads, his hand reaching back and up; his father's comes forward and down to hold it.
function handWalk(t, fa, sa, x0, y, h, v, extra) {
  const k = h / 640, sx = x0 - t * v, fx = sx + 200 * k;
  const sst = Object.assign({t, x: sx, x0: x0, y: y + 10 * k, h, dir: -1, swing: 0.6, lock: 1, head: 5}, extra || {});
  const fst = Object.assign({t, x: fx, x0: x0 + 200 * k, y, h: h * 0.98, dir: -1, swing: 0.6, lock: 1, head: 6}, extra || {});
  const M = {x: sx + 115 * k, y: y - 290 * k};
  sst.arm = Rig.reach(sa, sst, 0, M.x - 4 * k, M.y + 7 * k, 1);
  fst.arm = Rig.reach(fa, fst, 0, M.x + 5 * k, M.y - 7 * k, 1);
  sa.render(sst); fa.render(fst);
}
"""
scene("sc10", 92.6, 2.9, "02_neighborhood_lane",
      [rig("sc10-father", 20), rig("sc10-salem", 24), div("sc10-farm", 26, "left:0;top:0"), rig("sc10-girl", 10)],
      HAND_WALK + r"""
const fa = Rig.make(q('sc10-father'), 'father_side', {seed: 2, armLayer: q('sc10-farm')});
const sa = Rig.make(q('sc10-salem'), 'salem_side', {seed: 6});
const gi = Rig.figure(q('sc10-girl'), 'assets/chars/res_girl_stand.png', 512, 1204, {seed: 3});
const cam = Rig.camera(q('sc10-cam'));
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 1060 - t * 60, cy: 590, z: 1.15});
  handWalk(t, fa, sa, 1350, 975, 640, 110);
  gi.render({t, x: 430, y: 770, h: 260, dir: 1});
});
""")

# ------------------------------------------------------------------ sc11 days pass
scene("sc11", 95.5, 4.4, "01_hospital_exterior",
      [rig("sc11-father", 20), rig("sc11-salem", 24), div("sc11-farm", 26, "left:0;top:0")],
      HAND_WALK + r"""
const fa = Rig.make(q('sc11-father'), 'father_side', {seed: 4, armLayer: q('sc11-farm')});
const sa = Rig.make(q('sc11-salem'), 'salem_side', {seed: 8});
const cam = Rig.camera(q('sc11-cam'));
// day -> dusk -> night -> dawn
// day -> dusk -> night -> dawn, spread over the scene's length
const k = 4.4 / DUR;
const dusk0 = T([[0,0],[1.3,0],[2.0,0.75],[2.6,0.2],[3.3,0]]), dusk = (t) => dusk0(t * k);
const night0 = T([[0,0],[1.7,0],[2.3,0.72],[2.9,0.72],[3.6,0]]), night = (t) => night0(t * k);
const dawn0 = T([[0,0],[2.9,0],[3.5,0.6],[4.4,0.35]]), dawn = (t) => dawn0(t * k);
const walkOp0 = T([[0,1],[1.4,1],[1.9,0]]), walkOp = (t) => walkOp0(t * k);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 960, cy: 540, z: 1.0 + t * 0.01});
  q('sc11-dusk').style.opacity = dusk(t); q('sc11-night').style.opacity = night(t); q('sc11-dawn').style.opacity = dawn(t);
  handWalk(t, fa, sa, 1500, 840, 360, 110, {op: walkOp(t)});
});
""",
      overlay='<div id="sc11-dusk" class="grade" style="background:linear-gradient(180deg,rgba(214,110,50,.75),rgba(120,50,30,.55))"></div>'
              '<div id="sc11-night" class="grade" style="background:rgba(18,26,60,.85)"></div>'
              '<div id="sc11-dawn" class="grade" style="background:linear-gradient(180deg,rgba(255,200,150,.6),rgba(255,236,200,.1))"></div>')

# ------------------------------------------------------------------ sc12 interior: empty bed
scene("sc12", 99.9, 3.1, "04_salem_home_interior",
      [rig("sc12-salem", 20)],
      r"""
const sa = Rig.make(q('sc12-salem'), 'salem_q34', {seed: 3, lap: {y: 430}});
const cam = Rig.camera(q('sc12-cam'));
// «فتحت عيوني»: he straightens up from sleep, then turns to the empty bed
const lean = T([[0,26],[at(96.9),26],[at(97.7),2,'io'],[at(98.0),0]]);
const head = T([[0,16],[at(96.9),16],[at(97.6),-2],[at(98.1),0],[at(98.5),7],[at(99.4),5]]);
const dy = T([[0,10],[at(96.9),10],[at(97.7),0]]);
const pan = T([[0,1240],[at(98.1),1240],[at(99.3),820]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: pan(t), cy: 660, z: 1.55});
  sa.render({t, x: 1330, y: 805, h: 600, dir: -1, lean: lean(t), head: head(t), dy: dy(t), arm: [6, -8], shadow: 0.6});
});
""",
      overlay='<div class="grade" style="background:linear-gradient(115deg,rgba(255,214,140,0) 10%,rgba(255,214,140,.3) 24%,rgba(255,214,140,0) 36%);mix-blend-mode:screen"></div>')

# ------------------------------------------------------------------ sc13 courtyard: run
scene("sc13", 103.0, 1.4, "03_salem_home_courtyard",
      [div("sc13-dust", 15, "left:0;top:0"), rig("sc13-salem", 20), rig("sc13-mother", 10)],
      r"""
const sa = Rig.make(q('sc13-salem'), 'salem_side', {seed: 5});
const mo = Rig.make(q('sc13-mother'), 'mother_q34', {seed: 2});
const cam = Rig.camera(q('sc13-cam'));
const rx = (t) => 1430 - t * 560;
const dust = Rig.dust(q('sc13-dust'), Rig.footfalls(sa, {x: rx, x0: 1430, h: 560, run: 1, dir: -1, t0: 0, t1: DUR, y: 838}), {drift: -26});
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 1140 - t * 220, cy: 560, z: 1.12});
  dust.render(t);
  sa.render({t, x: rx(t), x0: 1430, y: 840, h: 560, dir: -1, run: 1});
  mo.render({t, x: 330, y: 885, h: 560, dir: 1, head: -4});
});
""")

# ------------------------------------------------------------------ sc14 palms: reunion
scene("sc14", 104.4, 9.1, "05_palm_garden",
      [div("sc14-dust", 18, "left:0;top:0"), rig("sc14-father", 20), rig("sc14-fatherF", 20), sickle("sc14-sickle", 21),
       div("sc14-fib", 22, "left:0;top:0"), rig("sc14-salem", 25), div("sc14-farm", 27, "left:0;top:0")],
      PALM_FATHER + r"""
const fa = Rig.make(q('sc14-father'), 'father_side', {seed: 2, armLayer: q('sc14-farm')});
const faF = Rig.make(q('sc14-fatherF'), 'father_front', {seed: 2});
const sa = Rig.make(q('sc14-salem'), 'salem_side', {seed: 7});
const cam = Rig.camera(q('sc14-cam'));
// «رفع راسه وابتسم»: he leaves the sickle in the trunk and turns round
const tStop = at(102.85), tA = at(103.0), tB = at(103.18);
const PW = palmWork(fa, tStop);
fa.render(PW.state(tStop)); const CUTPT = (() => { const h = Rig.attach(q('sc14-sickle'), fa, 0, SICKLE); return {x: h.x + 34, y: h.y - 96}; })();
const fib = fibres(q('sc14-fib'), PW.hits, CUTPT);
const drop = T([[0,0],[tStop,0],[tStop + 0.25,1]]);
const head = T([[0,0],[tB,6],[at(103.5),-5,'out'],[at(103.8),1],[at(104.1),-4],[at(104.6),-3],
                [at(105.4),3],[at(105.7),-3],[at(106.7),0],[at(108.2),4],[at(109.6),8]]);
const lean = T([[0,0],[tB,1],[at(103.5),-3],[at(103.75),-1],[at(104.05),-4],[at(106.8),-1],[at(109.6),3]]);
const dy = T([[0,0],[at(103.5),0],[at(103.7),-8],[at(103.95),0]]);
const pt = T([[0,0],[at(104.85),0],[at(105.4),1,'out'],[at(106.45),1],[at(106.9),0]]);
const sx = T([[0,-200],[at(102.4),880,'out'],[at(107.0),880],[at(108.15),1378]]);
const sset = T([[0,0],[at(102.25),0],[at(102.7),1],[at(107.0),1],[at(107.25),0],[at(108.0),0],[at(108.4),1]]);
const onShoulder = T([[0,0],[at(108.1),0],[at(108.8),1]]);
const sHead = T([[0,0],[at(102.7),0],[at(103.2),-9],[at(107.0),-6],[at(108.6),-11],[at(110.5),-8]]);
const sBounce = T([[0,0],[at(108.9),0],[at(109.1),-6],[at(109.3),0],[at(109.5),-4],[at(109.7),0]]);
const falls = Rig.footfalls(sa, {x: sx, x0: -200, h: 600, run: 1, dir: 1, t0: 0, t1: at(102.35), y: 962});
const dust = Rig.dust(q('sc14-dust'), falls, {drift: 26});
const c1 = at(104.5), c2 = at(106.95);
Rig.drive(tl, DUR, (t) => {
  if (t < c1) cam.render({cx: 1000 + t * 8, cy: 560, z: 1.03});
  else if (t < c2) cam.render({cx: 1230, cy: 535, z: 1.5});
  else cam.render({cx: 1300 + (t - c2) * 8, cy: 600, z: 1.38});
  fa.render(PW.state(Math.min(t, tStop)));
  Rig.attach(q('sc14-sickle'), fa, 0, SICKLE);
  const front = t >= tA && t < tB, left = t >= tB;
  const running = t < at(103);
  const sst = {t, x: sx(t), x0: running ? -200 : 880, y: 965, h: 600, dir: 1, run: running ? 1 : 0, settle: sset(t), head: sHead(t), dy: sBounce(t)};
  sa.render(sst);
  let st = PW.state(t);
  if (t > tStop) st.arm = Rig.mixArm(st.arm, [0, -9], Rig.smooth(drop(t)));
  if (left) { st = {t, x: FX, y: FY, h: FH, dir: -1, d: 0, settle: 1, head: head(t), lean: lean(t), dy: dy(t), idle: 0.6};
    // his hand comes down on Salem's head and ruffles his hair
    const top = Rig.pt(sa, sst, sa.R.head.pivot[0] - 26, 34);
    const ruf = t > at(108.8) ? 8 * Math.sin((t - at(108.8)) * 10) * Math.exp(-(t - at(108.8)) * 1.1) : 0;
    const up = Rig.mixArm([0, -9], [-152, -12], Rig.smooth(pt(t)));
    st.arm = Rig.mixArm(up, Rig.reach(fa, st, 0, top.x + ruf, top.y - 4, 1), Rig.smooth(onShoulder(t))); }
  st.op = front ? 0 : 1;
  fa.render(st);
  faF.render({t, x: FX, y: FY, h: FH, dir: -1, op: front ? 1 : 0});
  fib(t); dust.render(t);
});
""")

# ------------------------------------------------------------------ sc15 hospital, later: passing by, memory, Salem's back
scene("sc15", 113.5, 13.5, "01_hospital_exterior",
      [rig("sc15-marian", 8), rig("sc15-woman", 9), rig("sc15-girl", 9), rig("sc15-old", 9), rig("sc15-basket", 8),
       rig("sc15-salem", 24), rig("sc15-mfather", 26), rig("sc15-msalem", 27), div("sc15-mfarm", 28, "left:0;top:0"), rig("sc15-back", 30), rig("sc15-father", 29)],
      HAND_WALK + r"""
const ma = Rig.make(q('sc15-marian'), 'marian_side', {seed: 4});
const wo = Rig.figure(q('sc15-woman'), 'assets/chars/res_mombaby_stand.png', 592, 1328, {seed: 2});
const gi = Rig.figure(q('sc15-girl'), 'assets/chars/res_girl_walk.png', 672, 1204, {seed: 6, amp: 0.3});
const old = Rig.figure(q('sc15-old'), 'assets/chars/res_oldman_walk.png', 816, 1316, {seed: 3, amp: 0.3});
const bas = Rig.figure(q('sc15-basket'), 'assets/chars/res_basket_walk.png', 852, 1348, {seed: 5, amp: 0.3});
const sa = Rig.make(q('sc15-salem'), 'salem_side', {seed: 7});
const mf = Rig.make(q('sc15-mfather'), 'father_side', {seed: 1, armLayer: q('sc15-mfarm')});
const ms = Rig.make(q('sc15-msalem'), 'salem_side', {seed: 9});
const back = Rig.figure(q('sc15-back'), 'assets/chars/salem_back.png', 304, 708, {seed: 8, amp: 0.4});
const fa = Rig.make(q('sc15-father'), 'father_side', {seed: 3});
const cam = Rig.camera(q('sc15-cam'));
const M0 = at(114.75), M1 = at(117.6);
const mem = T([[0,0],[M0,0],[M0 + 0.35,1],[M1 - 0.35,1],[M1,0]]);
const mArm = T([[0,0],[at(113.1),0],[at(113.5),1],[at(114.4),1],[at(114.8),0]]);
const fx = T([[0,2080],[at(121.2),2080],[at(123.4),1260,'out']]);
const fset = T([[0,0],[at(123.3),0],[at(123.75),1]]);
const fHead = T([[0,0],[at(123.6),0],[at(124.1),8],[at(124.8),6]]);
Rig.drive(tl, DUR, (t) => {
  const memory = t >= M0 && t < M1;
  const later = t >= M1;
  if (!later) cam.render({cx: 980 - t * 10, cy: 540, z: 1.05});
  else cam.render({cx: 960, cy: 560 - (t - M1) * 4, z: 1.0 + (t - M1) * 0.02});
  // people at the door; Marian welcomes them in
  const m = mArm(t);
  ma.render({t, x: 900, y: 692, h: 118, dir: 1, d: 0, settle: 1, arm: [Rig.lerp(0, -70, m), Rig.lerp(0, -30, m)], head: -4 * m, op: later ? 0 : 1});
  wo.render({t, x: 965, y: 698, h: 128, dir: -1, op: later ? 0 : 1});
  gi.render({t, x: 1005, y: 700, h: 131, dir: -1, op: later ? 0 : 1});
  old.render({t, x: 760, y: 722, h: 167, dir: 1});
  bas.render({t, x: 1460, y: 735, h: 188, dir: -1, op: later ? 0 : 1});
  sa.render({t, x: 1780 - t * 150, x0: 1780, y: 990, h: 600, dir: -1, op: (memory || later) ? 0 : 1});
  q('sc15-memory').style.opacity = mem(t);
  if (memory) {
    handWalk(t - M0, mf, ms, 1250, 860, 420, 100, {op: 1});
  } else { mf.render({t, x: -500, y: 0, h: 10, op: 0}); ms.render({t, x: -500, y: 0, h: 10, op: 0}); }
  back.render({t, x: 900, y: 1070, h: 700, dir: 1, op: later ? 1 : 0});
  fa.render({t, x: fx(t), x0: 2080, y: 1070, h: 700, dir: -1, settle: fset(t), head: fHead(t), op: later ? 1 : 0});
});
""",
      overlay='<div id="sc15-memory" class="grade" style="z-index:25;background:radial-gradient(ellipse at 50% 55%,rgba(255,230,190,0) 30%,rgba(255,224,170,.55) 75%,rgba(250,236,210,.9) 100%)"></div>')

# ------------------------------------------------------------------ sc16 historical narration
scene("sc16", 127.0, 17.6, "01_hospital_exterior",
      [rig("sc16-pat", 9), rig("sc16-marian", 9), rig("sc16-old", 10), rig("sc16-mom", 10), rig("sc16-woman", 11), rig("sc16-girl", 11)],
      r"""
const pat = Rig.make(q('sc16-pat'), 'pat_q34', {seed: 2});
const ma = Rig.figure(q('sc16-marian'), 'assets/chars/marian_front.png', 648, 1644, {seed: 7, amp: 0.4});
const old = Rig.figure(q('sc16-old'), 'assets/chars/res_oldman_walk.png', 816, 1316, {seed: 4, amp: 0.3});
const mom = Rig.figure(q('sc16-mom'), 'assets/chars/res_mombaby_stand.png', 592, 1328, {seed: 3, amp: 0.8});
const wo = Rig.figure(q('sc16-woman'), 'assets/chars/res_woman_stand.png', 528, 1304, {seed: 5});
const gi = Rig.figure(q('sc16-girl'), 'assets/chars/res_girl_stand.png', 512, 1204, {seed: 6});
const cam = Rig.camera(q('sc16-cam'));
// archive photos on the narration: Sheikh Zayed with the Kennedys from «في العين سنة ١٩٦٠… قدّم الشيخ زايد»,
// Dr Pat on «بإشراف الدكتور بات كينيدي», Dr Marian on «وزوجته الدكتورة ماريان كينيدي»,
// then back to the house for «من هالبيت بدأت حكاية مستشفى الواحة… المعروف اليوم بمستشفى كند».
const P1 = at(124.0), P2 = at(130.0), P3 = at(133.6), P4 = at(136.15) + 0.5;
const X = 0.45;
const layer = T([[0,1],[P4 - X,1],[P4,0]]);
const ph1 = T([[0,1],[P2 - X,1],[P2,0]]);
const ph2 = T([[0,0],[P2 - X,0],[P2,1],[P3 - X,1],[P3,0]]);
const ph3 = T([[0,0],[P3 - X,0],[P3,1]]);
const cap1 = T([[0,0],[0.6,0],[1.3,1],[P2 - X,1],[P2,0]]);
const cap2 = T([[0,0],[P2 + 0.1,0],[P2 + 0.45,1],[P3 - X,1],[P3,0]]);
const cap3 = T([[0,0],[P3 + 0.1,0],[P3 + 0.45,1]]);
const kb = (t, t0, t1) => 1 + 0.045 * Rig.clamp((t - t0) / (t1 - t0), 0, 1);
const z = T([[0,1.3],[P4,1.3],[DUR,1.0,'io']]), cx = T([[0,900],[P4,900],[DUR,960,'io']]), cy = T([[0,600],[P4,600],[DUR,540,'io']]);
const fade = T([[0,0],[DUR - 1,0],[DUR,1]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: cx(t), cy: cy(t), z: z(t)});
  // people at the old house, sized to the building and standing on open ground
  pat.render({t, x: 815, y: 692, h: 118, dir: 1});
  ma.render({t, x: 905, y: 692, h: 118, dir: -1});
  mom.render({t, x: 1010, y: 700, h: 131, dir: -1});
  old.render({t, x: 420, y: 760, h: 228, dir: 1});
  wo.render({t, x: 1560, y: 790, h: 277, dir: -1});
  gi.render({t, x: 1625, y: 794, h: 283, dir: 1});
  q('sc16-photos').style.opacity = layer(t);
  q('sc16-ph1').style.opacity = ph1(t); q('sc16-ph2').style.opacity = ph2(t); q('sc16-ph3').style.opacity = ph3(t);
  q('sc16-ph1-img').style.transform = `scale(${kb(t, 0, P2)})`;
  q('sc16-ph2-img').style.transform = `scale(${kb(t, P2 - X, P3)})`;
  q('sc16-ph3-img').style.transform = `scale(${kb(t, P3 - X, P4)})`;
  q('sc16-cap1').style.opacity = cap1(t); q('sc16-cap2').style.opacity = cap2(t); q('sc16-cap3').style.opacity = cap3(t);
  q('sc16-fade').style.opacity = fade(t);
});
""",
      overlay='<div id="sc16-photos" class="photos">'
              '<div id="sc16-ph1" class="photo"><div class="print"><img id="sc16-ph1-img" src="assets/photos/zayed_kennedys.jpg"></div>'
              '<div id="sc16-cap1" class="cap">الشيخ زايد بن سلطان آل نهيان، رحمه الله<span>مع الدكتور بات كينيدي والدكتورة ماريان كينيدي</span></div></div>'
              '<div id="sc16-ph2" class="photo"><div class="print"><img id="sc16-ph2-img" src="assets/photos/pat_kennedy.jpg"></div>'
              '<div id="sc16-cap2" class="cap">الدكتور بات كينيدي</div></div>'
              '<div id="sc16-ph3" class="photo"><div class="print"><img id="sc16-ph3-img" src="assets/photos/marian_kennedy.jpg"></div>'
              '<div id="sc16-cap3" class="cap">الدكتورة ماريان كينيدي</div></div>'
              '</div>'
              '<div id="sc16-fade" class="grade" style="background:#140e09"></div>')

# ------------------------------------------------------------------ writers
STYLE = """
    @font-face { font-family: "Amiri"; src: url("assets/fonts/Amiri-Bold.ttf"); font-weight: 700; }
    @font-face { font-family: "Amiri"; src: url("assets/fonts/Amiri-Regular.ttf"); font-weight: 400; }
    #root { position: absolute; inset: 0; overflow: hidden; background: #140e09; }
    .stage { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    .bgimg { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    .actor { position: absolute; left: 0; top: 0; }
    .prop { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
    .grade { position: absolute; inset: 0; pointer-events: none; z-index: 40; }
    .title { position: absolute; left: 0; right: 0; top: 150px; text-align: center; direction: rtl; z-index: 50;
      font-family: "Amiri", serif; font-weight: 700; font-size: 104px; color: #fff6e6;
      text-shadow: 0 3px 18px rgba(60,30,10,.55), 0 1px 2px rgba(60,30,10,.6); }
    .place { position: absolute; right: 150px; bottom: 120px; direction: rtl; z-index: 50;
      font-family: "Amiri", serif; font-weight: 700; font-size: 54px; color: #fff6e6; text-shadow: 0 2px 12px rgba(40,20,5,.6); }
    .photos { position: absolute; inset: 0; z-index: 45; background: radial-gradient(ellipse at 50% 45%, #2a1e13 0%, #160f09 75%); }
    .photo { position: absolute; inset: 0; }
    .print { position: absolute; left: 448px; top: 120px; width: 1024px; height: 576px; overflow: hidden;
      outline: 10px solid #efe4cf; box-shadow: 0 18px 50px rgba(0,0,0,.55); }
    .print img { width: 1024px; height: 576px; display: block; transform-origin: 50% 50%; }
    .cap { position: absolute; left: 160px; right: 160px; top: 760px; text-align: center; direction: rtl;
      font-family: "Amiri", serif; font-weight: 700; font-size: 52px; line-height: 1.5; color: #f3e7d0; }
    .cap span { display: block; font-weight: 400; font-size: 38px; color: #d9c8a8; }
    .disc { position: absolute; left: 0; right: 0; bottom: 0; padding: 90px 220px 58px; text-align: center; direction: rtl; z-index: 50;
      font-family: "Amiri", serif; font-weight: 700; font-size: 40px; line-height: 1.6; color: #fff6e6;
      background: linear-gradient(180deg, rgba(20,12,6,0) 0%, rgba(20,12,6,.74) 58%); text-shadow: 0 2px 8px rgba(20,10,4,.75); }
    .card { position: absolute; left: 260px; right: 260px; top: 420px; text-align: center; direction: rtl; z-index: 50;
      font-family: "Amiri", serif; font-weight: 400; font-size: 54px; line-height: 1.75; color: #f1e4cc; }
"""


def write_scene(s):
    sid = s["id"]
    bg = f'<img id="{sid}-bg" class="bgimg" src="assets/bg/{s["bg"]}.png">' if s["bg"] else ""
    els = "\n        ".join(s["els"])
    html = f"""<template>
  <style>{STYLE}  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div id="{sid}-wrap" class="clip" data-start="0" data-duration="{s['dur']}" data-layout-allow-overflow data-layout-allow-overlap style="position:absolute;inset:0">
      <div id="{sid}-cam" class="stage">
        {bg}
        {els}
      </div>
      {s['overlay']}
    </div>
  </div>
  <script>
  (function () {{
    const q = (i) => document.getElementById(i);
    const T = Rig.track;
    const DUR = {s['dur']};
    // voice time (seconds into voice.mp3) -> scene time
    const W = {WARP_JS};
    const warp = (a) => {{ if (a <= W[0][0]) return a; for (let i = 1; i < W.length; i++) if (a <= W[i][0]) return W[i-1][1] + (W[i][1] - W[i-1][1]) * (a - W[i-1][0]) / (W[i][0] - W[i-1][0]); return W[W.length-1][1] + a - W[W.length-1][0]; }};
    const at = (a) => warp(a) + {VO} - {s['start']};
    const tl = gsap.timeline({{ paused: true }});
{s['js']}
    window.__timelines["{sid}"] = tl;
  }})();
  </script>
</template>
"""
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(html)


def write_index():
    total = round(SCENES[-1]["start"] + SCENES[-1]["dur"], 3)
    hosts = "\n      ".join(
        f'<div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
        f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="1" data-track-kind="graphics" '
        f'data-width="1920" data-height="1080" style="z-index:2"></div>' for s in SCENES)
    amb = json.load(open(os.path.join(OUT, "tools", "ambience.json"))) if os.path.exists(os.path.join(OUT, "tools", "ambience.json")) else []
    # the sickle's bites on the trunk: same stroke maths as PALM_FATHER (CYC, bite at 0.72 of a stroke)
    CYC = 1.15
    takes = [("rpg_chop.mp3", 0.053, 0.24), ("impact_wood_light_001.mp3", 0.001, 0.26), ("impact_wood_light_003.mp3", 0.001, 0.26)]
    n = 0
    for sid, stop_old in (("sc03", 17.95), ("sc14", 102.85)):
        st = next(x for x in SCENES if x["id"] == sid)["start"]
        tstop = warp(stop_old) + VO - st
        k = 0
        while tstop - (0.78 + k) * CYC > 0.05:
            f, peak, dur = takes[n % 3]
            amb.append(dict(id=f"sfx-cut{n + 1}", file=f, abs=round(st + tstop - (0.78 + k) * CYC - peak + 1 / 24, 3), dur=dur, vol=0.3, fin=0, fout=0.05))
            n += 1
            k += 1
    audio = "\n      ".join(
        f'<audio id="{a["id"]}" src="assets/sfx/{a["file"]}" data-start="{a['abs'] if 'abs' in a else round(g(a['start']), 3)}" data-duration="{a["dur"]}" '
        f'data-volume="{a["vol"]}" data-fade-in="{a.get("fin", 0.4)}" data-fade-out="{a.get("fout", 0.6)}" data-track-index="{3 + i % 2}"></audio>'
        for i, a in enumerate(amb))
    html = f"""<!doctype html>
<html lang="ar" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>البيت اللي صار مستشفى</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <script src="assets/rigs.js"></script>
    <script src="assets/rig.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #140e09; }}
      #film-ground {{ position: absolute; inset: 0; background: #140e09; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-fps="24" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
      <div id="film-ground" class="clip" data-start="0" data-duration="{total}" data-track-index="0" style="z-index:1"></div>
      {hosts}
      <audio id="voice" src="assets/audio/voice.wav" data-start="{VO}" data-volume="1" data-track-index="2"></audio>
      {audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(OUT, "index.html"), "w").write(html)
    return total


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    # contiguous slots: each scene runs until the next one starts; the last one ends just after the voice
    for a, b in zip(SCENES, SCENES[1:]):
        a["dur"] = round(b["start"] - a["start"], 3)
    SCENES[-1]["dur"] = round(END_VOICE + 1.3 - SCENES[-1]["start"], 3)
    for s in SCENES:
        write_scene(s)
    total = write_index()
    # timing sheet
    rows = [f"| {s['id']} | {s['start']:.2f} | {s['start'] + s['dur']:.2f} | {s['bg'] or '—'} |" for s in SCENES]
    print(f"{len(SCENES)} scenes, total {total}s")
