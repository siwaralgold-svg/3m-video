import sys,glob,os,numpy as np,cv2,torch
from PIL import Image
from spandrel import ModelLoader
m=ModelLoader().load_from_file(sys.argv[1]).model.eval()
torch.set_num_threads(os.cpu_count())
out=sys.argv[3];os.makedirs(out,exist_ok=True)
for f in sorted(glob.glob(sys.argv[2])):
    name=os.path.basename(f);dst=f'{out}/{name}'
    if os.path.exists(dst): continue
    a=np.array(Image.open(f).convert('RGBA'))
    al=a[...,3].astype(np.float32)/255
    light = not name.startswith(('res_','prop_','env_'))
    hard=(al>0.5).astype(np.uint8)
    if light: hard=cv2.erode(hard,np.ones((3,3),np.uint8))  # drop cream fringe
    rgb=a[...,:3].copy()
    # extend edge colours outward so the model sees no background
    inner=cv2.erode(hard,np.ones((3,3),np.uint8))
    rgb=cv2.inpaint(rgb,(1-inner).astype(np.uint8)*255,5,cv2.INPAINT_TELEA) if inner.sum() else rgb
    pad=8
    rgbp=cv2.copyMakeBorder(rgb,pad,pad,pad,pad,cv2.BORDER_REPLICATE)
    with torch.no_grad():
        t=torch.from_numpy(rgbp).float().permute(2,0,1)[None]/255
        y=m(t)[0].clamp(0,1).permute(1,2,0).numpy()
    y=(y*255).round().astype(np.uint8)[pad*4:-pad*4,pad*4:-pad*4]
    H,W=hard.shape
    au=cv2.resize(hard.astype(np.float32),(W*4,H*4),interpolation=cv2.INTER_CUBIC)
    au=cv2.GaussianBlur(au,(0,0),1.6)
    au=np.clip((au-0.5)*2.2+0.5,0,1)
    Image.fromarray(np.dstack([y,(au*255).astype(np.uint8)])).save(dst)
    print(name,W*4,H*4,flush=True)
