import sys
import numpy as np
import datetime

f = open(sys.argv[1],'r')
f_out = open(sys.argv[1].split('.')[0]+'_ord.dat','w')
header = f.readline()
for line in f:
    raw = line.strip().split()
    rawdate = raw[2].split('-')
    ord = datetime.date(int(rawdate[0]),int(rawdate[1]),int(rawdate[2])).toordinal()
    try:
        f_out.write(str(ord)+' '+raw[3]+'\n')
    except:
        print line
    
f.close()
f_out.close()
    