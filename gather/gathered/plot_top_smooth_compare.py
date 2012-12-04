import numpy as np
import pylab

org = np.loadtxt('ref\\cwm_topo.ref')

smooth = np.loadtxt('ref\\filter_20_edge.ref')

print org.shape,smooth.shape
#min,max = org.min(),org.max()
#min,max = 0,15

org = np.ma.masked_where(np.logical_or(org<min,org>max),org)
smooth = np.ma.masked_where(np.logical_or(smooth<min,smooth>max),smooth)

fig = pylab.figure()
ax1 = pylab.subplot(211)

ax1.pcolor(org,vmin=min,vmax=max)

ax2 = pylab.subplot(212)
ax2.pcolor(smooth,vmin=min,vmax=max)

pylab.show()

