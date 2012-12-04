import os
import sys
import re
import math
import shapefile

#poly_file = 'polylines_SpatialJoin2'
poly_file = '500grid_polylines'
poly_shp = shapefile.Reader(shapefile=poly_file)
num_poly_lines = poly_shp.numRecords
poly_lines = poly_shp.shapes()
poly_recs = poly_shp.records()
poly_header = poly_shp.dbfHeader()

#length = int(math.log10(len(poly_recs)))

r_idx = 7
rg_idx = 8
con_idx = 14

#--first get a list of rch groups with constant stage members
rg_const = []
for r in poly_recs:
    if r[con_idx] == 1:
        if r[rg_idx] not in rg_const:
            rg_const.append(r[rg_idx])


#--loop over each reach, writing stage and boundary files
stage = open('dataset14.dat','w')
bound = open('dataset6.dat','w')

s0 = 7.0
s1 = -0.5

for r in poly_recs:
    reach = r[r_idx]        
    rch_grp = r[rg_idx]
    const = r[con_idx]
    if rch_grp in rg_const:
        bound.write('{0:10.0f} {1:10.0f}  # {2:10.0f}\n'.format(reach,-1,rch_grp))
        stage.write('{0:10.0f} {1:10.3e}  # {2:10.0f}\n'.format(reach,s1,rch_grp))
    else:
        bound.write('{0:10.0f} {1:10.0f}  # {2:10.0f}\n'.format(reach,1,rch_grp))
        stage.write('{0:10.0f} {1:10.3e}  # {2:10.0f}\n'.format(reach,s0,rch_grp))
stage.close()
bound.close()        
