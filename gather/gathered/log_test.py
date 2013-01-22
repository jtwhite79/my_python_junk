import numpy as np
import pylab
norm = np.random.normal(1.0,0.1,10000)
print np.mean(norm),np.std(norm)
log_norm = np.log10(norm)
print np.mean(log_norm),np.std(log_norm)
#fig = pylab.figure()
#ax1,ax2 = pylab.subplot(211),pylab.subplot(212)
#ax1.hist(norm,bins=50)
#ax2.hist(log_norm,bins=50)
#pylab.show()

