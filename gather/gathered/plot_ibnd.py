import arrayUtil as au
import numpy as np

nrow,ncol = 301,501
ibnd_l1 = au.loadArrayFromFile(nrow,ncol,'ref\\icbnd_l1.ref')
#ibnd = au.loadArrayFromFile(nrow,ncol,'ref\\icbund.ref')

au.plotArray(ibnd_l1,500,500)
au.plotArray(ibnd,500,500)
