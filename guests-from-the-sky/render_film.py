from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np, math, subprocess, json, sys, os, shutil
from pathlib import Path
from functools import lru_cache

W,H,FPS=720,1280,24
DURATION=59.4
# The scenes were first timed to a 65.8 s recording. VOICE_MAP pins each scene
# boundary (and each timed caption) to the matching word in the new 58.1 s voice:
# (time in the new voice, time in the original scene layout).
VOICE_MAP=[(0,0),(5.6,6.8),(8.95,7.8),(10.6,12.75),(13.8,16.35),(17.55,20.7),(19.9,23.0),(22.45,24.7),(23.0,26.5),
 (26.55,31.3),(29.5,34.2),(31.8,35.9),(33.5,38.85),(35.2,40.95),(36.5,41.0),(39.4,45.85),(43.35,49.25),(45.8,52.35),
 (47.2,52.75),(49.2,53.6),(49.95,56.9),(53.4,60.9),(56.4,63),(59.4,67.2)]
OLD_DURATION=67.2
ROOT=Path(__file__).parent
A=ROOT/'assets'
OUT=ROOT/'output'
OUT.mkdir(exist_ok=True)
INK=(24,45,60)
CREAM=(255,237,195)
GOLD=(247,190,98)
RES=Image.Resampling.BICUBIC

def clamp(x):return max(0,min(1,x))
def ease(x):
 x=clamp(x);return x*x*(3-2*x)
def lerp(a,b,t):return a+(b-a)*t
def load(n):return Image.open(A/(n+'.png')).convert('RGBA')
def trim(im):
 alpha=im.getchannel('A').point(lambda x:255 if x>150 else (int(x*255/150) if x>110 else 0))
 im.putalpha(alpha)
 b=alpha.getbbox();return im.crop(b) if b else im
def silhouette(im):
 im=trim(im);out=Image.new('RGBA',im.size,INK+(255,));out.putalpha(im.getchannel('A'));return out
cast=load('cast')
# cast.png is the colour drawing (girl, father, mother). The other poses only exist
# as black silhouettes, so tools/colorize.py dresses them in the same fabrics: assets/color/.
family=trim(cast.crop((50,55,875,955)))
mother=trim(cast.crop((935,385,1536,945)))
father=trim(cast.crop((420,50,870,945)))
girlwalk=trim(load('color/girlwalk'))
girlpoint=trim(load('color/girlpoint'))
girlfly=trim(load('color/girlfly'))
fatherpoint=trim(load('color/fatherpoint'))
plane=trim(load('plane'))
passengers=[trim(load(f'color/p{i}')) for i in range(4)]
sprites={'family':family,'mother':mother,'girlwalk':girlwalk,'girlpoint':girlpoint,'girlfly':girlfly,'fatherpoint':fatherpoint,'father':father,'plane':plane}
for i,p in enumerate(passengers):sprites['p'+str(i)]=p
backs={k:load(k).convert('RGB') for k in ['street','airfield','home','museum']}

@lru_cache(300)
def font(size):
 f=ImageFont.truetype(str(A/'NotoSansArabic.ttf'),size)
 try:f.set_variation_by_axes([650,100])
 except Exception:pass
 return f
@lru_cache(200)
def textimg(txt,size,color):
 f=font(size);box=f.getbbox(txt,direction='rtl',language='ar');w=box[2]-box[0]+24;h=box[3]-box[1]+24
 im=Image.new('RGBA',(w,h));dr=ImageDraw.Draw(im)
 dr.text((12-box[0],12-box[1]),txt,font=f,fill=color,direction='rtl',language='ar')
 return im
def label(im,txt,y,size=38,color=CREAM,alpha=1,x=360,shadow=True):
 lay=textimg(txt,size,color).copy()
 if lay.width>640:lay=lay.resize((640,round(lay.height*640/lay.width)),RES)
 if alpha<1:lay.putalpha(lay.getchannel('A').point(lambda a:int(a*clamp(alpha))))
 px=int(x-lay.width/2);py=int(y-lay.height/2)
 if shadow:
  sh=Image.new('RGBA',lay.size,INK+(255,));sh.putalpha(lay.getchannel('A').point(lambda a:int(a*.36)));sh=sh.filter(ImageFilter.GaussianBlur(4));im.paste(sh,(px,py+3),sh)
 im.paste(lay,(px,py),lay)
def header(im,small,big,y=170,a=1,dark=False):
 color=INK if dark else CREAM
 accent=INK if dark else GOLD
 label(im,small,y,24,accent,a,shadow=not dark)
 label(im,big,y+63,54,color,a,shadow=not dark)
 d=ImageDraw.Draw(im);v=int(70*a);d.line((360-v,y+112,360+v,y+112),fill=accent,width=2)
def backdrop(name,zoom=1,pan=.5,py=.5):
 im=backs[name];scale=max(W/im.width,H/im.height)*zoom
 sw,sh=int(im.width*scale),int(im.height*scale)
 # Crop before resizing, avoiding repeated resize of oversized panoramas.
 cw,ch=W/scale,H/scale;cx=(im.width-cw)*clamp(pan);cy=(im.height-ch)*clamp(py)
 return im.crop((cx,cy,cx+cw,cy+ch)).resize((W,H),RES).convert('RGBA')
def vignette(im,strength=.32):
 im.alpha_composite(VIGNETTE if strength>.2 else LIGHT_VIGNETTE)
def warp(im,t,amp=5,mode='walk'):
 w,h=im.size;mesh=[];nx,ny=6,10
 def src(x,y):
  v=y/h;u=x/w
  if mode=='walk':dx=amp*math.sin(t*9+u*2.5)*max(0,(v-.53)/.47);dy=2*math.sin(t*9)*v
  elif mode=='knead':dx=amp*math.sin(t*3.5)*math.sin(v*math.pi);dy=amp*.8*math.sin(t*3.5)*math.sin(u*math.pi)*math.sin(v*math.pi)
  else:dx=amp*math.sin(t*2)*v;dy=0
  return x+dx,y+dy
 for yy in range(ny):
  y0=round(h*yy/ny);y1=round(h*(yy+1)/ny)
  for xx in range(nx):
   x0=round(w*xx/nx);x1=round(w*(xx+1)/nx)
   q=(*src(x0,y0),*src(x0,y1),*src(x1,y1),*src(x1,y0));mesh.append(((x0,y0,x1,y1),q))
 return im.transform((w,h),Image.Transform.MESH,mesh,RES)
@lru_cache(1200)
def sized(name,height,flip=False):
 p=sprites[name];p=p.resize((max(1,round(p.width*height/p.height)),height),RES)
 return ImageOps.mirror(p) if flip else p
def sprite(im,name,x,bottom,height,t=0,motion=None,angle=0,alpha=1,flip=False,shadow=False):
 p=sized(name,max(2,round(height)),flip).copy()
 if motion:p=warp(p,t,amp=max(2,height*.012),mode=motion)
 if angle:p=p.rotate(angle,RES,expand=True)
 if alpha<1:p.putalpha(p.getchannel('A').point(lambda a:int(a*clamp(alpha))))
 if shadow:
  sh=Image.new('RGBA',im.size);dr=ImageDraw.Draw(sh);dr.ellipse((x-p.width*.43,bottom-7,x+p.width*.5,bottom+13),fill=(25,36,41,45));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
 im.alpha_composite(p,(int(x-p.width/2),int(bottom-p.height)))
 return p.width,p.height
def dust(im,t,count=30,area=(0,0,720,1280),bright=False):
 dr=ImageDraw.Draw(im,'RGBA');x0,y0,x1,y1=area
 for i in range(count):
  x=x0+((i*137.31+t*(10+(i%5)*6))%(x1-x0));y=y0+((i*97.13-t*(5+i%7))%(y1-y0));r=1+(i%3)*.55
  dr.ellipse((x-r,y-r,x+r,y+r),fill=(255,235,185,60 if bright else 35))
def bird(im,x,y,s,t):
 dr=ImageDraw.Draw(im,'RGBA');h=math.sin(t*6)*s*.35;dr.line([(x-s,y+h),(x,y),(x+s,y+h)],fill=INK+(150,),width=2)
def crowd(im,t,near=False):
 specs=[(-20,1070,250),(105,1040,220),(600,1050,235),(735,1090,295)] if near else [(35,966,150),(130,962,145),(578,964,148),(674,964,158)]
 for i,(x,y,h) in enumerate(specs):
  sprite(im,'fatherpoint' if i%2 else 'father',x+math.sin(t*.8+i)*2,y,h,t,angle=math.sin(t*1.2+i)*1.4,alpha=.9,flip=bool(i%2))
def propellers(im,x,bottom,height,t,alpha=1):
 w=plane.width*height/plane.height;left=x-w/2;top=bottom-height;dr=ImageDraw.Draw(im,'RGBA')
 for px,py in [(.299,.254),(.415,.226),(.457,.59)]:
  cx=left+px*w;cy=top+py*height;r=height*.11;ph=t*80
  dr.ellipse((cx-r*.35,cy-r,cx+r*.35,cy+r),fill=(235,218,172,int(22*alpha)),outline=(235,218,172,int(65*alpha)),width=1)
  dr.line((cx-math.cos(ph)*r*.35,cy-math.sin(ph)*r,cx+math.cos(ph)*r*.35,cy+math.sin(ph)*r),fill=(255,235,189,int(160*alpha)),width=2)
def airplane(im,x,bottom,height,t,angle=0,shadow=False):
 sprite(im,'plane',x,bottom,height,t,angle=angle,shadow=shadow)
 if abs(angle)<1:propellers(im,x,bottom,height,t)
def caption(im,txt,y=1150,a=1):
 lay=Image.new('RGBA',im.size);d=ImageDraw.Draw(lay);d.rounded_rectangle((45,y-35,675,y+37),18,fill=INK+(int(190*a),));im.alpha_composite(lay);label(im,txt,y,30,CREAM,a,shadow=False)

y,x=np.mgrid[0:H,0:W];dist=((x-W/2)/(W*.73))**2+((y-H/2)/(H*.74))**2
v=np.uint8(np.clip((dist-.18)*65+np.maximum(0,(240-y)/240)*25,0,100))
VIGNETTE=Image.new('RGBA',(W,H),INK+(0,));VIGNETTE.putalpha(Image.fromarray(v))
LIGHT_VIGNETTE=VIGNETTE.copy();LIGHT_VIGNETTE.putalpha(Image.fromarray(v//2))

def scene(t):
 if t<6.8:
  p=t/6.8;im=backdrop('street',1.02+.035*p,.45+.075*p,.54)
  bird(im,520-t*16,350,9,t);bird(im,560-t*16,330,7,t+.5)
  sprite(im,'family',lerp(250,390,ease(p)),1120-abs(math.sin(t*4.6))*3,590,t,motion='walk',shadow=True)
  vignette(im)
  header(im,'الشارقة • حكاية أول مرة','ضيوف من السما',180,ease(t/.8)*ease((6.8-t)/.5),dark=True)
  dust(im,t)
 elif t<12.75:
  p=(t-6.8)/5.95;im=backdrop('airfield',1.03,.5,.9)
  crowd(im,t)
  sprite(im,'family',355+15*math.sin(p*1.7),1135,580,t,angle=math.sin(t)*.5,shadow=True)
  crowd(im,t,True);vignette(im);dust(im,t,35,area=(0,600,720,1100))
  header(im,'كل الناس تنتظر…','أكيد هالضيف مهم!',240,ease((t-7.8)/.5))
 elif t<16.35:
  p=(t-12.75)/3.6;im=backdrop('street',1.08,.51-.04*p,.43)
  sprite(im,'girlwalk',585,1160,450,t,angle=-4,flip=True,shadow=True)
  vignette(im);header(im,'طالعت صوب البحر…','بس وين سفينتهم؟',210,ease(p*5),dark=True)
  dust(im,t,18)
 elif t<20.7:
  p=(t-16.35)/4.35;im=backdrop('airfield',1.03+.1*p,.5,.5-.35*p)
  sprite(im,'fatherpoint',430,1160+p*70,680,t,angle=-1+math.sin(t)*.4,shadow=True)
  sprite(im,'girlpoint',190,1160+p*70,410,t,angle=-3*ease(p*2),shadow=True)
  vignette(im);header(im,'أبوي أشّر فوق…','رفعت راسي',210,ease(p*4)*ease((1-p)*4))
  dust(im,t,22)
 elif t<23.0:
  p=(t-20.7)/2.3;im=backdrop('airfield',1.15,.5,.08)
  height=lerp(120,355,ease(p));xx=lerp(830,345,ease(p));bottom=lerp(440,790,ease(p))
  airplane(im,xx,bottom,height,t,angle=lerp(7,0,ease(p)))
  vignette(im);label(im,'واااو… طيّارة!',240,52,CREAM,ease(p*5));dust(im,t,35)
 elif t<26.5:
  p=(t-23)/3.5;im=backdrop('airfield',1,.5,.5)
  h=275;xx=lerp(440,355,ease(p));bottom=lerp(740,1002,ease(p))
  sh=Image.new('RGBA',(W,H));d=ImageDraw.Draw(sh);d.ellipse((110,990,660,1010),fill=INK+(int(30+40*p),));im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
  airplane(im,xx,bottom,h,t)
  dust(im,t,60,area=(60,950,700,1030));vignette(im)
  header(im,'الطائرة التي فتحت باب الحكاية','هانو',230,ease((t-24.7)/.5))
 elif t<31.3:
  p=(t-26.5)/4.8;im=backdrop('airfield',1.02,.5,.7)
  airplane(im,340,935,275,t)
  dr=ImageDraw.Draw(im);dr.polygon([(508,860),(574,969),(595,969),(525,860)],fill=(190,143,86,255))
  for i in range(6):dr.line((510+i*11,873+i*17,532+i*11,873+i*17),fill=INK,width=3)
  for i in range(4):
   q=clamp((t-26.7-i*.55)/2.1)
   if t>26.7+i*.55:
    xx=lerp(520,255+i*77,ease(q));yy=lerp(906,1040,ease(q));sprite(im,'p'+str(i),xx,yy,118,t+i,motion='walk',alpha=ease((t-26.7-i*.55)*4),shadow=True)
  crowd(im,t,True);vignette(im);header(im,'والأهالي يرحّبون فيهم','أربعة ركّاب',230,ease(p*5));dust(im,t,22)
 elif t<34.2:
  p=(t-31.3)/2.9;im=backdrop('airfield',1.04,.5,.5)
  airplane(im,420,940,235,t)
  sprite(im,'girlpoint',240,1250,660+25*p,t,angle=-2,shadow=True)
  vignette(im);header(im,'وأنا؟','عيني ما فارقت الطيّارة',230,1)
 elif t<38.85:
  p=(t-34.2)/4.65;im=backdrop('home',1.02+.025*p,.55,.55)
  sprite(im,'mother',490,1100,350,t,motion='knead',shadow=True)
  sprite(im,'girlwalk',lerp(-100,225,ease(p*2.8)),1135-abs(math.sin(t*7))*4,350,t,motion='walk',shadow=True)
  vignette(im);dust(im,t,25,area=(50,300,670,1000),bright=True)
  header(im,'رجعت البيت…','من وين يَوْا الضيوف؟',220,ease((t-35.9)/.5),dark=True)
 elif t<40.95:
  p=(t-38.85)/2.1;im=backdrop('home',1.06,.48,.6)
  sprite(im,'mother',505,1150,350,t,motion='knead',shadow=True)
  sprite(im,'girlfly',240,1150-32*math.sin(clamp(p*1.6)*math.pi),470,t,angle=math.sin(p*8)*3,shadow=True)
  vignette(im);header(im,'يمّه…','من السما!',210,ease(p*5),dark=True);dust(im,t,40,bright=True)
 elif t<45.85:
  p=(t-40.95)/4.9;im=backdrop('airfield',1.07,.5,.3)
  veil=Image.new('RGBA',(W,H),(15,46,61,95));im.alpha_composite(veil)
  header(im,'ذاك اليوم…','٥ أكتوبر',290,ease(p*5))
  label(im,'١٩٣٢',540,140,CREAM,ease((p-.08)*5))
  label(im,'بداية حكاية الطيران في الشارقة',700,29,GOLD,ease((p-.2)*5))
  airplane(im,lerp(600,300,p),1060,210,t)
  vignette(im);dust(im,t,45,bright=True)
 elif t<52.35:
  p=(t-45.85)/6.5;im=backdrop('airfield',1.04,.5,.5)
  # Architectural paper layers rise separately to suggest the new air station.
  dr=ImageDraw.Draw(im)
  for i,(xx,ww,hh) in enumerate([(100,170,145),(267,190,110),(454,160,145)]):
   a=ease((t-45.85-i*.22)/1.3);top=1020-hh*a
   dr.rectangle((xx,top,xx+ww,1020),fill=(191+i*10,142+i*9,80+i*7))
   dr.rectangle((xx,top,xx+ww,top+9),fill=(238,195,121))
   if a>.7:
    for wx in range(xx+22,xx+ww-20,40):dr.rectangle((wx,top+35,wx+16,top+68),fill=INK)
  dr.rounded_rectangle((329,945,385,1020),radius=22,fill=INK)
  sprite(im,'father',122,1100,180,t,shadow=True);sprite(im,'fatherpoint',602,1100,180,t,flip=True,shadow=True)
  airplane(im,lerp(620,315,p),860,180,t)
  vignette(im);header(im,'المحطّة','أول مطار مدني',215,1)
  label(im,'في الإمارات',362,51,CREAM,ease(p*5))
  if t>49.25:
   label(im,'ومن أوائل مطارات',488,32,GOLD,ease((t-49.25)*3));label(im,'الخليج العربي',541,42,CREAM,ease((t-49.25)*3))
  dust(im,t,22)
 elif t<56.9:
  p=(t-52.35)/4.55;im=backdrop('street',1.04,.36+.06*p,.4)
  veil=Image.new('RGBA',(W,H),(13,41,54,160));im.alpha_composite(veil)
  label(im,'تأسست في عهد',340,32,GOLD,ease(p*5))
  label(im,'الشيخ سلطان بن صقر',445,45,CREAM,ease((p-.08)*5))
  label(im,'القاسمي',520,55,CREAM,ease((p-.13)*5))
  label(im,'رحمه الله',625,32,GOLD,ease((p-.28)*4))
  # Honorific presented in type, without inventing a portrait of the ruler.
  sprite(im,'family',360,1180,370,t,alpha=.75)
  vignette(im);dust(im,t,42,bright=True)
 elif t<60.9:
  p=(t-56.9)/4;im=backdrop('airfield',1.05,.5,.15);im.alpha_composite(Image.new('RGBA',(W,H),(15,44,60,120)))
  header(im,'محطة على طريق الرحلات','بريطانيا • الشارقة • الهند',230,1)
  points=[]
  for i in range(101):
   q=i/100;points.append((100+520*q,790-170*math.sin(q*math.pi)))
  dr=ImageDraw.Draw(im,'RGBA')
  for i in range(0,100,4):dr.line(points[i:i+3],fill=CREAM+(65,),width=2)
  upto=int(100*ease(p));dr.line(points[:max(2,upto+1)],fill=GOLD+(255,),width=4)
  for q,txt,yy in [(0,'بريطانيا',855),(.5,'الشارقة',715),(1,'الهند',855)]:
   xx=100+520*q;cy=790-170*math.sin(q*math.pi);dr.ellipse((xx-7,cy-7,xx+7,cy+7),fill=GOLD);label(im,txt,yy,27,CREAM,x=xx)
  xx,yy=points[upto];sprite(im,'plane',xx,yy+12,85,t,flip=True)
  label(im,'رحلات ربطت المسافات… وقرّبت العالم',1030,28,CREAM,1)
  vignette(im);dust(im,t,24,bright=True)
 else:
  p=(t-60.9)/(OLD_DURATION-60.9);im=backdrop('museum',1.05-.035*p,.5,.6)
  airplane(im,390,995,282,t)
  sprite(im,'family',215,1190,330,t,alpha=.97,shadow=True)
  vignette(im);header(im,'واليوم… الحكاية محفوظة','متحف المحطّة',220,ease(p*6),dark=True)
  label(im,'الشارقة',365,31,INK,ease(p*6),shadow=False)
  if t>63:
   caption(im,'تحقّقوا من إعادة الافتتاح قبل الزيارة',1120,ease((t-63)*2))
  label(im,'معالجة فنية مستوحاة من حدث تاريخي',1235,17,CREAM,ease((t-63)*2))
  dust(im,t,35,bright=True)
 return im

CUTS=[6.8,12.75,16.35,20.7,23,26.5,31.3,34.2,38.85,40.95,45.85,52.35,56.9,60.9]
def frame(t):
 t=float(np.interp(t,*zip(*VOICE_MAP)))
 im=scene(t)
 for cut in CUTS:
  if cut<=t<cut+.23:
   im=Image.blend(scene(cut-.001),im,ease((t-cut)/.23));break
 if t<.35:im=Image.blend(Image.new('RGBA',(W,H),INK+(255,)),im,ease(t/.35))
 if t>OLD_DURATION-.5:im=Image.blend(im,Image.new('RGBA',(W,H),INK+(255,)),ease((t-OLD_DURATION+.5)/.5))
 return im.convert('RGB')

def audio_track():
 sr=48000;audio=ROOT/'upload'/'voice.mp3'
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ar',str(sr),'-ac','1','-f','f32le','-'])
 voice=np.frombuffer(raw,np.float32).copy();out=np.zeros(round(DURATION*sr),np.float32);out[:len(voice)]=voice
 # Original, quiet pentatonic score: soft mallet over a warm sustained bed.
 score=np.zeros_like(out);notes=[293.665,369.994,440,493.883,587.33,493.883,440,369.994]
 for i,st in enumerate(np.arange(.4,DURATION-1,1.6)):
  tt=np.arange(int(sr*3.2))/sr;freq=notes[i%len(notes)];env=(1-np.exp(-tt*30))*np.exp(-tt*1.7)
  wave=(np.sin(2*np.pi*freq*tt)+.22*np.sin(2*np.pi*freq*2*tt)+.08*np.sin(2*np.pi*freq*3*tt))*env*.008
  a=int(st*sr);b=min(len(score),a+len(wave));score[a:b]+=wave[:b-a]
 # Propeller cue stays under the spoken narration.
 tt=np.arange(len(out))/sr;env=np.clip((tt-16.6)/2,0,1)*np.clip((25.5-tt)/2.5,0,1)
 engine=(np.sin(2*np.pi*74*tt)*(1+.4*np.sin(2*np.pi*16*tt))+.24*np.sin(2*np.pi*148*tt))*.009*env
 out+=score+engine.astype(np.float32)
 out*=np.minimum(1,np.maximum(0,(DURATION-tt)/1.0))
 subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','-','-c:a','pcm_s16le',str(OUT/'soundtrack.wav')],input=out.astype(np.float32).tobytes(),check=True)

def render():
 audio_track()
 command=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'soundtrack.wav'),'-map','0:v','-map','1:a','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(DURATION),str(OUT/'Guests_From_The_Sky.mp4')]
 proc=subprocess.Popen(command,stdin=subprocess.PIPE)
 for i in range(math.ceil(DURATION*FPS)):
  proc.stdin.write(frame(i/FPS).tobytes())
  if i%(FPS*5)==0:print(f'Rendered {i/FPS:.0f}/{DURATION:.1f} seconds',flush=True)
 proc.stdin.close();code=proc.wait()
 if code:raise RuntimeError('ffmpeg failed')
 print('Video ready',flush=True)

if __name__=='__main__':
 if '--preview' in sys.argv:
  times=[2.6,9.5,12,15.5,18.8,22.8,25,28,31.9,34.3,38,44,48.5,51.5,57]
  thumb=Image.new('RGB',(5*216,3*384),(24,45,60))
  for i,t in enumerate(times):
   im=frame(t).resize((216,384));ImageDraw.Draw(im).text((10,10),str(t),fill='white');thumb.paste(im,((i%5)*216,(i//5)*384))
  thumb.save(OUT/'contact_sheet.jpg')
  for t in [2.6,15.5,22.8,25,31.9,34.3,57]:frame(t).save(OUT/f'frame_{t}.jpg')
 else:render()
