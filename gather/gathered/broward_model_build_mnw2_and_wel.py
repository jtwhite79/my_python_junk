import sys
import os
import numpy as np
import numpy
from datetime import datetime,timedelta
import pandas
import shapefile
import pestUtil as pu
from bro import flow,seawat 

'''for now, we assume seawat and flow have the row col
'''


def intersect(well_interval,layer_elevs):
    lay,frac = [],[]
    for i in range(len(layer_elevs[:-1])):
        layer_interval = [layer_elevs[i],layer_elevs[i+1]]
        olap = overlap(well_interval,layer_interval)
        f = olap / (layer_interval[0] - layer_interval[1])
        #f = olap / (well_interval[0] - well_interval[1])
        if f > 0.0:
            lay.append(i)
            frac.append(f)
        #print well_interval,layer_interval,olap
    return lay,frac        

def overlap(interval1,interval2):
    olap = min(interval1[0],interval2[0]) - max(interval1[1],interval2[1])
    if olap > 0.0 :
        return olap
    else:
        return 0.0



#--load the pre-processed stress period aligned pumpage
pump_df = pandas.read_csv('..\\..\\_pumpage\\dataframes\\pws_filled_zeros.csv',index_col=0,parse_dates=True)
#--some defense
for well,series in pump_df.iteritems():
    assert series.shape[0] == flow.nper


#--load the botm's - for the standard wel package
botm = np.zeros((flow.nlay+1,flow.nrow,flow.ncol)) - 1.0e10
botm[0,:,:] = np.loadtxt(flow.ref_dir+'top_layering.ref')
for i,prefix in enumerate(flow.layer_botm_names):
    lay_botm = np.loadtxt(flow.ref_dir+prefix+'_bot.ref')    
    botm[i+1,:,:] = lay_botm

botm2 = np.zeros((seawat.nlay+1,seawat.nrow,seawat.ncol)) - 1.0e10
botm2[0,:,:] = np.loadtxt(seawat.ref_dir+'top_layering.ref')
for i,prefix in enumerate(seawat.layer_botm_names):
    lay_botm = np.loadtxt(seawat.ref_dir+prefix+'_bot.ref')    
    botm2[i+1,:,:] = lay_botm


pws_shapename = '..\\..\\_gis\\shapes\\pws_combine'
pws_recs = shapefile.load_as_dict(pws_shapename,loadShapes=False)
mnw_ds2 = []
dfs = []
#f = open('test.dat','w')
count = 1
inactive = []
wel_rcl = {}
wel_rcl2 = {}
nwells_flow,nwells_seawat = 0,0
for dep_name,r,c,top,bot,ibnd in zip(pws_recs['DPEP_NAME'],pws_recs['row'],pws_recs['column'],pws_recs['ztop'],pws_recs['zbot'],pws_recs['ibound_CS']):
    if ibnd > 0:
        if dep_name in pump_df.keys():                
            #--mnw 
            line_2a = dep_name.ljust(20)+'{0:10.0f}'.format(-1)+'{0:>33s}'.format('#2a')+'\n'
            mnw_ds2.append(line_2a)
            line_2b = 'THIEM'.ljust(19)+'0'.ljust(10)+'0'.ljust(10)+'0'.ljust(10)+'0'.ljust(10)+' #2b\n'
            mnw_ds2.append(line_2b)
            line_2c = '{0:10.4f}'.format(1.0)+'{0:>53s}'.format('#2c')+'\n'
            mnw_ds2.append(line_2c)
            line_2d2 = ' {0:9.4f} {1:9.4f} {2:9.0f} {3:9.0f}'.format(float(top),float(bot),int(r),int(c))+'{0:>26s}'.format('#2d-2\n')
            mnw_ds2.append(line_2d2) 
            
            #--wel - flow model
            wel_botm = botm[:,r-1,c-1]
            ks,fracs = intersect([float(top),float(bot)],wel_botm)
            #mlay = lays[frac.index(max(frac))] + 1
            lrc_strings = []
            if len(ks) == 1:
                lrc_string = ' {0:9.0f} {1:9.0f} {2:9.0f}'.format(ks[0]+1,r,c)
                lrc_strings.append(lrc_string)
                nwells_flow += 1
            else:
                for k,f in zip(ks,fracs):
                    if f > 0.1:
                        lrc_string = ' {0:9.0f} {1:9.0f} {2:9.0f}'.format(k+1,r,c)
                        lrc_strings.append(lrc_string)
                        nwells_flow +=1
            #--value as a list - in case of switch to multilayers later
            wel_rcl[dep_name] = lrc_strings

            #--wel seawat
            wel_botm = botm2[:,r-1,c-1]
            #lays,frac = intersect([float(top),float(bot)],wel_botm)
            #mlay = lays[frac.index(max(frac))] + 1
            #rcl_string = ' {0:9.0f} {1:9.0f} {2:9.0f}'.format(mlay,r,c)            
            ks,fracs = intersect([float(top),float(bot)],wel_botm)                        
            lrc_strings = []
            if len(ks) == 1:
                lrc_string = ' {0:9.0f} {1:9.0f} {2:9.0f}'.format(ks[0]+1,r,c)
                lrc_strings.append(lrc_string)
                nwells_seawat += 1
            else:
                for k,f in zip(ks,fracs):
                    if f > 0.1:
                        lrc_string = ' {0:9.0f} {1:9.0f} {2:9.0f}'.format(k+1,r,c)
                        lrc_strings.append(lrc_string)
                        nwells_seawat += 1
            #--value as a list - in case of switch to multilayers later
            wel_rcl2[dep_name] = lrc_strings
            count += 1

            #if count > 5:
            #    break   
        else:
            print 'no record for well',dep_name                                    
    else:
        inactive.append(dep_name)



#num_wells = len(pump_df.keys()) - len(inactive)

#--this is where we need the flow->seawat row col map for the wells


f_wel = open(flow.root+'.wel','w',0)
f_wel.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
f_wel.write(' {0:9.0f} {1:9.0f} {2}\n'.format(nwells_flow,flow.well_unit,"NOPRINT"))    

f_wel2 = open(seawat.root+'.wel','w',0)
f_wel2.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
f_wel2.write(' {0:9.0f} {1:9.0f} {2}\n'.format(nwells_seawat,seawat.well_unit,"NOPRINT"))    



#--write the mnw ds 1
#f_mnw = open(flow.root+'.mnw','w',0)
#f_mnw.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')
#f_mnw.write(' {0:9.0f} {1:9.0f} {2:9.0f}\n'.format(num_wells,0,0))    
#for line in mnw_ds2:
#    f_mnw.write(line)
   
sp_start = flow.sp_start
sp_len = flow.sp_len
i = 1

#--for writing the external wel lists
bnd_prefix = flow.list_dir+'wel_'
bnd_prefix2 = seawat.list_dir+'wel_'

for start,[end,record] in zip(sp_start,pump_df.iterrows()):       
    mnw_ds4 = []
    wel_sp,wel_sp2 = [],[]
    for dep_name,value in zip(record.index,record.values):
        if dep_name not in inactive:
            #--only write non-zero values fro mnw
            #if value > 0.0:
            #    line_ds4a = '{0:<20s}{1:>20.8e} {2:30s}\n'.format(dep_name,-1.0*value,'#4a')
            #    mnw_ds4.append(line_ds4a)
            #--write all values for wel - makes SSM much easier
            flow_val = value / len(wel_rcl[dep_name])
            for rcl_string in wel_rcl[dep_name]:
                line_wel = rcl_string + ' {0:20.8E} #{1}\n'.format(-flow_val,dep_name)
                wel_sp.append(line_wel)
            seawat_val = value / len(wel_rcl2[dep_name])                                            
            for rcl_string in wel_rcl2[dep_name]:
                line_wel = rcl_string + ' {0:20.8E} #{1}\n'.format(-seawat_val,dep_name)
                wel_sp2.append(line_wel)
    

    #f_mnw.write('{0:10.0f}'.format(len(mnw_ds4))+'{0:50s}'.format('')+'#3 Stress Period '+str(i+1)+' '+start.strftime('%Y%m%d')+'\n')    
    #for line in mnw_ds4:
    #    f_mnw.write(line)

    f_wel.write(' {0:9.0f} {1:9.0f} '.format(len(wel_sp),0)+'  # Stress Period '+str(i+1)+' '+start.strftime('%Y%m%d')+'\n')    
    f_wel2.write(' {0:9.0f} {1:9.0f} '.format(len(wel_sp2),0)+'  # Stress Period '+str(i+1)+' '+start.strftime('%Y%m%d')+'\n')    
    bnd_name = bnd_prefix+start.strftime('%Y%m%d')+'.dat'
    bnd_name2 = bnd_prefix2+start.strftime('%Y%m%d')+'.dat'
    f_wel.write('OPEN/CLOSE '+bnd_name+' \n')
    f_wel2.write('OPEN/CLOSE '+bnd_name2+' \n')
    f_bnd = open(bnd_name,'w',0)
    for line in wel_sp:
        f_bnd.write(line)
    f_bnd.close()

    f_bnd2 = open(bnd_name2,'w',0)
    for line in wel_sp2:
        f_bnd2.write(line)
    f_bnd2.close()

    i += 1
#f_mnw.close()  
f_wel.close()      
f_wel2.close() 

        


