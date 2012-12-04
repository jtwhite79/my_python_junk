import numpy as np
import arrayUtil as au

#--ascii raster
file = 'top.txt'
nrow,ncol,offset,gridDim,noData,array = au.loadGrdFromFile(file)


#au.plotArray(array,500,500)
np.savetxt('top.ref',array,fmt='%15.6e')