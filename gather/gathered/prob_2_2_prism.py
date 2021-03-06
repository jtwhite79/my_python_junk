import sys
import numpy as np
import pylab
import scipy
import calc_prism as cp


def find_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    print thres_idx
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])                     

def find_mins(arr):
    mins = []
    for idx in range(1,arr.shape[0]-1):
        if arr[idx] < arr[idx-1] and arr[idx] < arr[idx+1]:
            mins.append(idx)
    return mins


p_dict = {}
p_dict['g'] = 32.2
p_dict['q'] = 100.0
p_dict['y'] = 10.0
p_dict['v'] = 10.0
p_dict['b'] = 10.0

delta_z = 1.0

#p_dict['Y'] = np.arange(0.01,6.0,0.01)

e1 = cp.e_rect(p_dict)
yc1 = cp.yc_rect(p_dict)
ec1 = yc1*1.5

p_dict['b'] = 9.0

#--contraction mean new q 
p_dict['q'] = (10.0 / 9.0) * (100.0)


Y2 = np.arange(0.001,10.0,0.0001)

#--subtract off the step height

#--calculate the residuals
rs = np.zeros_like(Y2)
mins = []
for idx in range(Y2.shape[0]):
    #--calc this_e
    p_dict['y'] = Y2[idx]
    this_e2 = cp.e_rect(p_dict)
    #--calc this residual
    this_r = abs(this_e2 - e1)
    rs[idx] = this_r
    
#--loop over the residuals looking for minimums
mins = []
for idx in range(1,rs.shape[0]-1):
    if rs[idx] < rs[idx-1] and rs[idx] < rs[idx+1]:
        mins.append(idx)

print 'subcritical dw depth: ',Y2[mins[1]]
        
#--maximum contraction
#--e1 = e2c = 1.5y2c
q2c = ((2.0/3.0) * (e1))**(3.0/2.0) * (32.2)**0.5
b2c = 1000.0/q2c

print b2c

        