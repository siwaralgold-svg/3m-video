# Rebuild each upscaled figure: AI upscale for cloth, plain Lanczos for skin (faces/hands) so no features appear; smoother alpha.
import sys,glob,os,numpy as np,cv2
from PIL import Image
src,up,out=sys.argv[1],sys.argv[2],sys.argv[3];os.makedirs(out,exist_ok=True)
for f in sorted(glob.glob(src+'/*.png')):
    n=os.path.basename(f)
    a=np.array(Image.open(f).convert('RGBA'));H,W=a.shape[:2]
    u=np.array(Image.open(f'{up}/{n}').convert('RGBA'))
    lz=np.array(Image.fromarray(a[...,:3]).resize((W*4,H*4),Image.LANCZOS)).astype(np.float32)
    rgb=u[...,:3].astype(np.float32)
    person=not n.startswith(('prop_','env_'))
    if person:
        hsv=cv2.cvtColor(lz.astype(np.uint8),cv2.COLOR_RGB2HSV)
        h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
        skin=((h>=5)&(h<=22)&(s>70)&(s<200)&(v>110)).astype(np.uint8)
        skin=cv2.morphologyEx(skin,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
        # face zone: whole head area (top 30%) gets full lanczos where skin or near edge of skin
        zone=np.zeros_like(skin);zone[:int(H*4*0.32)]=1
        m=cv2.dilate(skin,np.ones((25,25),np.uint8))
        m=np.where(zone>0,m,cv2.dilate(skin,np.ones((9,9),np.uint8)))
        m=cv2.GaussianBlur(m.astype(np.float32),(0,0),3)[...,None]
        # flatten skin inside faces: median of lanczos removes any hint of features
        flat=cv2.medianBlur(lz.astype(np.uint8),9).astype(np.float32)
        fz=(cv2.GaussianBlur((skin*zone).astype(np.float32),(0,0),2)[...,None])
        base=lz*(1-fz)+flat*fz
        rgb=rgb*(1-m)+base*m
    al=a[...,3].astype(np.float32)/255
    light=not n.startswith(('res_','prop_','env_'))
    au=cv2.resize(al,(W*4,H*4),interpolation=cv2.INTER_CUBIC)
    au=cv2.GaussianBlur(au,(0,0),2.6)
    thr=0.62 if light else 0.5
    au=1/(1+np.exp(-(au-thr)*14))
    if light: au=cv2.erode(au,np.ones((3,3),np.uint8))
    Image.fromarray(np.dstack([np.clip(rgb,0,255).astype(np.uint8),(au*255).astype(np.uint8)])).save(f'{out}/{n}')
