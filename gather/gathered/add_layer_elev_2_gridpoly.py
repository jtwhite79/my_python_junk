import os
import sys
import numpy as np
import shapefile


#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 3
idx_ibnd = 5
idx_icbnd = 6


#--load elev arrays
dir = '..\\ascii_layer_work_oldlaptop\\ref\\'
elev_files = os.listdir(dir)
elev_arrays = []
for e in elev_files:
    this_array = np.loadtxt(dir+e)
    elev_arrays.append(this_array)


#--get the grid polygons
print 'loading grid polygons...'
file = 'broward_grid_ibound'
shp_poly = shapefile.Reader(shapefile=file)
shp_header = shp_poly.dbfHeader()
cells = shp_poly.shapes()


#--set the writer instance
wr = shapefile.Writer()
#--add all existing grid attributes
for item in shp_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])


#--add a field for each elev array
for e in elev_files:
    this_name = e.split('.')[0]
    wr.field(this_name,fieldType='N',size=50,decimal=10)
    
    
#--loop over each cell
for c in range(len(cells)):
    this_record = shp_poly.record(c)          
    print 'working on grid cell ',c+1,' of ',len(cells)
    
    this_row = this_record[idx_row]
    this_col = this_record[idx_col]
    
    #--loop over the elev arrays and append
    #--the appropriate value to the record
    for e in elev_arrays:
        this_record.append(e[this_row-1,this_col-1])
    
    wr.poly([cells[c].points], shapeType=5)     
    wr.record(this_record)
    #break
   
wr.save(target='broward_grid_elev')

      