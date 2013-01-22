import numpy as np
from simple import grid

l1_ibound = np.loadtxt('ref\\ibound.ref')
np.savetxt('ref\\ibound.ref',l1_ibound,fmt=' %3d')
#--how many layers per column
l2c = 3

last_layer = l1_ibound
for k in range(1,grid.nlay):
    ibound = last_layer.copy()
    for i in range(grid.nrow):
        #ibound[i,:] = 1
        idx = np.argwhere(last_layer[i,:]!=0)
        s_act,e_act = idx[0],idx[-1]
        ibound[i,:s_act+l2c] = 0
        ibound[i,s_act+l2c] = 5
        ibound[i,e_act-l2c:] = 0
        ibound[i,e_act-l2c] = 3
    name = 'ref\\ibound_'+str(k+1)+'.ref'
    np.savetxt(name,ibound,fmt=' %3d')
    last_layer = ibound

