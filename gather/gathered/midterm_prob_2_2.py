import sys
import numpy as np
import calc_prism as cp

p_rect = {}
p_rect['b']= 20.0 #ft
p_rect['Q']= 240.0 #cfs

p_rect['g'] = 9.81 #ft/sec2
p_rect['q'] = p_rect['Q'] / p_rect['b']


tw = 95.5 #ft
h_lake = 110.0
coeff_d = 0.5
area = 2.0
rho = 1.0

z = 88.8


Z = np.arange(80,95,0.01)
#Z = np.array([64.5])
Y1 = np.arange(0,5,0.01)
min_tw_resid = 1.0e+20
correct_z = -999
correct_y1 = -999
correct_f1 = -999
for z in Z:
    #--find y1
    min_z_resid = 1.0e+20
    y1 = -999
    for this_y1 in Y1:
        p_rect['y'] = this_y1
        this_f1 = cp.f_rect(p_rect)
        
        h_loss = k_loss * (h_lake - z - this_y1)
        this_z = h_lake - cp.e_rect(p_rect) - h_loss
        #print this_z
        if abs(this_z-z) < min_z_resid:
            y1 = this_y1
            min_z_resid = abs(this_z-z)
            f1 = this_f1
    #print y1
    #--set y as the correct y1
    p_rect['y'] = y1
    f1 = cp.f_rect(p_rect)    
    f1_sq = f1**2
    y2 = (y1 * 0.5) * ((1.0 + (8.0*f1_sq))**0.5 - 1.0)
    this_tw = y2 + z
    #print this_tw
    if abs(this_tw-tw) < min_tw_resid:
        correct_z = z
        correct_y1 = y1
        correct_y2 = y2
        correct_f1 = f1
        min_tw_resid = abs(this_tw-tw)


print 'z,y1,y2',correct_z,correct_y1,correct_y2
print 'f1',correct_f1
if correct_y1 == Y1[0] or correct_y1 == Y1[-1]:
    print 'warning y1 not bracketing...'

if correct_z == Z[0] or correct_z == Z[-1]:
    print 'warning z not bracketing...'
    
v = p_rect['q'] / correct_y1
print 'v',v    
D = coeff_d * rho * (v**2) / 2.0    



        
     
            
     