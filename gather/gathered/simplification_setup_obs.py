import os
import shutil
from datetime import datetime
import pandas
import shapefile
from simple import grid

f = open('settings.fig','w',0)
f.write('date = dd/mm/yyy\ncolrow=no\n')
f.close()

points,records = shapefile.load_as_dict('shapes\\simple_obs')
ids = records['Id']

#--set the obs at the bottom of upper
for olayer in range(grid.nlay):
    if grid.lay_key[olayer] != 'upper':
        break
print os.path.abspath('.\\')
f = open('_misc\\bore_coords.dat','w',0)
onames = []
for point,id in zip(points,ids):
    point = point.points[0]
    x,y = point
    oname = 'obs_'+str(id)
    onames.append(oname+'up')
    onames.append(oname+'lw')
    f.write('{0:25s} {1:15.5E} {2:15.5E} {3:6d}\n'.format(oname+'up',x,y,olayer))
    f.write('{0:25s} {1:15.5E} {2:15.5E} {3:6d}\n'.format(oname+'lw',x,y,9))
f.close()


f = open('_misc\\heads.smp','w',0)
for oname in onames:
    for end in grid.sp_end:
        f.write('{0:25s} {1:25s} {2:15.5E}\n'.format(oname,end.strftime('%d/%m/%Y %H:%M:%S'),1.0))
f.close()

#--run mod2obs
args = ['_misc\\simple.grd','_misc\\bore_coords.dat','_misc\\bore_coords.dat','_misc\\heads.smp','_model\\'+grid.modelname+'.hds','f',\
    '1.0e+10','d','01/01/2013','00:00:00',str(grid.nlay),str(grid.step.days),'mheads.smp']
f = open('mod2obs.in','w',0)
f.write('\n'.join(args)+'\n')
f.close()

os.system('mod2obs.exe <mod2obs.in')
shutil.copy('mheads.smp','_misc\\heads.smp')

