import numpy as np
import calc_prism as cp

p_trap = {}
p_trap['g'] = 9.81
p_trap['y'] = 0.5
p_trap['Q'] = 1.0
p_trap['b'] = 1.5
p_trap['m'] = 1.0
a_trap = cp.area_trap(p_trap)
b1_trap = cp.width_trap(p_trap)
#print a_trap,b1_trap
p_trap['v'] = p_trap['Q'] / a_trap
#print p_trap['v']
f_trap = cp.f_trap(p_trap)
#print f_trap

e_trap = cp.e_trap(p_trap)
#print e_trap

p_rect = {}
p_rect['b'] = 1.5
p_rect['g'] = 9.81
p_rect['Q'] = 1.0

y = np.arange(0.0001,2.0,0.0001)

rect_depths = cp.find_depths(e_trap,y,p_rect,cp.e_rect)
#print rect_depths
p_rect['y'] = rect_depths[1]

p_rect['q'] = p_rect['Q'] / p_rect['b']

yc = cp.yc_rect(p_rect)
print yc

p_rect['y'] = yc
e_c_rect = cp.e_rect(p_rect)
print e_c_rect

q2c = ((2.0/3.0) * (e_c_rect))**(3.0/2.0) * (9.9)**0.581
print q2c

print p_rect['Q'] / q2c