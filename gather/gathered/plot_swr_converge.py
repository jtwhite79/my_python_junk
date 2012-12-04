import numpy as np
import pylab

converge = np.loadtxt('swr_converge.out',skiprows=3,usecols=[0,1,2,3,4,5,6,7,8])

fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
bins = np.sort(np.unique(converge[:,7]))
b = ax.hist(converge[:,7],bins=bins)
norm_bins = np.linspace(1,b[0].shape[0],b[0].shape[0])    
print b[0].shape,norm_bins.shape    
ax2.bar(b[1][:-1],b[0]) 
ax2.set_xticks(bins)
print b[0]   
pylab.show()    