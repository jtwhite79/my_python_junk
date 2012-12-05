import os
import pandas
import pestUtil as pu


smp_dir = 'smp_waterlevel_navd\\'
smp_files = os.listdir(smp_dir)
dfs = []
for sf in smp_files:
    print sf
    siteno = str(sf.split('.')[1])
    smp = pu.smp(smp_dir+sf,load=True,pandas=True)
    df = smp.records
    df[siteno] = df['site']
    df.pop('site')
    dfs.append(df)
df = pandas.concat(dfs,axis=1)
df.to_csv('dataframes\\navd.csv',index_label='datetime')

