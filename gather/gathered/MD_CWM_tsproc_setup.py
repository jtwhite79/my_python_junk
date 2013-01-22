import copy
import os
from datetime import datetime,timedelta
import pandas

import tsprocClass as tc  
import pestUtil as pu 

#--since Joe is so pro-America...
tc.DATE_FMT = '%m/%d/%Y'

#--build a list of template and model-equivalent files
tpl_dir = 'tpl\\'
modin_dir = 'par\\'
tpl_files,modin_files = [],[]
files = os.listdir(modin_dir)
for file in files:
    modin_files.append(modin_dir+file)
    tpl_files.append(tpl_dir+file.split('.')[0]+'.tpl')
modin_files.append('UMD.01\\SWRREF\\SWR_Dataset11.ref')
tpl_files.append('tpl\\SWR_Dataset11.tpl')

#--start and end
start = datetime(1997,1,1,hour=12)
end = datetime(2010,12,31,hour=12)
start_str = start.strftime(tc.DATE_FMT)
end_str = end.strftime(tc.DATE_FMT)

date_dir = 'date_files\\'

#--instance
tsproc_infile = 'tsproc_setup.dat'
tsp = tc.tsproc(tsproc_infile,out_file='processed.dat',out_fmt='long')

hobs_file = 'UMD.01\\obsref\\head\\heads.smp'
hobs_smp = pu.smp(hobs_file,date_fmt = tc.DATE_FMT,load=True)
hobs_start,hobs_end = hobs_smp.get_daterange(site_name='all',startmin=start,endmax=end)

mobs_file = 'UMD.01\\modref\\head\\mheads.smp'
mobs_smp = pu.smp(mobs_file,date_fmt = tc.DATE_FMT,load=True)

site_names = hobs_smp.records.keys()

#--generate base names for processing
obs_names = []
mod_names = []
for i,s in enumerate(site_names):
    obs_names.append('ogw_{0:03.0f}or'.format(i+1))
    mod_names.append('mgw_{0:03.0f}or'.format(i+1))
    
#--write the load series block
oblocks = tsp.get_mul_series_ssf(site_names,hobs_file,block_operation='load_heads',context=tc.PEST_CONTEXT,series_list=obs_names)   
mblocks = tsp.get_mul_series_ssf(site_names,mobs_file,block_operation='load_heads',series_list=mod_names)   

pest_oblocks,pest_mblocks = [],[]

#--process each head record individually because of the variable record length

for i,[site_name,oblock,mblock] in enumerate(zip(site_names,oblocks,mblocks)):        
        oblock = [oblock]
        mblock = [mblock]
        
        #--get the starting and end date of each record within the reduced model sim time
        rstart,rend = hobs_start[site_name],hobs_end[site_name]        
        if rend > start:                                                 
            #--find the date range for this record and write date files
            dstart,dend = max(start,rstart),min(end,rend)
            print site_name,dstart,dend
            week_file = date_dir+site_name+'_wk.dat'
            full_file = date_dir+site_name+'.dat'
            dry_file = date_dir+site_name+'_dry.dat'
            #tc.write_date_file(week_file,dstart+timedelta(days=7),dend-timedelta(days=7),timedelta(days=7))
            tc.write_date_file(full_file,dstart,dend,None)                                            
            
            
            uniform_days = tsp.new_series_uniform([oblock[0].name],dstart+timedelta(days=7),dend)
            biweekly_days = tsp.new_series_uniform([oblock[0].name],dstart+timedelta(days=14),dend,interval=14,suffix='ub')
            #weekly_block = tsp.series_avg(relative_block,week_file,context=tc.PEST_CONTEXT)                            

            #--observation block            
            reduced_block = tsp.reduce_time(oblock,dstart,end_dt=dend,context=tc.PEST_CONTEXT)            
            relative_block = tsp.drawdown(reduced_block,full_file,first=True,context=tc.PEST_CONTEXT)  
            interp_block = tsp.new_time_base(relative_block,uniform_days,context=tc.PEST_CONTEXT)     
            filter_block = tsp.baseflow_filter(interp_block,context=tc.PEST_CONTEXT)
            diff_block = tsp.difference_2_series(interp_block,filter_block,context=tc.PEST_CONTEXT)
            bi_block = tsp.new_time_base(diff_block,biweekly_days,context=tc.PEST_CONTEXT,suffix='bi')                           
                        
            
            #--copy the final processed block to have the same name as the original
            renamed_block = tsp.copy_2_series(bi_block,[site_name+'_o'],role='final',wght=100.0,context=tc.PEST_CONTEXT)
            pest_oblocks.extend(renamed_block)            
            
            #--model simulated block            
            reduced_block = tsp.reduce_time(mblock,dstart,end_dt=dend)            
            relative_block = tsp.drawdown(reduced_block,full_file,first=True)  
            interp_block = tsp.new_time_base(relative_block,uniform_days)     
            filter_block = tsp.baseflow_filter(interp_block)
            diff_block = tsp.difference_2_series(interp_block,filter_block)
            bi_block = tsp.new_time_base(diff_block,biweekly_days,suffix='bi')

            #--copy the final processed block to have the same name as the original
            renamed_block = tsp.copy_2_series(bi_block,[site_name],role='final',wght=100.0)
            pest_mblocks.extend(renamed_block)           

        else:
            print 'no data for record in reduced sim time:',site_name           
        #if i > 100:
            #break

                                
#--SWR stage processing - using the flows file            
#reachgroups = [1]

#swr_fls_file = 'UMD.01\\Results\\md.fls'

#stage_blocks = tsp.get_mul_series_swr(reachgroups,'stage',swr_fls_file,mod_start,role='final')
#reduced_blocks = tsp.reduce_time(stage_blocks,start)#,end_dt=end)                  


tsp.write_pest(tpl_files,modin_files,pest_oblocks,pest_mblocks,svd=True,parms='pst_components\\params.dat',parm_grp='pst_components\\param_groups.dat')

tsp.write_tsproc()
os.system('tsproc.exe <tsproc_setup.in >tsproc_screen.out')
os.system('addreg1.exe pest.pst umd01.pst')
