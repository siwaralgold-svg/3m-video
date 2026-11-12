/* Shared character rig and helpers (art style from edison-stole, cast of the Dostoevsky film).
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  const COAT = (c) => `<path d="M-52 86 L0 176 L52 86Z" fill="#f4f6f9" ${S(6)}/><path d="M-52 86 L-104 132 L-26 250 M52 86 L104 132 L26 250" fill="none" ${S(6)}/>`;
  const WHO = {
    // Dostoevsky at 28: brown side-parted hair, short jaw beard, thin moustache
    fyodor: {
      skin: "#f1c9a6", suit: "#4a4038", hairC: "#6a4a2c", rx: 104,
      hair: `<path d="M-106 -104 C-126 -246 116 -252 106 -104 C98 -160 60 -196 10 -192 C-20 -150 -84 -150 -106 -104Z"/>`,
      beard: `<path d="M-104 -84 C-114 4 -56 48 0 48 C56 48 114 4 104 -84 C86 -34 46 -14 0 -14 C-46 -14 -86 -34 -104 -84Z"/>`,
      stache: `<path d="M-40 -64 Q-20 -76 0 -68 Q20 -76 40 -64 Q20 -58 0 -61 Q-20 -58 -40 -64Z"/>`,
      neckwear: `<path d="M-30 92 L30 92 L22 150 L0 168 L-22 150Z" fill="#26324a" ${S(5)}/>`,
    },
    // Dostoevsky as the world knows him: high bald forehead, long beard
    fyodorOld: {
      skin: "#efc6a2", suit: "#2f2a3d", hairC: "#7a6350", rx: 106,
      hair: `<path d="M-106 -92 C-138 -116 -132 -196 -92 -200 C-100 -160 -98 -120 -94 -92Z"/><path d="M106 -92 C138 -116 132 -196 92 -200 C100 -160 98 -120 94 -92Z"/><path d="M-44 -188 Q0 -198 44 -188 M-34 -168 Q0 -176 34 -168" fill="none"/>`,
      beard: `<path d="M-106 -84 C-128 40 -72 150 0 176 C72 150 128 40 106 -84 C84 -52 44 -74 0 -72 C-44 -74 -84 -52 -106 -84Z"/>`,
      stache: `<path d="M-52 -64 Q-26 -84 0 -70 Q26 -84 52 -64 Q26 -52 0 -60 Q-26 -52 -52 -64Z"/>`,
      neckwear: `<path d="M-14 96 L14 96 L20 170 L0 190 L-20 170Z" fill="#26324a" ${S(5)}/>`,
    },
    // Tsar Nicholas I: receding hair, big moustache, green uniform, epaulettes, blue sash
    tsar: {
      skin: "#f2c9a4", suit: "#2e4a3f", hairC: "#8a6a3f", rx: 108,
      hair: `<path d="M-108 -96 C-132 -150 -110 -214 -60 -214 C-84 -186 -96 -140 -94 -96Z"/><path d="M108 -96 C132 -150 110 -214 60 -214 C84 -186 96 -140 94 -96Z"/><path d="M-108 -96 L-94 -96 L-90 -34 L-106 -50Z"/><path d="M108 -96 L94 -96 L90 -34 L106 -50Z"/>`,
      stache: `<path d="M-70 -72 Q-40 -86 0 -68 Q40 -86 70 -72 Q44 -44 0 -58 Q-44 -44 -70 -72Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#2e4a3f" ${S(8)}/>
             <path d="M-130 116 L96 310 L160 310 L-96 96Z" fill="#2b4d7e" ${S(6)}/>
             <path d="M-48 70 H48 V120 Q0 138 -48 120Z" fill="#8c2f2f" ${S(7)}/>
             <g fill="#c7ccd6" ${S(6)}><path d="M-196 150 Q-150 96 -92 108 L-104 164 Q-150 160 -180 196Z"/><path d="M196 150 Q150 96 92 108 L104 164 Q150 160 180 196Z"/></g>
             <g fill="#c7ccd6" ${S(5)}><circle cx="0" cy="170" r="11"/><circle cx="0" cy="220" r="11"/><circle cx="0" cy="270" r="11"/></g>`,
    },
    // a soldier of the firing squad: shako, moustache, grey greatcoat, white cross-belts
    soldier: {
      skin: "#eec3a0", suit: "#55606b", hairC: "#1f2433", rx: 104,
      hair: `<path d="M-106 -176 L-94 -322 L94 -322 L106 -176Z"/><path d="M-120 -182 H120 V-162 H-120Z" fill="#39414f"/><circle cx="0" cy="-262" r="22" fill="#8c2f2f"/>`,
      stache: `<path d="M-50 -64 Q-24 -82 0 -68 Q24 -82 50 -64 Q24 -54 0 -60 Q-24 -54 -50 -64Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#55606b" ${S(8)}/>
             <path d="M-40 84 H40 V116 Q0 130 -40 116Z" fill="#39414f" ${S(6)}/>
             <path d="M-120 112 L70 310 L120 310 L-84 98Z M120 112 L-70 310 L-120 310 L84 98Z" fill="#f4f6f9" ${S(6)}/>`,
    },
    // three of the circle
    friend1: {
      skin: "#f3cdaa", suit: "#3d4a63", hairC: "#2a211b", rx: 100,
      hair: `<path d="M-102 -104 C-118 -240 -10 -250 0 -214 C10 -250 118 -240 102 -104 C92 -164 46 -190 0 -186 C-46 -190 -92 -164 -102 -104Z"/>`,
      glasses: true,
      neckwear: `<path d="M-14 96 L14 96 L18 160 L0 178 L-18 160Z" fill="#7a2f2f" ${S(5)}/>`,
    },
    friend2: {
      skin: "#f0c6a6", suit: "#55606b", hairC: "#8a4a2a", rx: 106,
      hair: `<path d="M-110 -100 C-150 -150 -120 -230 -70 -226 C-60 -262 0 -268 20 -240 C60 -266 124 -232 112 -180 C140 -150 124 -110 108 -100 C100 -150 60 -184 0 -182 C-60 -184 -100 -150 -110 -100Z"/><path d="M-108 -100 L-94 -100 L-88 -30 L-106 -46Z"/><path d="M108 -100 L94 -100 L88 -30 L106 -46Z"/>`,
      neckwear: `<path d="M0 104 L-40 86 L-40 124Z M0 104 L40 86 L40 124Z" fill="#26324a" ${S(6)}/>`,
    },
    friend3: {
      skin: "#f2c9a4", suit: "#4a4038", hairC: "#c9a25a", rx: 102,
      hair: `<path d="M-104 -104 C-120 -246 110 -250 104 -104 C90 -180 30 -200 -40 -176 C-70 -164 -94 -140 -104 -104Z"/>`,
      stache: `<path d="M-44 -62 Q-22 -80 0 -68 Q22 -80 44 -62 Q22 -54 0 -60 Q-22 -54 -44 -62Z"/>`,
      neckwear: `<path d="M-14 96 L14 96 L20 170 L0 190 L-20 170Z" fill="#3c4660" ${S(5)}/>`,
    },
  };
  // a convict's grey coat for Siberia
  WHO.fyodorK = Object.assign({}, WHO.fyodor, {
    body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#7b8494" ${S(8)}/><path d="M-44 84 H44 V112 Q0 128 -44 112Z" fill="#636c7c" ${S(6)}/><path d="M0 124 V310" fill="none" ${S(6)}/>`,
  });

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
  // a closed book standing upright, centred on 0,0
  EK.book = function (w, h, fill) {
    return `<rect x="${-w / 2}" y="${-h / 2}" width="${w}" height="${h}" rx="10" fill="${fill}" ${S(8)}/><rect x="${-w / 2}" y="${-h / 2}" width="34" height="${h}" rx="8" fill="${EK.INK}" opacity="0.35"/><path d="M${-w / 2 + 60} ${-h / 2 + 30} H${w / 2 - 26} M${-w / 2 + 60} ${h / 2 - 30} H${w / 2 - 26}" fill="none" stroke="#f4f6f9" stroke-width="6" stroke-linecap="round"/>`;
  };
  // snow-capped execution post, base at 0,0
  EK.post = function (h) {
    return `<rect x="-26" y="${-h}" width="52" height="${h + 40}" fill="#6b4226" ${S(8)}/><path d="M-38 ${-h} Q-30 ${-h - 34} 0 ${-h - 36} Q30 ${-h - 34} 38 ${-h} Q20 ${-h + 14} 0 ${-h + 6} Q-20 ${-h + 14} -38 ${-h}Z" fill="#f4f6f9" ${S(7)}/>`;
  };
  // a flintlock musket pointing right, the butt (pivot) at 0,0
  EK.rifle = function () {
    return `<path d="M-30 -8 L60 -26 L120 -26 L120 10 L40 14 L-20 44Z" fill="#6b4226" ${S(7)}/><rect x="110" y="-24" width="330" height="20" fill="#7b8494" ${S(6)}/><rect x="110" y="-4" width="230" height="16" fill="#8a5a33" ${S(6)}/><path d="M440 -30 L470 -14 L440 -6Z" fill="#c7ccd6" ${S(5)}/>`;
  };
  // pine tree with snow, base at 0,0
  EK.pine = function (h) {
    const w = h * 0.5;
    return `<rect x="-14" y="${-h * 0.18}" width="28" height="${h * 0.18 + 10}" fill="#6b4226" ${S(7)}/><path d="M0 ${-h} L${w / 2} ${-h * 0.55} L${w * 0.22} ${-h * 0.55} L${w * 0.62} ${-h * 0.14} L${-w * 0.62} ${-h * 0.14} L${-w * 0.22} ${-h * 0.55} L${-w / 2} ${-h * 0.55}Z" fill="#24493f" ${S(8)}/><path d="M0 ${-h} L${w * 0.26} ${-h * 0.76} Q0 ${-h * 0.7} ${-w * 0.26} ${-h * 0.76}Z" fill="#f4f6f9" ${S(6)}/>`;
  };
})();
// scene entrance: the whole stage whips in from one side
EK.whip = function (tl, sel, from) {
  tl.fromTo(sel, { x: from, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out" }, 0);
};
EK.fill = function (id, html) { document.getElementById(id).innerHTML = html; };

/* backgrounds: each returns SVG markup for a 1080x1920 frame */
(function () {
  const INK = EK.INK;
  // a library wall: shelves of books in navy tones, a wooden desk across the bottom
  EK.library = function () {
    const cols = ["#172f55", "#1C385A", "#24426e", "#1a3560", "#172f55", "#2a3f63"];
    let out = `<rect width="1080" height="1920" fill="#13294B"/>`;
    for (let r = 0; r < 4; r++) {
      const base = 400 + r * 262;
      let x = 14, i = r * 5;
      while (x < 1066) {
        const w = 44 + ((i * 37) % 5) * 9, h = 150 + ((i * 53) % 6) * 14, lean = i % 9 === 4;
        const fill = i % 11 === 6 ? "#5b3a24" : cols[i % cols.length];
        out += `<g${lean ? ` transform="rotate(-9 ${x} ${base})"` : ""}><rect x="${x}" y="${base - h}" width="${w}" height="${h}" fill="${fill}" stroke="${INK}" stroke-width="5"/><path d="M${x + 8} ${base - h + 26} H${x + w - 8}" stroke="#34507c" stroke-width="5"/></g>`;
        x += w + (lean ? 26 : 2); i++;
      }
      out += `<rect x="-10" y="${base}" width="1100" height="30" fill="#6b4226" stroke="${INK}" stroke-width="7"/>`;
    }
    return out;
  };
  EK.desk = function () {
    return `<rect x="-10" y="1150" width="1100" height="780" fill="#6b4226"/><rect x="-10" y="1150" width="1100" height="46" fill="#a8703f" stroke="${INK}" stroke-width="7"/><g fill="#7a4c2a" stroke="${INK}" stroke-width="6"><rect x="40" y="1250" width="480" height="560" rx="6"/><rect x="560" y="1250" width="480" height="560" rx="6"/></g>`;
  };
  // Semyonovsky Square at dawn: the city behind, snow underfoot
  EK.square = function () {
    const dome = (x, y, s) => `<path d="M${x - 34 * s} ${y} C${x - 60 * s} ${y - 50 * s} ${x - 14 * s} ${y - 70 * s} ${x} ${y - 112 * s} C${x + 14 * s} ${y - 70 * s} ${x + 60 * s} ${y - 50 * s} ${x + 34 * s} ${y}Z"/><path d="M${x} ${y - 112 * s} V${y - 150 * s} M${x - 14 * s} ${y - 134 * s} H${x + 14 * s}" fill="none"/>`;
    return `<rect width="1080" height="1920" fill="#13294B"/>
<g fill="#172f55" stroke="${INK}" stroke-width="6" stroke-linejoin="round">
  <rect x="-10" y="860" width="210" height="260"/><rect x="196" y="800" width="150" height="320"/>${dome(271, 800, 1)}
  <rect x="342" y="900" width="250" height="220"/><path d="M430 900 L467 690 L504 900Z"/>
  <rect x="588" y="840" width="170" height="280"/>${dome(673, 840, 1.25)}<rect x="754" y="890" width="336" height="230"/>${dome(900, 890, 0.8)}
</g>
<g fill="#1C385A"><rect x="40" y="910" width="30" height="44"/><rect x="110" y="910" width="30" height="44"/><rect x="380" y="950" width="30" height="44"/><rect x="520" y="950" width="30" height="44"/><rect x="800" y="940" width="30" height="44"/><rect x="980" y="940" width="30" height="44"/></g>
<path d="M-10 1090 Q270 1050 540 1084 Q810 1050 1090 1090 V1930 H-10Z" fill="#dfe7f1" stroke="${INK}" stroke-width="8"/>`;
  };
  // the snow in front of whoever stands in the square
  EK.snow = function () {
    return `<path d="M-10 1160 Q180 1120 400 1152 Q640 1112 860 1150 Q980 1130 1090 1156 V1930 H-10Z" fill="#f4f6f9" stroke="${INK}" stroke-width="8"/><path d="M90 1400 Q200 1380 300 1400 M700 1520 Q820 1496 940 1520 M380 1700 Q480 1684 600 1700" fill="none" stroke="#c7d3e3" stroke-width="8" stroke-linecap="round"/>`;
  };
})();
