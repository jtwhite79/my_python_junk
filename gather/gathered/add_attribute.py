import os
import re
import numpy as np
import shapefile

nrow,ncol = 383,262

#--name of points shapefile to attach to grid
shapefile_name = 'shapes\\trans4_pts_join'
#--10 character max
attribute_name = 'ufa_trans'

r_re = re.compile('row',re.IGNORECASE)
c_re = re.compile('column',re.IGNORECASE)
    
shp_pts = shapefile.Reader(shapefile_name)

print 'processing shapefile ',shapefile_name,' with ',shp_pts.numRecords,' points'

#--find the row,column,grid_code index in the DBF
header = shp_pts.dbfHeader()
row_idx,col_idx,grid_idx = None,None,None
for i,item in enumerate(header):
    #if item[0].upper() == 'ROW':
    #    row_idx = i
    #elif item[0].upper() == 'COLUMN':
    #    col_idx = i     
    #elif item[0].upper() == 'GRID_CODE':
    #    grid_idx = i                   
    if r_re.search(item[0]) != None:
        row_idx = i
    elif c_re.search(item[0]) != None:
        col_idx = i
    elif item[0].upper() == 'GRID_CODE':
        grid_idx = i
        
    
#-- some error checking
if row_idx == None:
    raise IndexError,'row attribute not found in dbf header'+\
                     'for shapefile ',shapefile_name
if col_idx == None:
    raise IndexError,'column attribute not found in dbf header'+\
                     'for shapefile ',shapefile_name
if grid_idx == None:
    raise IndexError,'grid_code attribute not found in dbf header'+\
                     'for shapefile ',shapefile_name                                                                           
#--get the dbf records for this shapefile
pts_records = shp_pts.records()

#--a total array - not expecting a rounding errors given small magnitude
total = np.zeros((nrow,ncol))

#--a counter array 
counter = np.zeros_like(total)

#--loop over each record
for r in pts_records:
        row = r[row_idx]
        col = r[col_idx]
        value = r[grid_idx]
        total[row-1,col-1] += value
        counter[row-1,col-1] += 1

               
#--calc average value in each cell
value_array = total / counter

#--try to fill in missing data by average from neighbors
for i in range(1,nrow-1):
    for j in range(1,ncol-1):
        if counter[i,j] == 0:
            avg = value_array[i-1,j] + value_array[i+1,j] + \
                  value_array[i,j+1] + value_array[i,j+1]
            avg /= 4.0
            value_array[i,j] = avg                  
            
           

#--load the grid
shp = shapefile.Reader('shapes\\elevation4')
cells = shp.shapes()
records = shp.records()
header = shp.dbfHeader()

wr = shapefile.Writer()
for item in header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr.field(attribute_name,fieldType='N',size=50,decimal=6)


for r,c in zip(records,cells):
    row = r[0]
    col = r[1]   
    value = value_array[row-1,col-1]
    r.append(value)    
    wr.poly(parts=[c.points],shapeType=5)
    wr.record(r)
wr.save('shapes\\test')    



    