import os
import pylab
import pandas
import pestUtil as pu
import bro


#--the tailwater coastal strutures
coastal = ['G56','G57','S37A','S36','S33','G54','S29']
data_dir = '..\\..\\_dbhydro\\stage_dfs_navd\\'
data_files = os.listdir(data_dir)
coastal_files,coastal_structs = [],[]
for dfile in data_files:
    raw = dfile.split('.')[0].split('_')
    if raw[0].upper() in coastal and raw[1].upper() == 'T' and len(raw) > 2:
        coastal_files.append(dfile)
        coastal_structs.append(raw[0].upper())

#--load each
dfs_daily = []
dfs_julian = []
for cfile,cname in zip(coastal_files,coastal_structs):
    df = pandas.read_csv(data_dir+cfile,index_col=0,parse_dates=True).dropna()
    #--the mean of each series for each julian day
    means = df.groupby(lambda x:x.timetuple()[7]).mean()
    dfs_julian.append(means)
    dfs_daily.append(df)

#--calc a global mean for each julian day and make a new series 
df = pandas.concat(dfs_julian,axis=1)
jd_vals = []
for jd,values in df.T.iteritems():
    print jd,values.mean()
    jd_vals.append(values.mean())
doff = pandas.date_range(bro.start,bro.end,freq='1D')
vals = []
for dt in doff:
    jd = dt.timetuple()[7]
    vals.append(jd_vals[jd-1])
df_jd = pandas.DataFrame({'jd':vals},index=doff)
df_jd.to_csv('coastal_stage_julianday_avg.csv',index_label='datetime')

#--merge the coastal records
df = pandas.concat(dfs_daily,axis=1)

#--calc the average water level of each day
dts,vals = [],[]
for dt,values in df.T.iteritems():
    values = values.dropna()
    if len(values) > 0:
        dts.append(dt)
        vals.append(values.mean())
df_avg = pandas.DataFrame({'avg':vals},index=dts)
df_avg.to_csv('coastal_stage_avg.csv',index_label='datetime')


   

