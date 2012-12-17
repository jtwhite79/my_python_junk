import os
import sys
from datetime import datetime,timedelta
import multiprocessing as mp
import numpy as np
from bro_pred import flow

def worker(jobq,pid):
    #--args[0] = output_filename
    #--args[1] = list of array file names to load and read
    
    while True:
        args = jobq.get()
        if args == None:
            break        
        astats = []
        tot = np.zeros((flow.nrow,flow.ncol))
        for aname in args[1]:            
            a = np.fromfile(aname,dtype=np.float32)
            a.resize(flow.nrow,flow.ncol)      
            tot += a
        print '----'+args[0]                   
        tot /= float(len(args[1]))              
        tot = tot.astype(np.float32)
        tot.tofile(args[0])
        jobq.task_done()        
    jobq.task_done()
    return        


def main():
    print 'grouping flow model rch files by month'
    rch_start,rch_end = datetime(year=2002,month=1,day=1),datetime(2012,month=1,day=1)
    rch_dir = '..\\..\\_model\\bro.02\\flowref\\rch\\'
    rch_files = os.listdir(rch_dir)
    rch_monthly = {}
    for rfile in rch_files:
        print 'processing file',rfile,'\r',        
        dt = datetime.strptime(rfile.split('.')[0].split('_')[-1],'%Y%m%d')
        if dt >= rch_start and dt <= rch_end:
            if dt.month not in rch_monthly.keys():
                rch_monthly[dt.month] = [rch_dir+rfile]
            else:
                rch_monthly[dt.month].append(rch_dir+rfile)
    
    
    print 'calculating average monthly rch arrays for period',rch_start,rch_end  
    aprefix = flow.ref_dir+'rch\\rch_'      
    monthly_names = {}    
    q_args = []
    for imonth,rfiles in rch_monthly.iteritems():
        
        aname = aprefix+str(imonth)+'.ref'
        monthly_names[imonth] = aname
        q_args.append([aname,rfiles])
        tot = np.zeros((flow.nrow,flow.ncol))
        #for rfile in rfiles:
        #    rcharr = np.fromfile(rfile,dtype=np.float32)
        #    rcharr.resize(flow.nrow,flow.ncol)       
        #    tot += rcharr
        #tot /= float(len(rfiles))
       

    #--use multiprocessing to speed things up
    jobq = mp.JoinableQueue()  
    procs = []
    num_procs = 4
    
    for i in range(num_procs):
        #--pass the woker function both queues and a PID
        p = mp.Process(target=worker,args=(jobq,i))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)
    
    for q in q_args:
        jobq.put(q)

    for p in procs:
        jobq.put(None)      

    #--block until all finish
    for p in procs:
        p.join() 
        print p.name,'Finished'    
                           
    f = open(flow.root+'.rch','w')
    f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    #f.write(' {0:9.0f} {1:9.0f}\n'.format(0,0))
    f.write(' {0:9.0f} {1:9.0f}\n'.format(3,flow.rch_unit))

    i = 1
    print 'processing stress periods'    
    for start,splen in zip(flow.sp_start,flow.sp_len):
        print 'stress period',i,'\r',
        #--write rch file entry
        outname = monthly_names[start.month]
        f.write(' {0:9.0f} {1:9.0f}'.format(1,0)+'  #STRESS PERIOD '+str(i)+' '+str(start)+'\n')
        f.write('OPEN/CLOSE '+outname+' {0:9.4f} (BINARY)  -1\n'.format(flow.rch_mult))                  
        i += 1
if __name__ == '__main__':                                                           
    main()   
