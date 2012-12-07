import os
import shutil

from bro import seawat,flow

f = open('settings.fig','w',0)
f.write('date=dd/mm/yyy\ncolrow=no\n')
f.close()


source_smp_files = ['..\\_nwis\\navd_cali.smp','..\\_nwis\\relconc_cali.smp','..\\_ftl_salt\\ftl_cali.smp']
source_bc_files = ['..\\_nwis\\nwis_navd_bore_coords.dat','..\\_nwis\\nwis_conc_bore_coords.dat','..\\_ftl_salt\\ftl_borecoords.dat']

smp_dir = 'smp\\obs\\'
bc_dir = 'bore_coords\\'

smp_files = []
for ssmp in source_smp_files:
    smp = ssmp.split('\\')[-1]
    shutil.copy(ssmp,smp_dir+smp)
    smp_files.append(smp_dir+smp)

bc_files = []
for sbc in source_bc_files:
    bc = sbc.split('\\')[-1]
    shutil.copy(sbc,bc_dir+bc)
    bc_files.append(bc_dir+bc)

mod_files = [flow.dir+flow.root+'.hds',seawat.dir+'MT3D001.UCN',seawat.dir+'MT3D001.UCN']
mod_types = ['f','t','t']
grid_files = ['grid\\'+flow.root+'.spc','grid\\'+seawat.root+'.spc','grid\\'+seawat.root+'.spc']
nlays = [str(flow.nlay),str(seawat.nlay),str(seawat.nlay)]
in_files = ['navd.in','nwis_conc.in','ftl_salt.in']
out_dir = 'smp\\mod\\'
out_files = ['navd_cali.smp','relconc_cali.smp','ftl_cali.smp']
mod_inact = '1.0e+10'
mod_time = 'd'
mod_start = flow.start.strftime('%d/%m/%Y')
mod_extrap_lim = '3200' #days


for smp,bc,mfile,mtype,ifile,gfile,nlay,ofile in zip(smp_files,bc_files,mod_files,mod_types,in_files,grid_files,nlays,out_files):
    f = open('mod2obs_'+ifile,'w',0)
    f.write(gfile+'\n')
    f.write(bc+'\n')
    f.write(bc+'\n')
    f.write(smp+'\n')
    f.write(mfile+'\n')
    f.write(mtype+'\n')
    f.write(mod_inact+'\n')
    f.write(mod_time+'\n')
    f.write(mod_start+'\n')
    f.write('00:00:00\n')
    f.write(nlay+'\n')
    f.write(mod_extrap_lim+'\n')
    f.write(out_dir+ofile+'\n')
    f.close()
    os.system('mod2obs.exe <mod2obs_'+ifile)