import sys
import os
import numpy as np
import pandas

from simple import grid
from flopy2.modflow import *

import simplification_prep_bc as prep
import simplification_apply_bc_factors as apply

import simplification_plot_results as plot
import simplification_build_modpath as mpath


#print grid.sp_start[-1],grid.sp_end[-1]
#os.chdir('..\\')
#prep.prep()
#apply.apply()
#os.chdir('_model\\')

modelname = grid.modelname
exe = 'MD_mfnwt_x64.exe'

#--external dir
ext_path = 'ref\\mod\\'
if not os.path.exists(ext_path):
    os.mkdir(ext_path)


print 'writing hydro_strat properties as ext arrays and building property name arrays'
for hname,prop_dict in grid.hydro_dict.iteritems():
    for pname,pval in prop_dict.iteritems():
        aname = 'ref\\'+hname+'_'+pname+'.ref'
        arr = np.zeros((grid.nrow,grid.ncol)) + pval
        np.savetxt(aname,arr,fmt='%15.4E')
prop_dict = {}
for pname in grid.prop_names:
    pvalues = []
    for lkey in grid.lay_key:
        name ='ref\\'+lkey+'_'+pname+'.ref'
        #pvalues.append(grid.hydro_dict[lkey][pname])
        pvalues.append(name)
    prop_dict[pname] = pvalues



ml = Modflow(modelname=modelname,exe_name=exe,external_path=ext_path)
setattr(ml,'use_existing',False)


thk = (grid.top - grid.bot) / grid.nlay
bot = [grid.top - thk]
for hydro_name in grid.hydro_dict.keys():
    np.savetxt('ref\\'+hydro_name+'_thk_frac.ref',thk,fmt=' %15.6E')
for i in range(1,grid.nlay):
    bot.append(bot[i-1] - thk)
perlen = []
for i in range(1,len(grid.sp_start)):
    perlen.append((grid.sp_end[i]-grid.sp_start[i]).days)
perlen[-1]
dis = ModflowDis(ml,grid.nlay,grid.nrow,grid.ncol,delr=grid.delr,delc=grid.delc,\
    top='ref\\top.ref',botm=bot,laycbd=0,perlen=perlen,nper=len(perlen),steady=False)
strt = []
for k in range(grid.nlay):
    strt.append('ref\\strt_'+str(k+1)+'.ref')
bas = ModflowBas(ml,ibound=grid.ibound_names,strt=strt)

#--only create once, otherwise, have to re-sample rech arrays - costly
rech = [0.00005]
beta = 0.5 
for i in range(1,len(perlen)):
    innov = np.random.normal(0.0,rech[0]*0.1)
    val = rech[-1] + (beta * innov)
    if val < 0.0:
        val = 0.0
    rech.append(val) 
rech[-1] = min(rech)
f = open('simple_rech_series.dat','w')
for r in rech:
    f.write('{0:15.6G}\n'.format(r))
f.close()
rch = ModflowRch(ml,rech=rech,bin=True)

lpf = ModflowLpf(ml,laytyp=0,hk=prop_dict['k'],vka=prop_dict['k'])
#upw = ModflowUpw(ml,laytyp=0,hk=prop_dict['k'],vka=prop_dict['k'])
oc = ModflowOc(ml,words=['head','budget'],save_head_every=1)
gmg = ModflowGmg(ml,hclose=0.35,rclose=5.0)
#nwt = ModflowNwt(ml,headtol=0.25,fluxtol=5.0)

#mfaddoutsidefile(ml,'RCH','rch',19)
mfaddoutsidefile(ml,'WEL','wel',30)
mfaddoutsidefile(ml,'GHB','ghb',31)
mfaddoutsidefile(ml,'SWR','swr',32)

ml.add_external(modelname+'.fls',101,True)
ml.add_external(modelname+'.stg',102,False)
ml.add_external(modelname+'.bfl',103,False)
ml.add_external(modelname+'.str',105,False)

dis.nper = 1
ml.write_input()
#mpath.build(ml)



ml.run_model2(pause=False)
#plot.plot()

#os.system(exe+' '+modelname+'.nam')




