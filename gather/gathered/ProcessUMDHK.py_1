import sys
import os
import math
import numpy as np
import pylab
import gc

from datetime import datetime
from datetime import timedelta

import MFArrayUtil as au
import MFBinaryClass as mfb 
import shapefile as sf

import UMDUtils as umdutils

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
ResultsDir = os.path.join( '..', 'Results' )
narg = len(sys.argv)
iarg = 0
if narg > 1:
    while iarg < narg-1:
        iarg += 1
        basearg = sys.argv[iarg].lower()
        if basearg == '-resultsdir':
            try:
                iarg += 1
                ResultsDir = sys.argv[iarg]
                print 'command line arg: -resultsdir = ', ResultsDir
            except:
                print 'cannot parse command line arg: -resultsdir'

#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nlay,nrow,ncol = 3,189,101
#--read ibound
ib_ref = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--read the top of the model
lse_ref = os.path.join( '..', 'REF', 'UMD_URBAN_EDEN_TOPO.ref' )
model_lse = au.loadArrayFromFile(nrow,ncol,lse_ref)
#--
botm = np.zeros( (nlay+1,nrow,ncol), np.float )
thick = np.zeros( (nlay,nrow,ncol), np.float )
botm[0,:,:] = np.copy( model_lse )
for ilay in xrange(0,nlay):
    fname = os.path.join( '..', 'REF', 'UMD_BOTM_L{0}.ref'.format( ilay+1 ) )
    botm[ilay+1,:,:] = au.loadArrayFromFile(nrow,ncol,fname)
    thick[ilay,:,:] = botm[ilay,:,:] - botm[ilay+1,:,:]
#--make sure output directories exist
OutputPropertiesDir = os.path.join( ResultsDir, 'Figures', 'Properties' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputPropertiesDir, 'dir.tst' )])
#--HK
HK = np.zeros( (nlay+1,nrow,ncol), np.float )
for ilay in xrange(0,nlay):
    fname = os.path.join( '..', 'REF', 'UMD_HK_L{0}.ref'.format( ilay+1 ) )
    HK[ilay,:,:] = au.loadArrayFromFile(nrow,ncol,fname)
    HK[nlay,:,:] = HK[nlay,:,:] + HK[ilay,:,:] * thick[ilay,:,:]
#--make a map 
#--read shapefile to use as base map on figures
shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','BaseMap')
hydrography = sf.load_shape_list(shape_name)
salinity_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','SalinityControlStructures')
salinity_struc = sf.load_shape_list(salinity_struct_shape_name)
df_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','DrainageFloodControlStructures')
df_struc = sf.load_shape_list(df_struct_shape_name)
pws_struct_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','Water Use','pumpwells_lb')
pws = sf.load_shape_list(pws_struct_shape_name)
hk_loc_shape_name = os.path.join('D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','HK_PTS')
hk_loc = sf.load_shape_list(hk_loc_shape_name)
#--coordinate information
x0, y0  = 539750.0, 2785750.0
dx,dy   = 500., 500.
xcell = np.arange(x0+dx/2.,x0+(ncol*dx)+dx/2.0,dx)
ycell = np.arange(y0+dy/2.,y0+(nrow*dy)+dy/2.0,dy)
Xcell,Ycell = np.meshgrid(xcell,ycell)
xedge = np.arange(x0,x0+float(ncol)*dx+0.001,dx)
yedge = np.arange(y0,y0+float(nrow)*dy+0.001,dy)
Xedge,Yedge = np.meshgrid(xedge,yedge)
xmin,xmax = x0,x0+float(ncol)*dx
ymin,ymax = y0,y0+float(nrow)*dy
#--common data for each figure
x1 = np.arange(0.0,6.0,0.25)
hkcontour = np.power(10.,x1)
hkcontour = [1.,2.5,5.,7.5,10.,25.,50.,75.,100.,250.,500.,750.,1000.,2500.,5000.,7500.,10000.,25000.,50000.]
x1 = np.arange(4.0,6.0,0.25)
tcontour = [1.e3,2.5e3,5.e3,7.5e3,1.e4,2.5e4,5.e4,7.5e4,1.e5,2.5e5,5.e5,7.5e5,1.e6]
imin = [2, 0, 2]
imax = [5, 2, 5]
#--create figures for each output time
for ilay in xrange(0,nlay+1):
    lv = np.log10( HK[ilay,:,:] )
    lv  = np.ma.masked_where(ib<1,lv)
    #--invert rows for plotting with pcolor
    v  = np.ma.masked_where(ib<1,np.copy(HK[ilay,:,:]))
    v  = np.flipud(v)
    #--calculate ranges
    minv, maxv = np.min(v), np.max(v)
    #--print summary of min and max hk
    print 'HK [{0:10.3f},{1:10.3f}]'.format(minv,maxv)
    #-Make figures
    #--head figure
    if ilay < nlay:
        output_name = os.path.join( OutputPropertiesDir, 'UMD_HK_L{0}.png'.format( ilay+1 ) )
        cc = hkcontour
        vmin,vmax = imin[ilay], imax[ilay]
        ctitle = 'Horizontal hydraulic conductivity layer {0}, in m/d'.format( ilay + 1 )
    else:
        output_name = os.path.join( OutputPropertiesDir, 'UMD_T.png' )
        cc = tcontour
        vmin,vmax = 3., 5.
        ctitle = 'Transmissivity, in m2/d'.format( ilay + 1 )
    print 'creating figure...{0}'.format( output_name )
    ztf = figure(figsize=(4.4, 6), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    hp = ax.imshow(lv,vmin=vmin,vmax=vmax,cmap='jet_r',alpha=1.0,extent=[xmin,xmax,ymin,ymax])
    au.polyline_plot( ax, hydrography, '0.25' )
    au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='red', markerfacecolor='red' )
    au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='blue', markerfacecolor='white' )
    au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
    au.point_plot( ax, pws, marker='+', markersize=3, markeredgecolor='black', markerfacecolor='black' )
    ch = ax.contour(xcell,ycell,v,levels=cc,colors='k',linewidths=0.5)
    ax.clabel(ch,inline=1,fmt='%5.1f',fontsize=6)
    #--plot limits
    ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
    #--save the figure
    ztf.savefig(output_name,dpi=300)
    #--clear memory
    mpl.pyplot.close('all')
    gc.collect()
