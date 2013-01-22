import sys
import math
import numpy as np
import pylab
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 10.0
p_dict['Q'] = 101.0
p_dict['n'] = 0.03
p_dict['s'] = 0.005
p_dict['kn'] = 1.0

p_dict['Y'] = np.arange(0.001,10.0,0.001)

rect = cpc.rect(p_dict)

#--normal depth
y0 = rect.y0()

#--critical depth
yc = rect.yc()
print 'y0,yc',y0,yc


#--M3 curve from gate to HJ
start = 0.47
end = rect.yc()*1.005
Y_m3 = np.linspace(start,end,200)

m3_results = rect.direct_step(Y_m3)
#for x,y in zip(m3_results[0],Y_m3):
#    print x,y   


#--M2 curve from free overfall to HJ
start = rect.yc()*1.005
end = rect.y0()*0.995
Y_m2 = np.linspace(start,end,20)
m2_results = rect.direct_step(Y_m2)
#for x,y in zip(m2_results[0],Y_m2):
#    print x,y   

#sys.exit()

m2_results[0] += 300.0 #+ m3_results[0][-1]
#--find the X where the momentum functions are equal
r = 1.0e+20
correct_x_m2 = -1.0e+20
correct_x_m3 = -1.0e+20
for m3_x,m3_m in zip(m3_results[0],m3_results[-1]):
    for m2_x,m2_m in zip(m2_results[0],m2_results[-1]):    
        this_r = abs(m2_m - m3_m)
        
        if this_r < r and m2_x != 0:
            print this_r,m2_x,m3_x,m2_m,m3_m
            r = this_r
            correct_m2 = m2_x
            correct_m3 = m3_x 
print correct_m2,correct_m3,r   

fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
ax.plot(m2_results[0],m2_results[-1],'g-')         
ax.plot(m3_results[0],m3_results[-1],'b-')
ax.set_xlim(0,300.0)
ax2.plot(m2_results[0],Y_m2,'g-')         
ax2.plot(m3_results[0],Y_m3,'b-')
ax2.plot([0,300],[y0,y0],'k-')         
ax2.set_xlim(0,300.0)
ax2.plot([0,300.0],[y0,y0],'k-')
ax2.plot([0,300.0],[yc,yc],'k--')
pylab.show()