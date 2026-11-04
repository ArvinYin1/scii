import numpy as np
from PIL import Image
a=np.asarray(Image.open('analysis/key_05.png').convert('RGB')).astype(int)
# clean empty area top-right for grid + paper
reg=a[120:300, 700:960]
lum=reg.mean(axis=2)
print("paper (p90 of clean area):", np.percentile(reg.reshape(-1,3),90,axis=0).round(1))
print("gridline (p3):", np.percentile(reg.reshape(-1,3),3,axis=0).round(1))
# bare glyph ink: bottom-left empty-ish region with only bare chars
reg2=a[560:720, 30:200]
l2=reg2.mean(axis=2)
dk=reg2.reshape(-1,3)[l2.reshape(-1)<200]
print("bare glyph ink n=%d p20:"%len(dk), np.percentile(dk,20,axis=0).round(0) if len(dk) else "none")
# headline
reg3=a[395:450, 280:720]; l3=reg3.mean(axis=2)
ink=reg3.reshape(-1,3)[l3.reshape(-1)<80]
print("headline ink n=%d p10:"%len(ink), np.percentile(ink,10,axis=0).round(0) if len(ink) else "none")
# placeholder text
reg4=a[505:535, 210:470]; l4=reg4.mean(axis=2)
ph=reg4.reshape(-1,3)[l4.reshape(-1)<190]
print("placeholder n=%d p20:"%len(ph), np.percentile(ph,20,axis=0).round(0) if len(ph) else "none")
# footer text
reg5=a[612:632, 240:720]; l5=reg5.mean(axis=2)
ft=reg5.reshape(-1,3)[l5.reshape(-1)<175]
print("footer n=%d p20:"%len(ft), np.percentile(ft,20,axis=0).round(0) if len(ft) else "none")
