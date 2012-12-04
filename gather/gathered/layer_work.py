import sys
import os
import math
import numpy as np
import shapefile
import arrayUtil as au

def dist(point1,point2):
    xx = (point1[0] - point2[0])**2
    yy = (point1[1] - point2[1])**2
    return math.sqrt(xx+yy)


def get_cent_of_cell(points):
    xmin,xmax = 1.0e+20,-1.0e+20
    ymin,ymax = 1.0e+20,-1.0e+20
    for p in points:
        if p[0] < xmin:
            xmin = p[0]
        if p[0] > xmax:
            xmax = p[0]
        if p[1] < ymin:
            ymin = p[1]
        if p[1] > ymax:
            ymax = p[1]
    #print xmin,xmax,ymin,ymax
    x = (xmin+xmax) / 2.0
    y = (ymin+ymax) / 2.0
    return [x,y]
    

#--search radius 
tol = 350.0


#--index of row and col values in the grid shapefile
idx_row = 0
idx_col = 1
idx_num = 3




top_sm = np.loadtxt('ref\\top_filter_20_edge.ref')

order = {'h':1,'q5':2,'q4':3,'q3':4,'q2':5,'q1':6,'t2':7,'t1':8}
names = ['top']
for o in range(8):
    names.append('')


dir = 'org\\'
files = os.listdir(dir)
nrow,ncol = 411,501

master = np.zeros((9,nrow,ncol)) - 999.9
master[0] = top_sm

for f in files:   
    nrow1,ncol1,offset,gridDim,noData,array = au.loadgrdfromfile(dir+f)   
    print f,nrow1,ncol1
    temp = np.zeros((nrow,ncol)) - 999.9
    temp[:,:ncol1] = array 
    tile = array[:,-1]
    for c in range(ncol-ncol1):
        tile = np.vstack((tile,array[:,-1])) 
    tile = tile.transpose()    
    temp[:,ncol1-1:] = tile        
    np.savetxt(f.split('.')[0]+'_thk.ref',temp,fmt='%15.6e')           
    try:
        master[order[f.split('.')[0]]] = temp
        names[order[f.split('.')[0]]] =  f.split('.')[0]
    except:
        print 'no key for: ',f


elev_master = np.zeros_like(master) - 1.0e+20
elev_master[0] = top_sm
this_elev = top_sm
for m in range(1,master.shape[0]):
    this_elev -= master[m]            
    elev_master[m] = this_elev
    np.savetxt('bot_'+names[m]+'.ref',this_elev,fmt='%15.6e')
    #au.plotArray(this_elev,500,500,output=f.split('.')[0]+'.png') 
    
    
##--get the grid polygons
#print 'loading grid polygons...'
#file = '..\\shapes\\broward_grid'
#shp_poly = shapefile.Reader(shapefile=file)
#cells = shp_poly.shapes()
#print 'grid loaded'
#
#
##--set the writer instance
#wr = shapefile.Writer()
#wr.field('row',fieldType='N',size=20)
#wr.field('col',fieldType='N',size=20)
#wr.field('cellnum',fieldType='N',size=20)
#wr.field('bot0_top',fieldType='N',size=100,decimal=10)
#wr.field('bot0_top_sm',fieldType='N',size=100,decimal=10)
#wr.field('bot1_h',fieldType='N',size=100,decimal=10)
#wr.field('bot2_q5',fieldType='N',size=100,decimal=10)
#wr.field('bot3_q4',fieldType='N',size=100,decimal=10)
#wr.field('bot4_q3',fieldType='N',size=100,decimal=10)
#wr.field('bot5_q2',fieldType='N',size=100,decimal=10)
#wr.field('bot6_q1',fieldType='N',size=100,decimal=10)
#wr.field('bot7_t3',fieldType='N',size=100,decimal=10)
#wr.field('bot8_t2',fieldType='N',size=100,decimal=10)
#wr.field('bot9_t1',fieldType='N',size=100,decimal=10)
#
#
#print master.shape
#
#
##--loop over each cell, looking for elev points within the tol distance
#for c in range(len(cells)):
#    this_record = shp_poly.record(c)  
#    this_row,this_col = this_record[idx_row],this_record[idx_col]
#    this_cellnum = this_record[idx_num]
#    print 'working on grid cell ',c+1,' of ',len(cells)
#    print '  row col',this_row,this_col    
#    elev = master[:,this_row-1,this_col-1]       
#    wr.poly(parts=[cells[c].points], shapeType=5)   
#    wr.record(this_row,this_col,this_cellnum,elev[0],elev[1],elev[2],elev[3],elev[4],\
#              elev[5],elev[6],elev[7],elev[8],elev[9],elev[10])
#    
#    
#wr.save(target='broward_grid_layers')           
