import sys
import shutil
import os
from datetime import datetime
from simple import grid

'''
prior to pest run: map arrays and map bcs

load simple parameter values to determine which nam file and mod2obs infile to use
if surfwater: convert ds6 to all specified, otherwise write ds6 as dynamic
run fac2real sequence
run apply_bc_factors
run thk2botm

'''

def setup():
    #--copy all of the nesscary scripts out of the project subdirs into the root dir

    pass




start = datetime.now()

#--open a log file
f_log = open('forward_run.log','w')
f_log.write(str(start)+' - starting forward run\n\n')

#--try to import python utilities needed to prepare for run
f_log.write(str(datetime.now())+' - import python utilities...\n')
try:
    import simplification_fac2real as f2r
    import simplification_apply_bc_factors as abf
    import simplification_thk2botm as t2b
except Exception as e:
    f_log.write('ERROR -- cannot import python fac2real\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise    
f_log.write(str(datetime.now())+' - done\n\n')  

#--try to load simple parameter values
f_log.write(str(datetime.now())+' - read par\\simple.dat...\n')
try:
    f = open('par\\simple.dat','r')
    simple = {}
    for line in f:
        raw = line.strip().split()
        simple[raw[0]] = float(raw[1])
    f.close()         
except Exception as e:
    f_log.write('ERROR -- cannot read par\\simple.dat\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise    
f_log.write(str(datetime.now())+' - done\n\n')  

 
f_log.write(str(datetime.now())+' - removing model files...\n')
rm_list = ['_model\\swr_ds6.dat','_model\\simple.hds','_model\\simple_rc.hds']
rm_list.append('_model\\simple.wel')
rm_list.append('_model\\simple.ghb')
for hydro in ['upper','lower','middle']:
    for ptype in ['k','thk_frac','ss','sy']:
        rm_list.append('_model\\ref\\'+hydro+'_'+ptype+'.ref')
for k in range(grid.nlay):
    rm_list.append('_model\\ref\\mod\\botm_Layer_'+str(k+1)+'.ref')
for fname in rm_list:
    try:
        os.remove(fname)
        f_log.write(' -- removed modelfile: '+str(fname)+'\n')
    except Exception as e:
        f_log.write(' -- unable to remove modelfile: '+str(fname)+'\n')
        f_log.write(str(e)+'\n')
f_log.write(str(datetime.now())+' - done\n\n')

f_log.write(str(datetime.now())+' - using fac2real to write property arrays...\n')
try:
    os.chdir('_model\\')
    f2r.apply()
    os.chdir('..\\')
except Exception as e:
    f_log.write('ERROR -- cannot run fac2real for property arrays\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise     
f_log.write(str(datetime.now())+' - done\n\n')

f_log.write(str(datetime.now())+' - applying bc factors...\n')
try:
    abf.apply('simple','_misc\\ghb_locs.csv','_misc\\well_locs.csv')
except Exception as e:
    f_log.write('ERROR -- cannot run apply_bc_factors for property arrays\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise     
f_log.write(str(datetime.now())+' - done\n\n')


f_log.write(str(datetime.now())+' - copying dataset 6...\n')
try:
    if simple['surfwat'] == 1:
        shutil.copy('base\\swr_ds6_dynamic.dat','_model\\swr_ds6.dat')
    else:
        shutil.copy('base\\swr_ds6_constant.dat','_model\\swr_ds6.dat')
except Exception as e:
    f_log.write('ERROR -- cannot copy dataset 6\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise   
        
f_log.write(str(datetime.now())+' - building botm from thk...\n')
try:
    t2b.apply()
except Exception as e:
    f_log.write('ERROR -- cannot run thk2botm\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise   


#--run MODFLOW
f_log.write(str(datetime.now())+' - starting modflow...\n')
try:
    if simple['rowcol'] != 1.0:
        name_file = 'simple_rc.nam'
    elif simple['layer'] != 1.0:
        name_file = 'simple_l.nam'
    else:
        name_file = 'simple.nam'
    print name_file
    os.chdir('_model\\')
    os.system('MD_mfnwt_x64.exe ' + name_file)   
except Exception as e:
    f_log.write('ERROR -- cannot run modflow\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise         
f_log.write(str(datetime.now())+' - done\n\n')

#--mod2obs
try:
    if simple['rowcol'] != 1.0:
        in_file = 'mod2obs_rc.in'
    elif simple['layer'] != 1.0:
        in_file = 'mod2obs_l.in'
    else:
        in_file = 'mod2obs.in'

    
    os.chdir('..\\')
    os.system('mod2obs.exe <' + in_file)
    #sp.Popen(['mod2obs.exe','mod2obs.in'])
except Exception as e:
    f_log.write('ERROR -- cannot run mod2obs\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise         
f_log.write(str(datetime.now())+' - done\n\n')

#--postprocessing with tsproc
try:
    os.system('tsproc.exe <tsproc_model_run.in')
    #sp.Popen(['tsproc.exe','tsproc_model_run.in'])
except Exception as e:
    f_log.write('ERROR -- cannot run tsproc\n')
    f_log.write(str(e)+'\n')
    f_log.close()
    raise         
f_log.write(str(datetime.now())+' - done\n\n')

f_log.close()