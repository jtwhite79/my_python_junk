import sys
import math
import numpy as np
import calc_prism as cp

    
p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 10.0

n = 0.030
s = 0.005

kn = 1.0

H_res = 3.50

#--eq 5.9
Y = np.arange(0.01,3.5,0.01)
Q = np.arange(1.0,200.0,1.0)

r_f = 1.0e+20
correct_y = -999
correct_f = -999
correct_Q = -999
#tol_f = 0.01
#tol_h = 0.01
for y in Y:
    p_dict['y'] = y
    #print y
    r_h = 1.0e+20
    correct_Q_temp = ((H_res - y)*(2.0*p_dict['g']*(cp.area_rect(p_dict)**2)))**0.5     
    p_dict['Q'] = correct_Q_temp        
    f = cp.f_rect(p_dict)
    
    print y,f,correct_Q_temp,r_h
    if abs(f-1.0) < r_f:
        r_f = abs(f-1.0)
        correct_y = y
        correct_f = f
        correct_Q = correct_Q_temp    
    #this_r_f = abs(f - 1.0) 
    #break 
print r_h,r_f
print 'y,f,Q,r_f',correct_y,correct_f,correct_Q,r_f
p_dict['y'] = correct_y
p_dict['Q'] = correct_Q
numer = n**2 * p_dict['Q']**2
demon = kn**2 * cp.area_rect(p_dict)**2 * cp.r_rect(p_dict)**(4.0/3.0)
so_crit = numer/demon
print so_crit

r_f = 1.0e+20
correct_y = -999
correct_f = -999
correct_Q_mild = -999
r_h = 1.0e+20
#tol_f = 0.01
#tol_h = 0.01
for y in Y:
    p_dict['y'] = y
    this_Q = (kn/n) * cp.area_rect(p_dict) * cp.r_rect(p_dict)**(2.0/3.0) * s**0.5
    p_dict['Q'] = this_Q
    sec_term = (this_Q**2/(2.0*p_dict['g']*(cp.area_rect(p_dict)**2)))
    h = y + sec_term
    #print y,q,sec_term,h                          
    this_r_h = abs(h - H_res)        
    if this_r_h < r_h :
        r_h = this_r_h                        
        correct_y = y
        p_dict['Q'] = this_Q
        correct_f = cp.f_rect(p_dict)
        correct_Q_mild = this_Q     
    
print 'y0,Q0,r_h',correct_y,correct_Q_mild,r_h     

