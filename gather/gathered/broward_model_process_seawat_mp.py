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
reload(mfb)
import shapefile as sf

from bro import flow,seawat

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




def plot_worker(jobq,pid,conc_file):
   
    concObj = mfb.MT3D_Concentration(seawat.nlay,seawat.nrow,seawat.ncol,conc_file)
    ctimes = concObj.get_time_list()

    while True:
        args = jobq.get()
        if args == None:
            break 
        '''args[0] = plot name           
           args[1] = conc seekpoint         
           args[2] = conc layer to plot 
           args[3] = active reaches
           args[4] = active wells                    
           args[5] = fig_title                 

        '''
        fig_name = args[0]
        conc_seekpoint = args[1]        
        lay_idxs = args[2]
        lines = args[3]
        wells = args[4]               
        fig_title = args[5]               

        totim,kstp,kper,c,success = concObj.get_array(conc_seekpoint)
        c = np.ma.masked_where(c<=1.0e-5,c)


        fig = pylab.figure(figsize=(8,8))                
        
        
        ax1 = pylab.axes((0.05,0.525,0.45,0.45))        
        ax2 = pylab.axes((0.05,0.055,0.45,0.45))
        ax3 = pylab.axes((0.525,0.525,0.45,0.45))        
        ax4 = pylab.axes((0.525,0.055,0.45,0.45))               
                    
        cax1 = pylab.axes((0.05,0.53,0.45,0.015))
        cax2 = pylab.axes((0.05,0.05,0.45,0.015)) 
        cax3 = pylab.axes((0.525,0.53,0.45,0.015))
        cax4 = pylab.axes((0.525,0.05,0.45,0.015))

        print np.max(c[lay_idxs[1],:,:])


        p1 = ax1.imshow(c[lay_idxs[0],:,:],extent=imshow_extent,cmap=cmap,interpolation='none')
        p2 = ax2.imshow(c[lay_idxs[1],:,:],extent=imshow_extent,cmap=cmap,interpolation='none')
        p3 = ax3.imshow(c[lay_idxs[2],:,:],extent=imshow_extent,cmap=cmap,interpolation='none')
        p4 = ax4.imshow(c[lay_idxs[3],:,:],extent=imshow_extent,cmap=cmap,interpolation='none')
                
        
        cb1 = pylab.colorbar(p1,cax=cax1,orientation='horizontal')
        cb2 = pylab.colorbar(p2,cax=cax2,orientation='horizontal')
        cb3 = pylab.colorbar(p3,cax=cax3,orientation='horizontal')
        cb4 = pylab.colorbar(p4,cax=cax4,orientation='horizontal')

        cb1.set_label('Concentration '+seawat.layer_botm_names[lay_idxs[0]])
        cb2.set_label('Concentration '+seawat.layer_botm_names[lay_idxs[1]])
        cb3.set_label('Concentration '+seawat.layer_botm_names[lay_idxs[2]])
        cb4.set_label('Concentration '+seawat.layer_botm_names[lay_idxs[3]])

        ax1.set_ylim(flow.plt_y)
        ax1.set_xlim(flow.plt_x)
        ax2.set_ylim(flow.plt_y)
        ax2.set_xlim(flow.plt_x) 
        ax3.set_ylim(flow.plt_y)
        ax3.set_xlim(flow.plt_x)
        ax4.set_ylim(flow.plt_y)
        ax4.set_xlim(flow.plt_x)

        ax1.set_xticklabels([])
        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax4.set_yticklabels([])               
        
        
        #-- plot active reaches
        for line in lines:                       
            ax1.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax2.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax3.plot(line[0,:],line[1,:],'k-',lw=0.25)
            ax4.plot(line[0,:],line[1,:],'k-',lw=0.25)


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
        if year < flow.start.year:
            year = flow.start.year
        dt = datetime(year=year,month=1,day=1)
        line_active.append(dt)


     #--head stuff
    #--use bot of Q5 to check for dry cells        
    #hds_elev = np.loadtxt(flow.ref_dir+'Q5_bot.ref')
    #hds_layer_idx = 0
    #head_file = flow.root+'.hds'
    #headObj = mfb.MODFLOW_Head(flow.nlay,flow.nrow,flow.ncol,head_file)
    #htimes = headObj.get_time_list()

    #--conc stuff
    conc_lay_idxs = [1,2,3,4,5]
    conc_file = 'MT3D001.UCN'
    concObj = mfb.MT3D_Concentration(seawat.nlay,seawat.nrow,seawat.ncol,conc_file)
    ctimes = concObj.get_time_list()

   

    #--zeta stuff  
    #zta_layer_idx = 0
    #zta_elev = np.loadtxt(flow.ref_dir+'Q1_bot.ref')
    #zeta_file = flow.root+'.zta'
    #zetaObj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,zeta_file)
    #zta_text = '    ZETAPLANE  1'
    #z1times = zetaObj.get_time_list(zta_text)
    #zeta_file = None
    
    #-- stress period step
    sp_step = 1
    plt_dir = 'png\\results\\seawat\\'

    #--for ffmpeg - sequentially numbered
    plt_num = 1
    istart = 0
    q_args = []
    for i,[start,end] in enumerate(zip(seawat.sp_start,seawat.sp_end)):
        if i >= istart and i%sp_step == 0:
            print 'building args list for stress period ending on ',end 
            #--find the conc output nearest the end of the stress period

            try:
                kper_seekpoints = ctimes[np.where(ctimes[:,2]==i+1),-1]
                c_seekpoint = long(kper_seekpoints[0][-1])

            except:
                break
            
            act_lines = []
            for ldt,line in zip(line_active,lines):
                if ldt <= start:
                    act_lines.append(line)
    
            act_wells = []
            if i == 0:
                plt_start = start
            else:
                plt_start = seawat.sp_start[i-sp_step]
            plt_end = seawat.sp_end[i]        
            pump_plt = pump[plt_start:plt_end]
            pump_plt_sum = pump_plt.sum()                          
            for wname,wpoint,wrow,wcol,wzbot in zip(well_names,well_points,well_rows,well_cols,well_zbots):            
                if wname in pump_plt.keys() and pump_plt_sum[wname] != 0:    
                    act_wells.append(wpoint)            

            
            fig_name = plt_dir+'sp{0:03.0f}_conc.png'.format(plt_num)
            fig_title = 'stress period '+str(i+1)+' start date '+start.strftime('%d/%m/%Y')
            args = [fig_name,c_seekpoint,conc_lay_idxs,act_lines,act_wells,fig_title]        
            q_args.append(args)
            plt_num += 1    


    jobq = mp.JoinableQueue() 
    
    
    #--for testing
    #jobq.put_nowait(q_args[0])
    #jobq.put_nowait(None)
    #plot_worker(jobq,1,conc_file)
    #return       
    
    procs = []
    num_procs = 3
    
    for i in range(num_procs):
        #--pass the woker function jobq and a PID
        p = mp.Process(target=plot_worker,args=(jobq,i,conc_file))
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
