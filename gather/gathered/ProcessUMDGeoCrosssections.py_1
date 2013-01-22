import sys
import os
import gc
import math
from datetime import datetime
from datetime import timedelta
import numpy as np
import shapefile as sf
import pylab as pl
import MFArrayUtil as au
import MFArrayUtil as au
import UMDUtils as umdutils
import MFData as mfd
import MFBinaryClass as mfb 
import pestUtil as pu

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

def Make_NewFigure():
    fwid, fhgt = 7.00, 1.75
    flft, frgt = 0.075, 0.95
    fbot, ftop = 0.1750, 0.925
    fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
    fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
    return fig

def findMinTwoVectors( v0, v1 ):
    n0 = v0.shape[0]
    n1 = v1.shape[0]
    if n0 == n1 or n0 > n1:
        vr = np.copy( v0 )
        for idx in xrange(0,n1):
            if v1[idx] < vr[idx]:
                vr[idx] = v1[idx]
    else:
        vr = np.copy( v1 )
        for idx in xrange(0,n0):
            if v0[idx] < vr[idx]:
                vr[idx] = v0[idx]
    return vr

def findMaxTwoVectors( v0, v1 ):
    n0 = v0.shape[0]
    n1 = v1.shape[0]
    if n0 == n1 or n0 > n1:
        vr = np.copy( v0 )
        for idx in xrange(0,n1):
            if v1[idx] > vr[idx]:
                vr[idx] = v1[idx]
    else:
        vr = np.copy( v1 )
        for idx in xrange(0,n0):
            if v0[idx] > vr[idx]:
                vr[idx] = v0[idx]
    return vr

#--main script
ft2m = 1.0 / 3.28081
#--get command line arguments
smp_ref = os.path.join( '..','obsref','stage', 'S123_T.smp')
ResultsDir = os.path.join( '..', 'Results' )
sl_change = 0.0
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
        elif basearg == '-slsmp':
            try:
                iarg += 1
                smp_ref = sys.argv[iarg]
                print 'command line arg: -slsmp = ', smp_ref
            except:
                print 'cannot parse command line arg: -slsmp'
        elif basearg == '-dsl':
            try:
                iarg += 1
                sl_change = float( sys.argv[iarg] )
                print 'command line arg: -dsl = ', sl_change
            except:
                print 'cannot parse command line arg: -dsl'
        elif basearg == '-dslft':
            try:
                iarg += 1
                sl_change = float( sys.argv[iarg] ) 
                print 'command line arg: -dslft = ', sl_change
                sl_change *= ft2m
                print 'dslft converted to m = ', sl_change
            except:
                print 'cannot parse command line arg: -dslft'

#--model start date
start_date = datetime.strptime( "19960101", "%Y%m%d")
#--problem size
nsurf,nlay,nrow,ncol = 2,3,189,101
#--read ibound
ib_ref = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
ib = au.loadArrayFromFile(nrow,ncol,ib_ref)
#--get layer geometry
botm = np.empty( (nlay+1,nrow,ncol), np.float )
#--read the top of the model
lse_ref = os.path.join( '..', 'REF', 'UMD_URBAN_EDEN_TOPO.ref' )
botm[0,:,:] = au.loadArrayFromFile(nrow,ncol,lse_ref)
#--read the bottom of the model
for ilay in xrange(0,nlay):
    bot_ref = os.path.join( '..', 'REF', 'UMD_BOTM_L{0}.ref'.format( ilay+1 ) )
    botm[ilay+1,:,:] = au.loadArrayFromFile(nrow,ncol,bot_ref)
#--read the Q surface data
nQ = 5
Qsurf = np.empty( (nQ,nrow,ncol), np.float )
for iQ in xrange(0,nQ):
    Q_ref = os.path.join( '..', 'REF', 'UMD_Q{0}E.ref'.format( nQ-iQ ) )
    Qsurf[iQ,:,:] = au.loadArrayFromFile(nrow,ncol,Q_ref)
#--smp data is already in m NAVD 88
smp = pu.smp(smp_ref,load=True,date_fmt='%m/%d/%Y')
site_names = smp.get_site_list()
site1 = site_names[0]
fs, d, v = smp.get_site(site1)
mean_sl = np.mean(v) + sl_change
#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'XSECT' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--default data if command line argument not defined for variable
head_file = os.path.join( ResultsDir, 'UMD.hds' )
#--get available times in the head file
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
mf_time_list = headObj.get_time_list()
ntimes = mf_time_list.shape[0]
mf_times = np.zeros( (ntimes), np.float )
for i in range(0,ntimes):
    mf_times[i] = mf_time_list[i,0]
h0_avg = np.zeros( (nrow,ncol), np.float )
for idx in xrange(0,ntimes):
    #--get head and zeta data
    ipointer = long( mf_time_list[idx,3] )
    totim,kstp,kper,h,success = headObj.get_array(ipointer)
    hd = np.copy( h[0,:,:] )
    h0_avg += hd / float( ntimes )
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
#--read shapefile with cross-section data
shape_name = os.path.join( '..','GIS','UMDCrossSections' )
print shape_name
xsect_list = sf.load_shape_list(shape_name)
shapes,records = sf.load_as_dict(shape_name)
nxsect = len(shapes)
xsect_name = []
xsect_label = []
for idx in xrange( 0, nxsect ):
    xsect_name.append( records['XSECT'][idx].replace(' ','') )
    xsect_label.append( records['Label'][idx] )
#--create crossection figures
dxsect = 5.
ifigure = 0
lay_width = [0.5,0.5,0.5,0.5]
lay_color = ['k','k','k','k']
#             fresh     brackish  saltwater
surf_color = ['#00FFFF','#ADD8E6','#00FFFF']
for idx,xsect in enumerate( xsect_list ):
    #--make figure
    fig = Make_NewFigure()
    ax = fig.add_subplot(1,1,1)
    #--build list of points along current line
    #pts = mfd.makeEqualSpacePointsAlongLine(dxsect,xsect[0,:],xsect[1,:])
    pts = mfd.makeCellEdgePointsAlongLine(xsect[0,:],xsect[1,:],xedge,yedge)
    #--plot a few things on the surface
    iv = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,ib)
    tv = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[0,:,:])
    d = np.copy( tv[:,0] )
    b = np.copy( tv[:,1] )
    #--sea-level
    s = np.empty( d.shape[0], np.float )
    s.fill( mean_sl )
    s = findMaxTwoVectors( s, b )
    dp = np.ma.masked_where(iv[:,1]<2,d)
    sp = np.ma.masked_where(iv[:,1]<2,s)
    bp = np.ma.masked_where(iv[:,1]<2,b)
    ax.fill_between(dp,y1=sp,y2=bp,color='#0000A0',linewidth=0.)
    #--reference line for sea level
    s.fill( mean_sl )
    ax.plot(d,s,color='#0000A0',linewidth=0.5)
    #--interpolate geometry data to points
    for ilay in xrange(0,nlay):
        t = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[ilay,:,:])
        if ilay == 0:
            h0 = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,h0_avg[:,:])
            s = findMinTwoVectors( t[:,1], h0[:,1] )
            t[:,1] = s
        b = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[ilay+1,:,:])
        #--plot fill_between for zone
        ax.fill_between(t[:,0],y1=t[:,1],y2=b[:,1],color=surf_color[ilay],linewidth=0.)    
        #--geometry data
        #surf = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[ilay,:,:])
        #ax.plot(surf[:,0],surf[:,1], color=lay_color[ilay], linewidth=lay_width[ilay])
    #--top of the aquifer
    aqt = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[0,:,:])
    ax.plot(aqt[:,0],aqt[:,1], color='k', linewidth=0.5)
    #--bottom of the aquifer
    aqb = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,botm[nlay,:,:])
    ax.fill_between(aqb[:,0],y1=aqb[:,1],y2=aqb[:,1].min(),color='0.5',linewidth=0.)    
    ax.plot(aqb[:,0],aqb[:,1], color=lay_color[nlay], linewidth=lay_width[nlay])
    #--Q surfaces
    for iQ in xrange(0,nQ):
        q = mfd.cellValueAtPoints(pts[:,0],pts[:,1],pts[:,2],xedge,yedge,Qsurf[iQ,:,:])
        #print q[:,1]
        ax.plot(q[:,0],q[:,1], color='k', linestyle='solid', linewidth=0.5)
    #--cross-section labels
    ctitle = "{0}".format( xsect_label[idx] )
    text(0.0,1.02,ctitle,horizontalalignment='center',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ctitle = "{0}'".format( xsect_label[idx] )
    text(1.0,1.02,ctitle,horizontalalignment='center',verticalalignment='bottom',size=7,transform=ax.transAxes)
    #--plot limits
    ax.set_xlim(aqb[:,0].min(),aqb[:,0].max()), ax.set_ylim(aqb[:,1].min(),5)
    #--axis labels
    ax.set_xlabel('Horizontal distance, in meters')
    ax.set_ylabel('Elevation, in meters')

    ifigure += 1
    fout = os.path.join( OutputDir, 'UMD_GEOXSECT_{0}.png'.format( xsect_name[idx] ) )
    fig.savefig(fout,dpi=300)
    print 'created...', fout
    #--clear memory
    mpl.pyplot.close('all')
    gc.collect()
