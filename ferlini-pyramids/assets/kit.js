/* Shared character rig and helpers (art style from edison-stole, cast of the Ferlini film).
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  const COAT = (c) => `<path d="M-52 86 L0 176 L52 86Z" fill="#f4f6f9" ${S(6)}/><path d="M-52 86 L-104 132 L-26 250 M52 86 L104 132 L26 250" fill="none" ${S(6)}/>`;
  const WHO = {
    // Giuseppe Ferlini: red tarboosh of the Egyptian army, dark side hair, moustache and chin beard
    ferlini: {
      skin: "#f0c6a2", suit: "#4a4038", hairC: "#2a211b", rx: 104,
      hair: `<path d="M-106 -92 C-140 -120 -128 -186 -92 -184 L-92 -96Z"/><path d="M106 -92 C140 -120 128 -186 92 -184 L92 -96Z"/><path d="M-94 -172 L-78 -304 L78 -304 L94 -172Z" fill="#8c2f2f"/><path d="M0 -304 Q60 -300 84 -236" fill="none"/><path d="M72 -240 L98 -236 L92 -186 L74 -190Z" fill="#1f2433"/>`,
      beard: `<path d="M-30 -14 Q0 -30 30 -14 Q26 46 0 58 Q-26 46 -30 -14Z"/>`,
      stache: `<path d="M-64 -70 Q-36 -84 0 -68 Q36 -84 64 -70 Q40 -48 0 -58 Q-40 -48 -64 -70Z"/>`,
      neckwear: `<path d="M-30 92 L30 92 L22 150 L0 168 L-22 150Z" fill="#26324a" ${S(5)}/>`,
    },
    // Queen Amanishakheto of Kush: skullcap crown with a gold band, earrings, broad collar
    queen: {
      skin: "#9a6a44", suit: "#f4f6f9", hairC: "#1f2433", rx: 104,
      hair: `<path d="M-106 -104 C-124 -252 124 -252 106 -104 C84 -176 -84 -176 -106 -104Z"/><path d="M-104 -150 C-60 -196 60 -196 104 -150 L100 -116 C60 -166 -60 -166 -100 -116Z" fill="#CEA532"/><path d="M-16 -176 Q0 -236 16 -176Z" fill="#CEA532"/><circle cx="-110" cy="-52" r="20" fill="#CEA532"/><circle cx="110" cy="-52" r="20" fill="#CEA532"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#f4f6f9" ${S(8)}/>
             <path d="M-112 104 Q0 60 112 104 Q84 214 0 230 Q-84 214 -112 104Z" fill="#CEA532" ${S(7)}/>
             <path d="M-84 122 Q0 90 84 122 M-66 156 Q0 130 66 156" fill="none" ${S(6)}/><circle cx="0" cy="196" r="13" fill="#8c2f2f" ${S(5)}/>`,
    },
    // a museum curator: bald, white side hair and moustache, glasses, bow tie
    curator: {
      skin: "#f3cdaa", suit: "#1f2433", hairC: "#c7ccd6", rx: 104,
      hair: `<path d="M-106 -92 C-138 -116 -132 -196 -92 -200 C-100 -160 -98 -120 -94 -92Z"/><path d="M106 -92 C138 -116 132 -196 92 -200 C100 -160 98 -120 94 -92Z"/>`,
      stache: `<path d="M-62 -66 Q-30 -86 0 -70 Q30 -86 62 -66 Q30 -48 0 -58 Q-30 -48 -62 -66Z"/>`,
      glasses: true,
      neckwear: `<path d="M0 104 L-44 84 L-44 126Z M0 104 L44 84 L44 126Z" fill="#8c2f2f" ${S(6)}/>`,
    },
    // Ludwig I of Bavaria: crown, brown curls, moustache, red robe with a white fur collar
    king: {
      skin: "#f2c9a4", suit: "#8c2f2f", hairC: "#6a4a2c", rx: 106,
      hair: `<path d="M-108 -96 C-150 -120 -140 -190 -96 -196 L-94 -96Z"/><path d="M108 -96 C150 -120 140 -190 96 -196 L94 -96Z"/><path d="M-98 -178 L-112 -300 L-52 -244 L0 -318 L52 -244 L112 -300 L98 -178Z" fill="#CEA532"/><circle cx="0" cy="-214" r="13" fill="#8c2f2f"/>`,
      stache: `<path d="M-52 -64 Q-26 -82 0 -68 Q26 -82 52 -64 Q26 -52 0 -60 Q-26 -52 -52 -64Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#8c2f2f" ${S(8)}/>
             <path d="M-150 120 Q-70 70 0 150 Q70 70 150 120 L120 220 Q50 150 0 250 Q-50 150 -120 220Z" fill="#f4f6f9" ${S(7)}/>
             <g fill="${INK}"><circle cx="-96" cy="140" r="8"/><circle cx="-56" cy="150" r="8"/><circle cx="96" cy="140" r="8"/><circle cx="56" cy="150" r="8"/><circle cx="0" cy="196" r="8"/></g>`,
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
    ${o.body || `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="${o.suit}" ${S(8)}/>${COAT()}${o.neckwear || ""}`}
    <g id="${p}-shroud" opacity="0"><path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#f4f6f9" ${S(8)}/><path d="M-46 84 Q0 150 46 84" fill="${o.skin}" ${S(6)}/><path d="M0 132 V310 M-120 180 Q-100 250 -112 310 M120 180 Q100 250 112 310" fill="none" stroke="#b9c4d4" stroke-width="6" stroke-linecap="round"/></g>
  </g>
  <g id="${p}-head">
    <circle cx="${-rx}" cy="-98" r="22" fill="${o.skin}" ${S(7)}/><circle cx="${rx}" cy="-98" r="22" fill="${o.skin}" ${S(7)}/>
    <ellipse cx="0" cy="-96" rx="${rx}" ry="124" fill="${o.skin}" ${S(8)}/>
    ${o.beard ? `<g ${hairFill}>${o.beard}</g>` : ""}
    <g ${hairFill}>${o.hair}</g>
    <g id="${p}-eyes">
      <ellipse cx="-40" cy="-112" rx="21" ry="23" fill="#fff" ${S(5)}/><ellipse cx="40" cy="-112" rx="21" ry="23" fill="#fff" ${S(5)}/>
      <g id="${p}-pupils"><circle cx="-40" cy="-110" r="10" fill="${INK}"/><circle cx="40" cy="-110" r="10" fill="${INK}"/></g>
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
    <g id="${p}-blind" opacity="0"><path d="M${-rx - 8} -136 H${rx + 8} V-88 H${-rx - 8}Z" fill="#f4f6f9" ${S(7)}/><path d="M${rx + 8} -124 L${rx + 46} -150 L${rx + 40} -106 L${rx + 60} -76 L${rx + 8} -98Z" fill="#f4f6f9" ${S(6)}/></g>
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

  // the mouth opens and closes while someone speaks aloud
  function talk(tl, p, from, to) {
    for (let t = from, i = 0; t < to; t += 0.17, i++) {
      MOUTHS.forEach((k) => tl.set(`#${p}-m-${k}`, { opacity: k === (i % 2 ? "flat" : "shock") ? 1 : 0 }, t));
      tl.set(`#${p}-m-shock`, { scaleX: 0.9, scaleY: i % 4 ? 0.55 : 0.8, transformOrigin: "50% 50%" }, t);
    }
    tl.set(`#${p}-m-shock`, { scaleX: 1, scaleY: 1 }, to);
  }
  // white death shirt on, blindfold on
  function shroud(tl, p, t) {
    tl.to(`#${p}-body`, { scaleX: 1.08, scaleY: 0.94, duration: 0.09, ease: "power2.in", transformOrigin: "50% 100%" }, t - 0.09);
    tl.set(`#${p}-shroud`, { opacity: 1 }, t);
    tl.to(`#${p}-body`, { scaleX: 1, scaleY: 1, duration: 0.35, ease: "elastic.out(1,0.5)", transformOrigin: "50% 100%" }, t);
  }
  function blind(tl, p, t) {
    tl.fromTo(`#${p}-blind`, { opacity: 0, y: -90 }, { opacity: 1, y: 0, duration: 0.16, ease: "power3.in" }, t - 0.16);
    tl.fromTo(`#${p}-head`, { y: 0 }, { y: 7, duration: 0.06, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }, t);
  }
  // cards: pop in with a small rotation, drop out
  function pop(tl, sel, t, rot) {
    tl.fromTo(sel, { opacity: 0, scale: 0.4, rotation: (rot || 0) - 8 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.3, ease: "back.out(2)" }, t);
  }
  function out(tl, sel, t) { tl.to(sel, { opacity: 0, duration: 0.14, ease: "power2.in" }, t - 0.14); }
  function shake(tl, sel, t, amt) {
    tl.fromTo(sel, { x: 0, y: 0 }, { x: amt || 9, y: -(amt || 9) * 0.7, duration: 0.045, ease: "none", yoyo: true, repeat: 5, immediateRender: false }, t);
  }
  // scene clock: w(i, offset) = the start of script word i in this scene's own time
  function clock(scene) { return (i, o) => +(DT.W[i] - DT.S[scene] + (o || 0)).toFixed(3); }

  return { put, face, mood, blink, look, idle, stamp, talk, shroud, blind, pop, out, shake, clock, INK };
})();

/* props */
(function () {
  const S = (w) => `stroke="${EK.INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  // a sheet of paper with written lines, centred on 0,0
  EK.letter = function (w, h) {
    let lines = "";
    for (let y = -h / 2 + 46; y < h / 2 - 30; y += 34) lines += `<path d="M${-w / 2 + 28} ${y} H${w / 2 - (y % 3 ? 28 : 70)}"/>`;
    return `<path d="M${-w / 2} ${-h / 2} H${w / 2 - 34} L${w / 2} ${-h / 2 + 34} V${h / 2} H${-w / 2}Z" fill="#f4f6f9" ${S(7)}/><path d="M${w / 2 - 34} ${-h / 2} V${-h / 2 + 34} H${w / 2}" fill="#c7ccd6" ${S(6)}/><g fill="none" stroke="#7b8494" stroke-width="7" stroke-linecap="round">${lines}</g>`;
  };
  // judge's gavel: head at the left end of a handle whose far end (the pivot) is at 0,0
  EK.gavel = function () {
    return `<rect x="-470" y="-25" width="470" height="50" rx="20" fill="#8a5a33" ${S(9)}/><rect x="-600" y="-125" width="170" height="250" rx="22" fill="#a8703f" ${S(9)}/><path d="M-600 -75 H-430 M-600 75 H-430" ${S(8)}/>`;
  };
})();
// scene entrance: the whole stage whips in from one side
EK.whip = function (tl, sel, from) {
  tl.fromTo(sel, { x: from, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out" }, 0);
};
EK.fill = function (id, html) { document.getElementById(id).innerHTML = html; };

/* props and backgrounds of the Ferlini film */
(function () {
  const INK = EK.INK;
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const f = (n) => +n.toFixed(1);
  // a steep Nubian pyramid of n stone courses; course i (0 = bottom) is <g id="<id>-r<i>">
  EK.pyr = function (id, cx, base, w, h, n, fill) {
    const hw = (t) => (w / 2) * (1 - t * 0.92), sw = w > 250 ? 7 : 5;
    let out = "";
    for (let i = 0; i < n; i++) {
      const y0 = f(base - (h * i) / n), y1 = f(base - (h * (i + 1)) / n), a = f(hw(i / n)), b = f(hw((i + 1) / n));
      let seams = "";
      if (w > 250) {
        const step = (h / n) * 1.5;
        for (let x = (i % 2 ? step / 2 : 0); x < b - 10; x += step) { seams += `M${f(cx + x)} ${y0} V${y1}`; if (x) seams += `M${f(cx - x)} ${y0} V${y1}`; }
      }
      out += `<g id="${id}-r${i}"><path d="M${cx - a} ${y0} L${cx - b} ${y1} H${cx + b} L${cx + a} ${y0}Z" fill="${fill || "#d9a868"}" ${S(sw)}/>${seams ? `<path d="${seams}" fill="none" stroke="#a8703f" stroke-width="4"/>` : ""}</g>`;
    }
    return out;
  };
  // the small offering chapel at a pyramid's foot
  EK.chapel = function (cx, base, s) {
    return `<g transform="translate(${cx},${base}) scale(${s})"><path d="M-72 0 L-58 -124 H58 L72 0Z" fill="#c8894e" ${S(7)}/><rect x="-22" y="-72" width="44" height="72" fill="${INK}"/></g>`;
  };
  // desert at night: far dunes and the ground the pyramids stand on
  EK.desert = function () {
    return `<rect width="1080" height="1920" fill="#13294B"/><circle cx="870" cy="330" r="96" fill="#1C385A"/>
<path d="M-10 1010 Q200 936 420 992 Q640 924 860 986 Q980 952 1090 990 V1930 H-10Z" fill="#6b4226" ${S(7)}/>
<path d="M-10 1094 Q270 1060 540 1088 Q810 1058 1090 1094 V1930 H-10Z" fill="#8a5a33" ${S(8)}/>`;
  };
  // the dune in front of whoever stands in the desert
  EK.sand = function () {
    return `<path d="M-10 1160 Q180 1124 400 1152 Q640 1116 860 1150 Q980 1134 1090 1156 V1930 H-10Z" fill="#a8703f" ${S(8)}/><path d="M90 1400 Q200 1380 300 1400 M700 1520 Q820 1496 940 1520 M380 1700 Q480 1684 600 1700" fill="none" stroke="#8a5a33" stroke-width="8" stroke-linecap="round"/>`;
  };
  // the court's table: a sandstone slab on stone blocks, top edge at y
  EK.table = function (y) {
    let seams = "";
    for (let r = 0; r < 6; r++) for (let x = (r % 2 ? 110 : 0); x < 1080; x += 220) seams += `M${x} ${y + 56 + r * 140} v140`;
    for (let r = 1; r < 6; r++) seams += `M-10 ${y + 56 + r * 140} H1090`;
    return `<rect x="-10" y="${y}" width="1100" height="${1940 - y}" fill="#a8703f"/><path d="${seams}" fill="none" stroke="#8a5a33" stroke-width="6"/><rect x="-10" y="${y}" width="1100" height="56" fill="#d9a868" ${S(7)}/>`;
  };
  // a wooden counter (museum, palace)
  EK.desk = function () {
    return `<rect x="-10" y="1150" width="1100" height="780" fill="#6b4226"/><rect x="-10" y="1150" width="1100" height="46" fill="#a8703f" ${S(7)}/><g fill="#7a4c2a" ${S(6)}><rect x="40" y="1250" width="480" height="560" rx="6"/><rect x="560" y="1250" width="480" height="560" rx="6"/></g>`;
  };
  // an indoor wall with two flat columns
  EK.hall = function () {
    const col = (x) => `<rect x="${x - 60}" y="250" width="120" height="910" fill="#1C385A" ${S(7)}/><rect x="${x - 84}" y="196" width="168" height="60" fill="#24426e" ${S(7)}/><path d="M${x - 24} 270 V1150 M${x + 24} 270 V1150" stroke="#172f55" stroke-width="8"/>`;
    return `<rect width="1080" height="1920" fill="#172f55"/><path d="M-10 150 H1090" stroke="${INK}" stroke-width="7"/><rect x="-10" y="-10" width="1100" height="160" fill="#13294B"/>${col(110)}${col(970)}`;
  };
  // a case file standing upright, centred on 0,0, with a number on its label
  EK.file = function (num) {
    return `<path d="M-95 -120 H-20 L0 -96 H95 V120 H-95Z" fill="#d9a868" ${S(8)}/><rect x="-58" y="-56" width="116" height="124" rx="8" fill="#f4f6f9" ${S(6)}/><text x="0" y="46" text-anchor="middle" font-family="Lalezar" font-size="112" fill="${INK}">${num}</text>`;
  };
  // an open treasure chest, base centre at 0,0
  EK.chest = function (empty) {
    return `<path d="M-150 -150 L-132 -292 Q0 -336 132 -292 L150 -150Z" fill="#6b4226" ${S(8)}/>${empty ? `<rect x="-132" y="-170" width="264" height="30" fill="${INK}"/>` : `<path d="M-134 -146 Q-96 -214 -44 -172 Q0 -236 48 -176 Q100 -220 134 -146Z" fill="#CEA532" ${S(7)}/>`}
<rect x="-150" y="-150" width="300" height="150" rx="8" fill="#8a5a33" ${S(8)}/><path d="M-84 -150 V0 M84 -150 V0" ${S(8)}/><rect x="-22" y="-112" width="44" height="52" rx="6" fill="#c7ccd6" ${S(6)}/>`;
  };
  // gold jewellery, centred on 0,0
  EK.bracelet = function (r) {
    return `<circle r="${r}" fill="none" stroke="${INK}" stroke-width="${r * 0.62}"/><circle r="${r}" fill="none" stroke="#CEA532" stroke-width="${r * 0.62 - 14}"/><circle cx="0" cy="${-r}" r="${r * 0.2}" fill="#8c2f2f" ${S(5)}/><circle cx="${-r * 0.8}" cy="${-r * 0.6}" r="${r * 0.12}" fill="#2b4d7e" ${S(4)}/><circle cx="${r * 0.8}" cy="${-r * 0.6}" r="${r * 0.12}" fill="#2b4d7e" ${S(4)}/>`;
  };
  EK.ring = function (r) {
    return `<circle r="${r}" fill="none" stroke="${INK}" stroke-width="${r * 0.5 + 12}"/><circle r="${r}" fill="none" stroke="#CEA532" stroke-width="${r * 0.5}"/><path d="M${-r * 0.5} ${-r * 1.1} L0 ${-r * 1.9} L${r * 0.5} ${-r * 1.1} L0 ${-r * 0.8}Z" fill="#8c2f2f" ${S(6)}/>`;
  };
  // a doctor's bag, base centre at 0,0
  EK.bag = function () {
    return `<path d="M-46 -150 Q-46 -206 0 -206 Q46 -206 46 -150" fill="none" ${S(12)}/><path d="M-110 -150 H110 L124 0 H-124Z" fill="#6b4226" ${S(8)}/><rect x="-118" y="-160" width="236" height="30" rx="10" fill="#8a5a33" ${S(7)}/><circle cx="0" cy="-66" r="38" fill="#f4f6f9" ${S(6)}/><path d="M0 -88 V-44 M-22 -66 H22" stroke="#8c2f2f" stroke-width="13" stroke-linecap="round"/>`;
  };
  // the governor's permit: a written sheet with a wax seal
  EK.permit = function (w, h) {
    return EK.letter(w, h) + `<circle cx="${w / 2 - 48}" cy="${h / 2 - 46}" r="30" fill="#8c2f2f" ${S(6)}/>`;
  };
  // a pile of pyramid stones, base centre at 0,0, about 2*hw wide
  EK.rubble = function (hw) {
    const k = hw / 300;
    const st = [[-250, 0, 150, 70, -4], [-90, 0, 170, 80, 3], [90, 0, 160, 74, -2], [240, 0, 120, 64, 6], [-170, -72, 150, 70, 5], [0, -80, 170, 76, -5], [160, -70, 130, 66, 8], [-70, -150, 140, 66, -8], [70, -152, 120, 62, 10], [0, -214, 110, 56, -3]];
    return st.map(([x, y, w, h, r], i) => `<rect x="${f((x - w / 2) * k)}" y="${f((y - h) * k)}" width="${f(w * k)}" height="${f(h * k)}" rx="6" transform="rotate(${r} ${f(x * k)} ${f(y * k)})" fill="${i % 3 ? "#d9a868" : "#c8894e"}" ${S(7)}/>`).join("");
  };
  // an ancient tomb robber: hooded figure with a sack, feet at 0,0
  EK.robber = function () {
    return `<circle cx="-120" cy="-190" r="92" fill="#6b4226" ${S(8)}/><path d="M-70 -260 L-40 -296" ${S(9)}/>
<path d="M-120 0 C-130 -210 -100 -350 0 -420 C100 -350 130 -210 120 0Z" fill="#1f2433" ${S(8)}/><ellipse cx="6" cy="-300" rx="62" ry="50" fill="${INK}"/><ellipse cx="-16" cy="-304" rx="13" ry="16" fill="#f4f6f9"/><ellipse cx="32" cy="-304" rx="13" ry="16" fill="#f4f6f9"/>`;
  };
  // a sailing ship, waterline centre at 0,0, bow to the left
  EK.ship = function () {
    return `<path d="M0 -40 V-400" ${S(12)}/><path d="M-14 -380 Q-170 -300 -150 -90 H-14Z" fill="#f4f6f9" ${S(8)}/><path d="M14 -350 Q130 -280 120 -90 H14Z" fill="#dfe7f1" ${S(8)}/><path d="M0 -400 L70 -380 L0 -360Z" fill="#8c2f2f" ${S(6)}/>
<g transform="translate(120,-56) scale(0.3)">${EK.chest()}</g>
<path d="M-250 -70 H230 L170 40 H-170 Q-220 20 -250 -70Z" fill="#8a5a33" ${S(8)}/><path d="M-226 -28 H206" stroke="#6b4226" stroke-width="10"/>`;
  };
  // a band of sea with a scalloped top edge at y
  EK.wave = function (y, fill, shift) {
    let d = `M${-80 + shift} ${y}`;
    for (let x = -80 + shift; x < 1160; x += 120) d += ` Q${x + 60} ${y - 44} ${x + 120} ${y}`;
    return `<path d="${d} V1940 H-90Z" fill="${fill}" ${S(7)}/>`;
  };
  // a museum front: steps, four columns and a pediment, base centre at 0,0
  EK.museum = function () {
    let cols = "";
    [-135, -45, 45, 135].forEach((x) => (cols += `<rect x="${x - 17}" y="-216" width="34" height="176" fill="#f4f6f9" ${S(6)}/>`));
    return `<rect x="-180" y="-220" width="360" height="180" fill="#24426e" ${S(7)}/>${cols}<path d="M-200 -220 L0 -330 L200 -220Z" fill="#dfe7f1" ${S(7)}/><rect x="-200" y="-40" width="400" height="40" fill="#c7ccd6" ${S(7)}/>`;
  };
  // Sudan as a simple shape in a 600x600 box, with the Nile; Khartoum at 350,290 and Meroe at 388,236
  EK.sudan = function () {
    return `<path d="M60 40 H430 L520 62 L560 160 L522 232 L500 330 L442 380 L430 470 L330 520 L230 500 L140 540 L90 460 L40 400 L30 300 L70 230 L60 120Z" fill="#a8703f" ${S(8)}/>
<path d="M340 520 L350 290 M440 384 L350 290 L372 262 L398 214 L380 150 L330 196 L300 130 L312 40" fill="none" stroke="#9fb4d0" stroke-width="11" stroke-linejoin="round" stroke-linecap="round"/>`;
  };
})();
// scene entrance: the whole stage whips in from one side
EK.whip = function (tl, sel, from) {
  tl.fromTo(sel, { x: from, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out" }, 0);
};
EK.fill = function (id, html) { document.getElementById(id).innerHTML = html; };
