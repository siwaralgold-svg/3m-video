/* Cut-out puppet rig for «البيت اللي صار مستشفى».
 * Every pose is a pure function of a state object, so any frame renders the same on seek.
 * Parts come from assets/rig/<id>/ (built from the reference sheets): body, head, hand<N>.
 * Faces stay blank: no part here draws eyes, nose or mouth.
 */
(function () {
  const RIGS = window.__RIGS; // filled by assets/rigs.js
  const D2R = Math.PI / 180;
  // Height of each figure relative to an adult man (father = 1).
  const REL = {
    salem_side: 0.76, salem_q34: 0.76, salem_back: 0.76, salem_front: 0.76, pat_side: 1.03,
    father_side: 1, father_front: 1, uncle_side: 1, uncle_q34: 1.0,
    mother_q34: 0.97, pat_q34: 1.03, marian_side: 0.98, marian_q34: 0.98,
    res_oldman_walk: 0.93, res_oldman_sit: 0.72, res_basket_stand: 1.0, res_basket_walk: 1.0,
    res_boy_stand: 0.8, res_boy_walk: 0.8, res_mombaby_stand: 0.96, res_mombaby_sit: 0.66,
    res_woman_stand: 0.95, res_woman_walk: 0.95, res_girl_stand: 0.72, res_girl_walk: 0.72,
  };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const smooth = (u) => u * u * (3 - 2 * u);
  const lerp = (a, b, u) => a + (b - a) * u;

  // ---------- keyframe tracks ----------
  const EASE = {
    lin: (u) => u,
    io: (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2),
    in: (u) => u * u,
    out: (u) => 1 - (1 - u) * (1 - u),
    hold: (u) => 0,
    s: smooth,
  };
  // track([[t, v, ease], ...]) -> f(t). ease names the curve INTO that key.
  function track(keys) {
    if (typeof keys === "number") return () => keys;
    return function (t) {
      if (t <= keys[0][0]) return keys[0][1];
      for (let i = 1; i < keys.length; i++) {
        const k = keys[i];
        if (t < k[0]) {
          const p = keys[i - 1];
          const u = (t - p[0]) / (k[0] - p[0] || 1);
          return lerp(p[1], k[1], (EASE[k[2] || "io"])(u));
        }
      }
      return keys[keys.length - 1][1];
    };
  }
  // A deterministic wobble for idle life: sum of two sines, phase from a seed.
  function wob(t, seed, period, amp) {
    const ph = ((seed * 9301 + 49297) % 233280) / 233280;
    return amp * (Math.sin(2 * Math.PI * (t / period + ph)) * 0.7 + Math.sin(2 * Math.PI * (t / (period * 0.53) + ph * 1.7)) * 0.3);
  }

  function el(tag, cls, parent, style) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (style) Object.assign(e.style, style);
    if (parent) parent.appendChild(e);
    return e;
  }
  const SVGNS = "http://www.w3.org/2000/svg";
  function svg(parent, w, h, style) {
    const s = document.createElementNS(SVGNS, "svg");
    s.setAttribute("width", w);
    s.setAttribute("height", h);
    s.setAttribute("viewBox", `0 0 ${w} ${h}`);
    Object.assign(s.style, { position: "absolute", overflow: "visible" }, style || {});
    parent.appendChild(s);
    return s;
  }
  function path(parent, d, fill, stroke, sw) {
    const p = document.createElementNS(SVGNS, "path");
    p.setAttribute("d", d);
    p.setAttribute("fill", fill || "none");
    if (stroke) {
      p.setAttribute("stroke", stroke);
      p.setAttribute("stroke-width", sw || 4);
      p.setAttribute("stroke-linejoin", "round");
      p.setAttribute("stroke-linecap", "round");
    }
    parent.appendChild(p);
    return p;
  }
  const abs = { position: "absolute", left: "0px", top: "0px" };

  // ---------- arm (two segments + bitmap hand) ----------
  function buildArm(parent, rid, a, idx, opts) {
    const sx = a.shoulder[0], sy = a.shoulder[1], cx = a.cuff[0], cy = a.cuff[1];
    const L = Math.hypot(cx - sx, cy - sy);
    const L1 = L * 0.47, L2 = L - L1;
    const a0 = Math.atan2(-(cx - sx), cy - sy) / D2R;
    const w = a.sleeveW;
    const root = el("div", "rig-arm", parent, { ...abs, left: sx + "px", top: sy + "px", transformOrigin: "0 0" });
    if (a.bitmap && a.bitmap.S) {
      // side views: the forward arm drawn in the walk pose, cut at the elbow. Rest (0, 0) hangs straight down.
      const B = a.bitmap, S = B.S, E = B.E, Pm = B.P;
      const ang = (p, q2) => Math.atan2(-(q2[0] - p[0]), q2[1] - p[1]) / D2R;
      const l1 = Math.hypot(E[0] - S[0], E[1] - S[1]), l2 = Math.hypot(Pm[0] - E[0], Pm[1] - E[1]);
      const ua = el("div", "", root, { ...abs, transformOrigin: "0 0", transform: `rotate(${-ang(S, E)}deg)` });
      const ui = el("img", "rig-sleeve", ua, { ...abs, left: B.upper.x - S[0] + "px", top: B.upper.y - S[1] + "px", width: B.upper.w + "px", height: B.upper.h + "px" });
      ui.src = `assets/rig/${rid}/upper${idx}.png`;
      const elb = el("div", "rig-elbow", root, { ...abs, top: l1 + "px", transformOrigin: "0 0" });
      const fa = el("div", "", elb, { ...abs, transformOrigin: "0 0", transform: `rotate(${-ang(E, Pm)}deg)` });
      const fi = el("img", "rig-sleeve", fa, { ...abs, left: B.fore.x - E[0] + "px", top: B.fore.y - E[1] + "px", width: B.fore.w + "px", height: B.fore.h + "px" });
      fi.src = `assets/rig/${rid}/fore${idx}.png`;
      return { root, elb, a0: 0, L1: l1, L2: l2, sx, sy, cuffEl: fa, handEl: fi, rest: -9 };
    }
    if (a.bitmap) {
      // the drawn sleeve and hand from the reference art, split at the elbow
      const B = a.bitmap, ex = B.elbow[0], ey = B.elbow[1];
      const l1 = Math.hypot(ex - sx, ey - sy), l2 = Math.hypot(cx - ex, cy - ey);
      const ua = el("div", "", root, { ...abs, transformOrigin: "0 0", transform: `rotate(${-a0}deg)` });
      const ui = el("img", "rig-sleeve", ua, { ...abs, left: B.upper.x - sx + "px", top: B.upper.y - sy + "px", width: B.upper.w + "px", height: B.upper.h + "px" });
      ui.src = `assets/rig/${rid}/upper${idx}.png`;
      const elb = el("div", "rig-elbow", root, { ...abs, top: l1 + "px", transformOrigin: "0 0" });
      const fa = el("div", "", elb, { ...abs, transformOrigin: "0 0", transform: `rotate(${-a0}deg)` });
      const fi = el("img", "rig-sleeve", fa, { ...abs, left: B.fore.x - ex + "px", top: B.fore.y - ey + "px", width: B.fore.w + "px", height: B.fore.h + "px" });
      fi.src = `assets/rig/${rid}/fore${idx}.png`;
      return { root, elb, a0, L1: l1, L2: l2, sx, sy, cuffEl: fa, handEl: fi };
    }
    const up = svg(root, w * 2, L1 + w * 2, { left: -w + "px", top: -w + "px" });
    // upper sleeve: a soft tapered tube
    const u0 = w * 0.46, u1 = w * 0.5;
    path(up, `M ${w - u0} ${w * 0.6} Q ${w} ${w * 0.05} ${w + u0} ${w * 0.6} L ${w + u1} ${w + L1} L ${w - u1} ${w + L1} Z`, a.color, a.stroke, 3.5);
    const elb = el("div", "rig-elbow", root, { ...abs, top: L1 + "px", transformOrigin: "0 0" });
    const cuff = el("div", "rig-cuff", elb, { ...abs, top: L2 + "px", transformOrigin: "0 0", transform: `rotate(${-a0}deg)` });
    const hand = el("img", "rig-hand", cuff, { ...abs, left: a.hand.x - cx + "px", top: a.hand.y - cy + "px", width: a.hand.w + "px", height: a.hand.h + "px" });
    hand.src = `assets/rig/${rid}/hand${idx}.png`;
    const fs = svg(elb, w * 2.4, L2 + w * 2, { left: -w * 1.2 + "px", top: -w * 0.6 + "px" });
    const f0 = w * 0.5, f1 = w * 0.58;
    const cxw = w * 1.2;
    path(fs, `M ${cxw - f0} ${w * 0.6} Q ${cxw} ${-w * 0.05} ${cxw + f0} ${w * 0.6} L ${cxw + f1} ${w * 0.6 + L2 + 6} Q ${cxw} ${w * 0.6 + L2 + 12} ${cxw - f1} ${w * 0.6 + L2 + 6} Z`, a.color, a.stroke, 3.5);
    return { root, elb, a0, L1, L2, sx, sy, cuffEl: cuff, handEl: hand };
  }

  // ---------- feet + legs (walkers) ----------
  function footPath(FL, H) {
    // heel at 0, toe at FL, sole on y=0; ankle near x=0.3FL
    const t = H * 0.03;
    return {
      sole: `M ${-FL * 0.08} 0 L ${FL * 0.98} 0 Q ${FL * 1.04} ${-t * 0.4} ${FL * 0.98} ${-t * 0.8} L ${-FL * 0.06} ${-t * 0.8} Q ${-FL * 0.12} ${-t * 0.4} ${-FL * 0.08} 0 Z`,
      skin: `M ${FL * 0.02} ${-t * 0.8} L ${FL * 0.9} ${-t * 0.8} Q ${FL * 0.92} ${-t * 1.9} ${FL * 0.62} ${-t * 2.3} Q ${FL * 0.45} ${-t * 2.6} ${FL * 0.4} ${-t * 3.6} L ${FL * 0.06} ${-t * 3.6} Q ${-FL * 0.03} ${-t * 2.0} ${FL * 0.02} ${-t * 0.8} Z`,
      strap: `M ${FL * 0.44} ${-t * 0.8} L ${FL * 0.72} ${-t * 0.8} L ${FL * 0.6} ${-t * 2.25} L ${FL * 0.36} ${-t * 2.6} Z`,
    };
  }

  function make(host, rid, opt) {
    opt = opt || {};
    const R = RIGS[rid];
    const W = R.w, H = R.h;
    const walker = !!R.hem;
    const head = R.head;
    const ox = head ? head.pivot[0] - (walker ? H * 0.02 : 0) : W / 2;
    const ground = R.ground || H - 4;
    host.style.position = "absolute";
    host.style.left = "0px";
    host.style.top = "0px";
    host.style.transformOrigin = "0 0";
    const shadow = el("div", "rig-shadow", host, { ...abs, width: W * 0.9 + "px", height: H * 0.05 + "px", left: ox - W * 0.45 + "px", top: ground - H * 0.025 + "px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(70,40,15,.42), rgba(70,40,15,0))" });
    const inner = el("div", "rig-inner", host, { ...abs, width: W + "px", height: H + "px", transformOrigin: `${ox}px ${ground}px` });
    const P = { rid, R, host, inner, W, H, ox, ground, walker, shadow, opt };

    // far arm (walkers): darker copy behind everything
    if (walker || opt.farArm) {
      const a = R.arms[0];
      const far = Object.assign({}, a, { shoulder: [a.shoulder[0] - H * 0.015, a.shoulder[1] + H * 0.004] , cuff: [a.cuff[0] - H * 0.015, a.cuff[1]], hand: Object.assign({}, a.hand, { x: a.hand.x - H * 0.015 }) });
      P.farArm = buildArm(inner, rid, far, 0);
      P.farArm.root.style.filter = "brightness(0.8) saturate(0.95)";
    }
    if (walker) {
      P.legSvg = svg(inner, W, H, { left: "0px", top: "0px", clipPath: `inset(${R.hem - H * 0.02}px -50% -10% -50%)` });
      const FL = H * (R.legs ? 0.105 : 0.1);
      P.FL = FL;
      const fp = footPath(FL, H);
      P.legs = [0, 1].map((k) => {
        const g = document.createElementNS(SVGNS, "g");
        P.legSvg.appendChild(g);
        const leg = path(g, "", "none", R.arms[0].skin, H * (R.legs ? 0.03 : 0.034));
        if (R.legs) leg.setAttribute("stroke", "#c99a74");
        const foot = document.createElementNS(SVGNS, "g");
        g.appendChild(foot);
        path(foot, fp.skin, R.legs ? "#c99a74" : R.arms[0].skin);
        path(foot, fp.sole, R.sandal);
        if (!R.legs) path(foot, fp.strap, R.sandal);
        else path(foot, `M ${-FL * 0.08} 0 L ${FL} 0 Q ${FL * 1.02} ${-H * 0.03} ${FL * 0.6} ${-H * 0.05} L ${FL * 0.1} ${-H * 0.06} Q ${-FL * 0.1} ${-H * 0.04} ${-FL * 0.08} 0 Z`, "#5d3420");
        if (k === 0) g.setAttribute("opacity", "1");
        else g.setAttribute("filter", "");
        return { g, leg, foot };
      });
      // far leg darker
      P.legs[1].g.style.filter = "brightness(0.78)";
      // order: far leg first in DOM
      P.legSvg.insertBefore(P.legs[1].g, P.legs[0].g);
      P.skirt = el("img", "rig-skirt", inner, { ...abs, width: W + "px", height: H + "px", clipPath: `inset(${R.waist}px 0 0 0)`, transformOrigin: `${ox}px ${R.waist}px` });
      P.skirt.src = `assets/rig/${rid}/body.png`;
    }
    P.upper = el("div", "rig-upper", inner, { ...abs, width: W + "px", height: H + "px", transformOrigin: `${ox}px ${walker ? R.waist : H * 0.55}px` });
    P.body = el("img", "rig-body", P.upper, { ...abs, width: W + "px", height: H + "px" });
    P.body.src = `assets/rig/${rid}/body.png`;
    if (walker) P.body.style.clipPath = `inset(0 0 ${H - R.waist - 8}px 0)`;
    if (opt.sit) {
      // seated (front views): drop the thigh band, show shins under the lap
      P.lower = el("img", "rig-lower", inner, { ...abs, width: W + "px", height: H + "px", clipPath: `inset(${opt.sit[1]}px 0 0 0)` });
      P.lower.src = `assets/rig/${rid}/body.png`;
      P.body.style.clipPath = `inset(0 0 ${H - opt.sit[0]}px 0)`;
      inner.insertBefore(P.lower, P.upper);
      P.sitGap = opt.sit[1] - opt.sit[0];
      // foreshortened thighs: a robe-coloured lap band over the seam
      const a = R.arms[0];
      const lw = W * 0.66, lh = H * 0.06;
      const lap = svg(P.upper, lw, lh, { left: (W - lw) / 2 + "px", top: opt.sit[0] - lh * 0.55 + "px" });
      path(lap, `M ${lw * 0.04} ${lh * 0.35} Q ${lw * 0.5} ${lh * 0.05} ${lw * 0.96} ${lh * 0.35} L ${lw * 0.98} ${lh * 0.8} Q ${lw * 0.5} ${lh * 1.05} ${lw * 0.02} ${lh * 0.8} Z`, a.color, a.stroke, 3.5);
      path(lap, `M ${lw * 0.5} ${lh * 0.25} L ${lw * 0.5} ${lh * 0.95}`, "none", a.stroke, 2.5);
    }
    if (opt.lap) {
      // cross-legged on the floor: a folded-robe lap in the robe colour
      const a = R.arms[0] || { color: "#ccc", stroke: "#aaa" };
      P.body.style.clipPath = `inset(0 0 ${H - opt.lap.y}px 0)`;
      const lap = svg(P.upper, W * 1.35, H * 0.16, { left: -W * 0.175 + "px", top: opt.lap.y - H * 0.05 + "px" });
      const lw = W * 1.35, lh = H * 0.16;
      path(lap, `M ${lw * 0.12} ${lh * 0.62} Q ${lw * 0.1} ${lh * 0.25} ${lw * 0.32} ${lh * 0.2} L ${lw * 0.68} ${lh * 0.2} Q ${lw * 0.9} ${lh * 0.25} ${lw * 0.88} ${lh * 0.62} Q ${lw * 0.5} ${lh * 0.82} ${lw * 0.12} ${lh * 0.62} Z`, opt.lap.color || a.color, opt.lap.stroke || a.stroke, 4);
      path(lap, `M ${lw * 0.3} ${lh * 0.5} Q ${lw * 0.5} ${lh * 0.6} ${lw * 0.7} ${lh * 0.5}`, "none", opt.lap.stroke || a.stroke, 3);
      P.lapSvg = lap;
      P.sitGap = P.ground - opt.lap.y - H * 0.07; // sit on the floor
    }
    // near arms
    let armParent = P.upper;
    if (opt.armLayer) {
      // near arm drawn in another layer (e.g. over a second puppet); that layer copies our transforms
      P.armHost = opt.armLayer;
      Object.assign(P.armHost.style, { position: "absolute", left: "0px", top: "0px", transformOrigin: "0 0" });
      const ai = el("div", "rig-inner", P.armHost, { ...abs, width: W + "px", height: H + "px" });
      P.armUpper = el("div", "rig-upper", ai, { ...abs, width: W + "px", height: H + "px", transformOrigin: P.upper.style.transformOrigin });
      armParent = P.armUpper;
    }
    P.arms = (walker ? [R.arms[0]] : R.arms).map((a, i) => buildArm(armParent, rid, a, i));
    if (head) {
      P.head = el("img", "rig-head", P.upper, { ...abs, width: W + "px", height: head.h + "px", transformOrigin: `${head.pivot[0]}px ${head.pivot[1]}px` });
      P.head.src = `assets/rig/${rid}/head.png`;
      // head above the arm root so a raised sleeve never covers the face
      P.upper.appendChild(P.head);
    }
    P.render = (s) => render(P, s);
    return P;
  }

  // IK: hip (hx,hy) to ankle (ax,ay), lengths l1,l2, knee forward (+x)
  function ik(hx, hy, ax, ay, l1, l2) {
    let dx = ax - hx, dy = ay - hy;
    let d = Math.hypot(dx, dy);
    const maxd = (l1 + l2) * 0.999;
    if (d > maxd) { ax = hx + (dx * maxd) / d; ay = hy + (dy * maxd) / d; dx = ax - hx; dy = ay - hy; d = maxd; }
    const a = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1));
    const base = Math.atan2(dy, dx);
    const ang = base - a; // knee toward +x when walking right (y down)
    const kx = hx + l1 * Math.cos(ang), ky = hy + l1 * Math.sin(ang);
    return [kx, ky, ax, ay];
  }

  // Walk/run cycle from distance travelled. Stance foot is fixed in the world: no sliding.
  function gait(P, d, run) {
    const H = P.H;
    const s = H * (run ? 0.3 : 0.2);     // half cycle distance
    const f = run ? 0.42 : 0.6;          // stance fraction
    const out = [];
    for (let k = 0; k < 2; k++) {
      const off = k === 0 ? 0.05 : 0.55;
      const phi = d / (2 * s) + off;
      const kk = Math.floor(phi), u = phi - kk;
      // world x of foot relative to walk start (d=0)
      const startRel = f * s - 2 * s * off; // rel to hip at d=0 for this phase, valid if off<f
      let wx, lift = 0, w = 0;
      // stance plant position for cycle kk: foot sits at hip+f*s at u=0
      const plant = 2 * s * (kk - off) + f * s;
      if (u < f) wx = plant;
      else {
        w = (u - f) / (1 - f);
        wx = plant + 2 * s * smooth(w);
        lift = Math.sin(Math.PI * w) * H * (run ? 0.06 : 0.035);
      }
      out.push({ rel: wx - d, lift, swing: u >= f ? w : 0 });
    }
    const spread = (out[0].rel - out[1].rel) / (2 * f * s);
    return { feet: out, s, f, spread };
  }

  function render(P, st) {
    const R = P.R, H = P.H;
    const t = st.t || 0;
    const seed = P.opt.seed || 1;
    const sc = (st.h || 400) * (REL[P.rid] || 1) / H; // screen px per rig px
    const dir = st.dir || 1;
    let bob = 0, lean = st.lean || 0, armN = st.arm ? st.arm[0] : 0, elN = st.arm ? st.arm[1] : 0;
    let armF = st.farArm ? st.farArm[0] : 0, elF = st.farArm ? st.farArm[1] : 0;
    let skirt = st.skirt || 0;
    const breathe = 1 + wob(t, seed, 3.4, 0.006) * (st.breath == null ? 1 : st.breath);
    let feet = null;
    if (P.walker) {
      const d = st.d != null ? st.d : st.x0 != null ? Math.abs(st.x - st.x0) / sc : 0;
      const run = st.run || 0;
      const g = gait(P, d, run);
      const stand = [{ rel: H * 0.05, lift: 0 }, { rel: -H * 0.035, lift: 0 }];
      const settle = clamp(st.settle == null ? 0 : st.settle, 0, 1);
      feet = g.feet.map((ft, k) => {
        // far foot (k=1) steps first, then near foot
        const b = smooth(clamp((settle - (k === 1 ? 0 : 0.5)) / 0.5, 0, 1));
        const rel = lerp(ft.rel, stand[k].rel, b);
        const lift = lerp(ft.lift, 0, b) + Math.sin(Math.PI * b) * H * 0.03 * (Math.abs(ft.rel - stand[k].rel) > H * 0.01 ? 1 : 0);
        return { rel, lift, swing: ft.swing * (1 - b) };
      });
      const walkAmt = 1 - settle;
      const nrm = (x) => x / (g.f * g.s);
      // arms counter-swing the legs
      const amp = (run ? 38 : 16) * walkAmt * (st.swing == null ? 1 : st.swing);
      // st.lock: the near arm is placed exactly (holding a hand, resting on a shoulder), so it does not swing
      if (!st.lock) armN += -amp * nrm(feet[0].rel) * 0.9 + (run ? -10 : 0);
      armF += -amp * nrm(feet[1].rel) * 0.9 + (run ? -10 : 0);
      if (!st.lock) elN += run ? -55 * walkAmt : -6 * walkAmt;
      elF += run ? -55 * walkAmt : -6 * walkAmt;
      const pass = 1 - Math.abs(nrm(feet[0].rel) - nrm(feet[1].rel)) / 2; // 1 at passing
      bob = -(pass * (run ? 0.03 : 0.012) * H) * walkAmt;
      lean += (run ? 7 : 1.5) * walkAmt;
      skirt += (-(nrm(feet[0].rel) + nrm(feet[1].rel)) * 2.5 + (run ? -6 : -1.5)) * walkAmt;
      P.lastFeet = feet;
    }
    // idle life (not in unison: seeded per puppet)
    const idle = st.idle == null ? 1 : st.idle;
    const headRot = (st.head || 0) + wob(t, seed + 3, 4.1, 0.8) * idle;
    lean += wob(t, seed + 7, 5.3, 0.35) * idle;
    armN += wob(t, seed + 11, 3.9, 1.2) * idle;

    const x = st.x, y = (st.y || 0) + (st.dy || 0);
    const rot = st.rot || 0;
    const hostT = `translate(${x}px, ${y}px) scale(${sc * dir}, ${sc}) rotate(${rot}deg) translate(${-P.ox}px, ${-P.ground}px)`;
    P.host.style.transform = hostT;
    if (P.armHost) P.armHost.style.transform = hostT;
    P.host.style.opacity = st.op == null ? 1 : st.op;
    if (P.armHost) P.armHost.style.opacity = P.host.style.opacity;
    P.shadow.style.opacity = st.shadow == null ? 1 : st.shadow;
    // the body rides the bob and lean; feet stay on the ground
    const upT = `translate(0px, ${bob + (P.sitGap || 0)}px) rotate(${lean}deg) scale(1, ${breathe})`;
    P.upper.style.transform = upT;
    if (P.armUpper) P.armUpper.style.transform = upT;
    if (P.skirt) P.skirt.style.transform = `translate(0px, ${bob}px) rotate(${lean * 0.6}deg) skewX(${skirt}deg)`;
    if (P.head) P.head.style.transform = `rotate(${headRot}deg)`;
    const setArm = (A, sh, e) => {
      A.root.style.transform = `rotate(${A.a0 + sh}deg)`;
      A.elb.style.transform = `rotate(${e}deg)`;
    };
    // a relaxed arm keeps a slight bend at the elbow
    if (P.arms[0] && P.arms[0].rest && !st.arm) elN += P.arms[0].rest;
    if (P.farArm && P.farArm.rest && !st.farArm) elF += P.farArm.rest;
    if (P.arms[0]) setArm(P.arms[0], armN, elN);
    if (P.arms[1]) setArm(P.arms[1], st.arm2 ? st.arm2[0] : 0, st.arm2 ? st.arm2[1] : 0);
    if (P.farArm) {
      setArm(P.farArm, armF, elF);
      P.farArm.root.style.transform = `translate(0px, ${bob}px) rotate(${P.farArm.a0 + armF}deg)`;
    }
    if (feet) {
      const hipY = R.waist + H * 0.06 + bob;
      const l = (P.ground - hipY + H * 0.015) / 2;
      feet.forEach((ft, k) => {
        const L = P.legs[k];
        const hx = P.ox + (k === 0 ? H * 0.008 : -H * 0.008);
        const ax = P.ox + ft.rel, ay = P.ground - ft.lift - H * 0.03 * 0.6;
        const [kx, ky, ax2, ay2] = ik(hx, hipY, ax + P.FL * 0.12, ay - H * 0.05, l, l);
        L.leg.setAttribute("d", `M ${hx} ${hipY} L ${kx} ${ky} L ${ax2} ${ay2}`);
        const toe = ft.swing > 0 ? -12 * Math.sin(Math.PI * ft.swing) : 0;
        L.foot.setAttribute("transform", `translate(${ax - P.FL * 0.1} ${P.ground - ft.lift}) rotate(${toe})`);
      });
    }
    // hand world position (for props): forward kinematics in screen space
    P.handWorld = (i) => {
      const A = i === "far" ? P.farArm : P.arms[i || 0];
      const sh = i === "far" ? armF : i === 1 ? (st.arm2 ? st.arm2[0] : 0) : armN;
      const e = i === "far" ? elF : i === 1 ? (st.arm2 ? st.arm2[1] : 0) : elN;
      const a1 = (A.a0 + sh + lean) * D2R, a2 = (A.a0 + sh + lean + e) * D2R;
      let px = A.sx - P.ox, py = A.sy - P.ground + bob + (P.sitGap || 0);
      // lean rotates about the upper origin; approximate with shoulder offset (small angles)
      px += -A.L1 * Math.sin(a1) - A.L2 * Math.sin(a2);
      py += A.L1 * Math.cos(a1) + A.L2 * Math.cos(a2);
      return { x: x + px * sc * dir, y: y + py * sc, ang: A.a0 + sh + e + lean, dir, sc };
    };
    return P;
  }

  // Whole-image figure (residents, back views): idle sway pivoting at the feet.
  function figure(host, src, w, h, opt) {
    opt = opt || {};
    host.style.position = "absolute";
    host.style.left = "0px";
    host.style.top = "0px";
    host.style.transformOrigin = "0 0";
    const shadow = el("div", "rig-shadow", host, { ...abs, width: w * 0.8 + "px", height: h * 0.05 + "px", left: w * 0.1 + "px", top: h * 0.975 - h * 0.025 + "px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(70,40,15,.4), rgba(70,40,15,0))" });
    const im = el("img", "fig-img", host, { ...abs, width: w + "px", height: h + "px", transformOrigin: `${w / 2}px ${h * 0.97}px` });
    im.src = src;
    const F = { host, im, w, h, shadow };
    F.render = (s) => {
      const key = (src.split("/").pop() || "").replace(".png", "");
      const sc = (s.h * (REL[key] || 1)) / h, dir = s.dir || 1, t = s.t || 0, seed = opt.seed || 1;
      host.style.transform = `translate(${s.x}px, ${s.y}px) scale(${sc * dir}, ${sc}) translate(${-w / 2}px, ${-h * 0.97}px)`;
      host.style.opacity = s.op == null ? 1 : s.op;
      const sway = (s.rot || 0) + wob(t, seed, opt.period || 4.6, opt.amp == null ? 0.6 : opt.amp);
      const br = 1 + wob(t, seed + 5, 3.3, 0.005);
      im.style.transform = `rotate(${sway}deg) scale(1, ${br}) skewX(${(s.skew || 0) + wob(t, seed + 9, 5.1, 0.4)}deg)`;
      return F;
    };
    return F;
  }

  // Drive a scene: one tween whose onUpdate renders everything from time.
  function drive(tl, dur, fn) {
    const clock = { t: 0 };
    tl.fromTo(clock, { t: 0 }, { t: dur, duration: dur, ease: "none", onUpdate: () => fn(clock.t) }, 0);
    fn(0);
  }

  // Camera: frame centre (cx, cy) and zoom z over a 1920x1080 stage.
  function camera(elm) {
    elm.style.transformOrigin = "0 0";
    return { render: (c) => {
      const z = Math.max(1, c.z || 1);
      const cx = clamp(c.cx, 960 / z, 1920 - 960 / z), cy = clamp(c.cy, 540 / z, 1080 - 540 / z);
      elm.style.transform = `translate(960px, 540px) scale(${z}) translate(${-cx}px, ${-cy}px)`;
    } };
  }
  // Put a prop image in a puppet's hand. grip = image px held by the hand; rot = extra degrees.
  function attach(img, P, arm, o) {
    const hw = P.handWorld(arm);
    const k = o.scale * hw.sc;
    img.style.transformOrigin = "0 0";
    img.style.transform = `translate(${hw.x}px, ${hw.y}px) scale(${hw.dir}, 1) rotate(${hw.ang + (o.rot || 0)}deg) translate(${(o.dx || 0) * hw.sc}px, ${(o.dy || 0) * hw.sc}px) scale(${k}) translate(${-o.grip[0]}px, ${-o.grip[1]}px)`;
    return hw;
  }
  // A short head-and-shoulder "speaking" gesture for in-scene lines (faceless: body carries the line).
  function talk(t, t0, t1, amp, seed) {
    if (t < t0 || t > t1) return 0;
    const env = Math.sin(Math.PI * clamp((t - t0) / (t1 - t0), 0, 1));
    return env * amp * (0.6 + 0.4 * Math.sin(2 * Math.PI * (t - t0) * 1.7 + seed));
  }
  // Arm IK: angles [shoulder, elbow] that put arm i's wrist on screen point (tx, ty).
  // st must hold the same x, y, h, dir the puppet renders with. bend = +1 or -1 picks the elbow side.
  function reach(P, st, i, tx, ty, bend) {
    const A = i === "far" ? P.farArm : P.arms[i || 0];
    const sc = (st.h || 400) * (REL[P.rid] || 1) / P.H, dir = st.dir || 1;
    // a walker leans into the walk; allow for it so the hand lands where asked
    const lean = (st.lean || 0) + (P.walker ? (st.run ? 7 : 1.5) * (1 - clamp(st.settle == null ? 0 : st.settle, 0, 1)) : 0);
    const sx = A.sx - P.ox, sy = A.sy - P.ground + (P.sitGap || 0);
    const lx = (tx - st.x) / (sc * dir), ly = (ty - (st.y || 0) - (st.dy || 0)) / sc;
    let vx = lx - sx, vy = ly - sy;
    let d = Math.hypot(vx, vy);
    const L1 = A.L1, L2 = A.L2, maxd = (L1 + L2) * 0.995;
    if (d > maxd) { vx *= maxd / d; vy *= maxd / d; d = maxd; }
    const aT = Math.atan2(-vx, vy);
    const g = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const a1 = aT + (bend || 1) * g;
    const ex = sx - L1 * Math.sin(a1), ey = sy + L1 * Math.cos(a1);
    const a2 = Math.atan2(-(sx + vx - ex), sy + vy - ey);
    return [a1 / D2R - A.a0 - lean, (a2 - a1) / D2R];
  }
  // Blend two [sh, el] pairs.
  function mixArm(a, b, u) { return [lerp(a[0], b[0], u), lerp(a[1], b[1], u)]; }
  // Screen point of a rig-space point (e.g. a shoulder) for a puppet state.
  function pt(P, st, rx, ry) {
    const sc = (st.h || 400) * (REL[P.rid] || 1) / P.H, dir = st.dir || 1;
    const r = (st.rot || 0) * D2R, lx = rx - P.ox, ly = ry - P.ground;
    const qx = lx * Math.cos(r) - ly * Math.sin(r), qy = lx * Math.sin(r) + ly * Math.cos(r);
    return { x: st.x + qx * sc * dir, y: (st.y || 0) + (st.dy || 0) + qy * sc };
  }
  // Where and when a walker's feet land, for a puppet moving along xOf(t) from x0 (sampled once at build).
  function footfalls(P, o) {
    const sc = (o.h * (REL[P.rid] || 1)) / P.H;
    const s = P.H * (o.run ? 0.3 : 0.2), f = o.run ? 0.42 : 0.6, out = [];
    [0.05, 0.55].forEach((off) => {
      let prev = null;
      for (let t = o.t0; t <= o.t1; t += 1 / 240) {
        const d = Math.abs(o.x(t) - o.x0) / sc, k = Math.floor(d / (2 * s) + off);
        if (prev !== null && k > prev) out.push({ t, x: o.x0 + (o.dir || 1) * (2 * s * (k - off) + f * s) * sc, y: o.y });
        prev = k;
      }
    });
    return out;
  }
  // Small dust puffs at footfalls: build once, then render(t).
  function dust(layer, falls, o) {
    o = o || {};
    const size = o.size || 46, life = o.life || 0.55;
    const els = falls.map(() => el("div", "rig-dust", layer, { ...abs, width: size + "px", height: size * 0.5 + "px", borderRadius: "50%", opacity: 0,
      background: "radial-gradient(closest-side, rgba(214,178,132,.75), rgba(214,178,132,0))", transformOrigin: "50% 100%" }));
    return { render: (t) => falls.forEach((fl, i) => {
      const a = (t - fl.t) / life, e = els[i];
      if (a < 0 || a > 1) { e.style.opacity = 0; return; }
      e.style.opacity = 0.7 * (1 - a) * (1 - a);
      e.style.transform = `translate(${fl.x - size / 2 - (o.drift || 0) * a}px, ${fl.y - size * 0.5}px) scale(${0.5 + 1.3 * a}, ${0.5 + 1.0 * a})`;
    }) };
  }
  window.Rig = { footfalls, dust, reach, mixArm, pt, make, figure, track, drive, wob, clamp, lerp, smooth, REL, gait, camera, attach, talk };
})();
