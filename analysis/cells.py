import numpy as np
from PIL import Image
from collections import Counter

img = Image.open('analysis/key_05.png').convert('RGB')
a = np.asarray(img).astype(int)
H,W,_=a.shape

# clean bg sample: bottom-left empty
for (y0,y1,x0,x1,lbl) in [(600,700,880,980,'bg A'),(940,980,300,500,'bg B'),(300,360,700,900,'bg C')]:
    r=a[y0:y1,x0:x1].reshape(-1,3)
    print(lbl, "median", np.median(r,axis=0), "p10", np.percentile(r,10,axis=0))

# saturated colored pixels = fish cell fills
mx=a.max(axis=2); mn=a.min(axis=2)
sat=mx-mn
mask=(sat>28)&(mx<235)
print("colored px count", mask.sum())
ys,xs=np.nonzero(mask)
cols=a[mask]
# cluster colors coarsely
q=(cols//16*16)
c=Counter(map(tuple,q))
print("\ntop cell colors (quantized):")
for col,n in c.most_common(14):
    print("  #%02X%02X%02X"%col, n)
