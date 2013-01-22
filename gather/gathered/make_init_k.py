import numpy as np
import kl_config

nrow,ncol = kl_config.nrow,kl_config.ncol   

np.savetxt('ref\\init_k.ref',np.zeros((nrow,ncol))+200.0,fmt=' %15.7e')