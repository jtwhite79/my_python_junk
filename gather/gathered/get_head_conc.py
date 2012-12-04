import sys
import calendar
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au

import bro_info as bi



#nrow,ncol,nlay = 411,501,6
#delr,delc = 500,500
#offset = [728600.0,577350.0,0.0]
#results = 'results\\'
#nreach = 10810

day_2_sec = 1.0/86400.0


hds_handle = mfb.MODFLOW_Head(bi.nlay,bi.nrow,bi.ncol,results+'bro_6lay.hds')
totim,kstp,kper,h,success = hds_handle.get_record()

conc_handle = mfb.MT3D_Concentration(bi.nlay,bi.nrow,bi.ncol,'MT3D001.UCN')
totim_c,kstp_c,kper_c,c,success = conc_handle.get_record()
ibound = np.loadtxt('ref\\ibound.ref')

for l in range(bi.nlay):
    print 'max conc in layer '+str(l+1)+' :'+str(c[l,:,:].max()),c[l,:,:].shape
    np.savetxt('init_conc_'+str(l+1)+'.ref',c[l,:,:],fmt='%15.6e')
    np.savetxt('init_heads_'+str(l+1)+'.ref',h[l,:,:],fmt='%15.6e')
