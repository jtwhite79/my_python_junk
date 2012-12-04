import sys
import os 
import numpy as np
import shapefile
import pestUtil as pu

import bro

#--first load the k locs to get a mean value
pp_dir = 'k_locs\\'
pp_files = os.listdir(pp_dir)
ilayer = {}
for pfile in pp_files:
    data = np.loadtxt(pp_dir+pfile,usecols=[1,2,3,4])
    kmean = np.mean(np.log10(data[:,-1]))
    ilayer[pfile.split('.')[0]] = [pp_dir+pfile,kmean,data.shape[0]]
#pp_file = 'k_locs_bylayer.dat'

#kdata = np.loadtxt(pp_file,usecols=[1,2,3,4])

#--check for co-located
#uni_x = np.unique(kdata[:,0])
#uni_y = np.unique(kdata[:,1])
#for x in uni_x:
#    for y in uni_y:
#        locs = kdata[np.where(np.logical_and(kdata[:,0]==x,kdata[:,1]==y))]
#        if locs.shape[0] >1:
#            print

spc_file = '..\\_model\\bro.01\\broward_coarse.spc'
search = '1.0E+10'
ppk2fac_args = [spc_file,'kfile','0.0','zone.ref','f','struct_file','struct1','s',search,'1','numpts','layerX_fac.dat','f','layerX_stdev.ref','f','layerX_reg.dat']
fac2real_args = ['layerx_fac.dat','f','kfile','s','1.0e-10','s','1.0e+10','layerx_k.ref','f','-999']
#--for each unique layer with a data point, interpolate
refdir = 'ref\\'
facdir = 'fac\\'
strdir = 'structures\\'
indir = 'in\\'
outdir = 'out\\'
k_names,std_names = [],[]
for lname,[klocs_name,kmean,numpts] in ilayer.iteritems():
    print 'interpolating',lname
    str_name = strdir+lname+'.dat'    
    k_name = refdir+lname+'.ref'
    std_name = refdir+lname+'_stdev.dat'
    fac_name = facdir+lname+'_fac.dat'
    reg_name = facdir+lname+'_reg.dat'
    zone_name = refdir+'zone.ref'
    ppkin_name = indir+lname+'_ppk.in'
    facin_name = indir+lname+'_fac.in'
    ppkout_name = outdir+lname+'_ppk.out'
    facout_name = outdir+lname+'_fac.out'


    k_names.append(k_name)
    std_names.append(std_name)

    ##--write a structure file - parameters from linzy's miamidade struct3.dat
    #pu.write_structure(str_name,'struct1',nugget=0.0,transform='log',numvariogram=1,variogram_name='var1',sill=0.9843,vartype=2,bearing=0.0,a=16405.0,anisotropy=1.0,mean=kmean)
    ##--save a zone file
    #np.savetxt(zone_name,np.ones((bro.nrow,bro.ncol)),fmt=' %2.0f')

    ##k_name = refdir+'layer{0:02.0f}_k.ref'.format(lay)
    ##std_name = refdir+'layer{0:02.0f}_stdev.dat'.format(lay)
    ##fac_name = facdir+'layer{0:02.0f}_fac.dat'.format(lay)
    ##reg_name = facdir+'layer{0:02.0f}_reg.dat'.format(lay)
    #
    ##--run ppk2fac
    #ppk2fac_args[1] = klocs_name
    #ppk2fac_args[3] = zone_name
    #ppk2fac_args[5] = str_name
    #ppk2fac_args[10] = str(int(numpts))
    #ppk2fac_args[-5] = fac_name
    #ppk2fac_args[-3] = std_name
    #ppk2fac_args[-1] = reg_name
    #f = open(ppkin_name,'w')
    #line = '\n'.join(ppk2fac_args)
    #f.write(line)
    #f.close()
    #os.system('ppk2fac1.exe <'+ppkin_name+' >'+ppkout_name)
    #
    ##--run fac2real
    #fac2real_args[0] = fac_name
    #fac2real_args[2] = klocs_name
    #fac2real_args[-3] = k_name
    #args = '\n'.join(fac2real_args)
    #f = open(facin_name,'w')
    #f.write(args)
    #f.close()
    #os.system('fac2real.exe <'+facin_name+' >'+facout_name)
    ##break


#--add the interpolated K to the grid shapefile
shapename = '..\\_gis\\shapes\\broward_grid_master'
grid = shapefile.Reader(shapename)
names = shapefile.get_fieldnames(shapename,ignorecase=True)
row_idx,col_idx = names.index('ROW'),names.index('COLUMN')


#--load the k arrays
print 'loading k and std arrays'
k_arrays = []
for name in k_names:
    k = pu.load_wrapped_format(bro.nrow,bro.ncol,name)
    #np.savetxt(name,k,fmt=' %15.6E')
    k_arrays.append(k)
std_arrays = []
for name in std_names:
    std = pu.load_wrapped_format(bro.nrow,bro.ncol,name)
    #np.savetxt(name,std,fmt=' %15.6E')
    std_arrays.append(std)



print 'writing new grid shapefile'
wr = shapefile.writer_like(shapename)
for name in k_names:
    lname = name.split('.')[0].split('\\')[-1]
    wr.field(lname+'_K',fieldType='N',size=50,decimal=10)

#for name in std_names:
#    lname = name.split('.')[0].split('\\')[-1]
#    wr.field(lname+'_std',fieldType='N',size=50,decimal=10)


for i in range(grid.numRecords):
    print i,'of',grid.numRecords,'\r',
    shape = grid.shape(i)
    record = grid.record(i)
    r,c = record[row_idx],record[col_idx]
    for k in k_arrays:
        val = k[r-1,c-1]
        record.append(val)
    #for std in std_arrays:
    #    val = std[r-1,c-1]
    #    record.append(val)
    wr.poly([shape.points],shapeType=shape.shapeType)
    wr.record(record)
wr.save('..\\_gis\\scratch\\broward_grid_k')
