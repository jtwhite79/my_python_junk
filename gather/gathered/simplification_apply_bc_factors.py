import sys
from datetime import datetime
import numpy as np
import pandas
from simple import grid

def apply(modelname,ghb_locs,wel_locs):
    ghb_iface,wel_iface = 4,0
    #--ghbs    
    pars = pandas.read_csv('par\\ghb.dat',index_col='ptype')    
    locations = pandas.read_csv(ghb_locs,index_col=0)
    f = open('_model\\'+modelname+'.ghb','w',0)
    f.write('# '+str(sys.argv[0])+'  '+str(datetime.now())+'\n')
    f.write('{0:10d}{1:10d} AUX IFACE NOPRINT\n'.format(locations.shape[0],53))
    dts = []
    for i,[dt_str,pvals] in enumerate(pars.iteritems()):
        dt = datetime.strptime(dt_str,'%Y%m%d')
        dts.append(dt)

    pars.columns = dts
    for i,sp in enumerate(grid.sp_start):
        if sp == grid.sp_start[-1]:
            pass
        for dt in dts:
            if sp <= dt:
                break 
        pvals = pars[dt] 
        f.write('{0:10d}{1:10d} # stress period {2:3d} {3:20s}\n'.format(locations.shape[0],0,i+1,str(sp)))
        stage = locations['stage'] * pvals['stage']
        cond = locations['conductance'] * pvals['conductance']
        for l,r,c,stg,cnd in zip(locations['layer'],locations['row'],locations['column'],stage,cond):
            f.write('{0:10d}{1:10d}{2:10d}{3:15.5E}{4:15.5E} {5:9d}\n'.format(l,r,c,stg,cnd,ghb_iface))
    f.close()
    
    
    
    #--wels
    pars = pandas.read_csv('par\\wel.dat',index_col='wel_name')
    base = pandas.read_csv('base\\wel.dat',index_col='wel_name')
    pars = pars.mul(base) 
   
    locations = pandas.read_csv(wel_locs,index_col='name')
    f = open('_model\\'+modelname+'.wel','w',0)
    f.write('# '+str(sys.argv[0])+'  '+str(datetime.now())+'\n')
    f.write('{0:10d}{1:10d} AUX IFACE NOPRINT\n'.format(locations.shape[0],53))
    dts = []
    for i,[dt_str,pvals] in enumerate(pars.iteritems()):
        dt = datetime.strptime(dt_str,'%Y%m%d')
        dts.append(dt)
    pars.columns = dts
    for i,sp in enumerate(grid.sp_start):
        if sp == grid.sp_start[-1]:
            pass
        for dt in dts:
            if sp <= dt:
                break 
        pvals = pars[dt]                
        f.write('{0:10d}{1:10d} # stress period {2:3d} {3:20s}\n'.format(locations.shape[0],0,i+1,str(sp)))
        flux = pvals
        for l,r,c,name in zip(locations['layer'],locations['row'],locations['column'],locations.index):
            flx = pvals[name]
            f.write('{0:10d}{1:10d}{2:10d}{3:15.5E} {4:9d} #{5:20s}\n'.format(l,r,c,flx,wel_iface,name))
    f.close()

    

if __name__ == '__main__':
    #apply('simple_rc','_misc\\ghb_locs_rc.csv','_misc\\well_locs_rc.csv')
    apply('simple_l','_misc\\ghb_locs_layer.csv','_misc\\well_locs_layer.csv')
