import sys
import os
import math
import multiprocessing as mp 
from Queue import Queue 
import numpy as np
import pylab
import gc
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import pandas

import MFBinaryClass as mfb 
import shapefile as sf

from bro import flow

from matplotlib.pyplot import *
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

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


#--global plotting stuff
hd_levels = [-15.0,-5.0,-2.5,0.0,2.5,5.0,15.0]
dtw_levels = [0.0,1.5,2.5,5.0,15.0]

imshow_extent = [flow.x[0],flow.x[-1],flow.y[0],flow.y[-1]]
#mask_color = '#E0E0E0'
mask_color = '#FFFFFF'
cmap = mpl.cm.jet 
cmap.set_bad(mask_color,1)

cmap_flood = mpl.cm.Set1
cmap_flood.set_bad(alpha=0.0)

cmap_dry = mpl.cm.cool
cmap_dry.set_bad(alpha=0.0)

salt_well_color = '#FF33FF'

elevmin = 0.1




def plot_worker(jobq,pid,hds_name,zta_name,dry_elev,zta_elev):
   
    if hds_name is not None:
        headObj = mfb.MODFLOW_Head(flow.nlay,flow.nrow,flow.ncol,hds_name)
        htimes = headObj.get_time_list()
        ntimes = htimes.shape[0]

    if zta_name is not None:
        zeta_file = flow.root+'.zta'
        zetaObj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,zeta_file)
        zta_text = '    ZETAPLANE  1'
        z1times = zetaObj.get_time_list(zta_text)

    while True:
        args = jobq.get()
        if args == None:
            break 
        '''args[0] = plot name           
           args[1] = hds seekpoint         
           args[2] = zeta seekpoint 
           args[3] = active reaches
           args[4] = active wells           
           args[5] = head layer index
           args[6] = zta layer index 
           args[7] = fig_title                 

        '''
        fig_name = args[0]
        hds_seekpoint = args[1]
        zta_seekpoint = args[2]
        lines = args[3]
        wells = args[4]       
        h_layer_idx = args[5]
        z_layer_idx = args[6]
        fig_title = args[7]       

        #--load and mask head        
        if hds_name is not None:
            totim,kstp,kper,h,success = headObj.get_array(hds_seekpoint)
        
            hd = np.copy(h[h_layer_idx,:,:])
            dtw = np.copy(h[h_layer_idx,:,:])
            dtw = flow.top - dtw
        
            mask_flood = np.ones_like(dtw)
            mask_flood = np.ma.masked_where(dtw>=0,mask_flood)
            mask_flood = np.ma.masked_where(np.logical_and(flow.ibound!=1,flow.ibound!=2),mask_flood)

            mask_dry = np.ones_like(dtw)
            mask_dry = np.ma.masked_where(hd>dry_elev,mask_dry)
            mask_dry = np.ma.masked_where(np.logical_and(flow.ibound!=1,flow.ibound!=2),mask_dry)

            hd = np.ma.masked_where(np.logical_and(flow.ibound!=1,flow.ibound!=2),hd)
            dtw = np.ma.masked_where(np.logical_and(flow.ibound!=1,flow.ibound!=2),dtw)
        
        #--load and mask zeta surface 1        
        if zta_name is not None:
            z,totim,success = zetaObj.get_array(zta_seekpoint)               

            z1 = z[z_layer_idx,:,:]        
            z1m = np.ma.masked_where(z1 < zta_elev,z1)
            z1m = np.ma.masked_where(np.logical_and(flow.ibound!=1,flow.ibound!=2),z1m)
            dz1 = flow.top - z1m                        
                      
        fig = pylab.figure(figsize=(8,8))                
        
        
        ax1 = pylab.axes((0.05,0.525,0.45,0.45))        
        ax2 = pylab.axes((0.05,0.055,0.45,0.45))
            
        cax1 = pylab.axes((0.05,0.53,0.45,0.015))
        cax2 = pylab.axes((0.05,0.05,0.45,0.015)) 
        

        p1 = ax1.imshow(hd,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=hd_levels[-1],vmin=hd_levels[0])        
        #p2 = ax2.imshow(dtw,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=dtw_levels[-1],vmin=dtw_levels[0])     
        p2 = ax2.imshow(z1m,extent=imshow_extent,interpolation='none')

        #ax1.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)
        #ax2.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)

        ax1.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)
        ax2.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)
        
        cb1 = pylab.colorbar(p1,cax=cax1,orientation='horizontal')
        cb2 = pylab.colorbar(p2,cax=cax2,orientation='horizontal')

        cb1.set_label('water table elevation $ft NGVD$')
        cb2.set_label('elevation of interface $ft NGVD$')

        ax1.set_ylim(flow.plt_y)
        ax1.set_xlim(flow.plt_x)
        ax2.set_ylim(flow.plt_y)
        ax2.set_xlim(flow.plt_x)    
            
        ax1.set_xticklabels([])
                        
        
        
        #-- plot active reaches
        for line in lines:            
            
            ax1.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax2.plot(line[0,:],line[1,:],'k-',lw=0.25)
            

        #-- plot active wells
        #for wpoint in wells:
        #    color=salt_well_color
        #    if hds_name:
        #        ax1.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #        ax2.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #    if zta_name:
        #        ax3.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #        ax4.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        for wpoint in wells:                
            color='k'
            
            ax1.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
            ax2.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
            
        fig.text(0.5,0.965,fig_title,ha='center')     
        pylab.savefig(fig_name,dpi=300,format='png',bbox_inches='tight')
        pylab.close('all') 
        print pid,'-- done--',fig_title
        jobq.task_done()
    jobq.task_done()
    return



def main():

    #--load well locations and pandas dataframe
    well_shapename = '..\\..\\_gis\\shapes\\pws_combine'
    well_points = sf.load_shape_list(well_shapename)
    #shp = sf.reader(well_shapename)
    #print sf.get_fieldnames(well_shapename)
    records = sf.load_as_dict(well_shapename,loadShapes=False)
    well_names = records['DPEP_NAME']
    well_zbots = records['zbot']
    float_zbots = []
    for i,wb in enumerate(well_zbots):
        float_zbots.append(float(wb))
    well_zbots = np.array(float_zbots)
    well_rows, well_cols = records['row'],records['column']
    pump = pandas.read_csv('..\\..\\_pumpage\\dataframes\\pws_filled_zeros.csv',index_col=0,parse_dates=True)

    #--load lines and active dates
    line_shapename = '..\\..\\_gis\shapes\sw_reaches'
    lines = sf.load_shape_list(line_shapename)
    shp = sf.Reader(line_shapename)
    fnames = sf.get_fieldnames(line_shapename,ignorecase=True)
    #for i,fn in enumerate(fnames):
    #    print i,fn
    a_idx = fnames.index('ACTIVE_ST')
    line_active = []
    for i in range(shp.numRecords):
        rec = shp.record(i)
        year = int(rec[a_idx])
        if year < flow.start.year:
            year = flow.start.year
        dt = datetime(year=year,month=1,day=1)
        line_active.append(dt)


    #--head stuff
    #--use bot of Q5 to check for dry cells        
    hds_elev = np.loadtxt(flow.ref_dir+'Q5_bot.ref')
    hds_layer_idx = 0
    head_file = flow.root+'.hds'
    headObj = mfb.MODFLOW_Head(flow.nlay,flow.nrow,flow.ncol,head_file)
    htimes = headObj.get_time_list()

    #--zeta stuff  
    zta_layer_idx = 0
    zta_elev = np.loadtxt(flow.ref_dir+'Q1_bot.ref')
    zeta_file = flow.root+'.zta'
    zetaObj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,zeta_file)
    zta_text = '    ZETAPLANE  1'
    z1times = zetaObj.get_time_list(zta_text)
    #zeta_file = None
    
    #-- stress period step
    sp_step = 1
    plt_dir = 'png\\results\\'

    #--for ffmpeg - sequentially numbered
    plt_num = 1
    istart = 0
    q_args = []
    for i,dt in enumerate(flow.sp_start):
        if i >= istart and i%sp_step == 0:
            print 'building args list for ',dt 
            try:
                h_seekpoint = long(htimes[i,3])
            except:
                break
            if zeta_file:
                z_seekpoint =  long(z1times[i,3])            
            else:
                z_seekpoint = None

            act_lines = []
            for ldt,line in zip(line_active,lines):
                if ldt <= dt:
                    act_lines.append(line)
    
            act_wells = []
            if i == 0:
                plt_start = dt
            else:
                plt_start = flow.sp_start[i-sp_step]
            plt_end = flow.sp_end[i]        
            pump_plt = pump[plt_start:plt_end]
            pump_plt_sum = pump_plt.sum()                          
            for wname,wpoint,wrow,wcol,wzbot in zip(well_names,well_points,well_rows,well_cols,well_zbots):            
                if wname in pump_plt.keys() and pump_plt_sum[wname] != 0:    
                    act_wells.append(wpoint)            

            
            fig_name = plt_dir+'sp{0:03.0f}.png'.format(plt_num)
            fig_title = 'stress period '+str(i+1)+' start date '+dt.strftime('%d/%m/%Y')
            args = [fig_name,h_seekpoint,z_seekpoint,act_lines,act_wells,hds_layer_idx,zta_layer_idx,fig_title]        
            q_args.append(args)
            plt_num += 1    


    jobq = mp.JoinableQueue() 
    
    
    #--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None)
    #plot_worker(jobq,0,head_file,None,hds_elev,zta_elev)
    #return       
    
    procs = []
    num_procs = 6
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,i,head_file,zeta_file,hds_elev,zta_elev))
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
    main()
