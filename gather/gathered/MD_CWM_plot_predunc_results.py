import numpy as np
import pylab
import pandas
import pst_handler as ph


pst = ph.pst('umd02_processed_head.pst')
pst.observation_data.index = pst.observation_data.obsnme

df_file = '\\\\IGSBAMEWMS152\\Home\jwhite\MiamiDade\\umd02_la_master\\sliced\\i64predunc1_unscaled.csv'
df = pandas.read_csv(df_file,sep='|',index_col=0)
pred_obs = pst.observation_data.ix[df.index.values].dropna()
print pst.observation_data.obsval.shape,df.shape
df = np.abs(df.div(pred_obs.obsval,axis=0)* 100.0)

col_strings = df.columns
rawpro,bf,prepost = [],[],[]
for c in col_strings:
    if 'raw' in c:
        rawpro.append('raw')
    else:
        rawpro.append('processed')
    if 'bf' in c:
        bf.append('with_bf')
    else:
        bf.append('no_bf')
    if 'pre' in c:
        prepost.append('pre-cal')
    else:
        prepost.append('post-cal')
tups = zip(*(rawpro,bf,prepost))
df.columns = pandas.MultiIndex.from_tuples(tups,names=('processing','with_bf','pre-post'))
df = df.xs('no_bf',level=1,axis=1)
for site,record in df.iterrows():
    record.ix[('raw','pre-cal')] = np.NaN
    
   
    ax = record.dropna().plot(kind='bar')
    ax.set_ylabel('% of calculated cumulative exchange')
    ax.set_title(site)
    pylab.show()
    break