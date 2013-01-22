import os
from datetime import datetime

smp_dir = 'UMD.01\\obsref\\head\\'
smp_files = os.listdir(smp_dir)

for smp_file in smp_files:
    print smp_file
    f = open(smp_dir+smp_file,'r')
    lines = []
    site_name = smp_file.split('.')[0]
    if len(site_name) > 8:
        site_name = site_name[:8]
    for line in f:
        raw = line.strip().split()
        raw[0] = site_name
        #dt = datetime.strptime(raw[1],'%Y-%m-%d')
        #raw[1] = dt.strftime('%m/%d/%Y')
        lines.append('  '.join(raw)+'\n')
    f.close()
    f = open(smp_dir+smp_file,'w')
    for line in lines:
        f.write(line)
    f.close()
        
             
