import sys
import os
import math
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
pump = pandas.read_csv('..\\..\\_pumpage\\pws_filled_zeros.csv',index_col=0,parse_dates=True)

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
#--use bot of layer 1 to check for dry cells
l1_bot = np.loadtxt('ref\\Q5_bot.ref')
hds_layer_idx = 0
head_file = bro.modelname+'.hds'
headObj = mfb.MODFLOW_Head(bro.nlay,bro.nrow,bro.ncol,head_file)
htimes = headObj.get_time_list()
ntimes = htimes.shape[0]

#--swi stuff
#zta_layer_idx_1 = 3
#zta_layer_idx_2 = 4
#zta_layer_bot_1 = np.loadtxt('ref\\Q2_bot.ref')
#zta_layer_bot_2 = np.loadtxt('ref\\Q1_bot.ref')
#zeta_file = bro.modelname+'.zta'
#zetaObj = mfb.MODFLOW_CBB(bro.nlay,bro.nrow,bro.ncol,zeta_file)
#zta_text = '    ZETAPLANE  1'
#z1times = zetaObj.get_time_list(zta_text)
#zta_text = '    ZETAPLANE  2'
#z2times = zetaObj.get_time_list(zta_text)

#--plot infos
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

#-- stress period step
sp_step = 1
plt_dir = 'png\\results\\'

#--for ffmpeg - sequentially numbered
plt_num = 1
istart = 320
for i,dt in enumerate(bro.sp_start):
    if i >= istart and i%sp_step == 0:
        
        #--load and mask head
        ipos = long(htimes[i,3])
        totim,kstp,kper,h,success = headObj.get_array(ipos)
        
        hd = np.copy(h[0,:,:])
        dtw = np.copy(h[0,:,:])
        dtw = bro.top - dtw
        
        mask_flood = np.ones_like(dtw)
        mask_flood = np.ma.masked_where(dtw>=0,mask_flood)
        mask_flood = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),mask_flood)

        mask_dry = np.ones_like(dtw)
        mask_dry = np.ma.masked_where(hd>l1_bot,mask_dry)
        mask_dry = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),mask_dry)

        hd = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),hd)
        dtw = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),dtw)
        
        #--load and mask zeta surface 1
        #ipos = long(z1times[i,3])
        #z,totim,success = zetaObj.get_array(ipos)               

        #z1 = z[zta_layer_idx_1,:,:]        
        #z1m = np.ma.masked_where(z1 < zta_layer_bot_1,z1)
        #z1m = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),z1m)
        #dz1 = bro.top - z1m        

        #z2 = z[zta_layer_idx_2,:,:]        
        #z2m = np.ma.masked_where(z1 < zta_layer_bot_2,z2)
        #z2m = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),z2m)
        #dz2 = bro.top - z2m        


        #--load and mask zeta surface 2
        #ipos = long(z2times[i,3])
        #z2,totim,success = zetaObj.get_array(ipos)               
        #z2 = z2[0,:,:]        
        #z2m = np.ma.masked_where(z1 < bis_bot,z2)
        #z2m = np.ma.masked_where(np.logical_and(bro.ibound!=1,bro.ibound!=2),z2m)
        #dz2 = bro.top - z2m        

        print dt
        print '-- head range ',hd.min(),hd.max()
               
        #fig_name = plt_dir+dt.strftime('%Y%m%d')+'_hds.png'
        
        fig_name = plt_dir+'sp{0:03.0f}.png'.format(plt_num)
        plt_num += 1
        fig = pylab.figure(figsize=(8,8))                
        
        ax1 = pylab.axes((0.05,0.525,0.45,0.45))        
        ax2 = pylab.axes((0.05,0.055,0.45,0.45))
        ax3 = pylab.axes((0.525,0.525,0.45,0.45))        
        ax4 = pylab.axes((0.525,0.055,0.45,0.45)) 
               
        cax1 = pylab.axes((0.05,0.53,0.45,0.015))
        cax2 = pylab.axes((0.05,0.05,0.45,0.015))
        cax3 = pylab.axes((0.525,0.53,0.45,0.015))
        cax4 = pylab.axes((0.525,0.05,0.45,0.015))

        fig.text(0.5,0.965,'stress period '+str(i+1)+' start date '+dt.strftime('%d/%m/%Y'),ha='center')

        #p1 = ax1.imshow(hd,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=hd_levels[-1],vmin=hd_levels[0])        
        #p2 = ax2.imshow(dtw,extent=imshow_extent,cmap=cmap,interpolation='none',vmax=dtw_levels[-1],vmin=dtw_levels[0])       
        #p3 = ax3.imshow(z1m,extent=imshow_extent,interpolation='none')
        #p4 = ax4.imshow(z2m,extent=imshow_extent,interpolation='none')        
      
        #ax1.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)
        #ax2.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)
        #ax3.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)
        #ax4.imshow(mask_flood,alpha=0.5,extent=imshow_extent,cmap=cmap_flood,interpolation='nearest',vmin=0,vmax=1)

        #ax1.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)
        #ax2.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)
        #ax3.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)
        #ax4.imshow(mask_dry,extent=imshow_extent,cmap=cmap_dry,interpolation='nearest',vmin=0,vmax=1)

        #cb1 = pylab.colorbar(p1,cax=cax1,orientation='horizontal')
        #cb2 = pylab.colorbar(p2,cax=cax2,orientation='horizontal')
        #cb3 = pylab.colorbar(p3,cax=cax3,orientation='horizontal')
        #cb4 = pylab.colorbar(p4,cax=cax4,orientation='horizontal')
                       
        #cb1.set_label('elevation $ft NGVD$')
        #cb2.set_label('depth to water $ft$')
        #cb3.set_label('interface elevation $ft NGVD$')
        #cb4.set_label('depth to interface $ft$')

        #c1 = ax1.contour(bro.X,bro.Y,np.flipud(hd),levels=hd_levels,colors='k',lw=0.1)
        #c3 = ax3.contour(bro.X,bro.Y,np.flipud(hd),levels=hd_levels,colors='k')        
        #ax1.clabel(c1,inline=1,fmt='%5.1f',fontsize=6)
        #ax3.clabel(c3,inline=1,fmt='%5.1f',fontsize=6)
        
        #-- plot active reaches
        #for ldt,line in zip(line_active,lines):
        #    if ldt <= dt:
        #       ax1.plot(line[0,:],line[1,:],'k-',lw=0.25)
        #        ax2.plot(line[0,:],line[1,:],'k-',lw=0.25)
        #        ax3.plot(line[0,:],line[1,:],'k-',lw=0.25)
        #        ax4.plot(line[0,:],line[1,:],'k-',lw=0.25)


        #-- plot active wells
        #if i == 0:
        #    plt_start = dt
        #else:
        #    plt_start = bro.sp_start[i-sp_step]
        #plt_end = bro.sp_end[i]        
        #pump_plt = pump[plt_start:plt_end]
        #pump_plt_sum = pump_plt.sum()              
        ##--only plot wells that have a non-zero extraction during the plot period
        #for wname,wpoint,wrow,wcol,wzbot in zip(well_names,well_points,well_rows,well_cols,well_zbots):            
        #    if wname in pump_plt.keys() and pump_plt_sum[wname] != 0:                
                #if z1[wrow-1,wcol-1] > wzbot:
                #    color=salt_well_color
                #else:
                #    color='k'
        #        color='k'
        #        ax1.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #        ax2.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #        ax3.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        #        ax4.plot(wpoint[0],wpoint[1],'.',mfc=color,mec='none',ms=4)       
        
        #ax1.set_ylim(bro.plt_y)
        #ax1.set_xlim(bro.plt_x)
        #ax2.set_ylim(bro.plt_y)
        #ax2.set_xlim(bro.plt_x)
        #ax3.set_ylim(bro.plt_y)
        #ax3.set_xlim(bro.plt_x)
        #ax4.set_ylim(bro.plt_y)
        #ax4.set_xlim(bro.plt_x)

        #ax1.set_xticklabels([])
        #ax3.set_xticklabels([])
        #ax3.set_yticklabels([])
        #ax4.set_yticklabels([])
        #pylab.savefig(fig_name,dpi=300,format='png',bbox_inches='tight')
        #pylab.close('all')
        #pylab.show() 
        
         


