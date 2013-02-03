import os
import sys
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time
import numpy as np
import pandas

from bro import flow as calflow
from bro_pred import flow as predflow


ghb_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('stage','f4'),('conductance','f4'),('aux','a20')])
wel_dtype = np.dtype([('layer','i4'),('row','i4'),('column','i4'),('flux','f4'),('aux','a20')])

ghb_fmt = ' %9d %9d %9d %15.6G %15.6G %20s'
wel_fmt = ' %9d %9d %9d %15.6G %20s'


def write_ascii_list(filename,arr):   
    if 'ghb' in filename:
        fmt = ghb_fmt
    elif 'wel' in filename:
        fmt = wel_fmt         
    np.savetxt(filename,arr,fmt=fmt)           


def load_bin_list(filename):
    if 'ghb' in filename.lower():         
        arr = np.fromfile(filename,dtype=ghb_dtype)   
    elif 'wel' in filename.lower():
        arr = np.fromfile(filename,dtype=wel_dtype)   
    else:
        raise Exception('unrecongnize list type: '+filename)
    return arr

def load_ascii_list(filename):    
        print filename  
        if 'ghb' in filename.lower():         
            arr = np.genfromtxt(filename,dtype=ghb_dtype,comments='|')   
        elif 'wel' in filename.lower(): 
            arr = np.genfromtxt(filename,dtype=wel_dtype,comments='|')   
        else:
            raise Exception('unrecongnize list type: '+filename)
        return arr




def apply():
    #--load the factors
    factor_file = 'par\\ghbwel_factors.dat'
    factors = pandas.read_csv(factor_file,index_col='datetime',parse_dates=True)
    #--setup the multiindex for the columns
    col_strings = factors.columns
    tups = []
    for c in col_strings:
        tups.append(c.split('_'))
    mi = pandas.MultiIndex.from_tuples(tups,names=('bc_type','p_type','zone'))
    factors.columns = mi
    factor_dts = factors.index


    start = time.clock()

    factor_dt_groups = {}
    bc_types = ['ghb','wel']
    for fdt in factor_dts:
        row = factors.ix[fdt]

        bc_groups = row.groupby(level=[0])
        btyp = {}
        for bc_type,group in bc_groups:
            p_groups = group.groupby(level=1)
            ptyp = {}
            for ptype,group in p_groups:
                ztyp = {}
                for idx,val in group.iteritems():
                    ztyp[idx[-1]] = val
                ptyp[ptype] = ztyp
            btyp[bc_type] = ptyp
        factor_dt_groups[fdt] = btyp    


    key_dir = 'misc\\'
    files = os.listdir(key_dir)
    key_files = []
    for f in files:
        if f.endswith('key'):
            key_files.append(f)



    #--process each key file
    for kfile in key_files:
        ascii_dir = '\\'.join(kfile.replace('.key','').split('_'))
        bin_dir = ascii_dir + 'bin' + '\\'
        ascii_dir += '\\'
        f = open(key_dir+kfile,'r')
        key_dict = {}
        for line in f:
            raw = line.strip().split()
            l,r,c = int(raw[1]),int(raw[2]),int(raw[3])
            key_dict[(l,r,c)] = raw[0]
        f.close()
        bin_files = os.listdir(bin_dir)
        factor = 1

        for bfile in bin_files:
            print bfile
            #--get the bc type and datetime from the file name
            raw = bfile.split('.')[0].split('_')
            bc_type = raw[0]        
            dt = datetime.strptime(raw[1],'%Y%m%d')
            #--find the factor row to use
            for fdt in factor_dts:
                if dt <= fdt:
                    break        
        
            #--load the bin list
            arr = load_bin_list(bin_dir+bfile)
            
            bc_factors = factor_dt_groups[fdt][bc_type]                                    
            for ptype,zone_group in bc_factors.iteritems():
                for zone,value in zone_group.iteritems():
                    arr[ptype][np.where(arr['aux']==zone)] *= value
            write_ascii_list(ascii_dir+bfile,arr)                  
            
            #--speed testing - pandas is slower (slightly)
            ##--get the factors for this bc type (ghb or wel)
            #bc_factors = factors.xs(bc_type,axis=1).ix[fdt]
            ##--group by par type (cond,stage,flux)
            #p_groups = bc_factors.groupby(level=0)        
        
            ##uzones = np.unique(arr['aux'])
            ##--apply the factors
            #for ptype,group in p_groups:
            #        for idx,value in group.iteritems():
            #            arr[idx[0]][np.where(arr['aux']==idx[1])] *= value
            ##--save the factored array as ascii
            ##write_ascii_list(ascii_dir+bfile,arr)
            #write_ascii_list('test\\'+bfile,arr)

    print 'total time:',time.clock() - start

def setup():
  
    
    '''loads the ascii lists and saves them to binary, writes the well and ghb template files,
    and writes param and pargp files 

    '''    
   
    in_dirs = ['..\\_model\\bro.03\\flowlist\\','..\\_model\\bro.03\\seawatlist\\','..\\_prediction\\bro.03.pred\\flowlist\\','..\\_prediction\\bro.03.pred\\seawatlist\\']
    out_dirs = ['bro.03\\calibration\\flowlist\\','bro.03\\calibration\\seawatlist\\','bro.03\\prediction\\flowlist\\','bro.03\\prediction\\seawatlist\\']
    par_types = {'ghb':['stage','conductance'],'wel':['flux']}
    unique_idents = {}
    for in_d,out_d in zip(in_dirs,out_dirs):  
        files = os.listdir(in_d)    
        zone_tups = {}
        for bctyp in par_types.keys():       
            fsize = None
            for i,f in enumerate(files):
                if bctyp in f:                
                    file_bctyp = f.split('_')[0]
                    dt = datetime.strptime(f.split('.')[0].split('_')[1],'%Y%m%d')      
                    if file_bctyp not in unique_idents.keys():                   
                        arr = load_ascii_list(in_d+f)                                
                        uarr = np.unique(arr['aux'])                    
                        unique = []
                        for u in uarr:
                            if '_' in u:
                                u = u.split('_')[0]                        
                            if u not in unique:
                                unique.append(u)                                                                                                  
                        
                        unique_idents[file_bctyp] = unique
                    if fsize is None or os.path.getsize(in_d+f) != fsize:
                        fsize = os.path.getsize(in_d+f)
                        arr = load_ascii_list(in_d+f)                                
                        uarr = np.unique(arr['aux']) 
                        for u in uarr:
                            u_key = u
                            if '_' in u:
                                u_key = u.split('_')[0]                                 
                            ulrc = arr[np.where(arr['aux']==u)]   
                            lrc_tups = zip(ulrc['layer'],ulrc['row'],ulrc['column'],ulrc['aux'],[file_bctyp]*ulrc.shape[0])       
                            if u_key not in zone_tups.keys():
                                #ulrc = arr[np.where(arr['aux']==u)]   
                                #lrc_tups = zip(ulrc['layer'],ulrc['row'],ulrc['column'],ulrc['aux'])   
                                zone_tups[u_key] = lrc_tups 
                            else:
                                zone_tups[u_key].extend(lrc_tups)                                                                                                      
                    
        f = open('misc\\'+'_'.join(out_d.split('\\')[:-1])+'.key','w',0)
        for key,tups in zone_tups.iteritems():
            for tup in tups:
                f.write('{0:15s} {1:5d} {2:5d} {3:5d} {4:s} {5:s}\n'.format(key,tup[0],tup[1],tup[2],tup[3],tup[4]))
        f.close()        
    #--tie stage parameters for the intercoastal (ui=51 to 55) to the atlantic stage (ui=2)
    tied_uids = ['#51','#52','#53','#54','#55']
    tpl_lines = []
    ptypes = {'ghb':['st','cd'],'wel':['fx']}
    names = {'st':'stage','cd':'conductance','fx':'flux'}
    param_groups = {}
    header = 'datetime,'    
    step = relativedelta(years=10)
    day = calflow.start
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
    panmes = []
    day = predflow.start
        #line = str(day)+','
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
    
    f_tpl = open('tpl\\ghbwel_flow.tpl','w',0)
    f_out = open('par\\ghbwel_flow.csv','w',0)
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

    


    f_grp = open('pst_components\\ghbwel_flow_grps.dat','w',0)
    f_par = open('pst_components\\ghbwel_flow_pars.dat','w',0)
    pargps = param_groups.keys()
    pargps.sort()
    for pargp in pargps:
        pnames = param_groups[pargp]
        f_grp.write('{0:<20s} factor 0.01  0.001 switch  2.0 parabolic\n'.format(pargp))
        for pname in pnames:

            f_par.write('{0:<20s} log factor  1.0 1.0e-10 1.0e+10 {1:<20s}  1.0 0.0  0\n'.format(pname,pargp))
    f_grp.close()
    f_par.close()



                            
if __name__ == '__main__':
    setup()
    #apply()        


    

