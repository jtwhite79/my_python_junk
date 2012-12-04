import sys
import os
import multiprocessing as mp 
from Queue import Queue 
import numpy as np
import pylab
import shapefile
import bro

def plot_worker(jobq,mask,pid,lineshape,range):
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
        if args[2]:
            arr = np.fromfile(args[0],dtype=np.float32)
            arr.resize(bro.nrow,bro.ncol)
        else:
            arr = np.loadtxt(args[0])
        
        if mask != None:
            arr = np.ma.masked_where(mask==0,arr)        
        #print args[0],arr.min(),arr.max(),arr.mean()
        #--generic plotting
        fig = pylab.figure()
        ax = pylab.subplot(1,1,1,aspect='equal')
        
        if range:
            vmax = range[1]
            vmin = range[0]
        else:
            vmax = arr.max()
            vmin = arr.min()

        #p = ax.imshow(arr,interpolation='none')        
        p = ax.pcolor(bro.X,bro.Y,np.flipud(arr),vmax=vmax,vmin=vmin)
        pylab.colorbar(p)
        if lines:
            for line in lines:
                ax.plot(line[0,:],line[1,:],'k-',lw=1.0)
                #break
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlim(bro.plt_x)
        ax.set_ylim(bro.plt_y)
        ax.set_title(args[0])
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
    binflag = True
    a_dir = 'luref\\'
    a_files = os.listdir(a_dir)
    
    lineshape = '..\\..\\_gis\\shapes\\sw_reaches'    
    #--dir to save figs in
    f_dir = 'png\\input\\'

    #--build a queue args
    q_args = []
    for i,a in enumerate(a_files):
        f_name = a.split('.')[0]+'.png'
        q_args.append([a_dir+a,f_dir+f_name,binflag])       

    #-load the mask
    mask = np.loadtxt('ref\\bro_ibound.ref')
    mask[np.where(mask!=1)] = 0
    jobq = mp.JoinableQueue()  

    #--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None)
    #plot_worker(jobq,mask,1,offset,500.0,lineshape,None)  
    #return  
    
    procs = []
    num_procs = 6
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,mask,i,lineshape,None))
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

