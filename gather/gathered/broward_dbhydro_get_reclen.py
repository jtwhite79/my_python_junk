import os
import pestUtil as pu
import dbhydro_util
stg_dir = 'SW\\STG\\'
stg_files = os.listdir(stg_dir)

nrecs = 0

for file in stg_files:
    #dbhydro_util.load_series(stg_dir+file)
    #smp = pu.smp(stg_dir+file,load=True)
    f = open(stg_dir+file,'r')
    for line in f:
        nrecs += 1
    f.close()
print nrecs