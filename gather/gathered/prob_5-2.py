import sys
import math
import numpy as np
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 32.2
p_dict['b'] = 20.0
p_dict['m'] = 3.0
p_dict['n']= 0.025
p_dict['s']= 0.001

p_dict['kn'] = 1.49

H_res = 10.0

#--eq 5.9



Y = np.arange(7.0,10.0,0.01)
Q = np.arange(2000.0,3000,0.1)

r_f = 1.0e+20
correct_y = -999
correct_f = -999
correct_Q = -999
r_h = 1.0e+20
#tol_f = 0.01
#tol_h = 0.01
trap = cpc.trap(p_dict)
#sys.exit()
for y in Y:
    p_dict['y'] = y
    trap.set('y',y)
    this_Q = (p_dict['kn']/p_dict['n']) * trap.area() * trap.r()**(2.0/3.0) * p_dict['s']**0.5
    sec_term = (this_Q**2/(2.0*p_dict['g']*(trap.area()**2)))
    h = y + sec_term
    #print y,q,sec_term,h                          
    this_r_h = abs(h - H_res)        
    if this_r_h < r_h :
        r_h = this_r_h                        
        correct_y = y
        p_dict['Q'] = this_Q
        #correct_f = cp.f_trap(p_dict)
        correct_Q = this_Q     
    
print 'y,Q,r_h',correct_y,correct_Q,r_h     
