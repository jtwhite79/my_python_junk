#--to read and process the ts_listing.csv, which
#--contains all of the dbhydro records for the
#--model domain area.  It contains duplicates,
#--those get filtered out here.

import numpy as np
import shapefile

fname = 'ts_listing.csv'
f = open(fname,'r')
header = f.readline().strip().split(',')

#--create a shapefile writer instance
wr = shapefile.Writer()
for h in header:
    wr.field(h,fieldType='C',size=50)

x_idx = header.index('X COORD')
y_idx = header.index('Y COORD')

for line in f:
    raw = line.strip().split(',')
    x,y = float(raw[x_idx]),float(raw[y_idx])
    wr.poly([[[x,y]]],shapeType=1)
    wr.record(raw)
wr.save('..\\_gis\\shapes\\dbhydro_sites')    
    

