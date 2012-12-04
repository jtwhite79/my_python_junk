import os,sys,pylab
import numpy as np
import gslibUtil as gu


import arrayUtil as au
import numpy as np
import pylab

#--load hard data
harddata_file = 'tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)

nrow,ncol = 197,116 
delr,delc = 2650,2650
offset = [668350.,288415.]

path = 'array_sk\\'
files = os.listdir(path) 
print files
for file in files:
    this_array = au.loadArrayFromFile(nrow,ncol,path+file)
    print np.mean(this_array)
    au.plotArray(this_array,delr,delc,gpts=harddata[:,0:2],offset=offset)
    




