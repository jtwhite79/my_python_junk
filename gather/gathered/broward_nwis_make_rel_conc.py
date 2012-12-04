import os
import numpy as np
import pestUtil


def parse_smp_filename(filename):
    raw = filename.split('.')[:-1]
    parsed = {'agency':raw[0],'site_no':raw[1],'name':raw[2],'param':raw[3]}
    return parsed

def build_smp_filename(dict):
    fname = dict['agency']+'.'+dict['site_no']+'.'+dict['name']+'.'+dict['param']+'.smp'
    return fname

#--constants
chl_seawater = 19400.0
tds_seawater = 35000.0


#--load the processed chl files and convert to relative chl values
chl_dir = 'smp_chl_mgl\\'
chl_files = os.listdir(chl_dir)
out_dir = 'smp_rel_conc_chl\\'


for chl_file in chl_files:
    
    smp = pestUtil.smp(chl_dir+chl_file,load=True)
    fi_attrib = parse_smp_filename(chl_file)
    smp.records['site'][:,1] /= chl_seawater
    #--correct values greater than 1.0
    smp.records['site'][np.where(smp.records['site'][:,1]>1.0),1] = 1.0
    fi_attrib['param'] = 'relconc'
    new_name = build_smp_filename(fi_attrib)
    smp.save(out_dir+new_name)

#--the regressed chl files
chl_dir = 'smp_chl_mgl_regressed\\'
chl_files = os.listdir(chl_dir)
out_dir = 'smp_rel_conc_regressed\\'

for chl_file in chl_files:
    
    smp = pestUtil.smp(chl_dir+chl_file,load=True)
    fi_attrib = parse_smp_filename(chl_file)
    smp.records['site'][:,1] /= chl_seawater
    #--correct values greater than 1.0
    smp.records['site'][np.where(smp.records['site'][:,1]>1.0),1] = 1.0
    fi_attrib['param'] = 'relconc'
    new_name = build_smp_filename(fi_attrib)
    smp.save(out_dir+new_name)

#rel_files = os.listdir(out_dir)

#--load the unprocessed tds files and convert to relative tds and merge with relative chl files
smp_dir = 'raw_smp\\'
smp_files = os.listdir(smp_dir)
tds_files = []
for smp_file in smp_files:
    if parse_smp_filename(smp_file)['param'] == 'dissolved':
        tds_files.append(smp_file)

out_dir = 'smp_rel_conc_tds\\'
for tds_file in tds_files:
    fi_attrib = parse_smp_filename(tds_file)
    smp = pestUtil.smp(smp_dir+tds_file,load=True)
    smp.records['site'][:,1] /= tds_seawater
    #--correct values greater than 1.0
    smp.records['site'][np.where(smp.records['site'][:,1]>1.0),1] = 1.0
    fi_attrib['param'] = 'relconc'
    new_name = build_smp_filename(fi_attrib)
    #if new_name in rel_files:
    #    other_smp = pestUtil.smp(out_dir+new_name,load=True)
    #    other_smp.merge(smp,how='left')
    #    other_smp.save(out_dir+new_name)
    #else:
    #    smp.save(out_dir+new_name)
    smp.save(out_dir+new_name)            