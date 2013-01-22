import pylab
import numpy as np

import MFBinaryClass as mfb
import arrayUtil as au

nrow, ncol, nlay = 383,262,3
#delr,delc = np.loadtxt('delr.dat'),np.loadtxt('delc.dat')
delr,delc = 1,1

hds_obj = mfb.MODFLOW_Head(nlay,nrow,ncol,'tsala.hds')
totim,kstp,kper,hd,success = hds_obj.get_record()
hd = np.ma.masked_where(hd < -900,hd)

#for l in range(nlay):
#    np.savetxt('ref\\init_heads_'+str(l+1)+'.ref',hd[l,:,:],fmt='%15.6e')
for l in range(nlay):
    ax1 = au.plotArray(hd[l,:,:],delc,delr,output=None)

pylab.show()
