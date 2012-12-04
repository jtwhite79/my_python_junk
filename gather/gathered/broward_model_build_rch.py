import os
import sys
from datetime import datetime,timedelta
import multiprocessing as mp
import numpy as np
from bro import flow

def worker(jobq,pid):
    #--args[0] = output_filename
    #--args[1] = list of array file names to load and read
    
    while True:
        args = jobq.get()
        if args == None:
            break        
        astats = []
        tot = np.loadtxt(args[1][0])
        for aname in args[1][1:]:
            a = np.loadtxt(aname)            
            tot += a
        print '----'+args[0]                   
        tot /= float(len(args[1]))              
        tot = tot.astype(np.float32)
        tot.tofile(args[0])
        jobq.task_done()        
    jobq.task_done()
    return        


def main():
    pt_dir = '..\\..\\_precip\\point_data\\point_rech_inch_day\\'
    nex_dir = '..\\..\\_precip\\nexrad\\nexrad_rech_inch_day\\'
    daily_avg_dir = '..\\..\\_precip\\summary_stats\\daily_mean_inch\\'
    print 'casting daily avg files'
    daily_avg_files = os.listdir(daily_avg_dir)
    nex_avg_files,nex_avg_dt = [],[]
    for dfile in daily_avg_files:
        print 'processing file',dfile,'\r',
        if dfile.startswith('nx'):
            dfile1 = dfile.split('.')[0]
            dt = datetime.strptime(dfile1,'nx_%b_%d')
            nex_avg_files.append(dfile)
            nex_avg_dt.append(dt.timetuple()[7])

    print 'casting nexrad files'
    nex_files = os.listdir(nex_dir)
    nex_dt = []
    for nfile in nex_files:
        print 'processing file',nfile,'\r',
        dt = datetime.strptime(nfile.split('.')[0],'nx_%Y%m%d')
        nex_dt.append(dt)
    
    print 'casting point files'
    pt_files = os.listdir(pt_dir)
    pt_dt = []
    for pfile in pt_files:
        print 'processing file',pfile,'\r',
        dt_str = pfile.split('.')[0].split('_')[1]
        dt = datetime.strptime(dt_str,'%Y%m%d')
        pt_dt.append(dt)
            
    f = open(flow.root+'.rch','w')
    f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    #f.write(' {0:9.0f} {1:9.0f}\n'.format(0,0))
    f.write(' {0:9.0f} {1:9.0f}\n'.format(3,0))


    print 'processing stress periods'
    out_dir = flow.ref_dir+'rch\\rch_'
    i = 1
    q_args = []
    for start,splen in zip(flow.sp_start,flow.sp_len):
        print 'stress period',i,'\r',
        #--write rch file entry
        outname = out_dir+str(i)+'_'+start.strftime('%Y%m%d')+'.ref'
        f.write(' {0:9.0f} {1:9.0f}'.format(1,0)+'  #STRESS PERIOD '+str(i)+' '+str(start)+'\n')
        f.write('OPEN/CLOSE '+outname+' {0:9.4f} (BINARY)  -1\n'.format(flow.rch_mult))
        
        #--find arrays for each day in this sp and add to job queue args
        files2load = []
        day = start
        while day < start+splen:
            #--first try nexrad
            if day in nex_dt:
                files2load.append(nex_dir+nex_files[nex_dt.index(day)])
            #--then try point arrays
            elif day in pt_dt:
                files2load.append(pt_dir+pt_files[pt_dt.index(day)])
            #--finally fill with the julian day average
            else:
                jd = day.timetuple()[7]
                if jd == 366:
                    jd -= 1
                files2load.append(daily_avg_dir+nex_avg_files[nex_avg_dt.index(jd)])
            day += timedelta(days=1)

        assert len(files2load) == splen.days
        q_args.append([outname,files2load])        
        i += 1
    
    f.close()
    return;
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

if __name__ == '__main__':                                                           
    main()   