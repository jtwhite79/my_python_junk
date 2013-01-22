import sys
import os
import multiprocessing as mp 
from Queue import Queue 
import shutil


def worker(jobq,pid):
    '''
    args[0] = in file name
    args[1] = out file name   
    '''
    while True:
        #--get some args from the queue
        args = jobq.get()
        #--check if this is a sentenial
        if args == None:
            break
        shutil.copy(args[0],args[1])
        jobq.task_done()
        print 'worker',pid,' finished',args[0]

    #--mark the sentenial as done
    jobq.task_done()
    return


def master():
    #--dir of arrays    
    in_dir = 'pet_mm_day\\'
    out_dir = 'temp\\'
    files = os.listdir(in_dir)
    
    #--build a queue args
    q_args = []
    for f in files:
        f_new = 'pet_'+f[3:]
        if not os.path.exists(in_dir+f_new):
            q_args.append([in_dir+f,out_dir+f_new])
        #break
       
    jobq = mp.JoinableQueue()  

    #--for testing
    #jobq.put_nowait(q_args[0])
    #worker(jobq,1)  
    #return  
    
    procs = []
    num_procs = 6
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
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
    return


if __name__ == '__main__':                                                                       
    master()                      
