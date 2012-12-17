import sys
import math
import re
import shapefile


file = 'shapes\\polylines'
reach_shp = shapefile.Reader(shapefile=file)

r_shapes = reach_shp.shapes()
r_recs = reach_shp.records()
dbf_header = reach_shp.dbfHeader()
#--tolerance distance for making a connection
tol = 1.0

#--the dbf attribute index of the reach identifier
col_re = re.compile('column',re.IGNORECASE)
row_re = re.compile('row',re.IGNORECASE)
col_idx = None
row_idx = None

for i,item in enumerate(dbf_header):
    if col_re.search(item[0]) != None:
        col_idx = i
    elif row_re.search(item[0]) != None:
        row_idx = i        

#--build a list of rows and cols for faster searching
rows,cols = [],[]
for r in r_recs:
    rows.append(r[row_idx])
    cols.append(r[col_idx])


#--set the writer instance
wr = shapefile.Writer()
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])

wr.field('elevation',fieldType='N',size=30,decimal=5)

#--load the model cells
file = 'shapes\\elevation4'
elev_shp = shapefile.Reader(shapefile=file)

e_shapes = elev_shp.shapes()
e_recs = elev_shp.records()
dbf_header = elev_shp.dbfHeader()
elev_idx = 5
erow_idx = 0
ecol_idx = 1 

r_count = 0
for es,er in zip(e_shapes,e_recs):
    this_row = er[erow_idx]
    this_col = er[ecol_idx]  
    if this_row in rows and this_col in cols:
        for rs,rr in zip(r_shapes,r_recs):
            if rr[row_idx] == this_row and rr[col_idx] == this_col:
                this_elev = er[elev_idx]
                rr.append(this_elev)
                wr.poly(parts=[rs.points], shapeType=3)       
                wr.record(rr)   
                r_count += 1
                print r_count, 'of ',len(r_shapes)
                
                                         
 
wr.save(target='shapes\\polylines_elev')
    