import os
import shutil
files = os.listdir('src_fixed')

for fi in files:
    if fi.endswith('f'):
        #shutil.copy('src_fixed\\'+f,f.split('.')[0]+'.f90')
        f = open('src_fixed\\'+fi,'r')
        f_out = open('src_free\\'+fi.split('.')[0]+'.f90','w')
        for line in f:
            if line[0] == 'c' or line[0] == '*':
                line = '!'+line[1:]
            f_out.write(line)
        f.close()
        f_out.close()
        