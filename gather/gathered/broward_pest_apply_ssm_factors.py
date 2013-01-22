from datetime import datetime
import numpy as np
import pandas
 
from bro_pred import seawat

'''writes the calibration and prediction ssm files and applies monthly multiplication factors to concentrations > 0 and < 1
'''
ssm_top = '''T F T T T T F F F F 
     33127
         1
         0       0.0                FREE         0
         1
         0       0.0                FREE         0\n'''

def write_ssm_sp(f_ssm,rec):
    arr = np.empty((rec.shape[0],5))
    lay,row,col,itype = rec.index.get_level_values('layer'),rec.index.get_level_values('row'),rec.index.get_level_values('column'),rec.index.get_level_values('itype')
    arr[:,0],arr[:,1],arr[:,2],arr[:,4] = lay,row,col,itype
    arr[:,3] = rec.values
    f_ssm.write(' {0:9d}\n'.format(rec.shape[0]))
    np.savetxt(f_ssm,arr,fmt=' %9d %9d %9d %9.3G %9d')
    f_ssm.write(' {0:9d}\n {0:9d}\n'.format(-1,-1))

    pass


def apply():    
    factor_file = 'par\\ssm_factors.dat'        
    df_file = 'conc_bc_dfs\\bro.02_calibration_seawat.csv'
    cal_ssm_name = 'bro.02\\calibration\\seawat.ssm'
    pred_ssm_name = 'bro.02\\prediction\\seawat.ssm'
    
    #--load the monthly conc factors
    factors = np.loadtxt(factor_file)
    
    print 'loading dataframe',df_file
    cal_df = pandas.read_csv(df_file,sep='|',index_col=['layer','row','column','itype'])
    print 'calibration dataframe shape',cal_df.shape
    #--cast the calibration dataframe columns to dts
    cal_dts = []
    for dt_str in cal_df.columns:
        dt = datetime.strptime(dt_str,'%Y%m%d')
        cal_dts.append(dt)
    cal_df.columns = cal_dts
    
    print 'forming prediction dataframe'
    cal_dts.sort()
    last_cal_ssm = cal_df[cal_dts[-1]]
    print last_cal_ssm.shape
    col_dict = {}
    for start in seawat.sp_start:
        col_dict[start] = last_cal_ssm
    pred_df = pandas.DataFrame(col_dict)
    
    print 'applying factors to prediction dataframe'
    groups = cal_df.groupby(lambda x:x.month,axis=1)
    applied = []
    for month,group in groups:       
        group *= factors[month-1]       
        group[group > 1.0] = 1.0
        applied.append(group)    
    pred_applied_df = pandas.concat(applied,axis=1)       
    
    print 'writing prediction ssm file'
    f_ssm = open(pred_ssm_name,'w',0)
    f_ssm.write(ssm_top)
    for dt,record in pred_applied_df.iteritems():
        print dt,'\r',
        write_ssm_sp(f_ssm,record.dropna()) 
        break 


    return
        
    print 'applying factors to calibration dataframe'
    groups = cal_df.groupby(lambda x:x.month,axis=1)
    applied = []
    for month,group in groups:
        #print group[group == 1.0].shape
        group *= factors[month-1]       
        group[group > 1.0] = 1.0
        #print group[group == 1.0].shape
        applied.append(group)    
    cal_applied_df = pandas.concat(applied,axis=1)        
        
       

    




if __name__ == '__main__':
    apply()

