import os
import pandas
from fuzzywuzzy import fuzz
import shapefile
import dbhydro_util

#--load the attributes of the structure shapefile
shapename = '..\\_gis\\shapes\\sw_structures'
shapes,records = shapefile.load_as_dict(shapename)

#--get a list of stage records
stg_dir = 'SW\\STG\\'
stg_files = os.listdir(stg_dir)

#--build a list of unique station names
station_names = []
for f in stg_files:
    fdict = dbhydro_util.parse_fname(f)
    sname = fdict['STATION']
    if '_' in sname:
        sname = sname.split('_')[0]
    if sname not in station_names:
        station_names.append(sname)


#--find all the records for each structure
shape_dbhydro_names = []
for system,name in zip(records['system'],records['name']):
    if system == 1:
        #--strip out the hyphen
        name = name.replace('-','')

        
        match = None
        #--try for a staight-up match
        for i,station in enumerate(station_names):
                if fuzz.ratio(name,station) > 80:
                    match = station
                    break
        #--try for a subset match                
        if match == None:
            for i,station in enumerate(station_names):
                if fuzz.partial_ratio(name,station) > 80:
                    match = station
                    break
        #--try for a token sort match                
        if match == None:
            for i,station in enumerate(station_names):
                if fuzz.token_sort_ratio(name,station) > 80:
                    match = station
                    break
        if match == None:
            #raise LookupError('could not found a match for primary structure'+str(name))
            print 'could not found a match for primary structure'+str(name)
            shape_dbhydro_names.append('none')
        else:
            shape_dbhydro_names.append(match)
    else:
        shape_dbhydro_names.append('none')

wr = shapefile.writer_like(shapename)
wr.field('dbhydro',fieldType='C',size=50)
shp = shapefile.Reader(shapename)
records = shp.records()

for shape,record,dbhydro_name in zip(shapes,records,shape_dbhydro_names):
    wr.poly([shape.points],shapeType=shape.shapeType)
    record.append(dbhydro_name)
    wr.record(record)
wr.save('..\\_gis\\scratch\\sw_structures')
