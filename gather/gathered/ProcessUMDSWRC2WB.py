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

Missing = 99999999.

def SWRBudgetError(text,error):
    cerror = {  0: '', \
                1: 'not defined', \
               10: 'no SWR data specified for extraction', \
               11: 'no pools specified' }              
    print 'Error: {0} {1}.'.format( text, cerror[error] )
    sys.exit(error)

def Make_NewFigure():
    fwid, fhgt = 7.00, 1.50
    flft, frgt = 0.075, 0.925
    fbot, ftop = 0.10, 0.925
    fig = pl.figure( figsize=(fwid, fhgt), facecolor='w' )
    fig.subplots_adjust(wspace=0.25,hspace=0.25,left=flft,right=frgt,bottom=fbot,top=ftop)
    return fig

def sampleDates( sim_dates, TimeSample ):
    output_dates = []
    if TimeSample.lower() == 'weekly':
        on_day = 0
        for idx,t in enumerate( sim_dates ):
            on_day += 1
            if on_day > 7:
                output_dates.append( sim_dates[idx-1] )
                on_day = 0
    if TimeSample.lower() == 'monthly':
        on_month = sim_dates[0].month
        for idx,t in enumerate( sim_dates ):
            if t.month != on_month:
                output_dates.append( sim_dates[idx-1] )
                on_month = t.month
    elif TimeSample.lower() == 'yearly':
        on_year = sim_dates[0].year
        for idx,t in enumerate( sim_dates ):
            if t.year != on_year:
                output_dates.append( sim_dates[idx-1] )
                on_year = t.year
    output_dates.append( sim_dates[-1] )
    return np.array( output_dates )

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

def accumulateData( output_dates, sim_dates, sim_data, fracTarget ):
    noutdates = output_dates.shape[0]
    output_data = np.empty( (noutdates), np.float )
    output_data.fill( Missing )
    jdx    = 0
    icount = 0.0
    iv     = 0.0
    vsum   = 0.0
    for idx,[d,v] in enumerate( zip( sim_dates, sim_data ) ):
        if d > output_dates[jdx]:
            frac = iv / icount
            if frac > fracTarget:
                output_data[jdx] = vsum / (iv * 60. * 60. * 24. )
            jdx   += 1
            icount = 0.0
            iv     = 0.0
            vsum   = 0.0
        icount += 1.0
        if v != Missing:
            iv   += 1.0
            vsum += v
    #--save final sum
    frac = iv / icount
    if frac > fracTarget:
        output_data[jdx] = vsum / (iv * 60. * 60. * 24. )
    #--return    
    return output_data

def processObservations( output_inflow, output_outflow ):
    output_obs = np.empty( (output_inflow.shape[0]), np.float )
    output_obs.fill( Missing )
    nobs = 0
    for idx,[inf,outf] in enumerate( zip( output_inflow, output_outflow ) ):
        if inf != Missing and outf != Missing:
            nobs += 1
            output_obs[idx] = outf - inf
    return nobs, output_obs

def saveData(f, ctag, tdates, tdata):
    for [d,v] in zip( tdates, tdata ):
        if v == Missing:
            continue
        cdate = datetime.strftime( d, '%m/%d/%Y %H:%M:%S' )
        f.write('{0} {1} {2}\n'.format( ctag, cdate, v ))

def MaskOutputTime(tdata):
    outdata = np.copy( tdata )
    #--mask data
    return np.ma.masked_equal( outdata, Missing )

def DailyStatistics(obs,sim):
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

PlotData = False
SaveObsData = False
SaveSimData = False
TimeSample = None

#--file names

#--command line arguments
ReplaceResultsDir = False
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
                ReplaceResultsDir = True
            except:
                print 'cannot parse command line arg: -resultsdir'
        elif basearg == '-timesample':
            try:
                iarg += 1
                TimeSample = sys.argv[iarg]
                print 'command line arg: TimeSample = ', TimeSample
            except:
                print 'cannot parse command line arg: TimeSample'

#--read base xml data
xml_file = os.path.join( '..', 'xml', 'SWC2Budget.xml' )
tree = xml.parse(xml_file)
root = tree.getroot()
ctag = 'SWRPoolFile'
child = root.find(ctag)
if child == None: SWRBudgetError(ctag,1)
SWRPoolFile = child.text
ctag = 'SWRFlowFile'
child = root.find(ctag)
if child == None: SWRBudgetError(ctag,1)
SWRFlowFile = child.text
if ReplaceResultsDir == True:
    SWRBaseName = os.path.basename( SWRFlowFile )
    SWRFlowFile = os.path.join( ResultsDir, SWRBaseName )
    print 'SWR flow file with user defined path...{0}'.format( SWRFlowFile )
ctag = 'StartDate'
child = root.find(ctag)
if child == None: SWRBudgetError(ctag,1)
start_date = datetime.strptime(child.text,'%m/%d/%Y')
ctag = 'EndDate'
child = root.find(ctag)
if child == None: SWRBudgetError(ctag,1)
end_date = datetime.strptime(child.text,'%m/%d/%Y')
if TimeSample == None:
    ctag = 'TimeSample'
    child = root.find(ctag)
    if child == None:
        TimeSample = 'Daily'
    else:
        TimeSample = child.text
ctag = 'FractionThreshold'
child = root.find(ctag)
if child == None:
    FractionThreshold = 0.0
else:
    FractionThreshold = float(child.text)
#--output formats
child = root.find('PlotData')
if child != None:
    PlotData = bool( child.text )
if PlotData == True:
    print 'Data will be plotted'
child = root.find('ObservedSMPResults')
if child != None:
    SaveObsData = True
    ftxt = '{0}_{1}.smp'.format( child.text, TimeSample )
    fobsout = open(ftxt,'w')
    print 'Processed observation data will be saved to...{0}'.format( ftxt )
child = root.find('SimulatedSMPResults')
if child != None:
    SaveSimData = True
    ftxt = '{0}_{1}.smp'.format( child.text, TimeSample )
    fsimout = open(ftxt,'w')
    print 'Processed simulated data will be saved to...{0}'.format( ftxt )
#--determine the SWR data to extract
swrdata = []
ctag = 'SWRModelItems'
swrmodelitems = root.find(ctag)
if swrmodelitems != None:
    for modelitem in swrmodelitems.findall('modelitem'):
        swrdata.append( modelitem.text )
if len(swrdata) == 0: SWRBudgetError(ctag,10)
#--build index of data to extract from the flow file
SWRObj = mfb.SWR_Record(-1,SWRFlowFile)
swrdata_index = []
for sd in swrdata:
    idx  = SWRObj.get_item_number(sd)
    swrdata_index.append( idx )
#--determine the number of pool budget observations
num_pools_obs = 0
ctag = 'swbudget'
for swbudget in root.findall(ctag):
    num_pools_obs += 1
if num_pools_obs == 0: SWRBudgetError(ctag,11)
#--write summary information
print 'SWR pool definition file...{0}'.format( SWRPoolFile )
print 'processing stage data from...{0}\nFor the period from {1} to {2}'.format( SWRFlowFile, start_date, end_date )
print '  for {0} pool(s)'.format( num_pools_obs )
#--open pool data xml
pool_tree = xml.parse(SWRPoolFile)
pool_root = pool_tree.getroot()
num_unique_pools = 0
#--determine the number of unique pools in SWR
for pool in pool_root.findall('pool'):
    num_unique_pools += 1
if num_unique_pools == 0: SWRBudgetError('No "pool" entries in {0}'.format(SWRPoolFile),0)
print 'Number of unique SWR pool(s) {0}'.format( num_unique_pools )
#--make sure output directories exist
OutputDir = os.path.join( ResultsDir, 'Figures', 'BudgetObs' )
umdutils.TestDirExist([os.path.join( ResultsDir,'Figures','dir.tst' ),os.path.join( OutputDir, 'dir.tst' )])
#--simulation dates
on_date = start_date
sim_dates = []
sim_dates.append( on_date )
while on_date < end_date:
    on_date += timedelta(days=1.)
    sim_dates.append( on_date )
sim_dates = np.array( sim_dates )

#--output dates
if TimeSample == 'Daily':
    output_dates = np.copy( sim_dates )
else:
    output_dates = sampleDates( sim_dates, TimeSample )
#--arrays for data
inflow  = np.empty( (len(sim_dates)), np.float )
outflow = np.empty( (len(sim_dates)), np.float )
sim     = np.empty( (len(sim_dates)), np.float )
sim_rg  = np.empty( (len(sim_dates)), np.float )

#--initialize figure and figure/plot counters
ifigure = 1
iplot = 1
nplots = 1
if PlotData == True: fig = Make_NewFigure()
#--matplotlib date specification
years, months = mdates.YearLocator(), mdates.MonthLocator()  #every year, every month
yearsFmt = mdates.DateFormatter('%Y')

#--process each station in the xml file
for idx,swbudget in enumerate( root.findall('swbudget') ):
    #--initialize data
    inflow.fill( Missing )
    outflow.fill( Missing )
    sim.fill( Missing )
    pools       = []
    pools_dict  = {}
    #--get smp inflow files from xml file
    processInflow = False
    child = swbudget.find('inflow_items')
    if child != None:
        processInflow = True
        for childitem in child.findall('smpitem'):
            print 'processing inflow...{0}'.format(childitem.text) 
            #--get the smp file data
            smpstation = os.path.basename(childitem.text).replace('.smp','')
            smp = pestUtil.smp(childitem.text,load=True,date_fmt='%m/%d/%Y')
            inflow = dataAdd(sim_dates,inflow,smp.records[smpstation][:,0],smp.records[smpstation][:,1])
    #--get smp outflow files from xml file
    child = swbudget.find('outflow_items')
    if child != None:
        for childitem in child.findall('smpitem'):
            print 'processing outflow...{0}'.format(childitem.text) 
            #--get the smp file data
            smpstation = os.path.basename(childitem.text).replace('.smp','')
            smp = pestUtil.smp(childitem.text,load=True,date_fmt='%m/%d/%Y')
            outflow = dataAdd(sim_dates,outflow,smp.records[smpstation][:,0],smp.records[smpstation][:,1])
    #--get station data from xml file
    station = swbudget.attrib['name']
    child = swbudget.find('pool_items')
    #--determine the SWR pool number for this pool
    for childitem in child.findall('poolitem'):
        pools.append( childitem.text )
        #--build pool dictionary
        pool_name = childitem.text
        for pool_childitem in pool_root.findall('pool'):
            if pool_childitem.attrib['name'] == pool_name:
                rg_child = pool_childitem.find('reachGroups')
                for rg in rg_child.findall('reachGroupItem'):
                    rg_number = int( rg.find('reachGroup').text )
                    print 'Station {0}...processing "{1}" pool - SWR reach group number {2}'.format(station, pool_childitem.attrib['name'], rg_number )
                    sim_rg.fill( Missing )
                    #read simulated data
                    SWRObj = mfb.SWR_Record(-1,SWRFlowFile)
                    ce1 = SWRObj.get_gage(rg_number)
                    #process each item
                    for jdx in swrdata_index:
                        sim_rg = dataAdd(sim_dates,sim_rg,sim_dates[0:ce1.shape[0]],ce1[:,jdx])
                    sim = dataAdd(sim_dates,sim,sim_dates[0:sim_rg.shape[0]],sim_rg)
    if processInflow == False:
        inflow.fill( 0.0 )
    #--average the inflow, outflow, and simulated data appropriately
    output_inflow = accumulateData( output_dates, sim_dates, inflow, FractionThreshold )
    output_outflow = accumulateData( output_dates, sim_dates, outflow, FractionThreshold )
    output_sim = accumulateData( output_dates, sim_dates, sim, FractionThreshold )
    #--calculate observed data
    nobs, output_obs = processObservations( output_inflow, output_outflow )
#    for [t,d] in zip( output_dates, output_sim ):
#        print t, d
    #--save the data
    if SaveObsData == True:
        ctag = '{0}o'.format( station )
        saveData(fobsout, ctag, output_dates, output_obs)
    if SaveSimData == True:
        ctag = '{0}s'.format( station )
        saveData(fsimout, ctag, output_dates, output_sim)
    #--plot the data
    if PlotData == True:
        ax = fig.add_subplot(nplots,1,iplot)
        #--plot the observed data
        if nobs > 0:
            tobs = MaskOutputTime(output_obs)
            ax.plot(pl.date2num(output_dates),tobs, color='b', linewidth=1.5, label='Observed')
        #--plot the simulated data
        tsim = MaskOutputTime(output_sim)
        ax.plot(pl.date2num(output_dates),tsim, color='r', linewidth=0.75, label='Simulated')
        #--calculate statistics
        cstats = ''
        me = 0.0
        mae = 0.0
        rmse = 0.0
        npairs = 0.0
        if nobs > 0:
            me, mae, rmse, npairs = DailyStatistics(tobs,tsim)
            if npairs > 0:
                cstats = 'ME {0: 5.3f} MAE {1: 5.3f} RMSE {2: 5.3f} Pairs {3}'.format( me, mae, rmse, npairs )
            else:
                cstats = 'Pairs {0}'.format( npairs )
        #--legends and axes
        leg = ax.legend(loc='best',ncol=1,labelspacing=0.25,columnspacing=1,\
                        handletextpad=0.5,handlelength=2.0,numpoints=1)
        leg._drawFrame=False
        ctxt = '{0} surface-water group'.format( station ) 
        ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
        ax.text(1.0,1.01,cstats,horizontalalignment='right',verticalalignment='bottom',size=7,transform=ax.transAxes)
        ax.xaxis.set_major_locator(years), ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.set_xlim(start_date, end_date)
        ax.set_ylabel( r'Net discharge, in m$^3$/s' )
        iplot += 1
        if iplot > nplots or idx == num_pools_obs-1:
            ax.set_xlabel( 'Year' )
            fout = os.path.join( OutputDir, 'UMD_{0}_C2BudgetObs_{1:03d}.png'.format(TimeSample,ifigure) )
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



if SaveObsData == True:
    fobsout.close()
if SaveSimData == True:
    fsimout.close()
