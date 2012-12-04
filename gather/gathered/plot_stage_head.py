import sys
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


reach_key = load_reaches(nreach,'dis\\dataset.txt',skiprows=2,usecols=[0,2,4,5])
reach_array = np.zeros((nrow,ncol)) - 999.


swr_obj = mfb.SWR_Record(-1,results+'bro_1lay.rgp')
totim,dt,kper,kstp,swrstp,success,compele = swr_obj.get_record()
fig_idx = [0,1,2,7]
#fig_idx = [0]
ce_items = swr_obj.get_item_list()
f_list = []
#print compele.shape
#sys.exit()


for i in fig_idx:
    
    array = np.zeros_like(reach_array) - 9999
    m_array = np.zeros_like(reach_array) - 999.    
    for a in range(0,len(compele)):
        thisCompele = reach_key[np.where(reach_key[:,1]==a+1)].astype(int)
        #print a+1,thisCompele[0,2],thisCompele[0,3]
        for r in thisCompele:
            #print r
            array[r[2]-1,r[3]-1] = compele[a,i]
            m_array[r[2]-1,r[3]-1] = 1
     
    array = ma.masked_where(m_array==-999.0,array)
    this_ax = au.plotArray(array,delr,delc,offset=offset,\
                  output=None,title=repr(i)+' '+ce_items[i])
                     
          
#--heads
top = np.loadtxt('ref\\top_filter_35_edge.ref')
hds_handle = mfb.MODFLOW_Head(1,nrow,ncol,results+'bro_1lay.hds')
totim,kstp,kper,h,success = hds_handle.get_record()
np.savetxt('init_heads.ref',h[0,:,:],fmt='%15.6e')
h = ma.masked_where(h < -900.0,h)
h = ma.masked_where(h > top,h)
au.plotArray(h[0,:,:],delr,delc,offset=offset,output=None,title='head')

#--get stages for init stage
swr_obj = mfb.SWR_Record(0,results+'bro_1lay.stg')
totim,dt,kper,kstp,swrstp,success,r = swr_obj.get_record()
#print reach_key[:,0],r
#np.savetxt('stage_out.dat',np.array([reach_key[:,0],r]))
save_stage(reach_key[:,0],reach_key[:,1],r)



pylab.show()  