import os,re
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
    
#--load processed file
data = np.fromfile('broward_data_np.dat',sep=',')
length =  np.shape(data)[0]
#--reshape after load
data.resize(length/8,8)
coopid = np.unique(data[:,0])
print data[0]

for id in range(0,len(coopid)-1):
    this_t = data[np.where(data[:,0]==coopid[id]),2][-1] 
    this_precip = data[np.where(data[:,0]==coopid[id]),:][0]
    #print np.shape(this_precip)
    this_wetdry = np.ones((np.shape(this_precip)[0],4),dtype='int')
    this_wetdry[:,-2:] = 0
    #print np.shape(this_wetdry),this_wetdry[0]
    #print np.shape(this_t),np.shape(this_precip),np.shape(this_wetdry)
    for day in range(1,np.shape(this_t)[0]):
        #print this_t[day]-1,this_t[day-1]
        if this_t[day]-1==this_t[day-1]:
            if this_precip[day,3]<=0.02:
                this_wetdry[day] = (0,this_precip[day,-1],this_precip[day,-2],this_precip[day,-3])
            elif this_precip[day,3]<16.0:
                this_wetdry[day] = (2,this_precip[day,-1],this_precip[day,-2],this_precip[day,-3])
    this_wetdry.tofile(str(coopid[id])+'_wetdry.dat',sep=',')
    