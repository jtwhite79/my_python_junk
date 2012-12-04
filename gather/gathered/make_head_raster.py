import sys
import calendar
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au




nrow,ncol,nlay = 411,501,6
delr,delc = 500,500
offset = [728600.0,577350.0,0.0]
results = 'results\\'
nreach = 2400

day_2_sec = 1.0/86400.0


shape_dir = 'shapes\\'


  
#sys.exit()
  
#--heads
ibound = np.loadtxt('ref\ibound.ref')


#--loop over each month, using the last day in the month
tot_days = 0
for m in range(1,13):
     
    days = calendar.mdays[m]
    tot_days += days
    
    hds_handle = mfb.MODFLOW_Head(nlay,nrow,ncol,results+'bro_6lay.hds')
    totim,kstp,kper,h,success = hds_handle.get_record(tot_days)
           
    
    print 'day',tot_days,' processing for month ',m
    for l in range(nlay):
        
        this_head = h[l,:,:]        
        this_head[np.where(ibound==0)] = -9999.0
                     
        au.ref2grd('shapes\\head_layer'+str(l+1)+'_month'+str(m)+'.txt',\
                   h[l,:,:],nrow,ncol,offset,500.0)        
