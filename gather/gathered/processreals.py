import os,re
import numpy as np
import gslibUtil as gu
import arrayUtil as au

nrow,ncol = 197,116
delc,delr = 2650.,2650.
offset = 668350.,288415.
realization_path = 'D:/Users/jwhite/Projects/Broward/Geostats/SGEMS/l1_ds_reals' 
realization_prefix = 'layer1_thk_omni_ds'

reg = re.compile(realization_prefix,re.IGNORECASE)

harddata_file = '..\\LayerThickness_fixed.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)

files = os.listdir(realization_path)
real_files = []
for file in files:
    if reg.search(file) is not None:
        real_files.append(file)

total = np.zeros((nrow*ncol),dtype='float')
file_count = 0
for file in real_files:
    file_count += 1   
    print file_count,' of ',len(real_files)
    title,prop_name,real_array = gu.loadGslibFile(realization_path+file)
    #real_array.resize(nrow,ncol)
    total += real_array
    #real_array = np.flipud(real_array)
    if file_count%500 == 0:
        expected = total/(float(file_count))
        mean = np.mean(expected)
        stdev = np.std(expected)
        print file_count,mean,stdev       
        expected.resize(nrow,ncol)    
        au.writeArrayToFile(np.flipud(expected),'Layer1_omni_'+str(file_count)+'_expected.dat')

expected = total/(float(file_count))
mean = np.mean(expected)
stdev = np.std(expected)
print file_count,mean,stdev       
expected.resize(nrow,ncol)    
au.writeArrayToFile(np.flipud(expected),'Layer1_omni_'+str(file_count)+'_expected_sk.dat')
au.plotArray(np.flipud(expected),delc,delc,offset=offset)
