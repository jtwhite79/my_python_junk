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

import bro

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

imshow_extent = [bro.x[0],bro.x[-1],bro.y[0],bro.y[-1]]
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




def plot_worker(jobq,pid,dry_elev,zta_elev):
   

    headObj1 = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,bro.modelname+'.hds')
    htimes1 = headObj1.get_time_list()
    ntimes1 = htimes1.shape[0]

    headObj2 = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,bro.seawatname+'.hds')
    htimes2 = headObj2.get_time_list()
    ntimes2 = htimes2.shape[0]

    zeta_file1 = bro.modelname+'.zta'
    zetaObj1 = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file1)
    zta_text1 = '    ZETAPLANE  1'
    z1times1 = zetaObj1.get_time_list(zta_text1)

    zeta_file2 = bro.seawatname+'.zta'
    zetaObj2 = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file2)
    zta_text2 = '    ZETAPLANE  1'
    z1times2 = zetaObj1.get_time_list(zta_text2)

    while True:
        args = jobq.get()
        if args == None:
            break 
        '''args[0] = plot name           
           args[1] = hds1 seekpoint         
           args[2] = zeta1 seekpoint
           args[3] = hds2 seekpoint
           args[4] = zeta2 seekpoint 
           args[5] = active reaches
           args[6] = active wells           
           args[7] = head layer index
           args[8] = zta layer index 
           args[9] = fig_title                 

        '''
        fig_name = args[0]
        hds1_seekpoint = args[1]
        zta1_seekpoint = args[2]
        hds2_seekpoint = args[3]
        zta2_seekpoint = args[4]
        lines = args[5]
        wells = args[6]       
        h_layer_idx = args[7]
        z_layer_idx = args[8]
        fig_title = args[9]       

        #--load and mask head        
        
        totim,kstp,kper,h1,success = headObj1.get_array(hds1_seekpoint)        
        hd1 = h1[h_layer_idx,:,:]                        
        hd1 = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),hd1)        
        
        totim,kstp,kper,h2,success = headObj2.get_array(hds2_seekpoint)        
        hd2 = h2[h_layer_idx,:,:]                        
        hd2 = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),hd2)        
        
        hd_diff = hd1 - hd2
        hd_diff = np.ma.masked_where(np.abs(hd_diff)<0.01,hd_diff)

        hd1 = np.ma.masked_where(np.abs(hd_diff)<0.01,hd1)        
        hd2 = np.ma.masked_where(np.abs(hd_diff)<0.01,hd2)        

        
        z1,totim,success = zetaObj1.get_array(zta1_seekpoint)               
        z1 = z1[z_layer_idx,:,:]        
        z1m = np.ma.masked_where(z1 < zta_elev,z1)
        z1m = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),z1m)
        
        z2,totim,success = zetaObj2.get_array(zta2_seekpoint)               
        z2 = z2[z_layer_idx,:,:]        
        z2m = np.ma.masked_where(z2 < zta_elev,z2)
        z2m = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),z2m)

        fig = pylab.figure(figsize=(8,8))                
        
        ax1 = pylab.axes((0.05,0.525,0.45,0.45))        
        ax2 = pylab.axes((0.05,0.055,0.45,0.45))            
        cax1 = pylab.axes((0.05,0.53,0.45,0.015))
        cax2 = pylab.axes((0.05,0.05,0.45,0.015)) 
        
        vmax = max(np.max(hd1),np.max(hd2))
        vmin = min(np.min(hd1),np.min(hd2))

        p1 = ax1.imshow(hd1,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=vmax,vmin=vmin)
        p2 = ax2.imshow(hd2,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=vmax,vmin=vmin)
      
        cb1 = pylab.colorbar(p1,cax=cax1,orientation='horizontal')
        cb2 = pylab.colorbar(p2,cax=cax2,orientation='horizontal')

        cb1.set_label('elevation $ft NGVD$')
        cb2.set_label('elevation $ft NGVD$')

        ax1.set_ylim(bro.plt_y)
        ax1.set_xlim(bro.plt_x)
        ax2.set_ylim(bro.plt_y)
        ax2.set_xlim(bro.plt_x)    
            
        ax1.set_xticklabels([])
                        
        

        ax3 = pylab.axes((0.525,0.525,0.45,0.45))        
        ax4 = pylab.axes((0.525,0.055,0.45,0.45))               
        cax3 = pylab.axes((0.525,0.53,0.45,0.015))
        cax4 = pylab.axes((0.525,0.05,0.45,0.015))
        p3 = ax3.imshow(hd_diff,extent=imshow_extent,interpolation='none',vmax=1.0,vmin=-1.0)
        p4 = ax4.imshow(z2m,extent=imshow_extent,interpolation='none')        
        
        cb3 = pylab.colorbar(p3,cax=cax3,orientation='horizontal')
        cb4 = pylab.colorbar(p4,cax=cax4,orientation='horizontal')
                                                     
        cb3.set_label('interface elevation $ft NGVD$')
        cb4.set_label('interface elevation $ft NGVD$')

        ax3.set_ylim(bro.plt_y)
        ax3.set_xlim(bro.plt_x)
        ax4.set_ylim(bro.plt_y)
        ax4.set_xlim(bro.plt_x)

        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax4.set_yticklabels([])
        
        #-- plot active reaches
        for line in lines:                       
            ax1.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax2.plot(line[0,:],line[1,:],'k-',lw=0.25)           
            ax3.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax4.plot(line[0,:],line[1,:],'k-',lw=0.25)


        for wpoint in wells:                
            color='k'
            ax1.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
            ax2.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)                  
            ax3.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
            ax4.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)                       
        
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
        if year < bro.start.year:
            year = bro.start.year
        dt = datetime(year=year,month=1,day=1)
        line_active.append(dt)


    #--head stuff
    #--use bot of Q5 to check for dry cells        
    hds_elev = np.loadtxt('ref\\Q5_bot.ref')
    hds_layer_idx = 0
    head_file1 = bro.modelname+'.hds'
    headObj1 = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,head_file1)
    htimes1 = headObj1.get_time_list()

    head_file2 = bro.seawatname+'.hds'
    headObj2 = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,head_file2)
    htimes2 = headObj2.get_time_list()


    #--zeta stuff  
    zta_layer_idx = 0
    zta_elev = np.loadtxt('ref\\T1_bot.ref')
    zeta_file1 = bro.modelname+'.zta'
    zetaObj1 = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file1)
    zta_text1 = '    ZETAPLANE  1'
    z1times1 = zetaObj1.get_time_list(zta_text1)
    
    zeta_file2 = bro.seawatname+'.zta'
    zetaObj2 = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file2)
    zta_text2 = '    ZETAPLANE  1'
    z1times2 = zetaObj2.get_time_list(zta_text2)
    
    #-- stress period step
    sp_step = 1
    plt_dir = 'png\\results_compare\\'

    #--for ffmpeg - sequentially numbered
    plt_num = 1
    istart = 0
    q_args = []
    for i,dt in enumerate(bro.sp_start):
        if i >= istart and i%sp_step == 0:
            print 'building args list for ',dt 
            try:
                h_seekpoint1 = long(htimes1[i,3])
                h_seekpoint2 = long(htimes2[i,3])
            except:
                break            
            z_seekpoint1 =  long(z1times1[i,3])            
            z_seekpoint2 =  long(z1times2[i,3])                        
                

            act_lines = []
            for ldt,line in zip(line_active,lines):
                if ldt <= dt:
                    act_lines.append(line)
    
            act_wells = []
            if i == 0:
                plt_start = dt
            else:
                plt_start = bro.sp_start[i-sp_step]
            plt_end = bro.sp_end[i]        
            pump_plt = pump[plt_start:plt_end]
            pump_plt_sum = pump_plt.sum()                          
            for wname,wpoint,wrow,wcol,wzbot in zip(well_names,well_points,well_rows,well_cols,well_zbots):            
                if wname in pump_plt.keys() and pump_plt_sum[wname] != 0:    
                    act_wells.append(wpoint)            
            
            fig_name = plt_dir+'sp{0:03.0f}.png'.format(plt_num)
            fig_title = 'stress period '+str(i+1)+' start date '+dt.strftime('%d/%m/%Y')
            args = [fig_name,h_seekpoint1,z_seekpoint1,h_seekpoint2,z_seekpoint2,act_lines,act_wells,hds_layer_idx,zta_layer_idx,fig_title]        
            q_args.append(args)
            plt_num += 1    


    jobq = mp.JoinableQueue() 
    
    
    #--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None)
    #plot_worker(jobq,1,hds_elev,zta_elev)
    #return       
    
    procs = []
    num_procs = 7
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,i,hds_elev,zta_elev))
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
