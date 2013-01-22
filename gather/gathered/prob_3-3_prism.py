import math
import numpy as np
import pylab

import calc_prism as cp


#--tri params
p_tri = {}    
p_tri['g'] = 9.81
p_tri['m'] = 2.0    
p_tri['y'] = 0.15 #m
p_tri['Q'] = 0.3


mc1 = cp.m_tri(p_tri)
print 'approach momentum: ',mc1

#--find conjugates
y = np.arange(0.1,1.0,0.00001)
conj_c = cp.find_depths(mc1,y,p_tri,cp.m_tri)

   
print conj_c
