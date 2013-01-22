import numpy as np
import calc_prism as cp


def e_rect_with_z(p_dict):
    
    
    term2 = p_dict['q']**2 / (2.0 * p_dict['g'] * ((p_dict['y_base']-p_dict['z'])**2))
    return p_dict['y_base'] + term2 - p_dict['z']



def find_z(target,z_array,p_dict,function):
    
    #--calculate the residuals
    rs = np.zeros_like(z_array)
    mins = []
    for idx in range(z_array.shape[0]):
        #--calc this_e
        p_dict['z'] = z_array[idx]
         
        this_val = function(p_dict)
        #--calc this residual
        this_r = abs(this_val - target)
        rs[idx] = this_r
        
    #--loop over the residuals looking for minimums
    mins = []
    for idx in range(1,rs.shape[0]-1):
        if rs[idx] < rs[idx-1] and rs[idx] < rs[idx+1]:
            mins.append(idx)
    
    return z_array[mins]



z = np.arange(0.0001,2.0,0.0001)

target_e = 0.551 #from problem 1

p_rect = {}
p_rect['b'] = 1.0
p_rect['g'] = 9.81
p_rect['Q'] = 1.0
p_rect['q'] = p_rect['Q'] / p_rect['b']
p_rect['y_base'] = 0.5

delta_z = find_z(target_e,z,p_rect,e_rect_with_z)
print delta_z
p_rect['y'] = p_rect['y_base'] + delta_z

print cp.e_rect(p_rect)
