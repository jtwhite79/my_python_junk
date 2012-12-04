import os
import datetime
import numpy as np
import pandas

import dbhydro_util as dbu

#--get a list of gate opening time series
g_dir = 'SW\\GATE\\'
gate_files = os.listdir(g_dir)

#--get a list of site names and structure numbers
g_sites,g_str_num = [],[]
for f in gate_files:
    s = f.split('.')[0]
    snum = int(f.split('.')[3])
    if s not in g_sites:
        g_sites.append(s)
        g_str_num.append([snum])
    else:
        idx = g_sites.index(s)
        if snum not in g_str_num[idx]:
            g_str_num[idx].append(snum)
                 
       
#--for each gate structure
og_dir = 'processed\\SW\\GATE_daily\\'
for g,g_str in zip(g_sites,g_str_num):
    #--find the records for this gate    
    for gg_str in g_str:
        this_gate_files,this_gate_info = [],[]
        for f in gate_files:
            fdict = dbu.parse_fname(f)            
            if fdict['site'] == g and fdict['strnum'] == gg_str:
                this_gate_files.append(f)
                this_gate_info.append(fdict)
        #print this_gate_files
        p_series = []
        for gf,gi in zip(this_gate_files,this_gate_info):       
            if gi['dtype'].upper() == 'BK':
                series,flg = dbu.load_series(g_dir+gf)            
                series = dbu.interp_breakpoint(series,flg)
                p_series.append(pandas.TimeSeries(series[:,1],index=series[:,0]))
            else:
                #raise TypeError,'Only use breakpoint data for gate openings'                
                print 'non break point record - skipping'
        
        #--create a full record
        final_p_series = dbu.create_full_record(p_series)                
        dbu.save_series(og_dir+g+'.'+str(gg_str)+'.dat',final_p_series)
        print 'processed record saved for structure,gate:',str(g),str(gg_str),'\n'
        #break
    #break                                    

        