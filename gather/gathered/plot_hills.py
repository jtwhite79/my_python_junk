import numpy as np
from numpy import ma
import pylab
from scipy import stats
import lstUtil as lu

data = np.loadtxt('hills_mb_ord.dat')
quan = stats.mstats.mquantiles(data[:,1])

q1 = ma.masked_where(data[:,1]>quan[0],data[:,1])
q2 = ma.masked_where(np.logical_and(data[:,1]<quan[0],data[:,1]>quan[1]),data[:,1])
q3 = ma.masked_where(data[:,1]<quan[2],data[:,1])
sk = np.zeros_like(data[:,0])

for day in range(0,data.shape[0]):
    sk[day] = stats.skew(data[:day,1])
mean_sk = np.mean(sk[7300:])
std_sk = np.std(sk[7300:])
quan_sk = stats.mstats.mquantiles(sk[3650:])
print quan_sk

print mean_sk    
fig = pylab.figure()
ax = pylab.subplot(111)
ax_t = pylab.twinx()

lu.plot_ts(data[:,0],q1,'',color='b',ax=ax,output=None)
lu.plot_ts(data[:,0],q2,'',color='g',ax=ax,output=None)
lu.plot_ts(data[:,0],q3,'',color='r',ax=ax,output=None)
lu.plot_ts(data[:,0],sk,'',color='k',ax=ax_t,output=None)
ax_t.plot((np.min(data[3650:,0]),np.max(data[:,0])),(mean_sk,mean_sk),'k--',lw=2.0)
ax_t.plot((np.min(data[3650:,0]),np.max(data[:,0])),(mean_sk+std_sk*2.0,mean_sk+std_sk*2.0),'k--',lw=1.0)
ax_t.plot((np.min(data[3650:,0]),np.max(data[:,0])),(mean_sk-std_sk*2.0,mean_sk-std_sk*2.0),'k--',lw=1.0)
#ax_t.plot((np.min(data[:,0]),np.max(data[:,0])),(quan_sk[0],quan_sk[0]),'k--',lw=2.0,alpha=0.4)
#ax_t.plot((np.min(data[:,0]),np.max(data[:,0])),(quan_sk[2],quan_sk[2]),'k--',lw=2.0,alpha=0.4)
ax.set_ylabel('flow (cfs)',fontsize=15)
ax_t.set_ylabel('skewness',fontsize=15)

mu,sigma = np.mean(sk[3650:]),np.std(sk[3650:])
x = np.arange(0.0,5.0,0.01)
gauss = 1.0/(np.sqrt(2.0*3.14159*sigma**2))*np.exp(-1.0*((x-mu)**2)/(2.0*sigma**2))


fig = pylab.figure()
ax2 = pylab.subplot(111)
ax2.hist(sk[3650:],bins=40,normed=True)
xmin,xmax = ax2.get_xlim()
ax2.plot(x,gauss,'k--',lw=2.0)
ax2.set_title('Distribution of Skewness')
ax2.set_xlim(xmin,xmax)


fig = pylab.figure()
ax3 = pylab.subplot(111)
ax3.hist(data[:,1],bins=40,normed=True)
ax3.text(3000,0.003,'Skewness = '+str(np.round(stats.skew(data[:,1]),3)),ha='center',fontsize=32)
ax3.set_ylabel('Probability')
ax3.set_xlabel('flow (cfs)')


fig = pylab.figure()
ax4 = pylab.subplot(111)
ax4.acorr(data[:,1])

pylab.show()