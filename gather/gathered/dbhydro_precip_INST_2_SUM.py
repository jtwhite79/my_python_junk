import os
import pandas
import dbhydro_util



#--load the record for each valid dbkey
data_dir = 'RAIN\\RAIN\\'
data_files = os.listdir(data_dir)
rain_files = []
rain_existing_dbkeys = []

for df in data_files:
    df_dict = dbhydro_util.load_header(data_dir+df)
    fname_dict = dbhydro_util.parse_fname(data_dir+df)    
    if df_dict['FQ'] == 'BK':
        dbhydro_util.interp_precip_pandas(data_dir+df)        
        break