import numpy as np
import MFBinaryClass as mfb
from bro_pred import flow
'''get initial conditions for flow model predictive run - heads and zetas
'''

hds_file = '..\\..\\_model\\bro.03\\flow.hds'
zta_file = '..\\..\\_model\\bro.03\\flow.zta'
zta_text = '    ZETAPLANE  1'

hds_obj = mfb.MODFLOW_Head(flow.nlay,flow.nrow,flow.ncol,hds_file)
zta_obj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,zta_file)

htimes = hds_obj.get_time_list()
ztimes = zta_obj.get_time_list(zta_text)

hseekpoint = long(htimes[-1,3])
zseekpoint = long(ztimes[-1,3])

hds_save = flow.ref_dir+'strt_1.ref'
zta_save = flow.ref_dir+'IZETA_1_L1.ref'

htotim,kstp,kper,h,hsuccess = hds_obj.get_array(hseekpoint)
z,ztotim,zsuccess = zta_obj.get_array(zseekpoint)
       
if not hsuccess:
    raise Exception('could not extract heads')

if not zsuccess:
    raise Exception('could not extract zetas')

np.savetxt(hds_save,h[0,:,:],fmt=' %15.6E')
np.savetxt(zta_save,z[0,:,:],fmt=' %15.6E')

