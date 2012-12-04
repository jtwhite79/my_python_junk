import os
import re
import numpy as np
import swr

est = re.compile('estimated',re.IGNORECASE)

xsec_files = os.listdir('xsec\\')

for xf in xsec_files:
    if est.search(xf) != None:    
        h,xsec = swr.load_xsec('xsec\\'+xf)
        raw = h[0].split()
        
        npt,x,y,area = int(raw[-4]),float(raw[-3]),float(raw[-2]),float(raw[-1])
        print xf,xsec[:,1].min()      
        if xsec[:,1].min() > -1.0:
         
            xsec[np.where(xsec[:,1] == xsec[:,1].min()),1] = -1.0
        h_new = ' {0:10d} {1:10.3e} {2:10.3e} {3:10.3e} '.format(xsec.shape[0],x,y,area)
        name_new = xf.replace('ESTIMATED','LOWERED')
        swr.write_profile('xsec\\'+name_new,xsec,h_new)
