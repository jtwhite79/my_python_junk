import sys
import os
import multiprocessing as mp 
from Queue import Queue 
import numpy as np
import pylab
import shapefile


def plot_worker(jobq,mask,pid,offset,delta,lineshape,range):
    '''
    args[0] = array file name
    args[1] = output figure name
    if mask, where masked==0 is masked
    '''

    if lineshape:
        lines = shapefile.load_shape_list(lineshape)
    else:
        lines = None

    

    while True:
        #--get some args from the queue
        args = jobq.get()
        #--check if this is a sentenial
        if args == None:
            break
        #--load
        arr = np.loadtxt(args[0])
        nrow,ncol = arr.shape
        x = np.arange(0,ncol*delta,delta) + offset[0]
        y = np.arange(0,nrow*delta,delta) + offset[1]
        X,Y = np.meshgrid(x,y)
        print x.shape,y.shape
        if mask != None:
            arr = np.ma.masked_where(mask==0,arr)
        #print args[0],arr.min(),arr.max(),arr.mean()
        #--generic plotting
        fig = pylab.figure()
        ax = pylab.subplot(111)
        #p = ax.pcolor(arr)
        if range:
            #p = ax.pcolor(X,Y,arr,vmax=range[1],vmin=range[0])
            if lines:
                for line in lines:
                    ax.plot(line[:,0],line[:,1],'k-',lw=1.0)
        else:
            p = ax.imshow(arr,interpolation='none')
       
        #pylab.colorbar(p)
        fmt = args[1].split('.')[-1]
        pylab.savefig(args[1],dpi=300,format=fmt)
        pylab.close(fig)
        #--mark this task as done
        jobq.task_done()
        print 'plot worker',pid,' finished',args[0]

    #--mark the sentenial as done
    jobq.task_done()
    return

def master():
    #--dir of arrays
    #a_dir = 'daily_mean_inch\\'
    a_dir = 'annual_total_inch\\'
    #a_dir = 'pet_minus_ret_mmday\\'
    #a_dir = 'hargreaves_correction_arrays\\'
    #a_dir = 'ret_mm_day\\'
    #a_dir = 'goes_summary_stats\\'
    #a_dir = 'nexrad_summary_stats\\'
    #a_dir = 'ref\\'
    a_files = os.listdir(a_dir)
    
    lineshape = '..\\..\\_gis\\shapes\\sw_reaches'
    offset = [728600.0,577350.0]
    #--dir to save figs in
    f_dir = 'png\\'

    #--build a queue args
    q_args = []
    for i,a in enumerate(a_files):
        f_name = a.split('.')[0]+'.png'
        q_args.append([a_dir+a,f_dir+f_name])
        break

    #-load the mask
    #mask = np.loadtxt('UMD_OFFSHORE.ref')
    #mask[np.where(mask==2)] = 0
    mask = np.loadtxt('ref\\bro_ibound.ref')
    jobq = mp.JoinableQueue()  

    #--for testing
    jobq.put_nowait(q_args[0])
    plot_worker(jobq,mask,1,offset,500.0,lineshape,[0,100.0])  
    return  
    
    procs = []
    num_procs = 6
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,None,i,lineshape,None))
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
