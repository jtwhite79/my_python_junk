import os
import shutil

#--files to copy out
cfiles = ['test.dat']

#--remote slave dir
slave_dir = 'Home\\jwhite\\miamidade'

#--get a nodelist 
nodes = ['\\\\IGSBAMESMS150\\']
f = open('nodes.dat','r')
for line in f:
    if not line.startswith('#'):
        nodes.append(line.strip())
f.close()

for f in cfiles:
    fullname = slave_dir+f
    if not os.path.exists(fullname):
        shutil.copy(cfile,fullname)




