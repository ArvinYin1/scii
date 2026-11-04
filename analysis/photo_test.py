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
            if sol[j,i]>0.55:
                col[j,i]=np.median(p,axis=0)     # fill colour, glyph is a minority
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

def lab(rgb):
    # cheap perceptual lightness
    return 0.299*rgb[0]+0.587*rgb[1]+0.114*rgb[2]

adj_d=[]; rnd_d=[]; grad_corr=[]
files=sorted(os.listdir('analysis/all'))[::4]
nfish=0
for f in files:
    sol,col=cellstats('analysis/all/'+f)
    body=sol>0.55
    for c in comps(body):
        if len(c)<60: continue
        S=set(c)
        L={}
        for y,x in c: L[(y,x)]=lab(col[y,x])
        vals=[]
        for (y,x) in c:
            for dy,dx in ((0,1),(1,0)):
                if (y+dy,x+dx) in S:
                    vals.append(abs(L[(y,x)]-L[(y+dy,x+dx)]))
        if len(vals)<20: continue
        adj_d.append(np.mean(vals))
        # null: random pairs inside the same fish
        keys=list(S); rp=[]
        for _ in range(200):
            a1=keys[np.random.randint(len(keys))]; a2=keys[np.random.randint(len(keys))]
            if a1!=a2: rp.append(abs(L[a1]-L[a2]))
        if rp: rnd_d.append(np.mean(rp))
        # countershading: lightness vs position along the MINOR (dorso-ventral) axis
        pts=np.array([[x,y] for y,x in c],float); mu=pts.mean(axis=0)
        cov=np.cov((pts-mu).T); w,v=np.linalg.eigh(cov)
        minor=v[:,0]
        proj=np.array([(np.array([x,y])-mu)@minor for y,x in c])
        Ls=np.array([L[(y,x)] for y,x in c])
        if proj.std()>0.3: grad_corr.append(np.corrcoef(proj,Ls)[0,1])
        nfish+=1

adj=np.mean(adj_d); rnd=np.mean(rnd_d)
print("fish analysed:", nfish)
print()
print("=== SPATIAL COHERENCE OF CELL COLOUR ===")
print("  mean |ΔL| between ADJACENT cells : %6.2f" % adj)
print("  mean |ΔL| between RANDOM  cells : %6.2f" % rnd)
ratio = adj/rnd if rnd else float('nan')
print("  ratio adjacent/random           : %.2f" % ratio)
print("  (≈1.0 -> colours are random noise;  <<1.0 -> smooth photographic field)")
print()
g=np.array(grad_corr)
g=g[~np.isnan(g)]
print("=== COUNTERSHADING (lightness vs dorso-ventral axis) ===")
print("  fish with a measurable gradient : %d" % len(g))
print("  mean correlation                : %+.3f" % g.mean())
print("  frac with |r|>0.5               : %.2f" % (np.abs(g)>0.5).mean())
