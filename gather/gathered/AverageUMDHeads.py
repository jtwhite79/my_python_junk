import sys
import os
import math
import numpy as np
import pylab
import gc

from datetime import datetime
from datetime import timedelta

import MFArrayUtil as au
import MFData as mfd
import MFBinaryClass as mfb 
import shapefile as sf

def SaltwaterPosition(nrow,ncol,elev,zeta):
    elevmin = 0.2 #1.0e-6
    value = np.zeros( (nrow,ncol), np.float )
    for irow in xrange(0,nrow):
        for jcol in xrange(0,ncol):
            if zeta[irow,jcol] > elev[irow,jcol] + elevmin:
                value[irow,jcol] = 1.0
            #--a little flim flam to get rid of boundary issues
            if jcol < 97:
                if irow < 11:
                    value[irow,jcol] = 0.0
            if jcol < 40:
                if irow < 35:
                    value[irow,jcol] = 0.0
    return value

#preliminary figure specifications
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

#--get command line arguments
REFDir = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','UMD.S1','REF' )
ResultsDir = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','UMD.S1','Results' )

#--data for file processing
OutputDir = os.path.join( '..', 'figures' )
#--default data if command line argument not defined for variable
model_dir = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','UMD.S1' )
results_dir = [ 'Results_stat', \
                'Results_PCT125', \
                'Results_DSL0304', \
                'Results_DSL0304_PCT125', \
                'Results_DSL0914', \
                'Results_DSL0914_PCT125', \
                 ]

head_file = 'UMD.hds'
zeta_file = 'UMD.zta'
zta_text = '    ZETAPLANE  2'
#--figure data
ztext = ['',\
         '25% increase in PWS', \
         'sea-level increase = 0.304 meters', \
         'sea-level increase = 0.304 meters and 25% increase in PWS', \
         'sea-level increase = 0.914 meters', \
         'sea-level increase = 0.914 meters and 25% increase in PWS', \
         ]
#--read shapefile to use as base map on figures
shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','BaseMap')
hydrography = sf.load_shape_list(shape_name)
salinity_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','SalinityControlStructures')
salinity_struc = sf.load_shape_list(salinity_struct_shape_name)
df_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','DrainageFloodControlStructures')
df_struc = sf.load_shape_list(df_struct_shape_name)
pws_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','Water Use','pumpwells_lb')
pws = sf.load_shape_list(pws_struct_shape_name)
#--contour intervals
hdcontour  = np.arange(-1.5,2.5,0.5)  
ddncontour  = np.array([-1.,-.8,-.6,-.4,-.2,.2,.4,.6,.8,1.])  
swlevels = [0.999999]
zeta_colors = ['cyan','green','gray']
#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nlay,nrow,ncol = 3,189,101
nscen = len( results_dir )
#--coordinate information
x0, y0  = 539750.0, 2785750.0
dx,dy   = 500., 500.
xcell, ycell = mfd.cell_coordinates(nrow,ncol,dx,dy)
xcell += x0
ycell += y0
xedge, yedge = mfd.edge_coordinates(nrow,ncol,dx,dy)
xedge += x0
yedge += y0
xmin,xmax = xedge.min(),xedge.max()
ymin,ymax = yedge.min(),yedge.max()
#--read ibound
ib_ref = os.path.join( REFDir, 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--read the top of the model
lse_ref = os.path.join( REFDir, 'UMD_URBAN_EDEN_TOPO.ref' )
model_lse = au.loadArrayFromFile(nrow,ncol,lse_ref)
#--read the top of the model
offshore_ref = os.path.join( REFDir, 'UMD_OFFSHORE.ref' )
offshore = au.loadArrayFromFile(nrow,ncol,offshore_ref)
#--read the bottom of the model
botm = np.empty( (nlay+1,nrow,ncol) )
botm[0,:,:] = np.copy( model_lse )
for ilay in xrange(0,nlay):
    bot_ref = os.path.join( REFDir, 'UMD_BOTM_L{0}.ref'.format( ilay+1 ) )
    b = au.loadArrayFromFile(nrow,ncol,bot_ref)
    botm[ilay+1] = np.copy( b )
h0_base = np.empty( (nrow,ncol), np.float )
for idx in xrange(0,nscen):
    hfile = os.path.join( model_dir, results_dir[idx], head_file )
    zfile = os.path.join( model_dir, results_dir[idx], zeta_file )
    #--get available times in the head file
    print 'processing...{0}'.format( os.path.join( results_dir[idx], head_file ) )
    headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,hfile)
    mf_time_list = headObj.get_time_list()
    ntimes = mf_time_list.shape[0]
    #--average head data
    h0_avg = np.zeros( (nrow,ncol), np.float )
    for jdx in xrange(0,ntimes):
        #--file position
        iposition = long( mf_time_list[jdx,3] )
        #--average head data
        totim,kstp,kper,h,success = headObj.get_array(iposition)
        hd = np.copy( h[0,:,:] )
        h0_avg += hd / float( ntimes )
    if idx == 0:
        h0_base = np.copy( h0_avg )
    #--zeta surface to extract
    print 'processing...{0}'.format( os.path.join( results_dir[idx], zeta_file ) )
    zetaObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,zfile)
    zeta_time_list = zetaObj.get_time_list(zta_text)
    #--get last zeta time
    iposition = long( zeta_time_list[-1,3] )
    #--read zeta data - final zeta surface
    z,totim,success = zetaObj.get_array(iposition)
    #--identify where the zeta surface is above the bottom of the model
    sw = np.zeros( (nlay,nrow,ncol), np.float )
    for ilay in xrange(0,nlay):
        sw[ilay,:,:] = SaltwaterPosition(nrow,ncol,botm[ilay+1,:,:],z[ilay,:,:])
        for irow in xrange(0,nrow):
            for jcol in xrange(0,ncol):
                if offshore[irow,jcol] == 2:
                   sw[ilay,irow,jcol] = 1 
    #--make the map 
    #--head plot
    ztf = mpl.pyplot.figure(figsize=(4.4, 6), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    ctitle = 'Average water-table'
    if idx > 0:
        ctitle = '{0}: {1}'.format( ctitle, ztext[idx] )
    ax.text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    temp = np.ma.masked_where(ib<1,h0_avg)
    hp = ax.imshow(temp,vmin=-1.5,vmax=2,cmap='jet_r',alpha=1.0,extent=[xmin,xmax,ymin,ymax])
    au.polyline_plot( ax, hydrography, 'blue' )
    au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='black', markerfacecolor='red' )
    au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='black', markerfacecolor='cyan' )
    au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
    ch = ax.contour(xcell,ycell,temp,levels=hdcontour,colors='k',linewidths=0.5)
    ax.clabel(ch,inline=1,fmt='%5.1f',fontsize=6)
    #--colorbar
    cax=mpl.pyplot.axes([0.75,0.065,0.025,0.20])
    mpl.pyplot.colorbar(hp,cax=cax,orientation='vertical')                                       
    cax.set_title('meters',size=8) 
    #--plot limits
    ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
    #--save the figure
    if idx == 0:
        output_name = os.path.join( OutputDir, 'Average_Head.png' )
    else:
        output_name = os.path.join( OutputDir, 'Average_Head_Scenario{0:02d}.png'.format( idx ) )
    print 'creating figure...{0}'.format( output_name )
    ztf.savefig(output_name,dpi=300)
    mpl.pyplot.close('all')
    gc.collect()
    #--head difference plot
    if idx > 0:
        ztf = mpl.pyplot.figure(figsize=(4.4, 6), facecolor='w')
        ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
        ax = ztf.add_subplot(1,1,1,aspect='equal')
        ctitle = 'Water-table difference'
        if idx > 0:
            ctitle = '{0}: {1}'.format( ctitle, ztext[idx] )
        ax.text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
        temp = np.ma.masked_where(ib<1,(h0_avg-h0_base))
        hp = ax.imshow(temp,vmin=-1,vmax=1,cmap='jet_r',alpha=1.0,extent=[xmin,xmax,ymin,ymax])
        au.polyline_plot( ax, hydrography, 'blue' )
        au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='black', markerfacecolor='red' )
        au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='black', markerfacecolor='cyan' )
        au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
        ch = ax.contour(xcell,ycell,temp,levels=ddncontour,colors='k',linewidths=0.5)
        ax.clabel(ch,inline=1,fmt='%5.1f',fontsize=6)
        #--colorbar
        cax=mpl.pyplot.axes([0.75,0.065,0.025,0.20])
        mpl.pyplot.colorbar(hp,cax=cax,orientation='vertical')                                       
        cax.set_title('meters',size=8) 
        #--plot limits
        ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
        #--save the figure
        output_name = os.path.join( OutputDir, 'Average_HeadDifference_Scenario{0:02d}-Base.png'.format( idx ) )
        print 'creating figure...{0}'.format( output_name )
        ztf.savefig(output_name,dpi=300)
        mpl.pyplot.close('all')
        gc.collect()
    #--plot final zeta
    ztf = figure(figsize=(4.4, 6), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    ctitle = 'Interface position'
    if idx > 0:
        ctitle = '{0}: {1}'.format( ctitle, ztext[idx] )
    ax.text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
#    temp = np.ma.masked_where(sw[nlay-1,:,:]<1,sw[nlay-1,:,:])
#    zim = ax.imshow(temp,vmin=0,vmax=2,cmap='gray',alpha=1.0,extent=[xmin,xmax,ymin,ymax],interpolation='none')
    pz = np.copy( sw[0,:,:] )
    for ilay in xrange(1,nlay):
        pz += sw[ilay,:,:]
    temp = np.ma.masked_where(pz<1,pz)
    temp = np.ma.masked_where(ib<1,temp)
    zim = ax.imshow(temp,vmin=0,vmax=4,cmap='gray_r',alpha=1.0,extent=[xmin,xmax,ymin,ymax],interpolation='none')
    au.polyline_plot( ax, hydrography, 'blue' )
    au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='black', markerfacecolor='red' )
    au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='black', markerfacecolor='cyan' )
    au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
    #--plot limits
    ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
    #--save the figure
    if idx == 0:
        output_name = os.path.join( OutputDir, 'Final_Zeta.png' )
    else:
        output_name = os.path.join( OutputDir, 'Final_Zeta_Scenario{0:02d}.png'.format( idx ) )
    print 'creating figure...{0}'.format( output_name )
    ztf.savefig(output_name,dpi=300)
    #--clear memory
    mpl.pyplot.close('all')
    gc.collect()
    
