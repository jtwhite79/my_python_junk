import sys
import os
import math
import numpy as np
import pylab
import gc

from datetime import datetime
from datetime import timedelta

import MFArrayUtil as au
import MFData as mfd
import MFBinaryClass as mfb 
import shapefile as sf


#--get command line arguments
REFDir = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','UMD.01','REF' )
OutputDir = os.path.join( 'D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Grid','UMD' )
#--problem size
nlay,nrow,ncol = 3,189,101
x0, y0  = 539750.0, 2785750.0
dx,dy   = 500., 500.
#--read ibound
ib_ref = os.path.join( REFDir, 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--read the top of the model
lse_ref = os.path.join( REFDir, 'UMD_URBAN_EDEN_TOPO.ref' )
model_lse = au.loadArrayFromFile(nrow,ncol,lse_ref)
#--read the offshore array
offshore_ref = os.path.join( REFDir, 'UMD_OFFSHORE.ref' )
offshore = au.loadArrayFromFile(nrow,ncol,offshore_ref)
#--read the HK
HK_ref = os.path.join( REFDir, 'UMD_HK_L1.ref' )
HK = au.loadArrayFromFile(nrow,ncol,HK_ref)
#--read the bottom of the model
botm = np.empty( (nlay+1,nrow,ncol) )
botm[0,:,:] = np.copy( model_lse )
for ilay in xrange(0,nlay):
    bot_ref = os.path.join( REFDir, 'UMD_BOTM_L{0}.ref'.format( ilay+1 ) )
    b = au.loadArrayFromFile(nrow,ncol,bot_ref)
    botm[ilay+1] = np.copy( b )
#--process BT and HK
BT = np.empty( (nrow,ncol), np.float )
for irow in xrange(0,nrow):
    for jcol in xrange(0,ncol):
        BT[irow,jcol] = (botm[0,irow,jcol] - botm[nlay,irow,jcol]) * HK[irow,jcol]
        HK[irow,jcol] = math.log10( HK[irow,jcol] )
#--save the data
temp = np.empty( (nrow,ncol) )
temp = botm[0,:,:] - botm[nlay,:,:]
Output_ref = os.path.join( OutputDir, 'UMD_BTHICK.asc' )
au.ref2grd(Output_ref,temp,nrow,ncol,[x0,y0],dx)
Output_ref = os.path.join( OutputDir, 'UMD_BLOGHK.asc' )
au.ref2grd(Output_ref,HK,nrow,ncol,[x0,y0],dx)
Output_ref = os.path.join( OutputDir, 'UMD_BT.asc' )
au.ref2grd(Output_ref,BT,nrow,ncol,[x0,y0],dx)
