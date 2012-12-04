import os,re,sys
import datetime
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab

import calcprob
reload(calcprob)

mon_labels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
mask_val = 2
bin_width = 0.1
#--load processed file
data = np.fromfile('broward_data_np.dat',sep=',')
length = np.shape(data)[0]
#--reshape after load
data.resize(length/8,8)
                                   

this_data = data[np.where(data[:,0]==83163)]
#interval = int(np.shape(this_data)[0]/2.0)
#interval = 3650

#ord=2,precip=3,yr=5,mn=6,dy=7
fig = pylab.figure()
intervals = np.array([1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],dtype='int')

total_histo,total_bins = calcprob.dist(this_data,mask_val,bin_width)

ax = pylab.subplot(6,2,1)



for i in range(0,len(intervals)-1):
    ax = pylab.subplot(5,2,i+1)
    this_decade = this_data[np.where(np.logical_and(this_data[:,-3] >= intervals[i],this_data[:,-3] < intervals[i+1]))]
    print this_decade[:,-3]
    this_hist,this_bins = calcprob.dist(this_decade,mask_val,bin_width)
    ax.plot(this_bins[-1,:-1],np.log10(this_hist[-1,:]),'g-',lw=1.5)
    ax.plot(total_bins[-1,:-1],np.log10(total_histo[-1,:]),'b--',lw=2.0,alpha=0.5)
    
    if i > 7:
        ax.set_xlabel('Precip total (inches)')
    else:
        ax.set_xticklabels([])
    ax.set_ylim(-2.5,1.0)
    ax.text(0.1,-2.0,str(intervals[i])+'\'s')
        
fig.text(0.5,0.95,'Decadal Precipitation Probability Distributions',ha='center')    

fig = pylab.figure()    
ax = pylab.subplot(111)
ax.plot(total_bins[-1,:-1],np.log10(total_histo[-1,:]),'b+',lw=2.0)
ax.plot(total_bins[-1,:-1],np.log10(total_histo[-1,:]),'b-',lw=2.0)

ax.set_xlim(0.002,mask_val)
#ax.text(0.1,0.8,'cumulative')
ax.set_title('Cumulative Precipitation Probability Distribution')
ax.set_xlabel('Precip total (inches)')
ax.set_ylabel('Log Probability')
pylab.show()
sys.exit()


fig = pylab.figure()
for mon in range(0,12):


   
   ax = pylab.subplot(6,2,mon+1)
   
   for i in range(0,len(intervals)-1):
    
       this_decade = this_data[np.where(np.logical_and(this_data[:,-3] >= intervals[i],this_data[:,-3] < intervals[i+1]))]
       this_hist,this_bins = calcprob.dist(this_data[i:i+interval],mask_val,bin_width)
       if i <= (np.shape(this_data)[0]/2.0)-1:
           ax.plot(this_bins[mon,:-1],np.log10(this_hist[mon,:]),'g')
       else:
           ax.plot(this_bins[mon,:-1],np.log10(this_hist[mon,:]),'r')
       
       
   
   ax.plot(total_bins[mon,:-1],np.log10(total_histo[mon,:]),'b+',lw=2.0)
   ax.plot(total_bins[mon,:-1],np.log10(total_histo[mon,:]),'b-',lw=2.0)
   if mon > 9:
       ax.set_xlabel('Precip total (inches)')
       #ax.set_ylabel('Log Probability')
   else: ax.set_xticklabels([])
   ax.set_xlim(0.002,mask_val)
   #ax.set_title(str(mon+1))
   ax.text(0.1,0.7,mon_labels[mon])
   
   
pylab.show()
    
   
   
