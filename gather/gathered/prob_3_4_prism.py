import numpy as np
import calc_prism as cp

p_dict = {}
p_dict['g'] = 9.81
p_dict['Q'] = 0.30
p_dict['y'] = 0.15
p_dict['m'] = 2.0

p_dict['Y'] = np.arange(0.00001,1.0,0.00001)
m1 = cp.m_tri(p_dict)
f_tri = cp.f_tri(p_dict)
yc_tri = cp.yc_tri(p_dict)
print f_tri,yc_tri

conj_ys = cp.find_depths(m1,p_dict['Y'],p_dict,cp.m_tri)
print conj_ys