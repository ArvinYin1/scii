import numpy as np
from PIL import Image
a=np.asarray(Image.open('analysis/key_05.png').convert('L')).astype(float)

def lines(y0,y1,x0,x1,axis,lbl):
    reg=a[y0:y1,x0:x1]
    p=reg.mean(axis=axis)
    base=np.percentile(p,85)
    found=[]
    for i in range(1,len(p)-1):
        if p[i]<p[i-1] and p[i]<=p[i+1] and p[i]<base-0.6:
            found.append((i, round(base-p[i],2)))
    # local coords offset
    off = x0 if axis==0 else y0
    print(lbl, "base=%.1f"%base)
    print("  positions(darkness):", [(i+off,d) for i,d in found][:26])
    pos=[i+off for i,d in found]
    if len(pos)>2:
        import numpy as np2
        print("  diffs:", np.diff(pos)[:24])
        # darkness of alternating
        print("  darkness:", [d for i,d in found][:26])
lines(140,300,700,960,0,'VERT lines (x)')
lines(140,300,700,960,1,'HORIZ lines (y)')
