import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas

ghb_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('stage','f4'),('conductance','f4'),('aux','a20')])

wel_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('flux','f4'),('aux','a20')])


def load_ascii_list(filename):    
    print filename  
    if 'ghb' in filename.lower():         
        arr = np.genfromtxt(filename,dtype=ghb_dtype,comments='|')   
    elif 'wel' in filename.lower(): 
        arr = np.genfromtxt(filename,dtype=wel_dtype,comments='|')   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr

def load_bin_list(filename):
    if 'ghb' in filename.lower():         
        arr = np.fromfile(filename,dtype=ghb_dtype)   
    elif 'wel' in filename.lower():
        arr = np.fromfile(filename,dtype=wel_dtype)   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr        


ascii_dirs = ['bro.02\\calibration\\flowlist\\','bro.02\\calibration\\seawatlist\\','bro.02\\prediction\\flowlist\\','bro.02\\prediction\\seawatlist\\']
bin_dirs = ['bro.02\\calibration\\flowlistbin\\','bro.02\\calibration\\seawatlistbin\\','bro.02\\prediction\\flowlistbin\\','bro.02\\prediction\\seawatlistbin\\']


date_fmt = '%Y%m%d'

for a_dir,b_dir in zip(ascii_dirs,bin_dirs):        
    afiles = os.listdir(a_dir)    
    for af in afiles:    
        dt = datetime.strptime(af.split('.')[0].split('_')[1],date_fmt)        
        bfile = af.split('.')[0]+'.bin'
        
        arr = load_ascii_list(a_dir+af)
        arr.tofile(b_dir+bfile)
        arr = load_bin_list(b_dir+bfile)
        print a_dir+af        