import pylab
import numpy as np

import MFBinaryClass as mfb

nrow,ncol,nlay = 383,262,3


hds_obj = mfb.MODFLOW_Head(nlay,nrow,ncol,'tsala.hds')
totim,kstp,kper,hd,success = hds_obj.get_record()

for l in range(nlay):
    np.savetxt('ref\\init_heads_'+str(l+1)+'.ref',hd[l,:,:],fmt='%15.6e')

