import math
import numpy as np
import calc_prism as cp



p_dict = {}
p_dict['g'] = 9.81
p_dict['m'] = 3.0
p_dict['b'] = 1.5
tao_perm = 29.0

avg_hgt = 10.0 #m
mei = 0.05

kn = 1.0
s = 0.012
rho = 1000.0
gamma = p_dict['g'] * rho

p_dict['y'] = tao_perm / (gamma * s)
rh = cp.r_trap(p_dict)
tao = gamma * rh * s
print tao
u_c_star = 0.028 + 6.33*mei**2
if u_c_star > 0.23*mei**0.106:
    u_c_start = 0.23*mei**0.106

k = avg_hgt * 0.14  * (((mei/tao)**0.25)/avg_hgt)**1.59

u_star = (p_dict['g'] * rh * s)**0.5
ratio = u_star/u_c_star
if ratio <= 1.0:
    a,b = 0.15,1.85
elif ratio > 1.0 and ratio <= 1.5:
    a,b = 0.2,2.7
elif ratio > 1.5 and ratio <=2.5:
    a,b = 0.28,3.08
else:
        a,b = 0.29,3.5
print a,b
n_term1 =  kn /((8.0*p_dict['g'])**0.5)
n_term2 = ((rh/k)**(1.0/6.0)/(a + (b * math.log10(rh/k))))
n = n_term1 * n_term2 * k**(1.0/6.0)

area = cp.area_trap(p_dict)
print area
Q = (kn/n) * cp.area_trap(p_dict) * rh**(2.0/3.0) * s**0.5
print Q,p_dict['y'],rh,tao,k,n
#
#Y = np.arange(0.001,10.0,0.001)
#r = 1.0e+20
#correct_y1 = -999
#correct_n = -999
#correct_tao = -999
#correct_v = -999
#for y in Y:
#    p_dict['y'] = y
#    rh = y
#    tao = gamma * y * s
#    u_star = (p_dict['g'] * rh * s)**0.5
#    ratio = u_star/u_c_star
#    if ratio <= 1.0:
#        a,b = 0.15,1.85
#    elif ratio > 1.0 and ratio <= 1.5:
#        a,b = 0.2,2.7
#    elif ratio > 1.5 and ratio <=2.5:
#        a,b = 0.28,3.08
#    else:
#        a,b = 0.29,3.5
#          
#    
#    n_term1 = k * kn /((8.0*p_dict['g'])**0.5)
#    n_term2 = ((rh/k)**(1.0/6.0)/(a + (b * math.log(rh/k))))
#    n = n_term1 * n_term2
#    v = (kn/n)*rh*(s**0.5)
#    #print n
#    #rhs = (n * p_dict['Q']) / (kn * (s**0.5))
#    #lhs = (cp.area_rect(dict)**(5.0/3.0)) /  (cp.p_rect(p_dict)**(2.0/3.0))
#    this_r = abs(tao-tao_perm)
#    if this_r < r:
#        r = this_r
#        correct_y1 = y
#        correct_n = n
#        correct_tao = tao
#        correct_v = v
#print 'y',correct_y1
#print 'n',correct_n
#print 'q',correct_y1 * correct_v
#tao_bot_max = gamma * correct_y1 * s
#print 'tao_perm,tao_max',tao_perm,correct_tao