import sys
import os
import re
import numpy as np
import shapefile
import arrayUtil

def loadtxt(nrow,ncol,file,dtype='float'):
	'''
	read 2darray from file
	file(str) = path and filename
	'''
	try:
		file_in = open(file,'r')
		openFlag = True
	except:
		assert os.path.exists(file)
		file_in = file
		openFlag = False
	
	data = np.zeros((nrow*ncol),dtype=dtype)-1.0E+10
	d = 0
	while True:
		line = file_in.readline()
		if line is None or d == nrow*ncol:break
		raw = line.strip('\n').split()
		for a in raw:
			try:
				data[d] = float(a)
			except:
				print 'error casting to float on line: ',line
				sys.exit()
			if d == (nrow*ncol)-1:
				assert len(data) == (nrow*ncol)
				data.resize(nrow,ncol)
				file_in.close()
				return np.flipud(data) 
			d += 1	
	file_in.close()
	data.resize(nrow,ncol)
	
	return data


#nrow,ncol = 189,101
nrow,ncol = 411,501

#--get a list of the smp files
sdir = 'smp\\'
smp_files = os.listdir(sdir)

#--get a list of the structures names
struct_file = 'pest_structures.dat'
f = open(struct_file,'r')
struct_names = []
for line in f:
    if re.match('STRUCTURE',line) is not None:
        s_name = line.strip().split()[-1]
        struct_names.append(s_name)
f.close()

#--for each smp file, krige for all associated structures
odir = 'output\\'
arrays = {}
for smp in smp_files:
    #--find associated structures
    prefix = smp.split('_')[1]
    structs = []
    for struct in struct_names:
        if struct.startswith(prefix):
            structs.append(struct)
    
    for s in structs:
        #--run ppk2fac
        #f = open('temp.in','w')
        ##f.write('md_cwm.grd\n')
        #f.write('bro.grd\n')
        #f.write(sdir+smp+'\n')
        #f.write('0.0\n')
        ##f.write('zone_md.ref\nf\n')
        #f.write('zone_bro.ref\nf\n')
        #f.write('pest_structures.dat\n')
        #f.write(s+'\n')
        #f.write('o\n1500000\n1\n100\n')
        #f.write(odir+s+'.fac\nf\n')
        #f.write(odir+s+'.stdev\nf\n')
        #f.write(odir+s+'.reg\n')
        #f.close()
        #os.system('ppk2fac.exe <temp.in')

        ##--run fac2real
        #f = open('temp.in','w')
        #f.write(odir+s+'.fac\nf\n')
        #f.write(sdir+smp+'\n')
        #f.write('s\n0.0\n')
        #f.write('s\n1.0e+10\n')
        #f.write(odir+s+'.ref\n')
        #f.write('-999\n')
        #f.close()
        #os.system('fac2real.exe <temp.in')

        #--load the array - warpped format - crap!
        arr = np.flipud(loadtxt(nrow,ncol,odir+s+'.ref'))
        np.savetxt(odir+s+'_unwrap.ref',arr,fmt='%16.7e')
        arrays[s] = arr.copy()
        #break
    #break
        #print arr[0,0]
        #print    


#--write the results to the grid shapefile
#shp = shapefile.Reader('D:\Users\jwhite\Projects\MiamiDade\_CWM\shapes\CWM_01_grid_processed')
shp = shapefile.Reader(r'D:\Users\jwhite\Projects\Broward\_gis\shapes\broward_grid_ibound')
header = shp.dbfHeader()
records = shp.records()
shapes = shp.shapes()

wr = shapefile.Writer()
row_idx,col_idx = None,None
for i,item in enumerate(header):
    wr.field(item[0],fieldType=item[1],size=item[2],decimal=item[3])
    if item[0] == 'row':
        row_idx = i
    elif item[0] == 'column':
        col_idx = i    
anames = []
for key in arrays.keys():
    wr.field(key,fieldType='N',size=20,decimal=6)
    anames.append(key)


for rec,shape in zip(records,shapes): 
    r,c = rec[row_idx],rec[col_idx]
    for a in anames:
        val = arrays[a][r-1,c-1]
        rec.append(val)
    wr.poly([shape.points],shapeType=shapefile.POLYGON)
    wr.record(rec)
wr.save(r'D:\Users\jwhite\Projects\Broward\_gis\shapes\broward_grid_strat')                    
    
    