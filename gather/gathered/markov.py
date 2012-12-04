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

def calc_prob(array):
    row,col = np.shape(array)
    #print array
    row_total = np.sum(array,axis=1)
    row_sum = np.cumsum(row_total)[-1]
    fix_prob_vec = row_total/row_sum
    #print 'row total,row_sum,prob_vec',row_total,row_sum,fix_prob_vec
    prob_mat = np.zeros_like(array)
    for c in range(0,col):
        prob_mat[:,c] = fix_prob_vec[c]*row_total
        #print fix_prob_vec[c],prob_mat
    #print prob_mat
    return prob_mat
    



path = 'markov\\'
files = os.listdir(path)

cum_t_total = np.zeros((2,2))
mean_t_prob = np.zeros_like(cum_t_total)
cum_wd_total = np.zeros((2))
f_count = 0

for file in files:
    t_total = np.zeros((2,2))
    wd_total = np.zeros((2))
    array = np.loadtxt(path+file,dtype='int',delimiter=',')
    
    array.resize(np.shape(array)[0]/3,3) 
    print array[0] 
    month = 10
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
        
    cum_t_total += t_total
    cum_wd_total += wd_total
    t_prob = calc_prob(t_total)
    mean_t_prob += t_prob
    #print t_total
    f_count += 1
print cum_t_total,'\n'
row_total =  np.sum(cum_t_total,axis=1)    
#cum_t_prob = calc_prob(cum_t_total)
#cum_t_prob = cum_t_total/row_total
print cum_t_total[0,:]/row_total[0]
print cum_t_total[1,:]/row_total[1]
mean_t_prob = mean_t_prob/f_count
#print cum_t_prob,'\n',mean_t_prob 