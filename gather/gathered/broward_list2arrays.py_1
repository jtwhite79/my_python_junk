import sys
import os
import numpy as np

'''writes nexrad,BLU arrays from list files
'''

def list_2_array(list_filename,maparray_filename,mapcol=0,bin=False,prefix='',dir='',warn=True):
    

    #--check for existence
    assert os.path.exists(list_filename),'List File not found: '+str(list_filename)
    assert os.path.exists(maparray_filename),'Interger mapping array not found: '+str(maparray_filename)

    #--read the 2 header lines of list file.  The first one is just column names, 
    #-- the second one is the name of the array to write for each data column
    f = open(list_filename,'r')
    header1 = f.readline().strip().split()
    header2 = f.readline().strip().split()

    #--load the remaining rows of the list file    
    pt_data = np.loadtxt(f)
    f.close()

    #--get the mapping points
    pt_map = pt_data[:,mapcol]

    #--load mapping array
    array_map = np.loadtxt(maparray_filename)

    #--iterate over h2
    for j,h2 in enumerate(header2):
        if h2.upper() != 'NONE' and j != mapcol:
            h2 = dir + prefix + h2
            arr = np.zeros_like(array_map) - 1.0e+30
            for i,pt in enumerate(pt_map):
                arr[np.where(array_map==pt)] = pt_data[i,j]
                pass
            #--check for unmapped cells
            if warn:
                if arr[np.where(arr==-1.0e+30)].shape[0] != 0:
                    print 'warning -- unmapped cells in array',h2
            #--save the array
            if bin:
                arr = arr.astype(np.float32)
                arr.tofile(h2)
            else:
                np.savetxt(h2,arr,fmt=' %20.8E')



if __name__ == '__main__':
    #--parse commandline args
    list_filename = sys.argv[1]
    maparray_filename = sys.argv[2]
    list_2_array(list_filename,maparray_filename)


