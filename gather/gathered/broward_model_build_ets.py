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
        #np.savetxt(args[0]+'.ascii',tot,fmt='%15.6e')               
        tot.tofile(args[0])
        jobq.task_done()        
    jobq.task_done()
    return        


def get_lu_year(dt,dt_list):
    #dt_list = dt_list.sort()
    if dt < dt_list[0]:
        return dt_list[0]
    elif dt >= dt_list[-1]:
        return dt_list[-1]
    else:
        for i in range(1,len(dt_list)):            
            if dt.year < dt_list[i].year:
                return dt_list[i-1]        


def write_sp(f,sp_str,etss,etsr,etsx,pxdp1,petm1,pxdp2,petm2):
    inetss,inetsr,inetsx,iniets = -1,-1,-1,-1
    if etss:
        assert os.path.exists(etss),'cant find '+etss
        inetss = 1
    if etsr:
        #assert os.path.exists(etsr),'cant find '+etsr
        inestr = 1
    if etsx:
        assert os.path.exists(etsx),'cant find '+etsx
        inetsx = 1
    if pxdp1 and pxdp2 and petm1 and petm2:
        assert os.path.exists(pxdp1),'cant find '+pxdp1
        assert os.path.exists(pxdp2),'cant find '+pxdp2
        assert os.path.exists(petm1),'cant find '+petm1
        assert os.path.exists(petm2),'cant find '+petm2
        insgdf = 1
    elif pxdp1 or pxdp2 or petm1 or petm2:
        raise TypeError('all or none must be passed')
    f.write(' {0:>9.0f} {1:>9.0f} {2:>9.0f} {3:>9.0f} {4:>9.0f} {5:>40s}\n'.format(inetss,inestr,inetsx,-1,insgdf,sp_str))   
    if etss:
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+etss,1.0,'(FREE)',-1,'#ETSS'))
    if etsr:
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+etsr,flow.ets_mult,'(BINARY)',-1,'#ETSR'))
    if etsx:
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+etsx,1.0,'(BINARY)',-1,'#ETSX'))
    if pxdp1 and pxdp2 and petm1 and petm2:
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+pxdp1,1.0,'(BINARY)',-1,'#PXDP1'))
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+petm1,1.0,'(BINARY)',-1,'#PETM1'))
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+pxdp2,1.0,'(BINARY)',-1,'#PXDP2'))
        f.write('{0:<60s} {1:>9.6f} {2:>9s} {3:9.0f} {4:>9s}\n'.format('OPEN/CLOSE '+petm2,1.0,'(BINARY)',-1,'#PETM2'))
    return

def main():

    
    ret_dir = '..\\..\\_pet\\goes\\ret_mm_day\\'
    daily_avg_dir = '..\\..\\_pet\\summary_stats\\goes_summary_stats\\'
    print 'casting daily avg files'
    daily_avg_files = os.listdir(daily_avg_dir)
    ret_avg_files,ret_avg_dt = [],[]
    for dfile in daily_avg_files:
        #print 'processing file',dfile,'\r',
        if dfile.startswith('ret') and dfile.split('.')[0].endswith('avg'):
            dfile1 = dfile.split('.')[0]
            #dt = datetime.strptime(dfile1,'nx_%b_%d')
            ret_avg_files.append(dfile)
            #ret_avg_dt.append(dt.timetuple()[7])
            ret_avg_dt.append(int(dfile.split('_')[2]))

    print 'casting ret files'
    ret_files = os.listdir(ret_dir)
    ret_dt = []
    for nfile in ret_files:
        #print 'processing file',dfile,'\r',
        dt = datetime.strptime(nfile.split('.')[0],'ret%Y%m%d')
        ret_dt.append(dt)
        
    f = open(flow.root+'.ets','w',0)
    f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    f.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.0f}\n'.format(3,0,0,3))
    
    #--get and process landuse files
    lu_dir = flow.ref_dir+'lu\\'
    lu_files = os.listdir(lu_dir)
    lu_dts = []    
    for lfile in lu_files:
        year = int(lfile.split('_')[0])
        dt = datetime(year=year,month=1,day=1)
        if dt not in lu_dts:
            lu_dts.append(dt)
    lu_dts.sort()  
    
    print 'processing stress periods'
    out_dir = flow.ref_dir+'ets\\ets_'    
    i = 1
    q_args = []
    current_year = get_lu_year(flow.sp_start[0],lu_dts)
    current_month = None    
    for start,splen in zip(flow.sp_start,flow.sp_len):
        print 'stress period',i,'\r',
        
        #--hard coding alert -- assuming stress periods are 1 month or shorter
        if (start + splen - timedelta(days=1)).month != start.month:
            raise IndexError('Stress period longer than days in month - need to update crop coeff arrays')
        outname = out_dir+str(i)+'_'+start.strftime('%Y%m%d')+'.ref'
        etsx,pxdp1,pxdp2 = None,None,None
        petm1,petm2 = None,None
        etsr,etss = outname,None
        if start.year==1958:
            pass
        yr = get_lu_year(start,lu_dts)
        mn = start.month
             
        if yr != current_year: 
            print 'changing year',start.year 
            current_year = yr           
            etsx = lu_dir+str(current_year.year)+'_bro_etsx.ref'
               
        if mn != current_month:
            print 'changing  to month',mn  
            current_month = mn                          
            pxdp1 = lu_dir+str(current_year.year)+'_bro_pxdp01.ref'
            pxdp2 = lu_dir+str(current_year.year)+'_bro_pxdp02.ref'
            petm1 = lu_dir+str(current_year.year)+'_bro_petm_{0:02.0f}.ref'.format(current_month)
            petm2 = lu_dir+str(current_year.year)+'_bro_petm_{0:02.0f}.ref'.format(current_month)
            
        if i == 1:
            etsx = lu_dir+str(current_year.year)+'_bro_etsx.ref'
            etss = flow.top_name
       
        sp_str = '#stress period '+str(i)+' '+str(start)
        
        write_sp(f,sp_str,etss,etsr,etsx,pxdp1,petm1,pxdp2,petm2)
        
        #files2load = []
        #day = start
        #while day < start+splen:
        #    if day in ret_dt:
        #        files2load.append(ret_dir+ret_files[ret_dt.index(day)])
        #    else:
        #        jd = day.timetuple()[7]
        #        files2load.append(daily_avg_dir+ret_avg_files[ret_avg_dt.index(jd)])
        #    day += timedelta(days=1)

        #assert len(files2load) == splen.days
        #
        #q_args.append([outname,files2load])        
        
        
        i += 1
    
    f.close()    
    return
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
