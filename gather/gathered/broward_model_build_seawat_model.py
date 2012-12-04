import os
import numpy as np
from datetime import datetime
import shutil

import shapefile
from mf import *
from mt import *
from mswt import *
from mfaddoutsidefile import mfaddoutsidefile
from bro import seawat,flow


strt = [seawat.ref_dir+'strt_L1.ref'] * seawat.nlay
ibound = [seawat.ref_dir+'ibound_CS.ref'] * seawat.nlay
botm = []
for l in seawat.layer_botm_names:
    botm.append(seawat.ref_dir+l+'_bot.ref')
#botm = ['ref\\T1_bot.ref']

modelname = seawat.root
mf = modflow(modelname,external_path=seawat.ref_dir+'mod\\')
perlen = []
nstp = [1] * seawat.nper
#nstp = []
for td in seawat.sp_len: 
    perlen.append(td.days)
#    nstp.append(td.days)

dis = mfdis(mf,seawat.nrow,seawat.ncol,seawat.nlay,seawat.nper,nstp=nstp,delr=500,delc=500,top=seawat.ref_dir+'top_mod.ref',botm=botm,perlen=perlen,steady=False,laycbd=0)
bas = mfbas(mf,ibound=ibound,strt=strt,hnoflo=1.0e+10)
#upw = mfupw(mf,laytyp=0,hk=4500.0,vka=4500.0)
#nwt = mfnwt(mf,headtol=0.15,fluxtol=100000.0,maxiterout=500)
lpf = mflpf(mf,laytyp=0,hk=4500.0,vka=4500.0)
gmg = mfgmg(mf,mxiter=100,hclose=0.25,rclose=1000.0)

oc = mfoc(mf,words=['head'],save_head_every=1)

#--externally generated...
ghb = mfaddoutsidefile(mf,'GHB','ghb',125)
shutil.copy(flow.root+'.ets',seawat.root+'.ets')
ets = mfaddoutsidefile(mf,'ETS','ets',126)
shutil.copy(flow.root+'.rch',seawat.root+'.rch')
rch = mfaddoutsidefile(mf,'RCH','rch',127)
wel = mfaddoutsidefile(mf,'WEL','wel',128)

shutil.copy(flow.root+'.riv',seawat.root+'.riv')
riv = mfaddoutsidefile(mf,'RIV','riv',124)

#--mt3d
sconc = []
for lname in seawat.layer_botm_names:
    sconc.append(seawat.ref_dir+lname+'_srconc.ref')

icbund = [seawat.ibound_name] * seawat.nlay

mt = mt3dms(seawat.root,'nam_mt3d',mf,external_path=seawat.ref_dir+'mod\\')
btn = mtbtn(mt,ncomp=1,mcomp=0,tunit='DAY',lunit='FEET',munit='KG',prsity=0.2,icbund=icbund,sconc=[sconc],cinact=0.0,thkmin=1.0,\
    ifmtcn=0,ifmtnp=0,ifmtrf=0,ifmtdp=0,savucn=True,nprs=-1,chkmas=True,nprmas=1,dt=0.0,mxstrn=10000,ttsmult=1.0,ttsmax=0)
adv = mtadv(mt,mixelm=0,percel=1.0,nadvfd=0)
dsp = mtdsp(mt,al=0.0,trpt=1.0,trpv=1.0) 
gcg = mtgcg(mt,mxiter=500,iter1=50,isolve=3,ncrs=0,cclose=0.001,iprgcg=0)

ssm = mfaddoutsidefile(mt,'SSM','ssm',36)

#--seawat
swt = mswt(seawat.root,namefile_ext='nam_swt',modflowmodel=mf,mt3dmsmodel=mt)
vdf = mswtvdf(swt,mtdnconc=1,mfnadvfd=2,nswtcpl=1,iwtable=1,densemin=0,densemax=0,\
    dnscrit=0,denseref=28.3127,denseslp=0.7078,firstdt=0.001)

mf.write_input()
mt.write_input()
swt.write_input()
#os.system('mfnwt-SWR_x64.exe '+modelname+'.nam')


