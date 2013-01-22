import sys
import os
import numpy as np
import pylab
import pestUtil as pu
import grid

def dist(p1,p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5



#--name of the structure file
sfile = 'structure.dat'
a = 10.0
sill = 1.0    
pu.write_structure('structure.dat','struct1',a=a,sill=sill,transform='log')

#--specify grid shape and create x,y locations vectors
offset = [0.0,0.0]
nrow,ncol = 25,25
delr,delc =  1.0,1.0
itrunc = 10
npar = nrow * ncol

#--build a selection matrix
sel = np.zeros((nrow,ncol))
for i in range(2,nrow,5):
    for j in range(2,ncol,5):
        sel[i,j] = 1
#pylab.pcolor(sel)
#pylab.show()

#--instance of a grid
mfgrid = grid.mfgrid(offset[0],offset[1],nrow,ncol,delr,delc)
node_locs = mfgrid.node_locations()

#--instance of geostats
mfgeo = grid.geostat(a,sill,'exponential',node_locs)
mfgeo.eig()

#--plot eigen components
X,Y = np.meshgrid(mfgrid.xnode_locations(),mfgrid.ynode_locations())
for itrunc in range(1,50):
    eig = mfgeo.eigvecs[:,itrunc]
    c = 0
    arr = np.zeros((nrow,ncol))
    for i in range(nrow):
        for j in range(ncol):
            arr[i,j] = eig[c]
            c += 1
    fig = pylab.figure()
    ax = pylab.subplot(111)
    ax.pcolor(X,Y,arr)
    pylab.show()
    pass
#mfgeo.build_forward_kl(itrunc)
#mfgeo.build_back_kl(itrunc)
#np.savetxt('scale2.dat',mfgeo.forward,fmt=' %15.6e')
#np.savetxt('unscale2.dat',mfgeo.back,fmt=' %15.6e')
