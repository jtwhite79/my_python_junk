import copy
import os
import pestUtil as pu


date_fmt = '%m/%d/%Y'

smp_dir = 'UMD.01\\obsref\\head\\'
smp_files = os.listdir(smp_dir)

obs_smp = pu.smp('UMD.01\\obsref\\head\heads.smp',date_fmt=date_fmt)
mod_smp = pu.smp('UMD.01\\modref\\head\heads.smp',date_fmt=date_fmt)
fcount = 1
for smp_file in smp_files:
    smp = pu.smp(smp_dir+smp_file,date_fmt=date_fmt,load=True)
    for site,record in smp.records.iteritems():
        obs_name = site
        mod_name = copy.deepcopy(site)
        if len(obs_name) > 7:
            print 'truncate',obs_name
            obs_name = obs_name[:7]
        if obs_name in obs_smp.records.keys():
            fc_str = str(fcount)
            obs_name =  fc_str + obs_name[:-len(fc_str)]
            fcount += 1
            print 'duplicate',obs_name
        obs_smp.records[obs_name] = record
        #mod_smp.records[obs_name] = record
obs_smp.save('UMD.01\\obsref\\head\heads.smp')
#mod_smp.save('UMD.01\\modref\\head\heads.smp')

print juunk
