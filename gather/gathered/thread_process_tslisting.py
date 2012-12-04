#--to read and process the ts_listing.csv, which
#--contains all of the dbhydro records for the
#--model domain area.  It contains duplicates,
#--those get filtered out here.
import math
import sys
import os
import re
import shutil
import urllib2 
import subprocess
import multiprocessing as mp                                                     
from Queue import Queue                                                          
from threading import Thread                                                     
import threading                 
from datetime import datetime
import numpy as np


#--globals
source1 = 'http://www.sfwmd.gov/dbhydroplsql/web_io.report_process?v_period=uspec&v_start_date='
source2 = '&v_end_date='
source3 = '&v_report_type=format6&v_target_code=screen&v_run_mode=onLine&v_js_flag=Y&v_db_request_id=2996422&v_where_clause=&v_dbkey='
source4 = '&v_os_code=Win&v_interval_count=5'
#source = 'http://www.sfwmd.gov/dbhydroplsql/web_io.report_process?v_period=uspec&v_start_date=19910501&v_end_date=19980828&v_report_type=format6&v_target_code=screen&v_run_mode=onLine&v_js_flag=Y&v_db_request_id=2996422&v_where_clause=&v_dbkey=PT190&v_os_code=Win&v_interval_count=5'
start_re = re.compile('Time Series Data',re.IGNORECASE)
end_re = re.compile('Query returned',re.IGNORECASE)
    

def get_record(dbkey,sdate,edate):
    #--reads the return webpage for data
    #--uses re matching for the start and the end of the 
    #--data record.  splits the data record into
    #--header (first 3 non-blank lines) and data(remaining non-blank)
    #--checks to make sure all data records are read
    print 'getting record ',dbkey,'from ',sdate,' to',edate
    source = source1+sdate+source2+edate+source3+dbkey+source4    
    url = urllib2.urlopen(source)
    data = []
    nrec = -999
    while True:
        line = url.readline()
        if line == '':
            break
        if start_re.search(line) != None:
            while True:
                line = url.readline()
                if line == '':
                    break
                elif end_re.search(line) != None:                    
                    #--read number of records from query returned line
                    nrec = int(line.strip().split()[2])                    
                    break
                else:    
                    raw = line.strip().split()
                    if len(raw) > 0:
                        data.append(line.strip().split())   
    if len(data[3:]) != nrec:
        raise IndexError,'data record does not have the correct number of records'                                        
    return nrec,data  
        
        
def savetxt(fname,dlist):    
    f = open(fname,'w')
    for entry in dlist:       
        s = ','.join(entry)
        f.write(s+'\n')
    f.close()          


def worker(queue):
    #print queue.qsize()
    args = queue.get()
    #nrec,data = get_record(args[0],args[1],args[2])
    #savetxt(args[3],data)
    #for q in iter(queue.get, None):
    #for q in queue:
    #    print q

def main():                                                                      
    
    #--see if a restart flag was passed
    try:
        if sys.argv[1].upper() == 'R':
            restart = True
        else:
            restart = False
    except:
        restart = False                    
    if restart:
        print 'Using existing dir and files'
    
    
    #--a dict of data types that are of interest
    use_dtypes = {'GW':['PSI','WELL'],'SW':['BOARD','FLOW','GATE','RPM','STG'],'RAIN':['RAIN']}
    
    #--create the directory structure
    if restart is False:
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
    
    
    #--get a list of file names and dbkeys to retrieve
    #--build queue_args = [[dbkey,sdate,edate,fname]]
    dbkeys = []
    fnames = []
    queue_args = []
    for i,line in enumerate(f):
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
        #--fix the dbkey since excel is a giant turd and removes leading '0's
        if len(dbkey) < 5:
            dbkey = '%05d'%int(dbkey)
            #print dbkey 
            #break     
            
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
            s = datetime.strptime(sdate,'%d-%b-%Y')
            sdate2 = s.strftime('%Y%m%d')            
            e = datetime.strptime(edate,'%d-%b-%Y')
            edate2 = e.strftime('%Y%m%d')
            #--build the output file name
            station_mod = station.replace('.','_')
            station_mod = station_mod.replace(' ','_')
            fname = dir1+dir2+station_mod+'.'+freq+'.'+stat+'.'+opnum+'.'+sdate2+'.'+edate2+'.'+struc+'.dat'        
            
            if restart:
                #--check that this fname doesn't exist
                if os.path.exists(fname) == False and fname not in fnames:
                    queue_args.append([dbkey,sdate2,edate2,fname])                                
                    fnames.append(fname)
            #--if not restart
            else:    
                if fname not in fnames:
                    queue_args.append([dbkey,sdate2,edate2,fname])                                
                    fnames.append(fname)                                                          

    print 'number of records to retrieve:',len(fnames)                    
    #    nrec,data = get_record(dbkey,sdate2,edate2)                        
    #--multiprocessing
    #--number of cores to use for threading
    num_cores = 8            
    
    #--some integer math tricks to load balance
    min_recthread = len(fnames)/(num_cores)
    extra_recthread = len(fnames) - (min_recthread*(num_cores))
    print 'minimum number of records for each thread:',min_recthread
    print 'extra records for each thread:',extra_recthread
    
    #--build the queue and create threads
    qlist = []
    threads = []
    prev = 0
    for i in range(num_cores):
        #--some integer math tricks to load balance
        if i < extra_recthread-1:
            recthread = min_recthread + 1
        else:
            recthread = min_recthread
                                            
        s_idx,e_idx = prev + 1,prev + recthread
        #print i,s_idx,e_idx,e_idx-s_idx
        #print queue_args[s_idx],queue_args[e_idx]
        q = Queue()                                                                  
        for qu in queue_args[s_idx:e_idx]:
            q.put_nowait(qu)
        q.put_nowait(None)                
        threads.append(Thread(target=worker,args=(q,)))
        prev = e_idx
    
    #--start the threads
    for t in threads:
        t.daemon = True
        t.start()
    #--block until all threads finish
    for t in threads:
        t.join() 
        print t.name,'Finished'       
                                     
   
if __name__ == '__main__':                                                       
    mp.freeze_support() # optional if the program is not frozen                  
    main()   
            
        
