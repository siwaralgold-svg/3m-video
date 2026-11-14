/* Shared character rig and helpers (art style from edison-stole, cast of the Radishchev film).
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  const COAT = (c) => `<path d="M-52 86 L0 176 L52 86Z" fill="#f4f6f9" ${S(6)}/><path d="M-52 86 L-104 132 L-26 250 M52 86 L104 132 L26 250" fill="none" ${S(6)}/>`;
  const JABOT = `<path d="M-34 90 H34 L40 130 L20 124 L26 170 L0 160 L-26 170 L-20 124 L-40 130Z" fill="#f4f6f9" ${S(6)}/>`;
  const WHO = {
    // the censor: powdered wig with side rolls, round glasses, brown coat
    censor: {
      skin: "#f2c9a4", suit: "#4a4038", hairC: "#d9dee6", rx: 110,
      hair: `<path d="M-112 -96 C-134 -256 134 -256 112 -96 C98 -170 50 -198 0 -196 C-50 -198 -98 -170 -112 -96Z"/><circle cx="-122" cy="-66" r="27"/><circle cx="122" cy="-66" r="27"/><circle cx="-124" cy="-16" r="25"/><circle cx="124" cy="-16" r="25"/>`,
      glasses: true, neckwear: JABOT,
    },
    // Alexander Radishchev: dark hair swept back, clean-shaven, blue-grey coat, white jabot
    radishchev: {
      skin: "#f1c9a6", suit: "#3d4a63", hairC: "#4a3524", rx: 102,
      hair: `<path d="M-106 -100 C-128 -250 120 -256 106 -100 C96 -172 40 -204 -24 -192 C-64 -184 -96 -150 -106 -100Z"/><path d="M-108 -100 L-92 -100 L-88 -36 L-110 -52Z"/><path d="M108 -100 L92 -100 L88 -36 L110 -52Z"/>`,
      neckwear: JABOT,
    },
    // Empress Catherine II: high grey hair, a small crown, blue gown with a white collar and red sash
    catherine: {
      skin: "#f3cdaa", suit: "#2b4d7e", hairC: "#e3e6ec", rx: 100,
      hair: `<path d="M-108 -90 C-156 -180 -116 -318 0 -322 C116 -318 156 -180 108 -90 C98 -160 50 -192 0 -190 C-50 -192 -98 -160 -108 -90Z"/><circle cx="-118" cy="-44" r="26"/><circle cx="118" cy="-44" r="26"/><path d="M-62 -300 L-74 -366 L-36 -334 L0 -384 L36 -334 L74 -366 L62 -300Z" fill="#CEA532"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#2b4d7e" ${S(8)}/>
             <path d="M-150 130 L80 310 L150 310 L-110 104Z" fill="#8c2f2f" ${S(6)}/>
             <path d="M-110 104 C-60 70 60 70 110 104 C70 150 30 168 0 170 C-30 168 -70 150 -110 104Z" fill="#f4f6f9" ${S(7)}/>
             <g fill="${INK}"><circle cx="-56" cy="118" r="6"/><circle cx="0" cy="140" r="6"/><circle cx="56" cy="118" r="6"/></g>`,
    },
  };
  // the grey coat of an exile
  WHO.radishchevK = Object.assign({}, WHO.radishchev, {
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

/* ---- Radishchev film: props, backgrounds, Lottie ---- */
(function () {
  const INK = EK.INK;
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  // a hand stamp, its face at 0,0
  EK.stampTool = () => `<rect x="-78" y="-44" width="156" height="44" rx="8" fill="#6b4226" ${S(8)}/><rect x="-28" y="-150" width="56" height="110" rx="14" fill="#a8703f" ${S(8)}/><circle cx="0" cy="-168" r="42" fill="#8a5a33" ${S(8)}/>`;
  // an open book, centred on 0,0
  EK.openBook = function (w, h) {
    let l = "";
    for (let y = -h / 2 + 50; y < h / 2 - 30; y += 38) l += `<path d="M${-w / 2 + 34} ${y} H-34 M34 ${y} H${w / 2 - (y % 3 ? 34 : 80)}"/>`;
    return `<rect x="${-w / 2 - 16}" y="${-h / 2 + 14}" width="${w + 32}" height="${h}" rx="12" fill="#5b3a24" ${S(8)}/><path d="M${-w / 2} ${-h / 2} Q${-w / 4} ${-h / 2 - 22} 0 ${-h / 2} V${h / 2} Q${-w / 4} ${h / 2 - 22} ${-w / 2} ${h / 2}Z M0 ${-h / 2} Q${w / 4} ${-h / 2 - 22} ${w / 2} ${-h / 2} V${h / 2} Q${w / 4} ${h / 2 - 22} 0 ${h / 2}Z" fill="#f4f6f9" ${S(7)}/><g fill="none" stroke="#7b8494" stroke-width="7" stroke-linecap="round">${l}</g>`;
  };
  // the dock of the court: bars in front of whoever stands in it. dockBack goes behind, dockFront in front.
  EK.dockFront = function () {
    let bars = "";
    for (let x = 240; x <= 840; x += 120) bars += `<rect x="${x - 11}" y="560" width="22" height="420" fill="#8a5a33" ${S(7)}/>`;
    return `${bars}<rect x="184" y="524" width="712" height="46" rx="10" fill="#a8703f" ${S(8)}/><rect x="150" y="960" width="780" height="64" rx="10" fill="#a8703f" ${S(8)}/><rect x="184" y="1020" width="712" height="920" fill="#6b4226" ${S(8)}/><g fill="#7a4c2a" ${S(6)}><rect x="230" y="1080" width="290" height="700" rx="6"/><rect x="560" y="1080" width="290" height="700" rx="6"/></g>`;
  };
  EK.hall = function () {
    const win = (x) => `<path d="M${x - 112} 940 V430 A112 112 0 0 1 ${x + 112} 430 V940Z" fill="#172f55" ${S(8)}/><path d="M${x} 320 V940 M${x - 112} 560 H${x + 112} M${x - 112} 750 H${x + 112}" fill="none" stroke="#1C385A" stroke-width="8"/>`;
    return `<rect width="1080" height="1920" fill="#13294B"/>${win(190)}${win(540)}${win(890)}<rect x="-10" y="1180" width="1100" height="750" fill="#172f55"/><path d="M-10 1180 H1090" ${S(8)}/>`;
  };
  // a country road between fields, three huts on the horizon
  EK.road = function () {
    const hut = (x, y, s) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-90" y="-110" width="180" height="110" fill="#8a5a33" ${S(8)}/><path d="M-116 -110 L0 -206 L116 -110Z" fill="#4a4038" ${S(8)}/><rect x="-22" y="-70" width="44" height="70" fill="${INK}"/><rect x="40" y="-80" width="30" height="30" fill="#1C385A" ${S(5)}/></g>`;
    return `<rect width="1080" height="1920" fill="#13294B"/><path d="M-10 860 Q200 760 420 840 Q700 740 1090 850 V1000 H-10Z" fill="#172f55" ${S(7)}/>
<path d="M-10 940 Q540 900 1090 940 V1930 H-10Z" fill="#24493f" ${S(8)}/>${hut(170, 960, 1)}${hut(930, 950, 0.82)}${hut(690, 930, 0.6)}
<path d="M330 1930 Q500 1300 520 936 L580 936 Q700 1300 900 1930Z" fill="#a8703f" ${S(8)}/><path d="M560 1840 V1700 M556 1560 V1450 M552 1330 V1250 M550 1150 V1090" fill="none" stroke="#6b4226" stroke-width="9" stroke-linecap="round"/>`;
  };
  // a peasant standing, feet at 0,0
  EK.peasant = function (shirt) {
    return `<path d="M-74 0 L-58 -196 Q0 -236 58 -196 L74 0Z" fill="${shirt || "#55606b"}" ${S(8)}/><path d="M-58 -120 H58" fill="none" ${S(6)}/><circle cx="0" cy="-268" r="54" fill="#eec3a0" ${S(8)}/><path d="M-50 -250 C-44 -196 44 -196 50 -250 C30 -236 -30 -236 -50 -250Z" fill="#6a4a2c" ${S(6)}/><path d="M-58 -284 C-56 -340 56 -340 58 -284Z" fill="#4a4038" ${S(7)}/><g fill="${INK}"><circle cx="-20" cy="-270" r="6"/><circle cx="20" cy="-270" r="6"/></g>`;
  };
  // screw press: the frame stands on 0,0; the platen is a separate part that travels
  EK.pressFrame = () => `<rect x="-250" y="-560" width="56" height="560" fill="#6b4226" ${S(8)}/><rect x="194" y="-560" width="56" height="560" fill="#6b4226" ${S(8)}/><rect x="-290" y="-610" width="580" height="70" rx="10" fill="#8a5a33" ${S(8)}/><rect x="-300" y="-50" width="600" height="60" rx="10" fill="#8a5a33" ${S(8)}/><rect x="-170" y="-76" width="340" height="28" fill="#f4f6f9" ${S(6)}/>`;
  EK.pressPlaten = () => `<rect x="-20" y="-560" width="40" height="330" fill="#7b8494" ${S(7)}/><path d="M-20 -500 H20 M-20 -440 H20 M-20 -380 H20 M-20 -320 H20" ${S(5)}/><rect x="-150" y="-470" width="300" height="24" rx="10" fill="#a8703f" ${S(7)}/><rect x="-180" y="-240" width="360" height="56" rx="8" fill="#4a4038" ${S(8)}/>`;
  EK.barrel = () => `<path d="M-96 0 C-132 -76 -132 -164 -96 -240 H96 C132 -164 132 -76 96 0Z" fill="#8a5a33" ${S(8)}/><path d="M-116 -66 H116 M-116 -174 H116" fill="none" stroke="${INK}" stroke-width="12"/><path d="M-40 0 V-240 M40 0 V-240" fill="none" stroke="#6b4226" stroke-width="6"/>`;
  EK.crown = () => `<path d="M-124 58 L-146 -64 L-72 -4 L0 -96 L72 -4 L146 -64 L124 58Z" fill="#CEA532" ${S(8)}/><rect x="-130" y="48" width="260" height="40" rx="8" fill="#b08a22" ${S(8)}/><g fill="#8c2f2f" ${S(6)}><circle cx="-146" cy="-68" r="16"/><circle cx="0" cy="-100" r="16"/><circle cx="146" cy="-68" r="16"/></g>`;
  EK.flame = () => `<path d="M0 0 C-70 -44 -56 -130 -12 -190 C-8 -144 34 -132 22 -88 C56 -110 66 -44 0 0Z" fill="#ffd94a" ${S(7)}/><path d="M0 -8 C-28 -30 -20 -70 0 -96 C18 -70 26 -30 0 -8Z" fill="#fff2b0"/>`;
  EK.pitchfork = () => `<rect x="-9" y="-270" width="18" height="270" fill="#8a5a33" ${S(6)}/><path d="M-54 -380 V-304 Q-54 -270 0 -270 Q54 -270 54 -304 V-380 M0 -270 V-390" fill="none" ${S(11)}/>`;
  // a candle, its base at 0,0; the flame is its own element so it can flicker
  EK.candle = (id) => `<rect x="-22" y="-104" width="44" height="104" fill="#f4f6f9" ${S(7)}/><path d="M-40 0 H40 V16 H-40Z" fill="#7b8494" ${S(6)}/><path id="${id}" d="M0 -110 C-22 -134 -10 -162 0 -184 C10 -162 22 -134 0 -110Z" fill="#ffd94a" ${S(6)}/>`;
  EK.palace = function () {
    let p = "";
    for (const x of [70, 400, 730]) p += `<rect x="${x}" y="300" width="280" height="760" rx="10" fill="#172f55" ${S(7)}/><rect x="${x + 34}" y="334" width="212" height="692" rx="6" fill="none" stroke="#1C385A" stroke-width="7"/>`;
    return `<rect width="1080" height="1920" fill="#13294B"/>${p}<path d="M-10 150 H260 C230 420 150 560 -10 640Z" fill="#5a2a34" ${S(8)}/><path d="M1090 150 H820 C850 420 930 560 1090 640Z" fill="#5a2a34" ${S(8)}/><rect x="-10" y="120" width="1100" height="46" fill="#8a5a33" ${S(7)}/>`;
  };
  // a hand holding a quill, the nib near 0,0 (from the Dostoevsky film)
  EK.quillHand = (sleeve) => `<path d="M-90 200 Q0 120 0 10" fill="none" stroke="${INK}" stroke-width="80" stroke-linecap="round"/><path d="M-90 200 Q0 120 0 10" fill="none" stroke="${sleeve || "#4a4038"}" stroke-width="64" stroke-linecap="round"/><g transform="rotate(24)"><path d="M0 0 C-50 -80 -44 -200 10 -290 C60 -200 54 -80 0 0Z" fill="#f4f6f9" ${S(7)}/><path d="M4 -270 L0 40 M-30 -120 L2 -90 M34 -150 L4 -120 M-26 -190 L4 -160" fill="none" ${S(6)}/></g><circle cx="0" cy="0" r="42" fill="#f1c9a6" ${S(8)}/>`;

  // A Lottie file from assets/lottie (embedded by tools/build.py as window.LOTTIE) played by the scene's timeline:
  // frames from..to over dur seconds starting at t, repeated `repeat` times. Seek-safe: the frame comes from the timeline.
  // The HyperFrames Lottie adapter would also seek every registered instance from the scene start at 1x;
  // here the scene timeline owns the frame (start time, range, reverse), so the instance ignores outside seeks.
  EK.lottie = function (tl, id, name, t, dur, o) {
    o = o || {};
    const data = JSON.parse(JSON.stringify(window.LOTTIE[name]));
    const a = lottie.loadAnimation({ container: document.getElementById(id), renderer: "svg", loop: false, autoplay: false, animationData: data });
    const from = o.from == null ? data.ip : o.from, to = o.to == null ? data.op - 1 : o.to, st = { f: from };
    const go = a.goToAndStop.bind(a); a.goToAndStop = function () {};
    go(from, true);
    tl.fromTo(st, { f: from }, { f: to, duration: dur, ease: "none", repeat: o.repeat || 0, onUpdate: () => go(st.f, true) }, t);
    return a;
  };
})();
// part change inside a scene: the next stage whips in over the old one
EK.cut = function (tl, fromSel, toSel, t, from) {
  tl.set(toSel, { opacity: 1 }, t);
  tl.fromTo(toSel, { x: from || 1080, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out", immediateRender: false }, t);
  tl.set(fromSel, { opacity: 0 }, t + 0.38);
};
// draw an SVG path's stroke from its start
EK.draw = function (tl, sel, t, dur) {
  document.querySelectorAll(sel).forEach((el) => {
    const n = Math.ceil(el.getTotalLength()) + 2;
    el.style.strokeDasharray = n; el.style.strokeDashoffset = n;
    tl.fromTo(el, { strokeDashoffset: n }, { strokeDashoffset: 0, duration: dur, ease: "power1.inOut" }, t);
  });
};
