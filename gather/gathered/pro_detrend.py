import os,re
import datetime
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab


days = np.arange(1,366)+365    
majortick   = MonthLocator()                                               
minortick   = WeekdayLocator()                                               
MonthsFmt = DateFormatter('%b') 

path = 'LT\\'

max_m = 0
max_s = 0
max_max = 0

files = os.listdir(path)
for file in files:
    print file
    data = np.loadtxt(path+file,delimiter=',')
    length =  np.shape(data)[0]
    #--reshape after load
    data.resize(length/8,8)
    
    print np.shape(data)
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
        this_count = np.shape(this_day)[0]
       
        day_mean[day-1],day_stdev[day-1] = np.mean(this_day[:,3]),np.std(this_day[:,3])
        day_max[day-1],day_count[day-1] = np.max(this_day[:,3]),this_count
    
    this_station = int(file.split('.')[0])
    #fig = pylab.figure(figsize=(11,8.5))
    #ax_m = pylab.subplot(3,1,1)
    #ax_m.plot(days,day_mean,'b+')
    #ax_m.set_title('Station: '+str(this_station)+' First Differences Daily Mean')
    #ax_m.xaxis.set_major_locator(majortick)
    #ax_m.xaxis.set_major_formatter(MonthsFmt)
    #ax_m.xaxis.set_minor_locator(minortick)
    #ax_m.set_xticklabels('') 
    #    
    #ax_s = pylab.subplot(3,1,2) 
    #ax_s.set_title('Daily Standard Deviation')
    #ax_s.plot(days,day_stdev,'b+')
    #ax_s.xaxis.set_major_locator(majortick)
    #ax_s.xaxis.set_major_formatter(MonthsFmt)
    #ax_s.xaxis.set_minor_locator(minortick)
    #ax_s.set_xticklabels('') 
    #
    #ax_max = pylab.subplot(3,1,3)
    #ax_max.plot(days,day_max,'b+')
    #ax_max.xaxis.set_major_locator(majortick)      
    #ax_max.xaxis.set_major_formatter(MonthsFmt)
    #ax_max.xaxis.set_minor_locator(minortick)
    #ax_max.set_title('Daily Maximum')  
    
    #ax_m.set_ylim(0,2.75)
    #ax_s.set_ylim(0,4.5)
    #ax_max.set_ylim(0,16)
    
    
    
    
    #pylab.show()
    #pylab.savefig('images\\'+file+'_pro.png',format='png')
    
    if np.max(np.abs(day_mean)) > max_m: max_m = np.max(np.abs(day_mean))
    if np.max(np.abs(day_stdev)) > max_s: max_s = np.max(np.abs(day_stdev))
    if np.max(np.abs(day_max)) > max_max: max_max = np.max(np.abs(day_max))
    
    fig2 = pylab.figure()
    ax = pylab.subplot(111)
    ax.acorr(data[:,3],maxlags=15,lw=3)
    pylab.savefig('images\\'+file+'_acf.png',format='png')
    
    
print max_m,max_s,max_max
    
    
    
    