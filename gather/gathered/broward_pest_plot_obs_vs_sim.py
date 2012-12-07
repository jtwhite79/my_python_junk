import os
import numpy as np
import pylab
import pandas
import pestUtil as pu

obs_dir = 'smp\\obs\\'
mod_dir = 'smp\\mod\\'
obs_files,mod_files = os.listdir(obs_dir),os.listdir(mod_dir)

obs_color,mod_color = 'b','g'
plt_dir = 'png\\obs_vs_sim\\'
for ofile in obs_files:
    assert ofile in mod_files,ofile+' not found in model smp files'
    osmp = pu.smp(obs_dir+ofile,load=True,pandas=True)
    msmp = pu.smp(mod_dir+ofile,load=True,pandas=True)
    odf = osmp.records
    mdf = msmp.records
    #--plotting
    
    if 'NAVD' in ofile.upper():
        ylabel = 'water level $ft NAVD$'
        ylim = [-10.0,10.0]
        plt_prefix = plt_dir+'navd_'
    else:
        ylabel = 'relative concetration'
        ylim = [-0.1,1.0]
        plt_prefix = plt_dir+'conc_'
    for site in odf.keys():
        print site

        fig = pylab.figure(figsize=(8,4))
        ax = pylab.subplot(111)
        ax.set_title(site)
        ax.plot(odf[site].index,odf[site].values,color=obs_color,ls='-')
        ax.plot(mdf[site.upper()].index,mdf[site.upper()].values,color=mod_color,ls='-')
        ax.set_ylim(ylim)
        ax.set_ylabel(ylabel)
        ax.grid()
        #axt = pylab.twinx()
        #axt.plot(odf[site].index,odf[site].values-mdf[site.upper()].values,'k-')
        pylab.savefig(plt_prefix+site,fmt='png',dpi=300,bbox_inches='tight')
        pylab.close('all')



        