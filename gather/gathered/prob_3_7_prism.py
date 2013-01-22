import math
import numpy as np
import pylab

import calc_prism as cp     
 
#--tri params    
p_dict = {}   
p_dict['y'] = 1.12
p_dict['v'] = 60.0
p_dict['g'] = 32.2
p_dict['q'] = 60.0 * 1.12
f = cp.f_rect(p_dict)
m = cp.m_rect(p_dict)
print 'approach F: ',f
y = np.arange(0.001,100.0,0.001)
conj_depths = cp.find_depths(m,y,p_dict,cp.m_rect)
print conj_depths
#--find conjugates
#
#conj_c = cp.find_depths(m,y,p_dict,cp.m_tri)
#print conj_c
