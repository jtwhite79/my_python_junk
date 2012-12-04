import sys
import math
import shapefile
import numpy as np

#--load the polylines
file = 'polylines_active_basins'
shp = shapefile.Reader(shapefile=file)
nrec = shp.numRecords
records = shp.records()
dbf_header = shp.dbfHeader()

for i,item in enumerate(dbf_header):
    print i,item

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
f_out = open('swr_ds4a.dat','w')
f_out.write('#                                        LAY        ROW        COL\n')
f_out.write('#    IRCH4A IROUTETYPE     IRGNUM       KRCH       IRCH       JRCH           RLEN\n')
f_out2 = open('swr_ds4b.dat','w')
f_out2.write('#    IRCH4B      NCONN      ICONN(1)...ICONN(NCONN)\n')

for idx,rec in enumerate(records):       
    reach = rec[reach_idx]
    rg = rec[rg_idx]
    name = rec[name_idx]
    row = rec[row_idx]
    col = rec[col_idx]
    conn = rec[conn_idx].split()
    nconn = rec[nconn_idx]
    iroute = rec[iroute_idx]
    length = rec[length_idx]
    
   
    f_out.write(' {0:10.0f} {1:10.0f} {2:10.0f} {3:10.0f} {4:10.0f} {5:10.0f} {6:15.6e}\n' \
               .format(reach,iroute,rg,1,row,col,length))       
    f_out2.write(' {0:10.0f} {1:10.0f} '.format(reach,nconn))
    for c in conn:
        f_out2.write(' {0:10.0f}'.format(int(c)))           
    f_out2.write('\n')
f_out.close()  
f_out2.close()  
    