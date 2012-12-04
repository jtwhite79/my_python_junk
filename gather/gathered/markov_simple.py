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
cum_t_total = np.zeros((2,2))
cum_wd_total = np.zeros((2))
monthly_trans = np.zeros((13,2,2))

t_total = np.zeros((2,2))
wd_total = np.zeros((2))

array = np.loadtxt('markov\\83163.0_wetdry.dat',dtype='int',delimiter=',')

array.resize(np.shape(array)[0]/3,3) 
print array[0] 
for month in range(1,13):
    month_idx = np.where(array[:,-1]==month)
    wetdry = array[month_idx,0][-1]  
    observations =  np.shape(wetdry)[0]     
    for obs in range(1,observations):
        if wetdry[obs-1] != 1:
            if wetdry[obs] == 0:
                wd_total[1] += 1
                if wetdry[obs-1] == 0:
                    t_total[1,1] += 1
                else:
                    t_total[1,0] += 1
            else:
                 wd_total[0] += 1
                 if wetdry[obs-1] == 0:
                    t_total[0,1] += 1
                 else:   
                     t_total[0,0] += 1
    
    row_total = np.sum(t_total,axis=1)        
    wet_prob = t_total[0,:]/row_total[0]
    dry_prob = t_total[1,:]/row_total[1]
    #print month
    #print wet_prob
    #print dry_prob
    monthly_trans[month-1,:,:] = [wet_prob,dry_prob]
    #print monthly_trans[month-1,1]
    cum_t_total += t_total
    cum_wd_total += wd_total
    t_total = np.zeros((2,2))
    wd_total = np.zeros((2)) 
    
func_monthly = calcprob.trans(array)
print func_monthly
#print '\n'
row_total =  np.sum(cum_t_total,axis=1)    
wet_prob = cum_t_total[0,:]/row_total[0]
dry_prob = cum_t_total[1,:]/row_total[1]
#print wet_prob
#print dry_prob
monthly_trans[12,:,:] = [wet_prob,dry_prob]
fig = pylab.figure()
ax = pylab.subplot(221)
ax.plot(np.arange(1,13),monthly_trans[:-1,0,0],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,0,0],'b-')
ax.plot(np.arange(1,13),func_monthly[:-1,0,0],'r+')
ax.plot(np.arange(1,13),func_monthly[:-1,0,0],'r-')
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,0,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,0,0],monthly_trans[-1,0,0]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Wet-Wet Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

for mon in range(0,12):
    print monthly_trans[mon,:,0],func_monthly[mon,:,0]


ax = pylab.subplot(222)
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,0,1],'b-')
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,0,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,0,1],monthly_trans[-1,0,1]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Wet-Dry Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

ax = pylab.subplot(223)
ax.plot(np.arange(1,13),monthly_trans[:-1,1,0],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,1,0],'b-')
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,1,0],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,1,0],monthly_trans[-1,1,0]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Dry-Wet Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)

ax = pylab.subplot(224)
ax.plot(np.arange(1,13),monthly_trans[:-1,1,1],'b+')
ax.plot(np.arange(1,13),monthly_trans[:-1,1,1],'b-')
#ax.bar(np.arange(0.25,12.25),monthly_trans[:-1,1,1],width=0.5,fc='b',alpha=0.5)
ax.plot([1,12],[monthly_trans[-1,1,1],monthly_trans[-1,1,1]],'k--',lw=2.0,alpha=0.5)
ax.set_xlim(1,12)
ax.set_title('Dry-Dry Probablity')
ax.set_xticks(np.arange(1,13))
ax.set_xticklabels(mon_labels)


pylab.show()