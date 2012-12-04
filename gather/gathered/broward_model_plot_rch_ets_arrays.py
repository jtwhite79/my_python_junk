import sys
import os
from datetime import datetime,timedelta
import multiprocessing as mp 
from Queue import Queue 
import numpy as np
from matplotlib.pyplot import *
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import pylab
import shapefile
import bro


mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed' #'Arial'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42

ticksize = 6
mpl.rcParams['legend.fontsize']  = 6
mpl.rcParams['axes.labelsize']   = 8
mpl.rcParams['xtick.labelsize']  = ticksize
mpl.rcParams['ytick.labelsize']  = ticksize




def plot_worker(jobq,resultq,mask,pid,lineshape):
    '''
    args[0] = figure name
    args[1] = sp length
    args[2] = rch array name
    args[3] = ets array name
    if mask, where masked==0 is masked
    '''
    imshow_extent = [bro.x[0],bro.x[-1],bro.y[0],bro.y[-1]]
    lines = shapefile.load_shape_list(lineshape)
    
    while True:
        #--get some args from the queue
        args = jobq.get()
        #--check if this is a sentenial
        if args == None:
            break
        #--load rch        
        rcharr = np.fromfile(args[2],dtype=np.float32)
        rcharr.resize(bro.nrow,bro.ncol)       
        #rcharr *= bro.rch_mult 
        rcharr = np.ma.masked_where(mask==0,rcharr)        
        
        #--load ets        
        etsarr = np.fromfile(args[3],dtype=np.float32)
        etsarr.resize(bro.nrow,bro.ncol)
        etsarr /= 25.4
        etsarr = np.ma.masked_where(mask==0,etsarr)                               

        ratemax = max(rcharr.max(),etsarr.max())
        ratemin = min(rcharr.min(),etsarr.min())
                
        rchdepth = rcharr * args[1]
        etsdepth = etsarr * args[1]
        depthmax = max(rchdepth.max(),etsdepth.max())
        depthmin = min(rchdepth.min(),etsdepth.min())                 

        #--plot
        fig = pylab.figure(figsize=(8,8))
        ax1 = pylab.axes((0.05,0.525,0.45,0.45))        
        ax2 = pylab.axes((0.05,0.055,0.45,0.45))
        ax3 = pylab.axes((0.525,0.525,0.45,0.45))        
        ax4 = pylab.axes((0.525,0.055,0.45,0.45)) 
               
        cax1 = pylab.axes((0.05,0.53,0.45,0.015))
        cax2 = pylab.axes((0.05,0.05,0.45,0.015))
        cax3 = pylab.axes((0.525,0.53,0.45,0.015))
        cax4 = pylab.axes((0.525,0.05,0.45,0.015))
        
        fig.text(0.5,0.965,args[0].split('.')[0])

        p1 = ax1.imshow(rcharr,extent=imshow_extent,interpolation='none')#,vmax=ratemax,vmin=ratemin)        
        p2 = ax2.imshow(etsarr,extent=imshow_extent,interpolation='none')#,vmax=ratemax,vmin=ratemin)
        p3 = ax3.imshow(rchdepth,extent=imshow_extent,interpolation='none')#,vmax=volmax,vmin=volmin)
        p4 = ax4.imshow(rchdepth-etsdepth,extent=imshow_extent,interpolation='none')#,vmax=volmax,vmin=volmin)
             
        cb1 = pylab.colorbar(p1,cax=cax1,orientation='horizontal')
        cb2 = pylab.colorbar(p2,cax=cax2,orientation='horizontal')
        cb3 = pylab.colorbar(p3,cax=cax3,orientation='horizontal')
        cb4 = pylab.colorbar(p4,cax=cax4,orientation='horizontal')
                       
        cb1.set_label('recharge rate $in/day$')
        cb2.set_label('reference ET rate $in/day$')
        cb3.set_label('recharge depth $inches$')
        cb4.set_label('recharge depth minus ref ET depth $inches$')
                        
        ax1.set_ylim(bro.plt_y)
        ax1.set_xlim(bro.plt_x)
        ax2.set_ylim(bro.plt_y)
        ax2.set_xlim(bro.plt_x)
        ax3.set_ylim(bro.plt_y)
        ax3.set_xlim(bro.plt_x)
        ax4.set_ylim(bro.plt_y)
        ax4.set_xlim(bro.plt_x)

        ax1.set_xticklabels([])
        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax4.set_yticklabels([])
        
        fmt = args[0].split('.')[-1]
        pylab.savefig(args[0],dpi=300,format=fmt)
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
    rch_dir = 'rchref\\'
    ets_dir = 'etsref\\'
    
    rch_files = os.listdir(rch_dir)
    ets_files = os.listdir(ets_dir)

    rch_dts = []
    for rfile in rch_files:
        dt = datetime.strptime(rfile.split('.')[0].split('_')[-1],'%Y%m%d')
        rch_dts.append(dt)

    ets_dts = []
    for efile in ets_files:
        dt = datetime.strptime(efile.split('.')[0].split('_')[-1],'%Y%m%d')
        ets_dts.append(dt)
    
    #--match up rch - ets files
    f_dir = 'png\\input\\'
    q_args = []
    for rfile,rdt in zip(rch_files,rch_dts):
        efile = ets_files[ets_dts.index(rdt)]        
        fname = rdt.strftime('%Y%m%d')+'.png'
        sp_len = bro.sp_len[list(bro.sp_start).index(rdt)].days
        q_args.append([f_dir+fname,sp_len,rch_dir+rfile,ets_dir+efile,rdt])      
        #break
    lineshape = '..\\..\\_gis\\shapes\\sw_reaches'        
        
    mask = bro.ibound
    mask[np.where(mask!=1)] = 0
    
    jobq = mp.JoinableQueue()  
    resultq = mp.Queue()
    
    ##--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None)
    #plot_worker(jobq,resultq,mask,1,lineshape)     
    #return  
    
    procs = []
    num_procs = 6
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,resultq,mask,i,lineshape))
        p.daemon = True
        print 'starting process',p.name
        p.start()
        procs.append(p)
    
    for q in q_args:
        jobq.put(q)

    for p in procs:
        jobq.put(None)      

    nsent = 0
    f = open('rch_ets_compare.dat','w')
    f.write('dt,rmean,rmax,rmin,emean,emax,emin\n')
    
    while True:
        r = resultq.get()
        line = str(r[0])
        for rr in r[1:]:
            line += ',{0:15.6e}'.format(rr)
        line += '\n'
        f.write(line)

        #--block until all finish
        for p in procs:
            p.join() 
            print p.name,'Finished'       
            nsent += 1
        if nsent == num_procs:
            break
        
    f.close()                        
    return

if __name__ == '__main__':                                                                       
    master()                      


