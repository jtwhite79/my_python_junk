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


hds_handle = mfb.MODFLOW_Head(nlay,nrow,ncol,results+'bro_6lay.hds')
totim,kstp,kper,h,success = hds_handle.get_record()

conc_handle = mfb.MT3D_Concentration(nlay,nrow,ncol,'MT3D001.UCN')
totim_c,kstp_c,kper_c,c,success = conc_handle.get_record()
ibound = np.loadtxt('ref\\ibound.ref')
for l in range(nlay):
    #au.plotArray(h[l,:,:],500,500,output=None,title='heads'+str(l+1))
    
    this_conc = c[l,:,:]
    this_conc = ma.masked_where(ibound==0,this_conc)
    au.plotArray(this_conc,500,500,output=None,title='conc'+str(l+1))
pylab.show()