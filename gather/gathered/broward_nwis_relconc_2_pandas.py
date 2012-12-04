import os
import pandas

import pestUtil as pu


dir_dict = {'chl':'smp_rel_conc_chl\\','cond':'smp_rel_conc_regressed\\','tds':'smp_rel_conc_tds\\'}
df_dict = {}
for dtype,smp_dir in dir_dict.iteritems():
    files = os.listdir(smp_dir)
    dfs = []
    for f in files:
        print dtype,f
        raw = f.split('.')
        siteno,sitename = raw[1],raw[2]
        smp = pu.smp(smp_dir+f,load=True,pandas=True)
        df = smp.records
        df[siteno] = df['site']
        df.pop('site')
        dfs.append(df)
        
    df = pandas.concat(dfs,axis=1)
    df.to_csv('dataframes\\'+dtype+'.csv',index_label='datetime')



