import math
import numpy as np
import scipy.linalg as la
import pylab
from matplotlib.patches import Ellipse

def rotate(point,angle):
    sin_phi = math.sin(angle*math.pi/180.0)
    cos_phi = math.cos(angle*math.pi/180.0)
    new_x = (point[0] * cos_phi) - (point[1] * sin_phi)
    new_y = (point[0] * sin_phi) + (point[1] * cos_phi)
    
    return new_x,new_y

#--first make some data
numpts = 500
rot_angle = 15

#xmin,xmax = 1.75,2.25
#ymin,ymax = 0.5,3.5
#xpts = np.random.uniform(xmin,xmax,numpts)
#ypts = np.random.uniform(ymin,ymax,numpts)

xmean,xstd = 0.0,1.5
xpts = np.random.normal(xmean,xstd,numpts)
ymean,ystd = 0.0,1.5
ypts = np.random.normal(ymean,ystd,numpts)

new_x,new_y = [],[]
for x,y in zip(xpts,ypts):
    nx,ny = rotate([x,y],rot_angle)
    new_x.append(nx)
    new_y.append(ny)

xpts = np.array(new_x)
ypts = np.array(new_y)


#--simple data stats
meanx,meany = xpts.mean(),ypts.mean()
varx,vary = np.var(xpts),np.var(ypts)

#fig = pylab.figure(figsize=(5,3.5))
#ax = pylab.subplot(121)
#ax.hist(xpts,50)
#ax.grid()
#ax.set_xlabel('$X_1$')
#ax.set_ylabel('count')
#pylab.savefig('x1.png',dpi=300,format='png',bbox_inches='tight')


##fig = pylab.figure(figsize=(5,5))
#ax2 = pylab.subplot(122)
#ax2.hist(xpts,50)
#ax2.grid()
#ax2.set_xlabel('$X_2$')
#ax2.set_ylabel('')
#ax2.set_yticklabels([])
#pylab.savefig('x2.png',dpi=300,format='png',bbox_inches='tight')



#--build covariance matrix
data = np.vstack((xpts,ypts))
cov = np.cov(data)

#--eigen decomposition
eig_vals,eig_vecs = la.eig(cov)
eig_vals = np.sqrt(eig_vals)
#print np.dot(eig_vecs[:,0],eig_vecs[:,1])

#--build scaled eigenvectors for plotting
cent = np.array([meanx,meany])
ev1 = (eig_vals[0].real * eig_vecs[:,0]) + cent
ev2 = (eig_vals[1].real * eig_vecs[:,1]) + cent

xmin,xmax = -5,5

#--plot 
fig = pylab.figure(figsize=(5,5))
ax = pylab.subplot(111)

#--scatter of data
ax.scatter(xpts,ypts,marker='.',color='k',s=1.0,alpha=0.5)
#xmin,xmax = ax.get_xlim()
#ymin,ymax = ax.get_ylim()
#ax.set_xlim(min(xmin,ymin),max(xmax,ymax))
#x.set_ylim(min(xmin,ymin),max(xmax,ymax))
ax.set_xlim(xmin,xmax)
ax.set_ylim(xmin,xmax)
ax.grid()
ax.set_xlabel('$X_1$')
ax.set_ylabel('$X_2$')
#pylab.savefig('scatter.png',dpi=300,format='png',bbox_inches='tight')

#--scaled eigenvectors 
ax.plot([cent[0],ev1[0]],[cent[1],ev1[1]],'b-',lw=3.0)
ax.plot([cent[0],ev2[0]],[cent[1],ev2[1]],'b-',lw=3.0)
ax.set_xlim(xmin,xmax)
ax.set_ylim(xmin,xmax)

#pylab.savefig('eigen.png',dpi=300,format='png',bbox_inches='tight')

#--ellipse
ax.add_artist(Ellipse(cent,eig_vals[0].real*2,eig_vals[1].real*2,rot_angle,alpha=0.25))
ax.set_xlim(xmin,xmax)
ax.set_ylim(xmin,xmax)
pylab.savefig('circ.png',dpi=300,format='png',bbox_inches='tight')


xmin,xmax = ax.get_xlim()
ymin,ymax = ax.get_ylim()
ax.set_xlim(min(xmin,ymin),max(xmax,ymax))
ax.set_ylim(min(xmin,ymin),max(xmax,ymax))
pylab.show()






