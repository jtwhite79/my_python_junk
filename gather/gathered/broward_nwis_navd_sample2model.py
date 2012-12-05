from datetime import datetime
import pandas
from bro import flow

#--load
df = pandas.read_csv('dataframes\\navd.csv',parse_dates=True,index_col=0)
print df.count().sum()
#--truncate over model date range
df = df[flow.start:flow.end]
#--group by 
groups = df.groupby([lambda x:x.year,lambda x:x.month]).mean()

#--very unpythonic...need to convert from yr,mn tup back to datetime
dfs = []
for site,rec in groups.iteritems():
    if rec.dropna().count() > 0:
        print site
        yrmn_tups = rec.dropna().index
        vals = rec.dropna().values
        dts = []
        for tup in yrmn_tups:
            dt = datetime(year=tup[0],month=tup[1],day=1)
            dts.append(dt)
        df = pandas.DataFrame({site:vals},index=dts)
        dfs.append(df)
df = pandas.concat(dfs,axis=1)
print df.count().sum()
df.to_csv('dataframes\\navd_sp.csv',index_label='datetime')

#pass