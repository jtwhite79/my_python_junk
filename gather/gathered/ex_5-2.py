import sys
import math
import numpy as np
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 8.0
p_dict['m'] = 2.0
p_dict['Q'] = 30.0
n = 0.025
s = 0.001
kn = 1.0

p_dict['n'] = n
p_dict['s'] = s
p_dict['kn'] = kn

p_dict['Y'] = np.arange(0.001,10.0,0.001)

trap = cpc.trap(p_dict)

#--normal depth
y0 = trap.y0()
print y0

#--critical depth
yc = trap.yc()
print yc

start = trap.yc()*1.005
end = trap.y0()*0.995
Y = np.linspace(start,end,20)

X,V,Se,E,DeltaE,DeltaX = trap.direct_step(Y)
for x,y in zip(X,Y):
    print x,y   
