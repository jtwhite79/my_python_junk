import os
import sys
from datetime import datetime
import time
import numpy as np
import pandas

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
                arr[ptype][np.where(arr['aux']==zone)] = value
        write_ascii_list('test\\'+bfile,arr)                  

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
                            
        


    
