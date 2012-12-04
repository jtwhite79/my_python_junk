import sys
import numpy as np
import pylab

import arrayUtil as au
import MFBinaryClass as mfb 
reload(mfb)


nlay,nrow,ncol = 9,301,501
delr,delc = 500,500
offset = [668350.,288415.]

hds_file = 'Results\\bro.hds'
hdsObj = mfb.MODFLOW_Head(nlay,nrow,ncol,hds_file)
totim,kstp,kper,heads,success = hdsObj.get_record()
for ilay in range(0,nlay):
    au.writeArrayToFile(heads[ilay,:,:],'layer_'+str(ilay+1)+'.ref')

au.plotArray(heads[0,::2,::2],delr,delc,bln='bro_hydro.bln',title=str(ilay+1)+' '+str(totim),offset=offset)
  



