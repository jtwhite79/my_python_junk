import sys
import calendar
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au


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
nreach = 2400

day_2_sec = 1.0/86400.0


shape_dir = 'shapes\\'

reach_shpfile = shape_dir+'polylines_SpatialJoin2'
reach_shp = shapefile.Reader(reach_shpfile)
num_records = reach_shp.numRecords
polylines = reach_shp.shapes()
polyline_header = reach_shp.dbfHeader()
rch_idx = 4
rchgrp_idx = 5
wr = shapefile.Writer()
for item in polyline_header:
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])


reach_key = load_reaches(nreach,'dis\\dataset.txt',skiprows=2,usecols=[0,2,4,5])
reach_array = np.zeros((nrow,ncol)) - 999.

ibnd = load_swr_ibnd('swr\\swr_ibnd.dat')
print ibnd[0]
#sys.exit()


swr_obj = mfb.SWR_Record(-1,results+'bro_7lay.rgp')
#totim,dt,kper,kstp,swrstp,success,compele = swr_obj.get_record()
ce_items = swr_obj.get_item_list()
#f_list = []
#print compele.shape
#sys.exit()

#for item in ce_items:
#    wr.field(item,fieldType='N',size=30,decimal=5)
#
##--loop over each polyline
#print 'processing reaches...'
#for p in range(num_records):
#    this_rec = reach_shp.record(p)
#    this_rchgrp = this_rec[rchgrp_idx]
#    this_reach = this_rec[rch_idx]
#    this_ibnd = ibnd[np.where(ibnd[:,0]==this_reach),1][0][0]        
#    if this_ibnd != 0:
#        this_results = compele[this_rchgrp-1]    
#        #print compele.shape,this_rchgrp,this_results[0]
#        #--stage
#        this_rec.append(this_results[0])
#        #--flows - convert from ft3/day to ft3/sec
#        for r in range(1,len(this_results)):
#            this_rec.append(this_results[r]*day_2_sec)
#        wr.poly([polylines[p].points],shapeType=3)
#        wr.record(this_rec)
#wr.save(shape_dir+'reach_results')
#print 'done' 
#
#swr_obj = mfb.SWR_Record(-1,results+'bro_1lay.rgp')

  
#sys.exit()
  
#--heads
ibound = np.loadtxt('ref\ibound.ref')

#print 'loading grid...'
#grid_shpfile = shape_dir+'broward_grid_elev'
#grid_shp = shapefile.Reader(grid_shpfile)
#cells = grid_shp.shapes()
#grid_header = grid_shp.dbfHeader()
#row_idx = 0
#col_idx = 1
#print 'done'
#

#--loop over each month, using the last day in the month
tot_days = 0
for m in range(1,13):
    #wr = shapefile.Writer()
    #for item in grid_header:
    #    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
    #wr.field('head_'+str(m),fieldType='N',size=30,decimal=5)  
    
    wrp = shapefile.Writer()
    for item in polyline_header:
        wrp.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])       
    
    for item in ce_items:                              
        wrp.field(item,fieldType='N',size=30,decimal=5) 
        #print item
       
    days = calendar.mdays[m]
    tot_days += days
    
    swr_obj = mfb.SWR_Record(-1,results+'bro_7lay.rgp')
    totim,dt,kper,kstp,swrstp,success,compele = swr_obj.get_record(tot_days)
    
    #hds_handle = mfb.MODFLOW_Head(1,nrow,ncol,results+'bro_1lay.hds')
    #totim,kstp,kper,h,success = hds_handle.get_record(tot_days)
    ##np.savetxt('init_heads.ref',h[0,:,:],fmt='%15.6e')
    #
    #print 'day',tot_days,' processing heads for month ',m
    #for c_idx in range(len(cells)):
    #    this_rec = grid_shp.record(c_idx)    
    #    this_row = this_rec[row_idx]
    #    this_col = this_rec[col_idx]
    #    this_ibound = ibound[this_row-1,this_col-1]
    #    if this_ibound != 0:
    #        this_head = h[0,this_row-1,this_col-1]
    #        this_rec.append(this_head)
    #        wr.poly([cells[c_idx].points],shapeType=5)
    #        #print this_rec
    #        wr.record(this_rec)
    #wr.save(shape_dir+'grid_heads_'+str(m))
    #print 'done'    
    #
    print 'day',tot_days,' processing reachs for month ',m
    for p in range(num_records):                                   
        this_rec = reach_shp.record(p)                             
        this_rchgrp = this_rec[rchgrp_idx]                         
        this_reach = this_rec[rch_idx]                             
        this_ibnd = ibnd[np.where(ibnd[:,0]==this_reach),1][0][0]  
        if this_ibnd != 0:                                         
            this_results = compele[this_rchgrp-1]                  
            #print compele.shape,this_rchgrp,this_results[0]       
            #--stage                                               
            this_rec.append(this_results[0])                       
            #--flows - convert from ft3/day to ft3/sec             
            #print len(this_rec)
            for r in range(1,len(this_results)):                   
                this_rec.append(this_results[r]*day_2_sec)         
            wrp.poly([polylines[p].points],shapeType=3)             
            wrp.record(this_rec)                                    
    wrp.save(shape_dir+'reach_results_'+str(m))



                    