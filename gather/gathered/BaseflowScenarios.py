import sys
import os
import gc
import math
import datetime as dt
import pylab
import numpy as np
import MFArrayUtil as au
import MFBinaryClass as mfb 
import pestUtil as pu


#-Figure defaults
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
mpl.rcParams['font.sans-serif']          = 'Univers 57 Condensed'
mpl.rcParams['font.serif']               = 'Times'
mpl.rcParams['font.cursive']             = 'Zapf Chancery'
mpl.rcParams['font.fantasy']             = 'Comic Sans MS'
mpl.rcParams['font.monospace']           = 'Courier New'
mpl.rcParams['pdf.compression']          = 0
mpl.rcParams['pdf.fonttype']             = 42
ticksize = 9
mpl.rcParams['font.size']        = 9
mpl.rcParams['legend.fontsize']  = 7
mpl.rcParams['axes.labelsize']   = 9
mpl.rcParams['axes.titlesize']   = 9
mpl.rcParams['xtick.labelsize']  = ticksize
mpl.rcParams['ytick.labelsize']  = ticksize
mpl.rcParams['contour.negative_linestyle'] = 'solid'

#--main script
dry_month_start = 11
dry_month_end = 6
#--dimensions
nlay,nrow,ncol = 3,189,101
start_date = dt.datetime(year=1996,month=1,day=1,hour=12)
end_date = dt.datetime(year=2010,month=12,day=31,hour=12)
#end_date = dt.datetime(year=1998,month=1,day=31,hour=12)
num_days = end_date - start_date

extract_well = ['SC', 'SW', 'ORR']
#extract_well = ['SC']

#--read pumpage data from smp files
smp_ref = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','Data','WEL', 'pumpwell2_extendedto2010.smp')
smp = pu.smp(smp_ref,load=True,date_fmt='%m/%d/%Y')
site_names = smp.get_unique_from_file(smp.site_index)

WellQ = 0.0
WellQDry = 0.0
IsDry = True
DryDays = 0
for iday in xrange(0,num_days.days+1):
    ondate = start_date + dt.timedelta(days=iday)
    if IsDry == True:
        if ondate.month == dry_month_end:
            IsDry = False
    elif IsDry == False:
        if ondate.month == dry_month_start:
            IsDry = True
    if IsDry == True:
        DryDays += 1
    [names,values] = smp.active(ondate)
    itmp = len( names )
    print ' Date: ', ondate
    #--calculate average rate for the three well fields 
    for iw in range(0,itmp):
        for ce in extract_well:
            if ce in names[iw].upper():
                WellQ -= values[iw] / ( float( num_days.days+1 ) * 60. * 60. * 24. )
                if IsDry == True:
                    WellQDry -= values[iw] / ( 60. * 60. * 24. )

WellQDry /= float( DryDays )

model_dir = os.path.join( 'D:/','Data','Users','jdhughes','Projects','2080DBF00','UMD','UMD.01' )
#flow_data = [ os.path.join( 'Results_DSL0304_PCT125', 'UMD.fls' ), \
#              os.path.join( 'Results_DSL0304_PCT110', 'UMD.fls' ), \
#              os.path.join( 'Results_DSL0304_PCT105', 'UMD.fls' ), \
#              os.path.join( 'Results_DSL0304', 'UMD.fls' ), \
#              os.path.join( 'Results_PCT125', 'UMD.fls' ), \
#              os.path.join( 'Results_stat', 'UMD.fls' ) ]
#yNames = [ '+0.304 m sea-level\n+25% PWS', \
#           '+0.304 m sea-level\n+10% PWS', \
#           '+0.304 m sea-level\n+ 5% PWS', \
#           '+0.304 m sea-level', \
#           '+25% PWS', \
#           'Base case' ]
flow_data = [ os.path.join( 'Results_DSL0304_PCT125', 'UMD.fls' ), \
              os.path.join( 'Results_DSL0304', 'UMD.fls' ), \
              os.path.join( 'Results_PCT125', 'UMD.fls' ), \
              os.path.join( 'Results_stat', 'UMD.fls' ) ]
yNames = [ '+0.304 m sea-level\n+25% PWS', \
           '+0.304 m sea-level', \
           '+25% PWS', \
           'Base case' ]
PBaseflow = np.zeros( (len(flow_data)), np.float )
NBaseflow = np.zeros( (len(flow_data)), np.float )
PBaseflowDry = np.zeros( (len(flow_data)), np.float )
NBaseflowDry = np.zeros( (len(flow_data)), np.float )
pool_number = 36
for idx,f in enumerate( flow_data ):
    print 'reading data from...{0}'.format( f )
    fn = os.path.join( model_dir, f )
    SWRObj = mfb.SWR_Record(-1,fn)
    index_time = SWRObj.get_item_number('totim')
    index_bf = SWRObj.get_item_number('qbflow')
    ce1 = SWRObj.get_gage(pool_number)
    IsDry = True
    DryDays = 0
    for jdx in xrange(0,ce1.shape[0]):
        on_time = ce1[jdx,index_time]
        ondate = start_date + dt.timedelta(days=int(on_time))
        if on_time > float( num_days.days ):
            break
        if IsDry == True:
            if ondate.month == dry_month_end:
                IsDry = False
        elif IsDry == False:
            if ondate.month == dry_month_start:
                IsDry = True
        if IsDry == True:
            DryDays += 1
        if ce1[jdx,index_bf] > 0.0:
            NBaseflow[idx] += ce1[jdx,index_bf] / ( float( num_days.days+1 ) * 60. * 60. * 24. )
            if IsDry == True:
                NBaseflowDry[idx] += ce1[jdx,index_bf] / ( 60. * 60. * 24. )
        else:
            PBaseflow[idx] -= ce1[jdx,index_bf] / ( float( num_days.days+1 ) * 60. * 60. * 24. )
            if IsDry == True:
                PBaseflowDry[idx] -= ce1[jdx,index_bf] / ( 60. * 60. * 24. )
    NBaseflowDry[idx] /= float( DryDays )
    PBaseflowDry[idx] /= float( DryDays )

pos = np.arange(2)
pQ = [WellQ*1.25, WellQ]
ip1 = len( flow_data ) - 2
ip2 = len( flow_data )
pP = np.copy( PBaseflow[ip1:ip2] )
pN = np.copy( NBaseflow[ip1:ip2] )  
pyNames = yNames[ip1:ip2]
pQDry = [WellQDry*1.25, WellQDry]
pPDry = np.copy( PBaseflowDry[ip1:ip2] )
pNDry = np.copy( NBaseflowDry[ip1:ip2] )  
    
output_name = os.path.join( '..', 'figures', 'SnapperCreekComparison_PWS.png' )
print 'creating figure...{0}'.format( output_name )
ztf = mpl.pyplot.figure(figsize=(4.4, 3.0), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.25,right=0.95,bottom=0.05,top=0.95)
ax = ztf.add_subplot(1,1,1)
ctxt = 'Snapper Creek (C-2)' 
ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=8,transform=ax.transAxes)
p1 = ax.barh(pos-0.35,pQ,height=0.20,color='k')
p2 = ax.barh(pos-0.10,pP,height=0.20,color='blue')
p3 = ax.barh(pos+0.15,pN,height=0.20,color='red')
for idx,p in enumerate( pos ):
    ax.text( pQ[idx]+.05,p-.25,'{0:4.2f}'.format( pQ[idx] ), size=8, verticalalignment='center' )
    ax.text( pP[idx]+.05,p,'{0:4.2f}'.format( pP[idx] ), size=8, verticalalignment='center' )
    ax.text( pN[idx]+.05,p+0.25,'{0:4.2f}'.format( pN[idx] ), size=8, verticalalignment='center' )
leg = ax.legend( (p1[0], p2[0], p3[0]), ('PWS withdrawals', 'Reach to aquifer seepage', 'Aquifer to reach seepage'), loc='best' )
leg._drawFrame=False
pylab.yticks(pos, pyNames)
ax.set_xlabel( r'Flow, in m$^{3}$/s' )
ax.set_ylim(-0.5, 1.5)
#--save the figure
ztf.savefig(output_name,dpi=300)
#--clear memory
mpl.pyplot.close('all')
gc.collect()

output_name = os.path.join( '..', 'figures', 'SnapperCreekComparison_Dry_PWS.png' )
print 'creating figure...{0}'.format( output_name )
ztf = mpl.pyplot.figure(figsize=(4.4, 3.0), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.25,right=0.95,bottom=0.05,top=0.95)
ax = ztf.add_subplot(1,1,1)
ctxt = 'Snapper Creek (C-2) - Dry Season' 
ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=8,transform=ax.transAxes)
p1 = ax.barh(pos-0.35,pQDry,height=0.20,color='k')
p2 = ax.barh(pos-0.10,pPDry,height=0.20,color='blue')
p3 = ax.barh(pos+0.15,pNDry,height=0.20,color='red')
for idx,p in enumerate( pos ):
    ax.text( pQDry[idx]+.05,p-.25,'{0:4.2f}'.format( pQDry[idx] ), size=8, verticalalignment='center' )
    ax.text( pPDry[idx]+.05,p,'{0:4.2f}'.format( pPDry[idx] ), size=8, verticalalignment='center' )
    ax.text( pNDry[idx]+.05,p+0.25,'{0:4.2f}'.format( pNDry[idx] ), size=8, verticalalignment='center' )
leg = ax.legend( (p1[0], p2[0], p3[0]), ('PWS withdrawals', 'Reach to aquifer seepage', 'Aquifer to reach seepage'), loc='best' )
leg._drawFrame=False
pylab.yticks(pos, pyNames)
ax.set_xlabel( r'Flow, in m$^{3}$/s' )
ax.set_ylim(-0.5, 1.5)
#--save the figure
ztf.savefig(output_name,dpi=300)
#--clear memory
mpl.pyplot.close('all')
gc.collect()

pos = np.arange(4)
#pWellQ = [WellQ*1.25, WellQ*1.1, WellQ*1.05, WellQ, WellQ*1.25, WellQ] 
#pWellQDry = [WellQDry*1.25, WellQDry*1.1, WellQDry*1.05, WellQDry, WellQDry*1.25, WellQDry] 
pWellQ = [WellQ*1.25, WellQ, WellQ*1.25, WellQ] 
pWellQDry = [WellQDry*1.25, WellQDry, WellQDry*1.25, WellQDry] 

output_name = os.path.join( '..', 'figures', 'SnapperCreekComparison.png' )
print 'creating figure...{0}'.format( output_name )
ztf = mpl.pyplot.figure(figsize=(4.4, 4.), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.25,right=0.95,bottom=0.05,top=0.95)
ax = ztf.add_subplot(1,1,1)
ctxt = 'Snapper Creek (C-2)' 
ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=8,transform=ax.transAxes)
p1 = ax.barh(pos-0.35,pWellQ,height=0.20,color='k')
p2 = ax.barh(pos-0.10,PBaseflow,height=0.20,color='blue')
p3 = ax.barh(pos+0.15,NBaseflow,height=0.20,color='red')
for idx,p in enumerate( pos ):
    ax.text( pWellQ[idx]+.05,p-.25,'{0:4.2f}'.format( pWellQ[idx] ), size=8, verticalalignment='center' )
    ax.text( PBaseflow[idx]+.05,p,'{0:4.2f}'.format( PBaseflow[idx] ), size=8, verticalalignment='center' )
    ax.text( NBaseflow[idx]+.05,p+0.25,'{0:4.2f}'.format( NBaseflow[idx] ), size=8, verticalalignment='center' )
leg = ax.legend( (p1[0], p2[0], p3[0]), ('PWS withdrawals', 'Reach to aquifer seepage', 'Aquifer to reach seepage'), loc='best' )
leg._drawFrame=False
pylab.yticks(pos, yNames)
ax.set_xlabel( r'Flow, in m$^{3}$/s' )
ax.set_ylim(-0.5, 3.5)
#--save the figure
ztf.savefig(output_name,dpi=300)
#--clear memory
mpl.pyplot.close('all')
gc.collect()

output_name = os.path.join( '..', 'figures', 'SnapperCreekComparison_Dry.png' )
print 'creating figure...{0}'.format( output_name )
ztf = mpl.pyplot.figure(figsize=(4.4, 4), facecolor='w')
ztf.subplots_adjust(wspace=0.2,hspace=0.2,left=0.25,right=0.95,bottom=0.05,top=0.95)
ax = ztf.add_subplot(1,1,1)
ctxt = 'Snapper Creek (C-2) - Dry Season' 
ax.text(0.0,1.01,ctxt,horizontalalignment='left',verticalalignment='bottom',size=8,transform=ax.transAxes)
p1 = ax.barh(pos-0.35,pWellQDry,height=0.20,color='k')
p2 = ax.barh(pos-0.10,PBaseflowDry,height=0.20,color='blue')
p3 = ax.barh(pos+0.15,NBaseflowDry,height=0.20,color='red')
for idx,p in enumerate( pos ):
    ax.text( pWellQDry[idx]+.05,p-.25,'{0:4.2f}'.format( pWellQDry[idx] ), size=8, verticalalignment='center' )
    ax.text( PBaseflowDry[idx]+.05,p,'{0:4.2f}'.format( PBaseflowDry[idx] ), size=8, verticalalignment='center' )
    ax.text( NBaseflowDry[idx]+.05,p+0.25,'{0:4.2f}'.format( NBaseflowDry[idx] ), size=8, verticalalignment='center' )
leg = ax.legend( (p1[0], p2[0], p3[0]), ('PWS withdrawals', 'Reach to aquifer seepage', 'Aquifer to reach seepage'), loc='best' )
leg._drawFrame=False
pylab.yticks(pos, yNames)
ax.set_xlabel( r'Flow, in m$^{3}$/s' )
ax.set_ylim(-0.5, 3.5)
#--save the figure
ztf.savefig(output_name,dpi=300)
#--clear memory
mpl.pyplot.close('all')
gc.collect()
