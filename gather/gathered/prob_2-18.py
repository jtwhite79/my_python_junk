import numpy as np
import pylab

def calc_Q(Cv,Cd,H,L,g=32.2):
    Q = Cv * Cd * (2./3.) * ((2./3.) * g)**0.5 * L * H**(3./2.)
    return Q
   
def find_nearest(value,array):
    min_diff = 1.0e+32
    min_idx = -999
    
    for idx in range(array.shape[0]):
        diff = abs(array[idx] - value)
        if diff < min_diff:
            min_diff = diff
            min_idx = idx   
    return min_idx
    
Qmax = 1.0 #cfs
Qmin = 0.1
Ymax =  1.5
b = 1.25
L = 0.75

P = 0.75
assert (Ymax-P)/Ymax > 0.35
l = (Ymax - P) / 0.33



print 'P,l',P,l
Cdmax = 0.848
Amax = L * (Ymax - P)
A1 = b * (Ymax)
print 'Amax,A1,CdAmax/A1',Amax,A1,(Cdmax * Amax) / A1
Cv = 1.01

#Q = calc_Q(Cv,Cdmax,Ymax-P,L)
#print Q

H_range = np.arange(0.01,1.5,.01)
Q_range = np.zeros_like(H_range)
for h_idx in range(H_range.shape[0]):
    Q_range[h_idx] = calc_Q(Cv,Cdmax,H_range[h_idx],L)
Qmax_idx = find_nearest(Qmax,Q_range)
#H_range += P
H_range *= 12.0
Hmax = H_range[Qmax_idx]
assert Hmax/12.0 + P < Ymax, str(Hmax/12.0 + P)
Qmin_idx = find_nearest(Qmin,Q_range)
print Qmin_idx
Hmin = H_range[Qmin_idx]
print Hmin
fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(H_range,Q_range,'k-',lw=2.0)
print 'head range:',Hmax-Hmin

ax.plot([Hmin,Hmin,0],[0,Qmin,Qmin],'b--',lw=1.5)
ax.plot([Hmax,Hmax,0],[0,Qmax,Qmax],'b--',lw=1.5)
ax.set_xlabel('depth in flume (in)')
ax.set_ylabel('Q (cfs)')
ax.text(0.25,3.0,'P (in):{0:5.2f}'.format(P*12.0))
ax.text(0.25,2.75,'L (in):{0:5.2f}'.format(L*12.0))
ax.text(0.25,2.5,'l_min (in):{0:5.2f}'.format(l*12.0))                                                                              
ax.text(0.25,2.25,'head range (in):{0:5.2f}'.format(Hmax-Hmin))                                                                              
ax.text(0.25,2.0,'free board (in):{0:5.2f}'.format(Ymax*12.0 - (Hmax+(P*12.0)))) 
ax.text(0.25,1.75,'Cv :{0:5.2f}'.format(Cv)) 
ax.text(0.25,1.5,'Cd :{0:5.2f}'.format(Cdmax))
ax.set_xlim(0,10)
                                                                       
pylab.show()
