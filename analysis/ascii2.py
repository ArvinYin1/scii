import numpy as np, sys
from PIL import Image
G=19.5; PX=0.0; PY=17.5
def grid(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    H,W,_=a.shape
    nx=int((W-PX)//G); ny=int((H-PY)//G)
    glyphs=[];fills=[];darks=[]
    for j in range(ny):
        gr=[];fr=[];dr=[]
        for i in range(nx):
            cx=int(PX+G*(i+.5)); cy=int(PY+G*(j+.5))
            p=a[max(0,cy-8):cy+9, max(0,cx-8):cx+9].reshape(-1,3)
            if p.size==0: gr.append(' ');fr.append(0);dr.append(0);continue
            med=np.median(p,axis=0); sat=med.max()-med.min(); lum=med.mean()
            darkfrac=(p.mean(axis=1)<150).mean()
            fr.append(1 if (sat>20 and lum<225) else 0)
            dr.append(darkfrac)
            gr.append(' ')
        glyphs.append(gr);fills.append(fr);darks.append(dr)
    return np.array(fills),np.array(darks),a
f,d,a=grid(sys.argv[1])
j0,j1,i0,i1=map(int,sys.argv[2:6])
print("    "+''.join(str(i%10) for i in range(i0,i1)))
for j in range(j0,j1):
    s=''
    for i in range(i0,i1):
        if f[j,i]: s+='#'
        elif d[j,i]>0.06: s+='.'
        else: s+=' '
    print("%3d|%s"%(j,s))
