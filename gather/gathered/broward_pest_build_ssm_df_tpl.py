import numpy as np
import pandas
from bro import seawat as cal
from bro_pred import seawat as pred

ssm_files = ['bro.02\\calibration\\seawat.ssm']#,'bro.02\\prediction\\seawat.ssm']
ssm_dtype = np.dtype([('layer',np.int),('row',np.int),('column',np.int),('concentration',np.float),('itype',np.int)])
ssm_columns = ['layer','row','column','concentration','itype']

#--write the monthly multiplier on intercoastal and tidal canal concentrations
f_tpl = open('tpl\\smm_mult.tpl','w',0)
pnames = []
f_tpl.write('ptf ~\n')
for i in range(1,13):
    pname = 'ssm_conc_{0:02d}'.format(i)
    pnames.append(pname)
    f_tpl.write('~{0:15s}~\n'.format(pname))
f_tpl.close()

f_par,f_grp = open('setup\\ssm_parms.dat','w',0),open('setup\\ssm_pargp.dat','w',0)
f_grp.write('ssm_conc  factor  0.01 0.001 switch 2.0 parabolic\n')
for pname in pnames:
    f_par.write('{0:20s} log factor  1.0 1.0e-10 1.0e+10 ssm_conc            1.0 0.0  0 \n'.format(pname))
f_grp.close()
f_par.close()


df_dir = 'conc_bc_dfs\\'
for ssm_file in ssm_files:    
    
    if 'cal' in ssm_file:
        dts = cal.sp_start
    else:
        dts = pred.sp_start
    
    f = open(ssm_file,'r')
    f.readline() #logicals
    f.readline() #mxssm
    for _ in range(4):
        f.readline()
    kper = 1
    df_points,df_nrows = [],[]
    print 'building index for',ssm_file    
    while True:
        print kper,'\r',
        try:
            line = f.readline()
            nact = int(line.strip())
        except:
            break        
        df_points.append(f.tell())
        df_nrows.append(nact)
        for i in range(nact):
            line = f.readline()
            if '-1' in line:
                raise Exception('error building ssm index - negative concentration for entry'+str(i)+' in SP '+str(kper))
        

        for i in range(2):
            line = f.readline()                            
        kper += 1
        if kper == 5:
            break

    #--load the dfs
    print '\nloading dataframes...'
    f.seek(0)    
    dfs = []
    for i,(seekpoint,nrows) in enumerate(zip(df_points,df_nrows)):
        dt = dts[i]        
        print dt,'loading dataframe',i,'of',len(df_points),'\r',
        #f.seek(seekpoint)
        #for n in range(nrows):
        #    line = f.readline()
        #    if '-1' in line:
        #        print dt,n,line.strip()
        f.seek(seekpoint)
        df = pandas.read_table(f,header=None,nrows=nrows,sep='\s*',index_col=(0,1,2,4),names=None) 
        print df.shape          
        df.columns = [dt.strftime('%Y%m%d')]             
        #ssm_columns[3] = dt.strftime('%Y%m%d')
        #df.columns = ssm_columns
        #df.index = pandas.MultiIndex.from_arrays((df.pop('layer'),df.pop('row'),df.pop('column'),df.pop('itype')))
        dfs.append(df)
    
    #df = pandas.concat(dfs,axis=1)
    df = dfs[0]
    for other in dfs[1:]:
        df = df.merge(other,how='outer',left_index=True,right_index=True)
    #--explode the multiindex for saving
    df['layer'] = df.index.get_level_values(0)
    df['row'] = df.index.get_level_values(1)
    df['column'] = df.index.get_level_values(2)
    df['itype'] = df.index.get_level_values(3)
    out_name = '_'.join(ssm_file.split('\\')) + '.csv'    
    df.to_csv(df_dir+out_name,index=False,sep='|')

