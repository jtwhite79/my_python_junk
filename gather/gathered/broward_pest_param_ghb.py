import os
from datetime import datetime
import numpy as np
import pandas

def apply_ghb_factors_cal():
    #--load the ghb parameter dataframe
    base_param_df = pandas.read_csv('par\\ghb_cal.csv',sep='|',index_col='datetime',parse_dates=True)
    unique_zones = base_param_df['zone'].value_counts()
    nan_dict = {}
    for key in base_param_df.keys():
        nan_dict[key] = np.NaN

    for zone,count in unique_zones.iteritems():                                    
        zone_param_df = base_param_df[base_param_df['zone']==zone]
        zone_mult_df = pandas.DataFrame(nan_dict,index=df.index)                    
        zone_mult_df = zone_mult_df.combine_first(zone_param_df)            
        zone_mult_df = zone_mult_df[df.index[0]:df.index[-1]]           
        zone_mult_df = zone_mult_df.fillna(method='bfill')       
        zone_mult_df = zone_mult_df.fillna(method='ffill')        

    
    ##--get a list of dataframes
    #df_dir = 'ghb_dfs\\'
    #df_files = os.listdir(df_dir)
    #for df_file in df_files:
    #    dtype = df_file.split('-')[1].split('.')[0]
    #    list_outdir = df_file.split('-')[0].replace('_','\\') + '\\'        
    #    df = pandas.read_csv(df_dir+df_file,sep='|',index_col='datetime',parse_dates=True)    
    #    #df = pandas.read_csv('test.csv',sep='|',index_col='datetime',parse_dates=True)    
               
    #    #--cast header into multiindex
    #    str_mess = df.columns
    #    lay,row,col,zone = [],[],[],[]
    #    for string in str_mess:
    #        string = string.replace('(','').replace(')','').replace('\'','')
    #        raw = string.split(',')
    #        l = int(raw[0])
    #        r = int(raw[1])
    #        c = int(raw[2])
    #        z = int(raw[3])
    #        lay.append(l)
    #        row.append(r)
    #        col.append(c)
    #        zone.append(z)
    #    mi = pandas.MultiIndex.from_tuples(zip(lay,row,col,zone),names=('layer','row','column','zone'))      
    #    df.columns = mi
    #    post_dfs = []
    #    for zone,count in unique_zones.iteritems():                                   
    #        zone_df = df.xs(zone,level='zone',axis=1)            
    #        zone_param_df = base_param_df[base_param_df['zone']==zone]
    #        zone_mult_df = pandas.DataFrame(nan_dict,index=df.index)                    
    #        zone_mult_df = zone_mult_df.combine_first(zone_param_df)            
    #        zone_mult_df = zone_mult_df[df.index[0]:df.index[-1]]           
    #        zone_mult_df = zone_mult_df.fillna(method='bfill')       
    #        zone_mult_df = zone_mult_df.fillna(method='ffill')                  
    #        for col,series in zone_df.iteritems():
    #            #print zone,'prior',zone_df[col].values[0]
    #            zone_df[col] *= zone_mult_df[dtype]
    #            #print zone,'post',zone_df[col].values[0]               
    #        post_dfs.append(zone_df)
    #    post_df = pandas.concat(post_dfs,axis=1)                   
    #    post_df.to_csv('test.csv',sep='|')    
    #    break

        

if __name__ == '__main__':
    apply_ghb_factors_cal()

    

