import os
import numpy as np
from datetime import datetime
import shutil

import shapefile
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile
from bro import flow




#--copy xsecs from _swr folder
xsec_src = '..\\..\\_swr\\xsec_navd'
xsec_dest = 'xsec_navd\\'
if os.path.exists(xsec_dest):
    shutil.rmtree(xsec_dest)
#xsec_files = os.listdir(xsec_src)
#for xfile in xsec_files:
shutil.copytree(xsec_src,xsec_dest)

#--copy layering files from _layering folder
lay_src = '..\\..\\_layering\\ref_new\\'
lay_dest = flow.ref_dir
lay_files = os.listdir(lay_src)
for lfile in lay_files:
    shutil.copy(lay_src+lfile,lay_dest+lfile)

strt = [flow.ref_dir+'strt_L1.ref'] * flow.nlay
ibound = [flow.ref_dir+'ibound_CS.ref'] * flow.nlay
botm = []
for l in flow.layer_botm_names:
    botm.append(flow.ref_dir+l+'_bot.ref')
#botm = ['ref\\T1_bot.ref']

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
lpf = mflpf(mf,laytyp=0,hk=4500.0,vka=4500.0)
gmg = mfgmg(mf,mxiter=100,hclose=0.25,rclose=1000.0)

oc = mfoc(mf,words=['head','budget'],save_head_every=1)

#--externally generated...
ghb = mfaddoutsidefile(mf,'GHB','ghb',125)
ets = mfaddoutsidefile(mf,'ETS','ets',126)
rch = mfaddoutsidefile(mf,'RCH','rch',127)
#mnw = mfaddoutsidefile(mf,'MNW2','mnw',128)
wel = mfaddoutsidefile(mf,'WEL','wel',128)

#--swi
swi = mfaddoutsidefile(mf,'SWI','swi',129)
mf.add_external(modelname+'.zta',130,binflag=True)


#--swr
swr = mfaddoutsidefile(mf,'SWR','swr',106)
mf.add_external(modelname+'.fls',101,binflag=True)
mf.add_external(modelname+'.stg',102,binflag=True)
mf.add_external(modelname+'.aqx',103,binflag=True)
mf.add_external(modelname+'.pqm',104,binflag=True)
mf.add_external(modelname+'.riv',107)

mf.write_input()
os.system('mfnwt-SWR_x64.exe '+modelname+'.nam')


