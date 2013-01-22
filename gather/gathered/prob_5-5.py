import sys
import math
import numpy as np
import pylab
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 9.81
p_dict['b'] = 6.1
p_dict['Q'] = 17.0
p_dict['n'] = 0.014
p_dict['s'] = 0.001
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
end = rect.yc()*1.001
Y_m3 = np.linspace(start,end,200)

m3_results = rect.direct_step(Y_m3)
#for x,y in zip(m3_results[0],Y_m3):
#    print x,y   


#--M2 curve from free overfall to HJ
start = rect.yc()*1.001
end = rect.y0()*0.999
Y_m2 = np.linspace(start,end,200)
m2_results = rect.direct_step(Y_m2)
#for x,y in zip(m2_results[0],Y_m2):
#    print x,y   

#sys.exit()

m2_results[0] += 300.0 

#Y_m2 += m2_results[0] * p_dict['s']
#Y_m3 += m3_results[0] * p_dict['s']
 

#--load curves from wsp
m2_wsp = np.loadtxt('p5-5_m2.txt',skiprows=8,delimiter=',')
m3_wsp = np.loadtxt('p5-5_m3.txt',skiprows=8,delimiter=',')

fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
ax.plot(m2_results[0],m2_results[-1],'g-',label='M2')         
ax.plot(m3_results[0],m3_results[-1],'b-',label='M1')
ax.plot(m2_wsp[:,0],m2_wsp[:,-1],'go',label='WSP M2')
ax.plot(m3_wsp[:,0],m3_wsp[:,-1],'bo',label='WSP M3')
ax.set_xlim(0,300.0)

m2_results[0] = np.ma.masked_where(m2_results[0]<59,m2_results[0])
m3_results[0] = np.ma.masked_where(m3_results[0]>53,m3_results[0])
#m2_wsp[:,0] = np.ma.masked_where(m2_wsp[:,0]<56,m2_wsp[:,0])
#m3_wsp[:,0] = np.ma.masked_where(m3_wsp[:,0]>56,m3_wsp[:,0])
#m2_wsp[:,1] = np.ma.masked_where(m2_wsp[:,0]<56,m2_wsp[:,1])
#m3_wsp[:,1] = np.ma.masked_where(m3_wsp[:,0]>56,m3_wsp[:,1])

idx = np.argwhere(m2_wsp[:,0]<59)
m2_wsp = np.delete(m2_wsp,idx,0)
idx = np.argwhere(m3_wsp[:,0]>53)
m3_wsp = np.delete(m3_wsp,idx,0)

idx = np.argmin(m2_results[0])
m2_xmin = m2_results[0][idx]
m2_ymin = Y_m2[idx]
idx = np.argmax(m3_results[0])
m3_ymax = Y_m3[idx]
m3_xmax = m3_results[0][idx]

jump_shift = Y_m2[idx]*5.5
#m2_results[0] += jump_shif

ax2.plot(m2_results[0],Y_m2,'g-')         
ax2.plot(m3_results[0],Y_m3,'b-')
ax2.plot(m2_wsp[:,0],m2_wsp[:,1],'go')
ax2.plot(m3_wsp[:,0],m3_wsp[:,1],'bo')
ax2.plot([m2_xmin,m3_xmax],[m2_ymin,m3_ymax],'r--',lw=5.5,label='hydraulic jump')    
    
ax2.plot([0,300],[y0,y0],'k-')         
ax2.set_xlim(0,300.0)
ax2.plot([0,300.0],[y0,y0],'k-',label='normal depth')
ax2.plot([0,300.0],[yc,yc],'k--',label='critical depth')
ax.set_ylabel('momentum')
ax2.set_ylabel('water surface profile (ft)')
ax2.set_xlabel('distance (ft)')
ax.set_xlabel('distance (ft)') 
ax.legend()
ax2.legend(loc=4)
pylab.show()