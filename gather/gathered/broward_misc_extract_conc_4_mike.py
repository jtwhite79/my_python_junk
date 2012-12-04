import os
import numpy as np
import pandas
from shapely.geometry import Point
import shapefile

airport_pt = Point([935003,632657])

select_radius = 5280.0 * 4.0

#--first get the nwis conc data
nwis_shapename = '..\\_gis\\scratch\\broward_nwis_sites_reclen_gw'
fields = shapefile.get_fieldnames(nwis_shapename)
conc_idx = fields.index('conc_len')
siteno_idx = fields.index('site_no')
sitename_idx = fields.index('station_nm')
hole_idx = fields.index('hole_depth')
wdepth_idx = fields.index('well_depth')
shp = shapefile.Reader(nwis_shapename)
shapes = shp.shapes()
records = shp.records()

wr = shapefile.writer_like(nwis_shapename)

#--only use those conc records that have > 0 length
sel_records,sel_points = [],[]
for shape,rec in zip(shapes,records):
    shp_pt = Point(shape.points[0])
    if (airport_pt.distance(shp_pt) < select_radius) and (int(rec[conc_idx]) > 0):
        sel_records.append(rec)
        sel_points.append(shape.points[0])
        wr.poly([shape.points],shapeType=shape.shapeType)
        wr.record(rec)
wr.save('..\\_gis\\scratch\\airport_nwis_sites')

#--build siteno,sitename tuples
sel_tups = []
for rec in sel_records:
    tup = (rec[siteno_idx],rec[sitename_idx])
    sel_tups.append(tup)

#--load the pandas dataframes for each type of data
#--and find the records for each selected record
dtypes = ['cond','chl','tds']
nwis_path = '..\\_nwis\\dataframes\\'
sel_dfs = {}
for dtype in dtypes:

    df = pandas.read_csv(nwis_path+dtype+'.csv',index_col=0)
    df_keys = list(df.keys())
    dfs = []
    series_dict = {}

    for tup in sel_tups:
        if tup[0] in df_keys:
            sub_df = df[tup[0]]
            sub_df.columns = ['datetime',tup[0]]
            series_dict[tup[0]] = sub_df.values
            dfs.append(sub_df)
        else:
            print 'record not found for dtype '+dtype+'  site no '+tup[0]           
    if len(dfs) > 0:
        df = pandas.DataFrame(series_dict,index=df.index)
        print df        
        sel_dfs[dtype] = df
        
#--write
f_out = open('airport_relative_conc.csv','w',0)
f_out.write('site,x,y,depth,source,datetime,value\n')


#--ftl saltdata 
salt_shapename = '..\\_gis\\shapes\\ftl_salt'
shapes,records = shapefile.load_as_dict(salt_shapename)

salt_dir = '..\\_ftl_salt\\dataframes\\'
salt_files = os.listdir(salt_dir)
#--load and write each salt file
for shape,rec in zip(shapes,records['Id']):
    salt_pt = Point(shape.points[0])
    if airport_pt.distance(salt_pt) < select_radius:
        df = pandas.read_csv(salt_dir+'SWMW-'+str(rec)+'_relconc.csv',index_col=0)
        line = ['SWMW-'+str(rec),str(shape.points[0][0]),str(shape.points[0][1]),None,'ftlsalt - regressed',None,None]
        for depth,record in df.iteritems():
            line[3] = str(depth)

            record = record.dropna()
            for dt,value in zip(record.index,record.values):
                line[-2] = str(dt)
                line[-1] = str(value)
                f_out.write(','.join(line)+'\n')





for dtype,df in sel_dfs.iteritems():
    for siteno,record in df.iteritems():                  
        #--find the record
        rec,pt = None,None
        for srec,sshp in zip(sel_records,sel_points):
            if srec[siteno_idx] == siteno:
                rec = srec
                pt = sshp
        if rec == None:
            raise Exception('record not found')
        x,y = pt
        name = rec[sitename_idx].replace(' ','')
        wd = rec[wdepth_idx]
        hd = rec[hole_idx]
        if hd == '':
            hd = wd
        if hd == '':
            hd = '-1.0e+30'

        line = [name,str(x),str(y),hd,None,None,None]
        if dtype == 'chl':
            line[-3] = 'nwis - native'
        else:
            line[-3] = 'nwis - regressed'
        record = record.dropna()
        for dt,val in zip(record.index,record.values):
            line[-2] = str(dt)
            line[-1] = str(val)
            f_out.write(','.join(line)+'\n')




