import math
import sys
import calendar
import numpy as np
from numpy import ma
import shapefile
import swr

def distance(point1,point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def load_reaches(nreach,file,skiprows=0,usecols=[0]):
    f = open(file,'r')
    for r in range(skiprows):
        f.readline()
    data = np.zeros(len(usecols))
    
    for line in f:
        this_line = line.strip().split()
        this_entry = []
        #print this_line
        for c in range(len(usecols)):
            this_entry.append(float(this_line[usecols[c]]))
        data = np.vstack((data,np.array(this_entry)))
        if data.shape[0] > nreach: break
    return np.delete(data,0,axis=0)


def load_swr_ibnd(file):
    irch = []
    ibnd = []
    f = open(file,'r')
    for line in f:
        if line[0] != '#' and line != '':
            raw = line.strip().split()
            irch.append(int(raw[0]))
            ibnd.append(int(raw[1]))
    f.close()
    return np.array([irch,ibnd]).transpose()



def save_stage(reach,rchgrp,stage,file='stage_out.dat'):
    assert len(reach) == len(stage)
    f = open(file,'w')
    for r in range(len(reach)):
        #print reach[r],stage[r]
        f.write('{0:10.0f} {2:15.6f}  # {1:1.0f} \n'.format(int(reach[r]),int(rchgrp[r]),float(stage[r])))
    f.close()
    return
    
   

nrow,ncol,nlay = 411,501,6
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]
results = 'results\\'
nreach = 10810

day_2_sec = 1.0/86400.0


shape_dir = 'shapes\\'
reach_shpfile = shape_dir+'polylines_active'
reach_shp = shapefile.Reader(reach_shpfile)
num_records = reach_shp.numRecords
polylines = reach_shp.shapes()
records = reach_shp.records()
polyline_header = reach_shp.dbfHeader()

rch_idx = 14
rchgrp_idx = 15


reach_key = load_reaches(nreach,'swr_full\\swr_ds4a.dat',skiprows=2,usecols=[0,2,4,5])
reach_array = np.zeros((nrow,ncol)) - 999.

swribnd = np.loadtxt('swr_full\\swr_ds6.dat',usecols=[0,1])


wr = shapefile.Writer()
wr.field('istrrch',fieldType='N',size=10,decimal=0)
wr.field('istrnum',fieldType='N',size=10,decimal=0)
wr.field('istrconn',fieldType='N',size=10,decimal=0)
wr.field('istrrch_rg',fieldType='N',size=10,decimal=0)
wr.field('istrcon_rg',fieldType='N',size=10,decimal=0)


#--load the structures
ds_13a = swr.ds_13a('swr_full\\swr_ds13a_w.dat')
ds_13a.load_structures()
s_count = 0
for s in ds_13a.structures:
    #--loop over each polyline
    istrrch = s['istrrch']
    istrconn = s['istrconn']
    istrnum = s['istrnum']
    ibnd_istrrch = swribnd[np.where(swribnd[:,0]==istrrch),1]
    ibnd_istrconn = swribnd[np.where(swribnd[:,0]==istrconn),1]
    if ibnd_istrrch != 0 and ibnd_istrconn != 0:
    #if True:
        #--get the points for the polylines of istrrch and istrconn
        istrrch_points = None
        istrconn_points = None
        istrrch_rg = None
        istrconn_rg = None
        for shp,rec in zip(polylines,records):    
            rchgrp = rec[rchgrp_idx]
            reach = rec[rch_idx]
            if reach == istrrch:
                istrrch_points = shp.points
                istrrch_rg = rchgrp
            elif reach == istrconn:
                istrconn_points = shp.points    
                istrconn_rg = rchgrp
        if istrconn_points == None or istrrch_points == None:
            raise IndexError,'reach not found: ',str(istrrch)+' '+str(istrconn)
        #--find the closest shared point between the two reaches
        min = 1.0e+32
        min_pt = None
        for pt in istrrch_points:
            for pt2 in istrconn_points:
                dist = distance(pt,pt2)
                if dist < min:
                    min = dist
                    min_pt = pt                   
        if min != 0.0:                                        
            print 'non-zero connection distance:',min
        attr = [istrrch,istrnum,istrconn,istrrch_rg,istrconn_rg]
        wr.poly([[min_pt]],shapeType=1)
        wr.record(attr)
        s_count += 1                        
    
wr.save(shape_dir+'structure_points')
print s_count,' structures processed'