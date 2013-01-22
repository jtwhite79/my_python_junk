import numpy as np


b = 40.0 #ft
Q = 10000.0 #cfs
tw = 100.0 #ft
g = 32.2 #ft/sec2

h_lake = 200.0
k_loss = 0.1

q = Q / b

Z = np.arange(0,100,0.1)
Y1 = np.arange(0,10,0.01)
min_tw_resid = 1.0e+20
correct_z = -999
correct_y1 = -999
for z in Z:
    #--find y1
    min_z_resid = 1.0e+20
    y1 = -999
    for this_y1 in Y1:
        h_loss = k_loss * (q**2/(2.0 * g * this_y1**2))
        this_z = h_lake - this_y1 - (q**2/(2.0 * g * this_y1**2)) - h_loss
        #print this_z
        if abs(this_z-z) < min_z_resid:
            y1 = this_y1
            min_z_resid = abs(this_z-z)
    #print y1
    v1 = q / y1
    f1 = v1 / (g * y1)**0.5
    f1_sq = f1**2
    y2 = (y1 * 0.5) * ((1.0 + (8.0*f1_sq))**0.5 - 1.0)
    this_tw = y2 + z
    #print this_tw
    if abs(this_tw-tw) < min_tw_resid:
        correct_z = z
        correct_y1 = y1
        min_tw_resid = abs(this_tw-tw)


print 'z,y1',correct_z,correct_y1

if correct_y1 == Y1[0] or correct_y1 == Y1[-1]:
    print 'warning y1 not bracketing...'

if correct_z == Z[0] or correct_z == Z[-1]:
    print 'warning z not bracketing...'
    


        
     
            
     