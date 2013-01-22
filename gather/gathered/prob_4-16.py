import math
import numpy as np
import calc_prism as cp



p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 3.0
p_dict['m'] = 3.0
p_dict['Q'] = 2.0

nm_2_lbft = 47.9

kn = 1.0
s = 0.01
rho = 1000.0
gamma = p_dict['g'] * rho

d50 = 70.0 #mm
d50 /= 1000.0 #m

tao_bot_crit = 4.0 * (d50 * 3.281) # in lbs/ft2
tao_bot_crit *= 47.9

Y = np.arange(0.001,10.0,0.001)
r = 1.0e+20
correct_y1 = -999
correct_n = -999
for y in Y:
    p_dict['y'] = y
    rh = cp.r_trap(p_dict)
    n_numer = d50**(1.0/6.0) * ((kn / (8.0*p_dict['g'])**0.5)) * (rh/d50)**(1.0/6.0)
    n_demon = 0.794 + (1.85 * np.log10(rh/d50))
    n = n_numer / n_demon
    rhs = (n * p_dict['Q']) / (kn * (s**0.5))
    lhs = (cp.area_trap(p_dict)**(5.0/3.0)) /  (cp.p_trap(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y
        correct_n = n
print 'y',correct_y1
print 'n',correct_n
tao_bot_max = gamma * correct_y1 * s
print 'tao_crit,tao_max',tao_bot_crit,tao_bot_max