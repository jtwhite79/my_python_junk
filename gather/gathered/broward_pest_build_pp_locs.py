import numpy as np
from shapely.geometry import Polygon,Point
import shapefile

from bro_pred import seawat


cols = seawat.x
rows = seawat.y

swi_shapename = '..\\_gis\\scratch\\pp_dense_poly'
swi_shape = shapefile.Reader(swi_shapename).shape(0)
swi_poly = Polygon(swi_shape.points)

ibound = np.flipud(np.loadtxt('bro.02\\calibration\\seawatref\\ibound_CS.ref'))

pp_space_coarse,pp_space_fine = 25,5

pp_locs = []
pp_types = []
for i,row in enumerate(rows):
    for j,col in enumerate(cols):
        if ibound[i,j] > 0:            
            if i % pp_space_coarse == 0.0 and j % pp_space_coarse == 0.0:
                pp_locs.append([col,row])
                pp_types.append('coarse')
            else:
                pt = Point([col,row])
                if pt.intersects(swi_poly):
                    if i % pp_space_fine == 0 and j % pp_space_fine == 0:
                        pp_locs.append([col,row])
                        pp_types.append('fine')
f = open('misc\\pp_locs.dat','w',0)
wr = shapefile.Writer()
wr.field('name','C',20)
wr.field('x','N',20,5)
wr.field('y','N',20,5)
wr.field('type','C',20)
for i,[pp_loc,pp_type] in enumerate(zip(pp_locs,pp_types)):
    pname = 'pp_{0:04d}'.format(i+1)
    f.write('{0:25s} {1:15.6G} {2:15.6G} {3:3d} {4:3.1f}\n'.format(pname,pp_loc[0],pp_loc[1],1,1))
    wr.poly([[pp_loc]],shapefile.POINT)
    wr.record([pname,pp_loc[0],pp_loc[1],pp_type])
wr.save('..\\_gis\\scratch\\pp_locs')
  


