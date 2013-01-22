import numpy as np
import simple

nrow,ncol,nlay = simple.grid.nrow,simple.grid.ncol,simple.grid.nlay
top = np.loadtxt('ref\\interp_topo.ref')
top[np.where(top<100.0)] = 100.0
bot = 0.0
thk = (top.min() - bot) / nlay
pass




