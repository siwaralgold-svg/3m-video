/* Shared character rig and helpers (from the Edison trial film), with the Qaraqush cast and props.
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  // a wrapped turban: one cloth shape and two fold lines
  const TURBAN = `<path d="M-128 -166 C-178 -250 -100 -340 0 -340 C100 -340 178 -250 128 -166 C80 -196 -80 -196 -128 -166Z"/><path d="M-138 -214 C-50 -264 70 -258 142 -206 M-112 -288 C-30 -238 80 -238 140 -258" fill="none"/>`;

  const WHO = {
    edison: {
      skin: "#f2c9a4", suit: "#3d4a63", hairC: "#e4e7ec", rx: 110,
      hair: `<path d="M-112 -112 C-128 -236 40 -272 108 -168 C118 -150 116 -122 108 -100 C92 -160 20 -196 -52 -168 C-84 -156 -104 -136 -112 -112Z"/>
             <path d="M-112 -112 C-120 -90 -116 -70 -108 -56 L-100 -110Z"/><path d="M108 -100 C118 -84 114 -66 106 -54 L100 -104Z"/><path d="M-30 -246 C-44 -214 -70 -190 -100 -170 M10 -250 C6 -224 -10 -204 -30 -190" fill="none"/>`,
      neckwear: `<path d="M0 104 L-46 82 L-46 128Z M0 104 L46 82 L46 128Z" fill="#8c2f2f" ${S(6)}/><circle cx="0" cy="104" r="10" fill="#8c2f2f" ${S(5)}/>`,
    },
    swan: {
      skin: "#f0c6a6", suit: "#4a4038", hairC: "#f1f2f4", rx: 108,
      hair: `<path d="M-108 -100 C-132 -120 -128 -170 -100 -176 C-104 -150 -100 -120 -96 -100Z"/><path d="M108 -100 C132 -120 128 -170 100 -176 C104 -150 100 -120 96 -100Z"/>`,
      beard: `<path d="M-108 -84 C-124 30 -60 112 0 114 C60 112 124 30 108 -84 C84 -52 44 -74 0 -72 C-44 -74 -84 -52 -108 -84Z"/>`,
      glasses: true,
      neckwear: `<path d="M-14 96 L14 96 L20 170 L0 190 L-20 170Z" fill="#26324a" ${S(5)}/>`,
    },
    dickson: {
      skin: "#f3cdaa", suit: "#55606b", hairC: "#5a3a22", rx: 104,
      hair: `<path d="M-106 -104 C-124 -244 114 -250 106 -104 C96 -168 50 -190 -10 -186 C-30 -150 -84 -150 -106 -104Z"/>`,
      stache: `<path d="M-46 -62 Q-22 -82 0 -68 Q22 -82 46 -62 Q22 -54 0 -60 Q-22 -54 -46 -62Z"/>`,
      neckwear: `<path d="M-14 96 L14 96 L20 170 L0 190 L-20 170Z" fill="#7a2f2f" ${S(5)}/>`,
    },
    melies: {
      skin: "#f1c8a2", suit: "#2f2a3d", hairC: "#c9ccd2", rx: 106,
      hair: `<path d="M-106 -96 C-134 -112 -130 -168 -98 -170 C-102 -144 -98 -116 -94 -96Z"/><path d="M106 -96 C134 -112 130 -168 98 -170 C102 -144 98 -116 94 -96Z"/>`,
      stache: `<path d="M-64 -84 Q-44 -58 0 -68 Q44 -58 64 -84 Q44 -46 0 -58 Q-44 -46 -64 -84Z"/>`,
      beard: `<path d="M-30 -14 Q0 -2 30 -14 L0 70Z"/>`,
      neckwear: `<path d="M0 104 L-40 86 L-40 124Z M0 104 L40 86 L40 124Z" fill="#1a1a22" ${S(6)}/>`,
    },
    tesla: {
      skin: "#efc8a6", suit: "#1f2433", hairC: "#1b1612", rx: 96,
      hair: `<path d="M-98 -100 C-116 -238 -12 -246 0 -206 C12 -246 116 -238 98 -100 C90 -162 44 -188 0 -184 C-44 -188 -90 -162 -98 -100Z"/>`,
      stache: `<path d="M-38 -64 Q-18 -76 0 -68 Q18 -76 38 -64 Q18 -60 0 -62 Q-18 -60 -38 -64Z"/>`,
      neckwear: `<path d="M-14 96 L14 96 L18 160 L0 178 L-18 160Z" fill="#3c4660" ${S(5)}/>`,
    },
    // Qaraqush: white turban with a red cap, no beard
    qaraqush: {
      skin: "#e9bf98", suit: "#3d4a63", hairC: "#f1f2f4", rx: 108, robe: "#8c2f2f",
      hair: `<path d="M-44 -326 C-34 -372 34 -372 44 -326Z" fill="#8c2f2f"/>${TURBAN}`,
    },
    // Saladin: dark full beard, grey turban
    saladin: {
      skin: "#e3b48c", suit: "#1f2433", hairC: "#2a211c", rx: 106, robe: "#55606b",
      hair: TURBAN.replace("<path ", '<path fill="#c9ccd2" '),
      beard: `<path d="M-106 -84 C-122 30 -60 112 0 114 C60 112 122 30 106 -84 C84 -52 44 -74 0 -72 C-44 -74 -84 -52 -106 -84Z"/>`,
      stache: `<path d="M-46 -62 Q-22 -82 0 -68 Q22 -82 46 -62 Q22 -54 0 -60 Q-22 -54 -46 -62Z"/>`,
    },
    // Ibn Mammati, the clerk: dark cap with a white band, grey pointed beard
    mammati: {
      skin: "#efc8a6", suit: "#4a4038", hairC: "#7b8494", rx: 104, robe: "#2f2a3d",
      hair: `<path d="M-112 -160 C-124 -300 124 -300 112 -160 C70 -186 -70 -186 -112 -160Z" fill="#2f2a3d"/><path d="M-118 -156 C-70 -188 70 -188 118 -156 L116 -200 C70 -230 -70 -230 -116 -200Z" fill="#f1f2f4"/>`,
      stache: `<path d="M-60 -80 Q-42 -58 0 -68 Q42 -58 60 -80 Q42 -48 0 -58 Q-42 -48 -60 -80Z"/>`,
      beard: `<path d="M-40 -16 Q0 -2 40 -16 L0 96Z"/>`,
    },
    // Ibn Khallikan, the historian: white beard, pale blue turban
    khallikan: {
      skin: "#f0c6a6", suit: "#55606b", hairC: "#f1f2f4", rx: 108, robe: "#3d4a63",
      hair: TURBAN.replace("<path ", '<path fill="#9fb4d0" '),
      beard: `<path d="M-108 -84 C-124 30 -60 112 0 114 C60 112 124 30 108 -84 C84 -52 44 -74 0 -72 C-44 -74 -84 -52 -108 -84Z"/>`,
    },
    // a builder: plain cloth cap, moustache
    worker: {
      skin: "#d9a67c", suit: "#6b4226", hairC: "#1b1612", rx: 104, robe: "#4a4038",
      hair: `<path d="M-110 -150 C-120 -262 120 -262 110 -150 C70 -180 -70 -180 -110 -150Z" fill="#c9ccd2"/>`,
      stache: `<path d="M-46 -62 Q-22 -82 0 -68 Q22 -82 46 -62 Q22 -54 0 -60 Q-22 -54 -46 -62Z"/>`,
    },
  };

  function bust(p, who) {
    const o = WHO[who];
    const rx = o.rx;
    const hairFill = `fill="${o.hairC}" ${S(7)}`;
    return `
<g id="${p}-rig">
  <g id="${p}-body">
    <rect x="-36" y="-10" width="72" height="110" fill="${o.skin}" ${S(7)}/>
    <path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="${o.suit}" ${S(8)}/>
    ${o.robe
      ? `<path d="M-52 86 L-6 168 L52 86Z" fill="#f4f6f9" ${S(6)}/><path d="M52 86 L-6 168 L-40 310 L-4 310 L22 180 L78 100Z" fill="${o.robe}" ${S(6)}/><path d="M-52 86 L-6 168" fill="none" ${S(6)}/>`
      : `<path d="M-52 86 L0 176 L52 86Z" fill="#f4f6f9" ${S(6)}/>
    <path d="M-52 86 L-104 132 L-26 250 M52 86 L104 132 L26 250" fill="none" ${S(6)}/>`}
    ${o.neckwear || ""}
  </g>
  <g id="${p}-head">
    <circle cx="${-rx}" cy="-98" r="22" fill="${o.skin}" ${S(7)}/><circle cx="${rx}" cy="-98" r="22" fill="${o.skin}" ${S(7)}/>
    <ellipse cx="0" cy="-96" rx="${rx}" ry="124" fill="${o.skin}" ${S(8)}/>
    ${o.beard ? `<g ${hairFill}>${o.beard}</g>` : ""}
    <g ${hairFill}>${o.hair}</g>
    <g id="${p}-eyes">
      <ellipse cx="-40" cy="-112" rx="21" ry="23" fill="#fff" ${S(5)}/><ellipse cx="40" cy="-112" rx="21" ry="23" fill="#fff" ${S(5)}/>
      <g id="${p}-pupils"><circle id="${p}-pL" cx="-40" cy="-110" r="10" fill="${INK}"/><circle id="${p}-pR" cx="40" cy="-110" r="10" fill="${INK}"/></g>
    </g>
    ${o.glasses ? `<g fill="none" ${S(6)}><circle cx="-40" cy="-112" r="31"/><circle cx="40" cy="-112" r="31"/><path d="M-9 -112 H9"/></g>` : ""}
    <path id="${p}-browL" d="M-66 -152 L-18 -150" fill="none" ${S(11)}/>
    <path id="${p}-browR" d="M18 -150 L66 -152" fill="none" ${S(11)}/>
    <path d="M-4 -96 Q-16 -74 6 -72" fill="none" ${S(6)}/>
    <g id="${p}-mouths">
      <path id="${p}-m-smug" d="M-30 -42 Q8 -26 40 -54" fill="none" ${S(7)}/>
      <path id="${p}-m-flat" d="M-28 -38 L28 -38" fill="none" ${S(7)} opacity="0"/>
      <path id="${p}-m-frown" d="M-32 -30 Q0 -52 32 -30" fill="none" ${S(7)} opacity="0"/>
      <ellipse id="${p}-m-shock" cx="0" cy="-34" rx="20" ry="25" fill="#5a1e1e" ${S(6)} opacity="0"/>
      <path id="${p}-m-grin" d="M-38 -50 Q0 -4 38 -50Z" fill="#fff" ${S(6)} opacity="0"/>
      <path id="${p}-m-smile" d="M-30 -44 Q0 -22 30 -44" fill="none" ${S(7)} opacity="0"/>
    </g>
    ${o.stache ? `<g ${hairFill}>${o.stache}</g>` : ""}
    <path id="${p}-sweat" d="M92 -190 Q76 -160 92 -150 Q108 -160 92 -190Z" fill="#8fd0f0" ${S(5)} opacity="0"/>
  </g>
</g>`;
  }

  const MOUTHS = ["smug", "flat", "frown", "shock", "grin", "smile"];
  // brow rotation (deg) for viewer-left and viewer-right brows, vertical offset, pupil offset
  const MOODS = {
    smug: { m: "smug", l: 0, r: -10, ly: 0, ry: -12, px: 0, py: 0 },
    calm: { m: "smile", l: 0, r: 0, ly: 0, ry: 0, px: 0, py: 0 },
    flat: { m: "flat", l: 0, r: 0, ly: 4, ry: 4, px: 0, py: 0 },
    annoyed: { m: "flat", l: 14, r: -14, ly: 8, ry: 8, px: 0, py: 0 },
    angry: { m: "frown", l: 20, r: -20, ly: 10, ry: 10, px: 0, py: 0 },
    worried: { m: "frown", l: -16, r: 16, ly: -6, ry: -6, px: 0, py: 2 },
    shock: { m: "shock", l: -8, r: 8, ly: -18, ry: -18, px: 0, py: 0 },
    laugh: { m: "grin", l: -6, r: 6, ly: -10, ry: -10, px: 0, py: -2 },
    sad: { m: "frown", l: -20, r: 20, ly: -2, ry: -2, px: 0, py: 6 },
    goofy: { m: "grin", l: -20, r: 16, ly: -16, ry: 2, px: 0, py: 0 },
  };

  function put(slotId, p, who) {
    document.getElementById(slotId).innerHTML = bust(p, who);
  }

  // start face without a take (use at time 0)
  function face(tl, p, mood, t) {
    const d = MOODS[mood];
    MOUTHS.forEach((k) => tl.set(`#${p}-m-${k}`, { opacity: k === d.m ? 1 : 0 }, t || 0));
    tl.set(`#${p}-browL`, { rotation: d.l, y: d.ly, transformOrigin: "50% 50%" }, t || 0);
    tl.set(`#${p}-browR`, { rotation: d.r, y: d.ry, transformOrigin: "50% 50%" }, t || 0);
    tl.set(`#${p}-pupils`, { x: d.px, y: d.py }, t || 0);
  }

  // a take: anticipation squash, new face, overshoot, settle
  function mood(tl, p, t, name, sweat) {
    const d = MOODS[name];
    const head = `#${p}-head`;
    tl.to(head, { scaleY: 0.92, scaleX: 1.05, duration: 0.1, ease: "power2.in", transformOrigin: "50% 92%" }, t);
    MOUTHS.forEach((k) => tl.set(`#${p}-m-${k}`, { opacity: k === d.m ? 1 : 0 }, t + 0.1));
    tl.to(`#${p}-browL`, { rotation: d.l, y: d.ly, duration: 0.16, ease: "back.out(2.5)", transformOrigin: "50% 50%" }, t + 0.1);
    tl.to(`#${p}-browR`, { rotation: d.r, y: d.ry, duration: 0.2, ease: "back.out(2.5)", transformOrigin: "50% 50%" }, t + 0.13);
    tl.to(`#${p}-pupils`, { x: d.px, y: d.py, duration: 0.15, ease: "power2.out" }, t + 0.1);
    tl.to(head, { scaleY: 1.07, scaleX: 0.96, duration: 0.12, ease: "power2.out", transformOrigin: "50% 92%" }, t + 0.1);
    tl.to(head, { scaleY: 1, scaleX: 1, duration: 0.3, ease: "elastic.out(1,0.5)", transformOrigin: "50% 92%" }, t + 0.22);
    if (sweat !== undefined) tl.to(`#${p}-sweat`, { opacity: sweat ? 1 : 0, duration: 0.15 }, t + 0.2);
  }

  function blink(tl, p, t) {
    tl.to(`#${p}-eyes`, { scaleY: 0.08, duration: 0.06, ease: "power1.in", transformOrigin: "50% 50%" }, t);
    tl.to(`#${p}-eyes`, { scaleY: 1, duration: 0.09, ease: "power1.out", transformOrigin: "50% 50%" }, t + 0.07);
  }

  function look(tl, p, t, x, y) {
    tl.to(`#${p}-pupils`, { x: x, y: y, duration: 0.18, ease: "power2.out" }, t);
  }

  // breathing: body rises and falls, head follows a beat later
  function idle(tl, p, from, to, period) {
    const per = period || 2.6;
    const n = Math.max(1, Math.round((to - from) / per));
    const half = (to - from) / n / 2;
    for (let i = 0; i < n; i++) {
      const t = from + i * half * 2;
      tl.to(`#${p}-body`, { scaleY: 1.025, duration: half, ease: "sine.inOut", transformOrigin: "50% 100%" }, t);
      tl.to(`#${p}-body`, { scaleY: 1, duration: half, ease: "sine.inOut", transformOrigin: "50% 100%" }, t + half);
    }
  }

  // verdict stamp slam: plate drops in, the stage shakes
  function stamp(tl, sel, stageSel, t, rot) {
    tl.fromTo(sel, { opacity: 0, scale: 2.8, rotation: rot - 10 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.17, ease: "power3.in" }, t - 0.17);
    tl.fromTo(stageSel, { x: 0, y: 0 }, { x: 9, y: -7, duration: 0.045, ease: "none", yoyo: true, repeat: 5, immediateRender: false }, t);
    tl.fromTo(sel, { scale: 1 }, { scale: 0.96, duration: 0.07, yoyo: true, repeat: 1, ease: "power1.inOut", immediateRender: false }, t);
  }

  // the joke's face: both eyes turn to the nose (on = true) or straighten
  function cross(tl, p, t, on, dur) {
    tl.to(`#${p}-pL`, { x: on ? 13 : 0, y: on ? 5 : 0, duration: dur === undefined ? 0.15 : dur, ease: "power2.out" }, t);
    tl.to(`#${p}-pR`, { x: on ? -13 : 0, y: on ? 5 : 0, duration: dur === undefined ? 0.15 : dur, ease: "power2.out" }, t);
  }

  return { put, face, mood, blink, look, idle, stamp, cross, INK };
})();

/* props */
EK.bulb = function (p) {
  const S = (w) => `stroke="${EK.INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  let rays = "";
  for (let i = 0; i < 8; i++) {
    const a = (Math.PI * 2 * i) / 8 - Math.PI / 2, c = Math.cos(a), s = Math.sin(a);
    if (s > 0.8) continue;
    rays += `<path d="M${(c * 108).toFixed(1)} ${(s * 108).toFixed(1)} L${(c * 150).toFixed(1)} ${(s * 150).toFixed(1)}"/>`;
  }
  return `
<g id="${p}-rays" fill="none" stroke="#ffd94a" stroke-width="12" stroke-linecap="round" opacity="0">${rays}</g>
<path d="M-56 58 C-96 20 -90 -82 0 -84 C90 -82 96 20 56 58 L44 96 L-44 96Z" fill="#aab6c8" ${S(8)}/>
<path id="${p}-lit" d="M-56 58 C-96 20 -90 -82 0 -84 C90 -82 96 20 56 58 L44 96 L-44 96Z" fill="#ffd94a" ${S(8)} opacity="0"/>
<path d="M-22 92 L-22 20 Q-10 -10 0 20 Q10 -10 22 20 L22 92" fill="none" ${S(6)}/>
<path d="M-48 96 H48 V150 Q0 176 -48 150Z" fill="#7b8494" ${S(8)}/><path d="M-48 116 H48 M-48 136 H48" ${S(5)}/>`;
};
EK.bulbOn = function (tl, p, t) {
  tl.to(`#${p}-lit`, { opacity: 1, duration: 0.05 }, t);
  tl.to(`#${p}-lit`, { opacity: 0.2, duration: 0.05 }, t + 0.07);
  tl.to(`#${p}-lit`, { opacity: 1, duration: 0.08 }, t + 0.14);
  tl.fromTo(`#${p}-rays`, { opacity: 0, scale: 0.5, transformOrigin: "50% 100%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t + 0.14);
};
// wooden box: a witness stand or the dock
EK.box = function (x, y, w, h, label) {
  const S = (sw) => `stroke="${EK.INK}" stroke-width="${sw}" stroke-linejoin="round"`;
  return `
<rect x="${x}" y="${y + 26}" width="${w}" height="${h - 26}" fill="#8a5a33" ${S(8)}/>
<rect x="${x + 28}" y="${y + 60}" width="${w - 56}" height="${h - 106}" fill="#6b4226" ${S(6)}/>
${label ? `<text x="${x + w / 2}" y="${y + 60 + (h - 106) / 2 + 15}" text-anchor="middle" font-family="Noto Kufi Arabic" font-weight="800" font-size="40" fill="#F4F6F9" direction="rtl">${label}</text>` : ""}
<rect x="${x - 18}" y="${y}" width="${w + 36}" height="40" rx="8" fill="#a8703f" ${S(8)}/>`;
};
EK.reel = function (r) {
  const S = (sw) => `stroke="${EK.INK}" stroke-width="${sw}"`;
  let holes = "";
  for (let i = 0; i < 5; i++) { const a = (Math.PI * 2 * i) / 5; holes += `<circle cx="${(Math.cos(a) * r * 0.55).toFixed(1)}" cy="${(Math.sin(a) * r * 0.55).toFixed(1)}" r="${r * 0.2}" fill="#8f99ab" ${S(5)}/>`; }
  return `<circle r="${r}" fill="#39414f" ${S(8)}/>${holes}<circle r="${r * 0.14}" fill="#F4F6F9" ${S(5)}/>`;
};
// scene entrance: the whole stage whips in from one side
EK.whip = function (tl, sel, from) {
  tl.fromTo(sel, { x: from, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out" }, 0);
};
EK.fill = function (id, html) { document.getElementById(id).innerHTML = html; };

/* Qaraqush props: all flat fills with the ink outline */
EK.S = function (w) { return `stroke="${EK.INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`; };
// a row of merlons along the top of a wall or tower
EK.merlons = function (x0, x1, y, w, h, fill) {
  let out = "";
  const n = Math.max(2, Math.round((x1 - x0) / (w * 2)));
  const step = (x1 - x0 - w) / (n - 1);
  for (let i = 0; i < n; i++) out += `<rect x="${(x0 + i * step).toFixed(1)}" y="${y - h}" width="${w}" height="${h + 6}" fill="${fill}" ${EK.S(6)}/>`;
  return out;
};
// the citadel: base line at y = 0, centred on x = 0, about 330 wide and 330 tall
EK.fort = function () {
  const S = EK.S, st = "#aab6c8", st2 = "#c9ccd2";
  return `
<path d="M0 -330 V-400" fill="none" ${S(7)}/><path d="M0 -400 L70 -378 L0 -356Z" fill="#8c2f2f" ${S(6)}/>
${EK.merlons(-44, 44, -306, 22, 26, st2)}<rect x="-44" y="-306" width="88" height="140" fill="${st2}" ${S(7)}/>
${EK.merlons(-165, -85, -246, 22, 26, st2)}<rect x="-165" y="-246" width="80" height="246" fill="${st2}" ${S(7)}/>
${EK.merlons(85, 165, -246, 22, 26, st2)}<rect x="85" y="-246" width="80" height="246" fill="${st2}" ${S(7)}/>
${EK.merlons(-90, 90, -176, 24, 26, st)}<rect x="-90" y="-176" width="180" height="176" fill="${st}" ${S(7)}/>
<path d="M-34 0 V-70 Q0 -122 34 -70 V0Z" fill="#6b4226" ${S(7)}/>
<path d="M-125 -190 V-150 M125 -190 V-150 M0 -270 V-230" fill="none" ${S(8)}/>`;
};
// a crenellated wall from x0 to x1 with its top at y
EK.wall = function (x0, x1, y, h, fill) {
  const f = fill || "#aab6c8";
  let lines = "";
  for (let x = x0 + 90; x < x1 - 20; x += 180) lines += `<path d="M${x} ${y + 40} V${y + 84} M${x + 90} ${y + 84} V${y + 128}" fill="none" ${EK.S(5)}/>`;
  return `${EK.merlons(x0, x1, y, 46, 40, f)}<rect x="${x0}" y="${y}" width="${x1 - x0}" height="${h}" fill="${f}" ${EK.S(8)}/><path d="M${x0} ${y + 40} H${x1} M${x0} ${y + 84} H${x1}" fill="none" ${EK.S(5)}/>${lines}`;
};
// the booklet: cover centred on 0,0, 250 x 330
EK.booklet = function (p) {
  const S = EK.S;
  return `
<rect x="-113" y="-153" width="250" height="330" rx="8" fill="#F4F6F9" ${S(7)}/>
<rect x="-125" y="-165" width="250" height="330" rx="8" fill="#8a5a33" ${S(8)}/>
<path d="M-93 -165 V165" fill="none" ${S(6)}/>
<rect x="-70" y="-112" width="172" height="104" rx="6" fill="#F4F6F9" ${S(6)}/>
<text id="${p}-name" x="16" y="-44" text-anchor="middle" font-family="Lalezar" font-size="46" fill="#0c1a30" direction="rtl">الفاشوش</text>
<path d="M-50 50 H82 M-50 86 H82" fill="none" ${S(6)}/>`;
};
