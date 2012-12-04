import os
import numpy as np
import pandas
import pestUtil as pu
import bro

#--model stress period date range
m_range = bro.sp_end

#--merged daily smp files
smp_dir = 'daily_stage_smp_navd\\'
smp_files = os.listdir(smp_dir)
out_dir = 'stressperiod_stage_smp_navd\\'
dfs = []
for i,sfile in enumerate(smp_files):
    print 'processing ',sfile,i,' of ',len(smp_files),'\r',
    depname = sfile.split('.')[0]
    smp = pu.smp(smp_dir+sfile,load=True,pandas=True)
    
    df = smp.records
    rname = df.keys()[0]
    df[depname] = df[rname]
    df.pop(rname)
    df = df.astype(float)    
    df = df.resample(bro.pandas_freq,how=np.mean)
    #--create dataframe that is aligned with model stress periods
    #--merge in the record and fill with 0.0
    df_mn = pandas.DataFrame({depname:np.NaN},index=m_range)
    df_mn = df_mn.combine_first(df)     
    df_mn = df_mn[bro.start:bro.end]
    df_mn = df_mn.dropna() 
    dfs.append(df_mn)
    smp.records = df_mn
    smp.save(out_dir+sfile)        
df = pandas.concat(dfs,axis=1)
df.to_csv('stage_stressperiod.csv',index_label='datetime')





