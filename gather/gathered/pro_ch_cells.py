import numpy as np
import arrayUtil as au

file = 'Export_Output_3.txt'
data = np.loadtxt(file,delimiter=',',skiprows=1,usecols=(1,2))

size = np.shape(data)
#print size
data = data - 1

nrow,ncol = 301,501

ibnd_l1 = np.ones((nrow,ncol),dtype='int')
ibnd = np.ones((nrow,ncol),dtype='int')
ibnd_l1[data[:,0].astype(int),data[:,1].astype(int)] = -1

for row in range(0,nrow):
    east_ch = np.argwhere(ibnd_l1[row,:]==-1)[-25]
    #print east_ch
    ibnd_l1[row,east_ch:] = 0
    ibnd[row,east_ch] = -1
    ibnd[row,east_ch+1:] = 0
    
au.plotArray(ibnd,500,500) 
au.plotArray(ibnd_l1,500,500)

au.writeArrayToFile(ibnd_l1,'ibound_l1.ref',oFormat='i',nWriteCol=30)
au.writeArrayToFile(ibnd,'ibound.ref',oFormat='i',nWriteCol=30)
