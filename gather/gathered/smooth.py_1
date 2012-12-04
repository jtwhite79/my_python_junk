import numpy as np
import pylab

import arrayUtil as au
import gslibUtil as gu


offset = [668350.,580985.]
filter = np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
#print np.shape(filter),np.cumsum(filter) 
max_elev = 10.0
nrow,ncol = 459,615

#--load hard data
harddata_file = '..\\tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)

top = au.loadArrayFromFile(nrow,ncol,'filter_2_edge.ref')
top[np.where(top>max_elev)] = max_elev 
#print top
new_top = np.zeros_like(top)
xi,yi = 2,2

while xi < ncol-3:
    while yi < nrow-3:
        temp = top[yi-2:yi+3,xi-2:xi+3] 
#        print xi,yi,np.shape(temp),np.shape(top)
        total = filter*temp
#        print np.cumsum(total)[-1],np.cumsum(filter)[-1]
        new_top[yi,xi] = np.cumsum(total)[-1]/np.cumsum(filter)[-1]
        yi += 1
    xi += 1
    yi = 2
    
au.writeArrayToFile(new_top,'filter_3_raw.ref')

new_top[:,:3] = new_top[:,4:7]
new_top[:,-3:] = new_top[:,-7:-4]

new_top[:3,:] = new_top[4:7,:]
new_top[-3:,:] = new_top[-7:-4,:]

au.writeArrayToFile(new_top,'filter_3_edge.ref')

au.plotArray(new_top,500,500,offset=offset,output=None,gpts=harddata[:,0:2])
au.plotArray(top,500,500,offset=offset,output=None,gpts=harddata[:,0:2])
pylab.show()