# Cut every figure out of the reference sheets into trimmed transparent PNGs.
import sys,os,json,numpy as np,cv2
from PIL import Image
src,out=sys.argv[1],sys.argv[2]
os.makedirs(out,exist_ok=True)
def save(rgba,mask,name):
    ys,xs=np.where(mask>0)
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    pad=4
    y0=max(0,y0-pad);x0=max(0,x0-pad);y1=min(mask.shape[0],y1+pad);x1=min(mask.shape[1],x1+pad)
    im=rgba[y0:y1,x0:x1].copy()
    m=mask[y0:y1,x0:x1].astype(np.float32)
    im[...,3]=(np.clip(m,0,1)*255).astype(np.uint8)
    Image.fromarray(im).save(f'{out}/{name}.png')
    return dict(name=name,box=[int(x0),int(y0),int(x1),int(y1)])
def light_sheet(path,rows,cols,colx,rowy,prefix):
    a=np.array(Image.open(path).convert('RGB')).astype(np.int16)
    bg=np.median(a[2:8,2:8].reshape(-1,3),0)
    cand=(np.abs(a-bg).max(2)<14).astype(np.uint8)
    n,lab=cv2.connectedComponents(cand,connectivity=4)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))
    bgm=np.isin(lab,list(border))
    fg=(~bgm).astype(np.uint8)
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    n,lab,stats,cent=cv2.connectedComponentsWithStats(fg,8)
    rgba=np.dstack([a.astype(np.uint8),np.full(a.shape[:2],255,np.uint8)])
    # soft edge
    soft=cv2.GaussianBlur(cv2.erode(fg,np.ones((2,2),np.uint8)).astype(np.float32),(3,3),0.6)
    res=[]
    for r,rn in enumerate(rows):
        for c,cn in enumerate(cols):
            x0,x1=colx[c];y0,y1=rowy[r]
            sel=np.zeros_like(fg)
            for i in range(1,n):
                cx,cy=cent[i]
                if x0<=cx<x1 and y0<=cy<y1 and stats[i,4]>30: sel[lab==i]=1
            m=np.where(sel>0,soft,0)
            res.append(save(rgba,m,f'{prefix}{rn}_{cn}'))
    return res
def alpha_sheet(path,cells,prefix):
    a=np.array(Image.open(path).convert('RGBA'))
    al=a[...,3]
    fg=(al>200).astype(np.uint8)
    fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,stats,cent=cv2.connectedComponentsWithStats(fg,8)
    soft=cv2.GaussianBlur(cv2.erode(fg,np.ones((2,2),np.uint8)).astype(np.float32),(3,3),0.6)
    res=[]
    for name,(x0,y0,x1,y1) in cells.items():
        sel=np.zeros_like(fg)
        for i in range(1,n):
            cx,cy=cent[i]
            if x0<=cx<x1 and y0<=cy<y1 and stats[i,4]>200: sel[lab==i]=1
        m=np.where(sel>0,soft,0)
        rgb=a.copy();rgb[...,3]=255
        res.append(save(rgb,m,prefix+name))
    return res
