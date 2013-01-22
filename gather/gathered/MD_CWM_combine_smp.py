import copy
import os
from datetime import datetime
import pestUtil as pu


date_fmt = '%m/%d/%Y'

smp_dir = 'UMD.01\\obsref\\head\\'
smp_files = os.listdir(smp_dir)

start = datetime(1996,1,1,12)
end = datetime(2004,12,31,12)


site_names = []
f = open('misc\\bore_coords.dat','r')
for line in f:
    site_names.append(line.split()[0].strip().upper())
f.close()

obs_smp = pu.smp('UMD.01\\obsref\\head\ALL_NWIS_GW.smp',date_fmt=date_fmt,load=True)
filt_smp = pu.smp('UMD.01\\obsref\\head\heads.smp',date_fmt=date_fmt)

f = open('misc\\missing_sites.dat','w')
for site in obs_smp.records.keys():
    #drange = obs_smp.get_daterange(site_name=site)
    if site.replace('-','').strip().upper() in site_names:
        filt_smp.records[site.replace('-','')] = obs_smp.records[site]

    else:
        print 'missing site',site    
        f.write('missing site '+site+'\n')

f.close()
filt_smp.set_daterange(start,end)    
filt_smp.save('UMD.01\\obsref\\head\heads.smp')

