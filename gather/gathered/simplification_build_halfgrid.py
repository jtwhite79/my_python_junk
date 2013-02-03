import numpy as np
import shutil
from simple import grid
from flopy2.modflow import *

import simplification_sample_arrays as sa
import simplification_sample_bcs as sbc


f = open('..\\_misc\\simple_rc.grd','w',0)
f.write('{0:10d} {1:10d}\n'.format(grid.nrow/grid.sample_stride,grid.ncol/grid.sample_stride))
f.write('{0:15.5G} {1:15.5G} 0.0\n'.format(grid.xmin,grid.cols[-1]))
for j in range(grid.ncol/grid.sample_stride):
    f.write(' {0:10.3f}'.format(grid.delr[0]*grid.sample_stride))
f.write('\n')
for i in range(grid.nrow/grid.sample_stride):
    f.write(' {0:10.3f}'.format(grid.delc[0]*grid.sample_stride))
f.write('\n')
f.close()

#sa.sample()
modelname = grid.modelname+'_rc'
exe = 'MD_mfnwt_x64.exe'
ext_path = 'ref_rc\\mod\\'

f = open('simple_rech_series.dat','r')
for i,line in enumerate(f):
    rech = float(line.strip())
    arr = np.zeros((grid.nrow/grid.sample_stride,grid.ncol/grid.sample_stride),dtype=np.float32) + rech
    aname = 'ref_rc\\mod\\rech_'+str(i+1)+'.ref'
    arr.tofile(aname)    

prop_dict = {}
for pname in grid.prop_names:
    pvalues = []
    for lkey in grid.lay_key:
        name ='ref_rc\\'+lkey+'_'+pname+'.ref'
        #pvalues.append(grid.hydro_dict[lkey][pname])
        pvalues.append(name)
    prop_dict[pname] = pvalues

ml = Modflow(modelname=modelname,exe_name=exe,external_path=ext_path)
setattr(ml,'use_existing',True)

f = open(ext_path+'delc.ref','w',0)
for i in range(grid.nrow/grid.sample_stride):
    f.write('{0:15.6f}'.format(grid.delc[0]*grid.sample_stride))
f.write('\n')
f.close()

f = open(ext_path+'delr.ref','w',0)
for i in range(grid.ncol/grid.sample_stride):
    f.write('{0:15.6f}'.format(grid.delr[0]*grid.sample_stride))
f.write('\n')
f.close()

botm = []
for k in range(grid.nlay):
    botm.append(ext_path+'botm_Layer_'+str(k+1)+'.ref')

perlen = []
for i in range(1,len(grid.sp_start)):
    perlen.append((grid.sp_end[i]-grid.sp_start[i]).days)
perlen[-1]
dis = ModflowDis(ml,grid.nlay,grid.nrow/grid.sample_stride,grid.ncol/grid.sample_stride,delr=grid.delr[0]*grid.sample_stride,delc=grid.delc[0]*grid.sample_stride,\
    top='ref_rc\\top.ref',botm=botm,laycbd=0,perlen=perlen,nper=len(perlen),steady=False)
strt = []
for k in range(grid.nlay):
    strt.append('ref_rc\\strt_'+str(k+1)+'.ref')
ibound = []
for name in grid.ibound_names:
    ibound.append('ref_rc\\'+name.split('\\')[1])
bas = ModflowBas(ml,ibound=ibound,strt=strt)

f_in = open(grid.modelname+'.rch','r')
f_out = open(modelname+'.rch','w',0)
for line in f_in:
    line = line.replace('ref\\mod','ref_rc\\mod')
    f_out.write(line)
f_in.close()
f_out.close()
mfaddoutsidefile(ml,'RCH','rch',19)

lpf = ModflowLpf(ml,laytyp=0,hk=prop_dict['k'],vka=prop_dict['k'])
oc = ModflowOc(ml,words=['head'],save_head_every=1)
gmg = ModflowGmg(ml,hclose=0.35,rclose=5.0)

mfaddoutsidefile(ml,'WEL','wel',30)
mfaddoutsidefile(ml,'GHB','ghb',31)
mfaddoutsidefile(ml,'SWR','swr',32)

ml.add_external(modelname+'.fls',101,True)
ml.add_external(modelname+'.stg',102,False)
ml.add_external(modelname+'.bfl',103,False)
ml.add_external(modelname+'.str',105,False)


ml.write_input()

ml.run_model2(pause=False)
plot.plot_rc()

#os.system(exe+' '+modelname+'.nam')




