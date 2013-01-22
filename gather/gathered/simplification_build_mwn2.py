import sys
from datetime import datetime
import numpy as np
import pylab
import pandas
import shapefile
from simple import grid

def add_zeros(rec,prob = 0.975):
    for i,r in enumerate(rec):
        rand = np.random.rand()
        if rand > prob:
            rec[i] = 0.0
    return rec

def write():
    #--get the well locations
    shapename = '..\\shapes\\simple_well_grid_join'
    records = shapefile.load_as_dict(shapename,loadShapes=False)
    rows,cols,ztops,zbots,ids,hydros = records['row'],records['column_'],records['ztop'],records['zbot'],records['Id'],records['hydro']


    #--random sampling
    #--first create normal distributions for the wells
    upper_mean,upper_std = -500.0,10.0
    lower_mean,lower_std = -5000.0,50.0
    nper = len(grid.sp_start)
    well_records = []
    for id,hydro in zip(ids,hydros):
        if hydro == 3:
            rec = np.random.normal(lower_mean,lower_std,nper)
        if hydro == 1:
            rec = np.random.normal(upper_mean,upper_std,nper)
        rec = add_zeros(rec)
        well_records.append(rec)
    well_records = np.array(well_records).transpose()
    well_records[np.where(well_records>0.0)] = 0.0
    mnw_ds2 = []
    names = []
    for id,r,c,top,bot,hydro in zip(ids,rows,cols,ztops,zbots,hydros):
        #--mnw 
        if hydro ==1:
            name = 'upper_'+str(id)
        else:
            name = 'lower_'+str(id)
        names.append(name)
        line_2a = '{0:20s}{1:10f}{2:>33s}\n'.format(name,-1,'#2a')
        mnw_ds2.append(line_2a)
        line_2b = '{0:20s}{1:10d}{2:10d}{3:10d}{4:10d} #2b\n'.format('THIEM',0,0,0,0)
        mnw_ds2.append(line_2b)
        line_2c = '{0:10.4f}{1:>53s}\n'.format(1.0,'#2c')
        mnw_ds2.append(line_2c)
        line_2d2 = ' {0:9.4f} {1:9.4f} {2:9.0f} {3:9.0f}{4:>26s}\n'.format(float(top),float(bot),int(float(r)),int(float(c)),'#2d-2\n')
        mnw_ds2.append(line_2d2) 

    f_mnw = open(grid.modelname+'.mnw','w',0)
    f_mnw.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    f_mnw.write(' {0:9.0f} {1:9.0f} {2:9.0f}\n'.format(len(ids),0,0))    
    for line in mnw_ds2:
        f_mnw.write(line)
    upper_layers = [3,4,5,6]
    lower_layers = [10,11,12,13,14,15,16,17,18]
    f_wel = open(grid.modelname+'.wel','w',0)
    f_wel.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
    f_wel.write(' {0:9.0f} {1:9.0f} {2:9.0f}\n'.format(300,0,0))    
    for i,slice in enumerate(well_records):
        lines = []
        for name,rate in zip(names,slice):
            lines.append('{0:20s}{1:15.4G}\n'.format(name,rate))
        f_mnw.write('{0:10d} {1:20s} {2:3d}\n'.format(len(lines),'#3 Stress Period',i+1))
        for line in lines:
            f_mnw.write(line)
        
        lines = []
        for name,rate,row,col in zip(names,slice,rows,cols):
            if 'upper' in name:
                layers = upper_layers
            else:
                layers = lower_layers
            rate /= float(len(layers))
            for lay in layers:
                line = '{0:10d}{1:10d}{2:10d}{3:15.4E}  #{4:20s}\n'\
                    .format(lay,int(float(row)),int(float(col)),rate,name)
                lines.append(line)
        f_wel.write('{0:10d}{1:10d} #{2:20s}{3:4d}\n'.format(len(lines),0,'stress period ',i+1))        
        for line in lines:
            f_wel.write(line)
    f_mnw.close()
    f_wel.close()

if __name__ == '__main__':
    write()
