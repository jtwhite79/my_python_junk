import os
import shutil
import pestUtil
'''converts ngvd to navd
'''

def parse_smp_filename(filename):
    raw = file.split('.')[:-1]
    parsed = {'agency':raw[0],'site_no':raw[1],'name':raw[2],'param':raw[3]}
    return parsed

def build_smp_filename(dict):
    fname = dict['agency']+'.'+dict['site_no']+'.'+dict['name']+'.'+dict['param']+'.smp'
    return fname


#--get a list of all the raw smp file
smp_in_dir = 'raw_smp\\'
smp_out_dir = 'smp\\'
smp_files = os.listdir(smp_in_dir)

#--parse the file names into dicts of attributes
parsed_smp_names = []
for file in smp_files:
    parsed = parse_smp_filename(file) 
    parsed_smp_names.append(parsed)


#--get a list of navd files
navd_files = []
for file,attributes in zip(smp_files,parsed_smp_names):
    if attributes['param'] == 'navd':
        navd_files.append(file)


#--write new smp files NGVD to NAVD
ngvd2navd = -1.5
for file,attributes in zip(smp_files,parsed_smp_names):
    if attributes['param'] == 'ngvd':
        smp = pestUtil.smp(smp_in_dir+file,load=True)
        smp.records['site'][:,1] += ngvd2navd
        attributes['param'] = 'navd'
        new_name = build_smp_filename(attributes)
        if new_name in navd_files:
            other_smp = pestUtil.smp(smp_in_dir+new_name,load=True)            
            smp.merge(other_smp)
            #--remove other smp from the navd list
            navd_files.pop(navd_files.index(new_name))            
        smp.save(smp_out_dir+new_name)
        #print
for file in navd_files:
    shutil.copy(smp_in_dir+file,smp_out_dir+file)
