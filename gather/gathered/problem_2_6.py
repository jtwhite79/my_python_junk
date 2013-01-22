import math
import numpy as np
import pylab

def Dh(y,d):
    #print y,d
    try:
        theta = 2.0 * math.acos(1.0 - (2.0*(y/d)))
        #print ' ',y,theta
        Dh_num = (theta - math.sin(theta)) * d**2 
        Dh_dem = d * math.sin(theta/2.0) * 8.0
        Dh = Dh_num / Dh_dem
    except:
        Dh = 0.0
    return Dh
      

def calc_e_circ(y,d,g=32.2):
    e = np.zeros_like(y)    
    for y_idx in range(y.shape[0]):
        this_Dh = Dh(y[y_idx],d)
        #print y[y_idx],this_Dh
        e[y_idx] = y[y_idx] + (this_Dh/2.0)
        
    return e
    
    


def calc_e_rect(y,q,g=32.2):
    e = np.zeros_like(y)    
    for y_idx in range(y.shape[0]):
        e[y_idx] = y[y_idx] + ((q**2)/(2.0*g*(y[y_idx]**2)))
        
    return e

def find_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])                     


y_max = 100.0
y = np.arange(0.01,y_max,0.01)
q1 = 1026.78

e = calc_e_rect(y,q1)
e1 = 21.35


e_min = e.min()
y_min = y[np.where(e==e_min)][0]
print 'ec,yc',e_min,y_min

fig = pylab.figure()
ax = pylab.subplot(1,1,1)
ax.plot(e,y,'b-',label='q=1.0',lw=2.0)
ax.plot((0,e_min,e_min),(y_min,y_min,0),'b--',lw=2.0)
y1 = y[find_idxs(e,e1,e_min)]

if e1 >= e_min:
    print 'e1,y1',e1,y1 
    for y_idx in range(y1.shape[0]):            
        ax.plot((0,e1),(y1[y_idx],y1[y_idx]),'b--')     
        ax.plot((e1,e1),(0,y1[y_idx]),'b--') 
else:
    print 'not enough energy to pass flow',e1
 
ax.plot(y,y,'k--',lw=2.0)
ax.set_xlim(0,y_max)
ax.set_ylim(0,y_max)
ax.set_ylabel('flow depth (ft)')
ax.set_xlabel('specific energy (ft)')
ax.legend()
pylab.show()

        