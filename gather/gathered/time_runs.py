import os
import time

exe_omp = 'predunc5.exe <1.in'
exe_serial = 'predunc5_serial.exe <1.in'

omp_start = time.time()
os.system(exe_omp)
elapsed_omp = (time.time() - omp_start)

serial_start = time.time()
os.system(exe_serial)
elapsed_serial = (time.time() - serial_start)


print '\n\n\n\n\n'
print 'omp,serial',elapsed_omp,elapsed_serial