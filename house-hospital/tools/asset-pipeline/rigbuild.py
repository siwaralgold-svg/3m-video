# Build cut-out rig parts from the 4x cutouts. Coordinates in specs are source (1x) pixels.
import sys,os,json,numpy as np,cv2
from PIL import Image
SRC,OUT=sys.argv[1],sys.argv[2]
K=4
SPECS={
 # walkers (side view, facing right). hem: robe bottom; feet replaced by animated feet.
 'salem_side': dict(src='salem_side',neck=44,pivot=(32,46),waist=96,hem=157,walker=True,
    arms=[dict(shoulder=(27,56),box=(10,100,34,124),w=9)]),
 'father_side':dict(src='father_side',neck=46,pivot=(40,48),waist=118,hem=211,walker=True,
    arms=[dict(shoulder=(35,60),box=(26,120,50,148),w=12)]),
 'uncle_side': dict(src='uncle_side',neck=45,pivot=(50,47),waist=118,hem=210,walker=True,
    arms=[dict(shoulder=(44,60),box=(34,124,56,150),w=14)]),
 'marian_side':dict(src='marian_side',neck=60,pivot=(62,62),waist=175,hem=348,walker=True,legs=True,
    arms=[dict(shoulder=(57,88),box=(44,200,78,248),w=16)]),
 # standing three-quarter / front rigs
 'salem_q34':  dict(src='salem_q34',neck=45,pivot=(40,47),
    arms=[dict(shoulder=(52,56),box=(48,98,68,124),w=9,cut=[(50,52),(66,60),(68,102),(54,102)])]),
 'father_front':dict(src='father_front',neck=48,pivot=(50,50),
    arms=[dict(shoulder=(80,58),box=(80,118,102,150),w=12,cut=[(78,56),(98,70),(102,122),(86,124)])]),
 'uncle_q34':  dict(src='uncle_q34',neck=47,pivot=(58,49),
    arms=[dict(shoulder=(86,62),box=(82,118,100,152),w=13,cut=[(84,58),(98,72),(101,124),(87,126)])]),
 'mother_q34': dict(src='mother_q34',neck=47,pivot=(60,49),soft_head=True,arms=[]),
 'pat_q34':    dict(src='pat_q34',neck=62,pivot=(68,64),
    arms=[dict(shoulder=(104,88),box=(104,200,132,252),w=20,cut=[(100,84),(120,96),(132,206),(108,210),(103,150)])]),
 'marian_q34': dict(src='marian_q34',neck=None,arms=[]),
}
def skinmask(rgb):
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV);h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
    return ((h>=4)&(h<=22)&(s>122)&(v>95)).astype(np.uint8)
os.makedirs(OUT,exist_ok=True)
allj={}
for rid,sp in SPECS.items():
    im=np.array(Image.open(f"{SRC}/{sp['src']}.png").convert('RGBA'));H,W=im.shape[:2]
    rgb=np.ascontiguousarray(im[...,:3]);al=im[...,3].copy()
    d=os.path.join(OUT,rid);os.makedirs(d,exist_ok=True)
    j=dict(w=W,h=H)
    body_rgb=rgb.copy();body_al=al.copy()
    arms=[]
    for i,a in enumerate(sp['arms']):
        x0,y0,x1,y1=[v*K for v in a['box']]
        sub=np.zeros((H,W),np.uint8);sub[y0:y1,x0:x1]=1
        hand=skinmask(rgb)*sub*(al>128)
        n,lab,st,_=cv2.connectedComponentsWithStats(hand,8)
        if n>1:
            big=1+np.argmax(st[1:,4]);hand=(lab==big).astype(np.uint8)
        hand=cv2.morphologyEx(hand,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        ys,xs=np.where(hand>0)
        hb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
        ha=cv2.GaussianBlur(cv2.dilate(hand,np.ones((5,5),np.uint8)).astype(np.float32),(0,0),1.2)
        hp=np.dstack([rgb,(np.minimum(ha,al/255)*255).astype(np.uint8)])[hb[1]-4:hb[3]+4,hb[0]-4:hb[2]+4]
        Image.fromarray(hp).save(f'{d}/hand{i}.png')
        # remove hand (and arm, if cut polygon) from body
        rm=cv2.dilate(hand,np.ones((11,11),np.uint8))
        if 'cut' in a:
            poly=np.array([[p[0]*K,p[1]*K] for p in a['cut']],np.int32)
            cm=np.zeros((H,W),np.uint8);cv2.fillPoly(cm,[poly],1)
            # outside the torso: drop alpha. Torso edge = column where the arm polygon starts.
            body_al=np.where(cv2.dilate(cm|rm,np.ones((7,7),np.uint8))>0,0,body_al)
            # repaint a margin inside for clean edge
            rm=rm|cm
        body_rgb=cv2.inpaint(body_rgb,rm*255,9,cv2.INPAINT_TELEA)
        sx,sy=a['shoulder'][0]*K,a['shoulder'][1]*K
        # sleeve colour: median of opaque pixels around the upper arm
        reg=rgb[sy+20:sy+90,max(0,sx-24):sx+24].reshape(-1,3);ra=al[sy+20:sy+90,max(0,sx-24):sx+24].reshape(-1)
        col=np.median(reg[ra>200],0) if (ra>200).sum()>20 else np.array([200,190,180])
        cuff=[(hb[0]+hb[2])/2,hb[1]+6]
        arms.append(dict(shoulder=[sx,sy],cuff=cuff,hand=dict(x=hb[0]-4,y=hb[1]-4,w=hp.shape[1],h=hp.shape[0]),
                         sleeveW=a['w']*K,color='#%02x%02x%02x'%tuple(int(c) for c in col),
                         stroke='#%02x%02x%02x'%tuple(int(c*0.82) for c in col),skin='#%02x%02x%02x'%tuple(int(c) for c in np.median(rgb[hand>0],0))))
    j['arms']=arms
    if sp.get('neck'):
        ny=sp['neck']*K
        hm=np.zeros((H,W),np.float32);hm[:ny+14]=1
        hm[ny-6:ny+14]=np.linspace(1,0,20)[:,None]
        if sp.get('soft_head'):
            pass
        head=np.dstack([rgb,(al*hm).astype(np.uint8)])[:ny+16]
        Image.fromarray(head).save(f'{d}/head.png')
        # body: erase head above neck-8 so head nods do not reveal a double
        cut=ny-10
        bm=np.ones((H,W),np.float32);bm[:cut]=0
        body_al=(body_al*bm).astype(np.uint8)
        j['head']=dict(h=ny+16,pivot=[sp['pivot'][0]*K,sp['pivot'][1]*K])
    if sp.get('walker'):
        hem=sp['hem']*K
        fr=rgb[hem+4:,:];fa=al[hem+4:,:]
        dark=fr[(fa>200)&(fr.sum(2)<330)]
        sand=np.median(dark,0) if len(dark) else np.array([90,50,30])
        skin=np.median(fr[(fa>200)&(skinmask(np.ascontiguousarray(fr))>0)],0) if (skinmask(np.ascontiguousarray(fr))*(fa>200)).sum()>10 else np.array([200,130,80])
        body_al[hem+2:]=0
        # soften hem bottom
        j['hem']=hem;j['waist']=sp['waist']*K;j['ground']=H-6
        j['sandal']='#%02x%02x%02x'%tuple(int(c) for c in sand);j['footSkin']='#%02x%02x%02x'%tuple(int(c) for c in skin)
        j['legs']=bool(sp.get('legs'))
    Image.fromarray(np.dstack([body_rgb,body_al])).save(f'{d}/body.png')
    allj[rid]=j
json.dump(allj,open(f'{OUT}/rigs.json','w'),indent=1)
print('built',list(allj))
