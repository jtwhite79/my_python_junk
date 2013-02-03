import os
import copy
import numpy as np
import pandas
import pestUtil as pu
from bro import flow

#--model stress period date range
m_range = flow.sp_end

#--merged daily smp files
smp_dir = 'pws_smp_daily\\'
smp_files = os.listdir(smp_dir)
out_dir = 'pws_smp_monthly\\'
dfs,dfs_nofill = [],[]
for i,sfile in enumerate(smp_files):
    print 'processing ',sfile,i,' of ',len(smp_files),'\r',
    depname = sfile.split('.')[0]
    smp = pu.smp(smp_dir+sfile,load=True,pandas=True)
    df = smp.records
    df = df.astype(float)
    df = df.fillna(0.0)
    df = df.resample(flow.pandas_freq,how=np.mean)
    #--create dataframe that is aligned with model stress periods
    #--merge in the record and fill with 0.0
    df_mod = pandas.DataFrame({depname:np.NaN},index=m_range)
    df_mod = df_mod.combine_first(df)
    dfs_nofill.append(copy.deepcopy(df_mod))
      
    df_mod = df_mod[flow.start:flow.end]    

    dfs.append(df_mod)
    smp.records = df_mod
    smp.save(out_dir+sfile)        
df = pandas.concat(dfs,axis=1)
df_nofill = pandas.concat(dfs_nofill,axis=1)
#df.to_csv('pws_monthly.csv',index_label='datetime')
df_nofill.to_csv('dataframes\\pws_monthly_nofill.csv',index_label='datetime')
df = df.fillna(0.0)
sum = df.sum(axis=1)
smp = pu.smp(None,pandas=True)
smp.records = pandas.DataFrame({'sum':sum.values},index=sum.index)
smp.save('sum.smp')



