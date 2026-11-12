/* Shared character rig and helpers (art style from the Edison film), with the Nero cast and Roman props.
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

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
    churchill: {
      skin: "#f2c9a4", suit: "#1f2433", hairC: "#1b1b22", rx: 118,
      hair: `<path d="M-102 -190 C-108 -262 -90 -310 0 -312 C90 -310 108 -262 102 -190Z"/><path d="M-103 -216 H103 V-190 H-103Z" fill="#3a3f4d"/><rect x="-160" y="-200" width="320" height="28" rx="14"/>`,
      neckwear: `<path d="M0 104 L-50 80 L-50 130Z M0 104 L50 80 L50 130Z" fill="#26324a" ${S(6)}/><circle cx="0" cy="104" r="11" fill="#26324a" ${S(5)}/><g fill="#F4F6F9"><circle cx="-36" cy="96" r="4"/><circle cx="-30" cy="114" r="4"/><circle cx="36" cy="96" r="4"/><circle cx="30" cy="114" r="4"/></g>`,
    },
    churchillYoung: {
      skin: "#f3cdaa", suit: "#3d4a63", hairC: "#b5713a", rx: 114,
      hair: `<path d="M-114 -118 C-122 -232 -30 -238 0 -214 C40 -240 124 -222 114 -118 C102 -170 50 -196 0 -190 C-50 -196 -102 -170 -114 -118Z"/>`,
      neckwear: `<path d="M0 104 L-46 82 L-46 128Z M0 104 L46 82 L46 128Z" fill="#26324a" ${S(6)}/><circle cx="0" cy="104" r="10" fill="#26324a" ${S(5)}/>`,
    },
    mother: {
      skin: "#b8825c", hairC: "#1b1612", rx: 100,
      hair: `<path d="M-104 -104 C-116 -250 116 -250 104 -104 C92 -164 46 -188 0 -186 C-46 -188 -92 -164 -104 -104Z"/>
             <path fill="#8c4a3a" d="M-118 -120 C-136 -292 136 -292 118 -120 L150 96 L100 96 L108 -110 C100 -216 50 -262 0 -262 C-50 -262 -100 -216 -108 -110 L-100 96 L-150 96Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#8c4a3a" ${S(8)}/><path d="M-120 124 L70 310 M-40 90 L150 250" fill="none" ${S(6)}/>`,
    },
    child: {
      skin: "#b8825c", hairC: "#1b1612", rx: 104,
      hair: `<path d="M-106 -104 C-124 -244 124 -244 106 -104 C96 -168 50 -190 0 -186 C-50 -190 -96 -168 -106 -104Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#d8cdb8" ${S(8)}/><path d="M-44 86 Q0 130 44 86" fill="none" ${S(6)}/>`,
    },
    iraqi: {
      skin: "#d2a077", hairC: "#F4F6F9", rx: 106,
      beard: `<path fill="#1b1612" d="M-106 -76 C-112 24 -52 46 0 46 C52 46 112 24 106 -76 C82 -34 40 -16 0 -16 C-40 -16 -82 -34 -106 -76Z"/>`,
      hair: `<path d="M-120 -116 C-138 -288 138 -288 120 -116 L156 96 L100 96 L108 -108 C98 -176 50 -200 0 -198 C-50 -200 -98 -176 -108 -108 L-100 96 L-156 96Z"/>
             <path d="M-112 -186 Q0 -236 112 -186 M-116 -160 Q0 -212 116 -160" fill="none" stroke-width="13"/>`,
      stache: `<path fill="#1b1612" d="M-46 -60 Q-22 -80 0 -66 Q22 -80 46 -60 Q22 -50 0 -56 Q-22 -50 -46 -60Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#5a4632" ${S(8)}/><path d="M-42 88 L0 132 L42 88 L42 310 L-42 310Z" fill="#F4F6F9" ${S(6)}/>`,
    },
    soldier: {
      skin: "#f2c9a4", hairC: "#6b6f4a", rx: 106,
      hair: `<path d="M-116 -186 C-114 -276 114 -276 116 -186Z"/><rect x="-164" y="-198" width="328" height="26" rx="13"/>`,
      stache: `<path fill="#5a3a22" d="M-40 -62 Q-20 -76 0 -66 Q20 -76 40 -62 Q20 -54 0 -58 Q-20 -54 -40 -62Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#6b6f4a" ${S(8)}/><path d="M-50 86 L0 150 L50 86 M0 150 V310 M-150 150 L-70 300" fill="none" ${S(6)}/><circle cx="0" cy="200" r="9" fill="#CEA532" ${S(4)}/><circle cx="0" cy="262" r="9" fill="#CEA532" ${S(4)}/>`,
    },
    nero: {
      skin: "#f2c9a4", hairC: "#8a4a2a", rx: 114,
      hair: `<path d="M-116 -112 C-130 -236 -36 -252 0 -222 C36 -252 130 -236 116 -112 C108 -150 86 -172 62 -160 C52 -182 22 -184 8 -166 C-2 -186 -34 -186 -44 -164 C-62 -182 -94 -170 -100 -146 C-110 -138 -114 -126 -116 -112Z"/>
             <g fill="#4d6b4a" stroke-width="5"><ellipse cx="-106" cy="-176" rx="27" ry="12" transform="rotate(-62 -106 -176)"/><ellipse cx="-82" cy="-208" rx="27" ry="12" transform="rotate(-42 -82 -208)"/><ellipse cx="-46" cy="-230" rx="27" ry="12" transform="rotate(-20 -46 -230)"/><ellipse cx="46" cy="-230" rx="27" ry="12" transform="rotate(20 46 -230)"/><ellipse cx="82" cy="-208" rx="27" ry="12" transform="rotate(42 82 -208)"/><ellipse cx="106" cy="-176" rx="27" ry="12" transform="rotate(62 106 -176)"/></g>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#F4F6F9" ${S(8)}/><path d="M-44 86 Q0 132 44 86" fill="none" ${S(6)}/>
             <path d="M-150 150 C-70 150 70 230 132 310 L190 310 C190 262 182 222 164 190 C100 150 10 100 -70 94 C-108 104 -134 124 -150 150Z" fill="#6b2f5a" ${S(7)}/><path d="M-120 200 Q-90 250 -96 310 M-40 230 Q-20 270 -24 310" fill="none" ${S(5)}/>`,
    },
    romanMother: {
      skin: "#e2b48c", hairC: "#3a2a1e", rx: 100,
      hair: `<path d="M-104 -104 C-120 -246 120 -246 104 -104 C92 -164 46 -192 0 -150 C-46 -192 -92 -164 -104 -104Z"/><circle cx="0" cy="-246" r="34"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#b9a58a" ${S(8)}/><path d="M-46 86 Q0 136 46 86 M-110 130 Q-60 220 -80 310" fill="none" ${S(6)}/>`,
    },
    romanChild: {
      skin: "#e2b48c", hairC: "#3a2a1e", rx: 104,
      hair: `<path d="M-106 -104 C-124 -244 124 -244 106 -104 C96 -168 50 -190 0 -186 C-50 -190 -96 -168 -106 -104Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#d8cdb8" ${S(8)}/><path d="M-44 86 Q0 130 44 86" fill="none" ${S(6)}/>`,
    },
    citizen: {
      skin: "#e8bd96", hairC: "#4a3526", rx: 106,
      hair: `<path d="M-108 -104 C-124 -240 124 -240 108 -104 C98 -160 60 -178 0 -176 C-60 -178 -98 -160 -108 -104Z"/>`,
      beard: `<path d="M-106 -76 C-112 24 -52 46 0 46 C52 46 112 24 106 -76 C82 -34 40 -16 0 -16 C-40 -16 -82 -34 -106 -76Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#7a5a44" ${S(8)}/><path d="M-44 86 Q0 130 44 86" fill="none" ${S(6)}/>`,
    },
    citizen2: {
      skin: "#f0c6a6", hairC: "#c9ccd2", rx: 104,
      hair: `<path d="M-106 -96 C-134 -112 -130 -168 -98 -170 C-102 -144 -98 -116 -94 -96Z"/><path d="M106 -96 C134 -112 130 -168 98 -170 C102 -144 98 -116 94 -96Z"/>`,
      body: `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="#55606b" ${S(8)}/><path d="M-44 86 Q0 130 44 86" fill="none" ${S(6)}/>`,
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
    ${o.body || `<path d="M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z" fill="${o.suit}" ${S(8)}/>
    <path d="M-52 86 L0 176 L52 86Z" fill="#f4f6f9" ${S(6)}/>
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

  return { put, face, mood, blink, look, idle, stamp, INK };
})();

/* props: flat fills, ink outline, no gradients */
(function () {
  const INK = EK.INK;
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  // manila folder, 300 x 200, with its number
  EK.folder = function (n) {
    return `<path d="M0 34 H112 L134 0 H300 V200 H0Z" fill="#d8b47a" ${S(8)}/><path d="M0 62 H300" fill="none" ${S(5)}/>
<circle cx="150" cy="128" r="48" fill="#F4F6F9" ${S(6)}/><text x="150" y="156" text-anchor="middle" font-family="Lalezar" font-size="84" fill="${INK}">${n}</text>`;
  };
  // British India, simplified, in a 620 x 700 box
  EK.india = function () {
    return `<path d="M250 20 L300 60 L290 120 L350 170 L430 200 L520 210 L560 190 L604 215 L578 262 L532 266 L522 312 L480 332 L440 330 L400 400 L340 480 L300 570 L270 650 L245 690 L215 640 L185 540 L160 430 L150 360 L90 350 L60 300 L110 280 L100 230 L150 180 L190 110 L210 50Z" fill="#a8703f" ${S(8)}/>`;
  };
  // Iraq, simplified, in a 500 x 500 box, with the two rivers
  EK.iraq = function () {
    return `<path d="M150 40 L230 20 L300 60 L330 130 L310 190 L370 260 L420 330 L440 400 L470 440 L430 470 L380 460 L330 480 L250 470 L150 400 L60 330 L30 300 L40 240 L110 200 L130 120Z" fill="#a8703f" ${S(8)}/>
<path d="M112 176 Q230 300 412 446 M232 44 Q300 250 412 446" fill="none" stroke="#8fd0f0" stroke-width="9" stroke-linecap="round"/>`;
  };
  EK.flag = function (w, h) {
    return `<rect x="-5" y="-6" width="12" height="${h * 2.4}" fill="#6b4226" ${S(6)}/>
<svg x="6" y="0" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#26427a"/>
<path d="M0 0 L${w} ${h} M${w} 0 L0 ${h}" stroke="#F4F6F9" stroke-width="${h * 0.2}"/><path d="M0 0 L${w} ${h} M${w} 0 L0 ${h}" stroke="#a83232" stroke-width="${h * 0.07}"/>
<path d="M${w / 2} 0 V${h} M0 ${h / 2} H${w}" stroke="#F4F6F9" stroke-width="${h * 0.3}"/><path d="M${w / 2} 0 V${h} M0 ${h / 2} H${w}" stroke="#a83232" stroke-width="${h * 0.17}"/></svg>
<rect x="6" y="0" width="${w}" height="${h}" fill="none" ${S(7)}/>`;
  };
  EK.bowl = function () {
    return `<path d="M-58 0 Q-50 50 0 50 Q50 50 58 0Z" fill="#a8703f" ${S(7)}/><ellipse cx="0" cy="0" rx="58" ry="15" fill="#6b4226" ${S(6)}/>`;
  };
  // crate of shells, 190 x 130
  EK.crate = function () {
    return `<rect width="190" height="130" fill="#a8703f" ${S(8)}/><path d="M0 34 H190 M0 96 H190" fill="none" ${S(5)}/>
<g fill="#55606b" ${S(5)}><path d="M52 90 V56 Q64 30 76 56 V90Z"/><path d="M114 90 V56 Q126 30 138 56 V90Z"/></g>`;
  };
  // relief ship carrying grain sacks
  EK.ship = function () {
    return `<path d="M96 -70 H140 V-10 H96Z" fill="#8c2f2f" ${S(7)}/><rect x="40" y="-40" width="150" height="46" fill="#F4F6F9" ${S(7)}/>
<g fill="#d8b47a" ${S(6)}><ellipse cx="-70" cy="-12" rx="34" ry="26"/><ellipse cx="-20" cy="-14" rx="34" ry="26"/></g>
<path d="M-140 0 H230 L190 78 H-104Z" fill="#55606b" ${S(8)}/>`;
  };
  EK.wave = function (w) {
    let d = "M0 0";
    for (let x = 0; x < w; x += 60) d += ` q15 -18 30 0 t30 0`;
    return `<path d="${d}" fill="none" stroke="#8fd0f0" stroke-width="8" stroke-linecap="round"/>`;
  };
  EK.palm = function () {
    return `<path d="M-8 0 Q-2 -70 4 -130 L18 -130 Q16 -70 12 0Z" fill="#6b4226" ${S(6)}/>
<g fill="#4d6b4a" ${S(6)}><path d="M10 -130 Q-50 -180 -84 -130 Q-40 -150 10 -130Z"/><path d="M10 -130 Q70 -180 104 -130 Q60 -150 10 -130Z"/><path d="M10 -130 Q-30 -210 -70 -196 Q-24 -180 10 -130Z"/><path d="M10 -130 Q50 -210 90 -196 Q44 -180 10 -130Z"/></g>`;
  };
  // faceless ink silhouette (same footprint as a bust)
  EK.shadow = function () {
    return `<path d="M-190 310 C-190 150 -104 84 -36 84 L-36 20 C-126 -6 -128 -220 0 -224 C128 -220 126 -6 36 20 L36 84 C104 84 190 150 190 310Z" fill="#04070d" ${S(8)}/>`;
  };
  // hand making the V sign
  EK.vhand = function (skin) {
    return `<g fill="${skin}" ${S(7)}><rect x="-34" y="-128" width="30" height="110" rx="15" transform="rotate(-13 -19 -20)"/><rect x="4" y="-128" width="30" height="110" rx="15" transform="rotate(13 19 -20)"/><circle r="46"/><path d="M-30 6 Q0 -22 30 6" fill="none"/></g>`;
  };
})();
// scene entrance: the whole stage whips in from one side
EK.whip = function (tl, sel, from) {
  tl.fromTo(sel, { x: from, filter: "blur(18px)" }, { x: 0, filter: "blur(0px)", duration: 0.38, ease: "power4.out" }, 0);
};
EK.fill = function (id, html) { document.getElementById(id).innerHTML = html; };
// card pops in on back.out(2) with a small rotation; out drops it
EK.pop = function (tl, sel, t, rot) {
  tl.fromTo(sel, { opacity: 0, scale: 0.4, rotation: (rot || 0) - 12 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.3, ease: "back.out(2)" }, t);
};
EK.out = function (tl, sel, t) {
  tl.to(sel, { opacity: 0, scale: 0.7, duration: 0.15, ease: "power2.in" }, t);
};
// wooden box with a label: a desk or counter front
EK.box = function (x, y, w, h, label) {
  const S = (sw) => `stroke="${EK.INK}" stroke-width="${sw}" stroke-linejoin="round"`;
  return `
<rect x="${x}" y="${y + 26}" width="${w}" height="${h - 26}" fill="#8a5a33" ${S(8)}/>
<rect x="${x + 28}" y="${y + 60}" width="${w - 56}" height="${h - 106}" fill="#6b4226" ${S(6)}/>
${label ? `<text x="${x + w / 2}" y="${y + 60 + (h - 106) / 2 + 15}" text-anchor="middle" font-family="Noto Kufi Arabic" font-weight="800" font-size="40" fill="#F4F6F9" direction="rtl">${label}</text>` : ""}
<rect x="${x - 18}" y="${y}" width="${w + 36}" height="40" rx="8" fill="#a8703f" ${S(8)}/>`;
};

/* Roman props for the Nero film */
(function () {
  const INK = EK.INK;
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  // a flame, base at 0,0, about 150 wide and 190 tall
  EK.flame = function () {
    return `<path d="M0 0 C-60 0 -70 -60 -40 -100 C-36 -70 -20 -64 -16 -84 C-10 -130 20 -150 14 -190 C60 -150 76 -90 50 -50 C70 -60 66 -84 64 -92 C90 -40 60 0 0 0Z" fill="#e8742a" ${S(7)}/>
<path d="M4 -8 C-28 -8 -32 -44 -12 -66 C-6 -50 6 -54 10 -84 C34 -56 40 -8 4 -8Z" fill="#ffd94a"/>`;
  };
  const win = (x, y) => `<path d="M${x} ${y} v-44 a18 18 0 0 1 36 0 v44Z" fill="${INK}"/>`;
  // Rome's skyline, 1080 wide, standing on y = 0
  EK.rome = function () {
    return `<g ${S(8)}>
<rect x="10" y="-300" width="240" height="300" fill="#6f7a86"/><path d="M-6 -300 H266 L240 -340 H20Z" fill="#a8553a"/>
<rect x="880" y="-340" width="190" height="340" fill="#6f7a86"/><path d="M866 -340 H1084 L1060 -378 H890Z" fill="#a8553a"/>
<rect x="660" y="-210" width="230" height="210" fill="#8b95a1"/><path d="M680 -210 A95 95 0 0 1 870 -210Z" fill="#a8553a"/>
<path d="M270 -280 H650 L460 -400Z" fill="#b9c0c9"/><rect x="270" y="-280" width="380" height="34" fill="#8b95a1"/>
<g fill="#b9c0c9"><rect x="290" y="-246" width="44" height="216"/><rect x="386" y="-246" width="44" height="216"/><rect x="490" y="-246" width="44" height="216"/><rect x="586" y="-246" width="44" height="216"/></g>
<rect x="256" y="-30" width="408" height="30" fill="#8b95a1"/></g>
${win(40, -190)}${win(110, -190)}${win(180, -190)}${win(40, -70)}${win(110, -70)}${win(180, -70)}${win(910, -230)}${win(990, -230)}${win(910, -90)}${win(990, -90)}${win(710, -70)}${win(800, -70)}`;
  };
  // garden gate: stone wall 760 x 700 standing on y = 0, door leaves "<p>-L" and "<p>-R" hinged at x = -200 and 200
  EK.gate = function (p) {
    return `<rect x="-380" y="-700" width="760" height="700" fill="#8b95a1" ${S(8)}/><path d="M-380 -560 H380 M-380 -420 H-200 M200 -420 H380 M-380 -280 H-200 M200 -280 H380 M-380 -140 H-200 M200 -140 H380" fill="none" ${S(5)}/>
<path d="M-200 0 V-380 A200 200 0 0 1 200 -380 V0Z" fill="#4d6b4a" ${S(8)}/>
<g fill="#35503a" ${S(6)}><ellipse cx="-110" cy="-190" rx="44" ry="150"/><ellipse cx="110" cy="-190" rx="44" ry="150"/><ellipse cx="0" cy="-250" rx="40" ry="130"/></g>
<path d="M-70 0 L-24 -120 H24 L70 0Z" fill="#d8cdb8" ${S(6)}/>
<path id="${p}-L" d="M-200 0 V-380 A200 200 0 0 1 0 -580 V0Z" fill="#8a5a33" ${S(8)}/>
<path id="${p}-R" d="M200 0 V-380 A200 200 0 0 0 0 -580 V0Z" fill="#8a5a33" ${S(8)}/>`;
  };
  // scales of justice standing on y = 0, 500 tall; the beam is "<p>-beam", pivot at 0,-494
  EK.scales = function (p) {
    return `<g fill="#CEA532" ${S(7)}><rect x="-14" y="-494" width="28" height="470"/><path d="M-130 0 H130 L96 -36 H-96Z"/>
<g id="${p}-beam"><rect x="-260" y="-506" width="520" height="24" rx="12"/><circle cx="0" cy="-494" r="28"/>
<path d="M-240 -494 L-306 -330 M-240 -494 L-174 -330 M240 -494 L306 -330 M240 -494 L174 -330" fill="none"/>
<path d="M-320 -330 H-160 Q-240 -262 -320 -330Z"/><path d="M320 -330 H160 Q240 -262 320 -330Z"/></g></g>`;
  };
  // an open case file, 300 x 220, with its number
  EK.folderOpen = function (n) {
    return `<path d="M0 40 H112 L134 10 H300 V220 H0Z" fill="#c29a5c" ${S(8)}/><rect x="34" y="-14" width="232" height="200" fill="#F4F6F9" ${S(6)}/><path d="M62 30 H238 M62 70 H238 M62 110 H190" fill="none" ${S(5)}/>
<path d="M-22 110 H322 L300 220 H0Z" fill="#d8b47a" ${S(8)}/><circle cx="150" cy="166" r="40" fill="#F4F6F9" ${S(6)}/><text x="150" y="190" text-anchor="middle" font-family="Lalezar" font-size="70" fill="${INK}">${n}</text>`;
  };
  // a house block standing on y = 0
  EK.house = function (w, h, wall) {
    let wins = "";
    for (let x = 36; x + 36 < w; x += 84) wins += win(x, -h + 130) + win(x, -40);
    return `<rect x="0" y="${-h}" width="${w}" height="${h}" fill="${wall}" ${S(8)}/><path d="M-16 ${-h} H${w + 16} L${w - 10} ${-h - 44} H10Z" fill="#a8553a" ${S(8)}/>${wins}`;
  };
  EK.basket = function () {
    return `<g fill="#d8b47a" ${S(6)}><ellipse cx="-44" cy="-66" rx="44" ry="30"/><ellipse cx="40" cy="-70" rx="46" ry="32"/><ellipse cx="0" cy="-92" rx="44" ry="30"/></g><path d="M-36 -98 l14 12 M-4 -104 l14 12" fill="none" ${S(5)}/>
<path d="M-104 -60 H104 L80 40 H-80Z" fill="#a8703f" ${S(8)}/><path d="M-96 -26 H96 M-88 8 H88" fill="none" ${S(5)}/>`;
  };
  EK.sack = function () {
    return `<path d="M-70 50 C-104 -20 -70 -96 -34 -110 L-44 -146 H44 L34 -110 C70 -96 104 -20 70 50Z" fill="#d8cdb8" ${S(8)}/><path d="M-40 -110 H40" fill="none" ${S(6)}/>
<path d="M0 26 V-60 M0 -20 l-26 -22 M0 -20 l26 -22 M0 -44 l-22 -20 M0 -44 l22 -20" fill="none" stroke="#a8703f" stroke-width="9" stroke-linecap="round"/>`;
  };
})();
