import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas

'''builds ghb stage and conductance dataframes and equivalent template dataframes
'''

def load_ghb_list(filename):
    f = open(filename,'r')
    lrc_tups,stage,cond,gtype = [],[],[],[]
    stage_dict,cond_dict,gtype_dict = {},{},{}
    for line in f:
        raw = line.strip().split()
        l = int(raw[0])
        r = int(raw[1])
        c = int(raw[2])
        stg = float(raw[3])
        cnd = float(raw[4])
        typ = int(raw[-1].replace('#',''))
        lrc = (l,r,c,typ)
        lrc_tups.append(lrc)
        #stage.append(stg)
        #cond.append(cnd)
        #gtype.append(typ)
        stage_dict[lrc] = stg
        cond_dict[lrc] = cnd
        gtype_dict[lrc] = typ
    return lrc_tups,stage_dict,cond_dict,gtype_dict


ghb_dirs = ['bro.02\\calibration\\flowlist\\']#,'ghb_cal_seawat':'bro.02\\calibration\\seawatlist\\'}
ghb_prefix = 'ghb'
date_fmt = '%Y%m%d'
start = datetime(year=1950,month=1,day=1)
end  = datetime(year=2112,month=5,day=31)
step = relativedelta(years=10)


unique_gtypes = []
for ghb_dir in ghb_dirs:
    df_name = 'ghb_dfs\\'+ghb_dir.replace('\\','_')[:-1]
    print 'building ',df_name
    files = os.listdir(ghb_dir)
    ghb_files,date_index = [],[]
    for f in files:
        if ghb_prefix in f:
            dt = datetime.strptime(f.split('.')[0].split('_')[1],date_fmt)
            ghb_files.append(f)
            date_index.append(dt)
            #break

    stage_dfs,cond_dfs,gtype_dfs = [],[],[]
    for dt,ghb_file in zip(date_index,ghb_files):
        print dt,'\r',      
        lrc_tups,stage_dict,cond_dict,gtype_dict = load_ghb_list(ghb_dir+ghb_file)
        stage_df = pandas.DataFrame(stage_dict,index=[dt])
        stage_dfs.append(stage_df)
        cond_df = pandas.DataFrame(cond_dict,index=[dt])
        cond_dfs.append(cond_df)
        gtype_df = pandas.DataFrame(gtype_dict,index=[dt])
        gtype_dfs.append(gtype_df)  
        
    print '  -  concat-ing stage dataframes...'
    stage_df = pandas.concat(stage_dfs,axis=0)   
    stage_df.to_csv(df_name+'-stage.csv',sep='|',index_label='datetime')

    print '  -  concat-ing cond dataframes...'
    cond_df = pandas.concat(cond_dfs,axis=0)    
    cond_df.to_csv(df_name+'-cond.csv',sep='|',index_label='datetime')
    print '  -  concat-ing zone dataframes...'
    gtype_df = pandas.concat(gtype_dfs,axis=0)    
    gtype_df.to_csv(df_name+'-zone.csv',sep='|',index_label='datetime')
    vals = gtype_df.ix[0].value_counts()
    for val,count in vals.iteritems():
        if val not in unique_gtypes:
            unique_gtypes.append(val)
 
tpl_dfs,in_dfs = [],[]
dtypes = ['cond','stage','conc']
for dtype in dtypes:
    pnames,dts,utypes = [],[],[]
    print dtype
    i,s = 1,start
    while s < end:
        for utype in unique_gtypes:
            #pname = utype.split()[0]+'_'+dtype+'_'+str(i)                    
            pname = '{0:03.0f}_{1:s}_{2:03.0f}'.format(int(utype),dtype,i)
            pstr = '~{0:25s}~'.format(pname)
            pnames.append(pstr)
            dts.append(s)
            utypes.append(utype)           
        s += step         
        i += 1
    df = pandas.DataFrame({dtype:pnames,'zone':utypes,'datetime':dts})
    tpl_dfs.append(df)
       
tpl_df = tpl_dfs[0]
for df in tpl_dfs[1:]:
    tpl_df = tpl_df.merge(df,left_on=('datetime','zone'),right_on=('datetime','zone'))
#print tpl_df.index.get_level_values(0)
tpl_df.index = tpl_df['datetime']
tpl_df.pop('datetime')
tpl_df.to_csv('tpl\\ghb.tpl',sep='|',index_label=('datetime','zone'))
#--write a generic infile df for testing
data = np.arange(0,len(dts))
for dtype in dtypes:
    tpl_df[dtype] = data
tpl_df.to_csv('par\\ghb.csv',sep='|',index_label='datetime')