
import sys
from datetime import datetime
import numpy as np
from simple import grid

pt_space = 0.5
pt_num = 1
pt_prefix = 'pt_'
grd_num = 1
grp_num = 1
rtime = 0.0
lines = []
for k in range(0,grid.nlay):
    ibound = np.loadtxt('_model\\'+grid.ibound_names[k])
    for i in range(1,grid.nrow):
        for j in range(1,grid.ncol):
            if ibound[i-1,j-1] == 1:
                ystart,yend = grid.rows[i-1],grid.rows[i]
                xstart,xend = grid.cols[i-1],grid.cols[i]
                #xpt = np.linspace(xstart,xend,pt_per_cell)
                #ypt = np.linspace(ystart,yend,pt_per_cell)
                #xpt = np.arange(xstart+pt_space,xend,pt_space)
                #ypt = np.arange(yend+pt_space,ystart,pt_space)
                xpt = np.arange(pt_space,1.0,pt_space)
                ypt = np.arange(pt_space,1.0,pt_space)
                zpt = np.arange(pt_space,1.0,pt_space)
                for x in xpt:
                    for y in ypt:
                        for z in zpt:
                            pt_name = pt_prefix + str(pt_num)
                            line = ' {0:10d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d} {6:1.5f} {7:1.5f} {8:1.5f} {9:15.6G} {10:40s}'\
                                .format(pt_num,grp_num,grd_num,k+1,i+1,j+1,x,y,z,rtime,pt_name)
                            lines.append(line)
                            pt_num += 1
print len(lines)
f = open('_model\\simple.locations','w',0)
f.write('# '+sys.argv[0] + ' ' + str(datetime.now())+'\n')
f.write('1  #input style\n')
f.write('1  #groupcount\n')
f.write('PG00 {0:10d}\n'.format(len(lines)))
for line in lines:
    f.write(line+'\n')

f.close()
