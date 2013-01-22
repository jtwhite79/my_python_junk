import numpy as np
import pylab
import pestUtil as pu


#--observation smps
obs_files = ['UMD.01\\obsref\\head\heads.smp']
mod_files= ['UMD.01\\modref\\head\mheads.smp']
plt_dir = 'png\\'
for obs_file,mod_file in zip(obs_files,mod_files):
    obs_smp = pu.smp(obs_file,load=True,date_fmt='%m/%d/%Y')
    mod_smp = pu.smp(mod_file,load=True,date_fmt='%m/%d/%Y')
    sites = obs_smp.records.keys()
    for site in sites:
        obs = obs_smp.records[site]
        mod = mod_smp.records[site]
        fig = pylab.figure(figsize=(5,5))
        ax = pylab.subplot(111)
        ax.plot(obs[:,0],obs[:,1],'b-',label='obs')
        ax.plot(mod[:,0],mod[:,1],'g-',label='mod')
        ax.grid()
        ax.legend()
        fname = plt_dir+site+'.png'
        pylab.savefig(fname,dpi=300,format='png',bbox_inches='tight')
        pylab.close('all')
        #break

