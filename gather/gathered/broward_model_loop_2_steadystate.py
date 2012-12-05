import os
import broward__model_extract_initial_concs as ext
from bro import seawat

iters = 100
seawat_cmdline = 'swt_v4x64.exe seawat.nam_swt'

for i in range(iters):
    print 'iteration ',i+1
    os.system(seawat_cmdline)
    ext.extract(i+1)

