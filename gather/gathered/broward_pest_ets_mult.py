import os
from datetime import datetime
import numpy as np



def apply():
    
    '''apply the 4 multiplier arrays to the calibration period arrays
    '''

    nex_start = datetime(year=1996,month=1,day=1)
    dry_months = [12,1,2,3,4,5]

    cal_end = datetime(year=2012,month=5,day=31)

    #--load the 4 multiplier arrays
    mult_dir = 'ref\\mult\\'
    dry_pt,dry_nx = np.loadtxt(mult_dir+'ets_dr_pt.ref'),np.loadtxt(mult_dir+'ets_dr_nx.ref')
    wet_pt,wet_nx = np.loadtxt(mult_dir+'ets_wt_pt.ref'),np.loadtxt(mult_dir+'ets_wt_nx.ref')
    
    shape = dry_pt.shape

    cal_dir = 'bro.03\\calibration\\flowref\\ets'
    base_dir = 'ref\\base\\ets\\'    
    ets_files = os.listdir(base_dir)

    for ets_file in ets_files:
        dt = datetime.strptime(ets_file.split('.')[0].split('_')[2],'%Y%m%d')
        print dt
        if dt < nex_start:
            if dt.month in dry_months:
                mult = dry_pt
            else:
                mult = wet_pt
        else:
            if dt.month in dry_months:
                mult = dry_nx
            else:
                mult = wet_nx
        arr = np.fromfile(base_dir+ets_file,dtype=np.float32)
        arr.resize(shape)
        arr *= mult
        arr.tofile(cal_dir+ets_file)






if __name__ == '__main__':
    apply()