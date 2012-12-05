import os
import pandas
import shapefile
import pestUtil as pu


#--get a list of site that are within the broward domain
shape_name = '..\\_gis\\scratch\\broward_nwis_gw_conc_depth'
records = shapefile.load_as_dict(shape_name,loadShapes=False)
sitenos = records['site_no']
dir_dict = {'chl':'smp_rel_conc_chl\\','cond':'smp_rel_conc_regressed\\','tds':'smp_rel_conc_tds\\'}
df_dict = {}
for dtype,smp_dir in dir_dict.iteritems():
    files = os.listdir(smp_dir)
    dfs = []
    for f in files:
        
        raw = f.split('.')
        siteno,sitename = raw[1],raw[2]
        if siteno in sitenos:
            print dtype,f
            smp = pu.smp(smp_dir+f,load=True,pandas=True)
            df = smp.records
            df[siteno] = df['site']
            df.pop('site')
            dfs.append(df)
        
    df = pandas.concat(dfs,axis=1)    
    df.to_csv('dataframes\\'+dtype+'.csv',index_label='datetime')