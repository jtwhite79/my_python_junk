import os
import sys
from datetime import datetime,timedelta
from bro import flow

#--load and parse rech file names
rech_files = os.listdir(flow.ref_dir+'rch\\')
rech_dts = []
for rfile in rech_files:
    dt_str = rfile.split('.')[0].split('_')[2]
    dt = datetime.strptime(dt_str,'%Y%m%d')
    rech_dts.append(dt)

rech = zip(rech_dts,rech_files)
rech.sort()

f = open(flow.root+'.xxx','w',0)
f.write('# '+sys.argv[0]+' '+str(datetime.now())+'\n')

items = ['POINT RECHARGE','NEXRAD RECHARGE']
f.write('{0:10d}{1:10d}\n'.format(len(items),203))
f.write('{0:20s}{1:10s}{2:10s}{3:10s}\n'.format('#NAME','NDIM','NOPT','NMULT'))
for item in items:
    f.write('{0:20s}{1:10d}{2:10d}{3:10d}\n'.format(item,2,1,1))
