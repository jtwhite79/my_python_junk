import numpy as np
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import pandas

import MFBinaryClass as mfb 
import shapefile as sf

import bro 


#--heads
head_file = bro.modelname+'.hds'
headObj = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,head_file)
htimes = headObj.get_time_list()
ntimes = htimes.shape[0]

#--date to extract heads
hds_dt = datetime(year=1953,month=1,day=1)
hds_idx = list(bro.sp_start).index(hds_dt)

hds_seek = long(htimes[hds_idx,3])
totim,kstp,kper,h,success = headObj.get_array(hds_seek)
if not success:
    raise Exception('could extract heads for time '+str(hds_dt))

strt_prefix = 'ref\\strt_L'
for l in range(bro.nlay):
    hlay = h[l,:,:]
    strt_name = strt_prefix+str(l+1)+'.ref'
    np.savetxt(strt_name,hlay,fmt=' %15.7E')



#--zeta
#--izeta instance
zeta_file = bro.modelname+'.zta'
zta_text = ['    ZETAPLANE  1','    ZETAPLANE  2']
zetaObj = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file)
ztimes = []
for ztext in zta_text:
    zts = zetaObj.get_time_list(ztext)
    ztimes.append(zts)


#--date to extract heads
zta_dt = datetime(year=1953,month=1,day=1)
zta_idx = list(bro.sp_start).index(zta_dt)

#--find the seek points for each of the zetas
zta_seeks = []
for zts in ztimes:
     zta_seek = long(zts[zta_idx,3])
     zta_seeks.append(zta_seek)

for iz,zseek in enumerate(zta_seeks):

    z,totim,success = zetaObj.get_array(zseek)
    if not success:
        raise Exception('could extract zeta for time, surface '+str(zta_dt)+' '+zeta_text[iz])

    izeta_prefix = 'ref\\izeta_'+str(iz+1)+'_L'
    for l in range(bro.nlay):
        zlay = z[l,:,:]
        izeta_name = izeta_prefix+str(l+1)+'.ref'
        np.savetxt(izeta_name,zlay,fmt=' %15.7E')



