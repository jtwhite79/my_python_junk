import sys
import numpy as np


def loadArrayFromFile(nrow,ncol,file):	
    file_in = open(file,'r')	
    data = np.zeros((nrow*ncol)) - 1.0e+30
    d = 0
    while True:
        line = file_in.readline()
        if line is None or d == nrow*ncol:break
        raw = line.strip('\n').split()        
        for a in raw:            
            try:
                data[d] = float(a)
            except:
                raise TypeError('error casting to float: '+str(a))				
            if d == (nrow*ncol)-1:
                file_in.close()
                #data = np.array(data)
                data.resize(nrow,ncol)
                return(data)                                                                			
            d += 1	
    file_in.close()
    #data = np.array(data)
    data.resize(nrow,ncol)
    return(data)

fname = sys.argv[1]
nrow,ncol = 411,501
arr = loadArrayFromFile(fname,nrow,ncol)
np.savetxt(fname,arr,fmt='%15.6e')