import sys
import numpy as np
import arrayUtil as au

refs = ['h_thk.ref','q5_thk.ref','q4_thk.ref']
array = np.loadtxt('ref\\'+refs[0])
array = array + np.loadtxt('ref\\'+refs[1])
array = array + np.loadtxt('ref\\'+refs[2])
np.savetxt('h_q5_q4_thk.ref',array,fmt'%15.6e')
    
