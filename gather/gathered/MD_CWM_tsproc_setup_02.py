import copy
import sys
import os
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas

import tsprocClass as tc  
import pestUtil as pu 

#update parameter values and fixed/unfixed

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
modin_files.append('UMD.03\\SWRREF\\SWR_Dataset11.ref')
tpl_files.append('tpl\\SWR_Dataset11.tpl')

#--start and end
model_start = datetime(1996,1,1,hour=12)
obs_start = datetime(1997,1,1,hour=12)
#obs_end = datetime(2010,12,31,hour=12)
obs_end = datetime(year=1999,month=12,day=12,hour=12)
obs_start_str = obs_start.strftime(tc.DATE_FMT)
obs_end_str = obs_end.strftime(tc.DATE_FMT)

date_dir = 'date_files\\'

#--instance
tsproc_infile = 'tsproc_setup.dat'
tsp = tc.tsproc(tsproc_infile,out_file='processed.dat',out_fmt='long')

pest_oblocks,pest_mblocks = [],[]

#--stage sites
stg_obs_file = 'UMD.03\\obsref\\stage\\All_DBHYDRO_stage.smp'
stg_reach_file = 'setup_files\\UMD.03_StageStats.csv'
f = open(stg_reach_file,'r')
reach_dict = {}
header = f.readline()
for line in f:
    raw = line.strip().split(',')
    name = raw[0].upper().replace(' ','_').replace('-','')
    if name.endswith('W'):
        name = name[:-1]
    reach_dict[name] = int(raw[1])
f.close()

#parser = lambda x: datetime.strptime(x,tc.DATE_FMT+' %H:%M:%S')
#stage_df = pandas.read_table(stg_obs_file,header=None,parse_dates=[[1,2]],date_parser=parser,sep='\s*')
#stage_df.columns = ['datetime','site','value']

stage_smp = pu.smp(stg_obs_file,date_fmt=tc.DATE_FMT,pandas=True,load=True)
stage_sites = stage_smp.records.keys()
for site in stage_sites:
    if site not in reach_dict.keys():
        print 'site not found in reach dict',site

obs_names = []
mod_names = []
reach_numbers = []
smp_site_names = []
for i,site in enumerate(reach_dict.keys()):
    if site not in stage_sites:
        print 'site not found in smp file',site
        reach_dict.pop(site)
    else:            
        obs_names.append('ost_{0:03.0f}or'.format(i+1))    
        mod_names.append('mst_{0:03.0f}or'.format(i+1))
        reach_numbers.append(reach_dict[site])
        smp_site_names.append(site)
mblocks = tsp.get_mul_series_swr(reach_numbers,None,'UMD.03\\Results\\UMD.stg',model_start,mod_names,swr_file_type='stage')
oblocks = tsp.get_mul_series_ssf(reach_dict.keys(),stg_obs_file,context=tc.PEST_CONTEXT,series_list=obs_names)

assert len(mblocks) == len(oblocks)


#--process each head record individually because of the variable record length
for i,[site,oblock,mblock] in enumerate(zip(smp_site_names,oblocks,mblocks)):   
    oblock = [oblock]
    mblock = [mblock]
    #--get the start and end of the observed record
    ostart = stage_smp.records[site].dropna().index[0]
    oend = stage_smp.records[site].dropna().index[-1]    
    dstart,dend = max(obs_start,ostart),min(obs_end,oend)
    print site,dstart,dend
    if dend > dstart:
        full_file = date_dir+site+'_stg.dat'
        tc.write_date_file(full_file,dstart,dend,None)

        uniform_days = tsp.new_series_uniform([oblock[0].name],dstart+timedelta(days=7),dend)
        biweekly_days = tsp.new_series_uniform([oblock[0].name],dstart+timedelta(days=14),dend,interval=14,suffix='ub')
        

        #--model simulated block            
        reduced_block = tsp.reduce_time(mblock,dstart,end_dt=dend)            
        relative_block = tsp.drawdown(reduced_block,full_file,first=True)  
        interp_block = tsp.new_time_base(relative_block,uniform_days)     
        filter_block = tsp.baseflow_filter(interp_block)
        diff_block = tsp.difference_2_series(interp_block,filter_block)
        bi_block = tsp.new_time_base(diff_block,biweekly_days,suffix='bi')

        #--copy the final processed block to have the same name as the original
        #renamed_block = tsp.copy_2_series(reduced_block,[site_name+'_r'],role='final',wght=100.0)
        #pest_mblocks.extend(renamed_block)
        renamed_block = tsp.copy_2_series(bi_block,[site],role='final',wght=100.0)
        pest_mblocks.extend(renamed_block)     


        reduced_block = tsp.reduce_time(oblock,dstart,end_dt=dend,context=tc.PEST_CONTEXT)        
        relative_block = tsp.drawdown(reduced_block,full_file,first=True,context=tc.PEST_CONTEXT)  
        interp_block = tsp.new_time_base(relative_block,uniform_days,context=tc.PEST_CONTEXT)     
        filter_block = tsp.baseflow_filter(interp_block,context=tc.PEST_CONTEXT)
        diff_block = tsp.difference_2_series(interp_block,filter_block,context=tc.PEST_CONTEXT)
        bi_block = tsp.new_time_base(diff_block,biweekly_days,context=tc.PEST_CONTEXT,suffix='bi')       
    
        #--copy the final processed block to have the same name as the original
        #renamed_block = tsp.copy_2_series(reduced_block,[site_name+'_ro'],role='final',wght=100.0,context=tc.PEST_CONTEXT)
        #pest_oblocks.extend(renamed_block)
        renamed_block = tsp.copy_2_series(bi_block,[site+'_o'],role='final',wght=100.0,context=tc.PEST_CONTEXT)
        pest_oblocks.extend(renamed_block)  
    
                   

#--baseflow obs
bf_obs_file = 'UMD.03\\Results\\UMDNetFlow_observed_Monthly.smp'
bf_mod_file = 'UMD.03\\Results\\UMDNetFlow_simulated_Monthly.smp'
bf_obs_smp = pu.smp(bf_obs_file,load=True,date_fmt=tc.DATE_FMT,pandas=True)
bf_mod_smp = pu.smp(bf_mod_file,load=True,date_fmt=tc.DATE_FMT,pandas=True)

bf_obs_sites = bf_obs_smp.records.keys()
bf_mod_sites = bf_mod_smp.records.keys()
assert len(bf_obs_sites) == len(bf_mod_sites)
bf_mod_sites = []
for osite in bf_obs_sites:
    print osite
    msite = osite[:-1]+'s'
    assert msite in bf_mod_smp.records.keys()
    bf_mod_sites.append(msite)
    print bf_obs_smp.records[osite].shape,bf_mod_smp.records[osite[:-1]+'s'].shape
 

obs_names = []
mod_names = []
for i,s in enumerate(bf_obs_sites):
    obs_names.append('obf_{0:03.0f}or'.format(i+1))    
    mod_names.append('mbf_{0:03.0f}or'.format(i+1))

bf_oblocks = tsp.get_series_ssf(bf_obs_sites,bf_obs_file,block_operation='load_bf_obs',series_list=obs_names,context=tc.PEST_CONTEXT)   
bf_mblocks = tsp.get_series_ssf(bf_mod_sites,bf_mod_file,block_operation='load_bf_mod',series_list=mod_names)
  

time_str = '00:00:00'
for mblock,oblock,site in zip(bf_mblocks,bf_oblocks,bf_obs_sites):    
    #--baseflow accumulation
    date_file_name = date_dir+site+'_bf.dat'
    obs_df = bf_obs_smp.records[site].dropna()
    obs_df = obs_df[obs_start:]
    ostart,oend = obs_df.index[0],obs_df.index[-1]    
    print site,ostart,oend
    f = open(date_file_name,'w',0)
    f.write(ostart.strftime(tc.DATE_FMT)+' '+time_str+'  '+oend.strftime(tc.DATE_FMT)+' '+time_str+'\n')
    f.close()    
    vcalc_mblock = tsp.volume_calc([mblock],date_file_name)
    vcalc_oblock = tsp.volume_calc([oblock],date_file_name,context=tc.PEST_CONTEXT)
    vser_mblock = tsp.vol_2_series(vcalc_mblock)
    vser_oblock = tsp.vol_2_series(vcalc_oblock,context=tc.PEST_CONTEXT)
    renamed_mblock = tsp.copy_2_series(vser_mblock,[site[:-1]+'p'],role='final',wght=0.0)
    renamed_oblock = tsp.copy_2_series(vser_oblock,[site[:-2]+'op'],role='final',wght=0.0,context=tc.PEST_CONTEXT)    
    pest_mblocks.extend(renamed_mblock)   
    pest_oblocks.extend(renamed_oblock)   

    #--the raw baseflow series
    renamed_mblock = tsp.copy_2_series([mblock],[site[:-1]+'s'],role='final',wght=100.0)
    renamed_oblock = tsp.copy_2_series([oblock],[site[:-1]+'o'],role='final',wght=100.0,context=tc.PEST_CONTEXT)
    pest_mblocks.extend(renamed_mblock)   
    pest_oblocks.extend(renamed_oblock)   
  

hobs_file = 'UMD.03\\obsref\\head\\heads.smp'
hobs_smp = pu.smp(hobs_file,date_fmt = tc.DATE_FMT,load=True)
hobs_start,hobs_end = hobs_smp.get_daterange(site_name='all',startmin=obs_start,endmax=obs_end)

mobs_file = 'UMD.03\\modref\\head\\mheads.smp'
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

#--process each head record individually because of the variable record length
for i,[site_name,oblock,mblock] in enumerate(zip(site_names,oblocks,mblocks)):        
        oblock = [oblock]
        mblock = [mblock]
        
        #--get the starting and end date of each record within the reduced model sim time
        rstart,rend = hobs_start[site_name],hobs_end[site_name]        
        if rend > obs_start:                                                 
            #--find the date range for this record and write date files
            dstart,dend = max(obs_start,rstart),min(obs_end,rend)
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
            #renamed_block = tsp.copy_2_series(reduced_block,[site_name+'_ro'],role='final',wght=100.0,context=tc.PEST_CONTEXT)
            #pest_oblocks.extend(renamed_block)
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
            #renamed_block = tsp.copy_2_series(reduced_block,[site_name+'_r'],role='final',wght=100.0)
            #pest_mblocks.extend(renamed_block)
            renamed_block = tsp.copy_2_series(bi_block,[site_name],role='final',wght=100.0)
            pest_mblocks.extend(renamed_block)           

        else:
            print 'no data for record in reduced sim time:',site_name           
        #if i > 100:
            #break

#--write the model run tspoc file                              
tsp.set_context('model_run')
tsp.tsproc_file = 'tsproc_model_run.dat'
tsp.write_tsproc()

#--write the setup tsproc file
tsp.write_pest(tpl_files,modin_files,pest_oblocks,pest_mblocks,svd=True,parms='pst_components\\params.dat',parm_grp='pst_components\\param_groups.dat')
tsp.set_context(tc.PEST_CONTEXT)
tsp.tsproc_file = 'tsproc_setup.dat'

tsp.write_tsproc()
os.system('tsproc.exe <tsproc_setup.in >tsproc_screen.out')
os.system('addreg1.exe pest.pst umd03.pst')

