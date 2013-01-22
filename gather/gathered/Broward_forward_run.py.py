import sys
import os
import subprocess as sp
from datetime import datetime

start = datetime.now()

cal_dir = 'bro.02\\calibration\\'
cal_flowexe = 'mfnwt-SWR_x64.exe'
cal_flowname = 'flow'
cal_seawatexe = 'swt_v4x64.exe'
cal_seawatname = 'seawat'

pred_dir = 'bro.02\\prediction\\'
pred_flowexe = 'mfnwt-SWR_x64.exe'
pred_flowname = 'flow'
pred_seawatexe = 'swt_v4x64.exe'
pred_seawatname = 'seawat'

#--open a log file
f_log = open('Broward_forward_run.log','w',0)
f_log.write(str(start)+' - starting forward run\n\n')


#-------------------------------------------------------------------------
#--some preliminaries
sys.path.append(cal_dir+'python\\')
import broward_cali_utilities as bcu


#-------------------------------------------------------------------------
#--run cali flow model prep utilities

#-------------------------------------------------------------------------
#--run cali flow model
try:
    success = False
    proc = sp.Popen([cal_flowexe,cal_flowname+'.nam'],stdout=sp.PIPE,cwd=cal_dir)
    while True:
        line = proc.stdout.readline()
        c = line.split('\r')
        print c[0]
        if line == '':
            break
        elif 'normal' in line.lower():
            success = True
        
    if not success:
        message = "cali flow model did not terminate normally"
        f_log.write(message)
        raise Exception(message)
except:
    message = "error runing cali flow model" + str(sys.exc_info())
    f_log.write(message)
    raise



#-------------------------------------------------------------------------
#--run cali flow 2 cali seawat utilities
try:
    bcu.flow_2_seawat(cal_dir+cal_flowname,cal_dir+cal_seawatname)
except:
    message = 'error translating cali swr results to seawat'
    f_log.write(message)
    raise Exception(message)

#-------------------------------------------------------------------------
#--run cali seawat model
try:
    success = False
    proc = sp.Popen([cal_seawatexe,cal_seawatname+'.nam_swt'],stdout=sp.PIPE,cwd=cal_dir)
    while True:
        line = proc.stdout.readline()
        c = line.split('\r')
        print c[0]
        if line == '':
            break
        elif 'normal' in line.lower():
                success = True        
    if not success:
        message = "cali seawat model did not terminate normally"
        f_log.write(message)
        raise Exception(message)
except:
    message = "error runing cali seawat model" + str(sys.exc_info())
    f_log.write(message)
    raise


#-------------------------------------------------------------------------
#--get results from cali

#-------------------------------------------------------------------------
#--run cali flow 2 pred flow utilities

#-------------------------------------------------------------------------
#--run cali seawat 2 pred seawat utilities

#-------------------------------------------------------------------------
#--run pred flow model

#-------------------------------------------------------------------------
#--run pred flow 2 pred seawat utilities

#-------------------------------------------------------------------------
#--run pred seawat model

#-------------------------------------------------------------------------
#--get results from pred



f_log.close()

