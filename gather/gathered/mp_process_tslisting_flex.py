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
import httplib
import subprocess
import signal
import multiprocessing as mp 
from Queue import Queue                                                          
from datetime import datetime,timedelta
import numpy as np


#--globals - shouldn't need to change these
source1 = 'http://www.sfwmd.gov/dbhydroplsql/web_io.report_process?v_period=uspec&v_start_date='
source2 = '&v_end_date='
source3 = '&v_report_type=format6&v_target_code=screen&v_run_mode=onLine&v_js_flag=Y&v_db_request_id=2996422&v_where_clause=&v_dbkey='
source4 = '&v_os_code=Win&v_interval_count=5'
start_re = re.compile('Time Series Data',re.IGNORECASE)
end_re = re.compile('Query returned',re.IGNORECASE)
    

def get_record(dbkey,sdate,edate,timeout=120.,header=True):
    #--reads the return webpage for data
    #--uses re matching for the start and the end of the 
    #--data record.  splits the data record into
    #--header (first 3 non-blank lines) and data(remaining non-blank)
    #--checks to make sure all data records are read
    
    #print 'with timeout',timeout
    source = source1+sdate+source2+edate+source3+dbkey+source4                
    url = urllib2.urlopen(source,timeout=timeout)    
    data = []
    nrec = -999
    while True:
        line = url.readline()
        if line == '':
            break
        if start_re.search(line) != None:
            while True:
                line = url.readline() 
                #print line
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
    url.close()                        
    if nrec == -999:
        raise LookupError,'nrec not found, probably blank record'+\
                          ' for request dates'    
    if len(data[3:]) != nrec:        
        raise IndexError,'data record does not have the'+\
                         'correct number of records'                                        
    
    print 'success - record ',dbkey,'from ',sdate,' to',edate
    if header:
        return nrec,data  
    else:
        return nrec,data[3:]        
        

def get_record_split(dbkey,sdate,edate,isRecurs=False,needHeader=True):
    #--reads the return webpage for data
    #--uses re matching for the start and the end of the 
    #--data record.  splits the data record into
    #--header (first 3 non-blank lines) and data(remaining non-blank)
    #--checks to make sure all data records are read
    #--splits up the dates to (hopefully) increase throughput
    #--can be recursive
    
    #--first request a really short record just to get the header 
    if needHeader:
        try:
            this_nrec,this_data = get_record(dbkey,sdate,sdate,header=True)
        except:
            print 'could not get header info on recursive call:',dbkey
            raise IndexError        
        header = this_data[:3]
    else:
        header = []
    #--number of splits in the time interval to try
    num_split = 10
    #--date casting
    syear,eyear = sdate[:4],edate[:4]       
    s = datetime.strptime(sdate,'%Y%m%d')
    e = datetime.strptime(edate,'%Y%m%d')
    #--use the timedelta objects
    tdelta = e - s       
    tdelta_split = tdelta / num_split    
    tdelta_day = timedelta(days=1)    
    
    #--fail if this is the smallest recursive level that will be used 
    if int(tdelta.days) < 1:
        print 'requested record length less than one day'      
        raise IndexError,'Error retrieving record:'+str(dbkey)
    
    #--if the splits are less than a day, reset to day
    #--if one of these fails, it will trigger the above exception
    if int(tdelta_split.days) < 1:
        print 'requested record length less than one day'
        #raise IndexError,'Error retrieving record:'+str(dbkey)
        num_split = int(tdelta.days)
        tdelta_split = tdelta_day
            
    #--loop over the splits
    prev = s
    data = []
    nrec = 0    
    for i in range(num_split):
        sd = prev
        sd_str = sd.strftime('%Y%m%d')
        #--if this is the last split, make sure we get the end of the record
        if i == num_split-1:
            ed_str = edate        
        else:            
            ed = sd + tdelta_split - tdelta_day
            ed_str = ed.strftime('%Y%m%d')              
            prev = ed + tdelta_day
        print tdelta.days,tdelta_split.days,sd_str,ed_str        
        
        #--call get_record with the reduced interval
        try:            
            this_nrec,this_data = get_record(dbkey,sd_str,ed_str,\
                                             header=False)
        #--an index error means nrec doesn't match number of records
        except IndexError:            
            raise IndexError,'Error retrieving record:'+str(dbkey)
            
        #--lookup or badstatusline error means that the record was blank
        except (LookupError,httplib.BadStatusLine) as e:
            this_nrec = 0
            this_data = []           
        
        #--URLError means a timeout, so keep recursing            
        except:            
            if isRecurs:                              
                #--call recursively
                print 'recursive call timeout on dbkey:',dbkey
                try:
                    this_nrec,this_data = get_record_split(dbkey,sd_str,\
                                                       ed_str,isRecurs=True,
                                                       needHeader=False)                
                except IndexError:
                    raise IndexError                                                       
                except LookupError:
                    pass
                #--pop the first three elements (header) off
                #this_data.pop(0)                   
                #this_data.pop(0)
                #this_data.pop(0)
            else:
                raise IndexError,'Error retrieving record:'+str(dbkey)   
                                                                     
        #print i,this_nrec
        data.extend(this_data)
        nrec += this_nrec                               
    #--no header yet
    if len(data) != nrec and raiseEx:
        raise IndexError,'data record does not have the correct number of records'  
    header.extend(data)
    return nrec,header        
    
          
def savetxt(fname,dlist):    
    f = open(fname,'w')
    for entry in dlist:       
        s = ','.join(entry)
        f.write(s+'\n')
    f.close()          
    
def worker(jobq,failq,pid):    
    #--jobq has the job args, failq is to track failed retrievals
    rec_count  = 0
    while True:   
        args = jobq.get()
        #--check for sentinel
        if args is None:
            break
        rec_count += 1
        #print pid,rec_count,args[0]
        try:            
            nrec,data = get_record(args[0],args[1],args[2])            
            savetxt(args[3],data)     
                                  
        except IndexError:
            print 'record retrieval failure:',args[0]
            failq.put_nowait(args)                           
        except LookupError:
            print 'blank record:',args[0] 
        except:
            print 'initial timeout on dbkey:',args[0]
            try:               
                nrec,data = get_record_split(args[0],args[1],args[2],\
                                             isRecurs=True)
                savetxt(args[3],data)     
            except IndexError:
                print 'recursive record retrieval failure:',args[0]
                failq.put_nowait(args)                                                                     
        jobq.task_done()
    #--sentinel task is done
    jobq.task_done()        






#-------------------------------------------------------------------------------        






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
    
    
    #--a dict of data types that are of interest - these become nested folders
    use_dtypes = {'GW':['PSI','WELL'],'SW':['BOARD','FLOW','GATE','RPM','STG'],\
                  'RAIN':['RAIN'],'EVAP':['EVAP','ETP','ETPI']}
    
    #--create the directory structure
    if restart is False:
        for key,val in use_dtypes.iteritems():
            if os.path.exists(key):
                shutil.rmtree(key)
            os.mkdir(key)
            for v in val:       
                os.mkdir(key+'\\'+v)
    else:
        for key,val in use_dtypes.iteritems():
            if not os.path.exists(key):
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
            fname = dir1+dir2+station_mod+'.'+freq+'.'+stat+'.'+opnum+'.'+\
                    sdate2+'.'+edate2+'.'+struc+'.dat'        
            
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
    
    #--multiprocessing
    #--number of process to spawn - do my bidding!
    num_procs = 20
        
    #--create a queue for jobs and to track failed retrievals
    jobq = mp.JoinableQueue()
    failq = mp.Queue()
    
    #--create and start the process instances
    procs = []
    for i in range(num_procs):
        #--pass the woker function both queues and a PID
        p = mp.Process(target=worker,args=(jobq,failq,i+1))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)       
        
    #--add the args to the queue
    for qa in queue_args:
        jobq.put(qa)
        #break
    
    #--add the sentinels so processes know when to terminate
    for p in procs:
        jobq.put(None)    
        
    #--block until all finish
    for p in procs:
        p.join() 
        print p.name,'Finished'       
    
    #--process the failed retrievals
    failq.put_nowait(None)
    f_out = open('failed.dat','w')
    for args in iter(failq.get,None):
        f_out.write(args[0]+'\n')
    f_out.close()        

       
if __name__ == '__main__':                                                       
    mp.freeze_support()               
    main()   
            
        
