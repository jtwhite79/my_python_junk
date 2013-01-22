import os
from datetime import datetime
import numpy as np
import pandas

ghb_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('stage','f4'),('conductance','f4'),('aux','a20')])
ghb_fmt = ' %9d %9d %9d %15.6G %15.6G %20s'
wel_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('flux','f4'),('aux','a20')])
wel_fmt = ' %9d %9d %9d %15.6G %20s'
column_dict = {'stage':3,'conductance':4,'flux':3,'layer':0,'row':1,'column':2}

def load_ascii_list(filename):    
    print filename  
    if 'ghb' in filename.lower():         
        arr = np.genfromtxt(filename,dtype=ghb_dtype,comments='|')   
    elif 'wel' in filename.lower(): 
        arr = np.genfromtxt(filename,dtype=wel_dtype,comments='|')   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr

def load_bin_list(filename):
    if 'ghb' in filename.lower():         
        arr = np.fromfile(filename,dtype=ghb_dtype)   
    elif 'wel' in filename.lower():
        arr = np.fromfile(filename,dtype=wel_dtype)   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr        


def write_ascii_list(filename,df):   
    if 'ghb' in filename:
        fmt = ghb_fmt
    elif 'wel' in filename:
        fmt = wel_fmt         
    arr = np.empty((df.shape[0],df.shape[1]+3))
    arr[:,0],arr[:,1],arr[:,2] = df.index.get_level_values('layer'),df.index.get_level_values('row'),df.index.get_level_values('column')
    for ptype in df.keys():
        arr[:,column_dict[ptype]] = df[ptype].values    
    arr = np.hstack((arr,np.atleast_2d(df.index.get_level_values('zone')).transpose()))
    np.savetxt(filename,arr,fmt=fmt)           

def apply():

    #
    cal_factors_file = 'par\\ghbwel_cal.dat'
    pred_factors_file = 'par\\ghbwel_pred.dat'
    
    #--load the factors
    bc_types,par_types,uids = [],[],[]
    f = open(cal_factors_file)
    hline = f.readline().strip().split(',')
    for entry in hline[1:]:        
        raw = entry.split('_')
        bc_types.append(raw[0])
        par_types.append(raw[1])
        uids.append(raw[2])                                        
            
    fac_dict = {}
    for line in f:
        raw = line.strip().split(',')  
        dt = datetime.strptime(raw[0],'%Y-%m-%d %H:%M:%S')             
        fa = []
        for r in raw[1:]:
            fa.append(float(r))            
        fac_dict[dt] = fa
    f.close()
    factor_df = pandas.DataFrame(fac_dict)
    factor_df.index = pandas.MultiIndex.from_tuples(zip(bc_types,par_types,uids),names=('bc_type','par_type','zone'))   
           
    df_dir = 'ghbwel_dfs\\'
    df_files = os.listdir(df_dir)    

    for df_file in df_files:
        print 'processing',df_file
        raw = df_file.replace('.csv','').split('-')
        bc_type = raw[1]       
        out_dir = '\\'.join(raw[0].split('_'))+'\\'

        #--load the dataframe
        df = pandas.read_csv(df_dir+df_file,sep='|') 
        
        #--this is painfull...form the multindex instances for the columns and rows
        ptypes,dts = [],[]
        idx_col_names,idx_names = [],[]
        col_strings = df.columns
        for cstr in col_strings:
            raw = cstr.replace('\'','').replace('(','').replace(')','').strip().split(',')            
            if raw[1] != '':
                #dt = datetime.strptime(raw[1].strip(),'%Y%m%d')
                dts.append(raw[1].strip())                
                ptypes.append(raw[0].strip())
            else:
                idx_col_names.append(cstr)
                idx_names.append(raw[0])
        idx_cols = []
        for icol in idx_col_names:
            col = df.pop(icol).values            
            idx_cols.append(col)                                
        df.index = pandas.MultiIndex.from_tuples(zip(*idx_cols),names=['layer','row','column','zone'])       
        df.columns = pandas.MultiIndex.from_tuples(zip(ptypes,dts),names=('ptype','dt_str'))  
                            

        #--select the factors for this bc type
        bc_factors = factor_df.xs(bc_type,axis=0,level=0)           
        
        #--iterate over dates
        factor_dts = factor_df.columns 
        record_dts = np.sort(np.unique(df.columns.get_level_values('dt_str')))       
        for dt_str in record_dts:                                        
            dt = datetime.strptime(dt_str,'%Y%m%d')
           
            #--find the right row in the factors dataframe
            factor_dt = None
            for i,d in enumerate(factor_dts):
                if dt >= d:
                    factor_dt = d
            if factor_dt is None:
                factor = factor_dts[-1]            
            print dt,factor_dt,'\r',
            this_factors = bc_factors.xs(factor_dt,axis=1)
            factor_groups = this_factors.groupby(level=1).groups
            #--get the record from the bc dataframe
            this_record = df.xs(dt_str,axis=1,level=1)
            
            #--groupby and apply factors
            record_groups = this_record.groupby(level='zone',sort=False)                       
            applied = []
            for zone,group in record_groups:  
                if '_' in zone:
                    zone = zone.split('_')[0]                                                             
                group *= this_factors[factor_groups[zone]].values                                
                applied.append(group)
                #write_ascii_list(bc_type+'_'+dt_str+'.dat',group)
                                        
            #--write the list file
            applied = pandas.concat(applied)
            write_ascii_list('test\\'+bc_type+'_'+dt_str+'.dat',applied)           
        print ''

if __name__ == '__main__':
    apply()