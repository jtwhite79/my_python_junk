import os
import sys
import numpy as np
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile


modelname = 'syn_1d'

mf = modflow(modelname,external_path='ref\\',load=False)

nrow, ncol, nlay = 1,10,1
delr,delc = 500.,500.
top = 5.0
botm = [0.0]

 
nstp = 1
nper = 1
perlen = np.ones((nper))
steady = [True]

for n in range(nper-1):   
    steady.append(False)

dis = mfdis(mf,nrow,ncol,nlay,nper=nper,delr=delr,delc=delc,laycbd=0,\
            top=top,botm=botm,perlen=perlen,nstp=nstp,steady=steady)
ibound = np.ones((nrow,ncol),dtype=np.int32)

#ibound[:,ncol-1] = -1
#ibound[:,0] = -1


#--set ghbs is col 1
ghb_lrchc = []
ghb_conc = []
for r in range(nrow):
    for l in range(nlay):
        ghb_lrchc.append(np.array([l+1,r+1,1,1.0,50.0]))
        ghb_conc.append(0.0)
        
init_heads = np.zeros((nrow,ncol))+1.0 
bas = mfbas(mf,ibound,init_heads)

lpf = mflpf(mf,hk=10.0,vka=10.0,laytyp=1)
#gmg = mfgmg(mf,mxiter=1000,hclose=1e-2,rclose=1e-2)
pcg = mfpcg(mf)
oc = mfoc(mf,words=['head','budget'],save_head_every=1,ihedfm=1,compact=True)
ghb = mfghb(mf,layer_row_column_head_cond=[ghb_lrchc])


rch = mfrch(mf,rech=0.00001,external=False)
 


#--run modflow to generate swr-equivalent river package
mf.write_input()    
os.system('MF2005-SWR_x64.exe '+modelname)
