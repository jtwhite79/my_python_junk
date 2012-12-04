from datetime import datetime
import numpy as np
import pylab
import pandas
import bro

#--load the census info
#census = pandas.read_csv('source_spreadsheets\\broward_population.csv',sep='|',index_col=1,parse_dates=True)
#census.pop('FIPS')
f = open('source_spreadsheets\\broward_population.csv','r')
f.readline()
dts,vals = [],[]
for line in f:
    raw = line.strip().split('|')
    dt = datetime(year=int(raw[1]),month=1,day=31)
    val = float(raw[2])
    dts.append(dt)
    vals.append(val)
df = pandas.DataFrame({'population':vals},index=dts)


df_model = pandas.DataFrame({'population':np.NaN},index=bro.sp_end)
df_model = df_model.combine_first(df)

#df_model['population_fill'] = df_model['population'].fillna()
df_model['pi'] = df_model['population'].interpolate()
df_model.pop('population')
df_model.to_csv('dataframes\\broward_population_interp.csv',index_label='datetime')
#df_model = df_model[bro.start:bro.end]
#pop_delta = (df_model['pi'][1:].values - df_model['pi'][:-1]).values
#pop_delta_frac = pop_delta / df_model['pi'][1:].values
#df_pdelta = pandas.DataFrame({'pdelta':1.0-pop_delta_frac},index=bro.sp_end[:-1])
#df_model.plot()
#df_pdelta.plot()
#pylab.show()
#df_pdelta.to_csv('broward_population_delta.csv',index_label='datetime')
#df_model.plot()
#pylab.show()