import pylab
import pestUtil as pu


smp_obs = pu.smp(fname='UMD.01\\obsref\\head\\heads.smp',load=True,date_fmt='%m/%d/%Y')
#smp_mod = pu.smp(fname='UMD.01\\modref\\head\\mheads.smp',load=True,date_fmt='%m/%d/%Y')

smp_filt = pu.load_smp_from_tsproc('processed_mod_vs_obs_biweek_filtered.dat')

#--get a list of 'observation' series names
osites = []
for site in smp_filt.records.keys():
    if site.endswith('_o') and site not in osites:
        osites.append(site)

plt_dir = 'png\\filt'
for site in osites:
    print site
    filt_obs = smp_filt.records[site]
    raw_obs = smp_obs.records[site[:-2].upper()]
    filt_mod = smp_filt.records[site[:-2]]
    #raw_mod = smp_mod.records[site[:-2].upper()]
    #fig = pylab.figure(figsize=(5,5))
    fig = pylab.figure()
    ax = pylab.subplot(111)    
    #ax.plot(filt_obs[:,0],filt_obs[:,1],'b.',color='b')
    ax.plot(filt_obs[:,0],filt_obs[:,1],'b-',label='processed',lw=0.5,color='b')
    
    #ax.plot(filt_mod[:,0],filt_mod[:,1],'g.',color='g')
    #ax.plot(filt_mod[:,0],filt_mod[:,1],'g-',label='modfilt',lw=0.5,color='g')
    ax.plot(raw_obs[:,0],raw_obs[:,1],'g-',label='native',lw=0.5,color='g')
    ax.grid()
    ax.set_ylabel('water level ($ft NAVD$)')
    ax.legend()
    #ax.set_xticklabels(ax.get_ticklabels(),rotation=90,size='small')
    fname = plt_dir+site+'.png'
    pylab.savefig(fname,dpi=300,format='png',bbox_inches='tight')
    pylab.close('all')



