import numpy as np
import pylab


def calc_e(y,q):
    g = 32.2
    e = np.zeros_like(y)
    for y_idx in range(y.shape[0]):
        e[y_idx] = y[y_idx] + ((q**2)/(2.0*g*(y[y_idx]**2)))
    return e

def find_idxs(arr,value,thres): 
    #print thres,arr.shape    
    thres_idx = np.argwhere(arr==thres)
    idx1=(np.abs(arr[:thres_idx]-value)).argmin()    
    idx2= thres_idx[0][0]+1 + (np.abs(arr[thres_idx:]-value)).argmin() 
    #print idx1,idx2,value,thres,arr[idx1],arr[idx2]   
    #print arr   
    return np.array([idx1,idx2])                     



y = np.arange(0.001,10.0,0.0001)
q1 = 1.0
e1 = calc_e(y,q1)

q2 = 2.0
e2 = calc_e(y,q2)

q3 = 3.0
e3 = calc_e(y,q3)

e1_min,e2_min,e3_min = e1.min(),e2.min(),e3.min()
y1_min = y[np.where(e1==e1_min)][0]
y2_min = y[np.where(e2==e2_min)][0]
y3_min = y[np.where(e3==e3_min)][0]

e_vals = [0.8,1.0,2.0,5.0]
print y1_min,y2_min,y3_min

fig = pylab.figure()
ax = pylab.subplot(1,1,1)
ax.plot(e1,y,'b-',label='q=1.0',lw=2.0)
ax.plot(e2,y,'r-',label='q=2.0',lw=2.0)
ax.plot(e3,y,'g-',label='q=3.0',lw=2.0)
ax.plot((0,e1_min,e1_min),(y1_min,y1_min,0),'b--',lw=2.0)
ax.plot((0,e2_min,e2_min),(y2_min,y2_min,0),'r--',lw=2.0)
ax.plot((0,e3_min,e3_min),(y3_min,y3_min,0),'g--',lw=2.0)




f_out = open('alternate_depths.dat','w')
f_out.write('Specific_Discharge,Critical_Energy,Critical_Depth,Specific_Energy,Supercritical_Depth,Subcritical_Depth\n')
f_out.write('(ft/sec),(ft),(ft),(ft),(ft),(ft)\n')
for e in e_vals:
    y1 = y[find_idxs(e1,e,e1_min)]   
    y2 = y[find_idxs(e2,e,e2_min)]
    y3 = y[find_idxs(e3,e,e3_min)] 
    
    #print e,e1_min,y1,e2_min,y2,e3_min,y3
    ax.plot((e,e),(0,6),'k--')         
    if e >= e1_min:
        f_out.write('1.0,'+str(e1_min)+','+str(y1_min)+','+str(e)+','+str(y1[0])+','+str(y1[1])+'\n')
    if e >= e2_min:
        f_out.write('2.0,'+str(e2_min)+','+str(y2_min)+','+str(e)+','+str(y2[0])+','+str(y2[1])+'\n')
    if e >= e3_min:
        f_out.write('3.0,'+str(e3_min)+','+str(y3_min)+','+str(e)+','+str(y3[0])+','+str(y3[1])+'\n')
    else:
        f_out.write('3.0,'+str(e3_min)+','+str(y3_min)+','+str(e)+',minimum energy greater than '+str(e)+'\n')


ax.plot(y,y,'k--',lw=2.0)
ax.set_xlim(0,6)
ax.set_ylim(0,6)
ax.set_ylabel('flow depth (ft)')
ax.set_xlabel('specific energy (ft)')
#ax.set_xticks(e_vals)
#ax.set_xticklabels(e_vals)
ax.legend()
pylab.show()

        