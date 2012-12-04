import os
import numpy as np
import shapefile


#--dir of refs
adir = 'ref_new\\'

ref_files = os.listdir(adir)
fnames = []
refs = []
for rfile in ref_files:
    fnames.append(rfile.split('.')[0])
    refs.append(np.loadtxt(adir+rfile))

shapename = '..\\_gis\\shapes\\broward_grid_master'
shp = shapefile.Reader(shapename)
names = shapefile.get_fieldnames(shapename,ignorecase=True)
wr = shapefile.writer_like(shapename)
for f in fnames:
    wr.field(f,fieldType='N',size=50,decimal=10)

ridx,cidx = names.index('ROW'),names.index('COLUMN')

for i in range(shp.numRecords):
    shape = shp.shape(i)
    record = shp.record(i)
    r,c = record[ridx],record[cidx]
    print r,c
    for ref in refs:
        record.append(ref[r-1,c-1])    
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record(record)
wr.save('..\\_gis\\scratch\\broward_grid_layers')

        


