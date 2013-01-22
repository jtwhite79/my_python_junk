import numpy as np
import pylab


def calc_e(y,q):
    e = np.zeros_like(y)
    g = 32.2
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



y = np.arange(0.01,100.0,0.01)
q1 = 121.25

e = calc_e(y,q1)
e1 = 11.55

e_min = e.min()
y_min = y[np.where(e==e_min)][0]
print 'ec,yc',e_min,y_min

fig = pylab.figure()
ax = pylab.subplot(1,1,1)
ax.plot(e,y,'b-',label='q=1.0',lw=2.0)
ax.plot((0,e_min,e_min),(y_min,y_min,0),'b--',lw=2.0)
y1 = y[find_idxs(e,e1,e_min)]

for y_idx in range(y1.shape[0]):
    if e1 >= e_min:
        print 'e1,y1',e1,y1 
        ax.plot((0,e1),(y1[y_idx],y1[y_idx]),'b--')     
        ax.plot((e1,e1),(0,y1[y_idx]),'b--') 
    else:
        print 'not enough energy to pass flow'
ax.plot(y,y,'k--',lw=2.0)
ax.set_xlim(0,20)
ax.set_ylim(0,20)
ax.set_ylabel('flow depth (ft)')
ax.set_xlabel('specific energy (ft)')
ax.legend()
pylab.show()

        