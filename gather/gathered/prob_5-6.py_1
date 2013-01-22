import sys
import math
import numpy as np
import pylab
import calc_prism_class as cpc

    
p_dict = {}
p_dict['g'] = 32.2
p_dict['b'] = 10.0
p_dict['m'] = 3.0
p_dict['n'] = 0.015
p_dict['s'] = 0.01
p_dict['kn'] = 1.49

p_dict['Y'] = np.arange(0.001,20.0,0.001)
trap = cpc.trap(p_dict)

#--------------
#--first find Q
H_res = 8.0
r_f = 1.0e+20
correct_y = -999
correct_f = -999
correct_Q = -999
trap.add_key('y')
trap.add_key('Q')
for y in np.arange(0.001,H_res,0.001):
    trap.set('y',y)    
    r_h = 1.0e+20
    correct_Q_temp = ((H_res - y)*(2.0*p_dict['g']*(trap.area()**2)))**0.5     
    trap.set('Q',correct_Q_temp)
    f = trap.f()    
    #print y,f,correct_Q_temp,r_h
    if abs(f-1.0) < r_f:
        r_f = abs(f-1.0)
        correct_y = y
        correct_f = f
        correct_Q = correct_Q_temp    
    #this_r_f = abs(f - 1.0) 
    #break 

print 'y,f,Q,r_f',correct_y,correct_f,correct_Q,r_f
trap.rm_key('y')
trap.set('Q',correct_Q)
#print trap.p_dict
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


#-----------------
#--next find gate opening with momentum
trap.add_key('y',10.0)
e_upGate = trap.e()
trap.rm_key('y')
alt_depths = trap.find_depths(e_upGate,trap.e)
gate_opening = alt_depths.min()
print 'gate',gate_opening
#sys.exit()
#--next get the curves
num_points = 200

#--S2 curve from upstream inlet (yc) downstream to y0
start= yc*0.999
end = y0*1.001

Y_s2 = np.linspace(end,start,num_points)
s2_results = trap.direct_step(Y_s2)
#for x,y in zip(s2_results[0],Y_s2):
#    print x,y   


#--s1 curve from upstream HJ to gate
start = 10.0
end = yc*1.001
Y_s1u = np.linspace(start,end,num_points)

s1u_results = trap.direct_step(Y_s1u)
#for x,y in zip(s1u_results[0],Y_s1u):
#    print x,y   


#--S3 curve from gate to normal depth
start = gate_opening
end = trap.y0()*0.999
Y_s3 = np.linspace(start,end,num_points)
s3_results = trap.direct_step(Y_s3)
#for x,y in zip(s3_results[0],Y_s3):
#    print x,y   

#--S1 curve from downstream res to upstream to HJ
start = 15.0
end = trap.yc()*1.001 
Y_s1d = np.linspace(start,end,num_points)
s1d_results = trap.direct_step(Y_s1d)
#for x,y in zip(s1d_results[0],Y_s1d):
#    print x,y   
#sys.exit()

#--plot to look from HJ downstream of gate
s2_results[0] -= 1000.0
s1d_results[0] += 1000.0

#Y_s1d -= s1d_results[0] * p_dict['s']
#Y_s1u -= s1u_results[0] * p_dict['s']
#Y_s3 -= s3_results[0] * p_dict['s']
#Y_s2 -= s2_results[0] * p_dict['s']
#Y_s3 -= yc
s1d_results[0] += 1000.0
s3_results[0] += 1000.0  
s1u_results[0] += 1000.0 
s2_results[0] += 1000.0

#--load the wsp results
s1d_wsp = np.loadtxt('p5-6_s1d_full.txt',skiprows=8,delimiter=',')
s1u_wsp = np.loadtxt('p5-6_s1u_full.txt',skiprows=8,delimiter=',')
s2_wsp = np.loadtxt('p5-6_s2_full.txt',skiprows=8,delimiter=',')
s3_wsp = np.loadtxt('p5-6_s3_full.txt',skiprows=8,delimiter=',')



#x_line = np.arange(-1000,1000.0,1.0) 
#y0_line = y0 - (x_line * p_dict['s'])
#yc_line = yc - (x_line * p_dict['s'])
#x_line += 1000.0
fig = pylab.figure()
ax = pylab.subplot(211)
ax2 = pylab.subplot(212)
#ax.plot(s1d_results[0],s1d_results[-1],'g-')         
#ax.plot(s3_results[0],s3_results[-1],'b-')
#ax.plot(s1u_results[0],s1u_results[-1],'r-')
#ax.plot(s2_results[0],s2_results[-1],'r--')
#ax.plot(s1d_wsp[:,0]+1000,s1d_wsp[:,-1],'go')
#ax.plot(s1u_wsp[:,0],s1u_wsp[:,-1],'ro')
#ax.plot(s2_wsp[:,0],s2_wsp[:,-1],'r+')
#ax.plot(s3_wsp[:,0]+1000,s3_wsp[:,-1],'bo')
ax.plot(s1d_wsp[:,0]+1000,s1d_wsp[:,-1],'g-',label='s1_dwstr',lw=1.5)
ax.plot(s1u_wsp[:,0],s1u_wsp[:,-1],'m-',label='s1_upstr',lw=1.5)
ax.plot(s2_wsp[:,0],s2_wsp[:,-1],'c-',label='s2',lw=1.5)
ax.plot(s3_wsp[:,0]+1000,s3_wsp[:,-1],'b-',label='s3',lw=1.5)
ax.set_xlim(0,2000)

#--deal with jumps
up_x = 850
dw_x = 1430

s1d_wsp = np.loadtxt('p5-6_s1d.txt',skiprows=8,delimiter=',')
s1u_wsp = np.loadtxt('p5-6_s1u.txt',skiprows=8,delimiter=',')
s2_wsp = np.loadtxt('p5-6_s2.txt',skiprows=8,delimiter=',')
s3_wsp = np.loadtxt('p5-6_s3.txt',skiprows=8,delimiter=',')
s1d_wsp[:,0] += 1400
s3_wsp[:,0] += 1000








#s1u_wsp[:,0] = np.ma.masked_where(s1u_wsp[:,0]<up_x,s1u_wsp[:,0])
idx = np.argwhere(s1u_wsp[:,0]<875)
s1u_wsp = np.delete(s1u_wsp,idx,0)
idx = np.argwhere(s2_wsp[:,0]>825)
s2_wsp = np.delete(s2_wsp,idx,0)
idx = np.argwhere(s1d_wsp[:,0]<1405)
s1d_wsp = np.delete(s1d_wsp,idx,0)
idx = np.argwhere(s3_wsp[:,0]>1355)
s3_wsp = np.delete(s3_wsp,idx,0)

#--dwstream jump
idx = np.argmin(s1d_wsp[:,0])
s1d_xmin = s1d_wsp[idx,0]
s1d_ymin = s1d_wsp[idx,1]
idx = np.argmax(s3_wsp[:,0])
s3_xmax = s3_wsp[idx,0]
s3_ymax = s3_wsp[idx,1]

#--upstrm jump
idx = np.argmin(s1u_wsp[:,0])
s1u_xmin = s1u_wsp[idx,0]
s1u_ymin = s1u_wsp[idx,1]
idx = np.argmax(s2_wsp[:,0])
s2_xmax = s2_wsp[idx,0]
s2_ymax = s2_wsp[idx,1]

#ax.set_xlim(0,2000.0)
#ax2.plot(s1d_results[0],Y_s1d,'g-')         
#ax2.plot(s1u_results[0],Y_s1u,'r-')         
#ax2.plot(s3_results[0],Y_s3,'b-')
#ax2.plot(s2_results[0],Y_s2,'r--')
#ax2.plot(s1d_wsp[:,0]+1000,s1d_wsp[:,1],'go')
#ax2.plot(s1u_wsp[:,0],s1u_wsp[:,1],'ro')
#ax2.plot(s2_wsp[:,0],s2_wsp[:,1],'r+')
#ax2.plot(s3_wsp[:,0]+1000,s3_wsp[:,1],'bo')
ax2.plot([0,2000.0],[y0,y0],'k-',label='normal depth')
ax2.plot([0,2000.0],[yc,yc],'k--',label='critical depth')
ax2.plot(s1d_wsp[:,0],s1d_wsp[:,1],'g-',lw=1.5)
ax2.plot(s1u_wsp[:,0],s1u_wsp[:,1],'m-',lw=1.5)
ax2.plot(s2_wsp[:,0],s2_wsp[:,1],'c-',lw=1.5)
ax2.plot(s3_wsp[:,0],s3_wsp[:,1],'b-',lw=1.5)
ax2.plot([s3_xmax,s1d_xmin],[s3_ymax,s1d_ymin],'r--',lw=2.5,label='hydraulic jump')    
ax2.plot([s2_xmax,s1u_xmin],[s2_ymax,s1u_ymin],'r--',lw=2.5) 
ax2.plot([1000,1000],[4.24,15],'k-',lw=2.5,label='gate')   
ax2.set_xlabel('distance (ft)')
ax2.set_ylabel('water surface profile')
ax.set_ylabel('momentum')
       
#ax2.set_xlim(0,2000.0)
#ax2.plot([0,2000.0],[y0,y0],'k-',label='normal depth')
#ax2.plot([0,2000.0],[yc,yc],'k--',label='critical depth')
#ax2.plot(x_line,y0_line,'k-.',label='y0')
#ax2.plot(x_line,yc_line,'k--',label='yc')
ax2.legend(loc=2)
ax.legend(loc=2)
pylab.show()