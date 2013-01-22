import sys
import os
import math
import numpy as np
import pylab
import gc

from datetime import datetime
from datetime import timedelta

import MFArrayUtil as au
import MFBinaryClass as mfb 
import shapefile as sf

import UMDUtils as umdutils

def SaltwaterPosition(nrow,ncol,elev,zeta):
    elevmin = 0.2 #1.0e-6
    value = np.zeros( (nrow,ncol), np.float )
    for irow in xrange(0,nrow):
        for jcol in xrange(0,ncol):
            if zeta[irow,jcol] > elev[irow,jcol] + elevmin:
                value[irow,jcol] = 1.0
    return value

#preliminary figure specifications
from matplotlib.pyplot import *
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed' #'Arial'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42

ticksize = 6
mpl.rcParams['legend.fontsize']  = 6
mpl.rcParams['axes.labelsize']   = 8
mpl.rcParams['xtick.labelsize']  = ticksize
mpl.rcParams['ytick.labelsize']  = ticksize

#--get command line arguments
ResultsDir = os.path.join( '..', 'Results' )
narg = len(sys.argv)
iarg = 0
if narg > 1:
    while iarg < narg-1:
        iarg += 1
        basearg = sys.argv[iarg].lower()
        if basearg == '-resultsdir':
            try:
                iarg += 1
                ResultsDir = sys.argv[iarg]
                print 'command line arg: -resultsdir = ', ResultsDir
            except:
                print 'cannot parse command line arg: -resultsdir'

#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nsurf,nlay,nrow,ncol = 2,3,189,101
#--read ibound
ib_ref = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--read the bottom of the model
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L1.ref' )
model_bot1 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L2.ref' )
model_bot2 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L3.ref' )
model_bot3 = au.loadArrayFromFile(nrow,ncol,bot_ref)
#--default data if command line argument not defined for variable
head_file = os.path.join( ResultsDir, 'UMD.hds' )
zeta_file = os.path.join( ResultsDir, 'UMD.zta' )
#--get available times in the head file
#--get available times in the head file
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
head_time_list = headObj.get_time_list()
#--zeta surface to extract
zetaObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,zeta_file)
zta_text = '    ZETAPLANE  1'
z1_time_list = zetaObj.get_time_list(zta_text)
zta_text = '    ZETAPLANE  2'
z2_time_list = zetaObj.get_time_list(zta_text)
#--get last head and last zeta
#--read head data - final zeta surface
iposition = long( head_time_list[-1,3] )
totim,kstp,kper,h,success = headObj.get_array(iposition)
#--read zeta data - final zeta surface
iposition = long( z1_time_list[-1,3] )
z1,totim,success = zetaObj.get_array(iposition)
iposition = long( z2_time_list[-1,3] )
z2,totim,success = zetaObj.get_array(iposition)
#--save data
#--heads
for ilay in xrange(0,nlay):
    hfile = os.path.join( '..','REF','UMD_IHEAD_L{0}_SIM.ref'.format( ilay+1 ) )
    print 'writing...{0}'.format( os.path.basename( hfile ) )
    np.savetxt(hfile,h[ilay,:,:])
    zfile = os.path.join( '..','REF','UMD_IZETA1_L{0}_SIM.ref'.format( ilay+1 ) )
    print 'writing...{0}'.format( os.path.basename( zfile ) )
    np.savetxt(zfile,z1[ilay,:,:])
    zfile = os.path.join( '..','REF','UMD_IZETA2_L{0}_SIM.ref'.format( ilay+1 ) )
    print 'writing...{0}'.format( os.path.basename( zfile ) )
    np.savetxt(zfile,z2[ilay,:,:])
    



