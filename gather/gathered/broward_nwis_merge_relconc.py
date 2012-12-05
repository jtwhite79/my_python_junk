
from datetime import timedelta
import numpy as np
import pylab
import pandas
import pestUtil as pu
from bro import seawat

#--load the dataframes
df_names = ['chl.csv','tds.csv','cond.csv']
df_dir = 'dataframes\\'
dfs = []
for dfn in df_names:
    df = pandas.read_csv(df_dir+dfn,index_col=0,parse_dates=True)
    df = df[seawat.start:seawat.end]
    dfs.append(df)

#--build a null df - sue the full freq because later we can use resample to get to monthly
sitenos = {}
drange = pandas.date_range(seawat.start,seawat.end,freq='1D')
for df in dfs:
    for siteno in df.keys():
        if siteno not in sitenos.keys():
            sitenos[siteno] = np.NaN
df_mod = pandas.DataFrame(sitenos,index=drange)

#--fill the null df by merging the data, starting with most accurate
for df in dfs:
    df_mod = df_mod.combine_first(df)
non_nans = df_mod.count()
print non_nans.sum()

df_mod.to_csv(df_dir+'relconc_merged_daily.csv',index_label='datetime')
smp = pu.smp(None,load=False,pandas=True)
smp.records = df_mod
smp.save('relconc.smp',dropna=True)

#--not using yet...going to try to use mod2obs to interpolate...we'll see...
#--thin the data if more than one value in a month
#groups = df_mod.groupby([lambda x:x.year,lambda x:x.month]).count()
#print groups
#for tup,count_rec in groups.iteritems():
#    if count_rec.count() > 1:
#        print tup
#        print count_rec


#df_mod_resamp = df_mod.resample(seawat.pandas_freq,how='mean')
#non_nans = df_mod_resamp.count()
#print non_nans.sum()
#df_mod_resamp.to_csv(df_dir+'relconc_merged_mod.csv',index_label='datetime')


#plt_dir = 'png\\'
#for site in df_mod.keys():
#    fig = pylab.figure()
#    ax = pylab.subplot(111)
#    ax.plot(df_mod[site].index,df_mod[site].values,'b.')
#    ax.plot(df_mod_resamp[site].index,df_mod_resamp[site].values,'g.')
#    ax.set_title(site)
#    pylab.savefig(plt_dir+str(site)+'.png',fmt='png')
    