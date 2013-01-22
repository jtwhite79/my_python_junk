import numpy as np
import runs
reload(runs)
data = np.loadtxt('earthq.dat')
um = data[np.where(data<np.median(data))]
print np.shape(um)
z = runs.runstest(data,splt=np.median(data))
print z