import pandas

#--load the master site CSV file
master = pandas.read_csv('spreadsheet_data\\broward_sites_master.csv',sep='|',header=0)

#--stack the two daily value files
f_dir = 'spreadsheet_data\\'
files = ['broward_gw_dv_data-1.csv','broward_gw_dv_data-2.csv','broward_qw_result_data.csv','broward_wl_result_data.csv']


#--load each file as a dataframe, using a multiindex on site and data type
dfs = []
for f in files:
    df = pandas.read_csv(f_dir+f,sep='|',header=0,index_col=[1,3])
    dfs.append(df)

df = pandas.concat(dfs)
df.to_csv('nwis_raw.csv',index_label=['site_no','parm_nm'],sep='|')
#grouped = df.groupby(level=[0,1])
#for (site_no,param),group in grouped:
#    print site_no,param
#print
