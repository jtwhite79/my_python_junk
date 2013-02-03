import sys
import os
import shutil
import numpy as np
import pandas

from simple import grid
from flopy2.modflow import *

modelname = grid.modelname+'_l'
exe = 'MD_mfnwt_x64.exe'

f_in = open('..\\_misc\\bore_coords.dat','r')
f_out = open('..\\_misc\\bore_coords_l.dat','w',0)
for line in f_in:
    layer = int(line.strip()[-1])
    layer = int(np.ceil(layer/float(grid.sample_stride)))
    line = line.strip()[:-1] + str(layer) + '\n'
    f_out.write(line)
f_in.close()
f_out.close()


#--external dir
ext_path = 'ref_l\\mod\\'
if not os.path.exists(ext_path):
    os.mkdir(ext_path)

ml = Modflow(modelname=modelname,exe_name=exe,external_path=ext_path)
setattr(ml,'use_existing',False)


bot = []
for k in range(0,grid.nlay,grid.sample_stride):
    bot.append('ref\\mod\\botm_Layer_'+str(k+1)+'.ref')
perlen = []
for i in range(1,len(grid.sp_start)):
    perlen.append((grid.sp_end[i]-grid.sp_start[i]).days)
perlen[-1]
dis = ModflowDis(ml,grid.nlay/grid.sample_stride,grid.nrow,grid.ncol,delr=grid.delr,delc=grid.delc,\
    top='ref\\top.ref',botm=bot,laycbd=0,perlen=perlen,nper=len(perlen),steady=False)
strt,ibound = [],[]
for k in range(0,grid.nlay,grid.sample_stride):
    strt.append('ref\\strt_'+str(k+1)+'.ref')
    ibound.append('ref\\ibound_'+str(k+1)+'.ref')
bas = ModflowBas(ml,ibound=ibound,strt=strt)

prop_dict = {}
for pname in grid.prop_names:
    pvalues = []
    for lkey in grid.lay_key[::grid.sample_stride]:
        name ='ref\\'+lkey+'_'+pname+'.ref'
        #pvalues.append(grid.hydro_dict[lkey][pname])
        pvalues.append(name)
    prop_dict[pname] = pvalues



lpf = ModflowLpf(ml,laytyp=0,hk=prop_dict['k'],vka=prop_dict['k'])
#upw = ModflowUpw(ml,laytyp=0,hk=prop_dict['k'],vka=prop_dict['k'])
oc = ModflowOc(ml,words=['head'],save_head_every=1)
gmg = ModflowGmg(ml,hclose=0.35,rclose=5.0)
#nwt = ModflowNwt(ml,headtol=0.25,fluxtol=5.0)
shutil.copy(grid.modelname+'.rch',modelname+'.rch')
mfaddoutsidefile(ml,'RCH','rch',19)
mfaddoutsidefile(ml,'WEL','wel',30)
mfaddoutsidefile(ml,'GHB','ghb',31)
shutil.copy(grid.modelname+'.swr',modelname+'.swr')
mfaddoutsidefile(ml,'SWR','swr',32)

ml.add_external(modelname+'.fls',101,True)
ml.add_external(modelname+'.stg',102,False)
ml.add_external(modelname+'.bfl',103,False)
ml.add_external(modelname+'.str',105,False)


ml.write_input()




ml.run_model2(pause=False)
plot.plot()

#os.system(exe+' '+modelname+'.nam')





