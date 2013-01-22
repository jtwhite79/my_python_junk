import numpy as np
import shapefile

from simple import grid


shape_name = 'shapes\\simple_grid'
record = shapefile.load_as_dict(shape_name,loadShapes=False)
rows = record.pop('row')
cols = record.pop('column')

for pname,plist in record.iteritems():
    arr = np.zeros((grid.nrow,grid.ncol))
    for r,c,val in zip(rows,cols,plist):
        arr[r-1,c-1] = val
    np.savetxt('ref\\'+pname+'.ref',arr,fmt=' %15.6G')