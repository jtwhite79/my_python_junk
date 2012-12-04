import os, sys
import subprocess as sp
import numpy as np
from os.path import normpath
import pylab


def AddToPyPath(pth):
    if pth not in sys.path:
        sys.path.append(pth)

#Add the flopy directory to the path
pth = '..\\..\\flopy'
AddToPyPath(normpath(pth))

from mf import *
from mfreadbinaries import *
from mt import *
from mswt import *
from numpy import *


modelname = 'bro_9lay'

# Create the basic MODFLOW model structure
mf = modflow(modelname)

nrow, ncol, nlay = 411, 501, 9

top = 'ref\\top_filter_35_edge.ref'
botm = ['ref\\bot_1.ref','ref\\bot_2.ref','ref\\bot_3.ref','ref\\bot_4.ref','ref\\bot_5.ref','ref\\bot_6.ref','ref\\bot_7.ref','ref\\bot_8.ref','ref\\bot_9.ref']

delta_x,delta_y = 500.,500.
perlen = 1.0
nstp = 1.0

dis = mfdis(mf, nrow, ncol, nlay, nper = 1, delr = delta_x, delc = delta_x, laycbd = 0,\
            top = top, botm = botm, perlen = perlen, nstp = nstp)

ibound = 'ref\\ibound.ref'
ibnd_list = []
strt_list = []
for l in range(nlay):
    ibnd_list.append(ibound)
    strt_list.append(top)

bas = mfbas(mf, ibnd_list, strt_list)
lpf = mflpf(mf, laytyp = 1, hk = 1000., vka = 100.)
pcg = mfpcg(mf,mxiter=1000,hclose=1e-6)
oc = mfoc(mf)
rch = mfrch(mf,rech=0.0014)

ghb_list = np.loadtxt('ghb.dat')
chd_list = np.loadtxt('chd.dat')
ghb_master = ghb_list.copy()
chd_master = chd_list.copy()
for l in range(1,nlay):
    this_lay = ghb_list.copy()
    this_lay[:,0] = l+1
    ghb_master = np.vstack((ghb_master,this_lay))
    this_lay = chd_list.copy()
    this_lay[:,0] = l+1
    chd_master = np.vstack((chd_master,this_lay))
    

ghb = mfghb(mf,layer_row_column_head_cond=ghb_master)
chd = mfchd(mf,layer_row_column_shead_ehead=chd_master)

mf.write_input()

