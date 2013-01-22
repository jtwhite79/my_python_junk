import os
import multiprocessing as mp
import Queue
from datetime import datetime,timedelta
import numpy as np
import shapefile


def worker(pid,nrow,ncol,jobq,resultq):
    '''
    args[0] = out array name
    args[1] = list of arrs
    '''

    while True:
        args = jobq.get()
        if args == None:
            break
        print 'worker',pid,'processing arrays',args[0]
        tot = np.zeros((nrow,ncol),dtype=np.float32)
        for aname in args[1]:
            a = np.fromfile(aname,dtype=np.float32)            
            a.resize(nrow,ncol)
            a[np.where(a<0.0)] = 0.0
            tot += a         
        tot.tofile(args[0])
        jobq.task_done()
    jobq.task_done()
    return

def main():
    adir = 'rch\\'
    out_prefix = 'summary\\rch_'
    field_prefix = 'nex_'
    out_shapename = '..\\shapes\\tsala_nexrad_summary'
    
    #adir = 'et\\'
    #out_prefix = 'summary\\et_'
    #field_prefix = 'pet_'
    #out_shapename = '..\\shapes\\tsala_pet_summary'

    
    nrow,ncol = 384,369
    

    afiles = os.listdir(adir)
    years = {}
    
    dts = []
    for a in afiles:
        dt = datetime.strptime(a.split('.')[0].split('_')[1],'%Y%m%d')
        dts.append(dt)
        if dt.year in years.keys():
            years[dt.year].append(adir+a)
        else:
            years[dt.year] = [adir+a]
    
    
    day = timedelta(days=1)
    dts.sort()
    #for i,today in enumerate(dts[1:]):
    #    if today - dts[i] > day:
    #        print 'missing day',today
    
    start = datetime(year=2000,month=1,day=1)
    end = datetime(year=2011,month=12,day=31)
    today = start
    while today < end:
        if today not in dts:
            print 'missing day',today
        today += day
    return

                    
            
    q_args = []
    yr_out = {}
    for yr,alist in years.iteritems():
        aname = out_prefix+str(yr)+'.ref'
        yr_out[yr] = aname
        q_args.append([aname,alist])
    
    jobq = mp.JoinableQueue()  
    resultq = mp.Queue()
    
    #--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None) 
    #worker(0,nrow,ncol,jobq,resultq)
    #return
   
    procs = []
    num_procs = 3
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=worker,args=(i,nrow,ncol,jobq,resultq))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)
    
    for q in q_args:
        jobq.put(q)

    for p in procs:
        jobq.put(None)      
    
    for p in procs:
        p.join() 
        print p.name,'Finished' 
    
    #--add summary arrs to shapefile
    print 'adding summary info to grid shapefile'
    shapename = '..\\shapes\\join_all2'
    shp = shapefile.Reader(shapename)
    shapes = shp.shapes()
    fieldnames = shapefile.get_fieldnames(shapename)
    row_idx,col_idx = fieldnames.index('row'),fieldnames.index('column_')

    wr = shapefile.Writer()
    wr.field('row',fieldType='N',size=10,decimal=0)            
    wr.field('column',fieldType='N',size=10,decimal=0)
    
    yr_list = years.keys()
    yr_list.sort()
    
    yr_avgs = []
    for yr in yr_list:
        wr.field(field_prefix+str(yr),fieldType='N',size=20,decimal=10)
        a = np.fromfile(yr_out[yr],dtype=np.float32)
        a.resize(nrow,ncol)        
        yr_avgs.append(a)    
                
    for i,shape in enumerate(shapes):
        if i % 500 == 0:
            print i,len(shapes),'\r',
        rec = shp.record(i)
        row,col = rec[row_idx],rec[col_idx]
        rec = [row,col]
        for yr_avg in yr_avgs:
            rec.append(yr_avg[row-1,col-1])
        wr.poly([shape.points],shapeType=shape.shapeType)
        wr.record(rec)
    wr.save(out_shapename)  
    return


if __name__ == '__main__':                                                                       
    main()                     