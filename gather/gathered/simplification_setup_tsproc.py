import os
import sys
from datetime import datetime,timedelta
import numpy as np
import tsprocClass as tc
import pestUtil as pu
from simple import grid
tc.DATE_FMT = '%d/%m/%Y'

#--build a list of template and model-equivalent files
tpl_dir = 'tpl\\'
modin_dir = 'par\\'
tpl_files,modin_files = [],[]
files = os.listdir(modin_dir)
for file in files:
    modin_files.append(modin_dir+file)
    tpl_files.append(tpl_dir+file.split('.')[0]+'.tpl')

#--build a single parameter and group file
par_dir = 'pst_components\\'
if os.path.exists(par_dir+'pars_all.dat'):
    os.remove(par_dir+'pars_all.dat')
if os.path.exists(par_dir+'grps_all.dat'):
    os.remove(par_dir+'grps_all.dat')
files = os.listdir(par_dir)

par_files,grp_files = [],[]
for file in files:
    if 'par' in file.lower():
        par_files.append(file)
    elif 'grp' in file.lower():
        grp_files.append(file)
    else:
        raise Exception('file not recognized as parameter or group: '+str(file))

f = open(par_dir+'pars_all.dat','w',0)
for file in par_files:
    f_in = open(par_dir+file,'r')
    for line in f_in:
        f.write(line)
    f_in.close()
f.close()


f = open(par_dir+'grps_all.dat','w',0)
for file in grp_files:
    f_in = open(par_dir+file,'r')
    for line in f_in:
        f.write(line)
    f_in.close()
f.close()


model_start = grid.start
obs_start = grid.start + timedelta(days=14)
obs_end = grid.sp_end[-2]
pred_start = grid.sp_end[-2]
pred_end = grid.end

date_dir = 'date_files\\'
tsproc_infile = 'tsproc_setup.dat'
tsp = tc.tsproc(tsproc_infile,out_file='processed.dat',out_fmt='long')

pest_oblocks,pest_mblocks = [],[]
hobs_file = '_misc\\heads.smp'
hobs_smp = pu.smp(hobs_file,date_fmt=tc.DATE_FMT,load=True)

mobs_file = 'mheads.smp'
mobs_smp = pu.smp(mobs_file,date_fmt=tc.DATE_FMT,load=True)

full_file = date_dir+'full_range.dat'
tc.write_date_file(full_file,obs_start,obs_end,None)                                            

pred_file = date_dir+'pred_range.dat'
tc.write_date_file(pred_file,pred_start,pred_end,None)                                            


#--swr - for prediction
ost_names = ['obf_1']
mst_names = ['mbf_1']
rgp_nums = [1]

mblocks = tsp.get_mul_series_swr(rgp_nums,'qbflow','_model\\simple.fls',grid.start,series_name_list=mst_names)
oblocks = tsp.get_mul_series_swr(rgp_nums,'qbflow','_model\\simple.fls',grid.start,context=tc.PEST_CONTEXT,series_name_list=ost_names)
obf_blocks = tsp.copy_2_series(oblocks,['obf'],role='final',wght=0.0,context=tc.PEST_CONTEXT)
mbf_blocks = tsp.copy_2_series(mblocks,['mbf'],role='final',wght=0.0)
pest_oblocks.extend(obf_blocks)
pest_mblocks.extend(mbf_blocks)


site_names = hobs_smp.records.keys()
oblocks = tsp.get_mul_series_ssf(site_names,hobs_file,block_operation='load_heads',context=tc.PEST_CONTEXT)   
mblocks = tsp.get_mul_series_ssf(site_names,mobs_file,block_operation='load_heads',prefix='m')   

biweekly_days = tsp.new_series_uniform(['biweekly'],obs_start+timedelta(days=14),obs_end,interval=14,suffix='ub')
            
#--obs - cal period
reduced_blocks = tsp.reduce_time(oblocks,obs_start,end_dt=obs_end,context=tc.PEST_CONTEXT,role='final',wght=100.0)                        
relative_blocks = tsp.drawdown(reduced_blocks,full_file,first=True,context=tc.PEST_CONTEXT,role='final',wght=100.0)  
#interp_blocks = tsp.new_time_base(relative_blocks,uniform_days,context=tc.PEST_CONTEXT)     
filter_blocks = tsp.baseflow_filter(relative_blocks,context=tc.PEST_CONTEXT)
diff_blocks = tsp.difference_2_series(relative_blocks,filter_blocks,context=tc.PEST_CONTEXT)
bi_blocks = tsp.new_time_base(diff_blocks,biweekly_days,context=tc.PEST_CONTEXT,suffix='bi',role='final',wght=100.0)                           
pest_oblocks.extend(reduced_blocks)
pest_oblocks.extend(relative_blocks)
pest_oblocks.extend(bi_blocks)
            
#--simulated - cal period
reduced_blocks = tsp.reduce_time(mblocks,obs_start,end_dt=obs_end+timedelta(seconds=1),role='final',wght=100.0)                        
relative_blocks = tsp.drawdown(reduced_blocks,full_file,first=True,role='final',wght=100.0)  
#interp_blocks = tsp.new_time_base(relative_blocks,uniform_days)     
filter_blocks = tsp.baseflow_filter(relative_blocks)
diff_blocks = tsp.difference_2_series(relative_blocks,filter_blocks)
bi_blocks = tsp.new_time_base(diff_blocks,biweekly_days,suffix='bi',role='final',wght=100.0)                           
pest_mblocks.extend(reduced_blocks)
pest_mblocks.extend(relative_blocks)
pest_mblocks.extend(bi_blocks)

#--obs - pred 
reduced_blocks = tsp.reduce_time(oblocks,pred_start,end_dt=pred_end,context=tc.PEST_CONTEXT,role='final',wght=0.0,suffix='pd')                        
pest_oblocks.extend(reduced_blocks)

#--simulated - pred
reduced_blocks = tsp.reduce_time(mblocks,pred_start,end_dt=pred_end,role='final',wght=0.0,suffix='p')                        
pest_mblocks.extend(reduced_blocks)



#--reset the weight for locs 5 and 6 to zero

tsp.set_context('model_run')
tsp.tsproc_file = 'tsproc_model_run.dat'
tsp.write_tsproc()

f = open('tsproc_setup.in','w',0)
f.write('tsproc_setup.dat\n,tsproc_setup.out\ny\ny\n')
f.close()

f = open('tsproc_model_run.in','w',0)
f.write('tsproc_model_run.dat\n,tsproc_model_run.out\n')
f.close()

#--write the setup tsproc file
tsp.write_pest(tpl_files,modin_files,pest_oblocks,pest_mblocks,svd=True,parms='pst_components\\pars_all.dat',parm_grp='pst_components\\grps_all.dat')
tsp.set_context(tc.PEST_CONTEXT)
tsp.tsproc_file = 'tsproc_setup.dat'

tsp.write_tsproc()
os.system('tsproc.exe <tsproc_setup.in >tsproc_screen.out')

#os.system('tsproc.exe <tsproc_model_run.in')
