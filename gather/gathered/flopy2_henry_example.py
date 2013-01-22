import os
import numpy as np

from flopy2.modflow import *
from flopy2.mt3dms import *
from flopy2.seawat import *

import coarse_config


#--external dir
ext_path = 'ref\\'
if not os.path.exists(ext_path):
    os.mkdir(ext_path)


real_num = 1
hk_unit = 150
vk_unit = 151
modelname = 'henry'
mf = Modflow(modelname,external_path=ext_path)
#setattr(mf,'free_format',True)

x_len = coarse_config.x_len
z_len = coarse_config.z_len
nrow = coarse_config.nrow
ncol = coarse_config.ncol
nlay = coarse_config.nlay
delr = x_len/ncol
delc =1.0
delz = z_len/nlay
print delr,delz
top = 0.0
botm = np.cumsum(np.zeros(nlay) - delz)
botm -= top

nstp = 1
nper = 2
perlen = np.zeros((nper))
perlen[0] = 1.0
perlen[1] = 0.33
steady = [True]

for n in range(nper-1):   
    steady.append(False)


dis = ModflowDis(mf,nlay=nlay,nrow=nrow,ncol=ncol,nper=nper,delr=delr,delc=delc,laycbd=0,\
            top=top,botm=botm,perlen=perlen,nstp=nstp,steady=steady)
ibound = np.ones((nrow,ncol),dtype=np.int32)

#--set ghbs is col 1
ghb_lrchc = []
ghb_conc = []

#--set ghbs along the right side
for r in range(nrow):
    for l in range(nlay):
        ghb_lrchc.append(np.array([l+1,r+1,ncol,0.0,1000.0]))
        ghb_conc.append(1.0)     
ghb_lrchc = [ghb_lrchc]      
init_heads = np.zeros((nrow,ncol)) + 0.0
init_conc = np.zeros_like(init_heads)
init_conc[:,-1] = 1.0
bas = ModflowBas(mf,ibound=ibound,strt=init_heads)

hk = 200
lpf = ModflowLpf(mf,hk=hk,vka=hk,laytyp=1)
gmg = ModflowGmg(mf,mxiter=1000,hclose=1e-2,rclose=1e-2)
oc = ModflowOc(mf,words=['head','budget'],save_head_every=1)
ghb = ModflowGhb(mf,layer_row_column_head_cond=ghb_lrchc)

#--well
sp1_q = 4.5
sp2_q = 0.0
sp3_q = 0.0
lrcq_1 = []
well_conc = []
#sp1
sp1_flux = sp1_q/(nlay)
for l in range(nlay):
    lrcq_1.append([l+1,1,1,sp1_flux])    
    well_conc.append(0.0)
#sp2
lrcq_2 = []
sp2_flux = sp2_q/nlay
for l in range(nlay):
    lrcq_2.append([l+1,1,1,sp2_flux])

lrcq = [lrcq_1,lrcq_2]    
well = ModflowWel(mf,layer_row_column_Q=lrcq)

 
#--MT3DMS 
mt = Mt3dms(modelname,namefile_ext='nam_mt3dms',modflowmodel=mf,external_path=ext_path,load=False)
#setattr(mt,'free_format',False)
adv = Mt3dAdv(mt, mixelm = -1)

btn = Mt3dBtn(mt,prsity=0.35,icbund=ibound,sconc=[init_conc],ncomp=1,ifmtcn=-1,chkmas=False,nprs=nper,dt0=0.0025,timprs=np.cumsum(perlen),ttsmult=1.0)
dsp = Mt3dDsp(mt,al=0.,trpt=1.,trpv=1.,dmcoef=0.1)
gcg = Mt3dGcg(mt,mxiter=250,isolve=3,cclose=1e-7)
ssm = Mt3dSsm(mt,cghb=[ghb_conc],cwel=well_conc)

mt.write_input()
mf.write_input()

#--SEAWAT
swt = Seawat(modelname, namefile_ext='nam_swt', modflowmodel=mf, mt3dmsmodel=mt) # Coupled to modflow model mf and mt3dms model mt
vdf = SeawatVdf(swt, iwtable = 0, densemin = 0, densemax = 0, denseref = 1000.0, denseslp = 24.5, firstdt = 1e-3)
swt.write_input()


#--finally...run SEAWAT
os.system('swt_v4x64.exe '+modelname+'.nam_swt')

