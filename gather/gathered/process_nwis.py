import sys
from datetime import datetime
import numpy as np
import xlrd
import shapefile

#--assume excel sorted by site number then by date

#--read the shapefile containing the requested data site
shp = shapefile.Reader('..\\GIS\\shapes\\broward_active_nwis_sites')
records = shp.records()
active_siteno,done_siteno = [],[]
siteno_idx = 1
for i,r in enumerate(records):
    active_siteno.append(str(r[siteno_idx]))
    done_siteno.append(False)
#print active_siteno

#--wl 
siteno_idx = 1
val_idx = 6
date_idx = 5
datum_idx = 7 
#--to convert to navd88
ngvd2navd = -1.5
fnames = ['broward_wl_result_data.xls']
for fn in fnames:
    wb = xlrd.open_workbook(fn)
    sh = wb.sheet_by_index(0)
    header_wl = sh.row_values(0)    
    prev = None
    for i in range(1,sh.nrows):
        row = sh.row_values(i)
        siteno = (row[siteno_idx])        
        if siteno in active_siteno:                            
            #print siteno
            date_tup = xlrd.xldate_as_tuple(row[date_idx],wb.datemode)
            date = datetime(year=date_tup[0],month=date_tup[1],day=date_tup[2])
            print row[val_idx]
            try:
                val = float(row[val_idx])
            except ValueError:
                val = 'NaN'                                            
            datum = row[datum_idx]
            if 'NGVD' in datum.upper() and val is not 'NaN':
                val += ngvd2navd                            
            if prev == None:
                outname = 'wl\\'+siteno+'.dat'
                f_out = open(outname,'w')                
            elif siteno != prev:
                f_out.close()
                outname = 'wl\\'+siteno+'.dat'
                f_out = open(outname,'w')                 
            f_out.write(date.strftime('%d/%m/%Y')+','+str(val)+'\n')
            prev = siteno                            
    f_out.close()                                                                                              
                    
#--qw                              
siteno_idx = 1
val_idx = 7
date_idx = 6
dtype_idx = 10

fnames = ['broward_qw_result_data_a.xls','broward_qw_result_data_b.xls']
for fn in fnames:
    wb = xlrd.open_workbook(fn)
    sh = wb.sheet_by_index(0)
    header_wl = sh.row_values(0)    
    prev = None
    for i in range(1,sh.nrows):
        row = sh.row_values(i)
        siteno = (row[siteno_idx])        
        if siteno in active_siteno:                            
            dtype = row[dtype_idx]
            date_tup = xlrd.xldate_as_tuple(row[date_idx],wb.datemode)
            date = datetime(year=date_tup[0],month=date_tup[1],day=date_tup[2])
            #print row[val_idx]
            try:
                val = float(row[val_idx])
            except ValueError:
                val = 'NaN'                                            
            if 'CHLORIDE' in dtype.upper():
                odir = 'qw\\chl\\'
            elif 'SPEC' in dtype.upper():
                odir = 'qw\\spcnd\\'
            elif 'SOLID' in dtype.upper():
                odir = 'qw\\tds\\'
            else:
                raise TypeError,dtype                                
                                      
            if prev == None:
                outname = odir+siteno+'.dat'
                f_out = open(outname,'w')                
            elif siteno != prev:
                f_out.close()
                outname = odir+siteno+'.dat'
                f_out = open(outname,'w')                 
            f_out.write(date.strftime('%d/%m/%Y')+','+str(val)+'\n') 
            prev = siteno                              
    f_out.close() 

                

            
            