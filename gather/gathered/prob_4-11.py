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
p_dict['g'] = 9.81

p_dict['Q'] = 1.0
n = 0.015
kn = 1.0
s = 0.0018
p_dict['Q'] = 1.0
p_dict['d'] = np.ceil(1.56 * ((n * p_dict['Q'])/(kn * s**0.5))**(3.0/8.0))
p_dict['d'] = 1.5
print 'd',p_dict['d']

rhs = (n * p_dict['Q']) / (kn * (s**0.5))

tol = 1.0e+20
Y = np.arange(0.001,p_dict['d'],0.001)
r = 1.0e+20
correct_y1 = -999
correct_f = -999
correct_re = -999
for y in Y:
    p_dict['y'] = y
    #re = cp.re_circ(p_dict)
    #f = find_f(re)
    #lhs = (p_dict['Q'] * (f**0.5)) / ((8.0 * p_dict['g'] * s)**0.5)
    #rhs = cp.area_circ(p_dict) * cp.r_circ(p_dict)**0.5
    lhs = (cp.area_circ(p_dict)**(5.0/3.0)) /  (cp.p_circ(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y        

print 'y,',correct_y1
p_dict['y'] = correct_y1

p_dict['v'] = p_dict['Q'] / cp.area_circ(p_dict)

froude = cp.f_circ(p_dict)

print 'v,fr',p_dict['v'],froude


p_dict['Q'] = 0.2
rhs = (n * p_dict['Q']) / (kn * (s**0.5))

r = 1.0e+20
correct_y1 = -999
correct_f = -999
correct_re = -999
for y in Y:
    p_dict['y'] = y
    #re = cp.re_circ(p_dict)
    #f = find_f(re)
    #lhs = (p_dict['Q'] * (f**0.5)) / ((8.0 * p_dict['g'] * s)**0.5)
    #rhs = cp.area_circ(p_dict) * cp.r_circ(p_dict)**0.5
    lhs = (cp.area_circ(p_dict)**(5.0/3.0)) /  (cp.p_circ(p_dict)**(2.0/3.0))
    this_r = abs(lhs-rhs)
    if this_r < r:
        r = this_r
        correct_y1 = y        

print 'y,',correct_y1
p_dict['y'] = correct_y1

p_dict['v'] = p_dict['Q'] / cp.area_circ(p_dict)

froude = cp.f_circ(p_dict)

print 'v,fr',p_dict['v'],froude

tao_c = 2.0
rho = 1000.0
u_star_c = (tao_c / rho)**0.5
af = 3.14159 * 0.5**2

a_af = cp.area_circ(p_dict) / af
print 'y/d,a/af,u_star_c',p_dict['y']/p_dict['d'],a_af,u_star_c
vc_star = 0.74 #from figure 4.11

vc = (vc_star * kn * u_star_c * p_dict['d']**(1.0/6.0)) / (n * p_dict['g']**0.5)
print 'vc',vc
