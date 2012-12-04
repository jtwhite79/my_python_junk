from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas

import shapefile
import bro
if bro.pandas_freq != '1M':
    raise Exception("must change time delta")

def backfill_missing(dname,drill_dt,series,pop):
    #--use only first five years to build month avgs
    series_clip = series[:series.index[0]+relativedelta(years=5)]
    means = series_clip.groupby(lambda x :x.month).mean()
    dts,vals = [],[]  
    #--get the population estimate for the first entry in series - used to calc scaling
    last_pop = pop[series.index[0]]  
    for sp_dt in bro.sp_end[::-1]:
        if sp_dt >= drill_dt and sp_dt < series.index[0]:
            sp_pop = pop[sp_dt]
            scale = 1.0 - (last_pop - sp_pop) / last_pop
            val = means[sp_dt.month] * scale
            vals.append(val)
            dts.append(sp_dt)
    df = pandas.DataFrame({dname:np.NaN},index=bro.sp_end)
    df_org = pandas.DataFrame({dname:series.values},index=series.index)    
    df = df.combine_first(df_org)
    df_fill = pandas.DataFrame({dname:vals[::-1]},index=dts[::-1])
    df = df.combine_first(df_fill)
    df = df.dropna()
    return df

    
    



pop = pandas.read_csv('dataframes\\broward_population_interp.csv',parse_dates=True,index_col=0)['pi']
pump = pandas.read_csv('dataframes\\pws_monthly_nofill.csv',parse_dates=True,index_col=0)

shapename = '..\\_gis\\shapes\\pws_combine'
shp = shapefile.Reader(shapename)
fieldnames = shapefile.get_fieldnames(shapename)
dril_idx = fieldnames.index('DRIL_YEAR')
dep_idx = fieldnames.index('DPEP_NAME')
dfs,dfs_filled = [],[]
for i in range(shp.numRecords):
    rec = shp.record(i)
    dname = rec[dep_idx]
    drill = datetime(year=int(rec[dril_idx]),month=12,day=31)
    if dname in pump.keys():
        series = pump[dname].dropna()
        
        if series.index[0] > bro.sp_end[0] and series.index[0] > drill:
            print 'missing records for well',dname,'from',drill.strftime('%d/%m/%Y'),'to',series.index[0].strftime('%d/%m/%Y')
            df = backfill_missing(dname,drill,series,pop)
            assert df.index[0] == drill, str(df.index[0])+' '+str(drill)
            df_mod = pandas.DataFrame({dname:np.NaN},index=bro.sp_end)
            df_mod = df_mod.combine_first(df)
            df_mod = df_mod.fillna(0.0)
            dfs_filled.append(df_mod)
            dfs.append(df)
        else:
            df = pandas.DataFrame(series)
            dfs.append(df)
            df_mod = pandas.DataFrame({dname:np.NaN},index=bro.sp_end)
            df_mod = df_mod.combine_first(df)
            df_mod = df_mod.fillna(0.0)            
            dfs_filled.append(df_mod)
    else:
        print 'no records for well',dname
df = pandas.concat(dfs,axis=1)
df.to_csv('dataframes\\pws_filled.csv',index_label='datetime')

df = pandas.concat(dfs_filled,axis=1)
df = df[bro.start:bro.end]
df.to_csv('dataframes\\pws_filled_zeros.csv',index_label='datetime')


        

