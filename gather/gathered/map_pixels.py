import sys
import os
import re
from datetime import datetime
import numpy as np
import shapefile


#--no unit conversions - faster to post process with numpy

rst = False
try:
    if sys.argv[1].upper() == 'R':
        rst = True
except:
    pass           

arr_prefix = 'nexrad_rech_inch_day\\rech'
pixel_file = 'pixel_data\\nexrad_inc138246_96_12_rainfall_ord.dat'

#arr_prefix = 'mm_day_pet\\pet'
#pixel_file = 'pet_pixel_all_ord.txt'

#--name of model grid shapefile with pixels attached - from make_pixel_map.py
print 'loading grid shapefile...'
shapefile_name = '..\\..\\_gis\\shapes\\broward_grid_master'
shapes,records = shapefile.load_as_dict(shapefile_name,attrib_name_list=['row','column','pixels','fractions'])
nrow,ncol = records['row'].max(),records['column'].max()        
print 'done'
print 'nrow,ncol',nrow,ncol

#--load the pixel timeseries with 
#--pixel, value and ord date index values for the timeseries file
p_idx,v_idx,d_idx = 0,1,2 
print 'loading pixel timeseries file',pixel_file
pixel = np.loadtxt(pixel_file,usecols=[0,2,3],delimiter=',')
print 'done - ',pixel.shape[0],' records loaded'

#--get a list of the unique ordinal days in pixel time series
pixel_days = np.unique(pixel[:,d_idx])

#--process each day    
missing_pixel_list = []
for i,d in enumerate(pixel_days):
    dt = datetime.fromordinal(int(d))
    dt_str = dt.strftime('%Y%m%d')
    print 'processing day',dt,'(',i+1,' of ',pixel_days.shape[0],')'   
    aname = arr_prefix+dt_str+'.ref'
    if rst and os.path.exists(aname):
        print 'found existing array...skipping'
    else:                
        #--a slice of pixels containing all of the pixels for this day
        pixels_this_day = pixel[np.where(pixel[:,d_idx]==d),:][0,:,:]                  
        #--an empty array for storing the mapped array
        arr = np.zeros((nrow,ncol))
        #--fill the array
        for r,c,plist,flist in zip(records['row'],records['column'],records['pixels'],records['fractions']):       
            val = 0.0        
            #--loop over each pixel/fraction value for this cell and accum into val
            for p,f in zip(plist.split(),flist.split()):
                #--the value for pixel p on this day
                v = pixels_this_day[np.where(pixels_this_day[:,p_idx]==int(p)),v_idx]  
                #print p,v              
                val += v[0][0]*float(f)
            arr[r-1,c-1] = val                                                    
        np.savetxt(aname,(arr),fmt=' %14.7e')       
    #break
