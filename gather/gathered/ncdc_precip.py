import os,re,sys
import datetime
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab

def write_to_file(data,filename):
    f = open(filename,'w')
    for line in range(0,len(data)):
        f.write(data[line]+'\n')
    f.close()
    return

mask_val = 999.99

#--load processed file
data = np.fromfile('broward_data_np.dat',sep=',')
length =  np.shape(data)[0]
#--reshape after load
data.resize(length/8,8)

#fig = pylab.figure(figsize=(11,8.5))
#ax= pylab.subplot(111)
##precip = ma.masked_where(data[:,3]>=16,data[:,3]).copy()
#precip = data[np.where(data[:,3]<2),3]
#precip = precip[np.where(precip>0.02)]
#print np.max(precip)
#print precip
#ax.hist(np.transpose(precip),bins=50,normed=True)
#hmin,hmax = ax.get_xlim()
#xhist = np.arange(hmin,hmax,0.05) 
#lamb = -4.5
#yhist = 4.5*np.exp(lamb*xhist)
#ax.plot(xhist,yhist,'r--',linewidth=3.0,label='Exponential Distribution, Rate Parameter  = 4.5')
#ax.legend()
#ax.set_xlabel('Daily Rainfall Intensity (inches)')
#ax.set_ylabel('Normalized Frequency of Occurence')


#--get max/mins for plotting
d_max,d_min = np.max(data[:,2]),np.min(data[:,2]) 
#d_min = datetime.date.toordinal(datetime.date(1990,1,1))
#d_max = datetime.date.toordinal(datetime.date(2000,1,1))
precip_max,precip_min = 16.0,0.0 
#print datetime.date.fromordinal(d_min)
print d_min
#--get unique record ids
coopid = np.unique(data[:,0])
#print coopid

#--set up date formatters
majortick   = YearLocator(10, month=1, day=1) #every 10 years on jan 1 
minortick   = YearLocator(1, month=1, day=1) #every 1 year on jan 1    
months  = MonthLocator()                                               
MonthsFmt = DateFormatter('%b %d')                                     
yearsFmt = DateFormatter('%Y')                                         


fig = pylab.figure(figsize=(11,8.5))   
y_ticks = [precip_min,1.0]


for id in range(0,len(coopid)-1):
    this_t = data[np.argwhere(data[:,0]==coopid[id]),2] 
    this_precip = data[np.argwhere(data[:,0]==coopid[id]),3]
    this_precip = ma.masked_where(this_precip>=mask_val,this_precip) 
    this_precip = ma.masked_where(this_precip<0.002,this_precip)
    #print np.min(this_precip),np.max(this_precip)   
    ax = pylab.subplot(len(coopid),1,id)
    ax.plot(this_t,this_precip,label=str(coopid[id]))
    #ax.legend()
    #ax.set_title(str(coopid[id]))
    ax.xaxis.set_major_locator(majortick)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(minortick)
    ax.set_xticklabels('')
    #ax.set_yticklabels(y_ticks)
    ax.set_yticklabels('')
    ax.set_xlim(d_min,d_max)
    ax.set_ylim(precip_min,precip_max)
    ax.text(698500,5,'Coopid #: '+str(int(coopid[id])))
pylab.figtext(0.1,0.3,'Daily Rainfall Intensity (0 to 16 inches)',horizontalalignment='center',rotation='vertical')

this_t = data[np.argwhere(data[:,0]==coopid[-1]),2]     
this_precip = data[np.argwhere(data[:,0]==coopid[-1]),3] 
this_precip = ma.masked_where(this_precip>=mask_val,this_precip)
this_precip = ma.masked_where(this_precip<0.002,this_precip)
ax = pylab.subplot(len(coopid),1,len(coopid)-1)
ax.plot(this_t,this_precip,label=str(coopid[-1])) 
#ax.set_title(str(coopid[-1]))
ax.set_xlim(d_min,d_max)
ax.set_ylim(precip_min,precip_max)
ax.set_yticklabels('')    
ax.set_xlabel('Year') 
ax.text(698500,5,'Coopid #: '+str(int(coopid[id])))
ax.xaxis.set_major_locator(majortick)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(minortick)

#--plot mean, stdev and count for each day
day_mean = np.zeros((365),dtype='float')
day_stdev = np.zeros_like(day_mean)
day_max = np.zeros_like(day_mean)
day_count = np.zeros((365),dtype='int')
#

print np.shape(data)
for day in range(1,366):
   
    this_date = datetime.date.fromordinal(day)
    m,d = this_date.month,this_date.day 
    m_idx = np.where(data[:,-2]==m)
    this_month = data[m_idx].copy()    
    d_idx = np.where(this_month[:,-1]==d)
    this_day = this_month[d_idx].copy()
    this_day = ma.masked_where(this_day>mask_val/10.0,this_day)
    this_count = np.shape(this_day)[0]
   
    day_mean[day-1],day_stdev[day-1] = np.mean(this_day[:,3]),np.std(this_day[:,3])
    day_max[day-1],day_count[day-1] = np.max(this_day[:,3]),this_count

days = np.arange(1,366)+365 
print np.shape(day_mean),np.shape(days) 
fig2 = pylab.figure(figsize=(11,8.5))
print days[0]
majortick   = MonthLocator()                                               
minortick   = WeekdayLocator()                                               
MonthsFmt = DateFormatter('%b')                                     


mean_ma = []
#-- ma for daily mean
for d in range(7,365-8):
    this_window = day_mean[d-7:d+8] 
    #print np.shape(this_window),this_window,day_mean[d]
    this_ma = (np.cumsum(this_window)[-1])/15
    mean_ma.append(this_ma)
f = open('15_day_ma.dat','w')

for i in range(7):
    mean_ma.insert(0,mean_ma[0])
    mean_ma.append(mean_ma[-1])
mean_ma.append(mean_ma[-1])
print len(mean_ma)

for d_idx in range(365):    
    f.write('{0:10.0f} {1:15.6e}\n'.format(d_idx+1,mean_ma[d_idx]))
f.close()


print len(mean_ma)
ax_mean = pylab.subplot(3,1,1)
ax_mean.set_title('Daily Mean')
ax_mean.plot(days,day_mean,'b+')
ax_mean.plot(days[7:365-8],mean_ma,'k-',linewidth=3.0,label='15-Day Moving Average')
ax_mean.legend(loc='upper left')

ax_stdev = pylab.subplot(3,1,2)
ax_stdev.set_title('Daily Standard Deviation') 
ax_stdev.plot(days,day_stdev,'b+')

ax_max = pylab.subplot(3,1,3)
ax_max.set_title('Daily Maximum')
ax_max.plot(days,day_max,'b+')

#ax_count = pylab.subplot(4,1,4)
#ax_count.set_title('Number of Observations')
#ax_count.plot(days,day_count,'b+')

ax_mean.set_xlim(days[0],days[-2])
ax_stdev.set_xlim(days[0],days[-2])
ax_max.set_xlim(days[0],days[-2])
#ax_count.set_xlim(days[0],days[-2])

ax_mean.xaxis.set_major_locator(majortick)
ax_mean.xaxis.set_major_formatter(MonthsFmt)
ax_mean.xaxis.set_minor_locator(minortick)
ax_mean.set_xticklabels('') 
ax_mean.set_ylabel('inches')

ax_stdev.xaxis.set_major_locator(majortick)
ax_stdev.xaxis.set_major_formatter(MonthsFmt)
ax_stdev.xaxis.set_minor_locator(minortick)
ax_stdev.set_xticklabels('')               
ax_stdev.set_ylabel('inches')

ax_max.xaxis.set_major_locator(majortick)
ax_max.xaxis.set_major_formatter(MonthsFmt)
ax_max.xaxis.set_minor_locator(minortick)    
#ax_max.set_xticklabels('')
ax_max.set_ylabel('inches')               
#ax_count.xaxis.set_major_locator(majortick)
#ax_count.xaxis.set_major_formatter(MonthsFmt)
#ax_count.xaxis.set_minor_locator(minortick)


pylab.show()