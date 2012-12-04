import os
import re
import shutil
from datetime import datetime

#--a dict of data types that are of interest
use_dtypes = {'GW':['PSI','WELL'],'SW':['BOARD','FLOW','GATE','RPM','STG'],\
              'RAIN':['RAIN'],'EVAP':['EVAP','ETP','ETPI']}

for key,val in use_dtypes.iteritems():
            if os.path.exists(key):
                shutil.rmtree(key)
            os.mkdir(key)
            for v in val:       
                os.mkdir(key+'\\'+v)

#--the time series listing CSV from dbhydro
fname = 'ts_listing.csv'
f = open(fname,'r')
header = f.readline().strip().split(',')

#--original data dir
odir = '_data_backup\\'
    
#--some column indices
idx = {}
idx['dbkey'] = 0 
idx['station'] = 1 
idx['dtype'] = 3
idx['freq'] = 4
idx['stat'] = 5
idx['sdate'] = 8
idx['edate'] = 9
idx['opnum'] = 12
idx['basin'] = 17
idx['struc'] = 18
    
    
dbkeys = []
fnames = []
missing = []
for i,line in enumerate(f):
    line = line.replace('"','')
    raw = line.strip().split(',')
    dbkey = raw[idx['dbkey']].strip()    
    station = raw[idx['station']].strip()    
    freq = raw[idx['freq']].strip()            
    stat = raw[idx['stat']].strip()            
    sdate = raw[idx['sdate']].strip()            
    edate = raw[idx['edate']].strip()            
    dtype = raw[idx['dtype']].strip()            
    opnum = raw[idx['opnum']].strip()
    struc = raw[idx['struc']].strip()
    #--fix the dbkey 
    if len(dbkey) < 5:
        dbkey = '%05d'%int(dbkey)          
            
    #--check if this is some data we want
    dir1,dir2 = None,None
    for key,val in use_dtypes.iteritems():
        if dtype in val:
            dir1 = key+'\\'
            dir2 = dtype+'\\'
            break
    #--if this isn't a dup and it is a data type we want and it has valid date ranges    
    if dbkey not in dbkeys and dir1 != None and sdate != '' and edate != '':
        #--if opnum is null, make it 1
        if opnum == '':
            opnum = '1'        
                        
        dbkeys.append(dbkey)        
        #--convert sdate and edate to dbhydro format 
        dfmt = '%d-%b-%Y'           
        s = datetime.strptime(sdate,dfmt)
        sdate2 = s.strftime('%Y%m%d')            
        e = datetime.strptime(edate,dfmt)
        edate2 = e.strftime('%Y%m%d')
        #--build the output file name
        station_mod = station.replace('.','_')
        station_mod = station_mod.replace(' ','_')
        fname = dir1+dir2+station_mod+'.'+freq+'.'+stat+'.'+opnum+'.'+\
                sdate2+'.'+edate2+'.'+struc+'.dat'  
        
        print 'processing file: ',fname
        
        #--check if station has a ' '
        if ' ' in station: 
            #--get number of spaces in station
            num_space = len(station.strip().split()) - 1           
            print 'repairing...'
            fnames.append(fname)
            #--open the existing file
            f = open(odir+fname,'r')            
            #--fix the primary header
            header1,values1 = f.readline().strip().split(','),f.readline().strip().split(',')
            h_idx = header1.index('STATION')
            for n in range(num_space):
                values1[h_idx] = values1[h_idx]+'_'+values1[h_idx+1]
                values1.pop(h_idx+1)
            dtype = values1[header1.index('TYPE')]
            freq = values1[header1.index('FQ')]
            
            #-read the record header
            header2 = f.readline().strip().split(',')
            #--find the index of 'station' - watch out for variable case
            h_idx = None
            for i,h2 in enumerate(header2):
                if re.search(h2,'station',re.I) is not None:
                    h_idx = i
                    break
            if h_idx is None:
                raise IndexError,'"station" attribute not found in record header'
            #--fix the records
            #--check for breakpoint records that don't really have the station as an attribute - BK evap and precip records
                        
            recs = []
            for line in f:
                rec = line.strip().split(',')
                if dtype in ['EVAP','RAIN'] and freq == 'BK':
                    recs.append(rec)
                else:
                    for n in range(num_space):
                        rec[h_idx] = rec[h_idx]+'_'+rec[h_idx+1]
                        rec.pop(h_idx+1)
                    recs.append(rec)
            f.close()

            #--write out the repaired file
            new_fname = dir1+dir2+dbkey+'.'+station_mod+'.'+freq+'.'+stat+'.'+opnum+'.'+\
                sdate2+'.'+edate2+'.'+struc+'.dat'  
        
            f_out = open(new_fname,'w')
            f_out.write(','.join(header1)+'\n')
            f_out.write(','.join(values1)+'\n')
            f_out.write(','.join(header2)+'\n')
            for rec in recs:
                f_out.write(','.join(rec)+'\n')
            f_out.close()            
        else:            
            new_fname = dir1+dir2+dbkey+'.'+station_mod+'.'+freq+'.'+stat+'.'+opnum+'.'+\
                sdate2+'.'+edate2+'.'+struc+'.dat' 
            
            if os.path.exists(odir+fname):
                shutil.copy(odir+fname,new_fname)
            else:
                print 'MISSING: ',fname
                missing.append(fname+'.'+dbkey)


f_out = open('repaired_files.dat','w')
for fname in fnames:
    f_out.write(fname+'\n')
f_out.close()    
f_out = open('missing.dat','w')
for m in missing:
    f_out.write(m+'\n')
f_out.close()

          