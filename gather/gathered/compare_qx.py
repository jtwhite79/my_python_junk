import numpy as np
import pylab

#pv1a = np.loadtxt('..\\..\\..\\predvar1a\\predvar1a\\test2\\qX.mat')

pv1b = np.loadtxt('qX.mat')
#diff = pv1a - pv1b
u,s,vt = np.linalg.linalg.svd((pv1b))
print pv1b[0,0]
np.savetxt('ua.dat',u)
np.savetxt('sa.dat',s)
np.savetxt('vta.dat',vt)

#lhs = np.loadtxt('lhs.mat')
#diff = vt - lhs
#diff = np.ma.masked_where(np.abs(diff) < 1.0e-5,diff)
#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.pcolor(diff)
#pylab.show()

print u.shape,s.shape,vt.shape
#print np.cumsum(diff)[-1]

#print diff.max(),diff.min()