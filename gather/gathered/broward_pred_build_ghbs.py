import sys
import os
import numpy as np
from datetime import datetime
import pylab
import pandas
import pestUtil as pu
import shapefile
from bro_pred import flow,seawat

'''for now we assume that flow and seawat have the same row col
'''


K = 200.0
L = 500.0
A = 500.0 * 100.0
cond = K * A / L

print 'loading north,south model-aligned dataframe and interpolation factors'
df_ns_data = pandas.read_csv('..\\..\\_nwis\\dataframes\\ghb_NS_stages_model.csv',index_col=0,parse_dates=True)
df_ns_fac = pandas.read_csv('ghb_NS_factors.dat',index_col=[0,1])

#--calc monthly average water levels for ns ghbs
df_ns_monthly = df_ns_data.groupby(lambda x:x.month).mean()
print df_ns_monthly.index
#--process stage record for coastal GHBs - presampled
coastal_df = pandas.read_csv('..\\..\\_noaa\\noaa_slr.csv',index_col=0,parse_dates=True)
coastal_stages = coastal_df['med_rise'].values

#--process stage records for WCA ghbs - these records should have been presampled to stress period dimensions
print 'processing EDEN records'
smp_dir = '..\\..\\_eden\\stage_smp_full\\'
#smp_files = os.listdir(smp_dir)
#eden_ids = []
#eden_sp_vals = {}
#for sfile in smp_files:
#    print 'loading smp file',sfile,'\r',
#    eden_id = int(sfile.split('.')[0])
#    eden_ids.append(eden_id)
#    smp = pu.smp(smp_dir+sfile,load=True)
#    rec = smp.records[str(eden_id)]
#    #--some defense 
#    assert rec.shape[0] == len(flow.sp_len)
#    assert rec[0,0].month == flow.start.month
#    assert rec[-1,0].month == flow.end.month
#    eden_sp_vals[eden_id] = rec[:,1]
df_eden = pandas.read_csv('..\\..\\_eden\\eden_sp.csv',index_col=0,parse_dates=True)
df_eden_monthly = df_eden.groupby(lambda x:x.month).mean()
print df_eden_monthly.index
#--load the row col for both GHB sets
print 'loading grid info for coastal GHBs'
g_att = shapefile.load_as_dict('..\\..\\_gis\\shapes\\broward_grid_master',loadShapes=False,attrib_name_list=['row','column','ibound_CS'])
icoast_rowcol,atlant_rowcol = [],[]
for r,c,i in zip(g_att['row'],g_att['column'],g_att['ibound_CS']):
    if i == 5:
        icoast_rowcol.append([r,c])
    elif i == 2:
        atlant_rowcol.append([r,c])
print 'loading grid info for WCA GHBs'
recs = shapefile.load_as_dict('..\\..\\_gis\\scratch\\broward_grid_eden',loadShapes=False)
wca_r,wca_c,eden_fracs,eden_cells = recs['row'],recs['column'],recs['eden_fracs'],recs['eden_cells']
#--cast fracs and cells
print 'casting fractions and cell numbers'
for i,fracs in enumerate(eden_fracs):
    raw = fracs.split()
    for ii,r in enumerate(raw):
        raw[ii] = float(r)
    eden_fracs[i] = raw
for i,cells in enumerate(eden_cells):
    raw = cells.split()
    for ii,r in enumerate(raw):
        raw[ii] = int(r)
    eden_cells[i] = raw
nghb = len(icoast_rowcol) + flow.nlay * ( len(atlant_rowcol) + len(wca_r) + df_ns_fac.shape[0])
nghb2 = len(icoast_rowcol) + seawat.nlay * ( len(atlant_rowcol) + len(wca_r) + df_ns_fac.shape[0])


#--header
print 'writing records'
f = open(flow.root+'.ghb','w')
f2 = open(seawat.root+'.ghb','w')
f.write('#'+sys.argv[0]+' '+str(datetime.now())+'\n')
f2.write('#'+sys.argv[0]+' '+str(datetime.now())+'\n')
#f.write(' {0:9.0f} {1:9.0f}\n'.format(0,0))
f.write(' {0:9.0f} {1:9.0f}  NOPRINT\n'.format(nghb,flow.ghb_unit))
f2.write(' {0:9.0f} {1:9.0f}  NOPRINT\n'.format(nghb2,seawat.ghb_unit))


for i,[sp,spe] in enumerate(zip(flow.sp_start,flow.sp_end)):
    f.write(' {0:9.0f} {1:9.0f}'.format(nghb,0))
    f.write(' # stress period '+str(i+1)+' '+str(sp)+'\n')

    f2.write(' {0:9.0f} {1:9.0f}'.format(nghb2,0))
    f2.write(' # stress period '+str(i+1)+' '+str(sp)+'\n')

    list_name = flow.list_dir+'ghb_'+sp.strftime('%Y%m%d')+'.dat'    
    list_name2 = seawat.list_dir+'ghb_'+sp.strftime('%Y%m%d')+'.dat'    
    print 'writing list file',list_name,'\r',
    f.write('OPEN/CLOSE '+list_name+'\n')
    f2.write('OPEN/CLOSE '+list_name2+'\n')
    
    fl = open(list_name,'w')            
    fl2 = open(list_name2,'w')            
    #--write coastal GHBs
    coastal_stage = coastal_stages[i]
    for r,c in icoast_rowcol:
        fl.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(1,r,c,coastal_stage,cond,'#icoast'))
    for l in flow.ghb_layers:        
        for r,c in atlant_rowcol:
            fl.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,coastal_stage,cond,'#atlant'))
    for r,c in icoast_rowcol:
        fl2.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(1,r,c,coastal_stage,cond,'#icoast'))
    for l in seawat.ghb_layers:
        for r,c in atlant_rowcol:
            fl2.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,coastal_stage,cond,'#atlant'))
    #--write wca ghbs
    #--build a dict of stage values for this stress period
    #evals = {}
    #for eid,estage in eden_sp_vals.iteritems():
    #    evals[eid] = estage[i]    
    #record = df_eden_monthly.ix[sp.month]
    stage_vals = []
    for eids,efracs in zip(eden_cells,eden_fracs):
        val = 0.0
        for eid,efrac in zip(eids,efracs):
            val += df_eden_monthly[str(eid)][sp.month] * efrac
        stage_vals.append(val)
    for l in flow.ghb_layers:
        for r,c,stage in zip(wca_r,wca_c,stage_vals):
            fl.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,stage,cond,'#eden'))
    for l in seawat.ghb_layers:
        for r,c,stage in zip(wca_r,wca_c,stage_vals):
            fl2.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,stage,cond,'#eden'))
    #--write north south ghbs
    #--write north south ghbs
    #df_ns_dt = df_ns_monthly.ix[sp.month]
    for [r,c],facs in df_ns_fac.iterrows():
        stage = 0.0
        for site,fac in zip(facs[1::2],facs[2::2]):
            site = long(site)
            val = df_ns_monthly[str(site)][sp.month]
            stage += val*fac
        if np.isnan(stage):
            raise Exception('NAN stage '+site+' '+str(dt))                        
        for l in flow.ghb_layers:
            fl.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,stage,cond,'#ns'))
        for l in seawat.ghb_layers:
            fl2.write(' {0:9.0f} {1:9.0f} {2:9.0f} {3:9.4e} {4:9.4e}  {5}\n'.format(l,r,c,stage,cond,'#ns'))
    fl.close()
    fl2.close()
f.close()
