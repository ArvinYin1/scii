import numpy as np
from PIL import Image, ImageDraw
G=19.5; PX=0.0; PY=17.5
im=Image.open('analysis/key_05.png').convert('RGB')
d=ImageDraw.Draw(im)
x=PX
while x<992: d.line([(x,0),(x,990)],fill=(0,110,255),width=1); x+=G
y=PY
while y<990: d.line([(0,y),(992,y)],fill=(0,110,255),width=1); y+=G
# bottom-centre fish region
im.crop((240,600,560,830)).resize((960,690),Image.NEAREST).save('analysis/ov_fish_zoom.png')
print("saved")
