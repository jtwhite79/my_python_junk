import numpy as np
import pandas
import pestUtil as pu

tsproc_file = 'processed.dat'

smp = pu.load_smp_from_tsproc(tsproc_file)

#--cast records to dataframe
dfs = []
for site,record in smp.records.iteritems():
    df = pandas.DataFrame({site:record[:,1]},index=record[:,0])
    dfs.append(df)

df = pandas.concat(dfs,axis=1)

#--find unique site names - strip off the last char
unique_records = {}
for site in df.keys():
    if site[:-1] not in unique_records.keys():
        unique_records[site[:-1]] = [site]
    else:
        unique_records[site[:-1]].append(site)

#--look for missing data
tot_rec = 0
for usite,sites in unique_records.iteritems():
    print '--',usite
    for site in sites:
        print '  ',df[site].dropna().shape
        tot_rec += df[site].dropna().shape[0]
print tot_rec







