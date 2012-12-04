import sys
import os
from datetime import datetime
import pandas
import shapefile

import swr
from bro import flow


#--build rain and evap entry dicts
rch_dir,ets_dir = flow.ref_dir+'rch\\',flow.ref_dir+'ets\\'
rch_files,ets_files = os.listdir(rch_dir),os.listdir(ets_dir)
rch_dts,ets_dts = [],[]
for rfile in rch_files:
    dt = datetime.strptime(rfile.split('.')[0].split('_')[-1],'%Y%m%d')
    rch_dts.append(dt)

for efile in ets_files:
    dt = datetime.strptime(efile.split('.')[0].split('_')[-1],'%Y%m%d')
    ets_dts.append(dt)

rain,evap = {},{}
for sday,eday in zip(flow.sp_start,flow.sp_end):
    rain[eday] = '#DATASET 7B RAIN\nOPEN/CLOSE '+rch_dir+rch_files[rch_dts.index(sday)] + ' {0:10.5f} (BINARY)  -1\n'.format(flow.rch_mult)
    evap[eday] = '#DATASET 8B EVAP\nOPEN/CLOSE '+ets_dir+ets_files[ets_dts.index(sday)] + ' {0:10.5f} (BINARY)  -1\n'.format(flow.ets_mult)

#--swrpre polyline shapefile with all the info
swr_shapename = '..\\..\\_gis\\scratch\\sw_reaches_conn_SWRpolylines'
shp = shapefile.Reader(swr_shapename)
fieldnames = shapefile.get_fieldnames(swr_shapename)
for i,name in enumerate(fieldnames):
    print i,name

#--map of where attributes are in the dbf - painful
idx = {'reach':22,'iroute':14,'reachgroup':23,'row':21,'column':20,'length':27,'conn':25,'nconn':24,'active':12,'str_num':10,'ibnd':16}

#-create reach instances
reaches,shp_records = swr.load_reaches_from_shape(swr_shapename,idx)

#--for testing
reaches_act = []

#--set the stage series for each reach
stage_df = pandas.read_csv('..\\..\\_swr\\reach_series.csv',parse_dates=True,index_col=0)
stage_reaches = stage_df.keys()
for reach in reaches:
    rnum = int(reach.reach)
    if rnum == 1010:
        pass
    if reach.ibnd != 0:
        series = stage_df[str(reach.reach)]
        if len(series) != len(series.dropna()):
            raise Exception('NANs in series for reach '+str(reach.reach))
        reach.set_stage_series(series)
        reaches_act.append(reach)
        #break

#--build the igeonumr list for dataset 10 - time invariant
xsec_idx = 4
reach_nums,xsec_names = [],[]
for r in shp_records:
    reach_nums.append(r[idx['reach']])
    xsec_names.append(r[xsec_idx])

unique_xsec_names = []
for xname in xsec_names:
    if xname not in unique_xsec_names:
        unique_xsec_names.append(xname)

igeonumr = []
for rnum,xname in zip(reach_nums,xsec_names):
    idx = unique_xsec_names.index(xname)    
    igeonumr.append([rnum,idx+1,0.0])
igeonumr = {flow.sp_end[0]:igeonumr}

#--build dataset 11a and 11b entries - time invariant
swr_xsec_path = 'xsec_navd\\'
xsec_path = '..\\..\\_swr\\xsec_navd\\'
igcndop = 3 #use K of the cell and leakance
igeotype = 3
gcndln = 250.0
glk = 5.0
gmann = 0.030
data_11 = []
for i,unique_xsec in enumerate(unique_xsec_names):
    #--get the number of points in the xsection
    f = open(xsec_path+unique_xsec,'r')
    ngeopts = int(f.readline().strip().split()[3])
    line1 = ' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.3G} {4:9.0F} {5:>39.3G} {6:9.3G}\n'.format(i+1,igeotype,igcndop,gmann,ngeopts,glk,gcndln)
    line2 = 'OPEN/CLOSE ' + swr_xsec_path + unique_xsec + '\n'
    data_11.append(line1+line2)
data_11 = {flow.sp_end[0]:data_11}    

f = open(flow.root+'.swr','w',0)
f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')


#-- ds-1 
options = ['PRINT_SWR_TO_SCREEN','SAVE_AVERAGE_RESULTS','USE_NONCONVERGENCE_CONTINUE','SAVE_RIVER_PACKAGE 107',\
    'USE_INEXACT_NEWTON','USE_LAGGED_OPR_DATA','USE_DIAGONAL_SCALING','USE_RCM_REORDERING','USE_EXPLICIT_NEWTON_CORRECTION']
ds_1 = swr.ds_1(len(reaches),iswrprgf=-101,iswrpstg=-102,iswrpqaq=-103,iswrpqm=-104,options=options)
ds_1.write(f)
#ds_1.add_2_namefile(bro.modelname)

#-- ds-2
ds_2 = swr.ds_2()
ds_2.write(f)

ds_3 = swr.ds_3()
ds_3.write(f)

ds_4a = swr.ds_4a(reaches)
f.write(ds_4a.get_entry(filename=flow.ref_dir+'swr\\ds_4a.dat')+'\n\n')

ds_4b = swr.ds_4b(reaches)
f.write(ds_4b.get_entry(filename=flow.ref_dir+'swr\\ds_4b.dat')+'\n\n')


lateral_inflows = None

swr_ts = swr.swr_timestep(f,reaches,rain,evap,lateral_inflows,igeonumr,data_11,flow.sp_end,datadir=flow.ref_dir+'swr\\')
swr_ts.write_transient_sequence()

