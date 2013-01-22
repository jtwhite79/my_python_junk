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

def arr3darr2d( nlay,nrow,ncol,t ):
    r = np.zeros( (nrow,ncol), np.float )
    for ilay in xrange(0,nlay):
        r += t[ilay,:,:]
    return r

def arr2dmask( ib,t ):
    return (np.ma.masked_where(ib<1,t))

def arr2dmaskzero( t ):
    return (np.ma.masked_where(t==0.0,t))

def plotData( cyear, cunits, ib, d_avg, f_text, d_text, metlevels, metcmap, \
              xmin, xmax, ymin, ymax, vmin, vmax, \
              hydrography, salinity_struc, df_struc, pws ):
    for jdx in xrange(0,len(d_text)):
        #-Make figures
        output_name = os.path.join( OutputDir, '{0}_{1}.png'.format( f_text[jdx],cyear ) )
        print 'creating figure...{0}'.format( output_name )
        ztf = figure(figsize=(4.4, 6), facecolor='w')
        ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.05,right=0.95,bottom=0.05,top=0.95)
        ax = ztf.add_subplot(1,1,1,aspect='equal')
        ctitle = '{0} {1}'.format( d_text[jdx], cyear )
        ax.text(0.0,1.01,ctitle,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
        temp = arr2dmask( ib,d_avg[jdx,:,:] )
        temp = arr2dmaskzero( temp )
        hp = ax.imshow(temp,cmap=metcmap[jdx],vmin=vmin[jdx],vmax=vmax[jdx],alpha=1.0,extent=[xmin,xmax,ymin,ymax],interpolation='None')
        au.polyline_plot( ax, hydrography, '0.25' )
        au.point_plot( ax, salinity_struc, marker='o', markersize=3, markeredgecolor='black', markerfacecolor='red' )
        au.point_plot( ax, df_struc, marker='s', markersize=3, markeredgecolor='black', markerfacecolor='cyan' )
        au.point_plot( ax, pws, marker='o', markersize=1, markeredgecolor='black', markerfacecolor='black' )
        ch = ax.contour(xcell,ycell,np.flipud(temp),levels=metlevels,colors='k',linewidths=0.5)
        ax.clabel(ch,inline=1,fmt='%3d',fontsize=6)
        #--colorbar
        cax=axes([0.740,0.065,0.025,0.20])
        colorbar(hp,cax=cax,orientation='vertical')                                       
        cax.set_title(cunits,size=8) 
        #--plot limits
        ax.set_xlim(xmin,xmax), ax.set_ylim(ymin,ymax)
        #--save the figure
        ztf.savefig(output_name,dpi=300)
        #--clear memory
        mpl.pyplot.close('all')
        gc.collect()
#--return
    return (True)
        


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
useSIUnits = False
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
        elif basearg == '-usesiunits':
            useSIUnits = True
            print 'output will be in SI units'
#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nlay,nrow,ncol = 3,189,101
#--read ibound
ib_ref = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'AnnualMET' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--default data if command line argument not defined for variable
met_file = os.path.join( ResultsDir, 'UMD.MET.bin' )
#--get available times in the head file
#--zeta surface to extract
metObj = mfb.MODFLOW_CBB(nlay,nrow,ncol,met_file)
text = '     ET SEGMENTS'
sys.stdout.write( 'Building time list for...{0}\n'.format( text ) ) 
ets_time_list = metObj.get_time_list(text)
text = ' NEXRAD RAINFALL'
sys.stdout.write( 'Building time list for...{0}\n'.format( text ) ) 
rch_time_list = metObj.get_time_list(text)
text = '   SEPTIC RETURN'
sys.stdout.write( 'Building time list for...{0}\n'.format( text ) ) 
sep_time_list = metObj.get_time_list(text)
ntimes = sep_time_list.shape[0]
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
scale = 3.28081 * 12. / ( dx * dy )
cunits = 'in/yr'
scaleSI = 1.0
if useSIUnits == True:
    scaleSI = 25.4
    scale *= scaleSI
    cunits = 'mm/yr'
#--annual arrays
d_text = ['Actual Evapotranspiration','NEXRAD Rainfall','Septic Return Flow','Net recharge']
f_text = ['EVT','RCH','SEPTIC','NETRCH']
d_avg = np.zeros( (len(d_text),nrow,ncol), np.float )
d_sim = np.zeros( (len(d_text),nrow,ncol), np.float )
#for idx in xrange(0,len(d_text)):
#    d_avg[idx,:,:] = np.ma.masked_where(ib<1,d_avg[idx,:,:])
#--contour intervals
if useSIUnits == True:
    metlevels = np.arange(-2000.,2000.,250.)
    vmin = np.array([500., 500., 0., -2000.])
    vmax = np.array([2000., 2000., 250., 2000.])
else:
    metlevels = np.arange(-70,70,10)
    vmin = np.array([20., 20., 0., -70.])
    vmax = np.array([70., 70., 10., 70.])
metcmap = ['GnBu','GnBu','GnBu','jet_r']
#--create figures for each output time
last_year = start_date.year
ndays = 0
dyears = 0.0
ntotal_days = 0
for idx in xrange(0,ntimes):
    #--calculate current date and create string of date
    on_date = start_date + timedelta(days=idx)
    on_year = on_date.year
    cdate = datetime.strftime( on_date, '%m/%d/%Y' )
    if on_year != last_year:
        cyear = '{0:04d}'.format( last_year )
        success = plotData( cyear, cunits, ib, d_avg, f_text, d_text, metlevels, metcmap, \
                            xmin, xmax, ymin, ymax, vmin, vmax, \
                            hydrography, salinity_struc, df_struc, pws )
        #--finish up
        ndays = 0
        dyears += 1.0
        last_year = on_year
        d_avg.fill( 0.0 )
    #--increment number of days
    ndays += 1
    ntotal_days += 1
    #--read data
    #--evapotranspiration
    ipos = 0
    sys.stdout.write( 'Processing data for {0}'.format( cdate ) )
    iposition = long( ets_time_list[idx,3] )
    t,totim,success = metObj.get_array(iposition)
    t0 = arr3darr2d( nlay,nrow,ncol,t )
    d_avg[ipos,:,:] -= np.copy( t0 ) * scale
    d_sim[ipos,:,:] -= np.copy( t0 ) * scale
    sys.stdout.write( ' {0}'.format( f_text[ipos] ) )
    #--rainfall
    ipos += 1
    iposition = long( rch_time_list[idx,3] )
    t,totim,success = metObj.get_array(iposition)
    t1 = arr3darr2d( nlay,nrow,ncol,t )
    d_avg[ipos,:,:] += np.copy( t1 ) * scale
    d_sim[ipos,:,:] += np.copy( t1 ) * scale
    sys.stdout.write( ' {0}'.format( f_text[ipos] ) )
    #--septic return
    ipos += 1
    iposition = long( sep_time_list[idx,3] )
    t,totim,success = metObj.get_array(iposition)
    t2 = arr3darr2d( nlay,nrow,ncol,t )
    d_avg[ipos,:,:] += np.copy( t2 ) * scale
    d_sim[ipos,:,:] += np.copy( t2 ) * scale
    sys.stdout.write( ' {0}'.format( f_text[ipos] ) )
    #--net recharge
    ipos += 1
    sys.stdout.write( '\n' )
    d_avg[ipos,:,:] += ( t1 + t2 + t0 ) * scale
    d_sim[ipos,:,:] += ( t1 + t2 + t0 ) * scale

##-calculate and plot average value for the entire simulation period
d_sim /= dyears
cyear = '{0:04d}-{1:04d}'.format( start_date.year, last_year )
success = plotData( cyear, cunits, ib, d_sim, f_text, d_text, metlevels, metcmap, \
                    xmin, xmax, ymin, ymax, vmin, vmax, \
                    hydrography, salinity_struc, df_struc, pws )
