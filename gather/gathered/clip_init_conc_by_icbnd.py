import sys
import calendar
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au




nrow,ncol,nlay = 411,501,6
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]
results = 'results\\'
nreach = 2400

day_2_sec = 1.0/86400.0

icbnd = np.loadtxt('ref\\icbnd_layer1.ref')

for l in range(nlay):
    init = np.loadtxt('ref\\init_conc_'+str(l+1)+'.ref')
    clip = init.copy()
    clip[np.where(icbnd<1)] = 0.0
    #au.plotArray(init,1,1,output=None)
    #au.plotArray(clip,1,1,output=None)
    #pylab.show()
    np.savetxt('ref\\init_conc_'+str(l+1)+'.ref',clip)
    #break