import numpy as np, subprocess, os
from PIL import Image
from collections import Counter, deque

V='/Users/yinwenlong.arvin/Downloads/3WzIRLEUmwL6GDHl.mp4'
os.makedirs('analysis/all',exist_ok=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',V,'-vf','fps=6','analysis/all/a_%03d.png'],check=True)
G=19.5; X0=18.0; Y0=17.0

def cellgrid(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    H,W,_=a.shape
    nx=int((W-X0)//G); ny=int((H-Y0)//G)
    # states: 0 empty, 1 bare glyph (dark ink, no fill), 2 filled color block
    st=np.zeros((ny,nx),dtype=int)
    col=np.zeros((ny,nx,3),dtype=int)
    for j in range(ny):
        for i in range(nx):
            cx=int(X0+G*(i+.5)); cy=int(Y0+G*(j+.5))
            patch=a[max(0,cy-6):cy+7, max(0,cx-6):cx+7].reshape(-1,3)
            if patch.size==0: continue
            mu=patch.mean(axis=0); sat=mu.max()-mu.min()
            p90=np.percentile(patch,90,axis=0)
            # filled: median-ish body color has saturation and is darker than bg
            if sat>22 and mu.max()<232 and mu.mean()<215:
                st[j,i]=2; col[j,i]=mu
            elif mu.mean()<185 and sat<=60:   # dark ink glyph on paper
                st[j,i]=1
    return st,col,a

def components(st):
    ny,nx=st.shape; seen=np.zeros_like(st,bool); comps=[]
    for j in range(ny):
        for i in range(nx):
            if st[j,i] and not seen[j,i]:
                q=deque([(j,i)]); seen[j,i]=True; cells=[]
                while q:
                    y,x=q.popleft(); cells.append((y,x))
                    for dy in(-1,0,1):
                        for dx in(-1,0,1):
                            yy,xx=y+dy,x+dx
                            if 0<=yy<ny and 0<=xx<nx and st[yy,xx] and not seen[yy,xx]:
                                seen[yy,xx]=True; q.append((yy,xx))
                comps.append(cells)
    return sorted(comps,key=len,reverse=True)

best=[]
for f in sorted(os.listdir('analysis/all')):
    p='analysis/all/'+f
    st,col,_=cellgrid(p)
    comps=components(st)
    for c in comps[:4]:
        ys=[y for y,x in c]; xs=[x for y,x in c]
        h=max(ys)-min(ys)+1; w=max(xs)-min(xs)+1
        best.append((len(c),w,h,f,min(ys),min(xs)))
best.sort(reverse=True)
print("N components scanned:",len(best))
print("top by cell count (count,w,h,frame,oy,ox):")
for b in best[:12]: print("  ",b)
print("\nsize distribution of biggest per frame:")
seenf=set()
for b in best:
    if b[3] in seenf: continue
    seenf.add(b[3])
    if len(seenf)>14: break
    print("  ",b)
