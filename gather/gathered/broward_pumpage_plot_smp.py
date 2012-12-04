import os
import numpy as np
import pylab
import shapefile
import pestUtil as pu

#smp_dir = 'pws_smp\\'
#smp_files = os.listdir(smp_dir)
#smp_files = os.listdir(smp_dir)#convert = 7.481/24.0/60.0 #to gpm

smp_dir ='.\\'
smp_files = ['sum.smp']
convert = 7.481/1.0e6/30 #to mgd - approx 30 days in a month
plt_dir = 'png\\'
f_out = open('missing.dat','w')
  
for smp_file in smp_files:
        print smp_file
        smp = pu.smp(smp_dir+smp_file,load=True)
        for site,record in smp.records.iteritems():
            smp.records[site][:,1] *= convert
        ax = smp.plot(None)
        pylab.show()
pass


