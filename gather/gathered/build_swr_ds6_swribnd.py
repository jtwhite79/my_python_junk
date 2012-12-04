import sys
import math
import shapefile
import numpy as np

#--load the polylines
file = 'polylines_active'
shp = shapefile.Reader(shapefile=file)
nrec = shp.numRecords
records = shp.records()
dbf_header = shp.dbfHeader()

#for i,item in enumerate(dbf_header):
#    print i,item

inactive_basins = ['HILLSBORO CANAL']

#--the dbf attribute index of the reach identifier
name_idx = 1
reach_idx = 12
rg_idx = 13
col_idx = 10
row_idx = 11 
basin_idx = 20 
coastal_idx = 21
iswrbnd_idx = 18
ipri_idx = 19
coastal_stage = -0.5

#--get the ibound array
ibound = np.loadtxt('..\\500_grid_setup\\ref\\ibound.ref')

#--get constant stage reaches
cnt_reaches = []
cnt_stage = []
f = open('constant_stage_reaches.dat','r')
for line in f:    
    raw = line.strip().split()
    if not raw[0].startswith('#'):
        cnt_reaches.append(int(raw[0]))    
        cnt_stage.append(float(raw[1]))

#--now find constant stage reach groups
cnt_rg = []
cnt_rg_stage = []
for idx,rec in enumerate(records):
    reach = rec[reach_idx]
    if reach in cnt_reaches:
        rg = rec[rg_idx]
        if rg not in cnt_rg:
            cnt_rg.append(rg)            
            cnt_rg_stage.append(cnt_stage[cnt_reaches.index(reach)])            

#--now find inactive reach groups - if any reach is in an inactive cell, the entire reachgrp is inactive
inact_rg = []
for idx,rec in enumerate(records):
    reach = rec[reach_idx]
    row = rec[row_idx]
    col = rec[col_idx]
    
    ibnd = ibound[row-1,col-1]        
    if ibnd == 0:
        rg = rec[rg_idx]
        if rg not in inact_rg:
            inact_rg.append(rg)


#--set the writer instance
#wr = shapefile.Writer()
#for item in dbf_header:
#    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
#wr.field('iswrbnd_new',fieldType='N',size=5,decimal=0) 

f_out = open('swr_ds6.dat','w')
for idx,rec in enumerate(records):       
    reach = rec[reach_idx]
    rg = rec[rg_idx]
    name = rec[name_idx]
    row = rec[row_idx]
    col = rec[col_idx]
    coastal = rec[coastal_idx]     
    basin = rec[basin_idx]
    iswrbnd = rec[iswrbnd_idx]    
    iprimary = rec[ipri_idx]    
    
    #--turn on the primary system
    if basin in inactive_basins:# and iprimary == 0:
        iswrbnd = 0
    #--if constant stage reach
    if rg in cnt_rg:
        iswrbnd = -1            
    
    #--if this reach (group) is over an inactive MODFLOW cell
    elif rg in inact_rg:
        iswrbnd = 0
    
    if basin in inactive_basins:# and iprimary == 0:
        iswrbnd = 0
                 
        #print shp.shape(idx)
    #rec.append(iswrbnd)
    #rec.append(iprimary)
    #wr.poly(parts=[shp.shape(idx).points],shapeType=3)
    #wr.record(rec)
        #print name
    f_out.write(' {0:10.0f} {1:10.0f}  # {2:10.0f}\n'.format(reach,iswrbnd,rg))       
    
f_out.close()  


#wr.save('')


    