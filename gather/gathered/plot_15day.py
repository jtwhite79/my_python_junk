import numpy as np

import pylab

data = np.loadtxt('15_day_ma.dat')

fig = pylab.figure()
ax = pylab.subplot(111)
axt = pylab.twinx()
data[:,1] /= 12.0
    
ax.plot(data[:,0],data[:,1])
axt.plot(data[:,0],np.cumsum(data[:,1]*12.0))
#pylab.show()
tot = 0.0
for i in range(data.shape[0]):
    scaled = data[i,1]
    print 1,'    ',-1        
    print 'constant     {0:10.3e}'.format(scaled),'    (FREE)'
    tot += scaled
#print tot * 12.0    