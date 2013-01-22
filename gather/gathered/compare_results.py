import numpy as np
import pylab

pv1b = np.loadtxt('pd_3_ten.out',skiprows=3)
pv1a = np.loadtxt('pd_3_ten_a.out',skiprows=3)

fig = pylab.figure()
ax = pylab.subplot(111)

ax.plot(pv1b[:,0],np.sqrt(pv1b[:,1]),label='underfit penalty',color='b')
ax.plot(pv1b[:,0],np.sqrt(pv1b[:,2]),label='overfit penalty',color='g')
ax.plot(pv1b[:,0],np.sqrt(pv1b[:,1]+pv1b[:,2]),label='sum',color='b')  
ax.set_ylim(0,1.0e+5)   
pylab.show()      