import os
import copy
import multiprocessing as mp
from datetime import datetime,timedelta
import numpy as np
import pestUtil as pu
import shapefile


def worker(jobq,pid):
    while True:    
        args = jobq.get()
        if args == None:
            break        
        dname = args[1][0].split('.')[0].split('\\')[-1]
        smp = pu.smp(args[1][0],load=True)
        rtype = smp.records.keys()[0]
        smp.records[dname] = smp.records[smp.records.keys()[0]]
        smp.records.pop(rtype)
        for smpname in args[1][1:]:
            smp2 = pu.smp(smpname,load=True)
            rtype = smp2.records.keys()[0]
            smp2.records[dname] = smp2.records[smp2.records.keys()[0]]
            smp2.records.pop(rtype)
            smp.merge(smp2,how='left')
        print '----'+args[0]                   
        smp.save(args[0])
        jobq.task_done()        
    jobq.task_done()
    return        



RECORD_ORDER = ['INDIVIDUAL','PARTIAL','ACCUMULATED','POPESTM']

def main():
    #--get a list of pws smp component files
    comp_dir = 'pws_smp_components\\'
    comp_files = os.listdir(comp_dir)

    #--get a list of unique dep well names
    dep_names = []
    for cfile in comp_files:
        if cfile.split('.')[0] not in dep_names:
            dep_names.append(cfile.split('.')[0])

    smp_dir = 'pws_smp_daily\\'

    cfd_2_gpm = 7.481/24.0/60.
    q_args = []
    for dname in dep_names:    
        #--find files

        print 'processing ',dname
        r_files = []
        for cf in comp_files:
            if cf.upper().startswith(dname.upper()):
                r_files.append(cf)
        if len(r_files) > 0:                   
            #--load records and merge
            #--order the records
            r_order = []
            for ro in RECORD_ORDER:
                for rf in r_files:
                    if ro.upper() in rf.upper():
                        r_order.append(comp_dir+rf)            
            q_args.append([smp_dir+dname+'.smp',r_order])
            #rec = load_well_record(well_dir+r_order[0])
            #rec = np.sort(rec,axis=0)
            #smp = pu.smp(comp_dir+r_order[0],load=True)
            #rtype = r_order[0].split('.')[1].lower()
            #smp.records[dname] = smp.records[rtype]
            #smp.records.pop(rtype) 
            #smp_plot = pu.smp(comp_dir+r_order[0],load=True)
            #smp_plot.records[r_order[0]] = rec
            
            #for ro in r_order[1:]:
            #    rtype = ro.split('.')[1].lower()
            #    #rec2 = load_well_record(well_dir+ro)
            #    #rec2 = np.sort(rec2,axis=0)
            #    smp2 = pu.smp(comp_dir+ro,load=True)
            #    smp2.records[dname] = smp2.records[rtype]
            #                    
            #    smp.merge(smp2,how='left')  
            #    smp_plot.records[rtype] = smp2.records[rtype]             
            #smp.save(smp_dir+dname+'.smp')        
            #for key in smp_plot.records.keys():
            #    smp_plot.records[key][:,1] *= cfd_2_gpm
            #smp_plot.plot('png\\'+dname+'.png') 
            ##for ro in r_order:
            ##    comp_files.pop(comp_files.index(ro))                          
        else:
            print 'no records found for well'+dname
    #f = open('smp_combine_missing.dat','w')
    #for cfile in comp_files:
    #    f.write(cfile+'\n')
    
    jobq = mp.JoinableQueue()  

    #jobq.put_nowait(q_args[0])
    #worker(jobq,1)
    #return


    procs = []
    num_procs = 5
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