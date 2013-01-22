import numpy as np
import kl_config

nrow,ncol = kl_config.nrow,kl_config.ncol   

#--load the intial conditions parameter array
arr = np.loadtxt('ref\\init_k.ref')
pval = []
for i in range(nrow):
    for j in range(ncol):
        pval.append(arr[i,j]) 
pval = np.log10(np.array(pval))

#--load the scaling array
scale = np.loadtxt('scale.mat')

pscale = np.dot(scale,pval).copy()

offset =.0
np.savetxt('kl_eig_init.dat',pscale+offset,fmt='%15.8e')