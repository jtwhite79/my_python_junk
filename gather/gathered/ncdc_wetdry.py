import os,re
import datetime
import numpy as np
from numpy import ma
from scipy import stats
from matplotlib.dates import *
import matplotlib.ticker as ticker
import pylab

    
#--load processed file
data = np.fromfile('broward_data_np.dat',sep=',')
length =  np.shape(data)[0]
#--reshape after load
data.resize(length/8,8)
coopid = np.unique(data[:,0])
fig = pylab.figure(figsize=(11,8.5))
row,col=1,1
for id in range(0,len(coopid)-1):
    this_t = data[np.where(data[:,0]==coopid[id]),2][-1] 
    this_precip = data[np.where(data[:,0]==coopid[id]),3][-1]
    #m,b = scipy.polyfit(this_t,this_precip,1)
    (a,b,r,tt,stderr)= stats.linregress(this_t,this_precip)
    #print coopid[id],a,b,r,tt,stderr
    #print coopid[id],'\n\n\n\n'
    #print this_precip
    #print '\n\n\n'
    this_wetdry = np.ones((np.shape(this_precip)),dtype='int')
    #print np.shape(this_t),np.shape(this_precip),np.shape(this_wetdry)
    for day in range(1,np.shape(this_t)[0]):
        #print this_t[day]-1,this_t[day-1]
        if this_t[day]-1==this_t[day-1]:
            if this_precip[day]<=0.02:
                this_wetdry[day] = 0
            elif this_precip[day]<16.0:
                this_wetdry[day] = 2
                
    print row,col
    ax = pylab.subplot(6,col,row)
    this_precip[np.where(this_precip>16.0)] = 0.0
    ax.acorr(this_precip,maxlags=15,lw=3,normed=False)
    cmin,cmax = ax.get_xlim()
    sig_val = 2.0/np.sqrt(np.shape(this_precip)[0])
    print sig_val,np.shape(this_precip),np.sqrt(np.shape(this_precip)[0])
    ax.plot([cmin,cmax],[sig_val,sig_val],'k-')
    ax.set_title('Coopid #: '+str(int(coopid[id])))
    ax.set_xlabel('Days')
    ax.set_ylabel('Ac.F.')
    row += 1
    if row > 6: 
        col = 2
        row = 1
    this_wetdry.tofile(str(coopid[id])+'_wetdry.dat',sep=',')
pylab.savefig(str(coopid[id])+'.png',format='png')    