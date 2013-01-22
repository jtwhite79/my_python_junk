import math
import numpy as np
import pylab

import calc_prism as cp     
 
#--tri params    
p_dict = {}   
p_dict['y'] = 1.12 
p_dict['Q'] = 60.0
p_dict['g'] = 32.2

m = cp.m_tri(p_dict)
print 'approach momentum: ',m

#--find conjugates
y = np.arange(0.1,1.0,0.00001)
conj_c = cp.find_depths(m,y,p_dict,cp.m_tri)
conj_c = y[find_conjugate_idxs(mc,mc1,mc_min)]  
print conj_c

fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(mc,y,'b-',lw=2.0)    
ax.plot((mc1,mc1),conj_c,'bo')
ax.plot((mc1,mc1),conj_c,'b--')

xmin,xmax = ax.get_xlim()
ax.plot((xmin,mc1),(conj_c[0],conj_c[0]),'b--')
ax.plot((xmin,mc1),(conj_c[1],conj_c[1]),'b--')

ax.text(0.1,0.95,'sequent depths:{0:3.2f} {1:3.2f}'.format(conj_c[0],conj_c[1]),color='b')
#ax.legend()
pylab.show()