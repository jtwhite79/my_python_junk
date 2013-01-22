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

def SaltwaterPosition(nrow,ncol,elev,zeta):
    elevmin = 0.1 #1.0e-6
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

#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nlay,nrow,ncol = 3,189,101
#--read ibound
ib_ref = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--read initial zetas
ref  = os.path.join( '..', 'REF', 'UMD_IZETA2_L1.ref' )
ztai1 = au.loadArrayFromFile(nrow,ncol,ref)
ref  = os.path.join( '..', 'REF', 'UMD_IZETA2_L2.ref' )
ztai2 = au.loadArrayFromFile(nrow,ncol,ref)
ref  = os.path.join( '..', 'REF', 'UMD_IZETA2_L3.ref' )
ztai3 = au.loadArrayFromFile(nrow,ncol,ref)
#--read the bottom of the model
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L1.ref' )
model_bot1 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L2.ref' )
model_bot2 = au.loadArrayFromFile(nrow,ncol,bot_ref)
bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L3.ref' )
model_bot3 = au.loadArrayFromFile(nrow,ncol,bot_ref)
#--identify where the zeta surface is above the bottom of the model
sw1 = SaltwaterPosition(nrow,ncol,model_bot1,ztai1)
sw2 = SaltwaterPosition(nrow,ncol,model_bot2,ztai2)
sw3 = SaltwaterPosition(nrow,ncol,model_bot3,ztai3)
#--mask data in inactive areas
sw1  = np.ma.masked_where(ib<1,sw1)
sw2  = np.ma.masked_where(ib<1,sw2)
sw3  = np.ma.masked_where(ib<1,sw3)
#--invert rows for plotting with pcolor
sw1  = np.flipud(sw1)
sw2  = np.flipud(sw2)
sw3  = np.flipud(sw3)
#--make a map 
#--read shapefile to use as base map on figures
shape_name = os.path.join( 'D:/','Data','Users','jdhughes','GIS','Project Data','2080DBF00','Spatial','FigureData','BaseMap' )
hydrography = sf.load_shape_list(shape_name)
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
#--calculate current date and create string of date
cdate = datetime.strftime( start_date, '%m/%d/%Y' )
#-Make figures
#--saltwater interface figure
output_name = os.path.join( '..', 'Figures', 'Zeta', 'Zeta_{0:05d}.png'.format( int( 0 ) ) )
print 'creating figure...{0}'.format( output_name )
ztf = figure(figsize=(4.4, 6), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
ax = ztf.add_subplot(1,1,1,aspect='equal')
ctitle = 'Position of the interface toe on {0}'.format( cdate )
text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
au.polyline_plot( ax, hydrography, '0.25' )
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


