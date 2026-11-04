import numpy as np, os
from PIL import Image
from collections import deque
G=19.5; PX=0.0; PY=17.5
PAPER=np.array([250,250,248])
def solidity(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    H,W,_=a.shape
    nx=int((W-PX)//G); ny=int((H-PY)//G)
    sol=np.zeros((ny,nx))
    for j in range(ny):
        for i in range(nx):
            cx=int(PX+G*(i+.5)); cy=int(PY+G*(j+.5))
            y0,y1=max(0,cy-8),min(H,cy+9); x0,x1=max(0,cx-8),min(W,cx+9)
            p=a[y0:y1,x0:x1].reshape(-1,3)
            if p.size==0: continue
            d=np.abs(p-PAPER).max(axis=1)
            sol[j,i]=(d>18).mean()
    return sol,a
def comps(body):
    ny,nx=body.shape; seen=np.zeros_like(body,bool); out=[]
    for j in range(ny):
        for i in range(nx):
            if body[j,i] and not seen[j,i]:
                q=deque([(j,i)]); seen[j,i]=True; c=[]
                while q:
                    y,x=q.popleft(); c.append((y,x))
                    for dy in(-1,0,1):
                        for dx in(-1,0,1):
                            yy,xx=y+dy,x+dx
                            if 0<=yy<ny and 0<=xx<nx and body[yy,xx] and not seen[yy,xx]:
                                seen[yy,xx]=True;q.append((yy,xx))
                out.append(c)
    return sorted(out,key=len,reverse=True)

cands=[]
files=sorted(os.listdir('analysis/all'))
for f in files:
    sol,_=solidity('analysis/all/'+f)
    body=sol>0.55
    cs=comps(body)
    for c in cs:
        if len(c)<25: continue
        ys=[y for y,x in c]; xs=[x for y,x in c]
        cands.append((len(c),max(xs)-min(xs)+1,max(ys)-min(ys)+1,f,min(ys),min(xs),max(ys),max(xs)))
cands.sort(reverse=True)
print("largest solid bodies (cells,w,h,frame,y0,x0,y1,x1):")
for c in cands[:14]: print("  ",c)
