import os,sys

import numpy as np
import pylab

import arrayUtil as au 
import gslibUtil as gu

offset = [668350.,288415.]
offset_new = [728600.,577350.]
#max_new = [982090.,739166.]
hm_delr,hm_delc = 2650,2650
hm_nrow,hm_ncol = 197,116

new_delr,new_delc = 500,500

hm_max = [((hm_ncol*hm_delr))+offset[0],((hm_nrow*hm_delc))+offset[1]]
print 'halfmile max',hm_max
max_new = hm_max

halfmile_x = np.arange(offset[0],hm_max[0]+hm_delc,hm_delc)
halfmile_y = np.arange(offset[1],hm_max[1]+hm_delr,hm_delr)
print 'halfmile x/y',np.shape(halfmile_x),np.shape(halfmile_y)

#new_ncol = int(round((max_new[0]-offset_new[0])/new_delr,0))
#new_nrow = int(round((max_new[1]-offset_new[1])/new_delc,0))
new_nrow,new_ncol = 301,501

print 'new row/col',new_nrow,new_ncol

new_max = [(new_ncol*new_delr)+offset_new[0],(new_nrow*new_delc)+offset_new[1]]
print 'new max',new_max


new_x = np.arange(offset_new[0],new_max[0]+new_delc,new_delc)
new_y = np.arange(offset_new[1],new_max[1]+new_delr,new_delr)
print np.shape(new_x),np.shape(new_y)

map_x = np.zeros((new_ncol))+1.0E+32
map_y = np.zeros((new_nrow))+1.0E+32
print np.shape(map_x),np.shape(map_y)

for x1 in range(0,np.shape(map_x)[0]):
    for x2 in range(1,np.shape(halfmile_x)[0]):
        node_x = new_x[x1+1]-(new_delc/2)
#        print node_x,halfmile_x[x2]
        if node_x <= halfmile_x[x2]:
            map_x[x1] = x2-1
            break            
map_x[-7:] = hm_ncol-1
#print map_x.astype(int)        


for y1 in range(0,np.shape(map_y)[0]):
    for y2 in range(1,np.shape(halfmile_y)[0]):
        node_y = new_y[y1+1]-(new_delc/2)
        if node_y <= halfmile_y[y2]:
            map_y[y1] = y2-1
            break
#print map_y.astype(int)        
   
#--load hard data
harddata_file = 'tbl29_pro.dat'
title,harddata_names,harddata = gu.loadGslibFile(harddata_file)
#print np.shape(harddata)




files = os.listdir('array_sk\\')
for file in files:
    print file
    new_array = np.zeros((new_nrow,new_ncol),dtype='float')+1.0e+32
    org_array = np.flipud(au.loadArrayFromFile(hm_nrow,hm_ncol,'array_sk\\'+file))
    for row in range(0,new_nrow):
        for col in range(0,new_ncol):
            new_array[row,col] =  org_array[map_y[row],map_x[col]]
    title = file.split('_')[0]+'_org.ref'
    au.plotArray(np.flipud(org_array),hm_delr,hm_delc,output='save',offset=offset,title=title,gpts=harddata[:,0:2])
    au.plotArray(np.flipud(new_array),new_delr,new_delc,offset=offset_new,output='save',title=title,gpts=harddata[:,0:2])
#    au.writeArrayToFile(np.flipud(new_array),title)
#    pylab.show()
    
