import numpy as np
import pylab

import pestUtil as pu

res = pu.load_res('pest.res')
print res[2]

par = np.loadtxt('pest.par',skiprows=1,usecols=[1])


x = np.array([250,750,1250,1750,2250,2750,3250,3750,4250,4750])
width = 500.0
print len(res[2][0])
fig = pylab.figure()
ax = pylab.subplot(111)
axt = pylab.twinx()
#ax.bar(x,res[2][0],width=width,color='g',alpha=0.5)
#ax.bar(x-width,res[3][0],width=width,color='b',alpha=0.5)
ax.plot(x,res[2][0],'g--',label='syn')
ax.plot(x,res[3][0],'b-',label='cal')
ax.plot(x,res[2][0],'g.',label='syn')
ax.plot(x,res[3][0],'b.',label='cal')
axt.bar(x-width/2.0,par[:-1],width=width,color='none')
axt.set_ylabel('K')
ax.set_ylabel('water level')

pylab.show()