import sys
import math
import numpy as np
import pylab
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 32.2
p_dict['b'] = 20.0
p_dict['m'] = 2.0
p_dict['n'] = 0.045
p_dict['s'] = 0.0005
p_dict['kn'] = 1.49

p_dict['Y'] = np.arange(0.01,20.0,0.01)
trap = cpc.trap(p_dict)
dist = 10000.0
H_res = 10.0
r = 1.0e+20
correct_head = -999
correct_y0 = -999
correct_yc = -999

correct_Q = -999
trap.add_key('Q')
Q = np.arange(500.0,1000.0,1.0)
for q in Q:
    trap.set('Q',q)
    yc = trap.yc()    
    y0 = trap.y0()
    #print q,yc,y0
    start = yc*1.001
    end = y0*0.999
    Y_m2 = np.linspace(start,end,1000)
    results_m2 = trap.direct_step(Y_m2)
    #print results_m2[0]
    
    #--account for free overfall
    #results_m2[0] += yc*4.0
    #--find the nearest point to the upstream res  
    diff = np.abs(np.abs(results_m2[0]) - dist)
    idx = np.argmin(diff)
    y = Y_m2[idx]
    v = results_m2[1][idx]
    v_head = v**2 / (2.0*p_dict['g'])
    head = y + v_head 
    #print idx
    #print 'Q,yc,y0,y,head,x',q,yc,y0,y,head,results_m2[0][idx]   
    #break
    this_r= np.abs(head - H_res)
    if this_r < r:
        r = this_r
        correct_Q = q
        correct_yc = yc
        correct_y0 = y0
        correct_head = head
print 'r',r
print 'Q,yc,y0,head',correct_Q,correct_yc,correct_y0,correct_head  
    
    #r_h = 1.0e+20
    #correct_Q_temp = ((H_res - y)*(2.0*p_dict['g']*(trap.area()**2)))**0.5     
    #trap.set('Q',correct_Q_temp)
    #f = trap.f()    
    ##print y,f,correct_Q_temp,r_h
    #if abs(f-1.0) < r_f:
    #    r_f = abs(f-1.0)
    #    correct_y = y
    #    correct_f = f
    #    correct_Q = correct_Q_temp    
    #this_r_f = abs(f - 1.0) 
    #break 

trap.rm_key('Q')

sys.exit()
print 'y,f,Q,r_f',correct_y,correct_f,correct_Q,r_f
trap.rm_key('y')
trap.set('Q',correct_Q)

#--normal depth
y0 = trap.y0()

#--critical depth
yc = trap.yc()

print 'y0,yc',y0,yc

#--critical slope
trap.add_key('y',val=yc)
so_crit = trap.sc()
print 'critical slope:',so_crit
trap.rm_key('y')

#--next get the curves
num_points = 20

#--S1 curve from downstream res to upstream to HJ
start = 8.0
end = trap.yc()*1.001 
Y_s1d = np.linspace(start,end,num_points)
s1d_results = trap.direct_step(Y_s1d)
#for x,y in zip(s1d_results[0],Y_s1d):
#    print x,y   
#sys.exit()

