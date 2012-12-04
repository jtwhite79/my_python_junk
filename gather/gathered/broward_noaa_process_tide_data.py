import os
import re
from datetime import datetime
import calendar
import numpy as np
import pandas

import bro

dstart_reg = re.compile('Station Year Mo')

d_start,d_end = 55,68

data_dir = 'raw_data\\'
data_files = os.listdir(data_dir)
dfs = []
for dfile in data_files:
    f = open(data_dir+dfile,'r')
    dts,vals = [],[]
    while True:
        line = f.readline()
        if line == '':
            break
        if dstart_reg.search(line) != None:
            while True:
                line = f.readline()
                if line == '':
                    break
                raw = line.strip().split()               
                yr = int(raw[1])
                mn = int(raw[2])
                dy = calendar.monthrange(yr,mn)[1]
                dt = datetime(year=yr,month=mn,day=dy)
                val = float(line[d_start:d_end].replace('[','').replace(']',''))
                dts.append(dt)
                vals.append(val)
    
    f.close()
    df = pandas.DataFrame({dfile.split('.')[0]:vals},index=dts)
    drange = pandas.date_range(min(dts),max(dts),freq='1D')
    df_daily = pandas.DataFrame({dfile.split('.')[0]:np.NaN},index=drange)
    df_daily = df_daily.combine_first(df)
    df_daily = df_daily.fillna(method='bfill')
    dfs.append(df_daily)

df = pandas.concat(dfs,axis=1)
df.to_csv('noaa_tidal_daily.csv',index_label='datetime')
d_range = pandas.date_range(df.index[0],df.index[-1],freq='1D')

#--create a single record
df = pandas.DataFrame({'rec':np.NaN},index=d_range)

for df2 in dfs:
    df2['rec'] = df2[df2.keys()[0]]
    df2.pop(df2.keys()[0])
    df = df.combine_first(df2)
df = df.fillna(method='bfill')
#dts,vals = [],[]
#for dt,values in df.T.iteritems():
#    values = values.dropna().mean()
#    dts.append(dt),vals.append(values)

f = open('noaa.smp','w')
#for dt,val in zip(dts,vals):
for dt,val in df.iterrows():
    f.write('noaa'.ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 00:00:00 {0:15.6e}\n'.format(val.values[0]))
f.close()

#--sample to model stress periods
df_mn = df.resample(bro.pandas_freq,how='mean')
df_mn = df_mn[bro.start:bro.end]

f = open('noaa_sp.smp','w')
#for dt,val in zip(dts,vals):
for dt,val in df_mn.iterrows():
    f.write('noaa'.ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 00:00:00 {0:15.6e}\n'.format(val.values[0]))
f.close()










