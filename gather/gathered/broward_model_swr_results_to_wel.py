import os
import sys
from datetime import datetime,timedelta
import numpy as np
import shapefile
import MFBinaryClass as mfb

from bro import flow,seawat
'''assigns all of the flow from the reach to the cell in layer 1
writes concentration comments to the bnd list
'''
lay = 1

#--get row-col-lay (seawat) for each reach group (flow)
#--get reach row,col from datasets 4a - faster than shapefile
ds4a_file = flow.ref_dir+'swr\\ds_4a.dat'
reach_rowcol = np.loadtxt(ds4a_file,skiprows=2,usecols=[0,2,4,5])
#--build into a dict - faster
unique_rgnum = np.unique(reach_rowcol[:,1])
rgnum_info = {}

for u in unique_rgnum:
    rec_rowcol = reach_rowcol[np.where(reach_rowcol[:,1]==u)]
    rgnum_info[u] = rec_rowcol[:,[0,2,3]]
rch_info = {}
rch_nums = []
for reach,row,col in reach_rowcol[:,[0,2,3]]:
    rch_info[reach] = (row,col)
    rch_nums.append(reach)

#--build a dict of external wel lists for the flow model for testing
bnd_dir = flow.list_dir
bnd_files = os.listdir(bnd_dir)
wel_bnds_flow = {}
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
        wel_bnds_flow[dt] = lines

#--build a dict of external wel lists for the seawat model
bnd_dir = seawat.list_dir
bnd_files = os.listdir(bnd_dir)
wel_bnds_seawat = {}
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
        wel_bnds_seawat[dt] = lines

#aq_file = flow.root+'.aqx'
#aq_obj = mfb.SWR_Record(flow.nlay,aq_file)

#--get baseflow from each reach
#fls_file = flow.root+'.fls'
#fls_obj = mfb.SWR_Record(-1,fls_file)
#fls_items = fls_obj.get_item_list()
#bf_idx = 6
sp_num = 1

cbc_file = flow.root+'_swr.cbc'
cbc_obj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,cbc_file)
flux_type = '     SWR LEAKAGE'



#--for writing the external wel lists
bnd_prefix_seawat = seawat.list_dir+'\\welswr_'
bnd_prefix_flow = flow.list_dir+'\\welswr_'

f_wel_seawat = open(seawat.root+'_swr.wel','w',0)
f_wel_seawat.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
f_wel_seawat.write('# combined pumpage and swr qbflow\n')
#--write a guess of mxact
f_wel_seawat.write(' {0:9.0f} {1:9.0f} {2}\n'.format(20000,seawat.well_unit,'NOPRINT'))

f_wel_flow = open(flow.root+'_swr.wel','w',0)
f_wel_flow.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
f_wel_flow.write('# combined pumpage and swr qbflow\n')
#--write a guess of mxact
f_wel_flow.write(' {0:9.0f} {1:9.0f} {2}\n'.format(20000,flow.well_unit,'NOPRINT'))

tot_vol_record = []
kper = 1
while True:

    #totim,length,kper,kstp,swrstp,success,records = fls_obj.next()
    #totim,length,kper,kstp,swrstp,success,records = aq_obj.next()
    flux,totim,success = cbc_obj.read_next_fluxtype(flux_type)
    if not success: break    
    
    td = timedelta(days=totim-1)
    end = flow.start + td
    start = flow.sp_start[kper-1]
    length = flow.sp_len[kper-1]
    print kper,start,np.cumsum(flux)[-1]
    lines_seawat = wel_bnds_seawat[start]
    lines_flow = wel_bnds_flow[start]
    tot_vol = 0.0
                                    
    kper += 1   
    visited = []
    for rch in rch_nums:        
        row,col = rch_info[rch]
        if (row-1,col-1) not in visited:
            visited.append((row-1,col-1))
            qb_reach = flux[0,row-1,col-1]
            tot_vol += qb_reach
            line = ' {0:9.0f} {1:9.0f} {2:9.0f} {3:20.8E} {4:9s}{5:6.0f}\n'.format(lay,row,col,qb_reach,' # reach ',rch)
            lines_seawat.append(line)
            lines_flow.append(line)
            
    #for i,rec in enumerate(records):    
        #rch,qb_reach = rec[0],rec[-1]
        #tot_vol += qb_reach
        #row,col = rch_info[rch]
        #line = ' {0:9.0f} {1:9.0f} {2:9.0f} {3:20.8E} {4:9s}{5:6.0f}\n'.format(lay,row,col,qb_reach,' # reach ',rch)
        #lines_seawat.append(line)
        #lines_flow.append(line)


        #qb_rg = -1.0 * rec[bf_idx]        
        #if qb_rg != 0.0:
        #    rchrowcol = rgnum_info[i+1]
        #    qb_reach = qb_rg / (rchrowcol.shape[0])
            
        #    for rch,row,col in rchrowcol:
        #        tot_vol += qb_reach
        #        line = ' {0:9.0f} {1:9.0f} {2:9.0f} {3:20.8E} {4:9s}{5:6.0f}{6:8s}{7:6.0f}\n'.format(lay,row,col,qb_reach,' # reach ',rch,' rchgrp ',i+1)
        #        lines_seawat.append(line)
        #        lines_flow.append(line)
    f_wel_seawat.write(' {0:9.0f} {1:9.0f} '.format(len(lines_seawat),0)+'  # Stress Period '+str(kper)+' '+start.strftime('%Y%m%d')+'\n')    
    f_wel_flow.write(' {0:9.0f} {1:9.0f} '.format(len(lines_flow),0)+'  # Stress Period '+str(kper)+' '+start.strftime('%Y%m%d')+'\n')    
    bnd_name_seawat = bnd_prefix_seawat+start.strftime('%Y%m%d')+'.dat'
    bnd_name_flow = bnd_prefix_flow+start.strftime('%Y%m%d')+'.dat'
    f_wel_seawat.write('OPEN/CLOSE '+bnd_name_seawat+' \n')
    f_wel_flow.write('OPEN/CLOSE '+bnd_name_flow+' \n')
    f_bnd_seawat = open(bnd_name_seawat,'w',0)
    for line in lines_seawat:
        f_bnd_seawat.write(line)
    f_bnd_seawat.close()  
    f_bnd_flow = open(bnd_name_flow,'w',0)
    for line in lines_flow:
        f_bnd_flow.write(line)
    f_bnd_flow.close()  
    tot_vol_record.append([kper,tot_vol])       
tot_vol_record = np.array(tot_vol_record)
print tot_vol_record.shape
np.savetxt('tot_vol_record.dat',tot_vol_record,fmt='%4.0f %20.8G')



