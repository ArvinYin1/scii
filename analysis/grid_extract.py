import numpy as np
from PIL import Image
from collections import Counter

img = Image.open('analysis/key_05.png').convert('RGB')
a = np.asarray(img).astype(int)
H,W,_=a.shape
G=19.5
# grid phase: gridlines at 18,37,57,76,96 -> ~19.5 starting 18? use x0=18-19.5*? 
def cells(x0,y0):
    out=[]
    ny=int((H-y0)//G); nx=int((W-x0)//G)
    for j in range(ny):
        for i in range(nx):
            cx=int(x0+G*(i+.5)); cy=int(y0+G*(j+.5))
            if not(2<=cx<W-2 and 2<=cy<H-2): continue
            out.append((i,j,cx,cy))
    return out
# find phase by checking fill detection stability: use 18.0/17.0
for (x0,y0) in [(18,17),(18.5,17.5)]:
    cs=cells(x0,y0)
    filled=0; dark=0
    for i,j,cx,cy in cs:
        p=a[cy-4:cy+5, cx-4:cx+5].reshape(-1,3).mean(axis=0)
        sat=p.max()-p.min()
        if sat>25 and p.max()<230: filled+=1
        if p.mean()<150: dark+=1
    print((x0,y0),"cells",len(cs),"coloredfill",filled,"darkglyph",dark)
