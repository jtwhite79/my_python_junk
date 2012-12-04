import sys
import os
import math
import shapefile
import numpy as np


#--load each xsection and find the minimum
xsec_dir = '..\\MIKE_SHE_Baseline\\xsec\\'
xsec_files = os.listdir(xsec_dir)
xsec_min = []
for f in xsec_files:
    xsec = np.loadtxt(xsec_dir+f,skiprows=1)
    #print f,xsec[:,1].min()
    xsec_min.append(xsec[:,1].min())    
    #break
#sys.exit()            
    



#--load the polylines
file = 'polylines_active'
shp = shapefile.Reader(shapefile=file)
nrec = shp.numRecords
records = shp.records()
reaches = shp.shapes()
dbf_header = shp.dbfHeader()

#for i,item in enumerate(dbf_header):
#    print i,item

#active_basins = ['HILLSBORO CANAL']

#--the dbf attribute index of the reach identifier
name_idx = 1
reach_idx = 14
rg_idx = 27
col_idx = 12
row_idx = 13 
conn_idx = 16
nconn_idx = 17
length_idx = 19
iroute_idx = 26
up_xsec_idx = 4
dw_xsec_idx = 5

#--set the writer instance
wr = shapefile.Writer()
for item in dbf_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
wr.field('up_xsec_min',fieldType='N',size=20,decimal=5) 
wr.field('dw_xsec_min',fieldType='N',size=20,decimal=5)


for reach,rec in zip(reaches,records):
    up_xsec = rec[up_xsec_idx]
    dw_xsec = rec[dw_xsec_idx]
    up_min = xsec_min[xsec_files.index(up_xsec)]
    dw_min = xsec_min[xsec_files.index(dw_xsec)]
    rec.append(up_min)
    rec.append(dw_min)
    wr.poly([reach.points],shapeType=3)
    wr.record(rec)
    
wr.save('polylines_geo')    