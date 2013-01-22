import math
import numpy as np
import pylab

import calc_prism as cp

delta_z = 3.279

p_circ = {}
p_circ['Q'] = 262.0
p_circ['d'] = 9.18
p_circ['y'] = 7.34
p_circ['g'] = 32.2
a = cp.area_circ(p_circ)
b = cp.width_circ(p_circ)
p_circ['v'] = p_circ['Q'] / a
e = cp.e_circ(p_circ)
f = cp.f_circ(p_circ)
print a,b,e,f
                                 
e2 = e - delta_z                                            

p_rect = {}
p_rect['g'] = 32.3
p_rect['b'] = 6.56
p_rect['q'] = p_circ['Q'] / 6.56
yc2 = cp.yc_rect(p_rect)
p_rect['y'] = yc2
ec2 = cp.e_rect(p_rect)
print yc2,ec2                
if e2 < ec2:
    print 'choking downstream'
    new_e1 = ec2 + delta_z
    print new_e1
    ys = np.arange(0.0001,9.17,0.0001)
    new_alt_ys = cp.find_alternate_depths(new_e1,ys,p_circ,cp.e_circ)
    print new_alt_ys
    

                                            