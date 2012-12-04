import os
import pylab
import pestUtil as pu


smp_dir = 'stage_smp_full\\'
smp_files = os.listdir(smp_dir)
plt_dir = 'png\\'
for sfile in smp_files:
    smp = pu.smp(smp_dir+sfile,load=True)
    #smp.plot(plt_dir+sfile.split('.')[0]+'.png')
    ax = smp.plot(None)
    pylab.show()
    break

