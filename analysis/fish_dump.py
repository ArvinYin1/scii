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
    return sol,ny,nx
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

best=None
for f in sorted(os.listdir('analysis/all')):
    sol,ny,nx=solidity('analysis/all/'+f)
    body=sol>0.55
    for c in comps(body)[:3]:
        ys=[y for y,x in c]; xs=[x for y,x in c]
        y0,y1,x0,x1=min(ys),max(ys),min(xs),max(xs)
        if y0<2 or x0<2 or y1>ny-3 or x1>nx-3: continue
        area=len(c)
        if best is None or area>best[0]:
            best=(area,f,y0,y1,x0,x1,sol,body)
if best:
    area,f,y0,y1,x0,x1,sol,body=best
    print("BEST FULLY-CONTAINED FISH:",f,"cells",area,"box w=%d h=%d"%(x1-x0+1,y1-y0+1))
    print("body mask (# = filled >0.55, o = bare glyph 0.10-0.55, space = empty)")
    for j in range(y0,y1+1):
        s=''
        for i in range(x0,x1+1):
            if body[j,i]: s+='#'
            elif sol[j,i]>0.10: s+='o'
            else: s+=' '
        print("  |"+s+"|")
else:
    print("none fully contained; showing best clipped")
