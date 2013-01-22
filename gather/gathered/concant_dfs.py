import os
import pandas

df_dir = 'dataframes\\'
files = os.listdir(df_dir)

dfs = []
for f in files:
    df = pandas.read_csv(df_dir+f,index_col=0,parse_dates=True)
    print f,df.shape
    dfs.append(df)
df = pandas.concat(dfs,axis=0)
df.to_csv('NEXRAD.csv',index_label='datetime')