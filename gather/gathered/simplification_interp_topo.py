import os
import numpy as np
from scipy.interpolate import Rbf

import shapefile
import simple

#--first write pilot points file from topot_points shape
shapename = 'shapes\\simple_topo_points'
f = open('misc\\topo_points.dat','w',0)
points,rec_dict = shapefile.load_as_dict(shapename)
xs,ys,ztops = [],[],[]
for pt,id,ztop in zip(points,rec_dict['Id'],rec_dict['ztop']):
    x,y = pt.points[0][0],pt.points[0][1]
    if x in xs and y in ys:
        print 'dup',id
    else:
        xs.append(x)
        ys.append(y)
        ztops.append(ztop)
    pname = 'topo_{0:02d}'.format(id)
    f.write('{0:20s} {1:15E} {2:15E}  1   {3:15E}\n'.format(pname,x,y,float(ztop)))
f.close()
xs,ys,ztops = np.array(xs),np.array(ys),np.array(ztops)
zs = np.ones(xs.shape)

#--write the grid file
f = open('misc\\simple.grd','w',0)
f.write('{0:10d} {1:10d}\n'.format(simple.grid.nrow,simple.grid.ncol))
f.write('{0:15.5G} {1:15.5G} 0.0\n'.format(simple.grid.xmin,simple.grid.cols[-1]))
for dr in simple.grid.delr:
    f.write(' {0:10.3F}'.format(dr))
f.write('\n')
for dc in simple.grid.delc:
    f.write(' {0:10.3F}'.format(dc))
f.write('\n')
f.close()

rbfi = Rbf(xs,ys,zs,ztops,epsilon=1000.0)
#xs,ys = simple.grid.cols[:-1] + (simple.grid.delta/2.0),simple.grid.rows[-1] + (simple.grid.delta/2.0)
#zs = np.ones(xs.shape)
#X,Y,Z = np.meshgrid(xs,ys)
print 'calc rbf...'
interp_topo = np.zeros((simple.grid.nrow,simple.grid.ncol))
for i in range(simple.grid.nrow):
    for j in range(simple.grid.ncol):
        x,y = simple.grid.cols[j] + (simple.grid.delta/2.0),simple.grid.rows[i] + (simple.grid.delta/2.0)
        itopo = rbfi(x,y,1)
        interp_topo[i,j] = itopo
interp_topo[np.where(interp_topo<100.0)] = 100.0
print interp_topo.min()
interp_topo = np.flipud(interp_topo)
np.savetxt('ref\\interp_topo.ref',interp_topo,fmt=' %15.6E')

print 'loading grid shape'        
shapes,records = shapefile.load_as_dict('shapes\\simple_grid')
wr = shapefile.writer_like('shapes\\simple_grid')

print 'writing new grid shape'
ibound = np.zeros((simple.grid.nrow,simple.grid.ncol))
for shape,row,col,ibnd in zip(shapes,records['row'],records['column'],records['ibound']):
    wr.poly([shape.points])
    ibound[row-1,col-1] = ibnd
    topo = interp_topo[row-1,col-1]
    rec = [row,col,ibnd,topo]
    wr.record(rec)

wr.save('shapes\\simple_topo')
np.savetxt('ref\\ibound.ref',ibound,fmt=' %4d')




