import numpy as np, os
from PIL import Image
from collections import deque
G=19.5; PX=0.0; PY=17.5
PAPER=np.array([250,250,248])
def cellstats(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float)
    H,W,_=a.shape
    nx=int((W-PX)//G); ny=int((H-PY)//G)
    sol=np.zeros((ny,nx)); col=np.full((ny,nx,3),np.nan)
    for j in range(ny):
        for i in range(nx):
            cx=int(PX+G*(i+.5)); cy=int(PY+G*(j+.5))
            x0,x1=max(0,cx-8),min(W,cx+9); y0,y1=max(0,cy-8),min(H,cy+9)
            p=a[y0:y1,x0:x1].reshape(-1,3)
            if p.size==0: continue
            d=np.abs(p-PAPER).max(axis=1)
            sol[j,i]=(d>18).mean()
            if sol[j,i]>0.55: col[j,i]=np.median(p,axis=0)
    return sol,col
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
    return out
def lab(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]

ADJ=[];RND=[];SIG=[]
for f in sorted(os.listdir('analysis/all'))[::4]:
    sol,col=cellstats('analysis/all/'+f)
    body=sol>0.55
    for c in comps(body):
        if len(c)<80: continue
        S=set(c)
        # INTERIOR only: every 8-neighbour also filled  -> pure cell fill, no paper contamination
        inner=[(y,x) for (y,x) in c if all((y+dy,x+dx) in S for dy in(-1,0,1) for dx in(-1,0,1))]
        if len(inner)<40: continue
        Si=set(inner); L={p:lab(col[p]) for p in inner}
        a1=[]
        for p in inner:
            for dy,dx in ((0,1),(1,0)):
                q=(p[0]+dy,p[1]+dx)
                if q in Si: a1.append(abs(L[p]-L[q]))
        if len(a1)<25: continue
        keys=list(Si); r=[]
        for _ in range(250):
            x1=keys[np.random.randint(len(keys))]
            x2=keys[np.random.randint(len(keys))]
            if x1!=x2: r.append(abs(L[x1]-L[x2]))
        if not r: continue
        ADJ.append(np.mean(a1)); RND.append(np.mean(r)); SIG.append(np.std(list(L.values())))
adj=np.mean(ADJ); rnd=np.mean(RND); sg=np.mean(SIG)
print("=== INTERIOR cells only (%d fish) ==="%len(ADJ))
print("  mean |dL| adjacent : %6.2f" % adj)
print("  mean |dL| random   : %6.2f" % rnd)
print("  ratio              : %.2f" % (adj/rnd))
print("  within-fish L sigma: %6.2f" % sg)
print()
print("  iid-jitter prediction for adjacent |dL| = %.2f  (1.128 * sigma)" % (1.128*sg))
print("  -> observed ~= prediction : colour independent per cell (procedural jitter)")
print("  -> observed << prediction : smooth spatial field (photographic)")
