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

    
hds_handle = mfb.MODFLOW_Head(nlay,nrow,ncol,results+'bro_7lay.hds')
totim,kstp,kper,h,success = hds_handle.get_record()
for l in range(nlay):
    np.savetxt('init_heads_'+str(l+1)+'.ref',h[l,:,:],fmt='%15.6e')
    



