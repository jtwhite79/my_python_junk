import numpy as np
from numpy import ma
import pylab
import scipy

data = np.loadtxt('midterm_2.dat')

pts = np.shape(data)[0]
x = np.arange(0,pts)

print np.mean(data[pts/2:]),np.mean(data[:pts/2])
print np.var(data[pts/2:]),np.var(data[:pts/2])
m,b = scipy.polyfit(x,data,1)
l_t = (x*m)+b
d_t = data - l_t
m2,b2 = scipy.polyfit(x,d_t,1)
print m
window = 30 
var_window = 500
tenpt_ma = np.zeros_like((x)).astype(float)+1.0e+32 
tenpt_var = np.zeros_like((x)).astype(float)+1.0e+32
for pt in range(0,pts): 
    try:
        this_tenpt_window = d_t[pt-window/2:pt+window/2]
      
        tenpt_ma[pt] = np.cumsum(this_tenpt_window)[-1]/(float(window))
        
    except:
        pass
        
    try:
        #print d_t[pt-var_window/2],d_t[pt+var_window/2]
        this_tenpt_var = np.var(d_t[pt-var_window/2:pt+var_window/2]) 
        tenpt_var[pt] = this_tenpt_var
    except:
        pass
     
print np.shape(x),np.shape(tenpt_ma)
tenpt_var[:var_window/2] = 1.0e+32 
tenpt_ma = ma.masked_where(tenpt_ma==1.0e+32,tenpt_ma)
tenpt_var = ma.masked_where(tenpt_var==1.0e+32,tenpt_var)

fig = pylab.figure(figsize=(5,7))
ax1 = pylab.subplot(211)
#ax1.plot(data,'b--',label='X')
#ax1.plot((x*m)+b,'k-',label='Linear Trend of X')
#ax1.text(200,3.25,'Linear Trend Parameters: '+str(m)+' '+str(b))
ax1.plot(tenpt_ma,'k-',label=str(window)+'-unit moving average')
#ax1.set_xticklabels('')
ax1.set_ylabel('X(t)')
ax1.set_xlim(0,pts)
ax1.legend()
#ax3 = pylab.twinx()
#ax3.plot(tenpt_var,'r-')

#ax1.plot((x*m2)+b2,'k-')
ax2 = pylab.subplot(212)
sig_val = 2.0/np.sqrt(pts)
lags = 10 
ax2.plot(tenpt_var,label=str(var_window)+'-unit variance')
ax2.plot((0,pt),(np.var(data),np.var(data)),label='variance')
ax2.set_ylabel('var(X(t))') 
ax2.legend()
ax2.set_xlim(0,pts)
ax2.set_xlabel('t')

#ax2.acorr(d_t,maxlags=lags)
#ax2.plot([-lags,lags],[sig_val,sig_val])
pylab.show()