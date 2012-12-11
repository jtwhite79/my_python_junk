import os

fdir = 'point_rech_inch_day\\'
prefix = 'pt_'
files = os.listdir(fdir)
for f in files:  
    print f      
    os.rename(fdir+f,fdir+prefix+f)
    
    
    