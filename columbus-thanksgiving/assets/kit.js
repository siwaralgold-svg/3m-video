/* Shared character rig and helpers (art style from the Edison film), with the Columbus and Thanksgiving cast and props.
   EK.put(slotId, prefix, who) draws a bust into an SVG <g> slot.
   Parts get ids "<prefix>-head", "-body", "-eyes", "-pupils", "-browL", "-browR", "-m-<mouth>".
   EK.mood(tl, prefix, t, mood) plays a take into a new face. */
window.EK = (function () {
  const INK = "#0c1a30";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

  const BODY = "M-190 310 C-190 150 -104 84 0 84 C104 84 190 150 190 310Z";
  const WHO = {
    // Columbus: soft dark cap, grey hair to the jaw, dark red doublet
    columbus: {
      skin: "#efc8a6", hairC: "#9aa0ab", rx: 108,
      hair: `<path d="M-108 -150 C-142 -96 -140 -14 -114 14 L-94 -22 C-106 -62 -104 -112 -98 -150Z"/><path d="M108 -150 C142 -96 140 -14 114 14 L94 -22 C106 -62 104 -112 98 -150Z"/>
             <g transform="translate(0,-16)"><path fill="#2a2433" d="M-126 -150 C-156 -252 -72 -302 0 -302 C72 -302 156 -252 126 -150 C80 -190 -80 -190 -126 -150Z"/>
             <path fill="#453a52" d="M-138 -146 C-82 -200 82 -200 138 -146 L130 -120 C80 -168 -80 -168 -130 -120Z"/></g>`,
      body: `<path d="${BODY}" fill="#6b2f33" ${S(8)}/><path d="M-40 86 L0 132 L40 86Z" fill="#F4F6F9" ${S(6)}/>
             <path d="M-40 86 L-92 112 L0 226 L92 112 L40 86 L0 150Z" fill="#3a2a22" ${S(7)}/>`,
    },
    // the judge of history: white wig, black robe
    judge: {
      skin: "#f0c6a6", hairC: "#eef0f3", rx: 104, glasses: true,
      hair: `<path d="M-110 -100 C-150 -246 150 -246 110 -100 L130 44 C98 62 86 22 94 -20 C100 -142 60 -188 0 -188 C-60 -188 -100 -142 -94 -20 C-86 22 -98 62 -130 44Z"/>
             <path d="M-118 -60 q-18 12 0 26 M-122 -10 q-18 12 0 26 M118 -60 q18 12 0 26 M122 -10 q18 12 0 26" fill="none"/>`,
      body: `<path d="${BODY}" fill="#1b1b22" ${S(8)}/><path d="M-24 88 H24 L34 196 H-34Z" fill="#F4F6F9" ${S(6)}/><path d="M0 92 V192" fill="none" ${S(5)}/>`,
    },
    // English settler, 1621: plain felt hat, flat linen collar
    settler: {
      skin: "#f2c9a4", hairC: "#6b4a2e", rx: 104,
      beard: `<path d="M-104 -70 C-112 30 -52 70 0 70 C52 70 112 30 104 -70 C84 -12 44 -4 0 -4 C-44 -4 -84 -12 -104 -70Z"/>`,
      hair: `<path d="M-106 -104 C-120 -170 -100 -200 -80 -196 L-84 -150Z"/><path d="M106 -104 C120 -170 100 -200 80 -196 L84 -150Z"/>
             <path fill="#4a4038" d="M-88 -196 L-70 -306 H70 L88 -196Z"/><rect fill="#4a4038" x="-176" y="-206" width="352" height="28" rx="14"/>`,
      stache: `<path d="M-42 -62 Q-20 -78 0 -66 Q20 -78 42 -62 Q20 -54 0 -58 Q-20 -54 -42 -62Z"/>`,
      body: `<path d="${BODY}" fill="#6b5a48" ${S(8)}/><path d="M0 110 V310" fill="none" ${S(6)}/><path d="M-96 100 L0 84 L96 100 L74 160 L0 124 L-74 160Z" fill="#F4F6F9" ${S(7)}/>`,
    },
    // Wampanoag man, 1621: long hair, deerskin mantle over one shoulder, shell beads
    wampanoag: {
      skin: "#bd8a62", hairC: "#1b1612", rx: 104,
      hair: `<path d="M-108 -100 C-126 -252 126 -252 108 -100 C96 -172 50 -198 0 -194 C-50 -198 -96 -172 -108 -100Z"/>
             <path d="M-108 -112 C-132 -40 -130 40 -124 100 L-90 100 C-100 30 -102 -40 -98 -112Z"/><path d="M108 -112 C132 -40 130 40 124 100 L90 100 C100 30 102 -40 98 -112Z"/>`,
      body: `<path d="${BODY}" fill="#bd8a62" ${S(8)}/><path d="M-190 310 C-190 150 -104 84 -40 86 L150 310Z" fill="#a8804f" ${S(8)}/>
             <g fill="#F4F6F9" ${S(4)}><circle cx="-44" cy="112" r="10"/><circle cx="-24" cy="128" r="10"/><circle cx="0" cy="134" r="10" fill="#6a4c7a"/><circle cx="24" cy="128" r="10"/><circle cx="44" cy="112" r="10"/></g>`,
    },
    // Lincoln: stovepipe hat, chin beard, no moustache
    lincoln: {
      skin: "#e9c19c", hairC: "#1b1612", rx: 98, suit: "#1f2433",
      beard: `<path d="M-98 -70 C-112 34 -56 100 0 102 C56 100 112 34 98 -70 C84 -8 44 4 0 4 C-44 4 -84 -8 -98 -70Z"/>`,
      hair: `<path d="M-100 -104 C-112 -170 -96 -200 -76 -196 L-82 -150Z"/><path d="M100 -104 C112 -170 96 -200 76 -196 L82 -150Z"/>
             <path fill="#1b1b22" d="M-92 -196 V-372 H92 V-196Z"/><path fill="#3a3f4d" d="M-92 -226 H92 V-196 H-92Z"/><rect fill="#1b1b22" x="-150" y="-206" width="300" height="28" rx="14"/>`,
      neckwear: `<path d="M0 104 L-46 82 L-46 128Z M0 104 L46 82 L46 128Z" fill="#1b1b22" ${S(6)}/><circle cx="0" cy="104" r="10" fill="#1b1b22" ${S(5)}/>`,
    },
    // a family at the table today
    dad: {
      skin: "#f3cdaa", hairC: "#5a3a22", rx: 104,
      hair: `<path d="M-106 -104 C-124 -244 114 -250 106 -104 C96 -168 50 -190 -10 -186 C-30 -150 -84 -150 -106 -104Z"/>`,
      body: `<path d="${BODY}" fill="#4d6b4a" ${S(8)}/><path d="M-46 86 Q0 136 46 86" fill="none" ${S(6)}/>`,
    },
    mom: {
      skin: "#e8bd98", hairC: "#3a2418", rx: 100,
      hair: `<path d="M-104 -104 C-120 -250 120 -250 104 -104 C92 -168 46 -192 0 -190 C-46 -192 -92 -168 -104 -104Z"/>
             <path d="M-104 -112 C-128 -40 -124 40 -116 96 L-86 96 C-96 30 -98 -40 -94 -112Z"/><path d="M104 -112 C128 -40 124 40 116 96 L86 96 C96 30 98 -40 94 -112Z"/>`,
      body: `<path d="${BODY}" fill="#8c4a3a" ${S(8)}/><path d="M-46 86 Q0 136 46 86" fill="none" ${S(6)}/>`,
    },
    // a Wampanoag man today, at the day of mourning
    mourner: {
      skin: "#bd8a62", hairC: "#1b1612", rx: 104,
      hair: `<path d="M-108 -100 C-126 -252 126 -252 108 -100 C96 -172 50 -198 0 -194 C-50 -198 -96 -172 -108 -100Z"/>
             <path d="M-108 -112 C-132 -40 -130 40 -124 100 L-90 100 C-100 30 -102 -40 -98 -112Z"/><path d="M108 -112 C132 -40 130 40 124 100 L90 100 C100 30 102 -40 98 -112Z"/>`,
      body: `<path d="${BODY}" fill="#26324a" ${S(8)}/><path d="M-50 86 L0 150 L50 86 M0 150 V310" fill="none" ${S(6)}/>`,
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
  // roast bird on a platter, about 350 wide, origin at its middle
  EK.roast = function () {
    return `<ellipse cx="0" cy="58" rx="176" ry="38" fill="#F4F6F9" ${S(8)}/>
<g fill="#4d6b4a" ${S(6)}><circle cx="-128" cy="42" r="22"/><circle cx="130" cy="44" r="20"/><circle cx="-96" cy="56" r="16"/></g>
<path d="M-70 -22 C-100 -70 -126 -92 -152 -104 L-166 -84 C-142 -66 -120 -38 -106 0Z" fill="#b5713a" ${S(7)}/><circle cx="-162" cy="-98" r="13" fill="#F4F6F9" ${S(6)}/>
<path d="M-112 34 C-134 -58 -44 -112 20 -102 C102 -92 134 -22 112 36 C60 62 -60 62 -112 34Z" fill="#b5713a" ${S(8)}/>
<path d="M70 -22 C100 -70 126 -92 152 -104 L166 -84 C142 -66 120 -38 106 0Z" fill="#b5713a" ${S(7)}/><circle cx="162" cy="-98" r="13" fill="#F4F6F9" ${S(6)}/>
<path d="M-50 -52 Q-6 -78 40 -60" fill="none" stroke="#8a5a33" stroke-width="7" stroke-linecap="round"/>`;
  };
  // caravel, origin at the waterline under the mast
  EK.caravel = function () {
    return `<rect x="-6" y="-300" width="12" height="266" fill="#6b4226" ${S(6)}/>
<path d="M6 -300 L74 -320 L6 -342Z" fill="#8c2f2f" ${S(6)}/>
<path d="M-92 -270 H92 Q114 -184 92 -100 H-92 Q-70 -184 -92 -270Z" fill="#F4F6F9" ${S(8)}/>
<path d="M0 -238 V-132 M-42 -194 H42" fill="none" stroke="#8c2f2f" stroke-width="20"/>
<path d="M-156 -44 V-86 H-92 V-44Z M156 -44 V-74 H102 V-44Z" fill="#a8703f" ${S(7)}/>
<path d="M-156 -44 H156 L122 30 H-112Z" fill="#8a5a33" ${S(8)}/><path d="M-140 -12 H140" fill="none" ${S(5)}/>`;
  };
  EK.wave = function (w) {
    let d = "M0 0";
    for (let x = 0; x < w; x += 60) d += ` q15 -18 30 0 t30 0`;
    return `<path d="${d}" fill="none" stroke="#8fd0f0" stroke-width="8" stroke-linecap="round"/>`;
  };
  // the Caribbean, simplified, in a 900 x 560 box. Hispaniola has id "<p>-hisp".
  EK.carib = function (p) {
    return `<g fill="#b5895a" ${S(7)}>
<path d="M0 0 H150 L192 122 L162 150 L118 62 L0 62Z"/>
<path d="M0 300 C60 330 90 420 150 470 C200 520 260 540 300 560 H0Z"/>
<path d="M300 560 C420 500 620 520 900 500 V560Z"/>
<path d="M150 230 C230 200 330 220 420 270 C470 290 520 300 540 320 C480 332 400 312 330 292 C260 272 200 272 150 252Z"/>
<ellipse cx="400" cy="402" rx="50" ry="17"/><ellipse cx="832" cy="352" rx="34" ry="15"/>
<circle cx="330" cy="112" r="13"/><circle cx="392" cy="152" r="13"/><circle cx="452" cy="132" r="11"/><circle cx="502" cy="192" r="13"/>
<path id="${p}-hisp" d="M580 332 C620 310 700 310 760 330 C772 350 730 372 700 366 C660 382 610 374 580 352Z"/></g>`;
  };
  // small ship marker for a map, origin at its middle
  EK.boat = function () {
    return `<path d="M-34 6 H34 L24 26 H-24Z" fill="#8a5a33" ${S(5)}/><path d="M-22 -40 H22 V0 H-22Z" fill="#F4F6F9" ${S(5)}/>`;
  };
  // iron shackles, about 340 wide
  EK.shackle = function () {
    const ring = (x, r) => `<circle cx="${x}" cy="0" r="${r}" fill="none" stroke="${INK}" stroke-width="34"/><circle cx="${x}" cy="0" r="${r}" fill="none" stroke="#8f99ab" stroke-width="20"/>`;
    const link = (x) => `<ellipse cx="${x}" cy="0" rx="26" ry="15" fill="none" stroke="${INK}" stroke-width="22"/><ellipse cx="${x}" cy="0" rx="26" ry="15" fill="none" stroke="#8f99ab" stroke-width="10"/>`;
    return link(-34) + link(34) + link(0) + ring(-118, 52) + ring(118, 52);
  };
  // Wampanoag house (wetu): a bark-covered dome
  EK.wetu = function () {
    return `<path class="wetu-skin" d="M-130 0 C-130 -156 130 -156 130 0Z" fill="#9a7a50" ${S(8)}/>
<path d="M-116 -52 Q0 -92 116 -52 M-88 -102 Q0 -134 88 -102 M-60 -4 V-112 M60 -4 V-112" fill="none" ${S(5)}/>
<path d="M-30 0 V-52 Q0 -84 30 -52 V0Z" fill="#3a2a1c" ${S(6)}/>`;
  };
  // settler house: timber walls, steep thatch
  EK.house = function () {
    return `<rect x="-90" y="-112" width="180" height="112" fill="#a8703f" ${S(8)}/><path d="M-90 -76 H90 M-90 -38 H90" fill="none" ${S(4)}/>
<path d="M-118 -110 L0 -236 L118 -110Z" fill="#d8b47a" ${S(8)}/>
<rect x="-24" y="-72" width="48" height="72" fill="#6b4226" ${S(6)}/><rect x="44" y="-84" width="30" height="30" fill="#F4F6F9" ${S(5)}/>`;
  };
  // palisade: n pointed stakes, origin at the bottom left
  EK.fence = function (n) {
    let s = "";
    for (let i = 0; i < n; i++) s += `<path d="M${i * 48} 0 V-150 L${i * 48 + 24} -192 L${i * 48 + 48} -150 V0Z" fill="#8a5a33" ${S(7)}/>`;
    return s + `<path d="M0 -64 H${n * 48}" fill="none" ${S(8)}/>`;
  };
  EK.corn = function () {
    return `<ellipse rx="19" ry="52" fill="#e0b84a" ${S(6)}/><path d="M-10 -20 H10 M-14 4 H14 M-10 28 H10" fill="none" ${S(3)}/>
<path d="M-22 56 C-40 20 -30 -10 -20 -20 C-22 14 -12 40 0 56Z M22 56 C40 20 30 -10 20 -20 C22 14 12 40 0 56Z" fill="#4d6b4a" ${S(5)}/>`;
  };
  EK.fish = function () {
    return `<ellipse cx="0" cy="12" rx="90" ry="22" fill="#F4F6F9" ${S(6)}/><path d="M-62 0 Q0 -38 48 0 Q0 38 -62 0Z M48 0 L84 -24 V24Z" fill="#8f99ab" ${S(6)}/><circle cx="-36" cy="-4" r="5" fill="${INK}"/>`;
  };
  EK.bowl = function () {
    return `<path d="M-58 0 Q-50 50 0 50 Q50 50 58 0Z" fill="#a8703f" ${S(7)}/><ellipse cx="0" cy="0" rx="58" ry="15" fill="#e0b84a" ${S(6)}/>`;
  };
  // paper with writing; the signature line is "<p>-sig", the wax seal "<p>-seal"
  EK.paper = function (p) {
    return `<rect x="-120" y="-160" width="240" height="320" fill="#F4F6F9" ${S(7)}/>
<path d="M-84 -112 H84 M-84 -72 H84 M-84 -32 H84 M-84 8 H30" fill="none" stroke="#9fb4d0" stroke-width="9" stroke-linecap="round"/>
<path id="${p}-sig" d="M-80 96 q14 -40 28 0 t28 0 t28 0 q12 -20 30 -4" fill="none" ${S(7)}/>
<circle id="${p}-seal" cx="76" cy="112" r="32" fill="#8c2f2f" ${S(6)}/>`;
  };
  EK.quill = function () {
    return `<path d="M0 0 L20 -46 C60 -150 130 -210 190 -226 C176 -150 120 -80 44 -30Z" fill="#F4F6F9" ${S(6)}/><path d="M20 -46 C80 -120 130 -180 190 -226" fill="none" ${S(4)}/>`;
  };
  // wall calendar, 260 x 290, origin top left; the page is left empty for an HTML number
  EK.calendar = function () {
    return `<rect x="0" y="0" width="260" height="290" rx="12" fill="#F4F6F9" ${S(8)}/><path d="M0 12 Q0 0 12 0 H248 Q260 0 260 12 V84 H0Z" fill="#8c2f2f" ${S(8)}/>
<g fill="#c7ccd6" ${S(5)}><rect x="56" y="-24" width="20" height="50" rx="10"/><rect x="184" y="-24" width="20" height="50" rx="10"/></g>`;
  };
  // candle, origin at its foot; the flame is "<p>-flame"
  EK.candle = function (p) {
    return `<rect x="-24" y="-130" width="48" height="130" fill="#F4F6F9" ${S(7)}/><path d="M0 -130 V-150" fill="none" ${S(5)}/>
<path id="${p}-flame" d="M0 -222 C32 -182 24 -150 0 -144 C-24 -150 -32 -182 0 -222Z" fill="#ffd94a" ${S(6)}/>`;
  };
  // hanging lamp, origin at the ceiling
  EK.lamp = function () {
    return `<path d="M0 0 V70" fill="none" ${S(6)}/><path d="M-70 130 Q-60 70 0 70 Q60 70 70 130Z" fill="#55606b" ${S(7)}/><path d="M-40 130 Q0 168 40 130Z" fill="#ffd94a" ${S(6)}/>`;
  };
  // the scales of the court, origin at the foot; the beam and pans are "<p>-beam"
  EK.scales = function (p, c) {
    return `<rect x="-14" y="-330" width="28" height="330" fill="${c}" ${S(8)}/><path d="M-124 0 H124 L92 -42 H-92Z" fill="${c}" ${S(8)}/>
<g id="${p}-beam"><rect x="-262" y="-342" width="524" height="26" rx="13" fill="${c}" ${S(8)}/>
<path d="M-232 -322 L-302 -170 M-232 -322 L-162 -170 M232 -322 L162 -170 M232 -322 L302 -170" fill="none" ${S(6)}/>
<path d="M-314 -170 H-150 Q-232 -86 -314 -170Z" fill="${c}" ${S(8)}/><path d="M150 -170 H314 Q232 -86 150 -170Z" fill="${c}" ${S(8)}/></g>
<circle cx="0" cy="-330" r="27" fill="${c}" ${S(8)}/>`;
  };
  // judge's gavel lying on its block, about 230 wide
  EK.gavel = function () {
    return `<rect x="-110" y="20" width="220" height="30" rx="8" fill="#6b4226" ${S(7)}/><rect x="-10" y="-50" width="150" height="22" rx="11" fill="#8a5a33" ${S(6)}/>
<rect x="-80" y="-78" width="92" height="78" rx="12" fill="#a8703f" ${S(7)}/><path d="M-80 -58 H12 M-80 -20 H12" fill="none" ${S(5)}/>`;
  };
  // a row of dots from (x1,y1) to (x2,y2): a link between two things
  EK.dots = function (cls, x1, y1, x2, y2, n) {
    let s = "";
    for (let i = 0; i < n; i++) { const k = i / (n - 1); s += `<circle class="${cls}" cx="${(x1 + (x2 - x1) * k).toFixed(1)}" cy="${(y1 + (y2 - y1) * k).toFixed(1)}" r="13" fill="#F4F6F9" ${S(5)}/>`; }
    return s;
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
// stage shake on an impact
EK.shake = function (tl, sel, t, a) {
  tl.fromTo(sel, { x: 0, y: 0 }, { x: a || 9, y: -(a || 9) * 0.7, duration: 0.045, ease: "none", yoyo: true, repeat: 5, immediateRender: false }, t);
};
// SVG group (inside a translate wrapper) drops from above and lands at t with a squash
EK.drop = function (tl, sel, t, from) {
  tl.fromTo(sel, { opacity: 0, y: from || -900 }, { opacity: 1, y: 0, duration: 0.26, ease: "power3.in" }, t - 0.26);
  tl.fromTo(sel, { scaleY: 0.86, scaleX: 1.08, svgOrigin: "0 0" }, { scaleY: 1, scaleX: 1, duration: 0.3, ease: "elastic.out(1,0.5)", immediateRender: false }, t);
};
// SVG group (inside a translate wrapper) pops up from its own origin
EK.spop = function (tl, sel, t) {
  tl.fromTo(sel, { opacity: 0, scale: 0.3, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t);
};
// a title lands and holds
EK.land = function (tl, sel, t) {
  tl.fromTo(sel, { opacity: 0, scale: 1.45 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, t);
};
