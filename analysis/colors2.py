import numpy as np
from PIL import Image
from collections import Counter
G=19.5; PX=0.0; PY=17.5
a=np.asarray(Image.open('analysis/key_05.png').convert('RGB')).astype(int)
H,W,_=a.shape
fills=[]
for j in range(int((H-PY)//G)):
    for i in range(int((W-PX)//G)):
        cx=int(PX+G*(i+.5)); cy=int(PY+G*(j+.5))
        p=a[cy-7:cy+8, cx-7:cx+8].reshape(-1,3)
        if p.size==0: continue
        # take the modal cluster: pixels that are NOT paper and NOT glyph-light
        med=np.median(p,axis=0); sat=med.max()-med.min()
        if sat>18 and med.mean()<228:
            fills.append(tuple(med.astype(int)))
print("filled cells sampled:", len(fills))
c=Counter(fills)
print("\nmost common exact fill colours:")
for col,n in c.most_common(18):
    print("  #%02X%02X%02X"%col, n)
arr=np.array(fills)
print("\nOverall fill stats: mean", arr.mean(axis=0).round(1), "median", np.median(arr,axis=0))
# hue families
import colorsys
fam=Counter()
for col in fills:
    r,g,b=[v/255 for v in col]
    h,s,v=colorsys.rgb_to_hsv(r,g,b)
    if s<0.10: fam['neutral/grey']+=1
    elif h<0.045 or h>0.95: fam['red/terracotta']+=1
    elif h<0.09: fam['orange/salmon']+=1
    elif h<0.19: fam['olive/ochre']+=1
    elif h<0.45: fam['green']+=1
    elif h<0.75: fam['blue/slate']+=1
    else: fam['violet']+=1
print("\nhue families:", fam.most_common())
