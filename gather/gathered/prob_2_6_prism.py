import numpy as np

import calc_prism as cp
#--brought over from calc_prism to include headloss
#--area2 is the area of the "other" section needed for headloss calc
def e_rect_mod(p_dict):
    
    
    head_loss = (abs((1.0/p_dict['area2']**2) -
                (1.0/cp.area_rect(p_dict)**2)) * \
                ((p_dict['Q']**2)/(2.0 * p_dict['g'])))
    head_loss *= p_dict['k_loss']
    #print p_dict['y'],head_loss   
    term2 = (p_dict['Q']**2) / (2.0 * p_dict['g'] * cp.area_rect(p_dict)**2)
    return p_dict['y'] + term2 - head_loss
    



p_rect = {}
p_rect['g'] = 32.2
p_rect['b'] = 49.0
p_rect['Q'] = 12600.0

p_trap = {}
p_trap['g'] = 32.2
p_trap['m'] = 2.0
p_trap['b'] = 75.0
p_trap['Q'] = 12600.0
p_trap['y'] = 22.0

delta_z = 1.0
k_loss = 0.5

#--energy downstream
e_trap = cp.e_trap(p_trap)        
print e_trap
#--energy upstream = e_dwn + delta_z + head_loss
e_trap -= delta_z

#--add parameters to p_rect for depth finding
p_rect['area2'] = cp.area_trap(p_trap)
p_rect['k_loss'] = k_loss



y = np.arange(0.001,100.0,0.001)
#y = np.array([19.88])
alt_depths = cp.find_depths(e_trap,y,p_rect,e_rect_mod)
print alt_depths

