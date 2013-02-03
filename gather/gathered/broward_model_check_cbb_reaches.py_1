import copy
from datetime import datetime,timedelta
import numpy as np
import pylab
import pandas
import shapefile
import MFBinaryClass as mfb

from bro import flow

shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_SWRpolylines_2'
records = shapefile.load_as_dict(shapename,loadShapes=False)
rc_tups = {}
rch_cbc,rch_aqx = {},{}
rch_init = {}
for r,c,rch,rchgrp in zip(records['ROW'],records['COLUMN'],records['REACH'],records['RCH_GRP']):
    rc_tup = (r,c)
    rc_tups[rch] = rc_tup
    rch_cbc[rc_tup] = []
    rch_aqx[rc_tup] = []
    rch_init[rc_tup] = 0.0


cbc_file = flow.root+'.cbc'
cbc_obj = mfb.MODFLOW_CBB(flow.nlay,flow.nrow,flow.ncol,cbc_file)
flux_type = '     SWR LEAKAGE'
#flux_times = cbb_obj.get_time_list(flux_type)
cbc_dts = []
#for flxtime in flux_times:
kper = 1
while True:
    flux,totim,success = cbc_obj.read_next_fluxtype(flux_type)
    if not success:
        break
    #seekpoint = flxtime[3]
    #flux,totim,success = cbb_obj.get_array(seekpoint) 
    #kper = flxtime[2]
    #td = timedelta(days=totim)
    #dt = flow.start + td
    #print dt
    dt = flow.sp_end[kper-1]
    print kper,dt
    cbc_dts.append(dt)
    #for r,c,rch,rgp in rc_tups:
    #    rch_cbc[rch].append(flux[0,r-1,c-1])
    for rc in rch_cbc.keys():
        rch_cbc[rc].append(flux[0,rc[0]-1,rc[1]-1])
    kper += 1

df_cbc = pandas.DataFrame(rch_cbc,index=cbc_dts)
df_cbc.to_csv('cbc_df.csv',index_label='datetime')
sys.exit()


aq_file = flow.root+'.aqx'
aq_obj = mfb.SWR_Record(flow.nlay,aq_file)
aqx_dts = []
while True:
    this_rec = copy.deepcopy(rch_init)
    totim,length,kper,kstp,swrstp,success,records = aq_obj.next()
    dt = flow.sp_end[kper-1]
    
   
    if not success: break
    print kper,dt
    aqx_dts.append(dt)
    for i,rec in enumerate(records):
        #rch_aqx[rec[0]].append(rec[-1])
        rc = rc_tups[rec[0]]
        this_rec[rc] += rec[-1]

    for rc in this_rec.keys():
        rch_aqx[rc].append(this_rec[rc])

#df_aqx = pandas.DataFrame(rch_aqx,index=dts)
#df_aqx.to_csv('aqx_df.csv',index_label='datetime')


#df_diff = df_cbc - df_aqx
#df_diff.to_csv('diff_df.csv',index_label='datetime')
plt_prefix = 'png\\results\\reach_aqx\\rch_'
for rch_num in rch_aqx.keys():
    cbc = np.array(rch_cbc[rch_num])
    aqx = np.array(rch_aqx[rch_num])
    print len(cbc),len(cbc_dts)
    print len(aqx),len(aqx_dts)
    fig = pylab.figure()
    ax1,ax2,ax3 = pylab.subplot(311),pylab.subplot(312),pylab.subplot(313)
    ax1.set_title('cbc '+str(rch_num))
    ax2.set_title('aqx '+str(rch_num))
    ax3.set_title('diff '+str(rch_num))
    ax1.plot(cbc_dts,cbc)
    ax2.plot(aqx_dts,aqx)
    ax3.plot(aqx_dts,cbc - aqx)
    ax1.grid()
    ax2.grid()
    ax3.grid()
    plt_name = plt_prefix+str(rch_num)+'.png.'
    pylab.savefig(plt_name,fmt='png',bbox_inches='tight')
    pylab.close('all')