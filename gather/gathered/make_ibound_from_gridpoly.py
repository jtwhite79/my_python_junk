import sys
import numpy as np
import shapefile


#nrow,ncol = 822,1002
nrow,ncol,nlay = 411,501,6

#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 3
idx_ibnd = 8
idx_icbnd = 7

ibound = np.zeros((nrow,ncol)) - 999.9
icbnd  = np.zeros((nrow,ncol)) - 999.9
#--get the grid polygons
print 'loading grid polygons...'
file = 'broward_grid_ibound'
shp_poly = shapefile.Reader(shapefile=file)
cells = shp_poly.shapes()
records = shp_poly.records()
print 'grid loaded'


#--loop over each cell
for c,r in zip(cells,records):
    this_record = r
    #print this_record
    #break
    #if c % 100 == 0:
    #    print 'working on grid cell ',c+1,' of ',len(cells)
    this_row = this_record[idx_row]
    this_col = this_record[idx_col]
    this_ibnd = this_record[idx_ibnd]
    this_icbnd = this_record[idx_icbnd]
    ibound[this_row-1,this_col-1] = this_ibnd
    icbnd[this_row-1,this_col-1] = this_icbnd
    if this_col % 100 == 0:
        print 'working on grid column ',this_col+1,' of ',ncol
np.savetxt('ibound.ref',ibound,fmt='%1.0f')
for l in range(nlay):
    np.savetxt('icbnd_layer'+str(l+1)+'.ref',icbnd,fmt='%3.0f')
      
