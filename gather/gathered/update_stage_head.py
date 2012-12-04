import sys
import shutil
import numpy as np
from numpy import ma
import pylab
import MFBinaryClass as mfb
import shapefile
import arrayUtil as au
import bro_info as bi


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

def save_stage(reach,rchgrp,stage,file='swr_full\\swr_ds14a.dat'):
    assert len(reach) == len(stage)
    f = open(file,'w')
    for r in range(len(reach)):
        #print reach[r],stage[r]
        f.write('{0:10.0f} {2:15.6f}  # {1:1.0f} \n'.format(int(reach[r]),float(stage[r]),int(rchgrp[r])))
    f.close()
    return
    
   
results = 'results\\'

reach_key = load_reaches(bi.nreach,'swr_full\\swr_ds4a.dat',skiprows=2,usecols=[0,2,4,5])
reach_array = np.zeros((bi.nrow,bi.ncol)) - 999.


#--use the iswrbnd to mask the inactive reaches
iswrbnd = np.loadtxt('swr_full\\swr_ds6.dat')



#--first make a backup copy
for l in range(bi.nlay):
    shutil.copy('ref\\init_heads_'+str(l+1)+'.ref','ref\\init_heads_'+str(l+1)+'_bak.ref')
shutil.copy('swr_full\\swr_ds14a.dat','swr_full\\swr_ds_14a_bak.dat')    
                     
          
#--heads
top = np.loadtxt('ref\\top_filter_20_edge.ref')
hds_handle = mfb.MODFLOW_Head(bi.nlay,bi.nrow,bi.ncol,results+'bro_6lay.hds')
try:
    totim,kstp,kper,h,success = hds_handle.get_record(float(sys.argv[1]))
    print 'heads from totim ',sys.argv[1],' read'
except:
    totim,kstp,kper,h,success = hds_handle.get_record()        
for l in range(bi.nlay):
    np.savetxt('ref\\init_heads_'+str(l+1)+'.ref',h[l,:,:],fmt='%15.6e')
h = ma.masked_where(h < -900.0,h)
h = ma.masked_where(h > top,h)
au.plotArray(h[0,:,:],bi.delr,bi.delc,offset=bi.offset,output=None,title='head')

#--get stages for init stage
swr_obj = mfb.SWR_Record(0,results+'bro_6lay.stg')
try:
    totim,dt,kper,kstp,swrstp,success,r = swr_obj.get_record(float(sys.argv[1]))
    print 'SWR binary from totim ',sys.argv[1],' read'
except:
    totim,dt,kper,kstp,swrstp,success,r = swr_obj.get_record()   
    
#print reach_key[:,0],r
#np.savetxt('stage_out.dat',np.array([reach_key[:,0],r]))
save_stage(reach_key[:,0],reach_key[:,1],r)



#pylab.show()  