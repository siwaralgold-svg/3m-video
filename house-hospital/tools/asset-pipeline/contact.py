import sys,glob,os
from PIL import Image,ImageDraw
files=sorted(glob.glob(sys.argv[1]));cell=int(sys.argv[3]) if len(sys.argv)>3 else 200
cols=10;rows=(len(files)+cols-1)//cols
W=Image.new('RGB',(cols*cell,rows*(cell+14)),(40,90,60))
d=ImageDraw.Draw(W)
for i,f in enumerate(files):
    im=Image.open(f).convert('RGBA');im.thumbnail((cell-6,cell-6))
    x,y=(i%cols)*cell,(i//cols)*(cell+14)
    W.paste(im,(x+3,y+3),im);d.text((x+3,y+cell),os.path.basename(f)[:28],fill='white')
W.save(sys.argv[2])
