#!/usr/bin/env python3
"""Writes compositions/s1..s11.html from the scene bodies below (markup + timeline script).
   python3 tools/scenes.py && python3 tools/build.py
Every beat is anchored to a script word with w(<word index>), so a new voiceover retimes the film."""
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SVG = '<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0">'
PANEL = '<rect width="1080" height="1920" fill="#13294B"/><g stroke="#172f55" stroke-width="8"><path d="M0 250 H1080 M0 520 H1080 M0 790 H1080 M0 1060 H1080 M0 1330 H1080 M0 1600 H1080"/></g>'
COVER = lambda p: f'''<div id="{p}-cv" style="position:absolute; left:280px; top:300px; width:520px; height:680px">
          <svg viewBox="-280 -360 560 720" width="560" height="720" style="position:absolute; left:-20px; top:-20px"><g id="{p}-cvb"></g></svg>
          <div class="disp" style="position:absolute; left:60px; right:20px; top:110px; text-align:center; font-size:170px; line-height:1.1; color:#F4F6F9">رحلة</div>
          <div class="kufi" style="position:absolute; left:60px; right:20px; top:330px; text-align:center; font-weight:800; font-size:46px; line-height:1.5; color:#e9d9a6">من بطرسبورغ<br/>إلى موسكو</div>'''
S = {}

S["s1"] = (f'''
      <div id="s1-a" class="stage">
        {SVG}<defs><clipPath id="s1-clip"><rect x="-200" y="0" width="1480" height="1160"/></clipPath></defs>
          <g id="s1-lib"></g>
          <g clip-path="url(#s1-clip)"><g id="s1-c-slot" transform="translate(560,940) scale(1.35)"></g></g>
          <g id="s1-desk"></g>
          <g id="s1-book" transform="translate(230,430) rotate(-7)"></g>
          <g id="s1-tool"><g id="s1-toolin" transform="translate(230,400) rotate(-7)"></g></g>
        </svg>
        <div id="s1-q" class="card disp" style="left:470px; top:200px; width:560px; height:170px; font-size:112px; line-height:176px">كتاب رحلات؟</div>
        <div id="s1-ok" class="disp" style="position:absolute; left:105px; top:372px; width:250px; height:110px; text-align:center; font-size:84px; line-height:104px; color:#8c2f2f; border:8px solid #8c2f2f; border-radius:14px; background:#F4F6F9">موافق</div>
      </div>
      <div id="s1-b" class="stage">
        {SVG}{PANEL}<g id="s1-paperup"><g id="s1-paper" transform="translate(540,800)"></g></g></svg>
        <div id="s1-after" class="disp" style="position:absolute; left:60px; right:60px; top:180px; text-align:center; font-size:150px; line-height:1.2; color:#F4F6F9">بعد شهرين</div>
        <div id="s1-m1" class="card disp" style="left:560px; top:400px; width:230px; height:150px; font-size:92px; line-height:156px">شهر</div>
        <div id="s1-m2" class="card disp" style="left:290px; top:400px; width:230px; height:150px; font-size:92px; line-height:156px">شهر</div>
        <div id="s1-pt" class="kufi" style="position:absolute; left:340px; top:560px; width:400px; text-align:center; font-weight:800; font-size:64px; color:#0c1a30">حُكم</div>
        <div id="s1-death" class="plate" style="left:250px; top:770px; width:580px; height:210px; font-size:170px; line-height:214px">الإعدام</div>
      </div>''', '''
    EK.fill("s1-lib", EK.library()); EK.fill("s1-desk", EK.desk()); EK.put("s1-c-slot", "s1-c", "censor");
    EK.fill("s1-book", EK.book(250, 330, "#5b3a24")); EK.fill("s1-toolin", EK.stampTool()); EK.fill("s1-paper", EK.letter(480, 600));
    const w = EK.clock("s1");
    const tl = gsap.timeline({ paused: true });
    EK.face(tl, "s1-c", "flat");
    gsap.set("#s1-q, #s1-ok, #s1-m1, #s1-m2, #s1-death, #s1-b", { opacity: 0 }); gsap.set("#s1-tool", { y: -900 });
    tl.fromTo("#s1-book", { scale: 0.86, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.4, ease: "back.out(2)" }, 0.05);
    EK.blink(tl, "s1-c", 0.5); EK.look(tl, "s1-c", w(2), -11, -7);
    EK.pop(tl, "#s1-q", w(4), 4); EK.mood(tl, "s1-c", w(5), "annoyed"); EK.talk(tl, "s1-c", w(4), w(5) + 0.6);
    EK.mood(tl, "s1-c", w(6), "laugh"); EK.look(tl, "s1-c", w(6) + 0.3, 0, 0);
    EK.out(tl, "#s1-q", w(7));
    tl.to("#s1-tool", { y: 0, duration: 0.2, ease: "power3.in" }, w(7) + 0.25);
    EK.shake(tl, "#s1-a", w(7) + 0.45, 8);
    tl.set("#s1-ok", { opacity: 1, rotation: -11 }, w(7) + 0.45);
    tl.to("#s1-tool", { y: -900, duration: 0.3, ease: "power2.in" }, w(7) + 0.62);
    EK.idle(tl, "s1-c", 0.2, w(8), 2.4);
    // two months later
    EK.cut(tl, "#s1-a", "#s1-b", w(8, -0.12), 1080);
    gsap.set("#s1-paperup, #s1-pt", { y: 1500 });
    tl.fromTo("#s1-after", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, w(8) + 0.05);
    EK.pop(tl, "#s1-m1", w(9), 4); EK.pop(tl, "#s1-m2", w(9) + 0.22, -5);
    EK.out(tl, "#s1-m1, #s1-m2", w(10) + 0.1);
    tl.to("#s1-paperup, #s1-pt", { y: 0, duration: 0.45, ease: "back.out(1.3)" }, w(10));
    EK.stamp(tl, "#s1-death", "#s1-b", w(13), -6);
    window.__timelines["s1"] = tl;''')

S["s2"] = (f'''
      <div id="s2-a" class="stage">
        {SVG}<defs><clipPath id="s2-clip"><rect x="-200" y="0" width="1480" height="1160"/></clipPath></defs>
          <g id="s2-city"></g>
          <g fill="#ffd94a"><rect x="110" y="910" width="30" height="44"/><rect x="520" y="950" width="30" height="44"/><rect x="800" y="940" width="30" height="44"/></g>
          <g clip-path="url(#s2-clip)"><g id="s2-up"><g id="s2-r-slot" transform="translate(540,940) scale(1.35)"></g></g></g>
          <g id="s2-snow"></g>
        </svg>
        <div id="s2-ru" class="disp" style="position:absolute; left:60px; right:60px; top:168px; text-align:center; font-size:150px; line-height:1.2; color:#F4F6F9">روسيا</div>
        <div id="s2-year" class="card disp" style="left:330px; top:356px; width:420px; height:176px; font-size:150px; line-height:186px">١٧٩٠</div>
        <div id="s2-name" class="sign" style="left:110px; top:190px; width:860px; height:170px; font-size:112px; line-height:172px">ألكسندر راديشيف</div>
        <div id="s2-nob" class="card disp" style="left:700px; top:420px; width:320px; height:150px; font-size:104px; line-height:156px">نبيل</div>
        <div id="s2-job" class="card disp" style="left:40px; top:420px; width:500px; height:150px; font-size:92px; line-height:156px">مدير الجمارك</div>
      </div>
      <div id="s2-b" class="stage">
        {SVG}{PANEL}
          <path id="s2-route" d="M250 1120 H830" fill="none" stroke="#F4F6F9" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 26"/>
          <g id="s2-d1"><circle cx="250" cy="1120" r="24" fill="#F4F6F9" stroke="#0c1a30" stroke-width="8"/></g>
          <g id="s2-d2"><circle cx="830" cy="1120" r="24" fill="#CEA532" stroke="#0c1a30" stroke-width="8"/></g>
        </svg>
        {COVER("s2")}</div>
        <div id="s2-l1" class="kufi" style="position:absolute; left:90px; top:1020px; width:320px; text-align:center; font-weight:800; font-size:44px; color:#F4F6F9">بطرسبورغ</div>
        <div id="s2-l2" class="kufi" style="position:absolute; left:670px; top:1020px; width:320px; text-align:center; font-weight:800; font-size:44px; color:#F4F6F9">موسكو</div>
        <div id="s2-inn" class="card disp" style="left:640px; top:200px; width:380px; height:160px; font-size:112px; line-height:166px">بريء؟</div>
      </div>''', '''
    EK.fill("s2-city", EK.square()); EK.fill("s2-snow", EK.snow()); EK.put("s2-r-slot", "s2-r", "radishchev"); EK.fill("s2-cvb", EK.book(520, 680, "#5b3a24"));
    const w = EK.clock("s2");
    const tl = gsap.timeline({ paused: true });
    EK.face(tl, "s2-r", "calm");
    gsap.set("#s2-year, #s2-name, #s2-nob, #s2-job, #s2-b, #s2-inn, #s2-l1, #s2-l2, #s2-d1, #s2-d2", { opacity: 0 });
    EK.whip(tl, "#s2-a", 1080);
    tl.fromTo("#s2-ru", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, 0.25);
    EK.pop(tl, "#s2-year", w(16), -3);
    EK.out(tl, "#s2-ru, #s2-year", w(19) + 0.1);
    tl.fromTo("#s2-up", { y: 800 }, { y: 0, duration: 0.45, ease: "back.out(1.4)" }, w(19));
    EK.pop(tl, "#s2-name", w(21), -2); EK.blink(tl, "s2-r", w(22) + 0.4);
    EK.look(tl, "s2-r", w(23), -9, 0); EK.look(tl, "s2-r", w(25), 9, 0); EK.look(tl, "s2-r", w(27), 0, 0);
    EK.pop(tl, "#s2-nob", w(27), 5); EK.mood(tl, "s2-r", w(27) + 0.1, "smug");
    EK.pop(tl, "#s2-job", w(28) + 0.1, -4);
    EK.idle(tl, "s2-r", w(19) + 0.5, w(32), 2.5);
    // the book and its road
    EK.cut(tl, "#s2-a", "#s2-b", w(32, -0.12), -1080);
    tl.fromTo("#s2-cv", { scale: 0.7, rotation: -8 }, { scale: 1, rotation: -3, duration: 0.45, ease: "back.out(1.6)" }, w(32));
    tl.fromTo("#s2-route", { scaleX: 0, svgOrigin: "250 1120" }, { scaleX: 1, duration: w(38) - w(36), ease: "power1.inOut" }, w(36));
    tl.to("#s2-d1, #s2-l1", { opacity: 1, duration: 0.15 }, w(36)); tl.to("#s2-d2, #s2-l2", { opacity: 1, duration: 0.15 }, w(38));
    tl.fromTo("#s2-d2", { scale: 0.3, svgOrigin: "830 1120" }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, w(38));
    EK.pop(tl, "#s2-inn", w(40), 6);
    tl.to("#s2-cv", { rotation: 2, duration: 0.5, ease: "sine.inOut" }, w(40) + 0.2);
    window.__timelines["s2"] = tl;''')

S["s3"] = (f'''
      <div id="s3-a" class="stage">
        {SVG}<g id="s3-hall"></g><g id="s3-bookup"><g id="s3-book" transform="translate(540,770) rotate(-3)"></g></g><g id="s3-dock"></g>
          <g id="s3-p1" transform="translate(270,1100) rotate(-6)"></g><g id="s3-p2" transform="translate(540,1108) rotate(3)"></g><g id="s3-p3" transform="translate(810,1100) rotate(7)"></g>
        </svg>
        <div id="s3-ttl" class="disp" style="position:absolute; left:40px; right:40px; top:176px; text-align:center; font-size:140px; line-height:1.15; color:#F4F6F9">محكمة التاريخ</div>
        <div id="s3-n" class="plate" style="left:330px; top:352px; width:420px; height:150px; font-size:112px; line-height:152px">ثلاث تهم</div>
      </div>''', '''
    EK.fill("s3-hall", EK.hall()); EK.fill("s3-book", EK.book(300, 400, "#5b3a24")); EK.fill("s3-dock", EK.dockFront());
    ["s3-p1", "s3-p2", "s3-p3"].forEach((id) => EK.fill(id, EK.letter(170, 200)));
    const w = EK.clock("s3");
    const tl = gsap.timeline({ paused: true });
    gsap.set("#s3-ttl, #s3-n", { opacity: 0 }); gsap.set("#s3-p1, #s3-p2, #s3-p3", { opacity: 0 });
    tl.fromTo("#s3-a", { y: 1920 }, { y: 0, duration: 0.42, ease: "power4.out" }, 0);
    tl.fromTo("#s3-bookup", { y: 520 }, { y: 0, duration: 0.5, ease: "back.out(1.5)" }, w(43, -0.15));
    tl.fromTo("#s3-book", { rotation: -3, svgOrigin: "540 970" }, { rotation: 3, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }, w(45));
    tl.fromTo("#s3-ttl", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(46));
    ["#s3-p1", "#s3-p2", "#s3-p3"].forEach((s, i) => { tl.set(s, { opacity: 1 }, w(50) + i * 0.16); tl.from(s, { y: -1300, duration: 0.3, ease: "power3.in" }, w(50) + i * 0.16); });
    EK.stamp(tl, "#s3-n", "#s3-a", w(51), -5);
    window.__timelines["s3"] = tl;''')

S["s4"] = (f'''
      <div id="s4-h" class="stage">{SVG}{PANEL}</svg>
        <div id="s4-count" class="count">التهمة الأولى</div><div id="s4-ttl" class="ttl" style="top:560px; font-size:170px">فضح المستور</div>
      </div>
      <div id="s4-a" class="stage">
        {SVG}<g id="s4-road"></g>
          <g id="s4-u1"><g id="s4-f1" transform="translate(240,1190) scale(1.45)"></g></g>
          <g id="s4-u2"><g id="s4-f2" transform="translate(540,1196) scale(1.6)"></g></g>
          <g id="s4-u3"><g id="s4-f3" transform="translate(840,1190) scale(1.45)"></g></g>
        </svg>
        <div id="s4-pic" class="card" style="left:330px; top:250px; width:420px; height:300px; overflow:hidden">
          <svg viewBox="0 0 420 300" width="406" height="286"><rect width="420" height="300" fill="#9fb4d0"/><circle cx="320" cy="80" r="36" fill="#ffd94a" stroke="#0c1a30" stroke-width="6"/><path d="M-10 300 L120 110 L210 230 L290 150 L430 300Z" fill="#24493f" stroke="#0c1a30" stroke-width="7" stroke-linejoin="round"/></svg>
        </div>
        <div id="s4-auc" class="sign" style="left:300px; top:220px; width:480px; height:170px; font-size:124px; line-height:172px">المزاد</div>
        <div id="s4-t1" class="card disp" style="left:150px; top:930px; width:180px; height:92px; font-size:62px; line-height:96px">للبيع</div>
        <div id="s4-t2" class="card disp" style="left:440px; top:900px; width:200px; height:104px; font-size:70px; line-height:108px">للبيع</div>
        <div id="s4-t3" class="card disp" style="left:750px; top:930px; width:180px; height:92px; font-size:62px; line-height:96px">للبيع</div>
      </div>
      <div id="s4-b" class="stage">
        {SVG}{PANEL}<g id="s4-wk"></g><g id="s4-f4" transform="translate(540,1196) scale(1.5)"></g></svg>
        <div id="s4-six" class="card disp" style="left:330px; top:500px; width:690px; height:140px; font-size:88px; line-height:146px">ستة أيام… أرض سيده</div>
        <div id="s4-sun" class="plate" style="left:60px; top:490px; width:230px; height:150px; font-size:100px; line-height:154px">الأحد</div>
      </div>''', '''
    EK.fill("s4-road", EK.road()); EK.fill("s4-f1", EK.peasant("#55606b")); EK.fill("s4-f2", EK.peasant("#7a6350")); EK.fill("s4-f3", EK.peasant("#4a4038")); EK.fill("s4-f4", EK.peasant("#7a6350"));
    let wk = ""; for (let i = 0; i < 7; i++) wk += `<rect id="s4-d${i}" x="${892 - i * 138}" y="300" width="124" height="170" rx="12" fill="#172f55" stroke="#0c1a30" stroke-width="8"/>`;
    EK.fill("s4-wk", wk);
    const w = EK.clock("s4");
    const tl = gsap.timeline({ paused: true });
    gsap.set("#s4-a, #s4-b, #s4-pic, #s4-auc, #s4-t1, #s4-t2, #s4-t3, #s4-six, #s4-sun, #s4-ttl", { opacity: 0 });
    gsap.set("#s4-u1, #s4-u2, #s4-u3", { y: 1300 });
    EK.whip(tl, "#s4-h", -1080);
    tl.fromTo("#s4-count", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 0.2);
    tl.fromTo("#s4-ttl", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(54));
    // the road: not the scenery, the people
    EK.cut(tl, "#s4-h", "#s4-a", w(56, -0.15), 1080);
    EK.pop(tl, "#s4-pic", w(57), -4);
    tl.to("#s4-pic", { y: 500, rotation: 24, opacity: 0, duration: 0.4, ease: "power2.in" }, w(59) + 0.35);
    tl.to("#s4-u2", { y: 0, duration: 0.45, ease: "back.out(1.3)" }, w(61, -0.1));
    tl.to("#s4-u1", { y: 0, duration: 0.45, ease: "back.out(1.3)" }, w(61) + 0.12);
    tl.to("#s4-u3", { y: 0, duration: 0.45, ease: "back.out(1.3)" }, w(61) + 0.3);
    EK.pop(tl, "#s4-auc", w(68, -0.1), -3);
    EK.pop(tl, "#s4-t2", w(66), -5); EK.pop(tl, "#s4-t1", w(69), 6); EK.pop(tl, "#s4-t3", w(70), -6);
    // the week
    EK.cut(tl, "#s4-a", "#s4-b", w(71, -0.12), -1080);
    for (let i = 0; i < 6; i++) tl.to("#s4-d" + i, { fill: "#8a5a33", duration: 0.12 }, w(71) + i * ((w(76) - w(71)) / 6));
    EK.pop(tl, "#s4-six", w(75), -2);
    tl.fromTo("#s4-d6", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.12, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, w(77));
    tl.to("#s4-d6", { fill: "#CEA532", duration: 0.12 }, w(80));
    EK.stamp(tl, "#s4-sun", "#s4-b", w(80) + 0.12, -5);
    window.__timelines["s4"] = tl;''')

S["s5"] = (f'''
      <div id="s5-h" class="stage">{SVG}{PANEL}</svg>
        <div id="s5-count" class="count">التهمة الثانية</div><div id="s5-ttl" class="ttl" style="top:560px; font-size:190px">التحريض</div>
      </div>
      <div id="s5-a" class="stage">
        {SVG}{PANEL}<g id="s5-ob" transform="translate(540,760)"></g>
          <path id="s5-crack" d="M540 1030 L520 930 L566 850 L524 770 L560 690 L530 610 L548 500" fill="none" stroke="#0c1a30" stroke-width="13" stroke-linejoin="round" stroke-linecap="round"/>
          <path id="s5-crack2" d="M566 850 L640 800 M524 770 L450 730 M560 690 L620 640" fill="none" stroke="#0c1a30" stroke-width="10" stroke-linecap="round"/>
        </svg>
        <div id="s5-boom" class="plate" style="left:250px; top:210px; width:580px; height:200px; font-size:160px; line-height:204px">بينفجر</div>
      </div>
      <div id="s5-b" class="stage">
        {SVG}{PANEL}<g id="s5-crownw"><g id="s5-crown" transform="translate(250,420) scale(1.1)"></g></g></svg>
        <div id="s5-quill" style="position:absolute; left:-420px; top:-65px; width:2000px; height:1500px"></div>
        <div id="s5-free" class="card disp" style="left:560px; top:230px; width:440px; height:180px; font-size:130px; line-height:186px">الحرية</div>
      </div>
      <div id="s5-c" class="stage">
        {SVG}{PANEL}<g id="s5-fl"><g id="s5-fli" transform="translate(540,1010) scale(2.3)"></g></g><g id="s5-pf"><g transform="translate(790,1180) scale(1.55) rotate(8)" id="s5-pfi"></g></g></svg>
        <div id="s5-fr" class="sign" style="left:130px; top:200px; width:820px; height:170px; font-size:112px; line-height:172px">الثورة الفرنسية</div>
        <div id="s5-pe" class="sign" style="left:130px; top:400px; width:820px; height:170px; font-size:112px; line-height:172px">ثورة الفلاحين</div>
      </div>''', '''
    EK.fill("s5-ob", EK.openBook(820, 540)); EK.fill("s5-crown", EK.crown()); EK.fill("s5-fli", EK.flame()); EK.fill("s5-pfi", EK.pitchfork());
    const w = EK.clock("s5");
    const tl = gsap.timeline({ paused: true });
    gsap.set("#s5-a, #s5-b, #s5-c, #s5-boom, #s5-free, #s5-fr, #s5-pe, #s5-ttl", { opacity: 0 }); gsap.set("#s5-pf", { y: 1300 });
    EK.whip(tl, "#s5-h", 1080);
    tl.fromTo("#s5-count", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 0.2);
    tl.fromTo("#s5-ttl", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(84));
    // the page says it plainly
    EK.cut(tl, "#s5-h", "#s5-a", w(85, -0.15), -1080);
    EK.draw(tl, "#s5-crack", w(88), w(90) - w(88) + 0.1); EK.draw(tl, "#s5-crack2", w(90), 0.25);
    EK.stamp(tl, "#s5-boom", "#s5-a", w(90) + 0.3, -6);
    // the ode
    EK.cut(tl, "#s5-a", "#s5-b", w(91, -0.12), 1080);
    EK.lottie(tl, "s5-quill", "quill", w(91), w(97) - w(91), { from: 0, to: 200 });
    EK.pop(tl, "#s5-free", w(94), 4);
    tl.fromTo("#s5-crownw", { y: -700 }, { y: 0, duration: 0.3, ease: "back.out(1.6)" }, w(95) + 0.2);
    tl.to("#s5-crownw", { rotation: -24, y: 50, duration: 0.35, ease: "back.out(2.5)", svgOrigin: "250 510" }, w(96) + 0.1);
    // the timing
    EK.cut(tl, "#s5-b", "#s5-c", w(97, -0.12), -1080);
    EK.pop(tl, "#s5-fr", w(98), -2);
    for (let i = 0; i < 16; i++) tl.to("#s5-fli", { scaleX: i % 2 ? 2.3 : 2.05, scaleY: i % 2 ? 2.3 : 2.55, duration: 0.26, ease: "sine.inOut", transformOrigin: "50% 100%" }, w(97) + i * 0.3);
    tl.to("#s5-fl", { x: -250, duration: 0.4, ease: "power2.inOut" }, w(102, -0.1));
    tl.to("#s5-pf", { y: 0, duration: 0.45, ease: "back.out(1.4)" }, w(102) + 0.1);
    EK.pop(tl, "#s5-pe", w(105, -0.1), 2);
    window.__timelines["s5"] = tl;''')

S["s6"] = (f'''
      <div id="s6-h" class="stage">{SVG}{PANEL}</svg>
        <div id="s6-count" class="count">التهمة الثالثة</div><div id="s6-ttl" class="ttl" style="top:560px; font-size:170px">خداع الرقابة</div>
      </div>
      <div id="s6-a" class="stage">
        {SVG}<defs><clipPath id="s6-clip"><rect x="-200" y="0" width="1480" height="1160"/></clipPath></defs>
          <g id="s6-lib"></g>
          <g clip-path="url(#s6-clip)"><g id="s6-c-slot" transform="translate(560,940) scale(1.35)"></g></g>
          <g id="s6-desk"></g>
          <g id="s6-book" transform="translate(230,430) rotate(-7)"></g>
          <g id="s6-tool"><g id="s6-toolin" transform="translate(230,400) rotate(-7)"></g></g>
        </svg>
        <div id="s6-ok" class="disp" style="position:absolute; left:105px; top:372px; width:250px; height:110px; text-align:center; font-size:84px; line-height:104px; color:#8c2f2f; border:8px solid #8c2f2f; border-radius:14px; background:#F4F6F9">موافق</div>
      </div>
      <div id="s6-b" class="stage">
        {SVG}{PANEL}<g transform="translate(540,1150) scale(1.12)"><g id="s6-pf"></g><g id="s6-pl"></g></g>
          <g id="s6-sheet" transform="translate(540,1050)"></g>
        </svg>
        <div id="s6-home" class="sign" style="left:270px; top:200px; width:540px; height:170px; font-size:124px; line-height:172px">في بيته</div>
      </div>
      <div id="s6-c" class="stage">
        {SVG}{PANEL}</svg>
        {COVER("s6")}
          <div class="kufi" style="position:absolute; left:70px; right:30px; top:540px; text-align:center; font-weight:800; font-size:44px; color:#F4F6F9">المؤلف: ـــــــــــ</div></div>
        <div id="s6-who" class="plate" style="left:640px; top:990px; width:180px; height:170px; font-size:140px; line-height:176px">؟</div>
      </div>''', '''
    EK.fill("s6-lib", EK.library()); EK.fill("s6-desk", EK.desk()); EK.put("s6-c-slot", "s6-c", "censor");
    EK.fill("s6-book", EK.book(250, 330, "#5b3a24")); EK.fill("s6-toolin", EK.stampTool());
    EK.fill("s6-pf", EK.pressFrame()); EK.fill("s6-pl", EK.pressPlaten()); EK.fill("s6-sheet", EK.letter(300, 150)); EK.fill("s6-cvb", EK.book(520, 680, "#5b3a24"));
    const w = EK.clock("s6");
    const tl = gsap.timeline({ paused: true });
    EK.face(tl, "s6-c", "smug");
    gsap.set("#s6-a, #s6-b, #s6-c, #s6-ok, #s6-home, #s6-who, #s6-ttl, #s6-sheet", { opacity: 0 }); gsap.set("#s6-tool", { y: -900 });
    EK.whip(tl, "#s6-h", -1080);
    tl.fromTo("#s6-count", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 0.2);
    tl.fromTo("#s6-ttl", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(109));
    // he stamps without looking
    EK.cut(tl, "#s6-h", "#s6-a", w(111, -0.15), 1080);
    EK.look(tl, "s6-c", w(111) + 0.1, 12, -6);
    tl.to("#s6-c-eyes", { scaleY: 0.08, duration: 0.08, transformOrigin: "50% 50%" }, w(112, -0.1));
    tl.to("#s6-tool", { y: 0, duration: 0.2, ease: "power3.in" }, w(112));
    EK.shake(tl, "#s6-a", w(112) + 0.2, 8);
    tl.set("#s6-ok", { opacity: 1, rotation: -11 }, w(112) + 0.2);
    tl.to("#s6-tool", { y: -900, duration: 0.3, ease: "power2.in" }, w(113));
    // printed at home
    EK.cut(tl, "#s6-a", "#s6-b", w(116, -0.12), -1080);
    for (let i = 0; i < 2; i++) {
      const t = w(117) + i * 0.62;
      tl.to("#s6-pl", { y: 150, duration: 0.2, ease: "power2.in" }, t); tl.to("#s6-pl", { y: 0, duration: 0.26, ease: "power2.out" }, t + 0.24);
    }
    tl.set("#s6-sheet", { opacity: 1 }, w(117) + 0.5);
    tl.fromTo("#s6-sheet", { x: 0, rotation: 0 }, { x: 330, y: -360, rotation: 12, duration: 0.5, ease: "power2.out", immediateRender: false }, w(117) + 0.5);
    EK.pop(tl, "#s6-home", w(118), -3);
    // and no name on it
    EK.cut(tl, "#s6-b", "#s6-c", w(120, -0.3), 1080);
    gsap.set("#s6-cv", { rotation: -3 });
    EK.stamp(tl, "#s6-who", "#s6-c", w(121), 8);
    window.__timelines["s6"] = tl;''')

S["s7"] = (f'''
      <div id="s7-a" class="stage">
        {SVG}<defs><clipPath id="s7-clip"><rect x="-200" y="0" width="1480" height="1160"/></clipPath></defs>
          <g id="s7-pal"></g>
          <g clip-path="url(#s7-clip)"><g id="s7-up"><g id="s7-k-slot" transform="translate(540,960) scale(1.2)"></g></g></g>
          <g id="s7-desk"></g>
          <g id="s7-bk"><g id="s7-book" transform="translate(540,640) rotate(-4)"></g></g>
          <g id="s7-open"><g id="s7-ob" transform="translate(540,350)"></g>
            <path id="s7-page" d="M540 200 Q670 178 800 200 V500 Q670 478 540 500Z" fill="#dfe5ee" stroke="#0c1a30" stroke-width="7" stroke-linejoin="round"/>
            <g id="s7-notes" fill="none" stroke="#8c2f2f" stroke-width="9" stroke-linecap="round"><path class="s7-n" d="M296 250 q14 -12 28 0 t28 0"/><path class="s7-n" d="M296 330 l40 24 l-40 0"/><path class="s7-n" d="M756 270 q-14 -12 -28 0 t-28 0"/><path class="s7-n" d="M740 380 l-22 34 M718 380 l22 34"/></g>
          </g>
        </svg>
        <div id="s7-one" class="card disp" style="left:290px; top:200px; width:500px; height:170px; font-size:112px; line-height:176px">نسخة وحدة</div>
        <div id="s7-name" class="sign" style="left:110px; top:190px; width:860px; height:170px; font-size:108px; line-height:172px">الإمبراطورة كاترين</div>
        <div id="s7-reb" class="plate" style="left:270px; top:190px; width:540px; height:190px; font-size:160px; line-height:194px">متمرّد</div>
        <div id="s7-pug" class="card disp" style="left:200px; top:398px; width:680px; height:100px; font-size:68px; line-height:104px">أسوأ من بوغاتشوف</div>
      </div>''', '''
    EK.fill("s7-pal", EK.palace()); EK.fill("s7-desk", EK.desk()); EK.put("s7-k-slot", "s7-k", "catherine");
    EK.fill("s7-book", EK.book(300, 400, "#5b3a24")); EK.fill("s7-ob", EK.openBook(540, 300));
    const w = EK.clock("s7");
    const tl = gsap.timeline({ paused: true });
    EK.face(tl, "s7-k", "flat");
    gsap.set("#s7-one, #s7-name, #s7-reb, #s7-pug, #s7-open, #s7-page", { opacity: 0 }); gsap.set("#s7-up", { y: 900 });
    EK.whip(tl, "#s7-a", 1080);
    tl.fromTo("#s7-bk", { x: -900, rotation: -30, svgOrigin: "540 640" }, { x: 0, rotation: 0, duration: 0.5, ease: "back.out(1.2)" }, 0.15);
    EK.pop(tl, "#s7-one", w(123), -3);
    EK.out(tl, "#s7-one", w(126, -0.1));
    tl.to("#s7-bk", { x: -330, y: 395, scale: 0.62, duration: 0.4, ease: "power2.inOut", svgOrigin: "540 640" }, w(126, -0.3));
    tl.to("#s7-up", { y: 0, duration: 0.45, ease: "back.out(1.4)" }, w(126, -0.1));
    EK.pop(tl, "#s7-name", w(126) + 0.15, -2);
    EK.blink(tl, "s7-k", w(127) + 0.3);
    // she reads every page
    EK.out(tl, "#s7-name", w(128));
    tl.fromTo("#s7-open", { opacity: 0, scale: 0.5, svgOrigin: "540 350" }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, w(128));
    EK.look(tl, "s7-k", w(128) + 0.1, 0, -9);
    [w(129), w(130)].forEach((t) => { tl.set("#s7-page", { opacity: 1, scaleX: 1 }, t); tl.to("#s7-page", { scaleX: -1, duration: 0.24, ease: "power1.inOut", svgOrigin: "540 350" }, t); tl.set("#s7-page", { opacity: 0 }, t + 0.25); });
    document.querySelectorAll(".s7-n").forEach((el, i) => { const n = Math.ceil(el.getTotalLength()) + 2; el.style.strokeDasharray = n; tl.fromTo(el, { strokeDashoffset: n }, { strokeDashoffset: 0, duration: 0.22, ease: "none" }, w(131) + i * 0.3); });
    EK.mood(tl, "s7-k", w(131) + 0.2, "annoyed");
    // and she says
    EK.out(tl, "#s7-open", w(134) + 0.2);
    EK.mood(tl, "s7-k", w(134), "angry"); EK.look(tl, "s7-k", w(134) + 0.3, 0, 0);
    EK.talk(tl, "s7-k", w(135), w(139) + 0.8);
    EK.stamp(tl, "#s7-reb", "#s7-a", w(136) + 0.15, -5);
    EK.pop(tl, "#s7-pug", w(137), 3);
    EK.idle(tl, "s7-k", w(126) + 0.4, DT.D.s7 - 0.1, 2.5);
    window.__timelines["s7"] = tl;''')

S["s8"] = (f'''
      <div id="s8-a" class="stage">
        {SVG}{PANEL}<g id="s8-paper" transform="translate(540,790)"></g>
          <path id="s8-strike" d="M250 800 L830 730" fill="none" stroke="#0c1a30" stroke-width="18" stroke-linecap="round"/>
        </svg>
        <div id="s8-ttl" class="disp" style="position:absolute; left:60px; right:60px; top:176px; text-align:center; font-size:160px; line-height:1.15; color:#F4F6F9">الحكم</div>
        <div id="s8-death" class="disp" style="position:absolute; left:240px; top:650px; width:600px; text-align:center; font-size:190px; line-height:1.2; color:#8c2f2f">الإعدام</div>
        <div id="s8-ten" class="plate" style="left:230px; top:930px; width:620px; height:190px; font-size:140px; line-height:194px">عشر سنين</div>
      </div>
      <div id="s8-b" class="stage">
        {SVG}<defs><clipPath id="s8-clip"><rect x="-200" y="0" width="1480" height="1170"/></clipPath></defs>
          <rect width="1080" height="1920" fill="#13294B"/>
          <path d="M-10 1000 Q270 930 540 990 Q810 930 1090 1000 V1930 H-10Z" fill="#dfe7f1" stroke="#0c1a30" stroke-width="8"/>
          <g id="s8-t1" transform="translate(130,1080)"></g><g id="s8-t2" transform="translate(960,1090)"></g><g id="s8-t3" transform="translate(300,1010)"></g>
          <g clip-path="url(#s8-clip)"><g id="s8-up"><g id="s8-r-slot" transform="translate(560,950) scale(1.3)"></g></g></g>
          <g id="s8-snowg"></g>
        </svg>
        <div id="s8-lsnow" style="position:absolute; left:0; top:0; width:1080px; height:1920px"></div>
        <div id="s8-sib" class="sign" style="left:190px; top:200px; width:700px; height:170px; font-size:112px; line-height:172px">نفي في سيبيريا</div>
      </div>
      <div id="s8-c" class="stage">
        {SVG}{PANEL}<g id="s8-bk" transform="translate(540,650) rotate(-3)"></g></svg>
        <div id="s8-lock" style="position:absolute; left:340px; top:440px; width:400px; height:400px"></div>
        <div id="s8-cent" class="card disp" style="left:180px; top:990px; width:720px; height:150px; font-size:96px; line-height:156px">أكثر من ١٠٠ سنة</div>
      </div>
      <div id="s8-d" class="stage">
        {SVG}<rect width="1080" height="1920" fill="#13294B"/><g stroke="#172f55" stroke-width="8"><path d="M0 250 H1080 M0 520 H1080 M0 790 H1080 M0 1060 H1080"/></g>
          <g id="s8-pg2" transform="translate(360,800) rotate(-5)"></g>
          <g id="s8-pg" transform="translate(420,800) rotate(3)"><path d="M-200 -260 H200 V260 H-200Z" fill="#f4f6f9" stroke="#0c1a30" stroke-width="7" stroke-linejoin="round"/>
            <g id="s8-lines" fill="none" stroke="#7b8494" stroke-width="8" stroke-linecap="round"><path class="s8-l" d="M160 -200 H-150"/><path class="s8-l" d="M160 -150 H-110"/><path class="s8-l" d="M160 -100 H-160"/><path class="s8-l" d="M160 -50 H-90"/><path class="s8-l" d="M160 0 H-150"/><path class="s8-l" d="M160 50 H-120"/><path class="s8-l" d="M160 100 H-160"/></g></g>
          <g id="s8-hand"><g id="s8-handin" transform="translate(690,960) scale(1.05)"></g></g>
          <g id="s8-desk"></g>
          <g id="s8-cn" transform="translate(900,1150) scale(1.9)"></g>
          <rect id="s8-dark" width="1080" height="1920" fill="#0c1a30"/>
        </svg>
        <div id="s8-copy" class="sign" style="left:210px; top:200px; width:660px; height:170px; font-size:112px; line-height:172px">نسخ بخط اليد</div>
      </div>''', '''
    EK.fill("s8-paper", EK.letter(520, 660)); EK.put("s8-r-slot", "s8-r", "radishchevK"); EK.fill("s8-snowg", EK.snow());
    EK.fill("s8-t1", EK.pine(420)); EK.fill("s8-t2", EK.pine(360)); EK.fill("s8-t3", EK.pine(250));
    EK.fill("s8-bk", EK.book(440, 580, "#5b3a24")); EK.fill("s8-pg2", EK.letter(400, 520)); EK.fill("s8-handin", EK.quillHand("#4a4038")); EK.fill("s8-desk", EK.desk()); EK.fill("s8-cn", EK.candle("s8-flame"));
    const w = EK.clock("s8");
    const tl = gsap.timeline({ paused: true });
    EK.face(tl, "s8-r", "sad");
    gsap.set("#s8-b, #s8-c, #s8-d, #s8-death, #s8-ten, #s8-sib, #s8-cent, #s8-copy", { opacity: 0 }); gsap.set("#s8-dark", { opacity: 0 });
    tl.fromTo("#s8-a", { y: 1920 }, { y: 0, duration: 0.4, ease: "power4.out" }, 0);
    tl.fromTo("#s8-ttl", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, w(140));
    tl.fromTo("#s8-death", { opacity: 0, scale: 2.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.17, ease: "power3.in" }, w(141) - 0.17 + 0.1);
    EK.shake(tl, "#s8-a", w(141) + 0.1, 8);
    EK.draw(tl, "#s8-strike", w(143), 0.35);
    EK.stamp(tl, "#s8-ten", "#s8-a", w(145) + 0.15, 5);
    // Siberia
    EK.cut(tl, "#s8-a", "#s8-b", w(147, -0.12), 1080);
    tl.fromTo("#s8-up", { y: 800 }, { y: 0, duration: 0.45, ease: "back.out(1.3)" }, w(147));
    EK.pop(tl, "#s8-sib", w(148), -2);
    EK.lottie(tl, "s8-lsnow", "snow", w(147, -0.12), 3, { from: 0, to: 90 });
    EK.blink(tl, "s8-r", w(149) + 0.3); EK.look(tl, "s8-r", w(149) + 0.5, 0, 7);
    // the book is banned
    EK.cut(tl, "#s8-b", "#s8-c", w(151, -0.3), -1080);
    EK.lottie(tl, "s8-lock", "padlock", w(151) + 0.1, 0.45, { from: 26, to: 0 });
    EK.shake(tl, "#s8-c", w(151) + 0.55, 6);
    EK.pop(tl, "#s8-cent", w(153), -2);
    // copied by hand, passed in secret
    EK.cut(tl, "#s8-c", "#s8-d", w(156, -0.12), 1080);
    EK.pop(tl, "#s8-copy", w(157), -2);
    document.querySelectorAll(".s8-l").forEach((el, i) => { const n = Math.ceil(el.getTotalLength()) + 2; el.style.strokeDasharray = n; tl.fromTo(el, { strokeDashoffset: n }, { strokeDashoffset: 0, duration: 0.3, ease: "none" }, w(157) + i * 0.33); });
    tl.fromTo("#s8-hand", { rotation: 0, svgOrigin: "690 960" }, { rotation: -6, duration: 0.15, yoyo: true, repeat: 15, ease: "sine.inOut" }, w(157));
    for (let i = 0; i < 10; i++) tl.to("#s8-flame", { scaleX: i % 2 ? 1 : 0.8, scaleY: i % 2 ? 1 : 1.16, duration: 0.28, ease: "sine.inOut", transformOrigin: "50% 100%" }, w(156) + i * 0.3);
    tl.to("#s8-dark", { opacity: 0.4, duration: 0.5, ease: "power1.inOut" }, w(160));
    tl.to("#s8-pg2", { x: -150, rotation: -12, duration: 0.5, ease: "power2.out" }, w(160) + 0.1);
    window.__timelines["s8"] = tl;''')

S["s9"] = (f'''
      <div id="s9-a" class="stage">
        {SVG}{PANEL}<rect x="-10" y="690" width="1100" height="1240" fill="#172f55"/><path d="M-10 690 H1090" stroke="#0c1a30" stroke-width="8"/>
          <g id="s9-top"><path id="s9-fuse" d="M300 330 C380 250 470 430 560 410 S720 400 760 480" fill="none" stroke="#c7ccd6" stroke-width="11" stroke-linecap="round"/>
            <g id="s9-barrel" transform="translate(300,640) scale(1.35)"></g></g>
          <g id="s9-rifle"><g transform="translate(120,960) scale(0.95)" id="s9-rin"></g></g>
          <path class="s9-x" d="M130 860 L600 1060" fill="none" stroke="#8c2f2f" stroke-width="18" stroke-linecap="round"/>
          <path class="s9-x" d="M600 860 L130 1060" fill="none" stroke="#8c2f2f" stroke-width="18" stroke-linecap="round"/>
          <g id="s9-pp"><g id="s9-ppin" transform="translate(830,960) rotate(5)"></g><g id="s9-q" transform="translate(900,880) scale(0.62)"></g></g>
        </svg>
        <div id="s9-spark" style="position:absolute; left:416px; top:249px; width:420px; height:420px"></div>
        <div id="s9-pro" class="sign" style="left:620px; top:180px; width:400px; height:124px; font-size:88px; line-height:126px">الادعاء</div>
        <div id="s9-pow" class="card disp" style="left:210px; top:460px; width:180px; height:92px; font-size:62px; line-height:96px">بارود</div>
        <div id="s9-def" class="sign" style="left:60px; top:712px; width:400px; height:130px; font-size:92px; line-height:132px">الدفاع</div>
      </div>''', '''
    EK.fill("s9-barrel", EK.barrel()); EK.fill("s9-rin", EK.rifle()); EK.fill("s9-ppin", EK.letter(260, 330)); EK.fill("s9-q", EK.quillHand("#3d4a63"));
    const w = EK.clock("s9");
    const tl = gsap.timeline({ paused: true });
    gsap.set("#s9-pro, #s9-pow, #s9-def, #s9-rifle, #s9-pp, #s9-spark", { opacity: 0 }); gsap.set("#s9-top", { opacity: 0 });
    EK.whip(tl, "#s9-a", -1080);
    EK.pop(tl, "#s9-pro", w(162), 2);
    tl.fromTo("#s9-top", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, w(164));
    tl.set("#s9-spark", { opacity: 1 }, w(167));
    EK.lottie(tl, "s9-spark", "spark", w(167), 1.0, { from: 20, to: 80, repeat: 6 });
    EK.pop(tl, "#s9-pow", w(169), -6);
    EK.pop(tl, "#s9-def", w(171), -2);
    tl.fromTo("#s9-rifle", { opacity: 0, x: -500 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.3)" }, w(174));
    EK.draw(tl, ".s9-x", w(176), 0.22);
    tl.fromTo("#s9-pp", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.5)" }, w(177));
    tl.fromTo("#s9-q", { rotation: 0, svgOrigin: "900 880" }, { rotation: -7, duration: 0.14, yoyo: true, repeat: 7, ease: "sine.inOut", immediateRender: false }, w(177) + 0.4);
    window.__timelines["s9"] = tl;''')

S["s10"] = (f'''
      <div id="s10-a" class="stage">
        {SVG}{PANEL}
          <g id="s10-cr"><rect x="150" y="760" width="260" height="330" fill="#6b4226" stroke="#0c1a30" stroke-width="8"/><rect x="120" y="720" width="320" height="56" rx="10" fill="#a8703f" stroke="#0c1a30" stroke-width="8"/><g id="s10-crown" transform="translate(280,620) scale(1.15)"></g></g>
          <g id="s10-mir"><g id="s10-bk" transform="translate(770,780)"></g>
            <rect x="610" y="560" width="330" height="440" rx="10" fill="#c7d3e3" stroke="#0c1a30" stroke-width="8"/>
            <g id="s10-ref"><g id="s10-crown2" transform="translate(775,790) scale(0.8)"></g></g>
            <path d="M640 640 L700 580 M650 720 L760 600" fill="none" stroke="#f4f6f9" stroke-width="10" stroke-linecap="round"/></g>
        </svg>
        <div id="s10-q1" class="card disp" style="left:150px; top:200px; width:780px; height:170px; font-size:118px; line-height:176px">هدّد الدولة؟</div>
        <div id="s10-q2" class="card disp" style="left:150px; top:200px; width:780px; height:170px; font-size:104px; line-height:176px">ولا خافت من المراية؟</div>
      </div>
      <div id="s10-b" class="stage">
        {SVG}{PANEL}</svg>
        <div id="s10-scales" style="position:absolute; left:40px; top:100px; width:1000px; height:1000px"></div>
        <div id="s10-you" class="plate" style="left:130px; top:960px; width:820px; height:200px; font-size:136px; line-height:204px">الحكم لك أنت</div>
      </div>''', '''
    EK.fill("s10-crown", EK.crown()); EK.fill("s10-crown2", EK.crown()); EK.fill("s10-bk", EK.book(440, 580, "#5b3a24"));
    const w = EK.clock("s10");
    const tl = gsap.timeline({ paused: true });
    gsap.set("#s10-q1, #s10-q2, #s10-b, #s10-you, #s10-ref", { opacity: 0 });
    tl.fromTo("#s10-a", { y: 1920 }, { y: 0, duration: 0.4, ease: "power4.out" }, 0);
    EK.pop(tl, "#s10-q1", w(182), -2);
    tl.fromTo("#s10-mir", { rotation: -4, svgOrigin: "770 1070" }, { rotation: 0, duration: 0.5, ease: "back.out(2)" }, w(181));
    EK.out(tl, "#s10-q1", w(184) + 0.1); EK.pop(tl, "#s10-q2", w(185), 2);
    tl.to("#s10-ref", { opacity: 1, duration: 0.4, ease: "power1.out" }, w(187));
    tl.fromTo("#s10-crown", { rotation: -5, transformOrigin: "50% 100%" }, { rotation: 5, duration: 0.07, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, w(186));
    tl.fromTo("#s10-crown2", { rotation: 5, transformOrigin: "50% 100%" }, { rotation: -5, duration: 0.07, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, w(187) + 0.4);
    // the verdict is yours
    EK.cut(tl, "#s10-a", "#s10-b", w(191, -0.35), 1080);
    EK.lottie(tl, "s10-scales", "scales", w(191, -0.35), 4, { from: 0, to: 239 });
    EK.stamp(tl, "#s10-you", "#s10-b", w(192) + 0.1, -3);
    window.__timelines["s10"] = tl;''')

S["s11"] = ('''
      <div id="s11-bg" style="position:absolute; inset:0; background:#13294B"></div>
      <div id="s11-wipe" style="position:absolute; left:0; top:0; width:1080px; height:1920px; background:#CEA532"></div>
      <div id="s11-logobox" style="position:absolute; left:250px; top:430px; width:580px; height:685px"><img id="s11-logo" src="assets/brand/t3m-logo-light.svg" style="width:580px; height:685px; display:block" /></div>''', '''
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#s11-bg", { clipPath: "circle(0% at 50% 40%)" }, { clipPath: "circle(120% at 50% 40%)", duration: 0.45, ease: "power3.out" }, 0);
    tl.fromTo("#s11-wipe", { clipPath: "circle(0% at 50% 40%)" }, { clipPath: "circle(120% at 50% 40%)", duration: 0.45, ease: "power3.out" }, 0);
    tl.to("#s11-wipe", { opacity: 0, duration: 0.3, ease: "power2.out" }, 0.3);
    tl.fromTo("#s11-logobox", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }, 0.35);
    window.__timelines["s11"] = tl;''')

for sid, (body, js) in S.items():
    open(f"compositions/{sid}.html", "w", encoding="utf-8").write(f'''<!-- generated by tools/scenes.py: edit that file, not this one -->
<template>
  <style>
    @font-face {{ font-family: "Lalezar"; src: url("assets/fonts/Lalezar-Regular.ttf"); font-weight: 400; }}
    @font-face {{ font-family: "Noto Kufi Arabic"; src: url("assets/fonts/NotoKufiArabic.ttf"); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-wrap" class="clip" data-start="0" data-duration="3.0" data-layout-allow-overflow style="position:absolute;inset:0">{body}
    </div>
  </div>
  <script>{js}
  </script>
</template>
''')
print("wrote", len(S), "scenes")
