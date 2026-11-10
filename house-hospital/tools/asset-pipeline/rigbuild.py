# Build cut-out rig parts from the 4x cutouts. Coordinates in specs are source (1x) pixels.
import sys,os,json,numpy as np,cv2
from PIL import Image
SRC,OUT=sys.argv[1],sys.argv[2]
K=4
SPECS={
 # walkers (side view, facing right). hem: robe bottom; feet replaced by animated feet.
 # walkarm: the forward arm drawn in the WALK pose. T0-T1 is the sleeve's top edge (where it leaves the body,
 # and the cuff's top corner), w the sleeve width, L shoulder-to-wrist length, hand its length, hwh its
 # half-width, front the body's front edge in that pose: the drawing is used right of it (forearm, cuff,
 # hand); left of it the upper arm is hidden by the body, so it is completed in the sleeve's own colour.
 # attach: the shoulder on the side view. hang: the side view's own hanging arm, painted out of the body.
 'salem_side': dict(src='salem_side',neck=44,pivot=(32,46),waist=96,hem=157,walker=True,
    arms=[dict(shoulder=(27,56),box=(10,100,34,124),w=9)],
    hang=[(18,53),(37,53),(38,106),(36,127),(14,127),(16,104)],
    walkarm=dict(src='salem_walk',T0=(64,57),T1=(84,88),w=12.5,L=49,hand=14,hwh=8.5,front=[(63,50),(64,57),(70,92),(71,105)],attach=(28,57))),
 'father_side':dict(src='father_side',neck=46,pivot=(40,48),waist=118,hem=211,walker=True,
    arms=[dict(shoulder=(35,60),box=(26,120,50,148),w=12)],
    hang=[(22,53),(49,55),(51,126),(50,151),(27,151),(23,126)],
    walkarm=dict(src='father_walk',T0=(89,68),T1=(115,104),w=18.5,L=65,hand=20,hwh=11.5,front=[(86,50),(89,68),(89,105),(92,125)],attach=(36,61))),
 'uncle_side': dict(src='uncle_side',neck=45,pivot=(50,47),waist=118,hem=210,walker=True,
    arms=[dict(shoulder=(44,60),box=(34,124,56,150),w=14)],
    hang=[(23,53),(58,55),(59,128),(58,153),(33,153),(24,128)],
    walkarm=dict(src='uncle_walk',T0=(105,65),T1=(138,109),w=20.5,L=66,hand=22,hwh=12.5,front=[(102,50),(105,65),(110,112),(110,132)],attach=(44,61))),
 'marian_side':dict(src='marian_side',neck=60,pivot=(62,62),waist=175,hem=348,walker=True,legs=True,
    arms=[dict(shoulder=(57,88),box=(44,200,78,248),w=16)],
    hang=[(37,80),(73,84),(75,210),(75,248),(47,248),(37,212)],
    walkarm=dict(src='marian_walk',T0=(128,112),T1=(181,158),w=26,L=112,hand=30,hwh=15.5,front=[(124,80),(128,112),(131,163),(132,200)],attach=(56,90))),
 'pat_side':   dict(src='pat_side',neck=62,pivot=(55,64),
    arms=[dict(shoulder=(46,90),box=(34,206,64,254),w=16)],
    hang=[(27,80),(61,84),(63,214),(63,254),(35,254),(27,216)],
    walkarm=dict(src='pat_walk',T0=(122,115),T1=(178,171),w=25,L=120,hand=32,hwh=15.5,front=[(118,75),(121,100),(122,115),(124,166),(124,200)],attach=(46,91))),
 # standing three-quarter / front rigs
 'salem_q34':  dict(src='salem_q34',neck=45,pivot=(40,47),
    arms=[dict(shoulder=(52,56),box=(48,98,68,124),w=9,cut=[(49,51),(72,58),(72,104),(53,104)])]),
 'father_front':dict(src='father_front',neck=48,pivot=(50,50),
    arms=[dict(shoulder=(80,58),box=(80,118,102,150),w=12,cut=[(77,55),(108,66),(108,124),(85,126)])]),
 'uncle_q34':  dict(src='uncle_q34',neck=47,pivot=(58,49),
    arms=[dict(shoulder=(86,62),box=(82,118,100,152),w=13,cut=[(83,57),(108,70),(108,128),(86,128)])]),
 'mother_q34': dict(src='mother_q34',neck=47,pivot=(60,49),soft_head=True,arms=[]),
 'pat_q34':    dict(src='pat_q34',neck=62,pivot=(68,64),
    arms=[dict(shoulder=(104,88),box=(104,200,132,252),w=20,cut=[(98,82),(140,96),(140,212),(106,212),(102,150)])]),
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
        bitmap=None
        if 'cut' in a:
            # keep the drawn sleeve + hand as two bitmap pieces split at the elbow
            poly=np.array([[p[0]*K,p[1]*K] for p in a['cut']],np.int32)
            pm=np.zeros((H,W),np.uint8);cv2.fillPoly(pm,[poly],1)
            armm=((pm|cv2.dilate(hand,np.ones((7,7),np.uint8)))>0).astype(np.float32)*(al/255.0)
            sx0,sy0=a['shoulder'][0]*K,a['shoulder'][1]*K
            cxc,cyc=(hb[0]+hb[2])/2,hb[1]+6
            ex,ey=sx0+(cxc-sx0)*0.47,sy0+(cyc-sy0)*0.47
            r=a['w']*K*0.62
            yy,xx=np.mgrid[0:H,0:W]
            disc=((xx-ex)**2+(yy-ey)**2)<=r*r
            pieces={}
            for nm,half in {'upper':(yy<ey),'fore':(yy>=ey)}.items():
                m=armm*((half|disc).astype(np.float32))
                ys,xs=np.where(m>0.01)
                x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
                Image.fromarray(np.dstack([rgb,(m*255).astype(np.uint8)])[y0:y1,x0:x1]).save(f'{d}/{nm}{i}.png')
                pieces[nm]=dict(x=int(x0),y=int(y0),w=int(x1-x0),h=int(y1-y0))
            bitmap=dict(pieces,elbow=[float(ex),float(ey)])
            poly=np.array([[p[0]*K,p[1]*K] for p in a['cut']],np.int32)
            cm=np.zeros((H,W),np.uint8);cv2.fillPoly(cm,[poly],1)
            # outside the torso: drop alpha. Torso edge = column where the arm polygon starts.
            body_al=np.where(cv2.dilate(cm|rm,np.ones((5,5),np.uint8))>0,0,body_al)
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
                         stroke='#%02x%02x%02x'%tuple(int(c*0.82) for c in col),bitmap=bitmap,skin='#%02x%02x%02x'%tuple(int(c) for c in np.median(rgb[hand>0],0))))
    if sp.get('walkarm'):
        wa=sp['walkarm']
        # paint the hanging arm out of the body: each row takes the robe colour found beside it
        hp=np.array([[q[0]*K,q[1]*K] for q in sp['hang']],np.int32)
        hm=np.zeros((H,W),np.uint8);cv2.fillPoly(hm,[hp],1)
        hm=cv2.dilate(hm,np.ones((33,33),np.uint8))*(al>0).astype(np.uint8)
        y0h,y1h=np.where(hm.any(1))[0][[0,-1]]
        ok=(al>220)&(hm==0)
        ref=np.median(rgb[y0h:y1h][ok[y0h:y1h]],0)
        ok&=(np.abs(rgb.astype(np.int16)-ref).max(2)<34)
        rows=np.zeros((H,3),np.float32);have=np.zeros(H,bool)
        for y in range(H):
            if ok[y].sum()>12: rows[y]=np.median(rgb[y][ok[y]],0);have[y]=True
        idx=np.where(have)[0]
        for c in range(3): rows[:,c]=np.interp(np.arange(H),idx,rows[idx,c])
        rows=cv2.GaussianBlur(rows[:,None,:],(1,0),sigmaX=0.1,sigmaY=14)[:,0,:]
        fill=np.repeat(rows[:,None,:],W,1)
        soft=cv2.GaussianBlur(hm.astype(np.float32),(0,0),6)[...,None]
        body_rgb=(body_rgb*(1-soft)+fill*soft).astype(np.uint8)
        # cut the drawn forward arm from the walk pose
        wim=np.array(Image.open(f"{SRC}/{wa['src']}.png").convert('RGBA'));WH,WW=wim.shape[:2]
        wrgb=np.ascontiguousarray(wim[...,:3]).astype(np.float32);wal=wim[...,3].astype(np.float32)/255
        T0=np.array(wa['T0'],np.float32)*K;T1=np.array(wa['T1'],np.float32)*K
        ax=(T1-T0)/np.linalg.norm(T1-T0);pd=np.array([-ax[1],ax[0]])   # pd: across the sleeve, top to underside
        w=wa['w']*K;L=wa['L']*K;hwh=wa['hwh']*K;hl=wa['hand']*K
        Wr=T1+pd*w/2;S=Wr-ax*L
        b=5*K
        poly=np.array([S-ax*b-pd*w/2,Wr-pd*w/2,Wr-pd*hwh,Wr+ax*hl-pd*hwh,Wr+ax*hl+pd*hwh,Wr+pd*hwh,Wr+pd*w/2,S-ax*b+pd*w/2],np.int32)
        pm=np.zeros((WH,WW),np.uint8);cv2.fillPoly(pm,[poly],1)
        yy,xx=np.mgrid[0:WH,0:WW].astype(np.float32)
        u=(xx-S[0])*ax[0]+(yy-S[1])*ax[1];v=(xx-S[0])*pd[0]+(yy-S[1])*pd[1]
        fr=np.array(wa['front'],np.float32)*K
        xf=np.interp(np.arange(WH),fr[:,1],fr[:,0])[:,None]
        hidden=np.clip((xf+2*K-xx)/(3*K),0,1)          # 1 where the body hides the arm
        real=(pm>0)&(hidden<0.05)&(wal>0.9)&(u<L-2*K)
        sleeve=np.median(wrgb[real],0)
        flat=sleeve[None,None,:]*(1-0.07*np.clip(v/w+0.5,0,1))[...,None]
        wrgb=wrgb*(1-hidden[...,None])+flat*hidden[...,None]
        alpha=np.maximum(wal,hidden)                     # the completed part is solid
        armm=cv2.GaussianBlur(pm.astype(np.float32),(0,0),1.2)*alpha
        armm*=np.clip((u+b)/(w*1.15),0,1)            # the shoulder end fades into the body's own cloth
        dist=cv2.distanceTransform((armm>0.5).astype(np.uint8),cv2.DIST_L2,5)
        rim=np.clip(1-dist/(1.8*K),0,1)[...,None]
        wrgb=wrgb*(1-0.12*rim*hidden[...,None])-0.03*rim*(1-hidden[...,None])*wrgb
        E=S+(Wr-S)*0.5;Pm=Wr+ax*hl*0.55
        disc=((xx-E[0])**2+(yy-E[1])**2)<=(w*0.5)**2
        pieces={}
        for nm,half in {'upper':(u<L*0.5),'fore':(u>=L*0.5)}.items():
            m=armm*((half|disc).astype(np.float32))
            ys,xs=np.where(m>0.01)
            x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
            Image.fromarray(np.dstack([np.clip(wrgb,0,255).astype(np.uint8),(m*255).astype(np.uint8)])[y0:y1,x0:x1]).save(f'{d}/{nm}0.png')
            pieces[nm]=dict(x=int(x0),y=int(y0),w=int(x1-x0),h=int(y1-y0))
        arms[0]['bitmap']=dict(pieces,S=[float(S[0]),float(S[1])],E=[float(E[0]),float(E[1])],P=[float(Pm[0]),float(Pm[1])],W=[float(Wr[0]),float(Wr[1])])
        arms[0]['shoulder']=[wa['attach'][0]*K,wa['attach'][1]*K]
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
