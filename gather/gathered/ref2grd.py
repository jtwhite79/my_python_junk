import os
import numpy as np
import arrayUtil as au

nrow,ncol = 301,501
offset = [728604.,577348.]
delt = 500

path = 'output_arrays\\'
files = os.listdir(path)

for file in files:
    print file
    array = au.loadArrayFromFile(nrow,ncol,path+file) 
    f_out = path+file.split('.')[0]+'.asc'
    print f_out
    f = open(f_out,'w')
    f.write('ncols '+str(ncol)+'\n')
    f.write('nrows '+str(nrow)+'\n')
    f.write('xllcorner '+str(offset[0])+'\n')
    f.write('yllcorner '+str(offset[1])+'\n')
    f.write('cellsize '+str(delt)+'\n')
    f.write('nodata_value -9999\n')
    au.writeArrayToFile(array,f,nWriteCol=ncol) 
    f.close()
    