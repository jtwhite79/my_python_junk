import numpy as np
import pylab
import kl_config

nrow,ncol = kl_config.nrow,kl_config.ncol

arr = np.loadtxt('ref\\hk_1_1.ref')
fig = pylab.figure()
ax = pylab.subplot(111)
ax.pcolor(arr)
pylab.show()
