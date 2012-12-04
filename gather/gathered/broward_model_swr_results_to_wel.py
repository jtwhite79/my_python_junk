import os
import sys
from datetime import datetime,timedelta
import numpy as np
import MFBinaryClass as mfb

import bro
'''assigns all of the flow from the reach to the cell in layer 1
'''
lay = 1

#--get reach row,col from datasets 4a - faster than shapefile
ds4a_file = 'swrref\\ds_4a.dat'
reach_rowcol = np.loadtxt(ds4a_file,skiprows=2,usecols=[0,2,4,5])
#--build into a dict - faster
unique_rgnum = np.unique(reach_rowcol[:,1])
rgnum_info = {}
for u in unique_rgnum:
    if u == 2243:
        pass
    rec_rowcol = reach_rowcol[np.where(reach_rowcol[:,1]==u)]
    rgnum_info[u] = rec_rowcol[:,[0,2,3]]
    #for reach,rgnum,row,col in rec_rowcol:



#--build a dict of external wel lists
bnd_dir = 'bndlist\\'
bnd_files = os.listdir(bnd_dir)
wel_bnds = {}
for f in bnd_files:
    if 'wel' in f:
        #--parse the datetime
        dt_string = f.split('.')[0].split('_')[-1]
        dt = datetime.strptime(dt_string,'%Y%m%d')
        lines = []
        f = open(bnd_dir+f,'r')
        for line in f:
            lines.append(line)
        f.close()
        wel_bnds[dt] = lines

#--get baseflow from each reach
fls_file = bro.modelname+'.fls'
fls_obj = mfb.SWR_Record(-1,fls_file)
fls_items = fls_obj.get_item_list()
bf_idx = 6
sp_num = 1

#--for writing the external wel lists
bnd_prefix = 'bndlist\\bro_welswr_'

f_wel = open(bro.seawatname+'.wel','w',0)
f_wel.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
f_wel.write('# combined pumpage and swr qbflow\n')
#--write a guess of mxact
f_wel.write(' {0:9.0f} {1:9.0f} {2}\n'.format(20000,0,'NOPRINT'))
tot_vol_record = []
while True:

    totim,length,kper,kstp,swrstp,success,records = fls_obj.next()
    if not success: break
    if kstp != 1:
        raise Exception('no support for more than one timestep..')
    
    td = timedelta(days=totim-1)
    end = bro.start + td
    start = bro.sp_start[kper-1]
    length = bro.sp_len[kper-1]
    print kper,start
    lines = wel_bnds[start]
    tot_vol = 0.0
    for i,rec in enumerate(records):
        qb_rg = -1.0 * rec[bf_idx]
        if i == 2243:
            pass
        if qb_rg != 0.0:
            rchrowcol = rgnum_info[i+1]
            qb_reach = qb_rg / (rchrowcol.shape[0])
            
            for rch,row,col in rchrowcol:
                tot_vol += qb_reach
                line = ' {0:9.0f} {1:9.0f} {2:9.0f} {3:20.8E} {4:9s}{5:6.0f}{6:8s}{7:6.0f}\n'.format(lay,row,col,qb_reach,' # reach ',rch,' rchgrp ',i+1)
                lines.append(line)
    f_wel.write(' {0:9.0f} {1:9.0f} '.format(len(lines),0)+'  # Stress Period '+str(kper)+' '+start.strftime('%Y%m%d')+'\n')    
    bnd_name = bnd_prefix+start.strftime('%Y%m%d')+'.dat'
    f_wel.write('OPEN/CLOSE '+bnd_name+' \n')
    f_bnd = open(bnd_name,'w',0)
    for line in lines:
        f_bnd.write(line)
    f_bnd.close()  
    tot_vol_record.append([kper,tot_vol])          
tot_vol_record = np.array(tot_vol_record)
np.savetxt('tot_vol_record.dat',tot_vol_record,fmt='%4.0f %20.8G')


