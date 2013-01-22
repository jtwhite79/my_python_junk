import numpy as np
import calc_prism as cp

y = 10.0
v = 10.0

ys = np.arange(0.001,10.0,0.001)
p_trap = {}
p_trap['y'] = 22.0
p_trap['g'] = 32.2
p_trap['Q'] = 12600.0
p_trap['m'] = 2.0
p_trap['b'] = 75.0
a_trap = cp.area_trap(p_trap)
print a_trap
b_trap = cp.width_trap(p_trap)
print b_trap
p_trap['v'] = 12600.0/a_trap

f_trap = cp.f_trap(p_trap)
print f_trap


