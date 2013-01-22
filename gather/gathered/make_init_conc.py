import numpy as np

nrow,ncol = 10,61
array = np.zeros((nrow,ncol))

for r in range(nrow):
    array[r,(10+r):] = 35

array = np.flipud(array)

np.savetxt('init.ref',array,fmt='%15.6e')