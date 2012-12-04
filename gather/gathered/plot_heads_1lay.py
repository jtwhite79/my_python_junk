import sys
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as tk
import pylab
import MFBinaryClass_jdh as mfb

import arrayUtil as au
reload(au)

nrow,ncol,nlay = 411,501,1
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]

#--heads
hds_handle = mfb.MODFLOW_Head(1,nrow,ncol,'results\\bro_1lay.hds')
totim,kstp,kper,h,success = hds_handle.get_record()
np.savetxt('ref\init_heads.ref',h[0,:,:],fmt='%15.6e')
h = ma.masked_where(h < -100,h)
au.plotArray(h[0,:,:],delr,delc,offset=offset)
