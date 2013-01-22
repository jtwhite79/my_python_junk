import math
import numpy as np
import pylab



def find_depths(target,y_array,p_dict,function):
    
    #--calculate the residuals
    rs = np.zeros_like(y_array)
    mins = []
    for idx in range(y_array.shape[0]):
        #--calc this_e
        p_dict['y'] = y_array[idx]
        this_val = function(p_dict)
        #--calc this residual
        this_r = abs(this_val - target)
        rs[idx] = this_r
        
    #--loop over the residuals looking for minimums
    mins = []
    for idx in range(1,rs.shape[0]-1):
        if rs[idx] < rs[idx-1] and rs[idx] < rs[idx+1]:
            mins.append(idx)
    
    return y_array[mins]




#-----------------------------------------------------------
#--rect section
def dh_rect(p_dict):
    return p_dict['y']

def area_rect(p_dict):
    return p_dict['y'] * p_dict['b']

def width_rect(p_dict):
    return p_dict['b']

def p_rect(p_dict):
    p = p_dict['b'] + (2.0 * p_dict['y'])
    return p

def r_rect(p_dict):
    r = area_rect(p_dict) / p_rect(p_dict)
    return r

def f_rect(p_dict):
    try:
        return p_dict['v'] / (p_dict['g'] * dh_rect(p_dict))**0.5
    except:
        try:
            v = p_dict['q'] / p_dict['y']        
            return v / (p_dict['g'] * dh_rect(p_dict))**0.5
        except:
            v = p_dict['Q'] / area_rect(p_dict)
            return v / (p_dict['g'] * dh_rect(p_dict))**0.5

def yc_rect(p_dict):
    try:
        return (p_dict['q']**2 / p_dict['g'])**(1.0/3.0)
    except:

        r = 1.0e+20
        yc = -999
        for y in p_dict['Y']:
            p_dict['y'] = y
            this_val = (p_dict['Q']**2 * width_rect(p_dict)) / (p_dict['g'] * area_rect(p_dict)**3)            
            this_r = abs(this_val - 1.0)
            if this_r < r:
                r = this_r
                yc = y
        return yc 

def m_rect(p_dict):
    term1 = (p_dict['b'] * p_dict['y']**2) / 2.0
    term2 = p_dict['Q']**2/(p_dict['g'] * p_dict['b'] * p_dict['y'])
    m = term1 + term2   
    return m

def e_rect(p_dict):
    try:
        term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * area_rect(p_dict)**2)
        return p_dict['y'] + term2
    except:
        term2 = p_dict['q']**2 / (2.0 * p_dict['g'] * p_dict['y']**2)
        return p_dict['y'] + term2

def re_rect(p_dict):
    try:
        re = (p_dict['v'] * 4.0 * r_rect(p_dict)) / p_dict['u']
        return re
    except:
        v = p_dict['Q'] / area_rect(p_dict)
        re = (v * 4.0 * r_rect(p_dict)) / p_dict['u']
        return re

def y0_rect(p_dict):
    rhs = (p_dict['n'] * p_dict['Q']) / (p_dict['kn'] * (p_dict['s']**0.5))  
    r = 1.0e+20
    correct_y0 = -999    
    for y in p_dict['Y']:
        p_dict['y'] = y
        lhs = (area_rect(p_dict)**(5.0/3.0)) /  (p_rect(p_dict)**(2.0/3.0))
        this_r = abs(lhs-rhs)
        if this_r < r:
            r = this_r
            correct_y0 = y
    #print correct_y0
    if correct_y0 == p_dict['Y'][-1] or correct_y0 == p_dict['Y'][0]:
        print 'Y does not bracket solution'
        raise IndexError
        
    return correct_y0




#-----------------------------------------------------------
#--trap section
def dh_trap(p_dict):
    area = area_trap(p_dict)
    width = width_trap(p_dict)
    dh = area / width
    return dh

def area_trap(p_dict):
    return p_dict['y'] * (p_dict['b'] + (p_dict['m'] * p_dict['y']))

def width_trap(p_dict):
    return p_dict['b'] + (2.0 * p_dict['m'] * p_dict['y'])

def p_trap(p_dict):
    p = p_dict['b'] + (2.0 * p_dict['y'] * (1.0 + p_dict['m']**2)**0.5)
    return p

def r_trap(p_dict):
    r = area_trap(p_dict) / p_trap(p_dict)
    return r    
    
def f_trap(p_dict):
    try:
        return p_dict['v'] / (p_dict['g'] * dh_trap(p_dict))**0.5
    except:
        v = p_dict['Q'] / area_trap(p_dict)
        return v / (p_dict['g'] * dh_trap(p_dict))**0.5

def yc_trap(p_dict):    
    r = 1.0e+20
    yc = -999
    for y in p_dict['Y']:
        p_dict['y'] = y
        this_f = f_trap(p_dict)
        #this_val = (p_dict['Q']**2 * width_trap(p_dict)) / (p_dict['g'] * area_trap(p_dict)**3)        
        this_r = abs(this_f - 1.0)
        if this_r < r:
            r = this_r
            yc = y
    return yc 

def m_trap(p_dict):
    term1 = (p_dict['b'] * p_dict['y']**2)/2.0
    term2 = (p_dict['m'] * p_dict['y']**3)/3.0
    term3 = p_dict['Q']**2 / (p_dict['g']*p_dict['y']*(p_dict['b']+(p_dict['m']*p_dict['y'])))
    m = term1 + term2 + term3
    return m

def e_trap(p_dict):
    term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * area_trap(p_dict)**2)
    return p_dict['y'] + term2


def re_trap(p_dict):
    try:
        re = (p_dict['v'] * 4.0 * r_trap(p_dict)) / p_dict['u']
        return re
    except:
        v = p_dict['Q'] / area_trap(p_dict)
        re = (v * 4.0 * r_trap(p_dict)) / p_dict['u']
        return re

def y0_trap(p_dict):
    rhs = (p_dict['n'] * p_dict['Q']) / (p_dict['kn'] * (p_dict['s']**0.5))          
    r = 1.0e+20
    correct_y0 = -999    
    for y in p_dict['Y']:
        p_dict['y'] = y
        lhs = (area_trap(p_dict)**(5.0/3.0)) /  (p_trap(p_dict)**(2.0/3.0))
        this_r = abs(lhs-rhs)
        if this_r < r:
            r = this_r
            correct_y0 = y
    #print correct_y0
    if correct_y0 == p_dict['Y'][-1] or correct_y0 == p_dict['Y'][0]:
        print 'Y does not bracket solution'
        raise IndexError
        
    return correct_y0




#-----------------------------------------------------------
#--circular section
def dh_circ(p_dict):
    #print y,d   
   theta = theta_circ(p_dict)
   #print ' ',y,theta
   width = width_circ(p_dict)
   area = area_circ(p_dict)
   dh = area/width
   return dh

def area_circ(p_dict):
    theta = theta_circ(p_dict)
    #print 'theta',theta
    return (theta - math.sin(theta)) * p_dict['d']**2  /8.0

def width_circ(p_dict):
    theta = theta_circ(p_dict)
    return p_dict['d'] * math.sin(theta/2.0)

def p_circ(p_dict):
    p = theta_circ(p_dict) * p_dict['d'] * 0.5
    return p

def r_circ(p_dict):
    r = area_circ(p_dict) / p_circ(p_dict)
    return r
    
def theta_circ(p_dict):
    return 2.0 * math.acos(1.0 - (2.0*(p_dict['y']/p_dict['d'])))

def f_circ(p_dict):
    try:
        return p_dict['v'] / (p_dict['g'] * dh_circ(p_dict))**0.5
    except:
        v = p_dict['Q'] / area_circ(p_dict)
        return v / (p_dict['g'] * dh_circ(p_dict))**0.5

def yc_circ(p_dict):    
    r = 1.0e+20
    yc = -999
    for y in p_dict['Y']:
        p_dict['y'] = y
        #this_val = (p_dict['Q']**2 * width_circ(p_dict)) / (p_dict['g'] * area_circ(p_dict)**3)       
        this_f = f_circ(p_dict)
        this_r = abs(this_f - 1.0)
        if this_r < r:
            r = this_r
            yc = y
    return yc 

def m_circ(p_dict):
    theta = theta_circ(p_dict)
    term1 = 3.0 * math.sin(theta/2.0)
    term2 = (math.sin(theta/2.0))**3
    term3 = 3.0 * (theta/2.0) * (math.cos(theta/2.0))
    term4 = (p_dict['d']**3)/24.0
    term5 = p_dict['Q']**2 / (((p_dict['g']*(p_dict['d']**2)) * (theta - math.sin(theta))) / 8.0)
    m = ((term1 - term2 - term3) * term4) + term5
    return m

def e_circ(p_dict):
    term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * area_circ(p_dict)**2)
    return p_dict['y'] + term2


def re_circ(p_dict):
    try:
        re = (p_dict['v'] * 4.0 * r_circ(p_dict)) / p_dict['u']
        return re
    except:
        v = p_dict['Q'] / area_circ(p_dict)
        re = (v * 4.0 * r_circ(p_dict)) / p_dict['u']
        return re

def y0_circ(p_dict):
    rhs = (p_dict['n'] * p_dict['Q']) / (p_dict['kn'] * (p_dict['s']**0.5))  
    r = 1.0e+20
    correct_y0 = -999    
    for y in p_dict['Y']:
        p_dict['y'] = y
        lhs = (area_circ(p_dict)**(5.0/3.0)) /  (p_area(p_dict)**(2.0/3.0))
        this_r = abs(lhs-rhs)
        if this_r < r:
            r = this_r
            correct_y0 = y
    #print correct_y0
    if correct_y0 == p_dict['Y'][-1] or correct_y0 == p_dict['Y'][0]:
        print 'Y does not bracket solution'
        raise IndexError
        
    return correct_y0



#-----------------------------------------------------------
#--triangular section
def dh_tri(p_dict):
    area = area_tri(p_dict)
    width = 2.0 * p_dict['m'] * p_dict['y']
    dh = area / width
    return dh      

def area_tri(p_dict):
    return p_dict['m'] * p_dict['y']**2

def width_tri(p_dict):
    return 2.0 * p_dict['m'] * p_dict['y']

def p_tri(p_dict):
    p = 2.0 * p_dict['y'] * (1 + p_dict['m']**2)**0.5
    return p
    
def r_tri(p_dict):
    r = area_tri(p_dict) / p_tri(p_dict)
    return r    

def f_tri(p_dict):
    try:
        return p_dict['v'] / (p_dict['g'] * dh_tri(p_dict))**0.5
    except:                       
        #print area_tri(p_dict),dh_tri(p_dict)
        v = p_dict['Q'] / area_tri(p_dict)
        return v / (p_dict['g'] * dh_tri(p_dict))**0.5

def yc_tri(p_dict):    
    r = 1.0e+20
    yc = -999
    for y in p_dict['Y']:
        p_dict['y'] = y
        this_val = (p_dict['Q']**2 * width_tri(p_dict)) / (p_dict['g'] * area_tri(p_dict)**3)

        this_r = abs(this_val - 1.0)
        if this_r < r:
            r = this_r
            yc = y
    return yc 

def m_tri(p_dict):
    term1 = (p_dict['m'] * p_dict['y']**3) / 3.0
    term2 = p_dict['Q']**2 / (p_dict['g'] * p_dict['m'] * p_dict['y']**2)
    m = term1 + term2
    return m

def e_tri(p_dict):
    term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * area_tri(p_dict)**2)
    return p_dict['y'] + term2

def re_tri(p_dict):
    try:
        re = (p_dict['v'] * 4.0 * r_tri(p_dict)) / p_dict['u']
        return re
    except:
        v = p_dict['Q'] / area_tri(p_dict)
        re = (v * 4.0 * r_tri(p_dict)) / p_dict['u']
        return re

def y0_tri(p_dict):
    rhs = (p_dict['n'] * p_dict['Q']) / (p_dict['kn'] * (p_dict['s']**0.5))  
    r = 1.0e+20
    correct_y0 = -999    
    for y in p_dict['Y']:
        p_dict['y'] = y
        lhs = (area_tri(p_dict)**(5.0/3.0)) /  (p_tri(p_dict)**(2.0/3.0))
        this_r = abs(lhs-rhs)
        if this_r < r:
            r = this_r
            correct_y0 = y
    #print correct_y0
    if correct_y0 == p_dict['Y'][-1] or correct_y0 == p_dict['Y'][0]:
        print 'Y does not bracket solution'
        raise IndexError
        
    return correct_y0



#-----------------------------------------------------------
#--parabolic section
def dh_para(p_dict):    
    area = area_para(p_dict)
    width = width_para(p_dict)
    dh = area/width
    return dh
 
def area_para(p_dict):
    return (2.0/3.0) * p_dict['b'] * p_dict['y']    
    
def width_para(p_dict):
    return p_dict['b'] * (p_dict['y']/p_dict['y1'])**0.5

def x_para(p_dict):
    return 4.0 * p_dict['y'] / p_dict['b']
    
def p_para(p_dict):
    p_dict['x'] = x_para(p_dict)
    term1 = p_dict['b'] / 2.0
    term2 = (1.0 + p_dict['x']**2)**0.5
    term3 = (1.0/p_dict['x'])
    term4 = math.log(p_dict['x'] + (1.0 + p_dict['x']**2)**0.5)    
    p = term1 * (term2 + (term3 * term4))
    return p 
    
def f_para(p_dict):
    try:
        return p_dict['v'] / (p_dict['g'] * dh_para(p_dict))**0.5
    except:
        v = p_dict['Q'] / area_para(p_dict)
        return v / (p_dict['g'] * dh_para(p_dict))**0.5
    
def yc_para(p_dict):    
    r = 1.0e+20
    yc = -999
    for y in p_dict['Y']:
        p_dict['y'] = y
        #this_val = (p_dict['Q']**2 * width_para(p_dict)) / (p_dict['g'] * area_para(p_dict)**3)        
        this_f = f_para(p_dict)
        this_r = abs(this_f - 1.0)
        if this_r < r:
            r = this_r
            yc = y
    return yc 

def m_para(p_dict):
    sigma = sigma_para(p_dict)
    term1 = (4.0/15.0) * sigma * y**(5.0/2.0)
    term2 = 1.5 * p_dict['Q']**2 / (p_dict['g'] * sigma * p_dict['y']**(3.0/2.0))
    m = term1 + term2
    
def calc_sigma(p_dict):
    return p_dict['b'] / (p_dict['y']**0.5)

def e_para(p_dict):
    term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * area_para(p_dict)**2)
    return p_dict['y'] + term2    
    

def re_para(p_dict):
    try:
        re = (p_dict['v'] * 4.0 * r_para(p_dict)) / p_dict['u']
        return re
    except:
        v = p_dict['Q'] / area_para(p_dict)
        re = (v * 4.0 * r_para(p_dict)) / p_dict['u']
        return re

def y0_para(p_dict):
    rhs = (p_dict['n'] * p_dict['Q']) / (p_dict['kn'] * (p_dict['s']**0.5))  
    r = 1.0e+20
    correct_y0 = -999    
    for y in p_dict['Y']:
        p_dict['y'] = y
        lhs = (area_para(p_dict)**(5.0/3.0)) /  (p_para(p_dict)**(2.0/3.0))
        this_r = abs(lhs-rhs)
        if this_r < r:
            r = this_r
            correct_y0 = y
    #print correct_y0
    if correct_y0 == p_dict['Y'][-1] or correct_y0 == p_dict['Y'][0]:
        print 'Y does not bracket solution'
        raise IndexError
        
    return correct_y0
    
    
    
    