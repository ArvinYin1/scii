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
def L(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
maj_r=[];min_r=[];rad_r=[];rng=[]
for f in sorted(os.listdir('analysis/all'))[::4]:
    sol,col=cellstats('analysis/all/'+f)
    for c in comps(sol>0.55):
        if len(c)<80: continue
        S=set(c)
        inner=[(y,x) for (y,x) in c if all((y+dy,x+dx) in S for dy in(-1,0,1) for dx in(-1,0,1))]
        if len(inner)<40: continue
        pts=np.array([[x,y] for y,x in inner],float); mu=pts.mean(axis=0)
        cov=np.cov((pts-mu).T); w,v=np.linalg.eigh(cov)
        major,minor=v[:,1],v[:,0]
        Ls=np.array([L(col[y,x]) for y,x in inner])
        if Ls.std()<5: continue
        pm=(pts-mu)@major; pn=(pts-mu)@minor; pr=np.linalg.norm(pts-mu,axis=1)
        maj_r.append(np.corrcoef(pm,Ls)[0,1])
        min_r.append(np.corrcoef(pn,Ls)[0,1])
        rad_r.append(np.corrcoef(pr,Ls)[0,1])
        rng.append((Ls.min(),Ls.max()))
maj_r=np.array(maj_r);min_r=np.array(min_r);rad_r=np.array(rad_r)
rng=np.array(rng)
print("=== where does the lightness gradient run? (%d fish interiors) ==="%len(maj_r))
print("  along body length (head->tail) r = %+.3f   |r|>0.5 in %.0f%%"%(maj_r.mean(),(np.abs(maj_r)>0.5).mean()*100))
print("  across body      (dorsal->ventral) r = %+.3f |r|>0.5 in %.0f%%"%(min_r.mean(),(np.abs(min_r)>0.5).mean()*100))
print("  radially from centre r = %+.3f           |r|>0.5 in %.0f%%"%(rad_r.mean(),(np.abs(rad_r)>0.5).mean()*100))
print()
print("=== dynamic range of lightness inside ONE fish ===")
print("  mean (max-min) = %.0f of 255   -> about %.0f%% of full range"%( (rng[:,1]-rng[:,0]).mean(), ((rng[:,1]-rng[:,0]).mean()/255)*100 ))
print("  mean min L = %.0f, mean max L = %.0f"%(rng[:,0].mean(), rng[:,1].mean()))
