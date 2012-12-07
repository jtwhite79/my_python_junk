from datetime import datetime
import numpy as np
import pandas
import shapefile
import pestUtil as pu
from bro import flow
'''samples the water level data to the model stress periods
'''


df = pandas.read_csv('dataframes\\navd.csv',parse_dates=True,index_col=0)
#--truncate over model date range
df = df[flow.start:flow.end]
#--get the average water level within each observation period
site_dict = {}
for site in df.keys():
    site_dict[site] = []
dfs = []
for os,oe,spe in zip(flow.obs_start,flow.obs_end,flow.sp_end):
    odf = df[os:oe].mean()
    print odf.shape
    dfs.append(odf)

    #for site,val in zip(odf.index,odf.values):
    #    site_dict[site].append([spe,val])
print len(dfs)
df = pandas.concat(dfs,axis=1).T
print df.shape,len(flow.sp_end)
df.index = flow.sp_end
df.to_csv('dataframes\\navd_modeltime.csv',index_label='datetime')
print df
#smp = pu.smp(None,load=False,pandas=False)
#smp.records = site_dict
#smp.save('navd_thinned.smp',dropna=True)

#dfs = []
#for site in site_dict.keys():
#    print site
#    arr = np.array(site_dict[site])
#    df = pandas.DataFrame({site:arr[:,1]},index=arr[:,0])
#    dfs.append(df)
#df = pandas.concat(dfs,axis=1)
#df.to_csv('dataframes\\navd_modeltime.csv',index_label='datetime')

#pass