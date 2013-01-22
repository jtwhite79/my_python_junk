from scipy import *                                                       
import scipy.io.array_import                                              
#from scipy import gplt                                                    
from scipy import fftpack                                                 
import pylab
import numpy as np
                                                                          
tempdata = scipy.io.array_import.read_array('sunspots.dat')               
                                                                          
year=tempdata[:,0]                                                        
wolfer=tempdata[:,1]
fig1 = pylab.figure()
ax1 = pylab.subplot(111)                                                      
ax1.plot(year,wolfer,'r+')                    

                                                                          
Y=fft(wolfer)
fig2 = pylab.figure()
ax2 = pylab.subplot(111)                                                                                                                   
ax2.plot(Y.real,Y.imag,'r+')                       
 
                                                                          
n=len(Y)                                                                  
power = abs(Y[1:(n/2)])**2                                                
nyquist=1./2                                                              
freq=array(range(n/2))/(n/2.0)*nyquist
print len(freq)                                    
fig3 = pylab.figure()
ax3 = pylab.subplot(111)                                                      
ax3.plot(freq[1:len(freq)], power)
ax3.set_xlim(0,0.2)       
                                                                          
period=1./freq                    
fig4 = pylab.figure()
ax4 = pylab.subplot(111)                                                                                              
ax4.plot(period[1:len(period)], power)
ax4.set_xlim(0,40)   

pylab.show()
