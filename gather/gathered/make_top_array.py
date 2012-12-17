import sys
import numpy as np
import shapefile



nrow,ncol = 383,262

#--the index of the row and column in the dbf
idx_row,idx_col = 0,1

print 'loading grid polygons...'
file = 'shapes\\elevation4'
shp_poly = shapefile.Reader(shapefile=file)
header = shp_poly.dbfHeader()
cells = shp_poly.shapes()
records = shp_poly.records()
elev_idx = 5

top_array = np.zeros((nrow,ncol))
    
name = 'top_array.dat'

#--loop over each cell
for r in records:                
    this_row = r[idx_row]
    this_col = r[idx_col]
    this_val = r[elev_idx]    
    top_array[this_row-1,this_col-1] = this_val        

np.savetxt(name,top_array,fmt='%15.6e')

    
    
    