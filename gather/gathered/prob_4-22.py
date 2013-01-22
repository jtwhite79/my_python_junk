import math
import numpy as np
import calc_prism as cp



p_dict = {}
p_dict['g'] = 32.2
p_dict['m'] = 1.0/(3.0)**0.5
p_dict['Q'] = 1500.0

#nm_2_lbft = 47.9
n = 0.015
kn = 1.49
s = 0.0005

Y = np.arange(0.001,20.0,0.001)
r = 1.0e+20
correct_y1 = -999
correct_n = -999
correct_b = -999
for y in Y:
    p_dict['y'] = y
    p_dict['b'] = (2.0/3.0) * y * (3.0)**0.5
    rh = cp.r_trap(p_dict)
    rhs = (n * p_dict['Q']) / (kn * (s**0.5))
    lhs = (cp.area_trap(p_dict)**(5.0/3.0)) /  (cp.p_trap(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y
        correct_n = n
        correct_b = p_dict['b']
print 'y',correct_y1
p_dict['y'] = correct_y1
print 'f',cp.f_trap(p_dict)
print 'n',correct_n
print 'b',correct_b