import numpy as np
import calc_prism as cp

p_dict = {}
p_dict['g'] = 9.81
p_dict['d'] = 1.8
p_dict['y'] = 0.7
p_dict['Q'] = 2.8
f = cp.f_circ(p_dict)
m = cp.m_circ(p_dict)
y = np.arange(0.0001,1.7,0.0001)
conj_ys = cp.find_depths(m,y,p_dict,cp.m_circ)

print f,conj_ys