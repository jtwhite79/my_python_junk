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

def trans(array):
    monthly_trans = np.zeros((13,2,2))
    cum_t_total = np.zeros((2,2))
    for month in range(1,13):    
        t_total = np.zeros((2,2))
        month_idx = np.where(array[:,-1]==month)
        wetdry = array[month_idx,0][-1]  
        observations =  np.shape(wetdry)[0]     
        for obs in range(1,observations):
            if wetdry[obs-1] != 1:
                if wetdry[obs] == 0:
           
                    if wetdry[obs-1] == 0:
                        t_total[1,1] += 1
                    else:
                        t_total[1,0] += 1
                else:
                     
                     if wetdry[obs-1] == 0:
                        t_total[0,1] += 1
                     else:   
                         t_total[0,0] += 1
        
        row_total = np.sum(t_total,axis=1)        
        wet_prob = t_total[0,:]/row_total[0]
        dry_prob = t_total[1,:]/row_total[1]
        monthly_trans[month-1,:,:] = [wet_prob,dry_prob]
        cum_t_total += t_total
    row_total = np.sum(cum_t_total,axis=1)        
    wet_prob = cum_t_total[0,:]/row_total[0]
    dry_prob = cum_t_total[1,:]/row_total[1]
    monthly_trans[12,:,:] = [wet_prob,dry_prob] 
    return monthly_trans    
    
    
def dist(array,mask_val,bw):
    
    bins = np.arange(0,mask_val,bw)
    monthly_histo = np.zeros((13,np.shape(bins)[0]-1),dtype='float')
    monthly_bins = np.zeros((13,np.shape(bins)[0]),dtype='float')
    for mon in range(0,12):
        this_month_data = array[np.where(array[:,6]==mon+1)]
        this_precip = this_month_data[:,3]
        this_hist,this_binedges = np.histogram(this_precip,bins=bins,range=(0.002,mask_val),normed=True)    
        monthly_histo[mon,] = this_hist
        monthly_bins[mon] = this_binedges
    this_precip = array[:,3]
    this_hist,this_binedges = np.histogram(this_precip,bins=bins,range=(0.002,mask_val),normed=True)    
    monthly_histo[12] = this_hist
    monthly_bins[12] = this_binedges
    return monthly_histo,monthly_bins