import sys
import numpy as np
import shapefile

import bro

col_name = 'ibound_CS'
grid_shapename = '..\\..\\_gis\\shapes\\broward_grid_master'
shape = shapefile.Reader(grid_shapename)
fieldnames = shapefile.get_fieldnames(grid_shapename)
v_idx = fieldnames.index(col_name)
r_idx,c_idx = fieldnames.index('row'),fieldnames.index('column')
arr = np.zeros((bro.nrow,bro.ncol)) - 1.0e+10
for i in range(shape.numRecords):
    rec = shape.record(i)
    r,c = rec[r_idx],rec[c_idx]
    val = rec[v_idx]
    arr[r-1,c-1] = val
np.savetxt('ibound_CS.ref',arr,fmt=' %3.0f')

