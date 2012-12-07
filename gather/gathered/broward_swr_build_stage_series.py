import os
import copy
from datetime import datetime
import pandas
import shapefile

import pestUtil as pu
from bro import flow

#--get the dbhydro sampled monthly series
db_dir = '..\\_dbhydro\\stressperiod_stage_smp_navd\\'
db_files = os.listdir(db_dir)
#db_names = []
db_dict = {}
for dfile in db_files:
    dname = dfile.split('.')[0].upper().strip()
    #db_names.append(dname)
    smp = pu.smp(db_dir+dfile,load=True,pandas=True)
    db_dict[dname] = copy.deepcopy(smp.records)

#--get the coastal stage record - sampled to stress periods
noaa_file = '..\\_noaa\\noaa_sp.smp'
noaa_smp = pu.smp(noaa_file,load=True,pandas=True)
noaa_df = noaa_smp.records

#--load the reach shapefile from swrpre
swr_shapename = '..\\_gis\\scratch\\sw_reaches_conn_SWRpolylines_2'
shp = shapefile.Reader(swr_shapename)
fnames = shapefile.get_fieldnames(swr_shapename)
ibnd_idx,stg_idx,reach_idx = 16,17,22

stg_dict = {}
m_range = flow.sp_end

out_dir = 'reach_series\\'
reach_dfs = []
for i in range(shp.numRecords):
    rec = shp.record(i)
    ibnd,stg = rec[ibnd_idx],rec[stg_idx]
    reach = rec[reach_idx]
    print 'processing reach',reach
    if ibnd > 0:
        #--parse the cryptic stg attribute
        raw = stg.split(',')        
        dfs = []
        for r in raw:
            r = r.replace('"','')
            try:
                val = float(r)
                df = pandas.DataFrame({reach:val},index=m_range)
                dfs.append(df)
            except ValueError:
                if 'COASTAL' in r.upper():
                    df = copy.deepcopy(noaa_df) 
                    df[reach] = df['noaa']
                    df.pop('noaa')                  
                    dfs.append(df)
                else:                    
                    df = db_dict[r.upper().strip()]
                    site = df.keys()[0]
                    df[reach] = df[site]
                    df.pop(site)
                    dfs.append(df)        

        df = dfs[0]
        for df2 in dfs[1:]:
            df = df.combine_first(df2)
        #df = df.dropna()
        df = df[flow.start:flow.end]
        if len(df) != len(df.dropna()):
            raise Exception('incomplete record '+str(reach))
        df.to_csv(out_dir+str(reach)+'.csv',index_label='datetime')
        reach_dfs.append(df)
df = pandas.concat(reach_dfs,axis=1)
df.to_csv('reach_series.csv',index_label='datetime')







