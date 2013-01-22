import numpy as np
import pylab 

wsp1 = np.loadtxt('p5-11_100ft.txt',skiprows=8,delimiter=',')
wsp2 = np.loadtxt('p5-11_10000ft.txt',skiprows=8,delimiter=',')

fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
ax.plot(wsp1[:,0],wsp1[:,-1],'go',label='100ft')
ax.plot(wsp2[:,0],wsp2[:,-1],'bo',label='10,000ft')

ax2.plot(wsp1[:,0],wsp1[:,1],'go')
ax2.plot(wsp2[:,0],wsp2[:,1],'bo')       
#ax2.plot([0,300.0],[y0,y0],'k-',label='normal depth')
#ax2.plot([0,300.0],[yc,yc],'k--',label='critical depth')
ax.set_ylabel('head')
ax2.set_ylabel('water surface profile (ft)')
ax2.set_xlabel('distance (ft)')
ax.set_xlabel('distance (ft)') 
ax.legend()
ax2.legend(loc=4)
pylab.show()