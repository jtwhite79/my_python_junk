import numpy as np
import pylab

delt_pix = 0.03

u = np.flipud(np.loadtxt('u.mat'))
s = (np.loadtxt('s.vec'))
print s.shape
s_mat = np.zeros((s.shape[0],s.shape[0]))
for i,ss in enumerate(s):
    s_mat[i,i] = ss
s_mat = np.flipud(s_mat) 
   
vt = (np.loadtxt('lhs.mat'))

u = np.ma.masked_where(u == 0.0,u)
s_mat = np.ma.masked_where(s_mat == 0.0,s_mat)
vt = np.ma.masked_where(vt == 0.0,vt)


fig = pylab.figure()
loc_1 = [0.05,0.05,delt_pix*u.shape[1],delt_pix*u.shape[0]]
ax = pylab.axes(loc_1)
ax.pcolor(u,vmin=-1.0,vmax=1.0)
loc_2 = [loc_1[0]+loc_1[2]+delt_pix,loc_1[1],delt_pix*s_mat.shape[0],delt_pix*s_mat.shape[0]]
ax2 = pylab.axes(loc_2)
#ax2 = pylab.subplot(132)
ax2.pcolor(s_mat,vmin=-1.0,vmax=1.0) 
loc_3 = [loc_2[0]+loc_2[2]+delt_pix,loc_1[1],delt_pix*vt.shape[0],delt_pix*vt.shape[0]]
#ax3 = pylab.subplot(133)
ax3 = pylab.axes(loc_3)
ax3.pcolor(np.flipud(vt.transpose()),vmin=-1.0,vmax=1.0)
pylab.show()
