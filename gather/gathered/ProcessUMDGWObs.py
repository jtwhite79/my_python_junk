import re
import sys
import os
import shutil
import math
import gc
import operator
from datetime import datetime,timedelta
import xml.etree.ElementTree as xml
import numpy as np
import MFArrayUtil as au
import MFData as mfd
import MFBinaryClass as mfb 
import pestUtil
import UMDUtils as umdutils

def Make_NewFigure():
    fwid, fhgt = 7.00, 9.00
    flft, frgt = 0.075, 0.925
    fbot, ftop = 0.10, 0.95
    fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
    fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
    return fig

def DailyMaskTime(outtime,intime,indata):
    Missing = 9999.
    nouttime = outtime.shape[0]
    outdata = np.empty( (nouttime), np.float )
    outdata.fill( Missing )
    for [d,v] in zip( intime, indata ):
        ipos = (d-outtime[0]).days
        if ipos < 0:
            continue
        elif ipos > nouttime - 1:
            break
        outdata[ipos] = v
    #--mask data
    return np.ma.masked_equal( outdata, Missing )

def DailyStatistics(obs,sim):
    Missing = 9999.
    me = 0.0
    mae = 0.0
    rmse = 0.0
    npairs = 0
    for [o,s] in zip(obs,sim):
        if o != Missing and s != Missing:
            npairs += 1
            me += (s - o)
            mae += abs( s - o )
            rmse += math.pow(( s - o ),2.0)
    if npairs > 0:
        me /= float(npairs)
        mae /= float(npairs)
        rmse /= float(npairs)
        rmse = math.sqrt( rmse )
    return me, mae, rmse, npairs 


#preliminary figure specifications
import pylab as pl
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates

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

Missing = 9999.
ft2m = 1.0 / 3.28081

#--file names
#--model ref files
IBOUND_file = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
DIS_file = os.path.join( '..', 'UMD.dis' )

#--read base xml data
xml_file = os.path.join( '..', 'xml', 'GWHead.xml' )
tree = xml.parse(xml_file)
root = tree.getroot()
HeadFile = root.find('HeadFile').text
ObsFile = root.find('ObsFile').text
start_date = datetime.strptime(root.find('StartDate').text,'%m/%d/%Y')
end_date = datetime.strptime(root.find('EndDate').text,'%m/%d/%Y')
child = root.find('InputUnits')
if child != None:
    cunits = child.text
else:
    cunits = 'meters'
child = root.find('OutputUnits')
if child != None:
    cunits = child.text
unit_conv = 1.0
child = root.find('OutputConversion')
if child != None:
    unit_conv = float(child.text)
#--determine the number of head sites
num_sites = 0
for gwhead in root.findall('gwhead'):
    num_sites += 1

#--get command line arguments
HeadBaseName = os.path.basename( HeadFile )
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
                #--replace path in HeadFile with the value passed from the command line
                HeadFile = os.path.join( ResultsDir, HeadBaseName )
                print 'command line arg: -resultsdir = ', ResultsDir
            except:
                print 'cannot parse command line arg: -resultsdir'


print 'processing head data from...{0}\nFor the period from {1} to {2}'.format( HeadFile, start_date, end_date )
print '  for {0} head stations'.format( num_sites )

#--read discretization data
offset,nlay,nrow,ncol,delr,delc = mfd.load_dis_file(DIS_file)
xedge,yedge = mfd.edge_coordinates(nrow,ncol,delr,delc)
#--open head file
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,HeadFile)
times = headObj.get_time_list()
#--read ibound
ib = au.loadArrayFromFile(nrow,ncol,IBOUND_file)
#--read the top of layer 1
top_file = os.path.join( '..', 'REF', 'UMD_URBAN_EDEN_TOPO.ref')
temp = au.loadArrayFromFile(nrow,ncol,top_file)
#--read layer bottoms
bot = np.zeros( (nlay+1,nrow,ncol), np.float )
bot[0,:,:] = np.copy( temp )
for k in xrange(0,nlay):
    bot_file = os.path.join( '..', 'REF', 'UMD_BOTM_L{0}.ref'.format( k+1 ))
    temp = au.loadArrayFromFile(nrow,ncol,bot_file)
    bot[k+1,:,:] = np.copy( temp )

#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'HeadObs' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--simulation dates
on_date = start_date
plot_dates = []
plot_dates.append( on_date )
while on_date < end_date:
    on_date += timedelta(days=1.)
    plot_dates.append( on_date )
plot_dates = np.array( plot_dates )

#--initialize figure and figure/plot counters
ifigure = 1
iplot = 1
nplots = 6
fig = Make_NewFigure()
#--matplotlib date specification
years, months = mdates.YearLocator(), mdates.MonthLocator()  #every year, every month
yearsFmt = mdates.DateFormatter('%Y')

#--open smp file
smp = pestUtil.smp(ObsFile,load=False,date_fmt='%m/%d/%Y')
#--process each station in the xml file
iwell = 0
pct_lay = np.empty( (nlay), np.float )
active_gwobs = []
active_gwobs_stats = []
for idx,gwhead in enumerate( root.findall('gwHead') ):
    station = gwhead.attrib['name']
    print 'Locating {0} in the model grid'.format( station )
    coordType = gwhead.find('coordType').text
    #--determine the location of the well
    if coordType.lower() == 'model':
        #--convert to zero based
        irow = int( gwhead.find('row').text ) - 1
        icol = int( gwhead.find('column').text ) - 1
    elif coordType.lower() == 'site':
        x = float( gwhead.find('coordX').text )
        y = float( gwhead.find('coordY').text )
        v = mfd.subtract_offset([[x,y]],offset)
        irow,icol = mfd.get_row_col(nrow,ncol,xedge,yedge,v[0][0],v[0][1])
    c = gwhead.find('layer')
    if c != None:
        ilay = int( gwhead.find('layer').text ) - 1
    else:
        dmult = 1.0
        c1 = gwhead.find('depthMult')
        if c1 != None:
            dmult = float( gwhead.find('depthMult').text )
        #--top and bottom of screen provided
        #  determine the layer with the maximum percentage of screen
        top = bot[0,irow,icol]
        ilay = -11
        c1 = gwhead.find('depthTop')
        if c1 != None:
            z0 = top - float( gwhead.find('depthTop').text ) * dmult
            z1 = top - float( gwhead.find('depthBot').text ) * dmult
            pct_lay.fill( 0.0 )
            max_pct = 0.0
            for k in xrange(0,nlay):
                if z0 <= bot[k+1,irow,icol]:
                    continue
                tl = min( z0, bot[k,irow,icol] )
                bl = max( z1, bot[k+1,irow,icol] )
                pct_lay[k] = ( tl - bl ) / ( z0 - z1 )
                if pct_lay[k] > max_pct:
                    max_pct = pct_lay[k]
                    ilay = k
                #print '   ***', k+1, tl, bl, pct_lay[k], z0, z1, bot[k,irow,icol], bot[k+1,irow,icol]
                if z1 >= bot[k+1,irow,icol]:
                    break
        #--single screen elevation specified
        #  determine the layer containing the specified elevation
        else:
            z = top - float( gwhead.find('depth').text ) * dmult
            for k in xrange(0,nlay):
                if z >= bot[k+1,irow,icol]:
                    ilay = k
                    break
    #--determine if the well is in an active portion of the model domain    
    useWell = True
    if irow*icol == 0:
        useWell = False
    if ib[irow,icol] < 1:
        useWell = False
    if ilay < 0 or ilay+1 > nlay:
        useWell = False
    if useWell == False:
        print '  Observation well {0} is in an inactive model cell'.format( station )
        continue
    #--deptermine if observation data should be processed
    processObs = False
    child = gwhead.find('readObs')
    if child != None:
        processObs = bool( child.text )
    active_gwobs.append( [station,ilay,irow,icol,processObs] )

#--read data and plot data for active wells
iwell = 0
for idx,t in enumerate( active_gwobs ):
    station = t[0]
    ilay = int( t[1] )
    irow = int( t[2] )
    icol = int( t[3] )
    processObs = bool( t[4] )
    print 'Processing head data for {0}'.format( station )
    #--read observed data
    nobs = 0
    if processObs == True:
        #--get the smp file data
        print '  ...reading observation data from smp file'
        records = smp.load(site=station)
        for record in records:
            a = np.copy( records[record] )
            #nobs = a.shape[0]
        for t in a[:,1]:
            t *= unit_conv
        for d in a[:,0]:
            if d >= start_date and d <= end_date:
                nobs += 1
    #--increment well counter
    iwell += 1
    #--read the simulated data
    print '  ...reading simulated data'
    inode = headObj.get_nodefromrcl(irow+1,icol+1,ilay+1)
    #success = headObj.rewind_file()
    #ce1 = headObj.get_gage(inode)
    ce1 = headObj.get_time_gage(inode)
    nt =  np.shape(ce1)[0]
    sim = np.zeros( (nt,2), np.float )
    for jdx in xrange(0,nt):
        sim[jdx,0] = ce1[jdx,0]
        sim[jdx,1] = ce1[jdx,1] * unit_conv
    #--plot the data
    ax = fig.add_subplot(nplots,1,iplot)
    #--plot the observed data
    if nobs > 0:
        obs = DailyMaskTime(plot_dates,a[:,0],a[:,1])
        ax.plot(pl.date2num(plot_dates),obs, color='b', linewidth=1.5, label='Observed')
    #--plot the simulated data
    sim = DailyMaskTime(plot_dates,plot_dates[0:sim.shape[0]],sim[:,1])
    ax.plot(pl.date2num(plot_dates),sim, color='r', linewidth=0.75, label='Simulated')
    #--calculate statistics
    cstats = ''
    me = 0.0
    mae = 0.0
    rmse = 0.0
    npairs = 0.0
    if nobs > 0:
        me, mae, rmse, npairs = DailyStatistics(obs,sim)
        if npairs > 0:
            cstats = 'ME {0: 5.3f} MAE {1: 5.3f} RMSE {2: 5.3f} Pairs {3}'.format( me, mae, rmse, npairs )
        else:
            cstats = 'Pairs {0}'.format( npairs )
    #--append to stats list
    active_gwobs_stats.append( [nobs,npairs,me,mae,rmse] )
    #--legends and axes
    leg = ax.legend(loc='best',ncol=1,labelspacing=0.25,columnspacing=1,\
                    handletextpad=0.5,handlelength=2.0,numpoints=1)
    leg._drawFrame=False
    ctxt = '{0} Layer {1:3d} Row {2:3d} Column {3:3d} LSE {4: 5.2f} Aquifer bottom {5: 5.2f}'.format( station, ilay+1, irow+1, icol+1, bot[0,irow,icol]*unit_conv, bot[nlay,irow,icol]*unit_conv ) 
    ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.set_xlim(start_date, end_date)
    ax.set_ylabel( 'Elevation, in {0}'.format( cunits ) )
    iplot += 1
    if iplot > nplots or idx == len( active_gwobs ) - 1:
        ax.set_xlabel( 'Year' )
        fout = os.path.join( OutputDir, 'UMD_HeadObs_{0:03d}.png'.format(ifigure) )
        fig.savefig(fout,dpi=300)
        print 'created...', fout
        #--clear memory
        SWRObj = None
        mpl.pyplot.close('all')
        gc.collect()
        #--reinitialize the figure
        fig = Make_NewFigure()
        #--update figure and plot counters
        ifigure += 1
        iplot = 1

stats_file = os.path.join( ResultsDir, 'UMD_GroundwaterStats.csv' )
f = open(stats_file, 'w')
f.write('"Well","Layer","Row","Column","Number of observations","Number of pairs","Mean error, in {0}","Mean absolute error in {1}","Root mean squared error in {2}"\n'.format(cunits,cunits,cunits) )
for idx,[t1,t2] in enumerate(zip(active_gwobs,active_gwobs_stats)):
    #--determine if any observation data is available
    if int( t2[0] ) < 1:
        continue
    f.write( '{0},{1},{2},{3},{4},{5},'.format( t1[0],t1[1],t1[2],t1[3],t2[0],t2[1] ) )
    if int( t2[1] ) > 0:
        f.write( '{0},{1},{2}'.format( t2[2],t2[3],t2[4] ) )
    else:
        f.write( '--,--,--' )
    f.write( '\n' )
f.close()
