import sys
from PIL import Image,ImageDraw
outs=[]
z=int(sys.argv[2])
for f in sys.argv[3:]:
    im=Image.open(f).convert('RGBA');bg=Image.new('RGBA',im.size,(60,120,80,255));bg.alpha_composite(im)
    im=bg.resize((im.width*z,im.height*z),Image.NEAREST);d=ImageDraw.Draw(im)
    for x in range(0,im.width,10*z):
        d.line([(x,0),(x,im.height)],fill=(255,0,0,90) if (x//z)%50 else (255,255,0,200));d.text((x+1,1),str(x//z),fill='yellow')
    for y in range(0,im.height,10*z):
        d.line([(0,y),(im.width,y)],fill=(255,0,0,90) if (y//z)%50 else (255,255,0,200));d.text((1,y+1),str(y//z),fill='yellow')
    outs.append(im)
W=Image.new('RGB',(sum(o.width for o in outs)+10*len(outs),max(o.height for o in outs)),'black');x=0
for o in outs: W.paste(o,(x,0));x+=o.width+10
W.save(sys.argv[1])
