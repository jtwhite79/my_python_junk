import pylab
import numpy as np
import numpy.random as random
num_lags = 10
total_lags = np.zeros(1+(num_lags*2),dtype='float')
print total_lags
for i in range(0,1000):
    #rand = np.loadtxt('norm_rand.dat',dtype='float')
    rand = random.uniform(low=-1.0, high=1.0, size=1000)
    #fig = pylab.figure()
    #ax = pylab.subplot(4,1,1)
    #ax.hist(rand,bins=20)
    #
    #ax2 = pylab.subplot(4,1,2)
    #ax2.plot(rand)               
    #
    #print np.cov(rand[1:],rand[:-1])
    #
    x = np.zeros_like(rand)
    
    alpha = [0.7,0.2]
    
    for t in range(2,np.shape(rand)[0]):
        x[t] = rand[t] + alpha[0]*rand[t-1] - alpha[1]*rand[t-2]
    
    ax3 = pylab.subplot(4,1,3)
    ax3.plot(x)
    
    sig_val = 2.0/np.sqrt(np.shape(rand)[0])                          
    fig2 = pylab.figure()
    ax4 = pylab.subplot(111)
    
    lags,c,lincol,b = ax4.acorr(x,maxlags=num_lags)
    total_lags += c
    ax4.plot((-num_lags,num_lags),(sig_val,sig_val),'b-')                          
    ax4.plot((-num_lags,num_lags),(-sig_val,-sig_val),'b-')                          
    sig_lags = c[np.where(np.abs(c)>=sig_val)]
    ax4.set_title('Second_order MA Process Ac.F.')
    #print sig_val,sig_lags[np.shape(sig_lags)[0]/2:]
    ax4.text(-num_lags+2,0.8,'Significant Ac.F. Coefficients:\n'+str(sig_lags[(np.shape(sig_lags)[0]/2)+1:]))
    
    #pylab.show()
print total_lags/1000

#fig = pylab.figure()
#ax = pylab.subplot(111)
#ax.plot(total_lags/1000)
##pylab.show()
