import numpy as np, os
from PIL import Image
from collections import deque, Counter
G=19.5; PX=0.0; PY=17.5
PAPER=np.array([250,250,248])

def cellstats(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float)
    H,W,_=a.shape
    nx=int((W-PX)//G); ny=int((H-PY)//G)
    sol=np.zeros((ny,nx)); lum=np.full((ny,nx),np.nan)
    for j in range(ny):
        for i in range(nx):
            cx=int(PX+G*(i+.5)); cy=int(PY+G*(j+.5))
            x0,x1=max(0,cx-8),min(W,cx+9); y0,y1=max(0,cy-8),min(H,cy+9)
            p=a[y0:y1,x0:x1].reshape(-1,3)
            if p.size==0: continue
            d=np.abs(p-PAPER).max(axis=1)
            sol[j,i]=(d>18).mean()
            if sol[j,i]>0.55: lum[j,i]=p.mean()
    return sol,lum

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

angles=[]; elong=[]; sizes=[]
files=sorted(os.listdir('analysis/all'))[::4]
for f in files:
    sol,lum=cellstats('analysis/all/'+f)
    body=sol>0.55
    for c in comps(body):
        if len(c)<45: continue
        pts=np.array([[x,y] for y,x in c],float)   # (col,row)
        pts-=pts.mean(axis=0)
        cov=np.cov(pts.T)
        w,v=np.linalg.eigh(cov)
        l2,l1=w[0],w[1]
        if l1<=0: continue
        axis=v[:,1]                                # major axis (dx,dy)
        ang=np.degrees(np.arctan2(axis[1],axis[0]))%180.0
        angles.append(ang); elong.append(np.sqrt(l1/max(l2,1e-9))); sizes.append(len(c))

angles=np.array(angles); elong=np.array(elong)
keep=elong>1.7
print("fish components measured:", len(angles), " elongated(>1.7):", keep.sum())
A=angles[keep]
print("\n=== principal-axis angle distribution (deg, mod 180) ===")
h,e=np.histogram(A,bins=18,range=(0,180))
for k in range(18):
    print("  %3d-%3d  %3d  %s"%(e[k],e[k+1],h[k],'#'*int(60*h[k]/max(h.max(),1))))
# is it clustered near 0/90, or spread?
near_axis=((A<12)|(A>168)|(np.abs(A-90)<12)).mean()
print("\nfraction within 12deg of horizontal/vertical: %.2f" % near_axis)
print("fraction in 30-60 or 120-150 (diagonal): %.2f" % (((A>30)&(A<60))|((A>120)&(A<150))).mean())
