import multiprocessing as mp

def worker(jobq,resultq,pid):
    while True:
        args = jobq.get()
        #--check for sentinel
        if args == None:
            print pid,'exiting'
            break
        num1 = args[0]
        num2 = args[1]
        result = num1 * num2
        resultq.put_nowait([num1,num2,result])
        jobq.task_done()
    jobq.task_done()
    resultq.put_nowait(None)
    return


def main():
    jobq = mp.JoinableQueue()
    resultq = mp.Queue()
    num_tasks = 472
    num_procs = 10

    for i in range(num_tasks):
        jobq.put_nowait([i,i*2])
    #--sentinel tasks
    for i in range(num_procs):
            jobq.put_nowait(None) 
                    
    #--start processes 
    procs = []                   
    for i in range(num_procs):
        p = mp.Process(target=worker,args=(jobq,resultq,i))
        p.daemon = True
        p.start()
        procs.append(p)
    
    num_sentinels = 0
    results = []
    while True:
        r = resultq.get()
        if r == None:
            num_sentinels += 1
            if num_sentinels == num_procs:
                break
        else:
            results.append(r)
                 
    #--block until all fini
    for p in procs:
        p.join() 
        print p.name,'Finished'                         
                            
    #--process the results queue
    results = []
    while True:
        try:            
            r = resultq.get_nowait()   
            results.append(r)            
        except:
            break        
    return

if __name__ == '__main__':                                                       
    mp.freeze_support() 
    main()     