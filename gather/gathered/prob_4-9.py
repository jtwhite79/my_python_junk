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
p_dict['d'] = 1.5
p_dict['y'] = 0.8
p_dict['u'] = 1.2e-5

target_v = 2.0
kn = 1.49

tol = 1.0e+20
S = np.arange(0.001,0.005,0.0001)
Q = np.arange(0.01,2.0,0.01)
r = 1.0e+20

for s in S:
    r1 = 1.0e+20
    for q in Q:
        p_dict['Q'] = q
        re = cp.re_circ(p_dict)
        f = find_f(re)        
        lhs = (p_dict['Q'] * (f**0.5)) / ((8.0 * p_dict['g'] * s)**0.5)
        rhs = cp.area_circ(p_dict) * cp.r_circ(p_dict)**0.5
        #print lhs,rhs,q
        this_r = abs(lhs-rhs)
        if this_r < r1:
            r1 = this_r
            correct_Q = q
            correct_f = f
            correct_re = re
    
    this_v = correct_Q / cp.area_circ(p_dict)
    #print s,correct_Q,this_v
    #break
    this_r = abs(this_v - target_v)
    if this_r < r:
        r = this_r
        correct_s = s
        correct_Q1 = correct_Q   
        correct_f1 = correct_f
        correct_re1 = correct_re


print 's,Q1,f,re',correct_s,correct_Q1,correct_f1,correct_re1
n = 0.015
r = 1.0e+20

for s in S:
    r1 = 1.0e+20
    for q in Q:
        p_dict['Q'] = q
        lhs = (cp.area_circ(p_dict)**(5.0/3.0)) /  (cp.p_circ(p_dict)**(2.0/3.0))        
        rhs = (n * p_dict['Q']) / (kn * (s**0.5))
        #print lhs,rhs,q
        this_r = abs(lhs-rhs)
        if this_r < r1:
            r1 = this_r
            correct_Q = q
            correct_f = f
            correct_re = re
    
    this_v = correct_Q / cp.area_circ(p_dict)
    #print s,correct_Q,this_v
    #break
    this_r = abs(this_v - target_v)
    if this_r < r:
        r = this_r
        correct_s = s
        correct_Q1 = correct_Q   
        correct_f1 = correct_f
        correct_re1 = correct_re


print 's,Q1,f,re',correct_s,correct_Q1,correct_f1,correct_re1


