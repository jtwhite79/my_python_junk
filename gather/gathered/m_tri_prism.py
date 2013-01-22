import math
import numpy as np
import pylab

import calc_prism as cp     
 
#--tri params    
p_dict = {}
p_dict['m'] = 2.0    
p_dict['y'] = 0.15 #m
p_dict['Q'] = 0.3
p_dict['g'] = 9.81

m = cp.m_tri(p_dict)
print 'approach momentum: ',m

#--find conjugates
y = np.arange(0.1,1.0,0.00001)
conj_c = cp.find_depths(m,y,p_dict,cp.m_tri)
print conj_c
