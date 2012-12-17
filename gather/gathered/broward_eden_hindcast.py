from datetime import datetime,timedelta
import numpy as np
import pandas
from bro import flow
'''samples up model stress periods'''





#--load the EDEN timeseries csv
df = pandas.read_csv('eden_timeseries.csv',parse_dates=True,index_col=0)

#--calc the julian day mean value for each timeseries
means = df.groupby(lambda x:x.timetuple()[7]).mean()

#--process each series - too large to do simultaneously
#start,end = datetime(year=1920,month=1,day=1),datetime(year=2012,month=5,day=31)
start,end = flow.start,flow.end
d_range = pandas.date_range(start,end,freq='1D')
m_range = pandas.date_range(start,end,freq='1M')
smp_dir = 'stage_smp_full\\'
dfs = []
for key in df:
    print 'processing',key
    #--create and fill a full-range time series with monthly average values
    df_full = pandas.DataFrame({key:np.NaN},index=d_range)
    for dt in d_range:
        jd = dt.timetuple()[7]
        df_full[key][dt] = means[key][jd]
    
    df_daily = pandas.DataFrame({key:np.NaN},index=d_range)                    
    df_daily = df_daily.combine_first(df)
    df_daily = df_daily.combine_first(df_full)
    for kkey in df_daily:
        if kkey != key:
            df_daily.pop(kkey)
    
    #--sample to model stress periods
    df_monthly = df_daily.resample('1M',how='mean')
    dfs.append(df_monthly)
                             
    f = open(smp_dir+str(key)+'.smp','w')
    for dt in df_monthly.index:
        f.write(str(key).ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 12:00:00 {0:15.6E}\n'.format(df_monthly[key][dt]))
    f.close()
    #dfs.append(df_daily)
df = pandas.concat(dfs,axis=1)
df.to_csv('eden_sp.csv',index_label='datetime')
#df_daily = pandas.concat(dfs,axis=1)
#df_daily.to_csv('eden_full.csv',index_label='datetime')





