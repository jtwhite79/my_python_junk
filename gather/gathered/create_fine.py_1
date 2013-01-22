import os
import sys
import re
import shutil
import numpy as np
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile

import fine_config



def write_borecoords(modelname,obs_locs_file,delz):
    f = open(obs_locs_file,'r')
    typ = obs_locs_file.split('.')[0].split('_')[-1]
    f_out = open('bore_coords_'+modelname+'_'+typ+'.dat','w')
    for line in f:
        raw = line.strip().split()
        depth = float(raw[-1])
        lay = -1 * int(depth/delz)
        print depth,lay
        raw[-1] = '0.5'
        raw.append(str(lay))
        f_out.write('  '.join(raw)+'\n')
    f.close()
    f_out.close()        

def update_preddist(delc):
    files = ['pred_dist_one.in','pred_dist_ten.in','pred_dist_half.in']
    for fi in files:
        f = open(fi,'r')
        f_out = open(fi.split('.')[0]+'_'+modelname+'.in','w')
        f_out.write(f.readline())
        f_out.write(str(delc)+'\n')
        f.readline()
        f_out.write(f.readline())
        f_out.write(f.readline())
            


def mod_lpf_4_xsec(fname,hk_unit,vk_unit):
    r_hk = re.compile('hk',re.IGNORECASE)
    r_vk = re.compile('vk',re.IGNORECASE)
    f = open(fname,'r')
    f_out = open('temp.lpf','w')
    for line in f:
        if r_hk.search(line) != None:
            raw = line.strip().split()
            raw[0] = 'EXTERNAL  '
            raw[1] = str(hk_unit).ljust(31)
            raw[3] = '  (FREE)'
            raw[4] = ' 1'
            line = ' '.join(raw)
        elif r_vk.search(line) != None:
            raw = line.strip().split()
            raw[0] = 'EXTERNAL  '
            raw[1] = str(vk_unit).ljust(31)
            raw[3] = '  (FREE)'
            raw[4] = ' 1'
            line = ' '.join(raw)
        f_out.write(line.strip()+'\n')
    f.close()
    f_out.close()        
    shutil.copy('temp.lpf',fname)



real_num = 1
hk_unit = 150
vk_unit = 151
modelname = 'henry_fine'
ext_path = 'ref_fine\\'
mf = modflow(modelname,external_path=ext_path,load=False)


x_len = fine_config.x_len     
z_len = fine_config.z_len     
nrow = fine_config.nrow
ncol = fine_config.ncol
nlay = fine_config.nlay
delr = x_len/ncol
delc =1.0
delz = z_len/nlay
print delr,delz
top = 0.0
botm = np.cumsum(np.zeros(nlay) - delz)
botm -= top

write_borecoords(modelname,'obs_locs_plot_conc.dat',delz)
write_borecoords(modelname,'obs_locs_plot_head.dat',delz)
update_preddist(delc)


nstp = 1
nper = 2
perlen = np.zeros((nper))
perlen[0] = 1.0
perlen[1] = 0.33
steady = [True]

for n in range(nper-1):   
    steady.append(False)


#--write grid.spc for xsection
f = open('grid_'+modelname+'.spc','w')
f.write('{0:6d} {1:6d}\n'.format(nlay,ncol))
f.write('0.0 0.0 0.0\n')
f.write(str(ncol)+'*'+str(delr)+'\n')
f.write(str(nlay)+'*'+str(delz)+'\n')
f.close()

#--write grid.spc for actual
f = open('grid_'+modelname+'_actual.spc','w')
f.write('{0:6d} {1:6d}\n'.format(nrow,ncol))
f.write('0.0 1.0 0.0\n')
f.write(str(ncol)+'*'+str(delr)+'\n')
f.write(str(nrow)+'* 1.0\n')
f.close()



#--write zone array
np.savetxt('zone_'+modelname+'.ref',np.ones((nlay,ncol)),fmt='%4d')


dis = mfdis(mf,nrow,ncol,nlay,nper=nper,delr=delr,delc=delc,laycbd=0,\
            top=top,botm=botm,perlen=perlen,nstp=nstp,steady=steady)
ibound = np.ones((nrow,ncol),dtype=np.int32)

#ibound[:,ncol-1] = -1
#ibound[:,0] = -1

#--set ghbs is col 1
ghb_lrchc = []
ghb_conc = []

#--set ghbs along the right side
for r in range(nrow):
    for l in range(nlay):
        ghb_lrchc.append(np.array([l+1,r+1,ncol,0.0,1000.0]))
        ghb_conc.append(1.0)     
ghb_lrchc = [ghb_lrchc]      
               
#--existing external initial heads and concentrations - not loaded into flopy
init_heads = []
init_conc = []
for l in range(nlay):
     init_heads.append(ext_path+'init_heads_'+str(l+1)+'.ref')
     ic_name = ext_path+'init_conc_'+str(l+1)+'.ref'
     init_conc.append(ic_name)
#init_heads = np.zeros((nrow,ncol)) + 0.0
#init_conc = np.zeros_like(init_heads)
#init_conc[:,-1] = 1.0
bas = mfbas(mf,ibound,init_heads)

#hk = []
#for l in range(nlay):
#    hk.append('ref\\hk_'+str(l+1)+'_1.ref')
hk = 200
lpf = mflpf(mf,hk=hk,vka=hk,laytyp=1)
gmg = mfgmg(mf,mxiter=1000,hclose=1e-2,rclose=1e-2)
oc = mfoc(mf,words=['head','budget'],save_head_every=1)
ghb = mfghb(mf,layer_row_column_head_cond=ghb_lrchc)

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
#sp2
lrcq_3 = []
sp3_flux = sp3_q/nlay
for l in range(nlay):
    lrcq_3.append([l+1,1,1,sp3_flux])

lrcq = [lrcq_1,lrcq_2,lrcq_3]    
well = mfwel(mf,layer_row_column_Q=lrcq)


#np.savetxt(ext_path+'hk.ref',np.zeros((nlay,ncol))+hk,fmt='%15.6g')
#np.savetxt(ext_path+'vk.ref',np.zeros((nlay,ncol))+hk,fmt='%15.6g')
mf.add_external(ext_path+'hk.ref',hk_unit)
mf.add_external(ext_path+'vk.ref',vk_unit)
 
 
 
#--MT3DMS 
mt = mt = mt3dms(modelname, 'nam_mt3dms', mf,external_path=ext_path,load=False)
adv = mtadv(mt, mixelm = 0)

btn = mtbtn(mt,prsity=0.35,icbund=ibound,sconc=[init_conc],ifmtcn=-1,chkmas=False,nprs=nper,dt0=0.0025,timprs=np.cumsum(perlen),ttsmult=1.0)
dsp = mtdsp(mt,al=0.,trpt=1.,trpv=1.,dmcoef=0.1)
gcg = mtgcg(mt,mxiter=250,isolve=3,cclose=1e-7)
ssm = mtssm(mt,cghb=[ghb_conc],cwel=well_conc)

mt.write_input()

#-- and rewrite modflow input
mf.write_input()

#--SEAWAT
mswt = mswt(modelname, 'nam_swt', mf, mt) # Coupled to modflow model mf and mt3dms model mt
vdf = mswtvdf(mswt, iwtable = 0, densemin = 0, densemax = 0, denseref = 1000.0, denseslp = 24.5, firstdt = 1e-3)
mswt.write_input()

#--mod lpf file for xsection 
mod_lpf_4_xsec(modelname+'.lpf',hk_unit,vk_unit)

#--finally...run SEAWAT
os.system('swt_v4x64.exe '+modelname+'.nam_swt')

