import sys
import os
import numpy as np
import shapefile

nrow,ncol = 384,369



#--a list of point shapes to process
#shapefile_names = ['paspts_100_SpatialJoin']
shapefile_names = []

shape_dir = '.\\'
files = os.listdir(shape_dir)
for f in files:
    if f.endswith('shp') and 'SpatialJoin' in f and 'grid_copy' not in f:
        shapefile_names.append(shape_dir+f)
        print f
#print shapefile_names
#sys.exit()


#--a total array - not expecting a rounding errors given small magnitude
total = np.zeros((nrow,ncol))

#--a counter array 
counter = np.zeros_like(total)

exceptions = []

for shpfile_name in shapefile_names:
    
    shp = shapefile.Reader(shpfile_name)
    
    print 'processing shapefile ',shpfile_name,' with ',shp.numRecords,' points'
    
    #--find the row,column,grid_code index in the DBF
    header = shp.dbfHeader()
    row_idx,col_idx,grid_idx = None,None,None
    for i,item in enumerate(header):
        #if item[0].upper() == 'ROW':
        if 'ROW' in item[0].upper():
                    row_idx = i
        #elif item[0].upper() == 'COLUMN':
        elif 'COLUMN' in item[0].upper():
        	col_idx = i     
        #elif item[0].upper() == 'GRID_CODE':
        elif 'GRID_CODE' in item[0]:
            grid_idx = i                   
    
    #-- some error checking
    if row_idx == None:
        raise IndexError,'row attribute not found in dbf header'+\
                         'for shapefile ',shpfile_name
    if col_idx == None:
        raise IndexError,'column attribute not found in dbf header'+\
                         'for shapefile '+shpfile_name
    if grid_idx == None:
        raise IndexError,'grid_code attribute not found in dbf header'+\
                         'for shapefile '+shpfile_name                                                                           
    ##--get the dbf records for this shapefile
    #records = shp.records()
    
    
    
    #--loop over record and add the elev value to total and count it
    #for r in records:
    for irec in range(shp.numRecords)
        r = shp.record(irec)
        row = r[row_idx]
        col = r[col_idx]
        elev = float(r[grid_idx])
        try:
            total[row-1,col-1] += elev
            counter[row-1,col-1] += 1
        except:
            print elev
            #sys.exit()
            exceptions.append([shpfile_name,elev])
    #break  


#--check to make sure every model cell has atleast one value
#for r in range(nrow):
#    for c in range(ncol):
#        if counter[r,c] == 0:
#            print 'no points in model cell (r,c)',r+1,c+1        
#
#--calc average elevation
elevation = np.zeros_like(total)
for i in range(nrow):
    for j in range(ncol):
        if counter[i,j] != 0:
            elevation[i,j] = (total[i,j] / counter[i,j])
elevation = np.round(elevation,decimals=6)

#--save the arrays
np.savetxt('avg_elevation.ref',elevation,fmt='%15.6e')
np.savetxt('total.ref',total,fmt='%15.6e')
np.savetxt('counter.ref',counter,fmt='%3.0f')
    
#--for error checking, load the grid shape and add the elevation to it
shp = shapefile.Reader('grid_copy')
cells = shp.shapes()
records = shp.records()
header = shp.dbfHeader()

wr = shapefile.Writer()
for item in header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr.field('elevation',fieldType='N',size=15,decimal=4)
wr.field('total',fieldType='N',size=25,decimal=6)
wr.field('count',fieldType='N',size=25,decimal=6)

for r,c in zip(records,cells):
    row = r[0]
    col = r[1]
    this_elev = elevation[row-1,col-1]
    this_total = total[row-1,col-1]
    this_count = counter[row-1,col-1]
    r.append(this_elev)
    r.append(this_total)
    r.append(this_count)
    wr.poly(parts=[c.points],shapeType=5)
    wr.record(r)
wr.save('elevation')    

for e in exceptions:
    print e[0],e[1]    