import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas
from bro import flow as calflow
from bro_pred import flow as predflow
'''loads the ascii lists and saves them to binary, writes the well and ghb template files,
and writes param and pargp files 

huge assumption - all of the BCs are listed in every ascii file

'''



ghb_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('stage','f4'),('conductance','f4'),('aux','a20')])
wel_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('flux','f4'),('aux','a20')])


def load_ascii_list(filename):    
    print filename  
    if 'ghb' in filename.lower():         
        arr = np.genfromtxt(filename,dtype=ghb_dtype,comments='|')   
    elif 'wel' in filename.lower(): 
        arr = np.genfromtxt(filename,dtype=wel_dtype,comments='|')   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr


#--calibration 
step = relativedelta(years=10)
day = calflow.start
ascii_dirs = ['bro.02\\calibration\\flowlist\\','bro.02\\calibration\\seawatlist\\','bro.02\\prediction\\flowlist\\','bro.02\\prediction\\seawatlist\\']
par_types = {'ghb':['stage','conductance'],'wel':['flux']}
unique_idents = {}
for ad in ascii_dirs:
   
    files = os.listdir(ad)    
    for bctyp in ['ghb','wel']:
        zone_tups = {}
        fsize = None
        for i,f in enumerate(files):
            if bctyp in f:                
                file_bctyp = f.split('_')[0]
                dt = datetime.strptime(f.split('.')[0].split('_')[1],'%Y%m%d')      
                if file_bctyp not in unique_idents.keys():                   
                    arr = load_ascii_list(ad+f)                                
                    uarr = np.unique(arr['aux'])                    
                    unique = []
                    for u in uarr:
                        if '_' in u:
                            u = u.split('_')[0]                        
                        if u not in unique:
                            unique.append(u)                                                                                                  
                        
                    unique_idents[file_bctyp] = unique
                if fsize is None:
                    fsize = os.path.getsize(ad+f)
                    arr = load_ascii_list(ad+f)                                
                    uarr = np.unique(arr['aux']) 
                    for u in uarr:
                        u_key = u
                        if '_' in u:
                            u_key = u.split('_')[0]                                 
                        ulrc = arr[np.where(arr['aux']==u)]   
                        lrc_tups = zip(ulrc['layer'],ulrc['row'],ulrc['column'])       
                        if u_key not in zone_tups.keys():
                            ulrc = arr[np.where(arr['aux']==u)]   
                            lrc_tups = zip(ulrc['layer'],ulrc['row'],ulrc['column'])   
                            zone_tups[u_key] = lrc_tups 
                        else:
                            zone_tups[u_key].extend(lrc_tups)                                                  
                            #for lrc in lrc_tups:
                            #    if lrc not in zone_tups[u]:
                            #        zone_tups[u_key].append(lrc)
                else:
                    if os.path.getsize(ad+f) != fsize:
                        print 'warning - ASCII files not the same size: '+\
                        str(os.path.getsize(ad+f))+' '+str(fsize)+' '+ad+f
                           
        f = open('misc\\'+'_'.join(ad.split('\\')[:-1])+'.key','w',0)
        for key,tups in zone_tups.iteritems():
            for tup in tups:
                f.write('{0:15s} {1:5d} {2:5d} {3:5d}\n'.format(key,tup[0],tup[1],tup[2]))
        f.close()
        #full_dfs = []
        #for ptyp,pdfs in dfs.iteritems():            
        #    df = pandas.concat(pdfs,axis=1)            
        #    full_dfs.append(df)        
        #df = pandas.concat(full_dfs,axis=1,keys=dfs.keys())
        #df['layer'] = df.index.get_level_values(0)
        #df['row'] = df.index.get_level_values(1)
        #df['column'] = df.index.get_level_values(2)
        #df['zone'] = df.index.get_level_values(3)       
        #df.to_csv('setup\\'+'_'.join(d.split('\\')[:-1])+'-'+bctyp+'.csv',sep='|',index=False)
#--tie that stage parameters for the intercoastal (ui=51 to 55) to the atlantic stage (ui=2)
tied_uids = ['#51','#52','#53','#54','#55']
tpl_lines = []
ptypes = {'ghb':['st','cd'],'wel':['fx']}
names = {'st':'stage','cd':'conductance','fx':'flux'}
param_groups = {}
header = 'datetime,'
while day < calflow.end:    
    panmes = []
    line = str(day)+','
    for typ,uids in unique_idents.iteritems():
        for ui in uids:            
            for ptype in ptypes[typ]:                
                if day == calflow.start:
                    header += typ+'_'+names[ptype]+'_'+ui+','
                this_ui = ui                                                           
                if ptype == 'st' and ui in tied_uids:
                    this_ui = '#2'
                this_day = day                        
                if ptype == 'cd' and day != calflow.start:
                    this_day = calflow.start
                pname = typ[0]+ptype+this_ui.replace('#','')+'_'+str(this_day.year)
                if len(pname) > 12:
                    raise Exception('pname too long: '+pname)
                pargp = typ+'_'+ptype
                if pargp not in param_groups.keys():
                    param_groups[pargp] = [pname]
                elif pname not in param_groups[pargp]:                    
                    param_groups[pargp].append(pname)                
                tpl_entry = '~{0:20s}~,'.format(pname)
                line += tpl_entry
    line = line[:-1]
    tpl_lines.append(line)            
    day += step
header = header[:-1]
line = str(predflow.start)+','
for typ,uids in unique_idents.iteritems():
    for ui in uids:
        for ptype in ptypes[typ]:                                                    
            this_ui = ui                                                           
            if ptype == 'st' and ui in tied_uids:
                this_ui = '#2'
            suffix = '_rate'            
            pname = typ[0]+ptype+this_ui.replace('#','')+suffix
            if len(pname) > 12:
                raise Exception('pname too long: '+pname)
            if ptype != 'cd':
                pargp = typ+'_'+ptype+'_pred'
                if pargp not in param_groups.keys():
                    param_groups[pargp] = [pname]
                elif pname not in param_groups[pargp]:                    
                    param_groups[pargp].append(pname)                
                tpl_entry = '~{0:20s}~,'.format(pname)
            else:
                tpl_entry = '1.0,'
            line += tpl_entry


f_tpl = open('tpl\\ghbwel_cal.tpl','w',0)
f_out = open('par\\ghbwel_cal.dat','w',0)
f_tpl.write('ptf ~\n')
f_tpl.write(header+'\n')
f_out.write(header+'\n')
for i,line in enumerate(tpl_lines):
    f_tpl.write(line+'\n')
    raw = line.split(',')
    f_out.write(raw[0]+',')
    line = ''
    for i in range(1,len(raw)):
        line += str(i) + ','
        
    f_out.write(line[:-1]+'\n')
f_tpl.close()
f_out.close()


#--reset to use the last dt
day -= step

#--prediction - we want to use the last stage/flux from the calibration and apply annual rate increase factor
#header = 'datetime,'
#tpl_lines = []
#line = str(predflow.start)+','
#for typ,uids in unique_idents.iteritems():
#    for ui in uids:
#        for ptype in ptypes[typ]:                                        
#            header += typ+'_'+ptype+'_'+ui+','
#            this_ui = ui                                                           
#            if ptype == 'st' and ui in tied_uids:
#                this_ui = '#2'
#            suffix = '_rate'            
#            pname = typ[0]+ptype+this_ui.replace('#','')+suffix
#            if len(pname) > 12:
#                raise Exception('pname too long: '+pname)
#            if ptype != 'cd':
#                pargp = typ+'_'+ptype+'_pred'
#                if pargp not in param_groups.keys():
#                    param_groups[pargp] = [pname]
#                elif pname not in param_groups[pargp]:                    
#                    param_groups[pargp].append(pname)                
#                tpl_entry = '~{0:20s}~,'.format(pname)
#            else:
#                tpl_entry = '1.0,'
#            line += tpl_entry
#tpl_lines = [line[:-1]]
#header = header[:-1]        

#f_tpl = open('tpl\\ghbwel_pred.tpl','w',0)
#f_out = open('par\\ghbwel_pred.dat','w',0)
#f_tpl.write('ptf ~\n')
#f_tpl.write(header+'\n')
#f_out.write(header+'\n')
#for i,line in enumerate(tpl_lines):
#    f_tpl.write(line+'\n')
#    raw = line.split(',')
#    f_out.write(raw[0]+',')
#    line = ''
#    for i in range(1,len(raw)):
#        line += str(i)+','

#    f_out.write(line[:-1]+'\n')
#f_tpl.close()
#f_out.close()


f_grp = open('setup\\ghbwel_pargp.dat','w',0)
f_par = open('setup\\ghbwel_parms.dat','w',0)
pargps = param_groups.keys()
pargps.sort()
for pargp in pargps:
    pnames = param_groups[pargp]
    f_grp.write('{0:<20s} factor 0.01  0.001 switch  2.0 parabolic\n'.format(pargp))
    for pname in pnames:

        f_par.write('{0:<20s} log factor  1.0 1.0e-10 1.0e+10 {1:<20s}  1.0 0.0  0\n'.format(pname,pargp))
f_grp.close()
f_par.close()