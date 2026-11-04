import numpy as np
from PIL import Image
import sys
G=19.5; X0=18.0; Y0=17.0
def dump(path, j0=0,j1=None,i0=0,i1=None):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    H,W,_=a.shape
    nx=int((W-X0)//G); ny=int((H-Y0)//G)
    j1=j1 or ny; i1=i1 or nx
    lines=[]
    for j in range(j0,min(j1,ny)):
        s=''
        for i in range(i0,min(i1,nx)):
            cx=int(X0+G*(i+.5)); cy=int(Y0+G*(j+.5))
            patch=a[max(0,cy-6):cy+7, max(0,cx-6):cx+7].reshape(-1,3)
            mu=patch.mean(axis=0); sat=mu.max()-mu.min()
            if sat>22 and mu.max()<232 and mu.mean()<215:
                # classify hue family
                r,g,b=mu
                if r>g>b and r-b>22: ch='R' if r>150 else 'r'
                elif abs(int(g)-int(b))<18 and g>r: ch='B'
                elif r>140 and g>120 and b<130: ch='Y'
                else: ch='#'
            elif mu.mean()<190: ch='.'
            else: ch=' '
            s+=ch
        lines.append('%2d|%s'%(j,s))
    # col ruler
    print('   '+''.join(str(i%10) for i in range(i0,min(i1,nx))))
    print('\n'.join(lines))
dump(sys.argv[1], *map(int,sys.argv[2:]))
