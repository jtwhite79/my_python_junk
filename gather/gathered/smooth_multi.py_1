import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab

import arrayUtil as au
import gslibUtil as gu


offset_new = [728600.,577350.]
filter = np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
#print np.shape(filter),np.cumsum(filter) 
min_elev,max_elev = 0.0,10.0
nrow,ncol = 301,501
iterations = 40

#--load hard data
print 'loading hard data...'
harddata_file = '..\\tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)

print 'loading top array...'
top = au.loadArrayFromFile(nrow,ncol,'filter_14_edge.ref')
top[np.where(top>max_elev)] = max_elev 
top[np.where(top<min_elev)] = min_elev 
#print top 
org_top = top
#au.plotArray(org_top,500,500,offset=offset,output='save',min=0,gpts=harddata[:,0:2],title='org')

new_top = np.zeros_like(top)
xi,yi = 2,2

print 'beginning smoothing iterations...'
for iter in range(14,iterations):
    
    print iter
    while xi < ncol-3:
        while yi < nrow-3:
            temp = top[yi-2:yi+3,xi-2:xi+3].copy() 
    #        print xi,yi,np.shape(temp),np.shape(top)
            total = filter*temp
    #        print np.cumsum(total)[-1],np.cumsum(filter)[-1]
            new_top[yi,xi] = np.cumsum(total)[-1]/np.cumsum(filter)[-1]
            yi += 1
        xi += 1
        yi = 2
    
    au.writeArrayToFile(new_top,'smoothed\\filter_'+str(iter+1)+'raw.ref')
        
    new_top[:,:3] = new_top[:,4:7]
    new_top[:,-3:] = new_top[:,-7:-4]
    
    new_top[:3,:] = new_top[4:7,:]
    new_top[-3:,:] = new_top[-7:-4,:]
    
    au.plotArray(new_top,500,500,offset=offset_new,output='save',min=-0,title=str(iter),gpts=harddata[:,0:2])
    au.writeArrayToFile(new_top,'smoothed\\filter_'+str(iter+1)+'_edge.ref')
    
    top = new_top.copy() 
    new_top = np.zeros_like(top)
    xi,yi = 2,2
