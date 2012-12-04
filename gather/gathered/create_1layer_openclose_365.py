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

def load_listarray(file):
    f = open(file,'r')
    lst = []
    line = f.readline()
    
    raw = line.strip().split()
    array = np.array(raw)
    lst.append(array)
    for line in f:
        raw = line.strip().split()
        for r in range(len(raw)):
            raw[r] = float(raw[r])
        array = np.array(raw)
        print array
        lst.append(array)
        break
    f.close()
    return lst       



modelname = 'bro_1lay'

# Create the basic MODFLOW model structure
mf = modflow(modelname)

nrow, ncol, nlay = 411, 501, 1

#top = np.loadtxt('ref\\top_filter_35_edge.ref')
#botm = np.loadtxt('ref\\t1.ref')
top = 'ref\\top_filter_35_edge.ref'
botm = 'ref\\bot_9.ref'

delta_x,delta_y = 500.,500.
#perlen = 1.0
nstp = 1.0
perlen = np.ones(365)
nstp = np.ones(365)

dis = mfdis(mf, nrow, ncol, nlay, nper = len(perlen), delr = delta_x, delc = delta_x, laycbd = 0,\
            top = top, botm = botm, perlen = perlen, nstp = nstp)

#ibound = np.loadtxt('ref\\ibound.ref',dtype='int')
ibound = 'ref\\ibound.ref'
bas = mfbas(mf, ibound, top)
lpf = mflpf(mf, hk = 1000., vka = 100.)
pcg = mfpcg(mf,mxiter=1000,hclose=1e-6)
oc = mfoc(mf)
rch_list = np.loadtxt('15_day_ma.dat')
rch = mfrch(mf,rech=list(rch_list[:,1]/12.0))
print 'annual rainfall (inches): ',np.cumsum(rch_list[:,1])[-1]
et_rate = 0.01 #70% of precip
et_extdepth = 3.0 #ft
evt = mfevt(mf,surf=[top],evtr=[et_rate],exdp=et_extdepth)

ghb_list = np.loadtxt('..\\shapes\\ghb.dat')
ghb = mfghb(mf,layer_row_column_head_cond=ghb_list)
chd_list = [np.loadtxt('..\\shapes\\chd.dat')]
chd = mfchd(mf,layer_row_column_shead_ehead=chd_list)

mf.write_input()

