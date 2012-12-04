#--transition matrix shape
#--   wet dry   2  0
#--wet        2
#--dry        0
#--
import os,re
import datetime
import numpy as np
from numpy import ma
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab

import calcprob
reload(calcprob)



path = 'markov\\'
files = os.listdir(path)
mon_labels = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
array = np.loadtxt('markov\\83163.0_wetdry.dat',dtype='int',delimiter=',')
array.resize(np.shape(array)[0]/3,3) 

#--calc trans prob for entire series
monthly_trans = calcprob.trans(array)
print np.shape(array)



#--monte carlo control parameters
interval = 3650 #days
samp_range = [0,np.shape(array)[0]]
numdraws = np.shape(array)[0]/interval
print numdraws

trans_draws = np.zeros((numdraws,13,2,2),dtype='float')
start_end = np.zeros((numdraws,2),dtype='int')

for draw in range(0,numdraws):
    this_start = draw*interval
    this_end = this_start + interval
    #print start,samp_range
    this_trans = calcprob.trans(array[this_start:this_end,:])
    #print np.shape(this_trans),np.shape(trans_draws[0,:,:,:])
    trans_draws[draw] = this_trans
    start_end[draw,0] = this_start
    start_end[draw,1] = this_end
    
fig = pylab.figure()
ax = pylab.subplot(221)


for d in range(0,numdraws):
    if start_end[d,0] < (np.shape(array)[0]/2):
        ax.plot(np.arange(1,13),trans_draws[d,:-1,0,0],'g-',lw=1.0)
    else:
        ax.plot(np.arange(1,13),trans_draws[d,:-1,0,0],'r-',lw=1.0)
ax.plot(np.arange(1,13),monthly_trans[:-1,0,0],'b+',lw=2.0)     
ax.plot(np.arange(1,13),monthly_trans[:-1,0,0],'b-',lw=2.0) #ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,0,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,0,0],monthly_trans[-1,0,0]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Wet-Wet Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

ax = pylab.subplot(222)
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b-',lw=2.0)
for d in range(0,numdraws):
    if start_end[d,0] < (np.shape(array)[0]/2):
        ax.plot(np.arange(1,13),trans_draws[d,:-1,0,1],'g-',lw=1.0)
    else:
        ax.plot(np.arange(1,13),trans_draws[d,:-1,0,1],'r-',lw=1.0)
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b-',lw=2.0)
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,0,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,0,1],monthly_trans[-1,0,1]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Wet-Dry Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

ax = pylab.subplot(223)

for d in range(0,numdraws):
    if start_end[d,0] < (np.shape(array)[0]/2):
        ax.plot(np.arange(1,13),trans_draws[d,:-1,1,0],'g-',lw=1.0)
    else:
        ax.plot(np.arange(1,13),trans_draws[d,:-1,1,0],'r-',lw=1.0)
ax.plot(np.arange(1,13),monthly_trans[:-1,1,0],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,1,0],'b-',lw=2.0)
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,1,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,1,0],monthly_trans[-1,1,0]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Dry-Wet Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

ax = pylab.subplot(224)

for d in range(0,numdraws):
    if start_end[d,0] < (np.shape(array)[0]/2):
        ax.plot(np.arange(1,13),trans_draws[d,:-1,1,1],'g-',lw=1.0)
    else:
        ax.plot(np.arange(1,13),trans_draws[d,:-1,1,1],'r-',lw=1.0)
ax.plot(np.arange(1,13),monthly_trans[:-1,1,1],'b+',lw=2.0)
ax.plot(np.arange(1,13),monthly_trans[:-1,1,1],'b-',lw=2.0)
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,1,1],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,1,1],monthly_trans[-1,1,1]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Dry-Dry Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)


pylab.show()