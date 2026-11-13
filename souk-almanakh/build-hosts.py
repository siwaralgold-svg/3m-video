import json,re,shutil,sys
import os
P=os.path.dirname(os.path.abspath(__file__))+'/'
scenes=[('s1',0,16.15),('s3',16.15,28.85),('s4',28.85,31.6),('s5',31.6,37.2),('s6',37.2,42.75),('s7',42.75,48.9),('s8',48.9,57.3),('s9',57.3,64.1),('s10',64.1,66.5),('s11',66.5,77.75),('s12',77.75,91.55),('s13',91.55,96.5),('s14',96.5,99.1)]
H=[]
for n,a,b in scenes:
    H.append(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:2"></div>')
H.append('      <div id="fly" data-composition-id="fly" data-composition-src="compositions/fly.html" data-start="0" data-duration="96.5" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:4"></div>')
H.append('      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="95.8" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:5"></div>')
H.append('      <audio id="voiceover" class="clip" src="assets/voiceover.mp3" data-start="0" data-track-index="10" data-volume="1"></audio>')
m=json.load(open(P+'../sfx-library/manifest.json'))
by={v['file'].split('/')[-1][:-4]:v for v in m.values()}
# (name, picture time, volume, mode) ; mode 'peak' aligns peak one frame after the picture
cuts=[16.15,28.85,31.6,37.2,42.75,48.9,57.3,66.5,69.0,73.7,77.75,91.55]
sw=['swipe_03','swipe_07','whoosh_fast_02']
S=[(sw[i%3],c,0.22) for i,c in enumerate(cuts)]
S+=[('impact_punch_heavy_000',5.47,0.4),('impact_punch_heavy_002',15.62,0.45),('impact_punch_heavy_003',19.07,0.45),
 ('impact_wood_heavy_000',30.3,0.4),('low_thud',32.97,0.3),('low_thud',33.27,0.3),('low_thud',33.57,0.3),('low_thud',33.87,0.3),
 ('rpg_metal_latch',39.34,0.5),('rpg_book_flip2',41.3,0.4),('impact_soft',55.86,0.4),
 ('impact_punch_heavy_000',64.68,0.5),('impact_punch_heavy_002',67.08,0.4),('ui_switch3',68.3,0.4),
 ('impact_punch_heavy_003',73.0,0.4),('ui_switch3',76.2,0.4),
 ('impact_wood_heavy_002',93.0,0.5),('impact_punch_heavy_000',94.66,0.5)]
S.sort(key=lambda x:x[1])
A=[]
for i,(n,t,v) in enumerate(S,1):
    it=by[n]; shutil.copy(P+'../sfx-library/'+it['file'],P+'assets/sfx/'+n+'.mp3')
    st=max(0,t-it['peak_at']+1/30)
    A.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{n}.mp3" data-start="{st:.3f}" data-duration="{min(it["duration"],0.29) if n=="low_thud" else it["duration"]}" data-track-index="11" data-volume="{v}"></audio>')
s=open(P+'index.html').read()
s=re.sub(r'<!--HOSTS-->.*<!--SFX-->|<!--HOSTS-->\n<!--SFX-->','<!--HOSTS-->\n'+'\n'.join(H)+'\n'+'\n'.join(A)+'\n<!--SFX-->',s,flags=re.S) if '<!--HOSTS-->' in s else s
open(P+'index.html','w').write(s)
