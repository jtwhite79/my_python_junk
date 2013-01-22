import numpy as np
from numpy import random
import pylab
totim = 1000
z = random.uniform(0.0,1.0,totim)
ma_len = 100 
ar_len = 2
betas = np.linspace(1,0,num=ma_len)
alphas = np.linspace(1,0,num=ar_len)
print betas
                       
x_ma = np.zeros_like(z)
x_ar = np.zeros_like(z)
             
x_ar[:ar_len] = z[:ar_len]                       
for t in range(ma_len,totim):
    x_ma[t] = np.cumsum(z[t-ma_len]*betas)[-1]

for t in range(ar_len,totim):
    x_ar[t] = np.cumsum(x_ar[t-ar_len]*alphas)[-1]+z[t]
    
    
fig = pylab.figure()
ax1 = pylab.subplot(211)
ax1.plot(x_ma,'b-')
ax1.plot(x_ar,'r+')

pylab.show()