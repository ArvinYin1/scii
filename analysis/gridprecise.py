import numpy as np
from PIL import Image
a=np.asarray(Image.open('analysis/key_05.png').convert('L')).astype(float)

def prof(y0,y1,x0,x1,axis):
    reg=a[y0:y1,x0:x1]
    return reg.mean(axis=axis)

for (y0,y1,x0,x1,lbl) in [(430,520,620,980,'clean A'),(140,300,700,960,'clean B'),(600,860,60,300,'clean C')]:
    px=prof(y0,y1,x0,x1,0); py=prof(y0,y1,x0,x1,1)
    for name,p in (('X',px),('Y',py)):
        q=p-p.mean()
        ac=np.correlate(q,q,'full')[len(q)-1:]
        ac/=ac[0]
        # first strong peak beyond lag 6
        cand=[(lag,ac[lag]) for lag in range(6,min(80,len(ac)-1))]
        cand.sort(key=lambda t:-t[1])
        print(lbl,name,"top lags:",[(l,round(v,3)) for l,v in cand[:4]])
    print()
