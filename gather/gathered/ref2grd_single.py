import numpy as np
import arrayUtil as au


nrow,ncol = 301,501
offset = [728604.,577348.]
delt = 500


array = au.loadArrayFromFile(nrow,ncol,'ref\\icbnd_l1.ref') 
array[:,:390] = 0
f_out = 'icbnd.asc'
f = open(f_out,'w')
f.write('ncols '+str(ncol)+'\n')
f.write('nrows '+str(nrow)+'\n')
f.write('xllcorner '+str(offset[0])+'\n')
f.write('yllcorner '+str(offset[1])+'\n')
f.write('cellsize '+str(delt)+'\n')
f.write('nodata_value -9999\n')
au.writeArrayToFile(array,f,nWriteCol=ncol) 
f.close()