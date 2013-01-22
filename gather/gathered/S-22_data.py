import math
import numpy as np
from numpy import ma
import pylab
import scipy
import matplotlib as mpl
from matplotlib.dates import *
from matplotlib.font_manager import FontProperties
import matplotlib.collections as collections

import MFBinaryClass as mfb 
reload(mfb)

#--main script
OutputToScreen = False
Res_Dir = '..\\Results\\'
outbase = 'S-22Flow'
outext = '.png'

xmin = 0.
xmax = 1035.
xtickv = [0,91,182,273,365,456,547,638,730,821,912,1003,1095]
xtickt = ['0','0.25','0.5','0.75','1','1.25','1.5','1.75','2','2.25','2.5','2.75','3']

cfs2cms = 1.0 / ( 3.28081 * 3.28081 * 3.28081 )
ft2m = 1.0 / 3.28081

cdata = '..\\Data\\S-22_H_T_Q.ref'
s22 = np.loadtxt(cdata,skiprows=1)
idxs = np.argwhere(np.abs(s22)>9998.0)
s22[idxs] = 0.0

#--detrend raw data
m,b = scipy.polyfit(s22[:,0],s22[:,1]*ft2m,1)
trd = s22[:,0]*m + b
print 'S-22_H\n slope: ', m,' intercept: ', b, ' mean: ', s22[:,1].mean()*ft2m
S22_H = s22[:,1]*ft2m - trd

m,b = scipy.polyfit(s22[:,0],s22[:,2]*ft2m,1)
trd = s22[:,0]*m + b
print 'S-22_T\n slope: ', m,' intercept: ', b, ' mean: ', s22[:,2].mean()*ft2m
S22_T = s22[:,2]*ft2m - trd

m,b = scipy.polyfit(s22[:,0],s22[:,3]*cfs2cms,1)
trd = s22[:,0]*m + b
print 'S-22_Q\n slope: ', m,' intercept: ', b, ' mean: ', s22[:,3].mean()*cfs2cms
S22_Q = s22[:,3]*cfs2cms - trd

m,b = scipy.polyfit(s22[:,0],s22[:,4]*ft2m,1)
trd = s22[:,0]*m + b
print 'G-3572\n slope: ', m,' intercept: ', b, ' mean: ', s22[:,4].mean()*ft2m
G3572 = s22[:,4]*ft2m - trd


#tot_len = min( s22.shape[0], 3592 )
tot_len = s22.shape[0]

avg_day = 30
avg_len = int( tot_len / avg_day )
a_time  = np.zeros( avg_len, np.float )
a_S22_H = np.zeros( avg_len, np.float )
a_S22_T = np.zeros( avg_len, np.float )
a_S22_Q = np.zeros( avg_len, np.float )
a_G3572 = np.zeros( avg_len, np.float )
d_S22_H = np.zeros( avg_len, np.float )
d_S22_T = np.zeros( avg_len, np.float )
d_S22_Q = np.zeros( avg_len, np.float )
d_G3572 = np.zeros( avg_len, np.float )

avg_fac = 1.0 / float( avg_day )
ipos = 0
for ia in range(0,avg_len):
    a_time[ia] = avg_day * float( ia + 1 )
    h = 0.0
    t = 0.0
    q = 0.0
    g = 0.0
    for i in range(0,avg_day):
        h += s22[ipos,1]*ft2m * avg_fac
        t += s22[ipos,2]*ft2m * avg_fac
        q += s22[ipos,3]*cfs2cms * avg_fac
        g += s22[ipos,4]*ft2m * avg_fac
        ipos += 1
    a_S22_H[ia] = h
    a_S22_T[ia] = t
    a_S22_Q[ia] = q
    a_G3572[ia] = g

#-detrend averaged data
m,b = scipy.polyfit(a_time,a_S22_H,1)
trd = a_time*m + b
print 'average S-22_H\n slope: ', m,' intercept: ', b, ' mean: ', a_S22_H.mean()
d_S22_H = a_S22_H - trd

m,b = scipy.polyfit(a_time,a_S22_T,1)
trd = a_time*m + b
print 'average S-22_T\n slope: ', m,' intercept: ', b, ' mean: ', a_S22_T.mean()
d_S22_T = a_S22_T - trd

m,b = scipy.polyfit(a_time,a_S22_Q,1)
trd = a_time*m + b
print 'average S-22_Q\n slope: ', m,' intercept: ', b, ' mean: ', a_S22_Q.mean()
d_S22_Q = a_S22_Q - trd

m,b = scipy.polyfit(a_time,a_G3572,1)
trd = a_time*m + b
print 'average G-3572\n slope: ', m,' intercept: ', b, ' mean: ', a_G3572.mean()
d_G3572 = a_G3572 - trd


#wet season - dry season dates
#dry = [0,121,335,486,700,851,1065,1216,1430,1582,1796,1947,2161,2312,2526,2677,2891,3043,3257,3408]
dry1 = [0,335,700,1065,1430,1796,2161,2526,2891,3257]
dry2 = [121,486,851,1216,1582,1947,2312,2677,3043,3408]
#wet = [152,305,517,670,882,1035,1247,1400,1612,1766,1978,2131,2343,2496,2708,2861,3073,3227,3439,3592]
wet1 = [152,517,882,1247,1612,1978,2343,2708,3073,3439]
wet2 = [305,670,1035,1400,1766,2131,2496,2861,3227,3592]
mdry = np.zeros(tot_len,np.int)
mwet = np.zeros(tot_len,np.int)
ipos = 0
for i in range(0,tot_len):
    t = s22[i,0]
    d1 = dry1[ipos]
    d2 = dry2[ipos]
    if t < d1:
        continue
    elif t >= d1 and t <= d2:
        mdry[i] = 1
    else:
        ipos += 1
        if ipos > len(dry1) - 1:
            break
        continue
ipos = 0
for i in range(0,tot_len):
    t = s22[i,0]
    w1 = wet1[ipos]
    w2 = wet2[ipos]
    if t < w1:
        continue
    elif t >= w1 and t <= w2:
        mwet[i] = 1
    else:
        ipos += 1
        if ipos > len(wet1) - 1:
            break
        continue
    

mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['legend.fontsize'] = 6
    
#raw data figure
fig = pylab.figure()
fig = pylab.figure(figsize=(9.0, 5.5), facecolor='w')
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=0.10,right=0.9125,bottom=0.075,top=0.95)

ax = pylab.subplot(311)
ax.plot(s22[:,0],s22[:,1]*ft2m,marker='o',markeredgecolor='black',markerfacecolor='blue',markersize=3,linewidth=0.0,label='S-22_H')
ax.plot(s22[:,0],s22[:,2]*ft2m,marker='o',markeredgecolor='black',markerfacecolor='red',markersize=3,linewidth=0.0,label='S-22_T')
#ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='black',markersize=3,linewidth=0.0,label='S-22_Q')
#ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='green',markersize=3,linewidth=0.0,label='G-3572')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

ax.set_ylabel(r'Elevation, $m$', size='8')
ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(xmin,xmax)
ax.set_ylim(-0.2,1.4)

ax = pylab.subplot(312)
ax.plot(s22[:,0],s22[:,3]*cfs2cms,marker='o',markeredgecolor='black',markerfacecolor='black',markersize=3,linewidth=0.0,label='S-22_Q')
ax.set_ylabel(r'Discharge, $m^3/s$', size='8')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(0.0,xmax)
ax.set_ylim(0.0,40.)


ax = pylab.subplot(313)
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='blue',markersize=3,linewidth=0.0,label='S-22_H')
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='red',markersize=3,linewidth=0.0,label='S-22_T')
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='black',markersize=3,linewidth=0.0,label='S-22_Q')
ax.plot(s22[:,0],s22[:,4]*ft2m,marker='o',markeredgecolor='black',markerfacecolor='green',markersize=3,linewidth=0.0,label='G-3572')
ax.set_ylabel(r'Elevation, $m$', size='8')
ax.set_xlabel(r'Simulation Time, $years$', size='8')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

#ax.set_ylim(0.0,40.)
ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(xmin,xmax)

leg = ax.legend(loc='upper left',numpoints=1)
leg.draw_frame(False)

outfig = '..\\Figures\\S-22_data.png'
fig.savefig(outfig,dpi=300)
print 'writing results to...', outfig

#--raw data correlogram
fig = pylab.figure()
fig = pylab.figure(figsize=(9.0, 5.5), facecolor='w')
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=0.10,right=0.9125,bottom=0.075,top=0.95)

mlags = 120
numer = math.sqrt( float(tot_len) )
sig   = 2.0 / numer

blw = 1.0
slw = 0.5

mv = s22[:,1].mean()*ft2m
ax = pylab.subplot(411)
#ax.acorr(s22[:,1]*ft2m-mv, usevlines=True, normed=True, maxlags=mlags, color='blue', lw=blw)
ax.acorr(S22_H, usevlines=True, normed=True, maxlags=mlags, color='blue', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='black', linewidth=0.0, alpha=0.5)
ax.grid(True)
#ax.axhline(0, color='black', lw=1)
ax.set_yticks([-0.2,0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-0.2,1)
ax.text(0.90, 0.90,'S-22_H',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)
     
mv = s22[:,2].mean()*ft2m
ax = pylab.subplot(412)
#ax.acorr(s22[:,2]*ft2m-mv, usevlines=True, normed=True, maxlags=mlags, color='red', lw=blw)
ax.acorr(S22_T, usevlines=True, normed=True, maxlags=mlags, color='red', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='black', linewidth=0.0, alpha=0.5)
ax.grid(True)
#ax.axhline(0, color='black', lw=1)
ax.set_yticks([-0.2,0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-0.2,1)
ax.text(0.90, 0.90,'S-22_T',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)

mv = s22[:,3].mean()*cfs2cms
ax = pylab.subplot(413)
#ax.acorr(s22[:,3]*cfs2cms-mv, usevlines=True, normed=True, maxlags=mlags, color='black', lw=blw)
ax.acorr(S22_Q, usevlines=True, normed=True, maxlags=mlags, color='black', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='black', linewidth=0.0, alpha=0.5)
ax.grid(True)
#ax.axhline(0, color='black', lw=1)
ax.set_yticks([-0.2,0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-0.2,1)
ax.text(0.90, 0.90,'S-22_Q',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)

mv = s22[:,4].mean()*ft2m
ax = pylab.subplot(414)
#ax.acorr(s22[:,4]*ft2m-mv, usevlines=True, normed=True, maxlags=mlags, color='green', lw=blw)
ax.acorr(G3572, usevlines=True, normed=True, maxlags=mlags, color='green', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='black', linewidth=0.0, alpha=0.5)
ax.grid(True)
#ax.axhline(0, color='black', lw=1)
ax.set_yticks([-0.2,0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-0.2,1)
ax.text(0.90, 0.90,'G-3572',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)
ax.set_xlabel(r'Number of Lags, $days$', size='8')

outfig = '..\\Figures\\S-22_data_acorr.png'
fig.savefig(outfig,dpi=300)
print 'writing results to...', outfig


#average data figure
fig = pylab.figure()
fig = pylab.figure(figsize=(9.0, 5.5), facecolor='w')
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=0.10,right=0.9125,bottom=0.075,top=0.95)

ax = pylab.subplot(311)
ax.plot(a_time,a_S22_H,marker='o',markeredgecolor='black',markerfacecolor='blue',markersize=3,color='blue',linewidth=0.5,label='S-22_H')
ax.plot(a_time,a_S22_T,marker='o',markeredgecolor='black',markerfacecolor='red',markersize=3,color='red',linewidth=0.5,label='S-22_T')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=-0.2, ymax=1.4, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

ax.set_ylabel(r'Elevation, $m$', size='8')
ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(xmin,xmax)
ax.set_ylim(-0.2,1.4)

ax = pylab.subplot(312)
ax.plot(a_time,a_S22_Q,marker='o',markeredgecolor='black',markerfacecolor='black',markersize=3,color='black',linewidth=0.5,label='S-22_Q')
ax.set_ylabel(r'Discharge, $m^3/s$', size='8')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(0.0,xmax)
ax.set_ylim(0.0,40.)


ax = pylab.subplot(313)
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='blue',markersize=3,color='blue',linewidth=0.5,label='S-22_H')
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='red',markersize=3,color='red',linewidth=0.5,label='S-22_T')
ax.plot([-10,-10],[0,0],marker='o',markeredgecolor='black',markerfacecolor='black',markersize=3,color='black',linewidth=0.5,label='S-22_Q')
ax.plot(a_time,a_G3572,marker='o',markeredgecolor='black',markerfacecolor='green',markersize=3,color='green',linewidth=0.5,label='G-3572')
ax.set_ylabel(r'Elevation, $m$', size='8')
ax.set_xlabel(r'Simulation Time, $years$', size='8')
# add wet-dry polygons
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mdry>0, facecolor='#8A4117', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=mwet>0, facecolor='#82CAFF', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)
collection = collections.BrokenBarHCollection.span_where(
       s22[:,0], ymin=0.0, ymax=40.0, where=s22[:,0]<365, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.add_collection(collection)

ax.set_ylim(0.0,3.0)
ax.set_xticks(xtickv)
ax.set_xticklabels(xtickt)
ax.set_xlim(xmin,xmax)

leg = ax.legend(loc='upper left',numpoints=1)
leg.draw_frame(False)

outfig = '..\\Figures\\S-22_data_am.png'
fig.savefig(outfig,dpi=300)
print 'writing results to...', outfig

#--average data correlogram
fig = pylab.figure()
fig = pylab.figure(figsize=(9.0, 5.5), facecolor='w')
fig.subplots_adjust(wspace=0.25,hspace=0.25,left=0.10,right=0.9125,bottom=0.075,top=0.95)

mlags = 36
numer = math.sqrt( float(avg_len) )
sig   = 2.0 / numer

blw = 2.0
slw = 0.5

ax = pylab.subplot(411)
ax.acorr(d_S22_H, usevlines=True, normed=True, maxlags=mlags, color='blue', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.grid(True)
ax.set_xticks([0,6,12,18,24,30,36])
ax.set_yticks([-1,-.75,-.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-1,1)
ax.text(0.85, 0.925,'S-22_H average monthly',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)
     
ax = pylab.subplot(412)
ax.acorr(d_S22_T, usevlines=True, normed=True, maxlags=mlags, color='red', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.grid(True)
ax.set_xticks([0,6,12,18,24,30,36])
ax.set_yticks([-1,-.75,-.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-1,1)
ax.text(0.85, 0.925,'S-22_T average monthly',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)

ax = pylab.subplot(413)
ax.acorr(d_S22_Q, usevlines=True, normed=True, maxlags=mlags, color='black', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.grid(True)
ax.set_xticks([0,6,12,18,24,30,36])
ax.set_yticks([-1,-.75,-.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-1,1)
ax.text(0.85, 0.925,'S-22_Q average monthly',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)

ax = pylab.subplot(414)
ax.acorr(d_G3572, usevlines=True, normed=True, maxlags=mlags, color='green', lw=blw)
ax.axhspan(ymin=-sig, ymax=sig, facecolor='#342826', linewidth=0.0, alpha=0.5)
ax.grid(True)
ax.set_xticks([0,6,12,18,24,30,36])
ax.set_yticks([-1,-.75,-.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xlim(0,mlags)
ax.set_ylim(-1,1)
ax.text(0.85, 0.925,'G-3572 average monthly',
     horizontalalignment='left',
     verticalalignment='center',
     fontsize = 6,
     transform = ax.transAxes)
ax.set_xlabel(r'Number of Lags, $months$', size='8')

outfig = '..\\Figures\\S-22_data_acorr_am.png'
fig.savefig(outfig,dpi=300)
print 'writing results to...', outfig
  