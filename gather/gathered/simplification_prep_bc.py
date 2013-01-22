import sys
import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pylab
import pandas
import shapefile
from simple import grid

def add_zeros(rec,prob = 0.975):
    for i,r in enumerate(rec):
        rand = np.random.rand()
        if rand > prob:
            rec[i] = 0.0
    return rec


def prep():
    upper_layers = [3,4,5,6]
    lower_layers = [10,11,12,13]

    print 'loading pumping well locations'
    shapename = 'shapes\\simple_well_grid_join'
    records = shapefile.load_as_dict(shapename,loadShapes=False)
    rows,cols,ztops,zbots,ids,hydros = \
        records['row'],records['column_'],records['ztop'],\
        records['zbot'],records['Id'],records['hydro']

    upper_flux,lower_flux = -500.0,-1000.0
    upper_std,lower_std = 10.0,10.0
    wel_row,wel_col,wel_lay,wel_name = [],[],[],[]
    wel_flux = []
    pred_name = 'lower_7'
    pred_rate = -2500.0
    for r,c,id,hydro in zip(rows,cols,ids,hydros):
        if id == pred_rate:
            layers = lower_layers
            name = 'pred_'+str(id)
            flux = pred_rate
        elif hydro == 1:
            layers = upper_layers
            name = 'upper_'+str(id)
            flux = upper_flux
        else:
            layers = lower_layers
            name = 'lower_'+str(id)
            flux = lower_flux
        for l in layers:
            wel_row.append(int(float(r)))
            wel_col.append(int(float(c)))
            wel_lay.append(int(float(l)))
            wel_name.append(name)
            wel_flux.append(flux)


    print 'building ghb and wel lrc lists from ibounds'
    ghb_stage,ghb_cond = 95.0,50000.0
    ghb_rows,ghb_cols,ghb_lays,ghb_stages,ghb_conds,ghb_names = [],[],[],[],[],[]
    flux_rows,flux_cols,flux_lays,flux_names = [],[],[],[]
    ghb_stage_rate = 0.0005
    dwn_j = 204
    for k,iname in enumerate(grid.ibound_names):
        arr = np.loadtxt('_model\\'+iname)
        for i in range(grid.nrow):
            for j in range(grid.ncol):
                if arr[i,j] == 4:
                    ghb_rows.append(i+1)
                    ghb_cols.append(j+1)
                    ghb_lays.append(k+1)
                    if j < dwn_j:
                        ghb_stages.append(ghb_stage + ((dwn_j - j) * ghb_stage_rate))
                    elif j == dwn_j:
                        ghb_stages.append(ghb_stage)
                    elif j > dwn_j:
                        ghb_stages.append(ghb_stage + ((j - dwn_j) * ghb_stage_rate))
                elif arr[i,j] == 2 and grid.lay_key[k] == 'upper':
                    flux_rows.append(i+1)
                    flux_cols.append(j+1)
                    flux_lays.append(k+1) 
                    flux_names.append('flux_'+str(k+1))
                        


    wel_row.extend(flux_rows)
    wel_col.extend(flux_cols)
    wel_lay.extend(flux_lays)
    wel_name.extend(flux_names)
    #--calc the flux on the north
    ncells = len(flux_rows)
    xsec = 5.0 * 100.0
    target_rate = 0.02
    flux = xsec * target_rate
    


    #wel_flux.extend([flux]*len(flux_rows))
    df_wel = pandas.DataFrame({'layer':wel_lay,'row':wel_row,'column':wel_col,'name':wel_name})
    df_wel.to_csv('_misc\\well_locs.csv')

    df_ghb = pandas.DataFrame({'layer':ghb_lays,'row':ghb_rows,'column':ghb_cols,'stage':ghb_stages})
    df_ghb['conductance'] = ghb_cond
    df_ghb.to_csv('_misc\\ghb_locs.csv')

    #--write tpl files for each 
    step = relativedelta(months=1)
    day = grid.start
    d_count = 1
    p_count = 1
    wel_pnames = []
    pdict = {}
    while day < grid.end:
        day_entries = []
        last = wel_name[0]
        for i,name in enumerate(wel_name):
            if 'flux' in name:
                name = name.split('_')[0]

            if name != last:
                p_count += 1
                last = name
            pname = 'w{0:04d}_{1:04d}'.format(p_count,d_count)
            if pname not in wel_pnames:
                wel_pnames.append(pname)
            tpl_string = '~{0:20s}~'.format(pname)
            day_entries.append(tpl_string)
        pdict[day.strftime('%Y%m%d')] = day_entries
        day += step
        d_count += 1
    wel_tpl = pandas.DataFrame(pdict,index=wel_name)
    f = open('tpl\\wel.tpl','w')
    f.write('ptf ~\n')
    wel_tpl.to_csv(f,index_label='wel_name')
    f.close()
    wel_tpl.dtype = np.float64
    
    for i,col in enumerate(wel_tpl.columns):
        wel_tpl[col] = 1.0
    wel_tpl.to_csv('par\\wel.dat',index_label='wel_name')
    #--generate markov series for the upper/lower and flux
    #--set the last entry to the max for the prediction
    flux_series = [float(flux)]
    beta = 0.5 
    for i in range(wel_tpl.shape[1]-1):
        innov = np.random.normal(0.0,flux*0.1)

        val = float(flux_series[-1]) + (beta * innov)
        print val
        flux_series.append(val)  
    flux_series[-1] = min(flux_series)
    lower_series = [lower_flux]
    beta = 0.5 
    for i in range(wel_tpl.shape[1]-1):
        innov = np.random.normal(0.0,lower_std)
        val = lower_series[-1] + (beta * innov)
        lower_series.append(val)  
    #lower_series = np.array(lower_series) - lower_flux
    for wname in wel_tpl.index:
        if wname == pred_name:
            wseries = np.zeros((len(lower_series)))
            wseries[-1] = pred_rate                   
            wel_tpl.ix[wname] = wseries

        elif 'upper' in wname:
            wseries = lower_series + np.random.normal(0.0,10.0,wel_tpl.shape[1])
            wseries[np.where(wseries > 0.0)] = 0.0
            wseries[-1] = np.min(wseries)
            wel_tpl.ix[wname] = wseries 
        elif 'lower' in wname:
            wseries = lower_series + np.random.normal(0.0,10.0,wel_tpl.shape[1])
            wseries[np.where(wseries > 0.0)] = 0.0
            wseries[-1] = np.min(wseries)
            wel_tpl.ix[wname] = wseries - (lower_flux - upper_flux)
        elif 'flux' in wname:
            wel_tpl.ix[wname] = flux_series
    
    wel_tpl.to_csv('base\\wel.dat',index_label='wel_name')
    #wel_tpl.dtype = np.float64
    
    #wel_tpl.ix['flux_1'].T.plot(legend=False)
    #wel_tpl.ix['upper_1'].T.plot(legend=False)
    #wel_tpl.ix['upper_5'].T.plot(legend=False)
    #wel_tpl.ix['lower_2'].T.plot(legend=False)
    #pylab.show()

    pdict = {}
    day = grid.start
    d_count = 1
    ghb_pnames = []
    while day < grid.end:
        day_entries = []    
        for ptype in ['stg','cnd']:
            pname = '{0:3s}_{1:04d}'.format(ptype,d_count)
            ghb_pnames.append(pname)
            tpl_string = '~{0:20s}~'.format(pname)
            day_entries.append(tpl_string)
        pdict[day.strftime('%Y%m%d')] = day_entries
        day += step
        d_count += 1
    ghb_tpl = pandas.DataFrame(pdict,index=('stage','conductance'))
    f = open('tpl\\ghb.tpl','w')
    f.write('ptf ~\n')
    ghb_tpl.to_csv(f,index_label='ptype')
    f.close()
    for i,col in enumerate(ghb_tpl.columns):
        ghb_tpl[col] = 1

    ghb_tpl.to_csv('par\\ghb.dat',index_label='ptype')
    


    f = open('pst_components\\ghbwel_pars.dat','w',0)
    for pname in wel_pnames:
        f.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  well_mult   1.0   0.0   1\n'.format(pname))
    for pname in ghb_pnames:
        f.write('{0:20s}  log   factor  1.0  1.0e-10  1.0e+10  ghb_mult   1.0   0.0   1\n'.format(pname))
    f.close()
    f = open('pst_components\\ghbwel_grps.dat','w',0)
    f.write('well_mult       relative     1.0000E-02   0.000      switch      2.000      parabolic\n')
    f.write('ghb_mult        relative     1.0000E-02   0.000      switch      2.000      parabolic\n')
    f.close()





#--random sampling
##--first create normal distributions for the wells
#upper_mean,upper_std = -500.0,10.0
#lower_mean,lower_std = -5000.0,50.0
#nper = len(grid.sp_start)
#well_records = []
#for id,hydro in zip(ids,hydros):
#    if hydro == 3:
#        rec = np.random.normal(lower_mean,lower_std,nper)
#    if hydro == 1:
#        rec = np.random.normal(upper_mean,upper_std,nper)
#    rec = add_zeros(rec)
#    well_records.append(rec)
#well_records = np.array(well_records).transpose()
#well_records[np.where(well_records>0.0)] = 0.0
#mnw_ds2 = []
#names = []
#for id,r,c,top,bot,hydro in zip(ids,rows,cols,ztops,zbots,hydros):
#    #--mnw 
#    if hydro ==1:
#        name = 'upper_'+str(id)
#    else:
#        name = 'lower_'+str(id)
#    names.append(name)
#    line_2a = '{0:20s}{1:10f}{2:>33s}\n'.format(name,-1,'#2a')
#    mnw_ds2.append(line_2a)
#    line_2b = '{0:20s}{1:10d}{2:10d}{3:10d}{4:10d} #2b\n'.format('THIEM',0,0,0,0)
#    mnw_ds2.append(line_2b)
#    line_2c = '{0:10.4f}{1:>53s}\n'.format(1.0,'#2c')
#    mnw_ds2.append(line_2c)
#    line_2d2 = ' {0:9.4f} {1:9.4f} {2:9.0f} {3:9.0f}{4:>26s}\n'.format(float(top),float(bot),int(float(r)),int(float(c)),'#2d-2\n')
#    mnw_ds2.append(line_2d2) 

#f_mnw = open(grid.modelname+'.mnw','w',0)
#f_mnw.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
#f_mnw.write(' {0:9.0f} {1:9.0f} {2:9.0f}\n'.format(len(ids),0,0))    
#for line in mnw_ds2:
#    f_mnw.write(line)

#f_wel = open(grid.modelname+'.wel','w',0)
#f_wel.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
#f_wel.write(' {0:9.0f} {1:9.0f} {2:9.0f}\n'.format(300,0,0))    
#for i,slice in enumerate(well_records):
#    lines = []
#    for name,rate in zip(names,slice):
#        lines.append('{0:20s}{1:15.4G}\n'.format(name,rate))
#    f_mnw.write('{0:10d} {1:20s} {2:3d}\n'.format(len(lines),'#3 Stress Period',i+1))
#    for line in lines:
#        f_mnw.write(line)
        
#    lines = []
#    for name,rate,row,col in zip(names,slice,rows,cols):
#        if 'upper' in name:
#            layers = upper_layers
#        else:
#            layers = lower_layers
#        rate /= float(len(layers))
#        for lay in layers:
#            line = '{0:10d}{1:10d}{2:10d}{3:15.4E}  #{4:20s}\n'\
#                .format(lay,int(float(row)),int(float(col)),rate,name)
#            lines.append(line)
#    f_wel.write('{0:10d}{1:10d} #{2:20s}{3:4d}\n'.format(len(lines),0,'stress period ',i+1))        
#    for line in lines:
#        f_wel.write(line)
#f_mnw.close()
#f_wel.close()

if __name__ == '__main__':
    prep()