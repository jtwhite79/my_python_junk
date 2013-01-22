import numpy as np
import kl_config

nrow,ncol = kl_config.nrow,kl_config.ncol

#--load the unscale matrix
unscale = np.loadtxt('unscale.mat')
assert unscale.shape[0] == nrow*ncol, 'number of rows of unscale not equal to nrow*ncol'

#--load the current parameters
#eig_pars = np.loadtxt('kl_eig.dat')
eig_pars = np.loadtxt('kl_eig.dat')
assert eig_pars.shape[0] == unscale.shape[1],'number of parameters not equal to the number of columns of unscale'

#--scale the columns of unscale by each parameter value
for j in range(unscale.shape[1]):
    unscale [:,j] *= eig_pars[j]


#punscale = np.dot(unscale,eig_pars).copy()
#arr = np.zeros((nrow,ncol))
#c = 0
#for i in range(nrow):
#    for j in range(ncol):
#        arr[i,j] = punscale[c]
#        c += 1

#--form the model array by summing the components along the rows
arr = np.zeros((nrow,ncol))
c = 0
for i in range(nrow):
    for j in range(ncol):
        arr[i,j] = 10**np.sum(unscale[c,:])
        c += 1

np.savetxt('ref\\hk_1_1.ref',10**arr,fmt=' %15.6e')            
        
            
    
