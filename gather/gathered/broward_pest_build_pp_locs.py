import os
import numpy as np
import pylab
from shapely.geometry import Polygon,Point,box
import shapefile
import pestUtil as pu
from bro_pred import seawat

'''setup two groups of pilot points - a coarse layer over the whole domain and a dense layer near the coast
run ppk2fac for both
'''

pp_space_coarse,pp_space_fine = 24,6

cols = seawat.x
rows = np.flipud(seawat.y)

swi_shapename = '..\\_gis\\scratch\\pp_dense_poly'
swi_shape = shapefile.Reader(swi_shapename).shape(0)
swi_poly = Polygon(swi_shape.points)

buffer_distance = pp_space_fine * seawat.delc * 1.25
swi_buffer = swi_poly.buffer(buffer_distance)
wr = shapefile.Writer()
wr.field('buf_dist','N',20,5)
wr.poly([swi_buffer.exterior.coords],shapefile.POLYGON)
wr.record([buffer_distance])
wr.save('..\\_gis\\scratch\\swi_buffer')

ibound = (np.loadtxt('bro.02\\calibration\\seawatref\\ibound_CS.ref'))



pp_locs = []
pp_types = []
pp_names = []
fcount,ccount = 1,1
fine_zone = np.zeros((seawat.nrow,seawat.ncol))
for i,row in enumerate(rows):
    for j,col in enumerate(cols):        
        if ibound[i,j] > 0:            
            xmin,xmax = col-(seawat.delr/2.0),col+(seawat.delr/2.0)
            ymin,ymax = row-(seawat.delc/2.0),row+(seawat.delc/2.0)
            cell = box(xmin,ymin,xmax,ymax)
            if cell.intersects(swi_buffer):
                fine_zone[i,j] = 1
            if i % pp_space_coarse == 0.0 and j % pp_space_coarse == 0.0:
                pp_locs.append([col,row])
                pp_types.append('coarse')
                pname = 'pp_'+str(ccount)
                pp_names.append(pname)
                ccount += 1
            else:
                pt = Point([col,row])
                if pt.intersects(swi_poly):
                    if i % pp_space_fine == 0 and j % pp_space_fine == 0:
                        pp_locs.append([col,row])
                        pp_types.append('fine')
                        pname = 'pp_'+str(fcount)
                        pp_names.append(pname)
                        fcount += 1

#fine_zone = np.flipud(fine_zone)
print 'fine_cells for interpolation:',np.cumsum(fine_zone)[-1]
np.savetxt('ref\\fine_zone.ref',fine_zone,fmt=' %3d')


coarse_zone = ibound.copy()
coarse_zone[np.where(coarse_zone!=0)] = 1
print 'coarse_cells for interpolation:',np.cumsum(coarse_zone)[-1]
#coarse_zone = np.ones((seawat.nrow,seawat.ncol))
np.savetxt('ref\\coarse_zone.ref',coarse_zone,fmt=' %3d')

#pylab.imshow(fine_zone)
#ylab.show()

#f = open('misc\\pp_locs.dat','w',0)
wr = shapefile.Writer()
wr.field('name','C',20)
wr.field('x','N',20,5)
wr.field('y','N',20,5)
wr.field('type','C',20)
wr.field('name','C',20)
for i,[pp_loc,pp_type,pp_name] in enumerate(zip(pp_locs,pp_types,pp_names)):
    pname = 'pp_{0:04d}'.format(i+1)
    #f.write('{0:25s} {1:15.6G} {2:15.6G} {3:3d} {4:3.1f}\n'.format(pname,pp_loc[0],pp_loc[1],1,1))
    wr.poly([[pp_loc]],shapefile.POINT)
    wr.record([pname,pp_loc[0],pp_loc[1],pp_type,pp_name])
wr.save('..\\_gis\\scratch\\pp_locs')

f_c,f_f = open('misc\\pp_locs_coarse.dat','w',0),open('misc\\pp_locs_fine.dat','w',0)
for pp_type,pp_name,pp_loc in zip(pp_types,pp_names,pp_locs):
    x,y = pp_loc[0],pp_loc[1]   

    if pp_type == 'fine':
        f_f.write('{0:25s} {1:15.5E} {2:15.5E} {3:6d} {4:15.5E}\n'.format(pp_name,x,y,1,1))
    else:
        f_c.write('{0:25s} {1:15.5E} {2:15.5E} {3:6d} {4:15.5E}\n'.format(pp_name,x,y,1,1))
f_f.close()
f_c.close()
        
#--write the structure files based on the pp spacing
struct_args = []
f = open('misc\\pp_struct_base.dat','r')
for line in f:
    struct_args.append(line.strip())
f.close()
coarse_A = pp_space_coarse * seawat.delc * 1.25
struct_args[11] = ' A '+str(coarse_A)
f = open('misc\\pp_struct_coarse.dat','w',0)
for arg in struct_args:
    f.write(arg+'\n')
f.close()
fine_A = pp_space_fine * seawat.delc * 1.25
struct_args[11] = ' A '+str(fine_A)
f = open('misc\\pp_struct_fine.dat','w',0)
for arg in struct_args:
    f.write(arg+'\n')
f.close()

#--run ppk2fac
args = []
f = open('misc\\ppk2fac1.in','r')
for line in f:
    args.append(line.strip())
f.close()
args[1] = 'misc\\pp_locs_coarse.dat'
args[3] = 'ref\\coarse_zone.ref'
args[5] = 'misc\\pp_struct_coarse.dat'
args[9] = str(coarse_A*10)
args[12] = 'factors\\pp_fac_coarse.fac'
args[14] = 'ref\\pp_stdev_coarse.ref'
args[15] = 'misc\\pp_reg_coarse.dat'
f = open('misc\\ppk2fac1_coarse.in','w',0)
for a in args:
    f.write(a+'\n')
f.close()
for i,a in enumerate(args):
    args[i] = a.replace('coarse','fine')
args[9] = str(fine_A*10)
f = open('misc\\ppk2fac1_fine.in','w',0)
for a in args:
    f.write(a+'\n')
f.close()    

os.system('ppk2fac1.exe <misc\\ppk2fac1_coarse.in')
os.system('ppk2fac1.exe <misc\\ppk2fac1_fine.in')


c_stdev = pu.load_wrapped_format(seawat.nrow,seawat.ncol,'ref\\pp_stdev_coarse.ref')
f_stdev = pu.load_wrapped_format(seawat.nrow,seawat.ncol,'ref\\pp_stdev_fine.ref')

c_stdev = np.ma.masked_where(coarse_zone==0,c_stdev)
pylab.imshow(c_stdev)
pylab.show()

f_stdev = np.ma.masked_where(fine_zone==0,f_stdev)
pylab.imshow(f_stdev)
pylab.show()





  


