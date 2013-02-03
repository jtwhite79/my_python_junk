import numpy as np
import MFBinaryClass as mfb
from bro_pred import seawat
'''get initial conditions for seawat model predictive run - heads and zetas
'''

hds_file = '..\\..\\_model\\bro.02\\seawat.hds'
conc_file = '..\\..\\_model\\bro.02\\MT3D001.UCN'

hds_obj = mfb.MODFLOW_Head(seawat.nlay,seawat.nrow,seawat.ncol,hds_file)
conc_obj = mfb.MT3D_Concentration(seawat.nlay,seawat.nrow,seawat.ncol,conc_file)

htimes = hds_obj.get_time_list()
ctimes = conc_obj.get_time_list()

hseekpoint = long(htimes[-1,3])
cseekpoint = long(ctimes[-1,3])

hds_save = seawat.ref_dir+'strt_'
conc_save = seawat.ref_dir+'sconc_1_'

htotim,kstp,kper,h,hsuccess = hds_obj.get_array(hseekpoint)
ctotim,ckstp,ckper,c,csuccess = conc_obj.get_array(cseekpoint)
       
if not hsuccess:
    raise Exception('could not extract heads')

if not csuccess:
    raise Exception('could not extract zetas')

for k in range(seawat.nlay):
    np.savetxt(hds_save+str(k+1)+'.ref',h[k,:,:],fmt=' %15.6E')
    np.savetxt(conc_save+str(k+1)+'.ref',c[k,:,:],fmt=' %15.6E')


