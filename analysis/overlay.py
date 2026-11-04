import numpy as np
from PIL import Image, ImageDraw
G=19.5; X0=18.0; Y0=17.0
src='analysis/key_05.png'
a=np.asarray(Image.open(src).convert('RGB')).copy()
im=Image.fromarray(a)
d=ImageDraw.Draw(im)
# draw detected grid in blue-ish
k=0
x=X0
while x<992:
    d.line([(x,0),(x,990)],fill=(0,120,255),width=1); x+=G
y=Y0
while y<990:
    d.line([(0,y),(992,y)],fill=(0,120,255),width=1); y+=G
im.crop((600,520,992,800)).resize((784,560),Image.NEAREST).save('analysis/overlay_crop.png')
im.resize((700,700)).save('analysis/overlay_full.png')
print("ok")
