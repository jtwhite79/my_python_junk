import numpy as np
import shapefile

from bro import flow


def load_shape_arrays(shapename,rowname='row',colname='column'):
    #--get the field names and make sure rowname and colname are found
    field_names = shapefile.get_fieldnames(grid_shapename)
    assert rowname in field_names
    assert colname in field_names

    #--get the decimal of each field - to get the array type later
    grid_shp = shapefile.Reader(shapename)
    header = grid_shp.dbfHeader()
    h_dict = {}
    for item in header:
        h_dict[item[0]] = int(item[-1])


    #--load all of the records as a dict
    records = shapefile.load_as_dict(shapename,loadShapes=False)
    
    #--get nrow and ncol
    nrow = max(records[rowname])
    ncol = max(records[colname])

    #--row and column maps
    row,col = records[rowname],records[colname]

    #--setup a dict for all of the arrays and map the values
    array_dict = {}
    for key,record in records.iteritems():
        
        decimal = h_dict[key]
        if decimal == 0:
            arr = np.zeros((nrow,ncol),dtype=np.int)               
        else: 
            arr = np.zeros((nrow,ncol))            
        print key,arr.dtype            
        try:
            for r,c,val in zip(row,col,record):
                arr[r-1,c-1] = val
            array_dict[key] = arr.copy()
        except:
            print 'couldnt cast '+str(key)+' field to array'
    


    return array_dict



#--load arrays from grid shapefile - very slow
grid_shapename = '..\\..\\_gis\\shapes\\broward_grid_master'
array_dict = load_shape_arrays(grid_shapename)
#--save the arrays to the "ref" folder
ref_dict = {}
for key,array in array_dict.iteritems():
    aname = flow.ref_dir+'gridmaster\\'+str(key)+'.ref'
    print aname
    ref_dict[key] = aname
    if array.dtype == np.int:
        np.savetxt(aname,array,fmt=' %4.0f')
    else:
        np.savetxt(aname,array,fmt=' %15.6f')
