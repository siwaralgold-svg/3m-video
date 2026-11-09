#!/usr/bin/env python3
"""Writes compositions/*.html and index.html for «البيت اللي صار مستشفى».

Each scene is timed against the recorded voice (assets/audio/voice.mp3).
Inside a scene, `at(a)` turns a voice time (seconds into voice.mp3) into scene time.
The voice starts at film time VO = 3.0 s, after the title.
Run:  python3 tools/build_scenes.py   (from the project folder)
"""
import json, os

VO = 3.0
END = 141.09 + VO  # voice ends
OUT = os.path.join(os.path.dirname(__file__), "..")

SCENES = []


def scene(sid, start, dur, bg, els, js, overlay=""):
    SCENES.append(dict(id=sid, start=round(start, 3), dur=round(dur, 3), bg=bg, els=els, js=js, overlay=overlay))


def rig(name, z, cls="actor"):
    return f'<div id="{name}" class="{cls}" style="z-index:{z}"></div>'


def img(name, src, z, style=""):
    return f'<img id="{name}" class="prop" src="assets/{src}" style="z-index:{z};{style}">'


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
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: cx(t), cy: cy(t), z: cz(t)});
  salem.render({t, x: 1120, y: 905, h: 560, dir: 1, head: head(t), lean: lean(t), arm: [arm(t), 0]});
  q('sc01-title').style.opacity = tOp(t);
  q('sc01-title').style.transform = `translateY(${tY(t)}px)`;
  q('sc01-dawn').style.opacity = glow(t);
});
""",
      overlay='<div id="sc01-dawn" class="grade" style="background:linear-gradient(180deg,rgba(255,196,120,.55),rgba(120,70,40,.25))"></div>'
              '<div id="sc01-title" class="title">البيت اللي صار مستشفى</div>')

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
const sx = T([[0,1560],[3.51,860,'lin']]);
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
function hoeArm(t, on) {
  // chop cycle: raise forward-up, strike down; on = 0..1 blend
  const c = ((t % 1.35) / 1.35);
  const up = c < 0.55 ? Rig.smooth(c / 0.55) : 1 - Rig.smooth((c - 0.55) / 0.45);
  return [Rig.lerp(-12, Rig.lerp(-32, -118, up), on), Rig.lerp(-8, Rig.lerp(-28, -10, up), on)];
}
"""
scene("sc03", 16.25, 7.85, "05_palm_garden",
      [rig("sc03-father", 20), img("sc03-hoe", "props/env_hoe.png", 21, "width:436px;height:816px"), rig("sc03-salem", 25)],
      PALM_FATHER + r"""
const fa = Rig.make(q('sc03-father'), 'father_side', {seed: 2});
const sa = Rig.make(q('sc03-salem'), 'salem_side', {seed: 7});
const cam = Rig.camera(q('sc03-cam'));
const work = T([[0,1],[at(18.0),1],[at(18.5),0]]);
const head = T([[0,7],[at(18.0),7],[at(18.45),-2],[at(19.5),-4],[at(19.9),3],[at(20.3),-3],[at(20.9),0]]);
const lean = T([[0,5],[at(18.0),5],[at(18.6),-3],[at(20.9),-1]]);
const far = T([[0,0],[at(19.1),0],[at(19.65),-150,'out'],[at(20.6),-145],[at(21.0),-40]]);
const farEl = T([[0,0],[at(19.1),0],[at(19.65),-10],[at(21.0),-20]]);
const sx = T([[0,-160],[at(15.4),-160],[at(18.25),640,'lin']]);
const sset = T([[0,0],[at(18.25),0],[at(18.75),1]]);
const sHead = T([[0,0],[at(18.8),0],[at(19.4),-6],[at(21),-4]]);
const cut = at(18.6);
Rig.drive(tl, DUR, (t) => {
  if (t < cut) cam.render({cx: 980 + t * 10, cy: 560, z: 1.02});
  else cam.render({cx: 1060 + (t - cut) * 6, cy: 560, z: 1.42 + (t - cut) * 0.01});
  const w = work(t);
  const st = {t, x: 1330, y: 930, h: 600, dir: -1, d: 0, settle: 1, head: head(t), lean: lean(t) * (0.5 + 0.5 * w),
              arm: hoeArm(t, w), farArm: [far(t), farEl(t)], idle: 1 - w};
  fa.render(st);
  Rig.attach(q('sc03-hoe'), fa, 0, {grip: [335, 215], rot: -18, scale: 0.66, dy: 30});
  sa.render({t, x: sx(t), x0: -160, y: 965, h: 600, dir: 1, settle: sset(t), head: sHead(t)});
});
""")

# ------------------------------------------------------------------ sc04 interior: the morning he did not get up
scene("sc04", 24.1, 12.9, "04_salem_home_interior",
      [rig("sc04-father", 14), div("sc04-blanket", 16, "left:0;top:0;width:620px;height:120px;transform-origin:0 0",
                                   '<svg width="620" height="120" viewBox="0 0 620 120"><path d="M8 40 Q40 8 120 14 L560 18 Q612 22 612 70 L610 110 L10 110 Q2 80 8 40 Z" fill="#7a4f33" stroke="#5c3a24" stroke-width="3"/>'
                                   '<path d="M440 18 L452 110 M470 19 L482 110" stroke="#e7d6b8" stroke-width="7" opacity=".85"/><path d="M60 40 Q300 30 600 46" stroke="#5c3a24" stroke-width="2" fill="none" opacity=".5"/></svg>'),
       rig("sc04-salemw", 20), rig("sc04-salem", 20)],
      r"""
const fa = Rig.make(q('sc04-father'), 'father_side', {seed: 9});
const sw = Rig.make(q('sc04-salemw'), 'salem_side', {seed: 4});
const ss = Rig.make(q('sc04-salem'), 'salem_q34', {seed: 6, lap: {y: 430}});
const cam = Rig.camera(q('sc04-cam'));
const sun = T([[0,0.05],[at(22.9),0.05],[at(24.1),0.85]]);
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
  q('sc04-blanket').style.transform = `translate(${p.x - 24}px, ${p.y - 46}px) scale(0.66, 0.85)`;
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
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] + 18, un.R.arms[0].shoulder[1] + 6);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, -1);
  fa.render(fst);
  sw.render({t, x: swx(t), x0: 1330, y: 806, h: 470, dir: -1, op: t >= at(43.9) ? 1 : 0});
});
""")

# ------------------------------------------------------------------ sc06 lane: walking through the neighbourhood
scene("sc06", 47.0, 1.4, "02_neighborhood_lane",
      [rig("sc06-father", 20), div("sc06-farm", 23, "left:0;top:0"), rig("sc06-uncle", 22), rig("sc06-salem", 24),
       rig("sc06-old", 10), rig("sc06-woman", 11)],
      r"""
const fa = Rig.make(q('sc06-father'), 'father_side', {seed: 1, armLayer: q('sc06-farm')});
const un = Rig.make(q('sc06-uncle'), 'uncle_side', {seed: 3});
const sw = Rig.make(q('sc06-salem'), 'salem_side', {seed: 5});
const old = Rig.figure(q('sc06-old'), 'assets/chars/res_oldman_walk.png', 816, 1316, {seed: 4, amp: 0.3});
const wo = Rig.figure(q('sc06-woman'), 'assets/chars/res_woman_walk.png', 748, 1300, {seed: 9, amp: 0.2});
const cam = Rig.camera(q('sc06-cam'));
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 980 - t * 30, cy: 560, z: 1.05});
  const ex = 1250 - t * 120;
  const ust = {t, x: ex, x0: 1250, y: 960, h: 600, dir: -1, swing: 0.6};
  const fst = {t, x: ex + 105, x0: 1355, y: 930, h: 588, dir: -1, head: 9, lean: 5, swing: 0.2};
  un.render(ust);
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] + 18, un.R.arms[0].shoulder[1] + 6);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, -1);
  fa.render(fst);
  sw.render({t, x: 1620 - t * 120, x0: 1620, y: 985, h: 600, dir: -1});
  old.render({t, x: 520, y: 770, h: 250, dir: 1});
  wo.render({t, x: 1500, y: 745, h: 230, dir: -1, rot: 1});
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
const ux = T([[0,1560],[stop,1270,'out'],[at(52.05),1270],[7.2,1130,'in']]);
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
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] + 18, un.R.arms[0].shoulder[1] + 6);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, -1);
  fa.render(fst);
  const walking = t < stop + 0.45 || t >= goT;
  const swst = {t, x: t < goT ? sx(t) : 1060 - (t - goT) * 140, y: 990, h: 600, dir: -1, op: walking ? 1 : 0};
  swst.x0 = t < goT ? 1330 : 1060; swst.settle = t < goT ? sset(t) : 0;
  sw.render(swst);
  const p = sPoint(t);
  sq.render({t, x: 1060, y: 990, h: 600, dir: sDir(t), head: sHead(t), dy: sDy(t), op: walking ? 0 : 1,
             arm: [Rig.lerp(0, -118, p), Rig.lerp(0, -12, p)]});
  wo.render({t, x: 640, y: 712, h: 190, dir: 1});
  gi.render({t, x: 690, y: 716, h: 190, dir: -1});
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
  const sh = Rig.pt(un, ust, un.R.arms[0].shoulder[0] + 18, un.R.arms[0].shoulder[1] + 6);
  fst.arm = Rig.reach(fa, fst, 0, sh.x, sh.y, -1);
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
       img("sc09-stetho-in", "props/prop_stetho.png", 11, "width:1272px;height:1344px"),
       rig("sc09-marian", 14), rig("sc09-father", 16), rig("sc09-pat", 18),
       img("sc09-stetho", "props/prop_stetho.png", 19, "width:1272px;height:1344px"),
       '<svg id="sc09-tube" style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible;z-index:19"><path id="sc09-tube-p" d="" fill="none" stroke="#2c2a2a" stroke-width="5" stroke-linecap="round"/><circle id="sc09-bell" r="11" fill="#c9cdd1" stroke="#6d7277" stroke-width="3"/></svg>',
       rig("sc09-uncle", 22), rig("sc09-salem", 24), div("sc09-farm", 26, "left:0;top:0")],
      r"""
const fa = Rig.make(q('sc09-father'), 'father_front', {seed: 3, armLayer: q('sc09-farm')});
const pat = Rig.make(q('sc09-pat'), 'pat_q34', {seed: 5});
const ma = Rig.figure(q('sc09-marian'), 'assets/chars/marian_front.png', 648, 1644, {seed: 2, amp: 0.4});
const un = Rig.make(q('sc09-uncle'), 'uncle_q34', {seed: 6});
const sa = Rig.make(q('sc09-salem'), 'salem_q34', {seed: 9});
const cam = Rig.camera(q('sc09-cam'));
const place = (id, x, y, w, op) => { const e = q(id); e.style.transformOrigin = '0 0'; e.style.transform = `translate(${x}px,${y}px) scale(${w / e.width})`; e.style.opacity = op; };
// shot cuts (scene time)
const S2 = at(65.95), S3 = at(68.5), S4a = at(72.95), S4b = at(74.3), S5 = at(78.7), S6 = at(85.05);
// --- shot 1: Pat at the desk opens the bag and lifts the stethoscope
const open = T([[0,0],[at(63.1),0],[at(63.5),1]]);
const p1 = T([[0,0],[at(62.95),0.25],[at(63.2),1],[at(63.6),0.5],[at(64.2),1],[at(64.7),1],[at(65.4),0.15]]);
const lifted = (t) => t >= at(64.6);
// --- shot 2: to the chest
const toChest = T([[0,0],[at(66.0),0],[at(66.9),1,'out'],[at(78.6),1],[at(79.4),0]]);
const reposition = T([[0,0],[at(76.6),0],[at(77.0),1],[at(77.4),0]]);
// --- shot 3: whisper
const sLean = T([[0,0],[at(68.6),0],[at(69.3),9],[at(70.7),11],[at(71.4),7],[at(72.4),3]]);
const sDy = T([[0,0],[at(69.0),0],[at(69.3),-10],[at(71.5),-10],[at(71.9),0]]);
const sHead = T([[0,0],[at(70.6),0],[at(70.85),-12],[at(71.4),-6],[at(72.9),-2]]);
const uHead = T([[0,0],[at(71.3),0],[at(71.6),10],[at(72.5),8],[at(73.0),2]]);
const uArm = T([[0,0],[at(71.5),0],[at(71.9),-28],[at(72.6),-30],[at(73.2),0]]);
// --- shot 5: watching
const s5lean = (t) => Rig.wob(t, 4, 2.3, 2.2);
const s5head = T([[0,-6],[at(81.3),-6],[at(81.7),-11],[at(83.0),-9],[at(83.6),-13],[at(85),-9]]);
const patNod = T([[0,0],[at(81.6),0],[at(81.85),6],[at(82.1),0],[at(82.35),5],[at(82.7),0]]);
// --- shot 6: the hand
const hand = T([[0,0],[at(86.35),0],[at(87.35),1,'io']]);
const fNod = T([[0,0],[at(87.9),0],[at(88.25),7],[at(88.55),1],[at(88.85),6],[at(89.6),2]]);
const fLean = T([[0,0],[at(87.9),0],[at(88.6),-4],[at(89.6),-3]]);
const salHand = T([[0,0],[at(86.5),0],[at(87.2),1]]);
Rig.drive(tl, DUR, (t) => {
  const shot = t < S2 ? 1 : t < S3 ? 2 : t < S4a ? 3 : t < S4b ? 4 : t < S5 ? 5 : t < S6 ? 6 : 7;
  if (shot === 1) cam.render({cx: 640, cy: 520, z: 1.8 + t * 0.02});
  else if (shot === 2) cam.render({cx: 1480, cy: 520, z: 1.55});
  else if (shot === 3) cam.render({cx: 960, cy: 560, z: 1.02});
  else if (shot === 4) cam.render({cx: 600, cy: 600, z: 2.0});
  else if (shot === 5) { const c = Rig.pt(fa, {x: 1660, y: 860, h: 610, dir: -1}, 202, 330); cam.render({cx: c.x - 60, cy: c.y + 10, z: 3.0 + (t - S4b) * 0.03}); }
  else if (shot === 6) cam.render({cx: 1350, cy: 540, z: 1.45});
  else cam.render({cx: 1420, cy: 560, z: 1.6 + (t - S6) * 0.01});
  // father seated on the bed edge, facing camera (mirrored so his free arm is toward Salem)
  const fst = {t, x: 1660, y: 860, h: 610, dir: -1, head: fNod(t), lean: fLean(t), idle: 0.6};
  // Pat: at the desk in shot 1 (facing the bag), at the bed afterwards
  const pst = shot === 1 ? {t, x: 760, y: 900, h: 640, dir: -1} : {t, x: 1475, y: 905, h: 640, dir: 1, head: patNod(t)};
  // bag on the desk
  place('sc09-bagc', 412, 432, 165, open(t) < 0.5 ? 1 : 0);
  place('sc09-bago', 418, 414, 154, open(t) >= 0.5 ? 1 : 0);
  place('sc09-stetho-in', 466, 432, 66, open(t) >= 0.5 && !lifted(t) ? 1 : 0);
  if (shot === 1) {
    const bagPt = {x: 500, y: 470};
    const restA = [0, -6];
    const ra = Rig.reach(pat, pst, 0, bagPt.x + 40, bagPt.y - 10, 1);
    const up = Rig.reach(pat, pst, 0, 690, 380, 1);
    const u = p1(t);
    pst.arm = t < at(64.7) ? Rig.mixArm(restA, ra, Rig.smooth(Math.min(1, u))) : Rig.mixArm(up, ra, Rig.smooth(u));
    pst.idle = 0.2;
  } else {
    const chest = Rig.pt(fa, fst, 202, 330);
    const target = {x: chest.x - 20 + reposition(t) * 18, y: chest.y + 16 - reposition(t) * 22};
    const ra = Rig.reach(pat, pst, 0, target.x - 38, target.y + 4, 1);
    pst.arm = Rig.mixArm([0, -6], ra, Rig.smooth(toChest(t)));
    pst.idle = 0.2;
  }
  pat.render(pst);
  fst.arm = [0, 0];
  // the hand: both hands meet at one point between them
  const sst7 = {x: 1545, y: 912, h: 640, dir: 1};
  const fS = Rig.pt(fa, fst, fa.R.arms[0].shoulder[0], fa.R.arms[0].shoulder[1]);
  const sS = Rig.pt(sa, sst7, sa.R.arms[0].shoulder[0], sa.R.arms[0].shoulder[1]);
  const fC = Rig.pt(fa, fst, fa.R.arms[0].cuff[0], fa.R.arms[0].cuff[1]);
  const Lf = Math.hypot(fC.x - fS.x, fC.y - fS.y) * 0.97;
  // father's hand only eases toward Salem; Salem lifts his hand into it
  const meet = {x: Rig.lerp(fC.x, sS.x, 0.22), y: fC.y + 8};
  if (shot === 7) {
    fst.arm = Rig.mixArm([0, 0], Rig.reach(fa, fst, 0, meet.x, meet.y, 1), Rig.smooth(hand(t)));
    fst.idle = 0;
  }
  fa.render(fst);
  // stethoscope: dangling in hand after lifting (shot 1), on the chest afterwards
  const hw = pat.handWorld(0);
  const inHand = shot === 1 && lifted(t);
  q('sc09-stetho').style.opacity = inHand ? 1 : 0;
  if (inHand) Rig.attach(q('sc09-stetho'), pat, 0, {grip: [330, 120], rot: 0, scale: 0.42, dy: 60});
  const onChest = shot >= 2 && shot !== 4 && toChest(t) > 0.02;
  const tube = q('sc09-tube');
  tube.style.opacity = onChest ? 1 : 0;
  if (onChest) {
    const ar = hw.ang * Math.PI / 180;
    const bx = hw.x - Math.sin(ar) * 62 * hw.sc * hw.dir, by = hw.y + Math.cos(ar) * 62 * hw.sc;
    const neck = Rig.pt(pat, pst, pat.R.head.pivot[0] + 6, pat.R.head.pivot[1] + 30);
    q('sc09-bell').setAttribute('cx', bx); q('sc09-bell').setAttribute('cy', by);
    q('sc09-tube-p').setAttribute('d', `M ${bx} ${by} C ${bx - 30} ${by + 120}, ${neck.x + 40} ${neck.y + 160}, ${neck.x + 8} ${neck.y + 20} M ${neck.x + 8} ${neck.y + 20} L ${neck.x - 10} ${neck.y - 8} M ${neck.x + 8} ${neck.y + 20} L ${neck.x + 26} ${neck.y - 6}`);
  }
  ma.render({t, x: 1880, y: 840, h: 640, dir: -1});
  // uncle + Salem by the door
  const uDir = 1;
  const ust = (shot === 7 || shot === 1) ? {t, x: 980, y: 930, h: 640, dir: uDir, op: 0} : {t, x: 470, y: 960, h: 640, dir: uDir, head: uHead(t), arm: [uArm(t), -10]};
  un.render(ust);
  let sst;
  if (shot <= 3) sst = {t, x: 640, y: 975, h: 640, dir: -1, lean: sLean(t), dy: sDy(t), head: sHead(t), op: shot === 1 ? 0 : 1};
  else if (shot === 4) sst = {t, x: 640, y: 975, h: 640, dir: 1, head: T([[S4a,-2],[S4a+0.5,-9]])(t)};
  else if (shot === 5) sst = {t, x: 1210, y: 975, h: 640, dir: 1, op: 0};
  else if (shot === 6) sst = {t, x: 1150, y: 980, h: 640, dir: 1, lean: s5lean(t), head: s5head(t), arm: [Rig.wob(t, 2, 1.7, 6), -10]};
  else sst = Object.assign({t, head: -8, idle: 0}, sst7);
  if (shot === 7) sst.arm = Rig.mixArm([0, 0], Rig.reach(sa, sst, 0, meet.x - 4, meet.y + 26, 1), Rig.smooth(salHand(t)));
  sa.render(sst);
});
""")

# ------------------------------------------------------------------ sc10 lane: walking home hand in hand
HAND_WALK = r"""
function handWalk(t, fa, sa, x0, y, h, v, extra) {
  const fx = x0 + 110 - t * v, sx = x0 - t * v;
  const sst = Object.assign({t, x: sx, x0: x0, y: y + 14, h, dir: -1, swing: 0.4}, extra || {});
  sst.farArm = [-22, -18];
  sa.render(sst);
  const hw = sa.handWorld('far');
  const fst = Object.assign({t, x: fx, x0: x0 + 110, y, h: h * 0.98, dir: -1, swing: 0.3}, extra || {});
  fst.arm = Rig.reach(fa, fst, 0, hw.x + 26, hw.y - 18, -1);
  fa.render(fst);
}
"""
scene("sc10", 92.6, 2.9, "02_neighborhood_lane",
      [rig("sc10-father", 20), rig("sc10-salem", 24), rig("sc10-girl", 10)],
      HAND_WALK + r"""
const fa = Rig.make(q('sc10-father'), 'father_side', {seed: 2});
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
      [rig("sc11-father", 20), rig("sc11-salem", 24)],
      HAND_WALK + r"""
const fa = Rig.make(q('sc11-father'), 'father_side', {seed: 4});
const sa = Rig.make(q('sc11-salem'), 'salem_side', {seed: 8});
const cam = Rig.camera(q('sc11-cam'));
// day -> dusk -> night -> dawn
const dusk = T([[0,0],[1.3,0],[2.0,0.75],[2.6,0.2],[3.3,0]]);
const night = T([[0,0],[1.7,0],[2.3,0.72],[2.9,0.72],[3.6,0]]);
const dawn = T([[0,0],[2.9,0],[3.5,0.6],[4.4,0.35]]);
const walkOp = T([[0,1],[1.4,1],[1.9,0]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 960, cy: 540, z: 1.0 + t * 0.01});
  q('sc11-dusk').style.opacity = dusk(t); q('sc11-night').style.opacity = night(t); q('sc11-dawn').style.opacity = dawn(t);
  handWalk(t, fa, sa, 1500, 840, 400, 120, {op: walkOp(t)});
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
      [rig("sc13-salem", 20), rig("sc13-mother", 10)],
      r"""
const sa = Rig.make(q('sc13-salem'), 'salem_side', {seed: 5});
const mo = Rig.make(q('sc13-mother'), 'mother_q34', {seed: 2});
const cam = Rig.camera(q('sc13-cam'));
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: 1140 - t * 220, cy: 560, z: 1.12});
  sa.render({t, x: 1430 - t * 560, x0: 1430, y: 840, h: 560, dir: -1, run: 1});
  mo.render({t, x: 330, y: 885, h: 560, dir: 1, head: -4});
});
""")

# ------------------------------------------------------------------ sc14 palms: reunion
scene("sc14", 104.4, 9.1, "05_palm_garden",
      [rig("sc14-father", 20), img("sc14-hoe", "props/env_hoe.png", 21, "width:436px;height:816px"), rig("sc14-salem", 25)],
      PALM_FATHER + r"""
const fa = Rig.make(q('sc14-father'), 'father_side', {seed: 2});
const sa = Rig.make(q('sc14-salem'), 'salem_side', {seed: 7});
const cam = Rig.camera(q('sc14-cam'));
const work = T([[0,1],[at(102.85),1],[at(103.2),0]]);
const head = T([[0,10],[at(102.9),10],[at(103.4),-3,'out'],[at(103.8),1],[at(104.1),-4],[at(104.6),-3],
                [at(105.4),3],[at(105.7),-3],[at(106.7),0],[at(108),2]]);
const lean = T([[0,6],[at(102.9),6],[at(103.4),-3],[at(103.75),-1],[at(104.05),-4],[at(106.8),-1]]);
const dy = T([[0,0],[at(103.5),0],[at(103.7),-8],[at(103.95),0]]);
const far = T([[0,0],[at(104.9),0],[at(105.45),-150,'out'],[at(106.5),-145],[at(106.9),-30]]);
const sx = T([[0,-200],[at(102.4),560,'out'],[at(107.6),560],[at(108.9),1090]]);
const srun = (t) => t < at(102.5) ? 1 : 0;
const sset = T([[0,0],[at(102.3),0],[at(102.75),1],[at(107.6),1],[at(107.9),0],[at(108.8),0],[at(109.2),1]]);
const drop = at(107.0);
const onShoulder = T([[0,0],[at(109.0),0],[at(109.8),1]]);
const sHead = T([[0,0],[at(103.5),0],[at(103.9),-8],[at(107.4),-5],[at(109.4),-10],[at(110.5),-7]]);
const sBounce = T([[0,0],[at(109.9),0],[at(110.1),-6],[at(110.3),0],[at(110.5),-4],[at(110.7),0]]);
const c1 = at(104.5), c2 = at(107.2);
let hoeAt = null;
Rig.drive(tl, DUR, (t) => {
  if (t < c1) cam.render({cx: 960 + t * 8, cy: 560, z: 1.02});
  else if (t < c2) cam.render({cx: 1120, cy: 540, z: 1.5});
  else cam.render({cx: 1040 + (t - c2) * 10, cy: 600, z: 1.2});
  const w = work(t);
  const fst = {t, x: 1330, y: 930, h: 600, dir: -1, d: 0, settle: 1, head: head(t), lean: lean(t), dy: dy(t),
               farArm: [far(t), -10], idle: 1 - w};
  const sst = {t, x: sx(t), x0: t < at(103) ? -200 : 560, y: 965, h: 600, dir: 1, run: srun(t), settle: sset(t), head: sHead(t), dy: sBounce(t)};
  sa.render(sst);
  const top = Rig.pt(sa, sst, sa.R.arms[0].shoulder[0] + 6, sa.R.arms[0].shoulder[1] - 4);
  const reachS = Rig.reach(fa, fst, 0, top.x + 20, top.y + 6, 1);
  fst.arm = t < drop ? hoeArm(t, w) : Rig.mixArm([-6, -6], reachS, Rig.smooth(onShoulder(t)));
  fa.render(fst);
  // the hoe: in his hand while he works, leaned on the trunk once he stops
  const hoe = q('sc14-hoe');
  if (t < drop) Rig.attach(hoe, fa, 0, {grip: [335, 215], rot: -18, scale: 0.66, dy: 30});
  else hoe.style.transform = 'translate(1395px, 930px) rotate(-74deg) scale(0.34)';
});
""")

# ------------------------------------------------------------------ sc15 hospital, later: passing by, memory, Salem's back
scene("sc15", 113.5, 13.5, "01_hospital_exterior",
      [rig("sc15-marian", 8), rig("sc15-woman", 9), rig("sc15-girl", 9), rig("sc15-old", 9), rig("sc15-basket", 8),
       rig("sc15-salem", 24), rig("sc15-mfather", 26), rig("sc15-msalem", 27), rig("sc15-back", 30), rig("sc15-father", 29)],
      HAND_WALK + r"""
const ma = Rig.make(q('sc15-marian'), 'marian_side', {seed: 4});
const wo = Rig.figure(q('sc15-woman'), 'assets/chars/res_mombaby_stand.png', 592, 1328, {seed: 2});
const gi = Rig.figure(q('sc15-girl'), 'assets/chars/res_girl_walk.png', 672, 1204, {seed: 6, amp: 0.3});
const old = Rig.figure(q('sc15-old'), 'assets/chars/res_oldman_walk.png', 816, 1316, {seed: 3, amp: 0.3});
const bas = Rig.figure(q('sc15-basket'), 'assets/chars/res_basket_walk.png', 852, 1348, {seed: 5, amp: 0.3});
const sa = Rig.make(q('sc15-salem'), 'salem_side', {seed: 7});
const mf = Rig.make(q('sc15-mfather'), 'father_side', {seed: 1});
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
  ma.render({t, x: 905, y: 690, h: 215, dir: 1, d: 0, settle: 1, arm: [Rig.lerp(0, -70, m), Rig.lerp(0, -30, m)], head: -4 * m, op: later ? 0 : 1});
  wo.render({t, x: 980, y: 694, h: 210, dir: -1, op: later ? 0 : 1});
  gi.render({t, x: 1040, y: 696, h: 210, dir: -1, op: later ? 0 : 1});
  old.render({t, x: 640, y: 706, h: 220, dir: 1});
  bas.render({t, x: 1240, y: 716, h: 230, dir: -1, op: later ? 0 : 1});
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
      [rig("sc16-pat", 9), rig("sc16-marian", 9), rig("sc16-old", 10), rig("sc16-mom", 10), rig("sc16-boy", 11), rig("sc16-basket", 10)],
      r"""
const pat = Rig.make(q('sc16-pat'), 'pat_q34', {seed: 2});
const ma = Rig.figure(q('sc16-marian'), 'assets/chars/marian_front.png', 648, 1644, {seed: 7, amp: 0.4});
const old = Rig.figure(q('sc16-old'), 'assets/chars/res_oldman_sit.png', 820, 1044, {seed: 4, amp: 0.3});
const mom = Rig.figure(q('sc16-mom'), 'assets/chars/res_mombaby_stand.png', 592, 1328, {seed: 3, amp: 0.8});
const boy = Rig.figure(q('sc16-boy'), 'assets/chars/res_boy_stand.png', 504, 1300, {seed: 5});
const bas = Rig.figure(q('sc16-basket'), 'assets/chars/res_basket_stand.png', 752, 1332, {seed: 6});
const cam = Rig.camera(q('sc16-cam'));
const z = T([[0,1.55],[17.6,1.0,'io']]), cx = T([[0,880],[17.6,960,'io']]), cy = T([[0,600],[17.6,540,'io']]);
const place = T([[0,0],[0.4,0],[1.4,1],[6.0,1],[7.0,0]]);
const fade = T([[0,0],[16.6,0],[17.6,1]]);
const patNod = T([[0,0],[at(130.2),0],[at(130.6),5],[at(131.0),0]]);
Rig.drive(tl, DUR, (t) => {
  cam.render({cx: cx(t), cy: cy(t), z: z(t)});
  pat.render({t, x: 800, y: 690, h: 200, dir: 1, head: patNod(t)});
  ma.render({t, x: 950, y: 690, h: 200, dir: -1});
  old.render({t, x: 560, y: 700, h: 220, dir: 1});
  mom.render({t, x: 1080, y: 700, h: 210, dir: -1});
  boy.render({t, x: 1150, y: 704, h: 210, dir: -1});
  bas.render({t, x: 1330, y: 712, h: 220, dir: -1});
  q('sc16-place').style.opacity = place(t);
  q('sc16-fade').style.opacity = fade(t);
});
""",
      overlay='<div id="sc16-place" class="place">العين&nbsp;&nbsp;·&nbsp;&nbsp;١٩٦٠</div>'
              '<div id="sc16-fade" class="grade" style="background:#140e09"></div>')

# ------------------------------------------------------------------ sc17 end card
scene("sc17", 144.6, 6.4, None, [],
      r"""
const op = T([[0,0],[0.4,0],[1.4,1],[5.6,1],[6.35,0]]);
const y = T([[0,10],[1.4,0,'out']]);
Rig.drive(tl, DUR, (t) => {
  q('sc17-card').style.opacity = op(t);
  q('sc17-card').style.transform = `translateY(${y(t)}px)`;
});
""",
      overlay='<div id="sc17-card" class="card">قصة درامية مستوحاة من تأسيس مستشفى الواحة في العين عام ١٩٦٠.<br>سالم وعائلته شخصيات متخيّلة.</div>')


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
    const at = (a) => a + {VO} - {s['start']};
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
    audio = "\n      ".join(
        f'<audio id="{a["id"]}" src="assets/sfx/{a["file"]}" data-start="{a["start"]}" data-duration="{a["dur"]}" '
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
      <audio id="voice" src="assets/audio/voice.mp3" data-start="{VO}" data-volume="1" data-track-index="2"></audio>
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
    for s in SCENES:
        write_scene(s)
    total = write_index()
    # timing sheet
    rows = [f"| {s['id']} | {s['start']:.2f} | {s['start'] + s['dur']:.2f} | {s['bg'] or '—'} |" for s in SCENES]
    print(f"{len(SCENES)} scenes, total {total}s")
