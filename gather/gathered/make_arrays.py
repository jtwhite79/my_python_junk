import sys
import numpy as np
import shapefile



nrow,ncol = 411,501

#--the index of the row and column in the dbf
idx_row,idx_col = 0,1

print 'loading grid polygons...'
file = 'shapes\\broward_grid_master'
shp_poly = shapefile.Reader(shapefile=file)
header = shp_poly.dbfHeader()
cells = shp_poly.shapes()
records = shp_poly.records()
print 'grid loaded'

#--get a list of numeric attributes
num_idx = []
for i,item in enumerate(header):
    if item[1] == 'N':
        num_idx.append(i)        

#--loop over each numeric field attribute and make an array
for i in num_idx:
    
    this_array_name = 'ref\\'+header[i][0]+'_array.ref'
    print 'building ',this_array_name
    #--determine the output format
    #--integers
    if header[i][-1] == 0:   
        ofmt = '4d'
    else:
        ofmt = '15.6e'
    #--create an 'empty' array
    this_array = np.zeros((nrow,ncol)) - 999
    
    #--loop over each cell
    for r in records:                
        this_row = r[idx_row]
        this_col = r[idx_col]
        this_val = r[i]
        
        this_array[this_row-1,this_col-1] = this_val        
    
    np.savetxt(this_array_name,this_array,fmt='%'+ofmt)
    
    
    
    