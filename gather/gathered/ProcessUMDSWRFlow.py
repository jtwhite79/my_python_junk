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

no_data = 9999.

def Make_NewFigure():
    fwid, fhgt = 7.00, 9.00
    flft, frgt = 0.075, 0.925
    fbot, ftop = 0.10, 0.95
    fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
    fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
    return fig

def dataAdd(unit_conv,outtime,data0,intime,indata):
    nobs = 0
    nouttime = outtime.shape[0]
    outdata = np.copy( data0 )
    for [d,v] in zip( intime, indata ):
        ipos = (d-outtime[0]).days
        if ipos < 0:
            continue
        elif ipos > nouttime - 1:
            break
        nobs += 1
        if data0[ipos] == no_data:
            outdata[ipos] = v * unit_conv
        else:
            outdata[ipos] += v * unit_conv
    return nobs, outdata

def DailyMaskTime(outtime,intime,indata):
    nouttime = outtime.shape[0]
    outdata = np.empty( (nouttime), np.float )
    outdata.fill( no_data )
    for [d,v] in zip( intime, indata ):
        ipos = (d-outtime[0]).days
        if ipos < 0:
            continue
        elif ipos > nouttime - 1:
            break
        outdata[ipos] = v
    #--mask data
    return np.ma.masked_equal( outdata, no_data )

def DailyStatistics(obs,sim):
    me = 0.0
    mae = 0.0
    rmse = 0.0
    npairs = 0
    for [o,s] in zip(obs,sim):
        if o != no_data and s != no_data:
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
child = root.find('InputUnits')
if child != None:
    cunits = child.text
else:
    cunits = 'm$^3$/s'
child = root.find('OutputUnits')
if child != None:
    cunits = child.text
unit_conv = 1.0
child = root.find('OutputConversion')
if child != None:
    unit_conv = float(child.text)
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

#--open swr connection flow file
SWRObj = mfb.SWR_Record(-2,SWRFlowFile)
itime  = SWRObj.get_item_number('totim')
iflow = SWRObj.get_item_number('flow')

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
    obs.fill( no_data )
    processObs = False
    nobs = 0
    child = swflow.find('ObsItems')
    if child != None:
        processObs = True
        for childitem in child.findall('ObsFile'):
            print 'processing observation data...{0}'.format(childitem.text) 
            #--get the smp file data
            smpstation = os.path.basename(childitem.text).replace('.smp','')
            smp = pestUtil.smp(childitem.text,load=True,date_fmt='%m/%d/%Y')
            nobs, obs = dataAdd(unit_conv,sim_dates,obs,smp.records[smpstation][:,0],smp.records[smpstation][:,1])
#    obs *= unit_conv
    #--read the simulated data
    if dsreach > 0:
        #SWRObj = mfb.SWR_Record(-2,SWRFlowFile)
        #SWRObj.rewind_file()
        #ce1 = SWRObj.get_gage(rec_num=usreach,iconn=dsreach)
        ce1 = SWRObj.get_time_gage(rec_num=usreach,iconn=dsreach)
        nt =  np.shape(ce1)[0]
        sim = np.zeros( (nt,2), np.float )
        for jdx in xrange(0,nt):
            sim[jdx,0] = ce1[jdx,itime]
            sim[jdx,1] = ce1[jdx,iflow] * unit_conv * -1. * sim_mult
    #--plot the data
    ax = fig.add_subplot(nplots,1,iplot)
    #--plot the observed data
    if processObs == True:
        temp = DailyMaskTime(sim_dates,sim_dates[0:obs.shape[0]],obs)
        ax.plot(pl.date2num(sim_dates),temp, color='b', linewidth=1.5, label='Observed')
    #--plot the simulated data
    sim = DailyMaskTime(sim_dates,sim_dates[0:sim.shape[0]],sim[:,1])
    ax.plot(pl.date2num(sim_dates),sim, color='r', linewidth=0.75, label='Simulated')
    #--calculate statistics
    cstats = ''
    me = 0.0
    mae = 0.0
    rmse = 0.0
    npairs = 0.0
#    if processObs == True:
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
    ctxt = '{0} -- Reach {1:4d}->{2:4d}'.format( station, usreach, dsreach ) 
    ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
    ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.set_xlim(start_date, end_date)
    ax.set_ylabel( r'Discharge, in {0}'.format( cunits ) )
    iplot += 1
    if iplot > nplots or idx == num_sites-1:
        ax.set_xlabel( 'Year' )
        fout = os.path.join( OutputDir, 'UMD_FlowObs_{0:03d}.png'.format(ifigure) )
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



