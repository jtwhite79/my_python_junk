import os,re,sys
import numpy as np
import gslibUtil as gu
import arrayUtil as au

file_out = 'T3_expected_sk.dat'

nrow,ncol = 197,116
delc,delr = 2650.,2650.
offset = 668350.,288415.


#--load hard data
harddata_file = 'tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)

#--load gslib file
file = 'SimpleKrig_all.dat'
title,var_names,array = gu.loadGslibFile(file)
if title == False: sys.exit()
print np.shape(array)

for prop in range(0,len(var_names)):
    this_prop = array[:,prop].copy() 
    print var_names[prop],np.shape(this_prop)
    this_prop.resize(nrow,ncol)
    au.writeArrayToFile(np.flipud(this_prop),var_names[prop]+'.ref')

#plt = array[:,0].copy()
#plt.resize(nrow,ncol)
#
#
#au.plotArray(np.flipud(plt),delc,delc,offset=offset,title=file_out,gpts=harddata[:,0:2])
#au.writeArrayToFile(np.flipud(plt),file_out,nWriteCol=ncol)
