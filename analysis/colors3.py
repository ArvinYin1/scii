import numpy as np, colorsys
from PIL import Image
a=np.asarray(Image.open('analysis/key_05.png').convert('RGB')).astype(int)
G=19.5;PX=0.;PY=17.5;H,W,_=a.shape
fams={}
for j in range(int((H-PY)//G)):
    for i in range(int((W-PX)//G)):
        cx=int(PX+G*(i+.5));cy=int(PY+G*(j+.5))
        p=a[cy-7:cy+8,cx-7:cx+8].reshape(-1,3)
        if p.size==0:continue
        med=np.median(p,axis=0);sat=med.max()-med.min()
        if sat>18 and med.mean()<228:
            h,s,v=colorsys.rgb_to_hsv(*(med/255))
            k=('red/terracotta' if (h<0.045 or h>0.95) else 'orange/salmon' if h<0.09
               else 'olive/ochre' if h<0.19 else 'green' if h<0.45 else 'blue/slate')
            fams.setdefault(k,[]).append(med)
print("family centroids (mean fill):")
for k,v in fams.items():
    m=np.mean(v,axis=0).round(0)
    print("  %-16s n=%3d  #%02X%02X%02X"% (k,len(v),*m.astype(int)))

# grid line colour: average along a known line x=0? use x=19.5*20=390
for x in [390,409,429]:
    col=a[150:900,x].mean(axis=0); print("gridline x=%d avg"%x, col.round(1), "#%02X%02X%02X"%tuple(col.astype(int)))
# paper between lines
print("paper:", a[150:900,395].mean(axis=0).round(1))

# bare glyph ink: darkest pixels in an area with only bare glyphs (left edge region)
reg=a[560:700, 20:150].reshape(-1,3)
dark=reg[reg.mean(axis=1)<170]
print("bare glyph ink (p10):", np.percentile(dark,10,axis=0).round(0), " n=",len(dark))
# headline ink
reg2=a[400:445, 300:700].reshape(-1,3)
ink=reg2[reg2.mean(axis=1)<90]
print("headline ink p10:", np.percentile(ink,10,axis=0).round(0), "n=",len(ink))
