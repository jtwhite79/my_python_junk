import os
import pandas
import shapefile
import dbhydro_util


df_dir = 'stage_dfs_navd\\'
smp_dir = 'stage_smp_navd\\'
ngvd_2_navd = -1.5
#--load the attributes of the structure shapefile
shapename = '..\\_gis\\shapes\\sw_structures'
records = shapefile.load_as_dict(shapename,attrib_name_list=['system','struct_num','dbhydro'],loadShapes=False)

#--get a list of stage records
stg_dir = 'SW\\STG\\'
stg_files = os.listdir(stg_dir)

#--build a list of station names
rec_attribs = []
for f in stg_files:
    fdict = dbhydro_util.parse_fname(f)    
    rec_attribs.append(fdict)

#--find all the records for each primary structure, headwater only
wl_stats = ['DA','BK','DWR','INST','FWM','MEAN']
for system,name in zip(records['system'],records['dbhydro']):
    if system == 1 and name != None:
        match_h,match_t = [],[]
        for i,rec in enumerate(rec_attribs):
            station = rec['STATION']
            if '_' in station:
                station = station.split('_')[0]
            if station.lower() == name.lower() and rec['STAT'] in wl_stats:
                if rec['STATION'].lower().endswith('h'):
                    match_h.append(rec)
                if rec['STATION'].lower().endswith('t'):
                    match_t.append(rec)
        #--headwater
        dfs = []
        for m in match_h:
            fname = stg_dir+dbhydro_util.build_fname(m)            
            if m['STAT'] != 'MEAN' or m['FREQUENCY'] != 'DA':            
                                
                if m['FREQUENCY'] == 'BK':
                    #print 'converting breakpoint data to daily average values'
                    #df = dbhydro_util.load_series(fname,aspandas=True)
                    #df_daily = dbhydro_util.make_daily_breakpoint(df)
                    #dfs.append(df_daily)    
                    pass
                else:
                    df = dbhydro_util.load_series(fname,aspandas=True)
                    df_daily = dbhydro_util.make_daily(df)
                    for site,series in df_daily.iteritems():
                        df_daily[site] += ngvd_2_navd
                    dfs.append(df_daily)
            else:
                df = dbhydro_util.load_series(fname,aspandas=True)
                for site,series in df.iteritems():
                        df[site] += ngvd_2_navd
                dbkey = df.columns.tolist()[0]
                #df[dbkey] = df[dbkey].interpolate()
                dfs.append(df)
                pass
        #--concat all of the dfs together as save for later
        if len(dfs) > 0:
            df = pandas.concat(dfs,axis=1)        
            df.to_csv(df_dir+name+'_h.csv',index_label='datetime')
        
            #--merge the dfs into a single record
            print len(dfs)
            df = dfs[0]
            df.columns = [name]
            for other in dfs[1:]:
                other.columns = [name]
                df = df.combine_first(other)
            #--interp to catch any missing days
            #df[name] = df[name].interpolate()
            df.to_csv(df_dir+name+'_h_merged.csv',index_label='datetime')                                                
            f = open(smp_dir+name+'_h.smp','w')
            for site,series in df.iteritems():
                for dt,val in zip(series.index,series.values):
                    f.write(name.ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 00:00:00 {0:15.6e}\n'.format(val))
                    pass
            f.close()

        else:
            #raise IndexError('no records found for structure'+str(name))
            print '-- NO RECORDS FOUND FOR STRUCTURE',name

        #--tailwater
        dfs = []
        for m in match_t:
            fname = stg_dir+dbhydro_util.build_fname(m)            
            if m['STAT'] != 'MEAN' or m['FREQUENCY'] != 'DA':            
                                
                if m['FREQUENCY'] == 'BK':
                    #print 'converting breakpoint data to daily average values'
                    #df = dbhydro_util.load_series(fname,aspandas=True)
                    #df_daily = dbhydro_util.make_daily_breakpoint(df)
                    #dfs.append(df_daily)
                    pass                    
                    
                else:
                    df = dbhydro_util.load_series(fname,aspandas=True)
                    df_daily = dbhydro_util.make_daily(df)
                    for site,series in df_daily.iteritems():
                        df_daily[site] += ngvd_2_navd
                    dfs.append(df_daily)
            else:
                df = dbhydro_util.load_series(fname,aspandas=True)
                for site,series in df.iteritems():
                    df[site] += ngvd_2_navd
                
                
                dfs.append(df)
                pass
        #--concat all of the dfs together as save for later
        if len(dfs) > 0:
            df = pandas.concat(dfs,axis=1)        
            df.to_csv(df_dir+name+'_t.csv',index_label='datetime')
        
            #--merge the dfs into a single record
            print len(dfs)
            df = dfs[0]
            df.columns = [name]
            for other in dfs[1:]:
                other.columns = [name]
                df = df.combine_first(other)
            #--interp to catch any missing days
            #df[name] = df[name].interpolate()
            df.to_csv(df_dir+name+'_t_merged.csv',index_label='datetime')                                                          
            f = open(smp_dir+name+'_t.smp','w')
            for site,series in df.iteritems():
                for dt,val in zip(series.index,series.values):
                    f.write(name.ljust(20)+' '+dt.strftime('%d/%m/%Y')+' 00:00:00 {0:15.6e}\n'.format(val))
                    pass
            f.close()
        else:
            #raise IndexError('no records found for structure'+str(name))
            print '-- NO RECORDS FOUND FOR STRUCTURE',name
