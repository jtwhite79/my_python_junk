import os
import numpy as np
from datetime import datetime
import shutil

import shapefile
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile
from bro_pred import flow


cali_ref_dir = '..\\..\\_model\\bro.03\\flowref\\mod\\'
strt,hk,ss = [],[],[]
ibound,botm = [],[]
for k in range(flow.nlay):
    strt.append(flow.ref_dir+'strt_'+str(k+1)+'.ref')
    kname = 'hk_'+str(k+1)+'_1.ref'
    sname = 'ss_'+str(k+1)+'_1.ref'
    shutil.copy(cali_ref_dir+kname,flow.ref_dir+kname)
    hk.append(flow.ref_dir+kname)
    shutil.copy(cali_ref_dir+sname,flow.ref_dir+sname)
    ss.append(flow.ref_dir+sname)
    bname = 'botm_'+str(k+1)+'.ref'
    shutil.copy(cali_ref_dir+bname,flow.ref_dir+bname)
    botm.append(flow.ref_dir+bname)
    ibname = 'ibound_'+str(k+1)+'.ref'
    shutil.copy(cali_ref_dir+ibname,flow.ref_dir+ibname)
    ibound.append(flow.ref_dir+ibname)

top = 'top_1.ref'
shutil.copy(cali_ref_dir+top,flow.ref_dir+top)

isource = 'ISOURCE_L1.ref'
shutil.copy('..\\..\\_model\\bro.03\\flowref\\'+isource,flow.ref_dir+isource)


#--copy xsecs from _swr folder
xsec_src = '..\\..\\_swr\\xsec_navd'
xsec_dest = 'xsec_navd\\'
if os.path.exists(xsec_dest):
    shutil.rmtree(xsec_dest)
#xsec_files = os.listdir(xsec_src)
#for xfile in xsec_files:
shutil.copytree(xsec_src,xsec_dest)

#--copy layering files from _layering folder
#lay_src = '..\\..\\_layering\\ref_new\\'
#lay_dest = flow.ref_dir
#lay_files = os.listdir(lay_src)
#for lfile in lay_files:
#    shutil.copy(lay_src+lfile,lay_dest+lfile)

#strt = [flow.ref_dir+'strt_L1.ref'] * flow.nlay
#ibound = [flow.ref_dir+'ibound_CS.ref'] * flow.nlay
#botm = []
#for l in flow.layer_botm_names:
#    botm.append(flow.ref_dir+l+'_bot.ref')
#botm = ['ref\\T1_bot.ref']

cali_ds_11 = '..\\..\\_model\\bro.03\\flowref\\swr\\ds_11_19500131.dat'
pred_ds_11 = flow.ref_dir+'swr\\ds_11_'+flow.sp_end[0].strftime('%Y%m%d')+'.dat'
shutil.copy(cali_ds_11,pred_ds_11)

modelname = flow.root
ext_path = flow.ref_dir+'mod\\'
if not os.path.exists(ext_path):
    os.mkdir(ext_path)
mf = modflow(modelname,external_path=ext_path)
perlen = []
nstp = [1] * flow.nper
#nstp = []
for td in flow.sp_len: 
    perlen.append(td.days)
#    nstp.append(td.days)

dis = mfdis(mf,flow.nrow,flow.ncol,flow.nlay,flow.nper,nstp=nstp,delr=500,delc=500,top=flow.ref_dir+'top_mod.ref',botm=botm,perlen=perlen,steady=False,laycbd=0)
bas = mfbas(mf,ibound=ibound,strt=strt,hnoflo=1.0e+10)
#upw = mfupw(mf,laytyp=0,hk=4500.0,vka=4500.0)
#nwt = mfnwt(mf,headtol=0.15,fluxtol=100000.0,maxiterout=500)
lpf = mflpf(mf,laytyp=0,hk=hk,vka=hk)
gmg = mfgmg(mf,mxiter=100,hclose=0.25,rclose=1000.0)

oc = mfoc(mf,words=['head','budget'],save_head_every=1)

#--externally generated...
ghb = mfaddoutsidefile(mf,'GHB','ghb',125)
ets = mfaddoutsidefile(mf,'ETS','ets',126)
rch = mfaddoutsidefile(mf,'RCH','rch',127)
#mnw = mfaddoutsidefile(mf,'MNW2','mnw',128)
wel = mfaddoutsidefile(mf,'WEL','wel',128)

#--swi
shutil.copy('..\\..\\_model\\bro.03\\flow.swi',flow.root+'.swi')
swi = mfaddoutsidefile(mf,'SWI','swi',129)
mf.add_external(modelname+'.zta',130,binflag=True)

#--add additional CBC units
mf.add_external(flow.root+'_wel.cbc',flow.well_unit,binflag=True)
mf.add_external(flow.root+'_rch.cbc',flow.rch_unit,binflag=True)
mf.add_external(flow.root+'_ets.cbc',flow.ets_unit,binflag=True)
mf.add_external(flow.root+'_ghb.cbc',flow.ghb_unit,binflag=True)



#--swr
swr = mfaddoutsidefile(mf,'SWR','swr',106)
mf.add_external(modelname+'.fls',101,binflag=True)
mf.add_external(modelname+'.stg',102,binflag=True)
mf.add_external(modelname+'.aqx',103,binflag=True)
mf.add_external(modelname+'.pqm',104,binflag=True)
mf.add_external(modelname+'.riv',107)
mf.add_external(flow.root+'_swr.cbc',flow.swr_unit,binflag=True)

mf.write_input()
os.system('mfnwt-SWR_x64.exe '+modelname+'.nam')



