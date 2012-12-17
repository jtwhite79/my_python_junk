import os
import re
import shapefile


shape_dir = 'shapes\\'
shapefile_names = ['FloralCity_outline_sp','hampton_outline_sp','hernando_outline_sp',\
                   'LittleHenderson_outline_sp','Spivey_outline_sp','Canals_primary_sp',\
                   'Canals_secondary_sp','river2']

wr = shapefile.Writer()
wr.field('name',fieldType='C',size=50)

re_name = re.compile('name',re.IGNORECASE)

for shpfile_name in shapefile_names:
    
    shp = shapefile.Reader(shape_dir+shpfile_name)    
    print 'processing shapefile ',shpfile_name,' with ',shp.numRecords,' points'
   
    #--look for name attribute
    name_idx = None
    header = shp.dbfHeader()
    for i,item in enumerate(header):
        if re_name.search(item[0]) != None:
            name_idx = i
    #if name_idx == None             
    
    lines = shp.shapes()    
    records = shp.records()
    for l,r in zip(lines,records):
        if name_idx != None:
            name = r[name_idx]
        else:
            name = shpfile_name
        wr.poly([l.points],shapeType=3)
        wr.record([name])
        
wr.save(shape_dir+'hydrography')    

    