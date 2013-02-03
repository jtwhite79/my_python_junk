import numpy as np
from simple import grid

def apply():
    ref_dir = '_model\\ref\\'
    thk_frac = {'upper':np.loadtxt(ref_dir+'upper_thk_frac.ref')}
    thk_frac['middle'] = np.loadtxt(ref_dir+'middle_thk_frac.ref')
    thk_frac['lower'] = np.loadtxt(ref_dir+'lower_thk_frac.ref')
    top = np.loadtxt(ref_dir + 'top.ref')
    bot1 = top - thk_frac['upper']
    np.savetxt(ref_dir+'mod\\botm_Layer_1.ref',bot1,fmt='%15.6G')
    prev = bot1
    for k in range(1,grid.nlay):
        thk = thk_frac[grid.lay_key[k]]
        bot = prev - thk
        np.savetxt(ref_dir+'mod\\botm_Layer_'+str(k+1)+'.ref',bot,fmt='%15.6G')
        prev = bot
if __name__ == '__main__':
    apply()
