/* Souk Al-Manakh drawing kit: faceless silhouettes, the cheque, buildings and props.
   Same rules as edison-stole/STYLE.md (flat fills, one dark outline, no gradients),
   in a sand and olive palette. Red is only for loss and the bounced cheque. */
window.MK = (function () {
  const INK = "#23261A", SAND = "#E6D5B0", PAPER = "#F6EEDA", OLIVE = "#5B6236", DARK = "#353A20",
    FACE = "#6E744A", RED = "#C23B2B", STONE = "#CDBE95", SHADE = "#4A4F30", LINE = "#B9AB84";
  const S = (w) => `stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  /* set an SVG group's pivot once, before any tween touches it */
  const pivot = (sel, xy) => gsap.set(sel, { svgOrigin: xy });
  const fill = (id, html) => { document.getElementById(id).innerHTML = html; };

  /* an arm that points sideways; rotate it about its shoulder (svgOrigin "sx -285") */
  function arm(p, side, body) {
    const sx = side === "l" ? -56 : 56, d = side === "l" ? -1 : 1;
    return `<g id="${p}-arm"><path d="M${sx} -285 L${sx + d * 150} -285" stroke="${INK}" stroke-width="48" stroke-linecap="round" fill="none"/>` +
      `<path d="M${sx} -285 L${sx + d * 150} -285" stroke="${body}" stroke-width="36" stroke-linecap="round" fill="none"/>` +
      `<circle cx="${sx + d * 166}" cy="-285" r="21" fill="${FACE}" ${S(6)}/></g>`;
  }
  /* a standing man in dishdasha, ghutra and agal, no face. Origin: feet centre; 420 tall.
     o.arm "l" | "r" adds a pointing arm, o.bisht adds a cloak, o.body overrides the robe colour */
  function man(p, o) {
    o = o || {};
    const body = o.body || DARK;
    const bisht = o.bisht
      ? `<path d="M-78 -262 L-96 0 L-30 0 L-16 -300 Z M78 -262 L96 0 L30 0 L16 -300 Z" fill="#1E2113" ${S(6)}/><path d="M-20 -296 L-33 -4 M20 -296 L33 -4" stroke="${STONE}" stroke-width="6" fill="none"/>`
      : "";
    return `<g id="${p}">` + (o.arm && o.armBack ? arm(p, o.arm, body) : "") +
      `<path d="M-70 -250 Q-70 -305 -30 -310 L30 -310 Q70 -305 70 -250 L62 0 L-62 0 Z" fill="${body}" ${S(7)}/>` + bisht +
      `<ellipse cx="0" cy="-352" rx="40" ry="48" fill="${FACE}" ${S(6)}/>` +
      `<path d="M-50 -372 Q-48 -420 0 -422 Q48 -420 50 -372 L80 -258 Q60 -282 40 -274 L36 -356 Q0 -376 -36 -356 L-40 -274 Q-60 -282 -80 -258 Z" fill="${PAPER}" ${S(6)}/>` +
      `<path d="M-45 -398 Q0 -416 45 -398 M-47 -384 Q0 -402 47 -384" stroke="#15170D" stroke-width="9" fill="none" stroke-linecap="round"/>` +
      (o.arm && !o.armBack ? arm(p, o.arm, body) : "") + `</g>`;
  }
  /* a woman in abaya, no face */
  function woman(p) {
    return `<g id="${p}"><path d="M0 -404 Q-56 -404 -56 -346 Q-56 -306 -82 -262 L-72 0 L72 0 L82 -262 Q56 -306 56 -346 Q56 -404 0 -404 Z" fill="#1E2113" ${S(7)}/>` +
      `<ellipse cx="0" cy="-346" rx="31" ry="38" fill="${FACE}" ${S(6)}/></g>`;
  }
  /* a child: big head, small cap */
  function kid(p) {
    return `<g id="${p}"><path d="M-62 -210 Q-62 -262 -24 -266 L24 -266 Q62 -262 62 -210 L56 0 L-56 0 Z" fill="${DARK}" ${S(8)}/>` +
      `<circle cx="0" cy="-322" r="58" fill="${FACE}" ${S(8)}/><path d="M-52 -348 Q0 -412 52 -348 Z" fill="${PAPER}" ${S(8)}/></g>`;
  }
  /* the cheque: 300 x 140, origin at its centre */
  function cheque(p, extra) {
    return `<g id="${p}"><rect x="-150" y="-70" width="300" height="140" rx="8" fill="${PAPER}" ${S(6)}/>` +
      `<path d="M-147 -67 h294 v26 h-294 z" fill="${OLIVE}"/>` +
      `<path d="M-126 -14 H40 M-126 12 H0" stroke="${LINE}" stroke-width="6" stroke-linecap="round" fill="none"/>` +
      `<rect x="56" y="-28" width="76" height="40" rx="4" fill="#EADFC0" ${S(4)}/>` +
      `<path d="M38 46 q12 -16 24 0 t24 0 t24 0" ${S(4)} fill="none"/>` + (extra || "") + `</g>`;
  }
  /* multi-storey car park. Origin: bottom centre. Each floor is its own group ${p}-f0.. so it can be built up */
  function park(p, floors, w, fh) {
    let out = `<g id="${p}">`;
    for (let i = 0; i < floors; i++) {
      const y = -(i + 1) * fh;
      let cols = "";
      const n = Math.round(w / 110);
      for (let k = 1; k < n; k++) cols += `<rect x="${-w / 2 + (w / n) * k - 8}" y="${y + fh * 0.3}" width="16" height="${fh * 0.7}" fill="${STONE}" ${S(4)}/>`;
      out += `<g id="${p}-f${i}"><rect x="${-w / 2}" y="${y}" width="${w}" height="${fh}" fill="${SHADE}" ${S(7)}/>${cols}` +
        `<rect x="${-w / 2 - 10}" y="${y}" width="${w + 20}" height="${fh * 0.3}" rx="5" fill="${STONE}" ${S(7)}/></g>`;
    }
    const ty = -floors * fh;
    out += `<g id="${p}-ac">`;
    for (let k = 0; k < 3; k++) {
      const x = -w / 2 + w * (0.2 + k * 0.3) - 34;
      out += `<g><rect x="${x}" y="${ty - 46}" width="68" height="46" rx="5" fill="${PAPER}" ${S(6)}/><path d="M${x + 12} ${ty - 30} h44 M${x + 12} ${ty - 17} h44" stroke="${INK}" stroke-width="4" fill="none"/></g>`;
    }
    return out + `</g></g>`;
  }
  /* an 80s bank front, no name or logo. Origin: bottom centre. Windows are ${p}-win */
  function bank(p, w, h) {
    let win = "";
    for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) {
      win += `<rect x="${-w / 2 + w * (0.14 + c * 0.27)}" y="${-h * (0.78 - r * 0.25)}" width="${w * 0.18}" height="${h * 0.16}" rx="3" ${S(5)}/>`;
    }
    return `<g id="${p}"><rect id="${p}-body" x="${-w / 2}" y="${-h}" width="${w}" height="${h}" fill="${STONE}" ${S(7)}/>` +
      `<rect x="${-w / 2 - 12}" y="${-h - 26}" width="${w + 24}" height="34" rx="5" fill="${OLIVE}" ${S(7)}/>` +
      `<g id="${p}-win" fill="${PAPER}">${win}</g>` +
      `<rect x="${-w * 0.13}" y="${-h * 0.3}" width="${w * 0.26}" height="${h * 0.3}" fill="${DARK}" ${S(6)}/></g>`;
  }
  /* a teller's window in a wall, with a counter. Draws into a 1080 stage; window centre x = cx */
  function tellerWindow(p, cx) {
    let bars = "";
    for (let k = 0; k < 5; k++) bars += `<path d="M${cx - 160 + k * 80} 470 V780" ${S(7)} fill="none"/>`;
    return `<g id="${p}"><rect x="${cx - 290}" y="330" width="580" height="850" fill="${OLIVE}" ${S(8)}/>` +
      `<rect x="${cx - 290}" y="330" width="580" height="60" fill="${DARK}" ${S(8)}/>` +
      `<rect x="${cx - 200}" y="450" width="400" height="400" rx="10" fill="#D8C99B" ${S(8)}/>` +
      `<g transform="translate(${cx},1010) scale(0.95)">${man(p + "-teller")}</g>` +
      `<rect x="${cx - 200}" y="780" width="400" height="70" fill="#D8C99B"/>` + bars +
      `<path d="M${cx - 200} 560 H${cx + 200}" ${S(7)} fill="none"/>` +
      `<rect x="${cx - 200}" y="450" width="400" height="400" rx="10" fill="none" ${S(8)}/>` +
      `<rect x="${cx - 110}" y="800" width="220" height="50" fill="${INK}"/>` +
      `<rect x="${cx - 250}" y="850" width="500" height="46" rx="6" fill="${STONE}" ${S(8)}/>` +
      `<rect x="${cx - 220}" y="896" width="440" height="284" fill="${DARK}" ${S(8)}/></g>`;
  }
  /* a kneeling camel, facing left. Origin: bottom centre, about 360 x 230 */
  function camel(p) {
    const C = "#B0935A";
    return `<g id="${p}"><path d="M-96 -70 Q-168 -84 -164 -178" stroke="${INK}" stroke-width="52" fill="none" stroke-linecap="round"/>` +
      `<path d="M150 -70 q34 20 26 58" ${S(8)} fill="none"/>` +
      `<path d="M-130 -4 Q-150 -70 -96 -96 Q-48 -104 -28 -160 Q8 -214 44 -160 Q62 -108 108 -92 Q160 -72 150 -4 Z" fill="${C}" ${S(8)}/>` +
      `<path d="M-96 -70 Q-168 -84 -164 -178" stroke="${C}" stroke-width="37" fill="none" stroke-linecap="round"/>` +
      `<path d="M-150 -204 Q-196 -214 -226 -190 Q-236 -172 -214 -166 L-158 -160 Q-138 -180 -150 -204 Z" fill="${C}" ${S(8)}/>` +
      `<path d="M-156 -204 l10 -22 l10 20" fill="${C}" ${S(7)}/>` +
      `<ellipse cx="-74" cy="-10" rx="52" ry="17" fill="#977C48" ${S(7)}/><ellipse cx="86" cy="-10" rx="52" ry="17" fill="#977C48" ${S(7)}/></g>`;
  }
  /* a clock tower for London. Origin: bottom centre */
  function tower(p) {
    return `<g id="${p}"><rect x="-38" y="-230" width="76" height="230" fill="#9A9777" ${S(7)}/>` +
      `<path d="M-46 -230 h92 l-10 -34 h-72 z" fill="#7F7C5E" ${S(7)}/><path d="M-30 -264 L0 -330 L30 -264 Z" fill="${DARK}" ${S(7)}/>` +
      `<circle cx="0" cy="-184" r="27" fill="${PAPER}" ${S(6)}/><path d="M0 -184 V-202 M0 -184 h12" ${S(5)} fill="none"/>` +
      `<path d="M-18 -130 V-20 M0 -130 V-20 M18 -130 V-20" stroke="${INK}" stroke-width="4" fill="none"/></g>`;
  }
  function barrel(p) {
    return `<g id="${p}"><rect x="-80" y="-220" width="160" height="220" rx="16" fill="${OLIVE}" ${S(8)}/>` +
      `<path d="M-80 -150 h160 M-80 -70 h160" ${S(7)} fill="none"/>` +
      `<path d="M0 -140 Q-26 -106 0 -88 Q26 -106 0 -140 Z" fill="${INK}"/></g>`;
  }
  /* the judge's gavel, head up. Rotate about the end of its handle (svgOrigin "0 0") */
  function gavel(p) {
    return `<g id="${p}"><rect x="-13" y="-250" width="26" height="250" rx="10" fill="#8A6B3C" ${S(7)}/>` +
      `<rect x="-90" y="-300" width="180" height="96" rx="14" fill="${DARK}" ${S(8)}/>` +
      `<path d="M-60 -300 v96 M60 -300 v96" stroke="${STONE}" stroke-width="7" fill="none"/></g>`;
  }
  /* the dock: a wooden rail the accused stands behind. Origin: bottom centre */
  function dock(p, w) {
    let posts = "";
    for (let k = 0; k <= 6; k++) posts += `<rect x="${-w / 2 + 14 + (k * (w - 50)) / 6}" y="-120" width="22" height="120" fill="#8A6B3C" ${S(6)}/>`;
    return `<g id="${p}">${posts}<rect x="${-w / 2}" y="-150" width="${w}" height="40" rx="8" fill="#A8854C" ${S(7)}/><rect x="${-w / 2}" y="-26" width="${w}" height="30" rx="6" fill="#A8854C" ${S(7)}/></g>`;
  }

  /* motion helpers */
  function pop(tl, sel, t, rot, late) {
    tl.fromTo(sel, { opacity: 0, scale: 0.4, rotation: (rot || 0) - 8 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.3, ease: "back.out(2)", immediateRender: !late }, t);
  }
  function out(tl, sel, t) { tl.to(sel, { opacity: 0, scale: 0.6, duration: 0.18, ease: "power2.in" }, t); }
  function shake(tl, stageSel, t, amt) {
    tl.fromTo(stageSel, { x: 0, y: 0 }, { x: amt || 9, y: -(amt || 9) * 0.8, duration: 0.045, ease: "none", yoyo: true, repeat: 5, immediateRender: false }, t);
  }
  /* late: true when the element is already on screen earlier in the scene, so the slam does not hide it at build time */
  function stamp(tl, sel, stageSel, t, rot, late) {
    tl.fromTo(sel, { opacity: 0, scale: 2.8, rotation: (rot || 0) - 10 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.17, ease: "power3.in", immediateRender: !late }, t - 0.17);
    shake(tl, stageSel, t);
    tl.fromTo(sel, { scale: 1 }, { scale: 0.96, duration: 0.07, yoyo: true, repeat: 1, ease: "power1.inOut", immediateRender: false }, t);
  }
  const fmt = (n) => Math.round(n).toLocaleString("en-US");
  /* typewriter count-up: the number is a function of timeline time (no callbacks, so any seek shows the right digits) */
  function count(tl, sel, a, b, t, dur, pre, plain) {
    const f = plain ? (n) => String(Math.round(n)) : fmt;
    tl.fromTo(sel, { textContent: a }, { textContent: b, duration: dur, ease: "power2.out", modifiers: { textContent: (v) => (pre || "") + f(parseFloat(v)) } }, t);
  }
  /* typewriter text: letters arrive one by one */
  function type(tl, sel, text, t, dur) {
    gsap.set(sel, { opacity: 0 }); tl.set(sel, { opacity: 1 }, t);
    tl.fromTo(sel, { textContent: 0 }, { textContent: text.length, duration: dur, ease: "none", modifiers: { textContent: (v) => text.slice(0, Math.round(parseFloat(v))) } }, t);
  }
  /* draw a line or path on */
  function draw(tl, sel, t, dur) {
    document.querySelectorAll(sel).forEach((el) => {
      const L = el.getTotalLength();
      el.style.strokeDasharray = L; el.style.strokeDashoffset = L;
      tl.to(el, { strokeDashoffset: 0, duration: dur || 0.3, ease: "power2.out" }, t);
    });
  }
  return { pivot, INK, SAND, PAPER, OLIVE, DARK, FACE, RED, STONE, SHADE, S, fill, man, woman, kid, cheque, park, bank, tellerWindow, camel, tower, barrel, gavel, dock, pop, out, shake, stamp, count, type, draw, fmt };
})();
