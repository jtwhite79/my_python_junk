import math
import numpy as np
import pylab


def calc_m_trap(b,y,m,Q,g=9.81):
    term1 = (b * y**2)/2.0
    term2 = (m * y**3)/3.0
    term3 = Q**2 / (g*y*(b+(m*y)))
    m = term1 + term2 + term3
    return m
 
def calc_m_rect(b,y,Q,g=9.81):
    term1 = (b * y**2) / 2.0
    term2 = Q**2/(g * b * y)
    m = term1 + term2
    #print m
    return m

def calc_m_circ(y,d,Q,g=9.81):
    theta = calc_theta(y,d)
    term1 = 3.0 * math.sin(theta/2.0)
    term2 = (math.sin(theta/2.0))**3
    term3 = 3.0 * (theta/2.0) * (math.cos(theta/2.0))
    term4 = (d**3)/24.0
    term5 = Q**2 / (((g*(d**2)) * (theta - math.sin(theta))) / 8.0)
    m = ((term1 - term2 - term3) * term4) + term5
    return m
    
def calc_theta(y,d):
    theta = 2.0 * math.acos(1.0 - (2.0 * (y/d)))
   
    return theta
 

def find_conjugate_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    #print thres_idx
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])  
     
 
#--circ params    
d = 3.0    
yc1 = 0.6
Q = 5.0

g = 9.81 * 3.281

mc1 = calc_m_circ(yc1,d,Q,g=g)
print 'approach momentum: ',mc1
Zcirc = Q / (g**0.5 * d**(5.0/2.0))
y1_over_d = yc1 / d
print 'Zcirc',Zcirc
print 'y1/d',y1_over_d
#--find conjugates
y = np.arange(0.25,1.0,0.00001)
mc = np.zeros_like(y)

for idx in range(y.shape[0]):
    mc[idx] = calc_m_circ(y[idx],d,Q,g=g)
   
mc_min = mc.min() 
print 'mc_min',mc_min
conj_c = y[find_conjugate_idxs(mc,mc1,mc_min)]  
print conj_c

fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(mc,y,'b-',lw=2.0)    
ax.plot((mc1,mc1),conj_c,'bo')
ax.plot((mc1,mc1),conj_c,'b--')

xmin,xmax = ax.get_xlim()
ax.plot((xmin,mc1),(conj_c[0],conj_c[0]),'b--')
ax.plot((xmin,mc1),(conj_c[1],conj_c[1]),'b--')

ax.text(1.5,0.8,'sequent depths:{0:3.2f} {1:3.2f}'.format(conj_c[0],conj_c[1]),color='b')
#ax.legend()
pylab.show()