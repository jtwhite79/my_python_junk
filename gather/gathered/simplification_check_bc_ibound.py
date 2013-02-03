import os
import numpy as np
import pandas
from simple import grid

ibound_prefix = '_model\\ref_rc\\ibound'
ibound_files = [ibound_prefix+'.ref']
for k in range(1,grid.nlay):
    ibound_files.append(ibound_prefix+'_'+str(k+1)+'.ref')

ibound = np.zeros((grid.nlay,grid.nrow/grid.sample_stride,grid.ncol/grid.sample_stride))

for k,ifile in enumerate(ibound_files):
    arr = np.loadtxt(ifile)
    ibound[k,:,:] = arr

locs = pandas.read_csv('_misc\\well_locs_rc.csv')
ob = []
for idx,entry in locs.iterrows():
    k,i,j = entry['layer']-1,entry['row']-1,entry['column']-1
    if ibound[k,i,j] == 0:
        ob.append(entry)
print ob


