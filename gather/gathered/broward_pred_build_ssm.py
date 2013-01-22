import sys
import os
from datetime import datetime
import numpy as np
import shapefile
from bro_pred import flow,seawat
'''three point source sink types - GHBs, RIVs, WELs
   hard coded rivers cells to layer 1
'''

def get_ssm_line(lay,row,col,conc,itype):
    return '{0:10.0f}{1:10.0f}{2:10.0f}{3:10.3G}{4:10.0f}\n'.format(lay,row,col,conc,itype)


sea_conc = 1.0
brackish_conc = 0.5
fresh_conc = 0.0


#--load a list of RIV locs and concentrtaions
#--into a dict that is keyed in the row-col tuple
f = open('..\\..\\_BCDPEP\\BCDPEP_reach_conc.dat','r')
f.readline()
tidal_conc = {}
for line in f:
    raw = line.strip().split(',')
    tidal_conc[int(raw[0])] = float(raw[1])
f.close()
print 'loading swr reach - concentration info'
shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_swrpolylines_2'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames

swr_conc = {}
#for r,c,strnum in zip(records['ROW'],records['COLUMN'],records['SRC_struct']):
for reach,strnum,source_reach in zip(records['REACH'],records['SRC_struct'],records['SRC_reach']):
    #--tidal=brackish
    if strnum == -1:
        swr_conc[reach] = tidal_conc[source_reach]
        #swr_conc[reach] = brackish_conc
    #--fresh
    else:
        swr_conc[reach] = fresh_conc

print 'loading SWR-output river info'
riv_filename = flow.root+'.riv'
f = open(riv_filename,'r')
while True:
    line = f.readline()
    if not line.strip().startswith('#'):
        break
mxact_riv = int(line.split()[0])
#--start sp loop
kper = 1
riv_sp = {}
while True:
    #print kper
    line = f.readline()
    if line == '':
        break
    sp_act = int(line.split()[0])
    active = []
    for i in range(sp_act):
        line = f.readline()
        raw = line.strip().split()
        r = int(raw[1])
        c = int(raw[2])
        active.append((r,c))
    riv_sp[kper] = active
    kper += 1


#--load a list of RIV locs and concentrtaions
#--into a dict that is keyed in the row-col tuple
shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_swrpolylines_2'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames
riv_itype = 4
riv_lrcconc = {}
riv_lrcconc_fresh = {}
for r,c,reach in zip(records['ROW'],records['COLUMN'],records['REACH']):
    line = get_ssm_line(1,r,c,swr_conc[reach],riv_itype)
    riv_lrcconc[(r,c)] = line
    line = get_ssm_line(1,r,c,0.0,riv_itype)
    riv_lrcconc_fresh[(r,c)] = line
    


#--load a list of well locs
print 'loading well info'
wel_lrcconc = []
wel_itype = 2
#--use one of the bndlist wel records
bnd_dir = seawat.list_dir
bnd_files = os.listdir(bnd_dir)
bnd_str = 'WEL'
#wel_sp = {}
wel_month = {}
mxact_wel = None
for bfile in bnd_files:
    if bnd_str in bfile.upper():
        #dt_str = bfile.split('.')[0].split('_')[-1]
        #print dt_str,'\r',
        #dt = datetime.strptime(dt_str,'%Y%m%d')
        #kper = list(seawat.sp_start).index(dt) + 1
        month = int(bfile.split('.')[0].split('_')[1])
        print month,'\r',
        wel_array = np.loadtxt(bnd_dir+bfile,usecols=[0,1,2])
        active = []
        
        for [lay,row,col] in wel_array:
            line = get_ssm_line(lay,row,col,fresh_conc,wel_itype)
            active.append(line)
                                
        #wel_sp[kper] = active
        wel_month[month] = active
        mxact_wel = max(mxact_wel,len(active))


#--load a list of GHB locs and concentrations
print 'loading ghb info'
ghb_itype = 5
sea_val,brackish_val = 2,5
ghb_lrcconc = []
for i in range(flow.nrow):
    for j in range(flow.ncol):
        ib_val = flow.ibound[i,j]
        if ib_val > 1:
            if ib_val == sea_val:
                conc = sea_conc
            elif ib_val == brackish_val:
                conc = brackish_conc
            else:
                conc = fresh_conc
            for lay in seawat.ghb_layers:
                line = get_ssm_line(lay,i+1,j+1,conc,ghb_itype)
                ghb_lrcconc.append(line)
                                                                 
print 'writing ssm file'                
mxact_ghb = len(ghb_lrcconc)

mxss = mxact_ghb + mxact_wel + mxact_riv 
#mxss = mxact_ghb + mxact_wel
f_ssm = open(seawat.root+'.ssm','w',0)
#f_ssm.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
flags = ['T','F','T','T','T','T','F','F','F','F']
#flags = ['T','F','T','F','T','T','F','F','F','F']
for f in flags:
    f_ssm.write('{0:2}'.format(f))
f_ssm.write('\n{0:10.0f}\n'.format(mxss))

for i,start in enumerate(flow.sp_start):
    print 'writing sp',i+1,' ',start
    if i == 0:
        #--incrch,crch=0
        f_ssm.write('{0:10.0f}\n'.format(1))
        f_ssm.write('{0:10.0f}{1:10.1f}{2:>20}{3:10.0f}\n'.format(0,0.0,'FREE',0))
        #--incevt,cevt=0
        f_ssm.write('{0:10.0f}\n'.format(1))
        f_ssm.write('{0:10.0f}{1:10.1f}{2:>20}{3:10.0f}\n'.format(0,0.0,'FREE',0))
    else:
        f_ssm.write('{0:10.0f}\n{1:10.0f}\n'.format(-1,-1))

    #--point sources/sinks
    riv_act = riv_sp[i+1]
    #wel_lines = wel_sp[i+1]
    wel_lines = wel_month[start.month]
    mxss = mxact_ghb + len(wel_lines) + len(riv_act)
    #mxss = mxact_ghb + len(wel_lines)
    f_ssm.write('{0:10.0f}\n'.format(mxss))
    for line in ghb_lrcconc:
        f_ssm.write(line)
    #if start.month in [6,7,8,9,10]:
    #    for rc_tup in riv_act:
    #        f_ssm.write(riv_lrcconc[rc_tup])
    #else:
    for rc_tup in riv_act:
        f_ssm.write(riv_lrcconc_fresh[rc_tup])
    for line in wel_lines:
        f_ssm.write(line)

f_ssm.close()
