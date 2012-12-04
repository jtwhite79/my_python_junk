import os

import pylab
import pandas
import shapefile

import dbhydro_util

#--load the shapefile of rain stations we have records for
#shape_name = '..\\_gis\\shapes\\dbhydro_rain_sites'
#shapes,records = shapefile.load_as_dict(shape_name)

#data_dir = 'RAIN\\RAIN\\'
#data_files = os.listdir(data_dir)
#rain_files = []
#for dbkey in records['Dbkey']:
#    this_file = None
#    for df in data_files:
#        df_dict = dbhydro_util.load_header(data_dir+df)
#        if df_dict['DBKEY'] == dbkey:
#            this_file = data_dir+df            
#            break
#    if this_file is None:
#        print 'missing record for dbkey: ',dbkey
#    else:
#        rain_files.append(this_file)



##--load each record file into the dataframe
#dfs = []
##df = dbhydro_util.load_series(rain_files[0],aspandas=True)
#for f in rain_files[1:]:    
##    df2 = dbhydro_util.load_series(f,aspandas=True)    
##    df = pandas.merge(df,df2,how='outer',right_on='datetime',left_on='datetime')
#    df = dbhydro_util.load_series(f,aspandas=True)    
#    dfs.append(df)
#    #break
##--reindex the dataframe by the 'datetime' 
##df.index = df['datetime']
##df.pop('datetime')
#df = pandas.concat(dfs,axis=1)
#df.to_csv('daily_average_precip.csv',index_label='datetime')

df = pandas.read_csv('daily_average_precip.csv',parse_dates=True,index_col=0)

df.plot()
pylab.show()