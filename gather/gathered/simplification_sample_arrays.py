import os
import numpy as np
from simple import grid


def sample():
    fine_dir = 'ref'
    rc_dir = 'ref_rc'
    lay_dir = 'ref_lay'
    
    if not os.path.exists(rc_dir):
        os.mkdir(rc_dir)        
    for root, dirs, files in os.walk(fine_dir):
        for file in files:
            outroot = root.replace(fine_dir,rc_dir)
            if not os.path.exists(outroot):
                os.mkdir(outroot)
            print root,file           
            fine = None
            if 'rech' not in file:
                try:
                    fine = np.atleast_2d(np.loadtxt(root+'\\'+file))
                    isBin = False
                except ValueError:
                    arr = np.fromfile(root+'\\'+file,dtype=np.float32)
                    arr.resize((grid.nrow,grid.ncol))
                    fine = np.atleast_2d(arr)
                    isBin = True            
                if fine.shape[0] > 1:
                    rc_nrow = fine.shape[0]/grid.sample_stride
                    rc_ncol = fine.shape[1]/grid.sample_stride
                    coarse = np.zeros((rc_nrow,rc_ncol)) - 1.0e+10
                    #--cheaper to duplicate the iteration than to check at file type at each position
                    if 'ibound' in file:
                        isInt = True
                        for ic in range(rc_nrow):
                            for jc in range(rc_ncol):                    
                                coarse[ic,jc] = np.max(fine[grid.row_map[ic],grid.col_map[jc]])
                    else:
                        isInt = False
                        for ic in range(rc_nrow):
                            for jc in range(rc_ncol):                         
                                coarse[ic,jc] = np.mean(fine[grid.row_map[ic],grid.col_map[jc]])
            
                    out_name = outroot+'\\'+file           
                    if isBin:
                        if isInt:
                            coarse = coarse.astype(np.int)
                        else:
                            coarse = coarse.astype(np.float32)
                        coarse.tofile(out_name)
                    else:
                        if isInt:
                            fmt = ' %4d'
                        else:
                            fmt = '%15.4G'
                        np.savetxt(out_name,coarse,fmt=fmt)

if __name__ == '__main__':
    sample()
