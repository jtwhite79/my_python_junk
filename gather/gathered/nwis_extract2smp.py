import os
import re
import shutil
from datetime import datetime

'''output smp files get a generic "site" name.
'''
def parse_line(line):
    line = line.replace(' ','')
    line = line.replace(',','')
    line = line.replace('/','_')
    raw = line.strip().split('|')
    return raw

def build_name(raw,dtypes,a_idx,s_idx,n_idx,p_idx):
    raw_dtype = raw[p_idx]
    dt = None
    for d in dtypes:
        if re.search(d,raw_dtype,re.I) != None:
            dt = d
    if dt is None:
        print raw
        raise TypeError('data type not found:'+str(raw_dtype))
    strg = raw[a_idx]+'.'+raw[s_idx]+'.'+raw[n_idx]+'.'+dt
    return strg


#--dtypes dict
#dtypes = {'spec':['Specific cond at 25C','SpecCondwu25degCLab'],'ngvd':['Elevation above NGVD',
dtypes = ['spec','ngvd','navd','chloride','dissolved']


files = ['broward_gw_dv_data-1.csv','broward_gw_dv_data-2.csv','broward_qw_result_data.csv','broward_wl_result_data.csv']
agy_idx = 0
site_idx = 1
name_idx = 2
param_idx = 3
val_idx = 6
dt_idx = 5
#--since parse line replaces forward slashes with underscores
dt_infmt = '%m_%d_%Y'
dt_outfmt = '%d/%m/%Y'

data_dir = 'spreadsheet_data\\'
output_dir = 'raw_smp\\'
site_file_names = []
not_sorted = []
site_lnum = []
for file in files:
    #--read through once to build a list of site file names and check for sorting by site no
    print file
    f = open(data_dir+file,'r')
    header = f.readline().strip().split('|')
    for i,line in enumerate(f):
        raw = parse_line(line)                      
        try:
            sf_name = build_name(raw,dtypes,agy_idx,site_idx,name_idx,param_idx)
        except TypeError:
            print 'line number ',i+2
            raise TypeError
        if sf_name not in site_file_names:
            site_file_names.append(sf_name)
            site_lnum.append(i+2)
        #--check that everything is sorted
        else:
            if site_file_names.index(sf_name) != len(site_file_names)-1:
                if sf_name not in not_sorted:
                    #raise IndexError('the records are not sorted'+sf_name+'. need to sort')
                    print 'duplicate record'+sf_name+' on line',i+2
                    print 'original record line number:',site_lnum[site_file_names.index(sf_name)]
                    
                    not_sorted.append(sf_name)

    f.close()

if len(not_sorted) > 0:
    sys.exit()

#--create a new dir for each parameter type
#shutil.rmtree(output_dir)
try:
    os.mkdir(output_dir)
except:
    pass

for file in files:
    #--now write the records as smp files - slow
    f = open(data_dir+file,'r')
    header = f.readline().strip().split('|')
    prev = site_file_names[0]
    f_out = open(output_dir+prev+'.smp','w')    
    for i,line in enumerate(f):
        raw = parse_line(line)
        #print raw
        dt = datetime.strptime(raw[dt_idx],dt_infmt)
        if raw[val_idx] != '':
            try:
                val = float(raw[val_idx])
            except ValueError:
                print raw
                raise ValueError
            sf_name = build_name(raw,dtypes,agy_idx,site_idx,name_idx,param_idx)
            if sf_name != prev:                
                f_out.close()                
                f_out = open(output_dir+sf_name+'.smp','w')
                prev = sf_name 
                print sf_name           
            f_out.write('site'.ljust(10)+' '+dt.strftime(dt_outfmt)+' 00:00:00 {0:15.6e}\n'.format(val))            

