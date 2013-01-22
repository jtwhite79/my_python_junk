import numpy as np
import calc_prism as cp



p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 10.0
p_dict['Q'] = 12.0
p_dict['y1'] = 2.0

kn = 1.0
s = 0.002
n = 0.015

rhs = (n * p_dict['Q']) / (kn * (s**0.5))
Y = np.arange(0.001,2.0,0.001)
r = 1.0e+20
correct_y1 = -999

for y in Y:
    p_dict['y'] = y
    lhs = (cp.area_para(p_dict)**(5.0/3.0)) /  (cp.p_para(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y
print 'y',correct_y1
p_dict['y'] = correct_y1
print 'f1',cp.f_para(p_dict)
p_dict['Y'] = Y
yc1 = cp.yc_para(p_dict)
print 'yc1',yc1
p_dict['y'] = yc1
print 'fc1',cp.f_para(p_dict)

s = 0.02
rhs = (n * p_dict['Q']) / (kn * (s**0.5))
r = 1.0e+20
correct_y2 = -999

for y in Y:
    p_dict['y'] = y
    lhs = (cp.area_para(p_dict)**(5.0/3.0)) /  (cp.p_para(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y2 = y
print 'y2',correct_y2
p_dict['y'] = correct_y2
print 'f2',cp.f_para(p_dict)
p_dict['Y'] = Y
yc2 = cp.yc_para(p_dict)
print 'yc2',yc2
p_dict['y'] = yc2
print 'fc2',cp.f_para(p_dict)





