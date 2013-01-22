import numpy as np
import calc_prism as cp

y = 10.0
v = 10.0

ys = np.arange(0.001,10.0,0.001)
p_circ = {}
p_circ['y'] = 7.34
p_circ['g'] = 32.2
p_circ['Q'] = 262.
p_circ['d'] = 9.18
a_circ = cp.area_circ(p_circ)
print a_circ
b_circ = cp.width_circ(p_circ)
print b_circ
p_circ['v'] = 262.0/a_circ

f_circ = cp.f_circ(p_circ)
print f_circ


