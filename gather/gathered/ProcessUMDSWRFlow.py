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

def dataAdd(outtime,data0,intime,indata):
    nouttime = outtime.shape[0]
    outdata = np.copy( data0 )
    for [d,v] in zip( intime, indata ):
        ipos = (d-outtime[0]).days
        if ipos < 0:
            continue
        elif ipos > nouttime - 1:
            break
        if data0[ipos] == Missing:
            outdata[ipos] = v
        else:
            outdata[ipos] += v
    return outdata

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
flow_mult = 1.0 / ( 60. * 60. * 60. )

#--read base xml data
xml_file = os.path.join( '..', 'xml', 'SWFlow.xml' )
tree = xml.parse(xml_file)
root = tree.getroot()
SWRFlowFile = root.find('SWRFlowFile').text
SWRRGFlowFile = ''
ReadRGFlowFile = False
c = root.find('SWRRGFlowFile').text
if c != None:
    SWRRGFlowFile = c
    ReadRGFlowFile = True

start_date = datetime.strptime(root.find('StartDate').text,'%m/%d/%Y')
end_date = datetime.strptime(root.find('EndDate').text,'%m/%d/%Y')
#--determine the number of stage sites
num_sites = 0
for swflow in root.findall('swflow'):
    num_sites += 1

#--get command line arguments
SWRBaseName = os.path.basename( SWRFlowFile )
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
                #--replace path in SWRFlowFile with the value passed from the command line
                SWRFlowFile = os.path.join( ResultsDir, SWRBaseName )
                print 'command line arg: -resultsdir = ', ResultsDir
            except:
                print 'cannot parse command line arg: -resultsdir'


print 'processing stage data from...{0}\nFor the period from {1} to {2}'.format( SWRFlowFile, start_date, end_date )
print '  for {0} discharge stations'.format( num_sites )

#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'FlowObs' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--simulation dates
on_date = start_date
sim_dates = []
sim_dates.append( on_date )
while on_date < end_date:
    on_date += timedelta(days=1.)
    sim_dates.append( on_date )
sim_dates = np.array( sim_dates )
obs = np.empty( (sim_dates.shape[0]), np.float )

#--initialize figure and figure/plot counters
ifigure = 1
iplot = 1
nplots = 6
fig = Make_NewFigure()
#--matplotlib date specification
years, months = mdates.YearLocator(), mdates.MonthLocator()  #every year, every month
yearsFmt = mdates.DateFormatter('%Y')

#--process each station in the xml file
for idx,swflow in enumerate( root.findall('swflow') ):
    station = swflow.attrib['name']
    print 'Station: {0}'.format( station )
    usreach = int( swflow.find('usreach').text )
    dsreach = int( swflow.find('dsreach').text )
    sim_mult = 1.0
    c = swflow.find('simmult')
    if c != None:
        sim_mult = float( c.text )
    print 'Processing flow data for...{0} - reach {1}->{2}'.format( station, usreach, dsreach )
    obs.fill( Missing )
    processObs = False
    child = swflow.find('ObsItems')
    if child != None:
        processObs = True
        for childitem in child.findall('ObsFile'):
            print 'processing observation data...{0}'.format(childitem.text) 
            #--get the smp file data
            smpstation = os.path.basename(childitem.text).replace('.smp','')
            smp = pestUtil.smp(childitem.text,load=True,date_fmt='%m/%d/%Y')
            obs = dataAdd(sim_dates,obs,smp.records[smpstation][:,0],smp.records[smpstation][:,1])
    obs *= flow_mult
    #--read the simulated data
    if dsreach > 0:
        SWRObj = mfb.SWR_Record(-2,SWRFlowFile)
        itime  = SWRObj.get_item_number('totim')
        iflow = SWRObj.get_item_number('flow')
        ce1 = SWRObj.get_gage(rec_num=usreach,iconn=dsreach)
        nt =  np.shape(ce1)[0]
        sim = np.zeros( (nt,2), np.float )
        for jdx in xrange(0,nt):
            sim[jdx,0] = ce1[jdx,itime]
            sim[jdx,1] = ce1[jdx,iflow] * flow_mult * -1. * sim_mult
    #--plot the data
    ax = fig.add_subplot(nplots,1,iplot)
    #--plot the observed data
    if processObs == True:
        ax.plot(pl.date2num(sim_dates),obs, color='b', linewidth=1.5, label='Observed')
    #--plot the simulated data
    sim = DailyMaskTime(sim_dates,sim_dates[0:sim.shape[0]],sim[:,1])
    ax.plot(pl.date2num(sim_dates),sim, color='r', linewidth=0.75, label='Simulated')
    #--calculate statistics
    cstats = ''
    me = 0.0
    mae = 0.0
    rmse = 0.0
    npairs = 0.0
    if processObs == True:
        me, mae, rmse, npairs = DailyStatistics(obs,sim)
        if npairs > 0:
            cstats = 'ME {0: 5.3f} MAE {1: 5.3f} RMSE {2: 5.3f} Pairs {3}'.format( me, mae, rmse, npairs )
        else:
            cstats = 'Pairs {0}'.format( npairs )
    #--legends and axes
    leg = ax.legend(loc='best',ncol=1,labelspacing=0.25,columnspacing=1,\
                    handletextpad=0.5,handlelength=2.0,numpoints=1)
    leg._drawFrame=False
    ctxt = '{0} -- Reach {1:4d}->{2:4d}'.format( station, usreach, dsreach ) 
    ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.set_xlim(start_date, end_date)
    ax.set_ylabel( r'Discharge, in m$^3$/s' )
    iplot += 1
    if iplot > nplots or idx == num_sites-1:
        ax.set_xlabel( 'Year' )
        fout = os.path.join( OutputDir, 'UMD_FlowObs_{0:03d}.png'.format(ifigure) )
        fig.savefig(fout,dpi=300)
        print 'created...', fout
        #--clear memory
        SWRObj = None
        mpl.pyplot.close('all')
        gc.collect()
        #--reinitialize the figure
        fig = Make_NewFigure()
        #mpl.pyplot.clf()
        #--update figure and plot counters
        ifigure += 1
        iplot = 1



