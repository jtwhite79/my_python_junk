import os
import numpy as np
import pandas
import pylab
import pestUtil as pu

import bro

#--load the selected smp files near the south boundary
south_smp_list = 'south_ghb_smps.txt'
f = open(south_smp_list,'r')
header = f.readline()
png_idx = 15
smp_dir = 'smp_waterlevel_navd\\'
smp_files = {}
for line in f:
    raw = line.strip().split(',')
    png_name = raw[png_idx]
    raw = png_name.split('\\')
    site_no = raw[-1].split('.')[1]
    smp_name = smp_dir+raw[-1].replace('png','smp').replace('"','')
    assert os.path.exists(smp_name)
    smp_files[site_no] = (smp_name)

#--load the selected smp files near the north boundary
south_smp_list = 'north_ghb_smps.txt'
f = open(south_smp_list,'r')
header = f.readline()
png_idx = 15
smp_dir = 'smp_waterlevel_navd\\'
for line in f:
    raw = line.strip().split(',')
    png_name = raw[png_idx]
    raw = png_name.split('\\')
    site_no = raw[-1].split('.')[1]
    smp_name = smp_dir+raw[-1].replace('png','smp').replace('"','')
    assert os.path.exists(smp_name)
    smp_files[site_no] = (smp_name)


#--load each smp file and concat into a single df
dfs = []
null_dict = {}
for site_no,smp in smp_files.iteritems():
    df = pu.smp(smp,load=True,pandas=True).records
    df[site_no] = df['site']      
    df.pop('site')
    
    dfs.append(df.dropna())
    null_dict[site_no] = np.NaN          
df_south = pandas.concat(dfs,axis=1)

#--calc julian day means
jd_means = df_south.groupby(lambda x:x.timetuple()[7]).mean()

#--create a null daily df over the model time span
dr = pandas.date_range(bro.start,bro.end,freq='1D')
df_daily = pandas.DataFrame(null_dict,index=dr)

#--fill in where we have data
df_daily = df_daily.combine_first(df_south)

#-- fill in with jd means and set fillin weigths
jd_daily_groups = df_daily.groupby(lambda x:x.timetuple()[7]).groups
for jd,idx_group in jd_daily_groups.iteritems():
    for site_no in df_daily.keys():        
        df_daily[site_no][idx_group] = df_daily[site_no][idx_group].fillna(jd_means[site_no][jd])       
        
#--truncated to model time span
df_daily = df_daily[bro.start:bro.end]

#--drop records that are incomplete
to_pop = []
for site,record in df_daily.iteritems():
    if record.shape[0] != record.dropna().shape[0]:
        to_pop.append(site)
for site in to_pop:
    df_daily.pop(site)

#--save the daily
df_daily.to_csv('ghb_NS_stages_daily.csv',index_label='datetime')

#--sample to model freq
df_daily = df_daily.resample(bro.pandas_freq)
df_daily.to_csv('ghb_NS_stages_model.csv',index_label='datetime')
df_daily.plot(subplots=True)
pylab.show()



