import copy
import os
import numpy as np
import pylab
import shapefile
from simple import grid


#--use ppk2fac to generate kriging factors
infile = 'ppk2fac1.in'
f = open(infile,'r')
in_lines = []
for line in f:
    in_lines.append(line.strip())
f.close()

#--write the grid file
f = open('_misc\\simple.grd','w',0)
f.write('{0:10d} {1:10d}\n'.format(grid.nrow,grid.ncol))
f.write('{0:15.5G} {1:15.5G} 0.0\n'.format(grid.xmin,grid.cols[-1]))
for dr in grid.delr:
    f.write(' {0:10.3F}'.format(dr))
f.write('\n')
for dc in grid.delc:
    f.write(' {0:10.3F}'.format(dc))
f.write('\n')
f.close()

pp_space = 10
ref_dir = '_model\\ref\\'
pp_files = []
zone_files = []
wr = shapefile.Writer()
wr.field('x','N',20,5)
wr.field('y','N',20,5)
wr.field('layer','N',10)
wr.field('name','C',25)

row_centers = grid.rows[:-1] - grid.deltaxy/2.0
col_centers = grid.cols[:-1] + grid.deltaxy/2.0

#--use uppermost layer in each hydro zone
up_layers = [grid.lay_key.index('upper'),grid.lay_key.index('middle'),grid.lay_key.index('lower')]
up_names = ['upper','middle','lower']
for k,kname in zip(up_layers,up_names):
    pp_file = 'pp_locs\\pp_locs_'+kname+'.dat'
    pp_files.append(pp_file)
    f = open(pp_file,'w',0)
    ibound = np.loadtxt(ref_dir+'ibound_'+str(k+1)+'.ref')
    zone = ibound.copy()
    zone[np.where(zone>0.0)] = 1
    print k+1,np.cumsum(zone)[-1]
    zone_file = 'ref\\zone_'+str(k+1)+'.ref'
    zone_files.append(zone_file)
    np.savetxt(zone_file,zone,fmt=' %2d')
    pp_count = 1
    for i,row in enumerate(row_centers):
        for j,col in enumerate(col_centers):
            if ibound[i,j] > 0 and i % pp_space == 0 and j % pp_space == 0:
                pp_name = 'pp_'+str(k+1)+'_'+str(pp_count)
                pp_locs = [col,row]
                f.write('{0:15s} {1:15.5g} {2:15.5g} {3:10d} {4:10.2f}\n'.format(pp_name,col,row,1,1.0))
                wr.poly([[[col,row]]],shapefile.POINT)
                wr.record([col,row,k+1,pp_name])
                pp_count += 1
    f.close()

    in_layer = copy.deepcopy(in_lines)
    in_layer[1] = pp_file
    in_layer[3] = zone_file
    in_layer[12] = 'factors\\pp_fac_'+kname+'.ref'
    in_layer[14] = 'ref\\stdev_'+kname+'.ref'
    in_layer[15] = '_misc\\pp_reg_'+kname+'.ref'
    f = open('temp.in','w',0)
    for line in in_layer:
        f.write(line+'\n')
    f.close()
    os.system('ppk2fac1.exe <temp.in')

    #--write

    
wr.save('shapes\\pp_locs')















