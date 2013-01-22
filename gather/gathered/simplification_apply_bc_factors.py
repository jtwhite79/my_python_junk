import sys
from datetime import datetime
import numpy as np
import pandas
from simple import grid

def apply():
    #--wels
    pars = pandas.read_csv('par\\wel.dat',index_col='wel_name')
    base = pandas.read_csv('base\\wel.dat',index_col='wel_name')
    pars = pars.mul(base) 
    #--align the pars dataframe with the model stress periods
    #empty_dict = dict(zip(pars.columns,[np.NaN] * len(pars.columns))) 
    #pars_model = pandas.DataFrame(empty_dict,index=grid.sp_start)
    #pars_model = pars_model.combine_first(pars)
    #pars_model = pars_model.fillna(method='ffill')  
    locations = pandas.read_csv('_misc\\well_locs.csv',index_col='name')
    f = open('_model\\'+grid.modelname+'.wel','w',0)
    f.write('# '+str(sys.argv[0])+'  '+str(datetime.now())+'\n')
    f.write('{0:10d}{1:10d}\n'.format(locations.shape[0],0))
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
        for l,r,c,flux,name in zip(locations['layer'],locations['row'],locations['column'],flux,locations.index):
            f.write('{0:10d}{1:10d}{2:10d}{3:15.5E} #{4:20s}\n'.format(l,r,c,flux,name))
    f.close()

    #--ghbs    
    pars = pandas.read_csv('par\\ghb.dat',index_col='ptype')    
    locations = pandas.read_csv('_misc\\ghb_locs.csv',index_col=0)
    f = open('_model\\'+grid.modelname+'.ghb','w',0)
    f.write('# '+str(sys.argv[0])+'  '+str(datetime.now())+'\n')
    f.write('{0:10d}{1:10d}\n'.format(locations.shape[0],0))
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
            f.write('{0:10d}{1:10d}{2:10d}{3:15.5E}{4:15.5E}\n'.format(l,r,c,stg,cnd))
    f.close()

if __name__ == '__main__':
    apply()
