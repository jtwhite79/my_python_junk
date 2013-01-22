import re
import sys
import os
import shutil
import math
import gc
import operator
#from operator import itemgetter
from datetime import datetime,timedelta
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

def sort_table(table, cols, directions=False):
    """ sort a table by multiple columns
        table: a list of lists (or tuple of tuples) where each inner list 
               represents a row
        cols:  a list (or tuple) specifying the column numbers to sort by
               e.g. (1,0) would sort by column 1, then by column 0
    """
    for [col,direction] in reversed(zip(cols,directions)):
        table = sorted(table, key=operator.itemgetter(col),reverse=direction)
    return table

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

#--file names
#--locations of observation locations
station_file = 'nwis_head_obs_location.csv'
#--model ref files
IBOUND_file = os.path.join( '..', 'REF', 'UMD_IBOUND.ref' )
DIS_file = os.path.join( '..', 'UMD.dis' )
#--observation well data
gw_smp_file = os.path.join( '..', 'obsref','head', 'All_NWIS_GW.smp' )
#--model results
head_file = os.path.join( ResultsDir, 'UMD.hds' )
#--output files
gw_loc_file = os.path.join( ResultsDir, 'mod2obs_loc.dat' )
gw_sum_file = os.path.join( ResultsDir, 'gw_sum_file.dat' )
#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'Obs' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--simulation dates
start_date = datetime.strptime( "19960101", "%Y%m%d") + timedelta(hours=12)
end_date = datetime.strptime( "20101231", "%Y%m%d") + timedelta(hours=12)
on_date = start_date
plot_dates = []
plot_dates.append( on_date )
while on_date < end_date:
    on_date += timedelta(days=1)
    plot_dates.append( on_date )
plot_dates = np.array( plot_dates )

#--open smp file
smp = pestUtil.smp(gw_smp_file,load=False,date_fmt='%m/%d/%Y')

#--site information
sites_header = []
sites = []
sites_dict = {}
f = open(station_file, 'r')
for idx,line in enumerate( f ):
    line = line.rstrip('\n')
    t = line.split(',')
    #--create site_header
    if idx == 0:
        for j in xrange(0,len(t)):
            sites_header.append( t[j] )
            sites_dict[t[j]] = j
        continue
    #--determine if any duplicate stations -- only keep the first instance
    idup = 0
    on_site_no = t[sites_dict['SITE_NO']]
    for tt in sites:
        if tt[sites_dict['SITE_NO']] == on_site_no:
            idup = 1
            print 'duplicate: {0}'.format( on_site_no )
            break
    if idup == 1:
        continue
    #--append t to sites
    sites.append( t )
f.close()

#sort data in the y and then x direction
#sites.sort(key=operator.itemgetter(sites_dict['Y_UTM'],sites_dict['X_UTM']))
sites = sort_table(sites, (sites_dict['Y_UTM'],sites_dict['X_UTM']), (True,False))

num_sites = len( sites )
sites = np.array( sites )

#--read discretization data
offset,nlay,nrow,ncol,delr,delc = mfd.load_dis_file(DIS_file)
xedge,yedge = mfd.edge_coordinates(nrow,ncol,delr,delc)
#--open head file
headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
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
#--open summary file
f = open(gw_loc_file, 'w')
fs = open(gw_sum_file, 'w')
fs.write( 'NO. WID SITE_NAME            X_UTM           Y_UTM      LAYER        ROW     COLUMN  LAND_SURF_ELEV      SCREEN_TOP   SCREEN_BOTTOM       LAYER_TOP    LAYER_BOTTOM         ME        MAE       RMSE     NPAIRS\n' )
#--initialize figure and figure/plot counters
ifigure = 1
iplot = 1
nplots = 6
fig = Make_NewFigure()
#--matplotlib date specification
years, months = mdates.YearLocator(), mdates.MonthLocator()  #every year, every month
yearsFmt = mdates.DateFormatter('%Y')
#--determine layer, row, column location and plot simulated and observed data
iwell = 0
for idx,site in enumerate(sites):
    #--locate observation well
    x = float(site[sites_dict['X_UTM']])
    y = float(site[sites_dict['Y_UTM']])
    SITE_NAME = site[sites_dict['SITE_NAME']]
    v = mfd.subtract_offset([[x,y]],offset)
    irow,icol = mfd.get_row_col(nrow,ncol,xedge,yedge,v[0][0],v[0][1])
    iuse = 1
    if irow*icol == 0:
        iuse = 0
    if ib[irow,icol] < 1:
        iuse = 0
    if iuse < 1:
        continue
    screen_top = float( site[sites_dict['SCREEN_TOP_FT']] )
    ilay = -11
    find_pt = False
    if screen_top == Missing:
        ilay = 0
        screen_top = Missing
        screen_bot = Missing
        avg_screen = Missing
    else:
        screen_top  = bot[0,irow,icol] - screen_top * ft2m
        cscreen_bot = site[sites_dict['SCREEN_BOTTOM_FT']]
        try:
            screen_bot = max( bot[0,irow,icol] - float( cscreen_bot ) * ft2m, bot[nlay,irow,icol] )
            if screen_top < screen_bot:
                #t = screen_top
                screen_top = screen_bot
                #screen_bot = t
            if screen_top == screen_bot:
                find_pt = True
            elif screen_top == bot[nlay,irow,icol]:
                fnd_pt = True
                screen_bot = screen_top
            else:
                pct_lay = np.zeros( (nlay), np.float )
                max_pct = 0.0
                for k in xrange(0,nlay):
                    if screen_top <= bot[k+1,irow,icol]:
                        continue
                    tl = min( screen_top, bot[k,irow,icol] )
                    bl = max( screen_bot, bot[k+1,irow,icol] )
                    pct_lay[k] = ( tl - bl ) / ( screen_top - screen_bot )
                    if pct_lay[k] > max_pct:
                        max_pct = pct_lay[k]
                        ilay = k
                    #print '   ***', k+1, tl, bl, pct_lay[k], screen_top, screen_bot, bot[k,irow,icol], bot[k+1,irow,icol]
                    if screen_bot >= bot[k+1,irow,icol]:
                        break
        except:
            find_pt = True
        #--find layer corresponding to screen_top (which equals screen_bot)
        if find_pt == True:
           for k in xrange(0,nlay):
               if screen_top >= bot[k+1,irow,icol]:
                   ilay = k
                   break
    #--determine if the well intecepts the model
    if ilay < 0:
        #continue
        ilay = -11
    #--increment well counter
    iwell += 1
    #--get the smp file data
    records = smp.load(site=SITE_NAME)
    nobs = 0
    for record in records:
        a = np.copy( records[record] )
        nobs = a.shape[0]
    #--read the simulated data
    inode = headObj.get_nodefromrcl(irow+1,icol+1,ilay+1)
    success = headObj.rewind_file()
    sim = headObj.get_gage(inode)
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
    #--legends and axes
    leg = ax.legend(loc='best',ncol=1,labelspacing=0.25,columnspacing=1,\
                    handletextpad=0.5,handlelength=2.0,numpoints=1)
    leg._drawFrame=False
    ctxt = '{0} Layer {1:3d} Row {2:3d} Column {3:3d} LSE {4: 5.2f}'.format( SITE_NAME, ilay+1, irow+1, icol+1, bot[0,irow,icol] ) 
    ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.set_xlim(start_date, end_date)
    ax.set_ylabel( 'Elevation, in meters' )
    iplot += 1
    if iplot > nplots or idx == num_sites-1:
        ax.set_xlabel( 'Year' )
        fout = os.path.join( OutputDir, 'UMD_HeadObs_{0:03d}.png'.format(ifigure) )
        fig.savefig(fout,dpi=300)
        print 'created...', fout
        #--clear memory
        headObj = None
        mpl.pyplot.close('all')
        gc.collect()
        #--reinitialize the head file object
        headObj = mfb.MODFLOW_Head(nlay,nrow,ncol,head_file)
        #--reinitialize the figure
        fig = Make_NewFigure()
        #mpl.pyplot.clf()
        #--update figure and plot counters
        ifigure += 1
        iplot = 1
    #--write data to files
    #--mod2obs file
    f.write( '{0:10s} {1:15.7g} {2:15.7g} {3:10d} {4:10d} {5:10d}\n'.format(SITE_NAME,x,y,ilay+1,irow+1,icol+1) )
    #--summary file
    k = ilay
    if k < 0:
        k = nlay - 1
    fs.write( '{0:3d} {1:3d} {2:10s} {3:15.7g} {4:15.7g} {5:10d} {6:10d} {7:10d} {8:15.7g} {9:15.7g} {10:15.7g} {11:15.7g} {12:15.7g} {13: 10.3f} {14: 10.3f} {15: 10.3f} {16:10d}\n'.format(idx,iwell,SITE_NAME,x,y,ilay+1,irow+1,icol+1, bot[0,irow,icol], screen_top, screen_bot, bot[k,irow,icol], bot[k+1,irow,icol], me, mae, rmse, npairs ) )

    

#--close the MOD2OBS location file
f.close()

fs.close()