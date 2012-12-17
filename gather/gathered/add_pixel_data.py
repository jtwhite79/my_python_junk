import os
import re
import numpy as np
import shapefile

data = np.loadtxt('tsala_et_avg_2000-2008.txt',skiprows=1)
attribute_name = '10_yr_pet'
           

#--load the grid
shp = shapefile.Reader('shapes\\tsala_pixels')
cells = shp.shapes()
records = shp.records()
header = shp.dbfHeader()

wr = shapefile.Writer()
for item in header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr.field(attribute_name,fieldType='N',size=50,decimal=6)


for r,c in zip(records,cells):
    pixel = float(r[0])
    print pixel,data[0]  
    value = data[np.where(data[:,0]==pixel),1][0][0]
    print value
    r.append(value)    
    wr.poly(parts=[c.points],shapeType=5)
    wr.record(r)
wr.save('shapes\\test')    



    