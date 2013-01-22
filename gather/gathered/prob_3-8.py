import math
import numpy as np
import pylab



def find_conjugate_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    #print thres_idx
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])  
     
 
#--params    
b = 40.0    
lake_head = 200ft
Q = 10000.0 #cfs

hl = 0.1

#--calc head at toe of spillway





#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.plot(mc,y,'b-',lw=2.0)    
#ax.plot((mc1,mc1),conj_c,'bo')
#ax.plot((mc1,mc1),conj_c,'b--')
#
#xmin,xmax = ax.get_xlim()
#ax.plot((xmin,mc1),(conj_c[0],conj_c[0]),'b--')
#ax.plot((xmin,mc1),(conj_c[1],conj_c[1]),'b--')
#
#ax.text(0.1,0.95,'sequent depths:{0:3.2f} {1:3.2f}'.format(conj_c[0],conj_c[1]),color='b')
##ax.legend()
#pylab.show()