#!/usr/bin/env python3
"""Generate the Al Fardan Abu Dhabi plan composition files (static HTML)."""
import json, os, sys

P = sys.argv[1]
FPS = 30
END = 58.95  # footage is 58.977 s

# ---------------------------------------------------------------- words
wl = json.load(open(os.path.join(P, 'assets/source/wl.json')))
W = []
for s in wl['transcription']:
    t = s['text'].strip()
    if t:
        W.append([s['offsets']['from'] / 1000, s['offsets']['to'] / 1000, t])

# corrections, 1:1 by position (whisper text -> spoken words)
fix = {
    'تخيل': 'تخيل', 'انك': 'إنك', 'تزورها': 'تزور', 'لمواكن': 'هالأماكن', 'بوضابي': 'أبوظبي',
    'المطار': 'المطار', 'الصباح': 'الصبح', 'اول': 'أول', 'القرن': 'القرم', 'اشجار': 'أشجار',
    'تجربة': 'تجرب', 'بذلتها': 'بذلته', 'اكيد': 'أكيد', 'يعان': 'جوعان', 'احد': 'أحد',
    'افضل': 'أفضل', 'الاماراتية': 'الإماراتية', 'الغدى': 'الغدا', 'احلى': 'أحلى',
    'كرنيش': 'كورنيش', 'اطلالة': 'إطلالة', 'اجمل': 'أجمل', 'اطلالات': 'إطلالات',
    'واطلالة': 'وإطلالة', 'الى': 'إلى', 'واوعدك': 'وأوعدك', 'باماكن': 'بأماكن',
    'وتجارة': 'وتجارب', 'بيديدة': 'جديدة', 'عشاء': 'عشا',
}
out = []
i = 0
while i < len(W):
    a, b, t = W[i]
    if t == 'المطار' and i < 20:      # "توصل المطار زايد" -> مطار زايد
        out.append([a, b, 'مطار']); i += 1; continue
    if t == 'ماعدنا':
        m = (a + b) / 2; out += [[a, m - .02, 'ما'], [m, b, 'عندنا']]; i += 1; continue
    if t == 'يا' and W[i + 1][2] == 'موعد':
        out.append([a, b, 'جا']); i += 1; continue
    if t == 'سيفود':
        m = a + (b - a) * .4; out += [[a, m, 'سي'], [m, b, 'فود']]; i += 1; continue
    if t == 'ياسبي':
        m = a + (b - a) * .5; out += [[a, m, 'ياس'], [m, b, 'باي']]; i += 1; continue
    if t == 'الي' and W[i + 1][2] == 'آية':
        out.append([a, W[i + 1][1], 'الجاية']); i += 2; continue
    if t == 'بارتبلك':
        m = a + (b - a) * .62; out += [[a, m, 'بارتب'], [m, b, 'لك']]; i += 1; continue
    if t == 'تشوف' and a > 29:       # whisper lost 27.2-30 s; rebuilt below
        i += 1; continue
    if t in ('الهيبة', 'والفخامة'):
        i += 1; continue
    out.append([a, b, fix.get(t, t)]); i += 1

# the stretch whisper dropped (re-transcribed separately, timed to the pauses)
gap = [[27.26, 27.78, 'والحين'], [27.95, 28.24, 'على'], [28.24, 28.58, 'قصر'], [28.58, 28.97, 'الوطن'],
       [29.30, 29.60, 'هني'], [29.60, 30.20, 'بتشوف'], [30.25, 30.75, 'الهيبة'], [30.75, 31.29, 'والفخامة']]
out = [w for w in out if w[0] < 27.2] + gap + [w for w in out if w[0] >= 31.3]
out.sort(key=lambda w: w[0])

def setstart(word, t):
    for w in out:
        if w[2] == word and abs(w[0] - t) < .4:
            w[0] = t; return
    raise SystemExit('no ' + word)
setstart('توصل', 4.45); setstart('يلا', 9.64); setstart('عندنا', 10.80)
for w in out:
    if w[2] == 'ما' and 10 < w[0] < 11: w[0] = 10.58
    if w[2] == 'الغالي': w[1] = 10.40
    if w[2] == 'بالعافية': w[1] = 27.14
    if w[2] == 'عليك' and 33 < w[0] < 33.2: w[0] = 33.15
    if w[2] == 'فقط': w[1] = 4.14
    if w[2] == 'أبوظبي' and 8.5 < w[0] < 9.3: w[1] = 9.27
# the last sentence: whisper ran 1.46 s past the end of the file; compress it
for w in out:
    for k in (0, 1):
        if w[k] > 53.55: w[k] = 53.55 + (w[k] - 53.55) * (58.90 - 53.55) / (60.44 - 53.55)
words = [{'id': 'w%d' % n, 'text': w[2], 'start': round(w[0], 3), 'end': round(w[1], 3)} for n, w in enumerate(out)]
json.dump(words, open(os.path.join(P, 'assets/transcript.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- caption groups
KEY = {'24', 'ساعة', 'مطار', 'زايد', '6', 'الصبح', 'الجبيل', 'القرم', 'الكاياك', 'ميلس', 'قصر', 'الوطن',
       'المرزاب', 'سي', 'فود', 'كورنيش', 'ياس', 'باي', 'المطار', 'جديدة', 'ومختلفة', 'تماماً', 'أبوظبي', 'الغروب', 'الغدا'}
breaks_after = {'أبوظبي', 'فقط', 'الصبح', 'الغالي', 'وقت', 'عندك', 'الجبيل', 'هناك', 'بالطبيعة', 'الكاياك', 'بذلته',
                'جوعان', 'ميلس', 'الإماراتية', 'بالعافية', 'والحين', 'الوطن', 'والفخامة', 'الغدا', 'المرزاب', 'حياتك',
                'الغروب', 'البحر', 'العاصمة', 'الحلوة', 'يومك', 'البحرية', 'للأسف', 'المطار', 'الجاية', 'ثاني', 'زايد', 'باي', 'البحرية', 'بتتمشي', 'القرم', 'إطلالة', 'وهني'}
GROUPS = """تخيل إنك تقدر تزور | هالأماكن كلها في أبوظبي | خلال 24 ساعة فقط | توصل مطار زايد | الساعة 6 الصبح | تستلم موترك | وهني تبدأ رحلتنا في أبوظبي | يلا الغالي | ما عندنا وقت | أول محطة بتكون عندك | في الممشى الخشبي | اللي في جزيرة الجبيل | هناك بتتمشي | وسط أشجار القرم | وتستمتع بالطبيعة | وبتكون عندك فرصة | تجرب الكاياك | وبعد هالمجهود اللي بذلته | أكيد إنك جوعان | عليك بمطعم ميلس | أحد أفضل المطاعم الإماراتية | عليك بالعافية | والحين | على قصر الوطن | هني بتشوف | الهيبة والفخامة | والحين جا موعد الغدا | عليك بمطعم المرزاب | بتاكل أحلى سي فود | في حياتك | ووقت الغروب | لا تفوت كورنيش أبوظبي | هناك بتتمشي على البحر | وبتشوف إطلالة | من أجمل إطلالات العاصمة | وعقب هالتمشية الحلوة | هني بتختم يومك | في ياس باي | عشا على البحر | وإطلالة على الواجهة البحرية | والحين للأسف | حان موعد العودة | إلى المطار | وأوعدك الزيارة الجاية | بارتب لك جدول ثاني | بأماكن وتجارب جديدة | ومختلفة تماماً"""
groups, k = [], 0
for chunk in GROUPS.split("|"):
    n = len(chunk.split())
    g = words[k:k + n]
    assert " ".join(x["text"] for x in g) == chunk.strip(), (chunk, [x["text"] for x in g])
    groups.append(g); k += n
assert k == len(words)
cap_html = []
for g, ws in enumerate(groups):
    gs = max(0.15, ws[0]['start'] - 0.08)
    ge = ws[-1]['end'] + 0.05
    if g + 1 < len(groups):
        ge = min(ge + 0.25, groups[g + 1][0]['start'] - 0.08)
    ge = min(ge, END - 0.02)
    spans = ''.join('<span class="cw%s" id="c%d-%d" data-ws="%.3f">%s</span> ' %
                    (' key' if w['text'] in KEY else '', g, k, w['start'], w['text']) for k, w in enumerate(ws))
    cap_html.append('      <div class="cg" id="cg%d" data-gs="%.3f" data-ge="%.3f"><span class="cline">%s</span></div>' % (g, gs, ge, spans.strip()))

captions = """<template>
  <style>
    @font-face { font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }
    @font-face { font-family: "Lalezar"; src: url("assets/fonts/Lalezar-Regular.ttf"); font-weight: 400; }
    #root { position: absolute; inset: 0; overflow: visible; }
    #cap-wrap { position: absolute; inset: 0; }
    .cg { position: absolute; left: 0; right: 0; top: 1130px; text-align: center; direction: rtl; opacity: 0; overflow: visible; }
    .cline { display: inline-block; max-width: 960px; font-family: "Noto Kufi Arabic", sans-serif; font-weight: 900;
      font-size: 70px; line-height: 1.5; color: #fff; -webkit-text-stroke: 14px #0a0e18; paint-order: stroke fill;
      text-shadow: 0 10px 22px rgba(0, 0, 0, 0.55); }
    .cw { display: inline-block; opacity: 0; margin: 0 4px; }
    .cw.key { color: #f2c14e; font-family: "Lalezar", sans-serif; font-weight: 400; font-size: 96px; line-height: 1; }
  </style>
  <div id="root" data-composition-id="cap" data-width="1080" data-height="1920">
    <div id="cap-wrap" class="clip" data-start="0" data-duration="%(END)s" data-layout-allow-overflow>
%(groups)s
    </div>
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      document.querySelectorAll("#cap-wrap .cg").forEach((g) => {
        const gs = +g.dataset.gs, ge = +g.dataset.ge;
        tl.set(g, { opacity: 1 }, gs);
        g.querySelectorAll(".cw").forEach((w) => {
          const ws = Math.max(gs, +w.dataset.ws - 0.04), key = w.classList.contains("key");
          if (key) tl.fromTo(w, { opacity: 0, y: 40, scale: 0.4, rotation: -8 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(2.6)" }, ws);
          else tl.fromTo(w, { opacity: 0, y: 28, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(1.8)" }, ws);
        });
        tl.to(g, { opacity: 0, y: -18, duration: 0.12, ease: "power2.in" }, ge - 0.12);
        tl.set(g, { opacity: 0, visibility: "hidden" }, ge);
      });
      window.__timelines["cap"] = tl;
    })();
  </script>
</template>
""" % {'END': END, 'groups': '\n'.join(cap_html)}
open(os.path.join(P, 'compositions/cap.html'), 'w').write(captions)

# ---------------------------------------------------------------- place cards
IMG = {
    'airport': ('assets/places/05-zayed-airport.jpg', 588, 441),
    'jubail': ('assets/places/01-jubail-mangrove-park.jpg', 800, 450),
    'meylas': ('assets/places/03-meylas-restaurant.jpg', 1440, 960),
    'watan': ('assets/places/04-qasr-al-watan-crop.jpg', 769, 640),
    'mirzab': ('assets/places/07-al-mirzab-restaurant.jpg', 386, 518),
    'corniche': ('assets/places/06-corniche.webp', 1500, 800),
    'kayak': ('assets/places/08-jubail-kayak.jpg', 1300, 867),
    'yasbay': ('assets/places/02-yas-bay-waterfront.jpg', 831, 831),
}
# id, image, chip, title, extra chip, big-in, shrink (None = leave from big), out, extra-chip time
STOPS = [
    ('st0', 'airport', 'الوصول', 'مطار زايد الدولي', '6:00 الصبح', 4.62, 6.75, 9.30, 5.45),
    ('st1', 'jubail', 'المحطة 1', 'ممشى القرم · جزيرة الجبيل', None, 12.72, 14.85, 18.7, None),
    ('st2', 'meylas', 'المحطة 2', 'مطعم ميلس', 'مطبخ إماراتي', 23.10, 25.10, 27.16, 24.67),
    ('st3', 'watan', 'المحطة 3', 'قصر الوطن', None, 28.20, 29.60, 31.42, None),
    ('st4', 'mirzab', 'المحطة 4', 'مطعم المرزاب', 'سي فود', 33.50, 35.40, 36.95, 35.78),
    ('st5', 'corniche', 'المحطة 5', 'كورنيش أبوظبي', 'وقت الغروب', 38.42, 40.40, 43.50, 38.42),
    ('st6', 'yasbay', 'المحطة 6', 'ياس باي', 'عشا على البحر', 46.80, 48.70, 50.40, 47.57),
    ('st7', 'kayak', 'تجربة', 'كاياك بين أشجار القرم', None, 19.15, None, 21.3, None),
]
BOXW, BOXH, BIGCY = 940, 760, 735
SLOTH, SLOTCY = 240, 355
PIN = '<svg class="pin" viewBox="0 0 24 24" width="46" height="46"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z" fill="#f2c14e"/></svg>'
hosts, sfx = [], []
whooshes = ['whoosh_soft_01', 'whoosh_soft_13', 'whoosh_soft_21']
WH = {'whoosh_soft_01': (0.928, 0.372), 'whoosh_soft_13': (0.676, 0.283), 'whoosh_soft_21': (1.048, 0.495)}
for n, (sid, im, chip, title, extra, tin, tsh, tout, tex) in enumerate(STOPS):
    src, iw, ih = IMG[im]
    s = min(BOXW / iw, BOXH / ih)
    w, h = round(iw * s), round(ih * s)
    left, top = (1080 - w) // 2, BIGCY - h // 2
    dur = round(tout - tin + 0.45, 3)
    lt = lambda t: round(t - tin, 3)
    small = SLOTH / h
    dy = SLOTCY - BIGCY
    small_label_top = SLOTCY + SLOTH // 2 + 14
    extra_html = '<div class="xchip" id="%s-x">%s</div>' % (sid, extra) if extra else ''
    shrink_js = ''
    if tsh is not None:
        shrink_js = '''
      tl.to("#%(s)s-scrim", { opacity: 0, duration: 0.4, ease: "power2.out" }, %(sh)s);
      tl.to("#%(s)s-bar, #%(s)s-chip, #%(s)s-back", { opacity: 0, duration: 0.2, ease: "power2.in" }, %(sh)s);
      tl.to("#%(s)s-card", { y: %(dy)s, scale: %(sm).4f, duration: 0.6, ease: "back.inOut(1.2)" }, %(sh)s);
      tl.fromTo("#%(s)s-label", { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, %(sh2)s);
      tl.to("#%(s)s-card, #%(s)s-label", { opacity: 0, y: "-=40", duration: 0.35, ease: "power2.in" }, %(out)s);''' % dict(
            s=sid, sh=lt(tsh), sh2=lt(tsh + 0.45), dy=dy, sm=small, out=lt(tout))
        exit_t = tout
    else:
        shrink_js = '''
      tl.to("#%(s)s-scrim", { opacity: 0, duration: 0.35, ease: "power2.in" }, %(out)s);
      tl.to("#%(s)s-chip", { opacity: 0, duration: 0.2, ease: "power2.in" }, %(out)s);
      tl.to("#%(s)s-card, #%(s)s-back", { opacity: 0, y: 160, rotation: -6, scale: 0.86, duration: 0.38, ease: "power2.in" }, %(out)s);''' % dict(s=sid, out=lt(tout))
    extra_js = ''
    if extra:
        # the extra chip sits on the big card while it is big, then under the small label
        extra_js = '''
      tl.fromTo("#%(s)s-x", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, %(t)s);''' % dict(s=sid, t=lt(max(tex, tin + 0.5)))
    html = '''<template>
  <style>
    @font-face { font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }
    #root { position: absolute; inset: 0; overflow: hidden; }
    #%(s)s-wrap { position: absolute; inset: 0; }
    #%(s)s-scrim { position: absolute; inset: 0; background: rgba(8, 12, 20, 0.58); opacity: 0; }
    #%(s)s-card { position: absolute; left: %(l)spx; top: %(t)spx; width: %(w)spx; height: %(h)spx; border-radius: 30px;
      border: 8px solid #fff; overflow: hidden; background: #0e1726; box-shadow: 0 24px 60px rgba(0,0,0,0.45); opacity: 0; }
    #%(s)s-back { position: absolute; left: %(l)spx; top: %(t)spx; width: %(w)spx; height: %(h)spx; border-radius: 30px; background: #f2c14e; opacity: 0; }
    #%(s)s-shine { position: absolute; top: -10%%; left: 0; width: 34%%; height: 120%%; opacity: 0.0;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.55), rgba(255,255,255,0)); }
    #%(s)s-img { position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; }
    #%(s)s-bar { position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 28px 26px; direction: rtl;
      background: rgba(10, 14, 24, 0.8); display: flex; align-items: center; gap: 14px; justify-content: flex-start; }
    #%(s)s-bar span { font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: %(fs)spx; color: #fff; line-height: 1.3; }
    #%(s)s-chip { position: absolute; top: %(ct)spx; right: %(cr)spx; padding: 6px 28px 12px; border-radius: 40px; background: #f2c14e;
      font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: 40px; color: #0e1726; direction: rtl; opacity: 0; }
    #%(s)s-label { position: absolute; left: 0; right: 0; top: %(slt)spx; text-align: center; direction: rtl; opacity: 0; }
    #%(s)s-label span { display: inline-block; padding: 4px 26px 10px; border-radius: 30px; background: rgba(10, 14, 24, 0.78);
      font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: 32px; color: #fff; }
    #%(s)s-label b { color: #f2c14e; font-weight: 800; }
    .xchip { position: absolute; padding: 4px 22px 10px; border-radius: 30px; background: #fff; color: #0e1726;
      font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: 34px; direction: rtl; opacity: 0; }
    #%(s)s-x { left: %(xl)spx; top: %(xt)spx; }
  </style>
  <div id="root" data-composition-id="%(s)s" data-width="1080" data-height="1920">
    <div id="%(s)s-wrap" class="clip" data-start="0" data-duration="%(dur)s" data-layout-allow-overlap>
      <div id="%(s)s-scrim"></div>
      <div id="%(s)s-back"></div>
      <div id="%(s)s-card">
        <img id="%(s)s-img" src="%(src)s" alt="%(title)s" />
        <div id="%(s)s-shine"></div>
        <div id="%(s)s-bar">%(pin)s<span data-var-text="%(s)s-title">%(title)s</span></div>
      </div>
      <div id="%(s)s-chip">%(chip)s</div>
      <div id="%(s)s-label"><span><b>%(chip)s</b> · %(title)s</span></div>
      %(extra)s
    </div>
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#%(s)s-scrim", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, 0);
      tl.fromTo("#%(s)s-back", { opacity: 0, y: 260, rotation: 12, scale: 0.8 }, { opacity: 1, y: 0, rotation: %(rot)s, scale: 1, duration: 0.62, ease: "back.out(1.3)" }, 0.05);
      tl.fromTo("#%(s)s-card", { opacity: 0 }, { opacity: 1, duration: 0.18, ease: "none" }, 0);
      tl.fromTo("#%(s)s-card", { y: 300, rotation: %(rot2)s, scale: 0.78 }, { y: 0, rotation: 0, scale: 1, duration: 0.62, ease: "back.out(1.5)" }, 0);
      tl.fromTo("#%(s)s-img", { scale: 1.35 }, { scale: 1.1, duration: 0.9, ease: "power3.out" }, 0);
      tl.to("#%(s)s-img", { scale: 1, duration: %(kb)s, ease: "none" }, 0.9);
      tl.fromTo("#%(s)s-bar", { yPercent: 100 }, { yPercent: 0, duration: 0.42, ease: "power3.out" }, 0.32);
      tl.fromTo("#%(s)s-shine", { xPercent: -160, skewX: -18, opacity: 1 }, { xPercent: 420, skewX: -18, opacity: 1, duration: 0.75, ease: "power2.inOut" }, 0.42);
      tl.fromTo("#%(s)s-chip", { opacity: 0, scale: 0.3, rotation: -14 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.36, ease: "back.out(2.6)" }, 0.38);%(extra_js)s%(shrink_js)s
      tl.to("#%(s)s-x", { opacity: 0, duration: 0.25, ease: "power2.in" }, %(xout)s);
      window.__timelines["%(s)s"] = tl;
    })();
  </script>
</template>
''' % dict(s=sid, l=left, t=top, w=w, h=h, src=src, title=title, chip=chip, pin=PIN, dur=dur,
           fs=50 if len(title) < 16 else 44, ct=top - 34, cr=left + 30, slt=small_label_top,
           extra=extra_html, extra_js=extra_js, shrink_js=shrink_js, kb=round(max(dur - 0.9, 0.3), 3), rot=(-4 if n % 2 == 0 else 4), rot2=(8 if n % 2 == 0 else -8),
           xl=left + 30, xt=top + 34 if True else 0, xout=lt(tsh if tsh else tout) if extra else 0)
    if not extra:
        html = html.replace('\n      tl.to("#%s-x", { opacity: 0, duration: 0.25, ease: "power2.in" }, 0);' % sid, '')
    open(os.path.join(P, 'compositions/%s.html' % sid), 'w').write(html)
    hosts.append('      <div id="%s" data-composition-id="%s" data-composition-src="compositions/%s.html" data-start="%s" data-duration="%s" data-track-index="%d" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:%d"></div>'
                 % (sid, sid, sid, tin, dur, 2 + n % 2, 3))
    wname = whooshes[n % 3]
    d, pk = WH[wname]
    sfx.append((('sfx-in-%d' % n), wname, round(tin + 0.30 - pk + 1 / FPS, 3), d))

# ---------------------------------------------------------------- route tracker
RT0, RT1 = 11.55, 52.75
RX = [900 - k * 144 for k in range(6)]
RY = 205
dots = ''.join('<div class="rt-dot" id="rt-d%d" style="left:%dpx"></div>' % (k, RX[k] - 15) for k in range(6))
mv = []
for k in range(6):
    tin = STOPS[k + 1][5]
    t_arr = round(tin + 0.3 - RT0, 3)
    if k == 0:
        mv.append('tl.fromTo("#rt-pin", { opacity: 0, y: -70 }, { opacity: 1, y: 0, duration: 0.4, ease: "bounce.out" }, %s);' % round(t_arr - 0.4, 3))
    else:
        mv.append('tl.to("#rt-pin", { x: %d, duration: 0.8, ease: "power2.inOut" }, %s);' % (RX[k] - RX[0], round(t_arr - 0.8, 3)))
        mv.append('tl.to("#rt-fill", { scaleX: %.4f, duration: 0.8, ease: "power2.inOut" }, %s);' % (k / 5, round(t_arr - 0.8, 3)))
    mv.append('tl.to("#rt-d%d", { backgroundColor: "#f2c14e", borderColor: "#f2c14e", duration: 0.12, ease: "none" }, %s);' % (k, t_arr))
    mv.append('tl.fromTo("#rt-d%d", { scale: 1 }, { scale: 1.7, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1 }, %s);' % (k, t_arr))
route = """<template>
  <style>
    #root { position: absolute; inset: 0; overflow: hidden; }
    #rt-wrap { position: absolute; inset: 0; }
    #rt-box { position: absolute; inset: 0; }
    #rt-line, #rt-fill { position: absolute; left: %(x1)spx; top: %(ly)spx; width: %(lw)spx; height: 8px; border-radius: 4px; }
    #rt-line { background: rgba(255, 255, 255, 0.45); }
    #rt-fill { background: #f2c14e; }
    .rt-dot { position: absolute; top: %(dy)spx; width: 30px; height: 30px; border-radius: 50%%; background: #0e1726; border: 5px solid #fff; opacity: 0; }
    #rt-pin { position: absolute; left: %(px)spx; top: %(py)spx; width: 56px; height: 56px; opacity: 0; }
  </style>
  <div id="root" data-composition-id="route" data-width="1080" data-height="1920">
    <div id="rt-wrap" class="clip" data-start="0" data-duration="%(dur)s">
      <div id="rt-box">
        <div id="rt-line"></div>
        <div id="rt-fill"></div>
        %(dots)s
        <svg id="rt-pin" viewBox="0 0 24 24"><path d="M12 1.5C7.9 1.5 4.5 4.8 4.5 9c0 5.6 7.5 13.5 7.5 13.5S19.500 14.600 19.500 9c0-4.200-3.400-7.500-7.500-7.500z" fill="#f2c14e" stroke="#0e1726" stroke-width="1.6"/><circle cx="12" cy="9" r="2.800" fill="#0e1726"/></svg>
      </div>
    </div>
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#rt-line", { scaleX: 0, transformOrigin: "100%% 50%%" }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, 0);
      tl.set("#rt-fill", { scaleX: 0, transformOrigin: "100%% 50%%" }, 0);
      document.querySelectorAll("#rt-box .rt-dot").forEach((d, k) => {
        tl.fromTo(d, { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2.5)" }, 0.15 + k * 0.07);
      });
      %(mv)s
      tl.to("#rt-box", { opacity: 0, y: -30, duration: 0.3, ease: "power2.in" }, %(out)s);
      window.__timelines["route"] = tl;
    })();
  </script>
</template>
""" % dict(x1=RX[5], lw=RX[0] - RX[5], ly=RY - 4, dy=RY - 15, px=RX[0] - 28, py=RY - 68, dots=dots,
           dur=round(RT1 - RT0, 3), mv='\n      '.join(mv), out=round(RT1 - RT0 - 0.32, 3))
open(os.path.join(P, 'compositions/route.html'), 'w').write(route)
hosts.append('      <div id="route" data-composition-id="route" data-composition-src="compositions/route.html" data-start="%s" data-duration="%s" data-track-index="6" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:4"></div>' % (RT0, round(RT1 - RT0, 3)))

# ---------------------------------------------------------------- hook (0.15 - 4.4)
hook = '''<template>
  <style>
    @font-face { font-family: "Lalezar"; src: url("assets/fonts/Lalezar-Regular.ttf"); font-weight: 400; }
    @font-face { font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }
    #root { position: absolute; inset: 0; overflow: hidden; }
    #hook-wrap { position: absolute; inset: 0; }
    #hook-box { position: absolute; left: 0; right: 0; top: 196px; text-align: center; direction: rtl; }
    #hook-city { font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: 58px; color: #fff; line-height: 1.3;
      text-shadow: 0 4px 18px rgba(0,0,0,0.6); }
    #hook-row { display: flex; justify-content: center; align-items: baseline; gap: 22px; direction: rtl; margin-top: 4px; }
    #hook-num { font-family: "Lalezar", sans-serif; font-size: 200px; line-height: 1; color: #f2c14e; text-shadow: 0 6px 24px rgba(0,0,0,0.55); min-width: 230px; }
    #hook-unit { font-family: "Lalezar", sans-serif; font-size: 110px; line-height: 1; color: #fff; text-shadow: 0 6px 24px rgba(0,0,0,0.55); }
  </style>
  <div id="root" data-composition-id="hook" data-width="1080" data-height="1920">
    <div id="hook-wrap" class="clip" data-start="0" data-duration="4.25">
      <div id="hook-box">
        <div id="hook-city">أبوظبي في</div>
        <div id="hook-row"><div id="hook-num">00</div><div id="hook-unit">ساعة</div></div>
      </div>
    </div>
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      const num = document.querySelector("#hook-num");
      tl.fromTo("#hook-city", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 0);
      tl.fromTo("#hook-row", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, 0.15);
      const c = { v: 0 };
      tl.to(c, { v: 24, duration: 0.55, ease: "power2.out", onUpdate: () => { num.textContent = String(Math.round(c.v)).padStart(2, "0"); } }, 2.97);
      tl.fromTo("#hook-num", { scale: 1 }, { scale: 1.15, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1 }, 3.5);
      tl.to("#hook-box", { opacity: 0, y: -30, duration: 0.3, ease: "power2.in" }, 3.92);
      window.__timelines["hook"] = tl;
    })();
  </script>
</template>
'''
open(os.path.join(P, 'compositions/hook.html'), 'w').write(hook)
sfx.append(('sfx-hook', 'pop', round(0.15 + 3.52 - 0.014 + 1 / FPS, 3), 0.12))

# ---------------------------------------------------------------- recap (54.15 - END)
REC0 = 54.15
order = ['jubail', 'meylas', 'watan', 'mirzab', 'corniche', 'yasbay']
thumbs = []
for k, im in enumerate(order):
    thumbs.append('<div class="rc-t" id="rc-t%d"><img src="%s" alt="" /><i>✓</i></div>' % (k, IMG[im][0]))
recap = '''<template>
  <style>
    @font-face { font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }
    #root { position: absolute; inset: 0; overflow: hidden; }
    #rc-wrap { position: absolute; inset: 0; }
    #rc-title { position: absolute; left: 0; right: 0; top: 196px; text-align: center; direction: rtl; opacity: 0;
      font-family: "Noto Kufi Arabic", sans-serif; font-weight: 800; font-size: 44px; color: #fff; text-shadow: 0 4px 16px rgba(0,0,0,0.6); }
    #rc-title b { color: #f2c14e; }
    #rc-row { position: absolute; left: 0; right: 0; top: 290px; display: flex; justify-content: center; gap: 14px; direction: rtl; }
    .rc-t { position: relative; width: 132px; height: 132px; border-radius: 22px; border: 5px solid #fff; overflow: hidden;
      box-shadow: 0 10px 26px rgba(0,0,0,0.45); opacity: 0; }
    .rc-t img { width: 100%%; height: 100%%; object-fit: cover; display: block; }
    .rc-t i { position: absolute; left: 6px; bottom: 6px; width: 38px; height: 38px; border-radius: 50%%; background: #f2c14e; color: #0e1726;
      font-style: normal; font-weight: 900; font-size: 26px; line-height: 38px; text-align: center; font-family: sans-serif; }
  </style>
  <div id="root" data-composition-id="recap" data-width="1080" data-height="1920">
    <div id="rc-wrap" class="clip" data-start="0" data-duration="%(dur)s">
      <div id="rc-title">خلصنا <b>6 محطات</b> في يوم واحد</div>
      <div id="rc-row">
        %(thumbs)s
      </div>
    </div>
  </div>
  <script>
    (function () {
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#rc-title", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }, 0.05);
      document.querySelectorAll("#rc-row .rc-t").forEach((t, k) => {
        tl.fromTo(t, { opacity: 0, y: 30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, 0.3 + k * 0.17);
      });
      tl.to("#rc-title, #rc-row", { opacity: 0, duration: 0.3, ease: "power2.in" }, %(fade)s);
      window.__timelines["recap"] = tl;
    })();
  </script>
</template>
''' % dict(dur=round(END - REC0, 3), thumbs='\n        '.join(thumbs), fade=round(END - REC0 - 0.4, 3))
open(os.path.join(P, 'compositions/recap.html'), 'w').write(recap)
ticks = ['soft_tick', 'interface_tick_002']
for k in range(6):
    sfx.append(('sfx-rc-%d' % k, ticks[k % 2], round(REC0 + 0.3 + k * 0.17 + 0.12 + 1 / FPS, 3), 0.06))

# ---------------------------------------------------------------- index
sfx_html = '\n'.join('      <audio id="%s" class="clip" src="assets/sfx/%s.mp3" data-start="%s" data-duration="%s" data-track-index="11" data-volume="%s"></audio>'
                     % (i, f, st, d, 0.3 if 'tick' in f else 0.35) for i, f, st, d in sfx)
index = '''<!doctype html>
<html lang="ar" data-resolution="portrait"
  data-composition-variables='[{"id":"gold","type":"color","label":"Accent","default":"#f2c14e"}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #000; }
      #footage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%(END)s" data-width="1080" data-height="1920">
      <div id="fzoom" style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:1">
        <video id="footage" class="clip" src="assets/footage.mp4" data-start="0" data-duration="%(END)s" data-track-index="0" playsinline data-has-audio="true" data-volume="1"></video>
      </div>

      <div id="hook" data-composition-id="hook" data-composition-src="compositions/hook.html" data-start="0.15" data-duration="4.25" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:3"></div>
%(hosts)s
      <div id="recap" data-composition-id="recap" data-composition-src="compositions/recap.html" data-start="%(REC0)s" data-duration="%(RD)s" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:3"></div>

      <div id="cap" data-composition-id="cap" data-composition-src="compositions/cap.html" data-start="0" data-duration="%(END)s" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:5"></div>

%(sfx)s
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      (function () {
        const tl = gsap.timeline({ paused: true });
        const cuts = [0, 4.367, 11.367, 19.933, 31.5, 37.0, 43.6, 50.5, 53.533, %(END)s];
        for (let i = 0; i < cuts.length - 1; i++) {
          const a = cuts[i], d = cuts[i + 1] - a, inward = i %% 2 === 0;
          tl.fromTo("#fzoom", { scale: inward ? 1 : 1.07, transformOrigin: "50%% 38%%" }, { scale: inward ? 1.07 : 1, duration: d, ease: "none", immediateRender: false }, a);
        }
        window.__timelines["main"] = tl;
      })();
    </script>
  </body>
</html>
''' % dict(END=END, hosts='\n'.join(hosts), REC0=REC0, RD=round(END - REC0, 3), sfx=sfx_html)
open(os.path.join(P, 'index.html'), 'w').write(index)
print('words', len(words), 'groups', len(groups))
for g in groups: print('%.2f-%.2f' % (g[0]['start'], g[-1]['end']), ' '.join(w['text'] for w in g))
