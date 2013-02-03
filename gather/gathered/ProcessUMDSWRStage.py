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

#--read base xml data
xml_file = os.path.join( '..', 'xml', 'SWStage.xml' )
tree = xml.parse(xml_file)
root = tree.getroot()
SWRStageFile = root.find('SWRStageFile').text
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
#--determine the number of stage sites
num_sites = 0
for swstage in root.findall('swstage'):
    num_sites += 1

#--get command line arguments
SWRBaseName = os.path.basename( SWRStageFile )
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
                #--replace path in SWRStageFile with the value passed from the command line
                SWRStageFile = os.path.join( ResultsDir, SWRBaseName )
                print 'command line arg: -resultsdir = ', ResultsDir
            except:
                print 'cannot parse command line arg: -resultsdir'


print 'processing stage data from...{0}\nFor the period from {1} to {2}'.format( SWRStageFile, start_date, end_date )
print '  for {0} stage stations'.format( num_sites )

#--open swr stage file
SWRObj = mfb.SWR_Record(0,SWRStageFile)
itime  = SWRObj.get_item_number('totim')
istage = SWRObj.get_item_number('stage')

#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'StageObs' )
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
#--summary data
active_stageobs = []
active_stageobs_stats = []
#--process each station in the xml file
for idx,swstage in enumerate( root.findall('swstage') ):
    station = swstage.attrib['name']
    reach = int( swstage.find('reach').text )
    nobs = 0
    processObs = False
    child = swstage.find('ObsFile')
    if child != None:
        processObs = True
        ObsFile = child.text
        #--test if smp file exists
        smpExists = os.path.exists(ObsFile)
        if smpExists == True:
            SITE_NAME = os.path.basename(ObsFile).replace('.smp','')
            print 'Reading observed data for {0}'.format( SITE_NAME )
            #--get the smp file data
            smp = pestUtil.smp(ObsFile,load=False,date_fmt='%m/%d/%Y')
            records = smp.load(site=SITE_NAME)
            for record in records:
                a = np.copy( records[record] )
                nobs = a.shape[0]
            for t in a:
                t[1] *= unit_conv
        else:
            print 'Specified smp file [{0}] does not exist'.format( os.path.basename(ObsFile) )
    else:
        print 'No observation data for {0}'.format( station )
    print 'Processing stage data for...{0} - reach {1}'.format( station, reach )
    #--read the simulated data
    #SWRObj.rewind_file()
    #ce1 = SWRObj.get_gage(reach)
    ce1 = SWRObj.get_time_gage(reach)
    nt =  np.shape(ce1)[0]
    sim = np.zeros( (nt,2), np.float )
    for jdx in xrange(0,nt):
        sim[jdx,0] = ce1[jdx,itime]
        sim[jdx,1] = ce1[jdx,istage] * unit_conv
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
    active_stageobs.append( [station,reach] )
    active_stageobs_stats.append( [nobs,npairs,me,mae,rmse] )
    #--legends and axes
    leg = ax.legend(loc='best',ncol=1,labelspacing=0.25,columnspacing=1,\
                    handletextpad=0.5,handlelength=2.0,numpoints=1)
    leg._drawFrame=False
    ctxt = '{0} -- Reach {1:4d}'.format( station, reach ) 
    ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.set_xlim(start_date, end_date)
    ax.set_ylabel( 'Elevation, in {0}'.format( cunits ) )
    iplot += 1
    if iplot > nplots or idx == num_sites-1:
        ax.set_xlabel( 'Year' )
        fout = os.path.join( OutputDir, 'UMD_StageObs_{0:03d}.png'.format(ifigure) )
        fig.savefig(fout,dpi=300)
        print 'created...', fout
        #--clear memory
        #SWRObj = None
        mpl.pyplot.close('all')
        gc.collect()
        #--reinitialize the figure
        fig = Make_NewFigure()
        #mpl.pyplot.clf()
        #--update figure and plot counters
        ifigure += 1
        iplot = 1

stats_file = os.path.join( ResultsDir, 'UMD_StageStats.csv' )
f = open(stats_file, 'w')
f.write('"Station","Reach","SMP_TAG","Number of observations","Number of pairs","Mean error, in {0}","Mean absolute error in {1}","Root mean squared error in {2}"\n'.format(cunits,cunits,cunits) )
for idx,[t1,t2] in enumerate(zip(active_stageobs,active_stageobs_stats)):
    #--determine if any observation data is available
    if int( t2[0] ) < 1:
        continue
    smp_tag = t1[0].replace('-','')
    smp_tag = smp_tag.replace('HW','H')
    smp_tag = smp_tag.replace('TW','T')
    smp_tag = smp_tag.replace(' ','_')
    #--write data
    f.write( '{0},{1},{2},{3},{4},'.format( t1[0],t1[1],smp_tag,t2[0],t2[1] ) )
    if int( t2[1] ) > 0:
        f.write( '{0},{1},{2}'.format( t2[2],t2[3],t2[4] ) )
    else:
        f.write( '--,--,--' )
    f.write( '\n' )
f.close()


