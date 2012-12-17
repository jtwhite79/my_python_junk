import numpy as np
import pylab
import pandas
import pestUtil as pu

from bro_pred import flow

smp = pu.smp('noaa_sp.smp',load=True,pandas=True)
df = smp.records
df = df.resample('1M',how='mean')
#--use the last value in the dataframe as the base for the projections
start_value = df['noaa'][-1]
print start_value
low_rate = 0.015 #9 inches in 50 years
med_rate = 0.0275 #16.5 inches in 50 years
high_rate = 0.05 #24 inches in 50 years
df_slr = pandas.DataFrame({'no_rise':start_value},index=flow.sp_end)
nyears = df_slr.index.year - df_slr.index[0].year
df_slr['low_rise'] = start_value + low_rate * nyears
df_slr['high_rise'] = start_value + high_rate * nyears
df_slr['med_rise'] = start_value + med_rate * nyears

df_slr.to_csv('noaa_slr.csv',index_label='datetime')
df_slr.plot()
pylab.show()


