import numpy as np
from PIL import Image

img = Image.open('analysis/key_05.png').convert('RGB')
a = np.asarray(img).astype(int)
H,W,_ = a.shape
print("size", W, H)

# ---- background & grid detection on a clean corner region ----
reg = a[500:900, 900:990]   # right side, empty
print("bg mean", reg.reshape(-1,3).mean(axis=0), "min", reg.reshape(-1,3).min(axis=0))

# column profile to find vertical grid lines
strip = a[560:900, 0:992, :].mean(axis=(0,2))
# find local minima (darker = gridline)
med = np.median(strip)
dark = strip < med - 0.35
idx = np.where(dark)[0]
# group consecutive
groups=[]
cur=[idx[0]] if len(idx) else []
for i in idx[1:]:
    if i-cur[-1]<=2: cur.append(i)
    else: groups.append(cur); cur=[i]
if cur: groups.append(cur)
centers=[int(np.mean(g)) for g in groups]
print("vert gridlines:", centers[:40])
if len(centers)>2:
    d=np.diff(centers); print("spacing med", np.median(d), "diffs", d[:25])

rowstrip = a[0:990, 60:300, :].mean(axis=(1,2))
med2=np.median(rowstrip); dark2=rowstrip<med2-0.35
idx2=np.where(dark2)[0]; groups=[]; cur=[idx2[0]] if len(idx2) else []
for i in idx2[1:]:
    if i-cur[-1]<=2: cur.append(i)
    else: groups.append(cur); cur=[i]
if cur: groups.append(cur)
c2=[int(np.mean(g)) for g in groups]
print("horiz gridlines:", c2[:40])
if len(c2)>2:
    d2=np.diff(c2); print("spacing med", np.median(d2), "diffs", d2[:25])
