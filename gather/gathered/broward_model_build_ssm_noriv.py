import sys
import os
from datetime import datetime
import numpy as np
import shapefile
from bro import flow,seawat
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
print 'loading swr reach - concentration info'
shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_swrpolylines_2'
records = shapefile.load_as_dict(shapename,loadShapes=False)
fnames = shapefile.get_fieldnames(shapename)
#print fnames
swr_conc = {}
#for r,c,strnum in zip(records['ROW'],records['COLUMN'],records['SRC_struct']):
for reach,strnum in zip(records['REACH'],records['SRC_struct']):
    #--tidal=brackish
    if strnum == -1:
        swr_conc[reach] = brackish_conc
    #--fresh
    else:
        swr_conc[reach] = fresh_conc

#--load a list of well locs
print 'loading well info'
wel_lrcconc = []
wel_itype = 2
#--use one of the bndlist wel records
bnd_dir = seawat.list_dir
bnd_files = os.listdir(bnd_dir)

bnd_str = 'WELSWR'
wel_sp = {}
mxact_wel = None
for bfile in bnd_files:
    if bnd_str in bfile.upper():
        dt_str = bfile.split('.')[0].split('_')[-1]
        print dt_str,'\r',
        dt = datetime.strptime(dt_str,'%Y%m%d')
        kper = list(seawat.sp_start).index(dt) + 1
        wel_array = np.loadtxt(bnd_dir+bfile,usecols=[0,1,2])
        active = []        
        f = open(bnd_dir+bfile,'r')
        for i,line in enumerate(f):
            lay,row,col = wel_array[i,:]
            if 'REACH' in line.upper():
                #--find reach number
                reach = int(line.upper().split('REACH')[-1].split()[0])
                ssmline = get_ssm_line(lay,row,col,swr_conc[reach],wel_itype)
                active.append(ssmline)
            else:
                ssmline = get_ssm_line(lay,row,col,fresh_conc,wel_itype)
        wel_sp[kper] = active
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

mxss = mxact_ghb + mxact_wel
f_ssm = open(seawat.root+'.ssm','w',0)
#f_ssm.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
flags = ['T','F','T','T','F','T','F','F','F','F']

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
    wel_lines = wel_sp[i+1]
    mxss = mxact_ghb + len(wel_lines)
    f_ssm.write('{0:10.0f}\n'.format(mxss))
    for line in ghb_lrcconc:
        f_ssm.write(line)    
    for line in wel_lines:
        f_ssm.write(line)

f_ssm.close()
