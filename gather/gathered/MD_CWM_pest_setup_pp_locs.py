import os
import numpy as np
from shapely.geometry import Polygon
import shapefile
import pestUtil


#--load the grid info
gridname = 'grid.spc'
grid_info = pestUtil.load_grid_spec(gridname)

row_centers = np.flipud(grid_info['yoffset'] + np.cumsum(grid_info['delc']) - (grid_info['delc'] / 2.0))
col_centers = (grid_info['xoffset'] + np.cumsum(grid_info['delr']) - (grid_info['delr'] / 2.0))

#--write the crappy settings file
f = open('settings.fig','w')
f.write('date=dd/mm/yyyy\ncolrow=no\n')
f.close()


#--build the ibound from the grid shape
shapename = '..\\shapes\\CWM_01_grid_processed'
records = shapefile.load_as_dict(shapename,loadShapes=False)
ibound = np.zeros((grid_info['nrow'],grid_info['ncol'])) + np.NaN
for row,col,ibnd in zip(records['row'],records['column'],records['ibound']):
    ibound[row-1,col-1] = ibnd
ibound_interp = ibound.copy()
ibound_interp[np.where(np.logical_or(ibound==3,ibound==4))] = 1
np.savetxt('ibound_interp.ref',ibound_interp,fmt='%3.0f')


#--setup pilot point locations
pp_cell_space = 3
pp_locs = []
pp_num = 1
for i,rc in enumerate(row_centers):
    for j,cc in enumerate(col_centers):
        if ibound [i,j] > 0 and ibound[i,j] != 2:
            if ibound[i,j] == 1 and i % pp_cell_space == 0 and j % pp_cell_space == 0:
                pp_locs.append([pp_num,cc,rc,1,0.0])
                pp_num += 1            
            elif ibound[i,j] == 3 and i % (pp_cell_space*2) == 0 and j % (pp_cell_space*2) == 0:
                pp_locs.append([pp_num,cc,rc,1,0.0])
                pp_num += 1
            elif ibound[i,j] == 4 and i % (pp_cell_space*2) == 0 and j % (pp_cell_space*2) == 0:
                pp_locs.append([pp_num,cc,rc,1,0.0])
                pp_num += 1
pp_locs = np.array(pp_locs)
np.savetxt('pp_locs.dat',pp_locs,fmt='pp%04.0f %15.6e %15.6e %10.0f %10.3f')  
    
wr = shapefile.Writer()
wr.field('name',fieldType='C',size=20)
wr.field('x',fieldType='N',size=20,decimal=4)
wr.field('y',fieldType='N',size=20,decimal=4)
for [pp_num,x,y,zone,val] in pp_locs:
    wr.poly([[[x,y]]],shapeType=shapefile.POINT)
    wr.record(['pp{0:04.0f}'.format(pp_num),x,y])
wr.save('shapes\\pp_locs')

#--structure parameters
s = {}
s['STRUCTNAME'] = 'struct1'
s['NUGGET'] = '0.0'
s['TRANSFORM'] = 'log'
s['NUMVARIOGRAM'] = '1'
s['VAR1'] = {'CONTRIBUTION':'1.0','VARNAME':'var1','VARTYPE':'1','BEARING':'0.0','A':'1500.0','ANISOTROPY':'1.0'}
pestUtil.write_structure_from_dict('pp_struct.dat','struct1',s)

#--run ppk2fac
args = ['grid.spc','pp_locs.dat','0.0','ibound_interp.ref','f','pp_struct.dat','','struct1','o','5000.0','1','5','','','','pp_fac.dat','f','pp_stdev.ref','pp_reg.dat']
f = open('ppk2fac1.in','w')
f.write('\n'.join(args))
f.close()
os.system('ppk2fac1.exe <ppk2fac1.in')

#--load the stdev array
stdev = pestUtil.load_wrapped_format(grid_info['nrow'],grid_info['ncol'],'pp_stdev.ref')

#--add the stdev array to the grid shapefile
shp = shapefile.Reader(shapename)
shapes,records = shp.shapes(),shp.records()

wr = shapefile.writer_like(shapename)
wr.field('stdev',fieldType='N',size=20,decimal=5)
header = shp.dbfHeader()
row_idx,col_idx = None,None
for i,item in enumerate(header):
    if item[0] == 'row':
        row_idx = i
    elif item[0] == 'column':
        col_idx = i
        
for shape,record in zip(shapes,records):
    r,c = record[row_idx],record[col_idx]
    sd = stdev[r-1,c-1]
    wr.poly([shape.points],shapeType=shape.shapeType)
    record.append(sd)
    wr.record(record)
wr.save('shapes\\grid_stdev')


