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
 

def find_conjugate_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    #print thres_idx
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])  
     
 
#--trap params    
b = 20.0    
yt1 = 1.25
m = 2.0
Q = 1000.0

g = 9.81 * 3.281

#--calc trap approach F
A1 = yt1 * (b + (m*yt1))
V1 = Q / A1
b1 = b + (2.0 * m * yt1)
F1 = (Q * b1**0.5) / (g**0.5 * A1**1.5)
#print A1,V1,b1,F1
mt1 = calc_m_trap(b,yt1,m,Q,g=9.81*3.281)
#print yt1,mt1
#--use approach F to find rect y1
yr1 = ((Q/b)**2/(g * F1))**(1.0/3.0)
mr1 = calc_m_rect(b,yr1,Q,g=9.81*3.281)
#print yr1,mr1
#--find conjugates
y = np.arange(1.0,10.0,0.001)
mt = np.zeros_like(y)
mr = np.zeros_like(y)
for idx in range(mt.shape[0]):
    mt[idx] = calc_m_trap(b,y[idx],m,Q,g=g)
    mr[idx] = calc_m_rect(b,y[idx],Q,g=g)
mt_min = mt.min() 
mr_min = mr.min()    
#print mt_min,mr_min
conj_t = y[find_conjugate_idxs(mt,mt1,mt_min)]  
conj_r = y[find_conjugate_idxs(mr,mr1,mr_min)]  
print conj_t,conj_r  



fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(mt,y,'b-',lw=2.0,label='trapezoidal')    
ax.plot(mr,y,'g-',lw=2.0,label='rectangular')    
ax.plot((mt1,mt1),conj_t,'bo')
ax.plot((mt1,mt1),conj_t,'b--')

ax.plot((mr1,mr1),conj_r,'go') 
ax.plot((mr1,mr1),conj_r,'g--')
xmin,xmax = ax.get_xlim()
ax.plot((xmin,mt1),(conj_t[0],conj_t[0]),'b--')
ax.plot((xmin,mt1),(conj_t[1],conj_t[1]),'b--')
ax.plot((xmin,mr1),(conj_r[0],conj_r[0]),'g--')
ax.plot((xmin,mr1),(conj_r[1],conj_r[1]),'g--')
ax.text(500,9.6,' trapezoidal sequent depth ratio:{0:3.2f}'.format(conj_t[1]/conj_t[0]),color='b')
ax.text(500,9.2,' rectangular sequent depth ratio:{0:3.2f}'.format(conj_r[1]/conj_r[0]),color='g')
ax.legend()
pylab.show()