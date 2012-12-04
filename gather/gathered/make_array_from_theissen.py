import os
import sys
import numpy as np
import shapefile


#--the names of the dbf attributes
row_name = 'row'
col_name = 'column'
key_name = 'new_key'
joincount_name = 'Join_Count'

nrow,ncol = 411,501

#--get a list of theissen shapes
#directory = 'theiseen_dir\\'
#files = os.listdir(directory)
#shp_files = []
#for f in files:
#    if f.endswith('shp')
#    shp_files.append(f.split('.')[0])

shp_files = ['ConfigT_config_2916grid']
array_directory = 'refs\\'
try:
    os.mkdir(array_directory)
except:
    pass
#--start main loop
for s in shp_files:
    
    #--initialize this array
    this_array = np.zeros((nrow,ncol)) - 999                    
    
    #--shape object
    shp_poly = shapefile.Reader(shapefile=s)    
    header = shp_poly.dbfHeader()        
    
    #--get the index of the row,col,dbkey - might be different for each theissen file
    row_idx,col_idx,key_idx,jc_idx = None,None,None,None
    for h_idx in range(len(header)):
        #print header[h_idx][0]
        if header[h_idx][0] == row_name:
            row_idx = h_idx
        elif header[h_idx][0] == col_name:
            col_idx = h_idx
        elif header[h_idx][0] == key_name: 
            key_idx = h_idx               
        elif header[h_idx][0] == joincount_name:
            jc_idx = h_idx
    
    
    #--loop over each record in the shapefile
    for rec_idx in range(shp_poly.numRecords):
        
        #--get the attribute record
        rec = shp_poly.record(rec_idx)
                               
        #--get the needed attributes
        this_row = rec[row_idx]
        this_col = rec[col_idx]
        this_key = rec[key_idx]
        this_jc = rec[jc_idx]
        
        #--if the join count is greater than 0
        if this_jc > 0:        
            #--assign to the array
            this_array[this_row-1,this_col-1] = this_key
      
    np.savetxt(array_directory+s+'.ref',this_array,fmt='%5.0f')

    
          
    