import numpy as np
from datetime import datetime
import shutil
import MFBinaryClass as mfb
from bro import seawat


def toString(arr,fmt='{0:13.4G}'):
    nrow,ncol = arr.shape
    a_string = ''
    for i in range(nrow):
        for j in range(ncol):
            a_string += fmt.format(arr[i,j])
        a_string += '\n'
    return a_string

def extract(iter):

   
    init_kper = 24
    if iter != None:
        bak_prefix = seawat.ref_dir+'bak\\'+str(iter)+'_'

    conc_file = 'MT3D001.UCN'
    concObj = mfb.MT3D_Concentration(seawat.nlay,seawat.nrow,seawat.ncol,conc_file)
    ctimes = concObj.get_time_list()
    init_time = ctimes[np.where(ctimes[:,2]==init_kper)][0]
    init_seekpoint = long(init_time[-1])
    totim,kstp,kper,c,success = concObj.get_array(init_seekpoint)
    for k,lay in enumerate(seawat.layer_botm_names):
        aname = seawat.ref_dir+'mod\\sconc_1_'+str(k+1)+'.ref'            
        if iter != None:
            bakname = bak_prefix+'sconc_1_'+str(k+1)+'.ref'
            shutil.copy(aname,bakname)
        print 'writing ',aname
        f = open(aname,'w',0)
        f.write(toString(c[k,:,:]))
        f.close()
 
if __name__ == '__main__':
    extract(None)            