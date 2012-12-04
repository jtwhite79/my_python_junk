import os
import pestUtil

smp_dir = 'raw_smp\\'
smp_files = os.listdir(smp_dir)

for smp_file in smp_files:
    print smp_file
    smp = pestUtil.smp(smp_dir+smp_file,load=True)
    smp.make_unique()
    smp.save('test\\'+smp_file)
