import sys
import math
import numpy as np
import shapefile

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)

def conn_2_string(conn):
    conn_str = ''
    for c in conn:
        conn_str += str(c) + ' '
    return conn_str


file = '500_grid_polylines'

shp = shapefile.Reader(shapefile=file)
#print shp.numRecords,shp.fields
lines = shp.shapes()


#--the dbf attribute index of the reach identifier
row_idx = 6
col_idx = 5
reach_idx = 7

icbnd = np.loadtxt('icbnd_layer1.ref')

coastal_conc = 1.0
inland_conc = 0.0

#--load the coastal source reaches
f = open('coastal_src_reaches.dat')
coastal_src_reaches = []
for line in f:
    coastal_src_reaches.append(int(line.strip()))
f.close()


for l_idx in range(len(lines)):    
    conc = inland_conc
    row = shp.record(l_idx)[row_idx]
    col = shp.record(l_idx)[col_idx]
    
    reach = shp.record(l_idx)[reach_idx]
    if src_reach in coastal_src_reaches and icbnd[row-1,col-1] != 0:
        conc = coastal_conc
    print reach,conc
    