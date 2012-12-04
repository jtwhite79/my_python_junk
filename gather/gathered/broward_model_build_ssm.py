import sys
import os
from datetime import datetime
import numpy as np
import shapefile
from bro import flow,seawat
'''three point source sink types - GHBs, RIVs, WELs
   all WEL locs should be written to WEL file each sp
   hard coded rivers cells to layer 1
'''

def get_ssm_line(lay,row,col,conc,itype):
    return '{0:10.0f}{1:10.0f}{2:10.0f}{3:10.3G}{4:10.0f}\n'.format(lay,row,col,conc,itype)


sea_conc = 1.0
brackish_conc = 0.5
fresh_conc = 0.0


#--load the swr-output river package
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
    print kper
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
shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_swrpolylines'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames
riv_itype = 4
riv_lrcconc = {}
for r,c,strnum in zip(records['ROW'],records['COLUMN'],records['SRC_struct_']):
    #--tidal=brackish
    if strnum == -1:
        line = get_ssm_line(1,r,c,brackish_conc,riv_itype)
    #--fresh
    else:
        line = get_ssm_line(1,r,c,fresh_conc,riv_itype)
    riv_lrcconc[(r,c)] = line





#--load a list of GHB locs and concentrations
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
                                                                 


#--load a list of well locs
wel_lrcconc = []
wel_itype = 2
#--use one of the bndlist wel records
bnd_dir = seawat.list_dir
bnd_files = os.listdir(bnd_dir)
for wel_file in bnd_files:
    if 'WEL' in wel_file.upper():
        break
wel_array = np.loadtxt(bnd_dir+wel_file,usecols=[0,1,2])
for [lay,row,col] in wel_array:
    line = get_ssm_line(lay,row,col,fresh_conc,wel_itype)
    wel_lrcconc.append(line)


mxact_ghb = len(ghb_lrcconc)
mxact_wel = len(wel_lrcconc)

mxss = mxact_ghb + mxact_riv + mxact_wel
f_ssm = open(seawat.root+'.ssm','w',0)
#f_ssm.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
flags = ['T','F','T','T','T','T','F','F','F','F']
for f in flags:
    f_ssm.write('{0:2}'.format(f))
f_ssm.write('\n{0:10.0f}\n'.format(mxss))

for i,start in enumerate(flow.sp_start):
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
    mxss = mxact_ghb + mxact_wel + len(riv_act)
    f_ssm.write('{0:10.0f}\n'.format(mxss))
    for line in ghb_lrcconc:
        f_ssm.write(line)
    #for line in riv_lrcconc:
    for rc_tup in riv_act:
        f_ssm.write(riv_lrcconc[rc_tup])
    for line in wel_lrcconc:
        f_ssm.write(line)

f_ssm.close()