import sys
import math
import numpy as np
import calc_prism as cp

def find_f(re):
    F = np.arange(0.0001,0.1,0.0001)
    r = 1.0e+20
    correct_f = -999.0
    for f in F:
        lhs = 1.0 / math.sqrt(f)
        rhs = (2.0 * np.log10(re * math.sqrt(f))) - 0.8
        this_r = abs(lhs - rhs)
        if this_r < r:
            r = this_r
            correct_f = f
    if correct_f == -999.0:
        print 'warning - correct f not found'
        raise ValueError
    return correct_f



p_dict = {}
p_dict['g'] = 32.2
p_dict['d'] = 2.0
p_dict['Q'] = 20.0
p_dict['u'] = 1.2e-5

kn = 1.49
s = 0.005

tol = 1.0e+20
Y = np.arange(0.001,1.0,0.001)
r = 1.0e+20
correct_y1 = -999
correct_f = -999
correct_re = -999
for y in Y:
    p_dict['y'] = y
    re = cp.re_circ(p_dict)
    f = find_f(re)
    lhs = (p_dict['Q'] * (f**0.5)) / ((8.0 * p_dict['g'] * s)**0.5)
    rhs = cp.area_circ(p_dict) * cp.r_circ(p_dict)**0.5
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y
        correct_f = f
        correct_re = re

print 'y,f,re',correct_y1,correct_f,correct_re
p_dict['y'] = correct_y1

p_dict['v'] = p_dict['Q'] / cp.area_circ(p_dict)

froude = cp.f_circ(p_dict)

print 'v,fr',p_dict['v'],froude
