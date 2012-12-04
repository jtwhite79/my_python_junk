import sys
import numpy as np
import shapefile


nrow,ncol,nlay = 411,501,6 

#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 4

#--load the ibound
ibound = (np.loadtxt('..\\500_grid_setup\\ref\ibound.ref'))
print ibound.max()
#sys.exit()

#--get the grid polygons
print 'loading grid polygons...'
file = 'broward_grid'
shp_poly = shapefile.Reader(shapefile=file)
dbf_header = shp_poly.dbfHeader()
cells = shp_poly.shapes()
print 'grid loaded'



#--instance of the writer class
wr = shapefile.Writer()
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])

wr.field('ibound',fieldType='N',size=10,decimal=0)


#--loop over each cell
for c in range(len(cells)):
    this_record = shp_poly.record(c)  
    #print this_record
    #break
    print 'working on grid cell ',c+1,' of ',len(cells)
    this_row = this_record[idx_row]
    this_col = this_record[idx_col]
    this_ibound = ibound[this_row-1,this_col-1]
    this_record.append(this_ibound)
    wr.poly(parts=[cells[c].points], shapeType=5)       
    wr.record(this_record)   
      
wr.save('broward_grid_ibound')