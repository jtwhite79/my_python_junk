#--TSA - Homework #2 - Trend Analysis
#--Jeremy White Sept 2010

#--libraries
import numpy as np
from numpy import ma
import scipy
import pylab

#--load
file = 'trend_example_data.dat'
data = np.loadtxt(file)
col_labels = ['Year','Annual Mean (J-D)']

#--plot data
fig1 = pylab.figure(figsize=(8.5,8.5))
ax = pylab.subplot(2,1,1)
ax.plot(data[:,0],data[:,1],'b+')
ax.plot((np.min(data[:,0]),np.max(data[:,0])),(0,0),'b--')
ax.set_ylabel(col_labels[1])
ax.set_xticklabels('')
ax.set_ylim(-np.abs(np.max(data[:,1])),np.abs(np.max(data[:,1])))

#--calc linear trend
m,b = scipy.polyfit(data[:,0],data[:,1],1)
lin_trend = data[:,0]*m + b
ax.plot(data[:,0],lin_trend,'k-',label='linear trendline')
ax.set_ylim(-np.abs(np.max(data[:,1])),np.abs(np.max(data[:,1]))) 
ax.text(1885,30,'trendline parameters: \n'+str(np.round(m,3))+' '+str(np.round(b,3)))
#ax.set_title('Temperature Anamoly vs Time')
#ax.legend(loc='lower right')

#--calc linear residuals 
res = data[:,1] - lin_trend
m_r,b_r = scipy.polyfit(data[:,0],res,1)
res_lin_trend = data[:,0]*m_r + b_r

#--plot linear residuals
ax2 = pylab.subplot(2,1,2)
ax2.plot(data[:,0],res,'b+')
ax2.plot(data[:,0],res_lin_trend,'k-')
ax2.set_ylabel(col_labels[1]+' - residuals')
ax2.set_xlabel(col_labels[0])
ax2.set_ylim(-np.abs(np.max(res)),np.abs(np.max(res)))
ax2.text(1885,30,'trendline parameters: \n'+str(np.round(m_r,3))+' '+str(np.round(b_r,3)))
#ax2.set_title('Linear Trend Residuals')
#pylab.show()

#--calc MAs 
data_pts = np.shape(data)[0]
tenpt_ma = np.zeros((data_pts),dtype='float')+1.0e+32
fif_ma = np.zeros_like(tenpt_ma)+1.0e+32
twen_ma = np.zeros_like(tenpt_ma)+1.0e+32

for x in range(0,data_pts):
    try:
        this_tenpt_window = data[x-10:x,1]
        tenpt_ma[x] = np.cumsum(this_tenpt_window)[-1]/10.0
    except:
        print 'cant calc past MA for idx: ',x
    
    try:
        print data[x+8,1]   
        this_fif_window = data[x-7:x+8,1]
        fif_ma[x] = np.cumsum(this_fif_window)[-1]/15.0
    except:
        print 'cant calc fif MA for idx: ',x
    
    try:
        print data[x+13,1]
        this_twen_window = data[x-12:x+13,1]
        twen_ma[x] = np.cumsum(this_twen_window)[-1]/25.0
    except:
        print 'cant calc twen MA for idx: ',x      

#--mask locs not calculated
tenpt_ma = ma.masked_where(tenpt_ma==1.0e+32,tenpt_ma)
fif_ma = ma.masked_where(fif_ma==1.0e+32,fif_ma)
twen_ma = ma.masked_where(twen_ma==1.0e+32,twen_ma)

#--plot MAs
fig2 = pylab.figure(figsize=(8.5,8.5))
ax = pylab.subplot(111)
ax.plot(data[:,0],data[:,1],'b+')
ax.plot((np.min(data[:,0]),np.max(data[:,0])),(0,0),'b--')
ax.plot(data[:,0],tenpt_ma,'r-',label='10-point past MA')
ax.plot(data[:,0],fif_ma,'k-',label='15-point central MA')
ax.plot(data[:,0],twen_ma,'g-',label='25-point central MA')
ax.set_xlabel(col_labels[0])
ax.set_ylabel(col_labels[1])
ax.set_ylim(-np.abs(np.max(data[:,1])),np.abs(np.max(data[:,1])))
ax.legend(loc='upper left')
#ax.set_title('Temperature Anamoly vs Time with Moving Averages')


#--calc differencing
f_diff = data[0:-1,1] - data[1:,1]
s_diff = f_diff[0:-1] - f_diff[1:]
t = data[:,0]

#--calc linear trend on diff arrays
m_fd,b_fd = scipy.polyfit(t[:-1],f_diff,1)
m_sd,b_sd = scipy.polyfit(t[:-2],s_diff,1)

#--calc trend lines
fd_trd = t[:-1]*m_fd + b_fd
sd_trd = t[:-2]*m_sd + b_sd

#--plot diff arrays
fig3 = pylab.figure(figsize=(8.5,8.5))

ax = pylab.subplot(2,1,1)
ax.plot(t[:-1],f_diff,'b+')
ax.plot(t[:-1],fd_trd,'k-',label='linear trendline') 
ax.plot((np.min(data[:,0]),np.max(data[:,0])),(0,0),'b--')
ax.set_ylim(-np.abs(np.max(f_diff)),np.abs(np.max(f_diff)))   
ax.set_xlabel(col_labels[0])
ax.set_ylabel(col_labels[1])
ax.set_xticks([])
#ax.set_title('1st-Order Differencing')
ax.text(1885,25,'trendline parameters:\n'+str(np.round(m_fd,3))+' '+str(np.round(b_fd,3)))

ax2 = pylab.subplot(2,1,2)
ax2.plot(t[:-2],s_diff,'b+')
ax2.plot(t[:-2],sd_trd,'k-',label='linear trendline')
ax2.set_ylim(-np.abs(np.max(s_diff)),np.abs(np.max(s_diff)))
ax2.plot((np.min(data[:,0]),np.max(data[:,0])),(0,0),'b--')
#ax2.set_title('2nd-Order Differencing')
ax2.text(1885,40,'trendline parameters:\n'+str(np.round(m_sd,3))+' '+str(np.round(b_sd,3)))
ax2.set_xlabel(col_labels[0])
ax2.set_ylabel(col_labels[1])              

pylab.show()




