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

theis = np.loadtxt(r'..\..\GIS\shapes\refs\ConfigT_config_2916grid.ref')

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


wr.field('new_key',fieldType='N',size=50,decimal=10)
    
    
#--loop over each cell
for c in range(len(cells)):
    this_record = shp_poly.record(c)          
    print 'working on grid cell ',c+1,' of ',len(cells)
    
    this_row = this_record[idx_row]
    this_col = this_record[idx_col]
    
    this_record.append(theis[this_row-1,this_col-1])
    
    wr.poly([cells[c].points], shapeType=5)     
    wr.record(this_record)
    #break
   
wr.save(target='broward_grid_config')

      