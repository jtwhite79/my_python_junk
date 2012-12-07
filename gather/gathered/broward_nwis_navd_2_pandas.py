import os
import pandas
import pestUtil as pu
'''merges all the records from the same site number
'''

smp_dir = 'smp_waterlevel_navd\\'
smp_files = os.listdir(smp_dir)
dfs = []
sitenos = []
for sf in smp_files:
    print sf
    siteno = str(sf.split('.')[1])    
   
    smp = pu.smp(smp_dir+sf,load=True,pandas=True)
    df = smp.records
    df[siteno] = df['site']
    df.pop('site')
    if siteno in sitenos:
        print 'duplicate sites - : ',siteno
        df_left = dfs[sitenos.index(siteno)]        
        df_left = df_left.combine_first(df)        
        #for dt in df_left.index:
        #    if dt not in dfs[sitenos.index(siteno)].index:
        #        print dt
        #pass
    else:
        dfs.append(df)
        sitenos.append(siteno)
df = pandas.concat(dfs,axis=1)
df.to_csv('dataframes\\navd.csv',index_label='datetime')

