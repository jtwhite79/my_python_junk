import os,re
import datetime
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab
from scipy import stats

    
#--load processed file
data = np.fromfile('broward_data_np.dat',sep=',')
length =  np.shape(data)[0]
#--reshape after load
data.resize(length/8,8)
coopid = np.unique(data[:,0])

majortick1   = YearLocator(10, month=1, day=1) #every 10 years on jan 1 
minortick1   = YearLocator(1, month=1, day=1) #every 1 year on jan 1    
majortick2   = YearLocator(1, month=1, day=1) #every 10 years on jan 1                                                                         
minortick2   = YearLocator(1, month=1, day=1) #every 1 year on jan 1                                                                            
months  = MonthLocator()                                               
MonthsFmt = DateFormatter('%b %d')                                     
yearsFmt = DateFormatter('%Y')


for id in range(0,len(coopid)): 
    print coopid[id]
    this_t = data[np.where(data[:,0]==coopid[id]),2][-1].copy()
    this_precip = data[np.where(data[:,0]==coopid[id]),:][0].copy()
    null_idx = np.where(this_precip[:,3] < 16.0)
    this_precip_strip =  this_precip[null_idx].copy()
    this_t_strip = this_t[null_idx].copy()
    this_diff = this_precip_strip[1:].copy()
    this_diff[:,3] = this_precip_strip[1:,3]-this_precip_strip[:-1,3]
    print np.shape(this_precip)
    fig = pylab.figure(figsize=(11,8.5))
    ax1 = pylab.subplot(211)
    ax1.set_title('Station Number: '+str(coopid[id])+' First-Differences')
    ax1.plot(this_t_strip,this_precip_strip[:,3])
    ax1.set_ylim(0,16)
    
    
    ax2 = pylab.subplot(212)
    ax2.plot(this_t_strip[:-1],this_diff[:,3])
    ax2.set_ylim(0,16)
     
    if np.max(this_t_strip)-np.min(this_t_strip) > 3650:
        ax1.xaxis.set_major_locator(majortick1)
        ax1.xaxis.set_major_formatter(yearsFmt)
        ax1.xaxis.set_minor_locator(minortick1)
        ax2.xaxis.set_major_locator(majortick1)     
        ax2.xaxis.set_major_formatter(yearsFmt)
        ax2.xaxis.set_minor_locator(minortick1)
    else:
        ax1.xaxis.set_major_locator(majortick2)
        ax1.xaxis.set_major_formatter(yearsFmt)
        ax1.xaxis.set_minor_locator(minortick2)
        ax2.xaxis.set_major_locator(majortick2)     
        ax2.xaxis.set_major_formatter(yearsFmt)
        ax2.xaxis.set_minor_locator(minortick2) 
        
    pylab.savefig('images\\'+str(coopid[id])+'diff.png',format='png')
      
    #this_diff.tofile(str(coopid[id])+'_diff.dat',sep=',')