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
print a_trap,b1_trap
p_trap['v'] = p_trap['Q'] / a_trap
print p_trap['v']
f_trap = cp.f_trap(p_trap)
print f_trap