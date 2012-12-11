import os
import numpy as np
import multiprocessing as mp 
from Queue import Queue         
import arrayUtil as au

def loadArrayFromFile(nrow,ncol,file):	
    file_in = open(file,'r')	
    data = np.zeros((nrow*ncol)) - 1.0e+30
    d = 0
    while True:
        line = file_in.readline()
        if line is None or d == nrow*ncol:break
        raw = line.strip('\n').split()        
        for a in raw:            
            try:
                data[d] = float(a)
            except:
                raise TypeError('error casting to float: '+str(a))				
            if d == (nrow*ncol)-1:
                file_in.close()
                #data = np.array(data)
                data.resize(nrow,ncol)
                return(data)                                                                			
            d += 1	
    file_in.close()
    #data = np.array(data)
    data.resize(nrow,ncol)
    return(data)

def worker(jobq,id):
    nrow,ncol = 411,501
    fdir = 'point_rech_inch_day\\'
    newdir = 'temp\\'
    while True:
        args = jobq.get()
        if args == None: 
            break        
        print args 
        arr = loadArrayFromFile(nrow,ncol,fdir+args)         
        print arr.shape
        np.savetxt(newdir+args,arr,fmt='%15.3e')          
        jobq.task_done()
    jobq.task_done()  
    return      
    	
	
	
def main():
    fdir = 'point_rech_inch_day\\'
    files = os.listdir(fdir)    
    jobq = mp.JoinableQueue()
    procs = []
    nprocs = 8
    for i in range(nprocs):
        #--pass the woker function both queues and a PID
        p = mp.Process(target=worker,args=(jobq,i+1))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)       
        
    #--add the args to the queue
    for f in files:
        jobq.put(f)
        #break
    
    #--add the sentinels so processes know when to terminate
    for p in procs:
        jobq.put(None)    
        
    #--block until all finish
    for p in procs:
        p.join() 
        print p.name,'Finished'       
        
if __name__ == '__main__':                                                       
    mp.freeze_support() # optional if the program is not frozen                  
    main()       