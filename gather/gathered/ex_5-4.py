import sys
import math
import copy
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

#--steep
s_dict = copy.deepcopy(p_dict)
s_dict['s'] = 0.02

rect_s = cpc.rect(s_dict)
#--normal depth
y0_s = rect_s.y0()
#--critical depth
yc_s = rect_s.yc()
print 'y0_s,yc_s',y0_s,yc_s

tw = 5.0

#--m2 from slope break upstream on mild slope
start = yc*1.005
end = y0*0.995
Y_m2 = np.linspace(start,end,200)
m2_results = rect.direct_step(Y_m2)


#--s2 from break downstream on steep slope
start = yc*0.999
end = y0_s*1.001
Y_s2 = np.linspace(start,end,200)
s2_results = rect_s.direct_step(Y_s2)


#--s1 from TW upstream
start = tw
end = yc*1.001
Y_s1 = np.linspace(start,end,200)
s1_results = rect_s.direct_step(Y_s1)

s1_results[0] += 700.0
s2_results[0] += 500.0
fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
ax.plot(s2_results[0],s2_results[-1],'g-')         
ax.plot(s1_results[0],s1_results[-1],'b-')
ax2.plot(s2_results[0],Y_s2,'g-')         
ax2.plot(s1_results[0],Y_s1,'b-')
#ax2.plot([0,300],[y0,y0],'k-')         
#ax2.plot([0,300.0],[y0,y0],'k-')
#ax2.plot([0,300.0],[yc,yc],'k--')
pylab.show()