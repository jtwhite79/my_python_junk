import os
import shutil
import numpy as np

in_dir = 'ref_org\\'
out_dir = 'ref_homo\\'

in_files = os.listdir(in_dir)
for ifile in in_files:
    if '_K' in ifile.upper():
        a = np.loadtxt(in_dir+ifile)
        print ifile,a.mean()
        a = np.zeros_like(a) + a.mean()
        np.savetxt(out_dir+ifile,a,fmt=' %15.6E')
    else:
        shutil.copy(in_dir+ifile,out_dir+ifile)

