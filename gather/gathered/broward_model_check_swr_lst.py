import re
import numpy as np

reg = re.compile('REACH   =')

lst_file = 'bro.list'
f = open(lst_file,'r')

fields = ['pt','elev','xsecarea','vol','wetperm','topwidth','surfarea']
f_warn = open('swr_list.warn','w')
while True:
    line = f.readline()
    if line == '':
        break
    if reg.search(line) is not None:
        rnum = int(line.strip().split()[-1])
        rdata = []
        f.readline()
        f.readline()
        header = f.readline()
        f.readline()
        while True:
            line = f.readline()
            if line.strip() == '':
                break
            raw = line.strip().split()
            pt = int(raw[0])
            vals = [pt]
            for r in raw[1:]:
                vals.append(float(r))
            rdata.append(vals)
           
        #--check for zero wetted perimeter
        rdata = np.array(rdata)
        if rdata[:,4].sum() == 0:            
            f_warn.write(str(rnum)+'\n')
f.close()
f_warn.close()