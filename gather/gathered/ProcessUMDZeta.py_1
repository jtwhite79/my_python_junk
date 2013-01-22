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

def SaltwaterPosition(nrow,ncol,elev,zeta):
    elevmin = 0.2 #1.0e-6
    value = np.zeros( (nrow,ncol), np.float )
    for irow in xrange(0,nrow):
        for jcol in xrange(0,ncol):
            if zeta[irow,jcol] > elev[irow,jcol] + elevmin:
                value[irow,jcol] = 1.0
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
#--read the bottom of the model
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L1.ref' )
model_bot1 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L2.ref' )
model_bot2 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L3.ref' )
model_bot3 = au.loadArrayFromFile(nrow,ncol,bot_ref)
#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'Zeta' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--default data if command line argument not defined for variable
head_file = os.path.join( ResultsDir, 'UMD.hds' )
zeta_file = os.path.join( ResultsDir, 'UMD.zta' )
#--get available times in the head file
#--zeta surface to extract
zta_text = '    ZETAPLANE  2'
zetaObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,zeta_file)
times = zetaObj.get_time_list(zta_text)
ntimes = times.shape[0]
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
#--contour intervals
swlevels = [0.999999]
#--create figures for each output time
icount = 0
iweek = 0
for i in xrange(0,ntimes):
    #--only process every 7th value
    icount += 1
    if icount < 7:
        continue
    else:
        icount = 0
        iweek += 1
    on_time = i + 1
    iposition = long( times[i,3] )
    #--read zeta data - final zeta surface
    #zetaObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,zeta_file)
    #z,totim,success = zetaObj.get_record(findsurf,kstp,kper)
    #zt = np.copy( z[nlay-1,:,:] )    
    z,totim,success = zetaObj.get_array(iposition)
    #--identify where the zeta surface is above the bottom of the model
    sw1 = SaltwaterPosition(nrow,ncol,model_bot1,z[0,:,:])
    sw2 = SaltwaterPosition(nrow,ncol,model_bot2,z[1,:,:])
    sw3 = SaltwaterPosition(nrow,ncol,model_bot3,z[2,:,:])
    #--mask data in inactive areas
    sw1  = np.ma.masked_where(ib<1,sw1)
    sw2  = np.ma.masked_where(ib<1,sw2)
    sw3  = np.ma.masked_where(ib<1,sw3)
    #--invert rows for plotting with pcolor
    sw1  = np.flipud(sw1)
    sw2  = np.flipud(sw2)
    sw3  = np.flipud(sw3)
    #--calculate current date and create string of date
    on_date = start_date + timedelta(days=on_time)
    cdate = datetime.strftime( on_date, '%m/%d/%Y' )
    #-Make figures
    #--saltwater interface figure
    output_name = os.path.join( OutputDir, 'Zeta_{0:05d}.png'.format( int( iweek ) ) )
    print 'creating figure...{0}'.format( output_name )
    ztf = figure(figsize=(4.4, 6), facecolor='w')
    ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
    ax = ztf.add_subplot(1,1,1,aspect='equal')
    ctitle = 'Position of the interface toe on {0}'.format( cdate )
    text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    au.polyline_plot( ax, hydrography, '0.25' )
    au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='red', markerfacecolor='red' )
    au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='blue', markerfacecolor='white' )
    au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
    ch1 = ax.contour(xcell,ycell,sw1,levels=swlevels,colors='b',linewidths=0.5)
    ch2 = ax.contour(xcell,ycell,sw2,levels=swlevels,colors='g',linewidths=0.5)
    ch3 = ax.contour(xcell,ycell,sw3,levels=swlevels,colors='r',linewidths=0.5)
    #--plot limits
    ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
    #--save the figure
    ztf.savefig(output_name,dpi=300)
    #--clear memory
    mpl.pyplot.close('all')
    gc.collect()


