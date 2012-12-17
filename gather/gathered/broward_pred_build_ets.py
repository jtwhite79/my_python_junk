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

    
    ret_dir = '..\\..\\_model\\bro.02\\flowref\\ets\\'
    print 'casting ret filenames and writing average monthly arrays'
    ret_files = os.listdir(ret_dir)
    ret_dt = []
    ret_monthly = {}
    for rfile in ret_files:
        dt = datetime.strptime(rfile.split('.')[0].split('_')[-1],'%Y%m%d')
        if dt.month in ret_monthly:
            ret_monthly[dt.month].append(ret_dir+rfile)
        else:
            ret_monthly[dt.month] = [ret_dir+rfile]
    aprefix = flow.ref_dir+'ets\\ets_'
    monthly_names = {}    
    q_args = []
    for imonth,rfiles in ret_monthly.iteritems():
        aname = aprefix+str(imonth)+'.ref'
        monthly_names[imonth] = aname
        q_args.append([aname,rfiles])

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
                
    f = open(flow.root+'.ets','w',0)
    f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    f.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.0f}\n'.format(3,flow.ets_unit,0,3))
    
    #--get and process landuse files
    lu_dir = flow.ref_dir+'lu\\'
    lu_files = os.listdir(lu_dir)
    lu_dts = []    
    for lfile in lu_files:
        year = int(lfile.split('_')[0])
        dt = datetime(year=year,month=1,day=1)
        if dt not in lu_dts:
            lu_dts.append(dt)
                
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
        outname = monthly_names[start.month]
        etsx,pxdp1,pxdp2 = None,None,None
        petm1,petm2 = None,None
        etsr,etss = outname,None        
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
        i += 1 
    f.close()        


if __name__ == '__main__':                                                           
    main()   

