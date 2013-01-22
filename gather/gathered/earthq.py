import numpy as np

data = np.loadtxt('earthq.dat')
med = np.median(data)
u1_idx = np.argwhere(data>med)
l1_idx = np.argwhere(data<med)
print np.shape(u1_idx),np.shape(l1_idx)
#print u1_idx
#print l1_idx

#print np.shape(idx)
#print np.mean(data[idx])
#print np.mean(data[idx+1])
data2 = data[u1_idx+1]
#print data2
u2_idx = np.where(data2>med)[1]
l2_idx = np.where(data2<med)[1]
print np.shape(u2_idx),np.shape(l2_idx)